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
