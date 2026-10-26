"""Paper earnings rockets, live, on SYNTHETIC data (no network): detection
uses the research rule, the paper position closes with the research's
trailing exit, and paper results never mix with real ones."""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from app.db import SignalRecord, get_session, init_db
from app.journal import repository as journal
from app.live_rockets import find_rockets, format_rocket_buy
from app.paper_trading.simulator import run_paper_trading_update
from app.rockets import EarningsParams

# This file tests the detection/paper-tracking MECHANICS (saving, closing,
# message formatting), not the current live threshold values — those have
# their own dedicated tests in test_rockets.py — so it uses an explicit,
# deliberately loose EarningsParams rather than the (stricter) live default.
LOOSE = EarningsParams(min_surprise_pct=0.0, min_reaction=0.10)


def _frame(closes, start="2026-01-01", volumes=None):
    closes = np.asarray(closes, float)
    days = pd.bdate_range(start, periods=len(closes))
    ct = (days.tz_localize("America/New_York") + pd.Timedelta(hours=16)).tz_convert("UTC")
    return pd.DataFrame({"open": closes, "high": closes * 1.01, "low": closes * 0.99, "close": closes,
                         "volume": volumes if volumes is not None else np.full(len(closes), 1e6),
                         "close_time": ct, "open_time": ct}).set_index("close_time", drop=False)


class Client:
    def __init__(self, frames):
        self.frames = frames

    def get_klines(self, symbol, interval, limit=500):
        return self.frames[symbol].tail(limit)

    def prefetch(self, *a, **k):
        return {}


@pytest.fixture
def clean_journal():
    init_db()
    with get_session() as s:
        s.query(SignalRecord).delete()
        s.commit()


def test_detects_earnings_rocket_follows_it_on_paper_and_keeps_it_separate(clean_journal):
    base = [20.0] * 40
    rocket = base + [21.0, 22.6]           # report between the last-but-two and last-but-one close: +13% over two sessions
    flat = base + [20.1, 20.2]
    frames = {"RKT": _frame(rocket), "FLT": _frame(flat), "MISS": _frame(rocket)}
    session_close = frames["RKT"]["close_time"].iloc[-1]
    announced = frames["RKT"]["close_time"].iloc[-3] + pd.Timedelta(minutes=30)   # after the close, 2 sessions ago

    def lookup(symbol, before, not_before):
        assert not_before <= announced < before
        return (25.0, announced) if symbol == "RKT" else (-3.0, announced)

    day = find_rockets(Client(frames), ["RKT", "FLT", "MISS"], session_close, params=LOOSE, surprise_lookup=lookup)
    assert [r["symbol"] for r in day.new] == ["RKT"] and day.candidates == 2   # MISS jumped but missed estimates
    msg = format_rocket_buy(day.new[0], None)
    assert msg.startswith("🚀 RAKET (papper — köp inte) — RKT") and "+25%" in msg

    journal.save_rocket_paper(day.new[0], None)
    # Afterwards: opens 23, runs to 30, then closes 25% below the peak (22.5) -> 'sold' at the next open.
    later = rocket + [23.0, 26.0, 30.0, 28.0, 22.0, 21.5] + [21.5] * 5
    frames["RKT"] = _frame(later)
    frames["RKT"].loc[frames["RKT"].index[42], "open"] = 23.0
    frames["RKT"].loc[frames["RKT"].index[47], "open"] = 21.8
    delivered = []
    import app.notify.notifier as notifier
    orig = notifier._deliver
    notifier._deliver = delivered.append
    try:
        update = run_paper_trading_update(client=Client(frames))["updated"]
    finally:
        notifier._deliver = orig
    rkt = next(u for u in update if u["symbol"] == "RKT")
    assert rkt["result"] == "ROCKET_TRAIL" and rkt["fill_price"] == 23.0 and rkt["exit_price"] == pytest.approx(21.8)
    assert any(m.startswith("🚀 RAKET (papper) avslutad — RKT") for m in delivered)
    assert journal.rocket_paper_summary()["n"] == 1
    assert journal.performance_summary()["closed_total"] == 0   # paper never counts as a real result


def test_closed_paper_rocket_gets_its_own_headline():
    from app.daily import _rocket_closed_headline

    assert _rocket_closed_headline([{"symbol": "RKT", "return_pct": 12.4}, {"symbol": "ABC", "return_pct": -8.0}]) == \
        "🚀 avslutad (papper) RKT +12%, ABC -8%"


def test_find_rockets_requires_volume_confirmation_when_configured():
    base = [20.0] * 40
    rocket = base + [21.0, 22.6]
    flat_vol = np.full(42, 1e6)
    frames = {"RKT": _frame(rocket, volumes=flat_vol)}
    session_close = frames["RKT"]["close_time"].iloc[-1]
    announced = frames["RKT"]["close_time"].iloc[-3] + pd.Timedelta(minutes=30)
    lookup = lambda symbol, before, not_before: (25.0, announced)
    strict_vol = EarningsParams(min_surprise_pct=0.0, min_reaction=0.10, min_volume_ratio=2.0)

    day = find_rockets(Client(frames), ["RKT"], session_close, params=strict_vol, surprise_lookup=lookup)
    assert day.new == []   # flat volume -> no confirmation, never reaches the earnings lookup

    confirmed_vol = flat_vol.copy()
    confirmed_vol[41] = 3e6   # the second reaction session trades at 3x normal volume
    frames["RKT"] = _frame(rocket, volumes=confirmed_vol)
    day = find_rockets(Client(frames), ["RKT"], session_close, params=strict_vol, surprise_lookup=lookup)
    assert [r["symbol"] for r in day.new] == ["RKT"]


def test_find_rockets_requires_relative_strength_when_configured():
    from app.rotation import RS_LOOKBACK

    n = RS_LOOKBACK + 42
    strong = np.concatenate([np.linspace(100, 150, n - 2), [160.0, 180.0]])   # big 6-month run, then a rocket day
    weak = np.linspace(100, 105, n)                                           # flat 6-month return
    frames = {"RKT": _frame(strong), "WEAK": _frame(weak)}
    session_close = frames["RKT"]["close_time"].iloc[-1]
    announced = frames["RKT"]["close_time"].iloc[-3] + pd.Timedelta(minutes=30)
    lookup = lambda symbol, before, not_before: (25.0, announced)
    strict_rs = EarningsParams(min_surprise_pct=0.0, min_reaction=0.10, min_rs=0.8)

    # Among just these two, RKT (the strong 6-month performer) clears a top-20% bar; a short-history
    # symbol with no computable RS is never guessed into passing.
    day = find_rockets(Client(frames), ["RKT", "WEAK"], session_close, params=strict_rs, surprise_lookup=lookup)
    assert [r["symbol"] for r in day.new] == ["RKT"]

    short_history = {"RKT": _frame(np.concatenate([[100.0] * 30, [100.0] * 8, [110.0, 125.0]]))}
    day = find_rockets(Client(short_history), ["RKT"], short_history["RKT"]["close_time"].iloc[-1],
                       params=strict_rs, surprise_lookup=lookup)
    assert day.new == []   # not enough history for RS -> unknown, never assumed to pass


def test_live_paper_params_match_the_research_variant_name():
    from app.live_rockets import PAPER_PARAMS

    assert PAPER_PARAMS.name == "EPS surprise>20%, reaction>=10%, volume>=2x, RS>=0.8"


# ---------------------------------------------------------------------------
# Lekpott (real-money rockets) — sizing, sell alerts, pause rule, capital split
# ---------------------------------------------------------------------------

def _pot_settings(monkeypatch, pot_pct=20.0, pause_pct=30.0):
    import dataclasses

    from app.config import settings
    monkeypatch.setattr("app.config.settings", dataclasses.replace(settings, rocket_pot_pct=pot_pct,
                                                                   rocket_pot_pause_pct=pause_pct, bot_share_pct=100.0))


def test_pot_takes_its_share_out_of_the_rotation(monkeypatch):
    from app.live_rotation import bot_capital, capital_line, rocket_pot_capital
    from app.runtime_settings import get_effective_settings

    total = get_effective_settings().portfolio_size_usd
    _pot_settings(monkeypatch, pot_pct=20.0)
    assert rocket_pot_capital() == pytest.approx(total * 0.2)
    assert bot_capital() == pytest.approx(total * 0.8)
    assert "lekpott" in capital_line()
    _pot_settings(monkeypatch, pot_pct=0.0)
    assert rocket_pot_capital() == 0 and bot_capital() == pytest.approx(total)


def test_allocate_pot_sizes_whole_shares_and_keeps_the_rest_on_paper():
    from app.live_rockets import RocketPot, allocate_pot

    pot = RocketPot(capital=2000.0)          # slot = 10% = $200
    new = [{"symbol": "A", "last_close": 50.0}, {"symbol": "B", "last_close": 900.0},
           {"symbol": "C", "last_close": 120.0}, {"symbol": "D", "last_close": 10.0}, {"symbol": "E", "last_close": 10.0}]
    allocate_pot(new, pot)
    assert (new[0]["pot_shares"], new[0]["pot_usd"]) == (4, 200.0)
    assert "pot_shares" not in new[1] and "dubbla" in new[1]["paper_reason"]      # one share > 2x the slot
    assert new[2]["pot_shares"] == 2 and new[3]["pot_shares"] == 20
    assert "pot_shares" not in new[4] and "per dag" in new[4]["paper_reason"]     # max 3 new per day

    full = RocketPot(capital=2000.0, open_count=10)
    one = [{"symbol": "A", "last_close": 50.0}]
    allocate_pot(one, full)
    assert "pot_shares" not in one[0] and "redan 10" in one[0]["paper_reason"]

    paused = RocketPot(capital=2000.0, return_pct=-31.0, paused=True)
    one = [{"symbol": "A", "last_close": 50.0}]
    allocate_pot(one, paused)
    assert "pot_shares" not in one[0] and "pausad" in one[0]["paper_reason"]

    none = [{"symbol": "A", "last_close": 50.0}]
    allocate_pot(none, RocketPot(capital=0.0))
    assert none == [{"symbol": "A", "last_close": 50.0}]                        # no pot -> untouched (paper)


def test_pot_buy_message_says_how_much_to_buy_and_warns():
    r = {"symbol": "RKT", "surprise_pct": 25.0, "reaction": 0.13, "last_close": 22.6, "pot_shares": 9, "pot_usd": 203.4}
    msg = format_rocket_buy(r, None)
    assert msg.startswith("🚀 RAKET (lekpott, hög risk) — KÖP RKT")
    assert "9 st ≈ $203" in msg and "inte bevisad" in msg and "köp inte" not in msg
    paper = format_rocket_buy({**{k: v for k, v in r.items() if not k.startswith("pot_")}, "paper_reason": "lekpotten är pausad"}, None)
    assert paper.startswith("🚀 RAKET (papper — köp inte)") and "lekpotten är pausad" in paper


class _Rec:
    def __init__(self, id, result="OPEN", return_pct=None, timestamp=None, tier="POT"):
        self.id, self.result, self.return_pct, self.timestamp, self.tier = id, result, return_pct, timestamp, tier


def test_pot_return_banks_closed_and_marks_open_slots():
    from app.live_rockets import pot_return_pct

    records = [_Rec(1, "ROCKET_TRAIL", -20.0), _Rec(2, "ROCKET_TIME", 50.0), _Rec(3), _Rec(4)]
    marks = {3: {"fill_price": 10.0, "unrealized_pct": -10.0}, 4: {"fill_price": None, "unrealized_pct": None}}
    # 10% slots: -2 + 5 - 1 + 0 (not filled yet)
    assert pot_return_pct(records, marks) == pytest.approx(2.0)


def test_pot_sell_signal_follows_the_research_trailing_rule():
    from app.live_rockets import pot_sell_signal

    closes = [20.0, 21.0, 30.0, 28.0, 22.4]   # fill at the open after bar 0; peak close 30 -> 22.5 is the line
    df = _frame(closes)
    rec = _Rec(1, timestamp=df["close_time"].iloc[0].isoformat())
    assert "under sin högsta" in pot_sell_signal(df, rec)
    assert pot_sell_signal(_frame(closes[:4]), rec) is None                      # 28 is only 7% under the peak
    long_hold = _frame([20.0] + [21.0] * 60)
    assert "60 handelsdagar" in pot_sell_signal(long_hold, _Rec(1, timestamp=long_hold["close_time"].iloc[0].isoformat()))


def test_pot_pause_is_sticky_until_resumed(clean_journal, monkeypatch):
    from app.live_rockets import rocket_pot_state

    _pot_settings(monkeypatch, pot_pct=20.0, pause_pct=30.0)
    journal.set_rocket_pot_paused(None)
    ids = [journal.save_rocket_paper({"symbol": s, "timestamp": "2026-10-01T20:00:00+00:00", "last_close": 10.0,
                                      "surprise_pct": 30.0, "pot_shares": 20}, None) for s in ("A", "B", "C", "D")]
    marks = {i: {"fill_price": 10.0, "unrealized_pct": -80.0} for i in ids}      # 4 slots x 10% x -80% = -32%
    pot = rocket_pot_state(lambda r: marks[r.id])
    assert pot.paused and pot.return_pct == pytest.approx(-32.0) and pot.open_count == 4
    assert journal.rocket_pot_paused_at() is not None

    recovered = {i: {"fill_price": 10.0, "unrealized_pct": 0.0} for i in ids}
    assert rocket_pot_state(lambda r: recovered[r.id]).paused                    # stays paused until resumed on purpose
    journal.set_rocket_pot_paused(None)
    assert not rocket_pot_state(lambda r: recovered[r.id]).paused


def test_closed_headline_separates_pot_from_paper():
    from app.daily import _rocket_closed_headline

    assert _rocket_closed_headline([{"symbol": "RKT", "return_pct": 12.4, "tier": "POT"},
                                    {"symbol": "ABC", "return_pct": -8.0, "tier": "PAPER"}]) == \
        "🚀 avslutad (lekpott) RKT +12% · 🚀 avslutad (papper) ABC -8%"
