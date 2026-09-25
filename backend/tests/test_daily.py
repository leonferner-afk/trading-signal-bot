"""The daily job end to end on SYNTHETIC data (no network): market data is
served from generated frames, notifications are captured instead of sent.
Verifies wiring and bookkeeping only — nothing here says anything about
real strategy performance."""
from __future__ import annotations

import datetime as dt

import numpy as np
import pandas as pd
import pytest

import app.daily as daily
from app.db import SignalRecord, get_session, init_db
from app.policy import LivePolicy
from app.scoring.score import ScoreBreakdown, Signal


def _frame(n: int, end: pd.Timestamp, seed: int, drift: float = 0.002) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    closes = 100 * np.cumprod(1 + drift + rng.normal(0, 0.02, n))
    opens = np.concatenate([[100.0], closes[:-1]])
    highs = np.maximum(opens, closes) * (1 + rng.uniform(0, 0.01, n))
    lows = np.minimum(opens, closes) * (1 - rng.uniform(0, 0.01, n))
    close_time = pd.bdate_range(end=end, periods=n).tz_localize("America/New_York") + pd.Timedelta(hours=16)
    close_time = close_time.tz_convert("UTC")
    df = pd.DataFrame({"open": opens, "high": highs, "low": lows, "close": closes,
                       "volume": rng.uniform(1e6, 3e6, n), "close_time": close_time})
    df["open_time"] = df["close_time"]
    return df.set_index("close_time", drop=False)


@pytest.fixture
def market(monkeypatch, tmp_path):
    last_session = pd.Timestamp(dt.date.today()) - pd.offsets.BDay(1)
    frames = {s: _frame(400, last_session, i) for i, s in enumerate(["SPY", "AAA", "BBB", "CCC"])}
    monkeypatch.setattr(daily.StockClient, "prefetch", lambda self, symbols, interval="1d", limit=500: {})
    monkeypatch.setattr(daily.StockClient, "get_klines", lambda self, s, i, limit=500: frames[s].tail(limit))
    monkeypatch.setattr("app.scanner.scanner.earnings_warning", lambda symbol: None)
    sent: list[str] = []
    monkeypatch.setattr("app.notify.notifier.telegram_client.send_message", lambda msg: sent.append(msg) or True)
    monkeypatch.setattr(daily.github_issue, "publish", lambda title, body: sent.append(title) or "https://example/issue/1")
    with get_session() as session:
        session.query(SignalRecord).delete()
        session.commit()
    from app.runtime_settings import update_settings_overrides

    update_settings_overrides(watchlist=["AAA", "BBB", "CCC"])
    yield frames, sent
    update_settings_overrides(watchlist=None)


def _signal(symbol: str, score: float, strategy: str = "momentum", **context) -> Signal:
    bd = ScoreBreakdown(20, 25, 15, 20, 15, 20, 10, 15, 0, 10, "none", 5, 10, score, "HIGH_QUALITY")
    return Signal(symbol=symbol, strategy=strategy, direction="LONG", timestamp="2026-01-02T21:00:00+00:00",
                  entry=100, stop=95, target=150, risk_pct=5, reward_pct=50, rr_ratio=10, invalidation=95,
                  invalidation_reason="", target_reason="", realistic=True, warning=None, score=score,
                  tier="HIGH_QUALITY", breakdown=bd, reasons=["r"], regime_label="x",
                  context={"spy_above_200": True, "stock_above_200": True, **context})


def test_select_buys_respects_policy_limits_and_existing_positions():
    policy = LivePolicy("score>=80", ("momentum",), 80, True, False)
    signals = [_signal("A", 95), _signal("B", 90), _signal("C", 85), _signal("D", 70), _signal("E", 99, strategy="reversal"),
               _signal("F", 88, spy_above_200=False)]
    buys, watch = daily.select_buys(signals, policy, open_symbols={"B"}, open_count=6)
    # 8 max open - 6 open = 2 slots: A, then C (B already held).
    assert [s.symbol for s in buys] == ["A", "C"]
    reasons = dict((s.symbol, why) for s, why in watch)
    assert "saknar stöd" in reasons["E"] and "redan" in reasons["B"] and "score" in reasons["D"] and "SPY" in reasons["F"]


def test_daily_run_writes_report_and_tracks_positions(market, tmp_path, monkeypatch):
    frames, sent = market
    permissive = LivePolicy("all", ("breakout", "momentum", "reversal"), 0, False, False)
    monkeypatch.setattr(daily, "active_policy", lambda: permissive)
    init_db()

    outcome = daily.run_daily(report_dir=tmp_path / "reports")
    assert outcome.ok
    assert (tmp_path / "reports" / "latest.md").read_text().startswith("# Tradingbot")
    assert "## 🟢 KÖP" in outcome.report_markdown and "## 📊 Öppna positioner" in outcome.report_markdown
    for signal in outcome.buys:
        assert any(signal.symbol in msg for msg in sent)  # KÖP NU delivered

    # A buy is never repeated while the position is open.
    again = daily.run_daily(report_dir=tmp_path / "reports")
    assert not {s.symbol for s in again.buys} & {s.symbol for s in outcome.buys}


def test_buy_then_target_exit_uses_next_open_fill(market, tmp_path, monkeypatch):
    frames, sent = market
    permissive = LivePolicy("all", ("breakout", "momentum", "reversal"), 0, False, False)
    monkeypatch.setattr(daily, "active_policy", lambda: permissive)
    init_db()

    aaa = frames["AAA"]
    signal_bar = aaa.iloc[-3]  # two sessions exist after the signal
    signal = _signal("AAA", 90)
    signal.timestamp = signal_bar["close_time"].isoformat()
    signal.entry = float(signal_bar["close"])
    signal.stop = signal.entry * 0.9
    signal.target = signal.entry * 1.2
    # Day 1 after the signal opens flat, day 2 spikes through the target.
    day1, day2 = aaa.index[-2], aaa.index[-1]
    aaa.loc[day1, ["open", "high", "low", "close"]] = [signal.entry, signal.entry * 1.01, signal.entry * 0.99, signal.entry]
    aaa.loc[day2, ["open", "high", "low", "close"]] = [signal.entry * 1.05, signal.entry * 1.3, signal.entry * 1.04, signal.entry * 1.25]

    scans = iter([[signal], []])

    def fake_scan(universe, interval, client=None, strategies=None):
        return daily.ScanResult(scanned_at="now", watchlist=universe, market_wide_risk="NEUTRAL",
                                signals=next(scans), spy_above_200=True)

    monkeypatch.setattr(daily, "run_scan", fake_scan)

    # Run 1 happens "on the signal day": hide the later bars from the exit check.
    real_get = daily.StockClient.get_klines
    monkeypatch.setattr(daily.StockClient, "get_klines",
                        lambda self, s, i, limit=500: frames[s].loc[: signal_bar.name].tail(limit))
    first = daily.run_daily(report_dir=tmp_path / "r")
    assert [s.symbol for s in first.buys] == ["AAA"]
    assert any("KÖP NU — AAA" in m for m in sent)

    monkeypatch.setattr(daily.StockClient, "get_klines", real_get)
    second = daily.run_daily(report_dir=tmp_path / "r")
    exit_ = next(e for e in second.exits if e["symbol"] == "AAA")
    assert exit_["result"] == "TARGET_HIT"
    assert exit_["fill_price"] == pytest.approx(signal.entry)          # bought at day-1 open
    assert exit_["exit_price"] == pytest.approx(signal.target)         # sold at the target
    assert exit_["return_pct"] == pytest.approx(20 - 0.3, abs=0.1)     # minus fees+slippage both ways
    assert exit_["r_multiple"] == pytest.approx(2.0, abs=0.05)
    assert "## 🔴 SÄLJ (1)" in second.report_markdown and any("SÄLJ NU — AAA" in m for m in sent)
