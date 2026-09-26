"""Rotation mode of the daily job, end to end on SYNTHETIC data (no
network): buys the strongest names, sells on a lost trend, closes at the
next open, stays quiet on a re-run. Bookkeeping only — says nothing about
real performance."""
from __future__ import annotations

import datetime as dt

import numpy as np
import pandas as pd
import pytest

import app.daily as daily
from app.db import BotRun, SignalRecord, get_session, init_db
from app.journal import repository as journal
from app.rotation import RotationParams


def _frame(n: int, end: pd.Timestamp, seed: int, drift: float) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    closes = 100 * np.exp(np.cumsum(drift + rng.normal(0, 0.01, n)))
    opens = np.concatenate([[100.0], closes[:-1]])
    close_time = (pd.bdate_range(end=end, periods=n).tz_localize("America/New_York") + pd.Timedelta(hours=16)).tz_convert("UTC")
    df = pd.DataFrame({"open": opens, "high": np.maximum(opens, closes) * 1.005, "low": np.minimum(opens, closes) * 0.995,
                       "close": closes, "volume": 1e6, "close_time": close_time})
    df["open_time"] = df["close_time"]
    return df.set_index("close_time", drop=False)


@pytest.fixture
def world(monkeypatch):
    last = pd.Timestamp(dt.date.today()) - pd.offsets.BDay(1)
    drifts = {"SPY": 0.002, "UP1": 0.004, "UP2": 0.0035, "UP3": 0.003, "UP4": 0.0025}
    drifts.update({f"FL{i}": 0.0 for i in range(6)})
    frames = {s: _frame(400, last, i, d) for i, (s, d) in enumerate(drifts.items())}
    view = {"cut": 2}  # how many of the latest bars are still "in the future"

    def get_klines(self, symbol, interval, limit=500):
        f = frames[symbol]
        return (f.iloc[: len(f) - view["cut"]] if view["cut"] else f).tail(limit)

    monkeypatch.setattr(daily.StockClient, "prefetch", lambda self, symbols, interval="1d", limit=500: {})
    monkeypatch.setattr(daily.StockClient, "get_klines", get_klines)
    sent: list[str] = []
    monkeypatch.setattr("app.notify.notifier.telegram_client.send_message", lambda msg: sent.append(msg) or True)
    monkeypatch.setattr(daily.github_issue, "publish", lambda title, body: sent.append(title) or "https://example/issue/1")
    monkeypatch.setenv("POLICY_MODE", "rotation")
    monkeypatch.setattr(daily, "active_rotation_params",
                        lambda: RotationParams(max_positions=3, entry_rs=0.8, exit_rs=0.5, max_new_per_day=3))
    init_db()
    with get_session() as session:
        session.query(SignalRecord).delete()
        session.query(BotRun).delete()
        session.commit()
    from app.runtime_settings import update_settings_overrides

    update_settings_overrides(watchlist=[s for s in frames if s != "SPY"])
    yield frames, view, sent
    update_settings_overrides(watchlist=None)


def test_rotation_buys_sells_and_closes_at_next_open(world, tmp_path):
    frames, view, sent = world

    day1 = daily.run_daily(report_dir=tmp_path)
    assert day1.ok
    assert day1.rotation_buys == ["UP1", "UP2", "UP3"]  # the 3 strongest (top 3 of 10 by 6-month return)
    assert sum("KÖP NU — UP" in m for m in sent) == 3
    assert "## 🟢 KÖP (3)" in day1.report_markdown

    # Next session: UP1 collapses below its 200-day average at the close.
    crash_day = frames["UP1"].index[-2]
    frames["UP1"].loc[crash_day, ["open", "high", "low", "close"]] = [60.0, 61.0, 29.0, 30.0]
    frames["UP1"].loc[frames["UP1"].index[-1], ["open", "high", "low", "close"]] = [31.0, 32.0, 30.0, 31.5]
    view["cut"] = 1
    sent.clear()
    day2 = daily.run_daily(report_dir=tmp_path)
    assert day2.rotation_sells == ["UP1"]
    assert any(m.startswith("🔴 SÄLJ NU — UP1") and "200-dagars" in m for m in sent)
    assert day2.rotation_buys == ["UP4"]  # the freed slot goes to the next strongest

    # Session after that: UP1 is sold at the open — no second SÄLJ message.
    view["cut"] = 0
    sent.clear()
    day3 = daily.run_daily(report_dir=tmp_path)
    closed = [e for e in day3.exits if e["symbol"] == "UP1"]
    assert closed and closed[0]["result"] == "ROTATION_EXIT" and closed[0]["exit_price"] == pytest.approx(31.0)
    assert not any("SÄLJ NU — UP1" in m for m in sent)
    assert "Avslutade sedan förra rapporten" in day3.report_markdown

    # Re-run on the same data: nothing new happens and nothing is sent.
    sent.clear()
    again = daily.run_daily(report_dir=tmp_path)
    assert again.ok and again.rotation_buys == [] and again.rotation_sells == [] and sent == []
    assert {r.symbol for r in journal.get_open_signals()} == {"UP2", "UP3", "UP4"}


def test_rotation_evidence_comes_from_the_hindsight_free_group(monkeypatch):
    from app.live_rotation import rotation_evidence
    from app.notify.notifier import format_rotation_buy
    from app.live_rotation import equal_weight_size

    params = RotationParams(max_positions=5)
    stats = {"trades": 90, "cagr_pct": 20.0, "max_drawdown_pct": -30.0, "sharpe": 0.9, "years": 8.7,
             "win_rate": 0.45, "avg_trade_pct": 12.0, "avg_days": 110.0}
    block = lambda cagr: {"rotation": {"configs": [{"name": params.name, "full": {**stats, "cagr_pct": cagr}, "oos": stats}],
                                       "spy": {"cagr_pct": 14.5, "max_drawdown_pct": -34.0}, "spy_oos": {"cagr_pct": 16.7}}}
    evidence = {"universes": {"all": block(99.0), "largecap_2015": block(20.0)}, "meta": {"years": 10}}
    monkeypatch.delenv("ROTATION_UNIVERSE", raising=False)
    ev = rotation_evidence(evidence, params)
    assert ev["cagr_pct"] == 20.0 and ev["spy_cagr_pct"] == 14.5
    assert rotation_evidence(evidence, RotationParams(max_positions=7)) is None  # other rule set -> no borrowed numbers

    size = equal_weight_size(50.0, 10000, params, free=10000)
    assert size.position_size_usd == 2000.0 and size.units == 40.0
    msg = format_rotation_buy("ABC", {"rs": 0.95, "ret_6m": 0.42, "last_close": 50.0, "universe": 100}, size, params, ev)
    assert msg.startswith("🟢 KÖP NU — ABC") and "+20.0%/år" in msg and "SPY samma period: +14.5%/år" in msg


def test_gate_warning_when_research_no_longer_supports_the_rule():
    from app.live_rotation import gate_status

    params = RotationParams(max_positions=5)
    ok = {"rotation_selection": {"chosen": params.name, "gates": [{"name": params.name, "passes": True, "checks": {}}]}}
    assert gate_status(ok, params) is None and gate_status(None, params) is None
    bad = {"rotation_selection": {"chosen": None, "gates": [
        {"name": params.name, "passes": False, "checks": {"ranking_beats_random": False, "drawdown_close_to_spy": True}}]}}
    msg = gate_status(bad, params)
    assert "slumpvis" in msg and "S&P 500-fond" in msg
