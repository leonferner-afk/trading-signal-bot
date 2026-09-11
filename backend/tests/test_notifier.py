"""Unit tests for KÖP NU / SÄLJ NU notification logic — network calls are
stubbed out (no real Telegram/webhook delivery in tests)."""
from __future__ import annotations

import datetime as dt

import pytest

from app.db import SignalRecord
from app.notify import notifier
from app.scoring.score import ScoreBreakdown, Signal


def _breakdown(total: float) -> ScoreBreakdown:
    return ScoreBreakdown(
        momentum=20, momentum_max=25, volume=15, volume_max=20, structure=15, structure_max=20,
        regime=10, regime_max=15, catalyst=0, catalyst_max=10, catalyst_reason="no data",
        risk_reward=5, risk_reward_max=10, total=total, tier="HIGH_QUALITY",
    )


def _signal(direction="LONG", score=85.0) -> Signal:
    return Signal(
        symbol="BTCUSDT", strategy="breakout", direction=direction, timestamp="2024-01-01T00:00:00Z",
        entry=100.0, stop=97.0, target=106.0, risk_pct=3.0, reward_pct=6.0, rr_ratio=2.0,
        invalidation=97.0, invalidation_reason="ATR x1.5", target_reason="ATR x3",
        realistic=True, warning=None, score=score, tier="HIGH_QUALITY", breakdown=_breakdown(score),
        reasons=["breakout confirmed", "volume spike"], regime_label="TRENDING_UP / NORMAL_VOLATILITY",
    )


@pytest.fixture(autouse=True)
def stub_delivery(monkeypatch):
    # settings.notify_webhook_url is None by default in this environment
    # (no NOTIFY_WEBHOOK_URL set) — only Telegram delivery needs stubbing.
    calls = {"telegram": []}
    monkeypatch.setattr(notifier.telegram_client, "send_message", lambda msg: calls["telegram"].append(msg) or True)
    return calls


def test_entry_message_says_kop_nu():
    msg = notifier.format_entry_message(_signal())
    assert msg.startswith("🟢 KÖP NU")
    assert "BTCUSDT" in msg
    assert "Target: 106" in msg


def test_notify_entry_sends_for_long_above_threshold(stub_delivery, monkeypatch):
    monkeypatch.setattr(notifier, "is_within_trading_hours", lambda: True)
    sent = notifier.notify_entry(_signal(direction="LONG", score=85.0), min_score=80.0)
    assert sent is True
    assert len(stub_delivery["telegram"]) == 1


def test_notify_entry_skips_short_direction(stub_delivery):
    sent = notifier.notify_entry(_signal(direction="SHORT", score=90.0), min_score=80.0)
    assert sent is False
    assert stub_delivery["telegram"] == []


def test_notify_entry_skips_below_threshold(stub_delivery):
    sent = notifier.notify_entry(_signal(direction="LONG", score=72.0), min_score=80.0)
    assert sent is False
    assert stub_delivery["telegram"] == []


def test_notify_entry_respects_quiet_hours_gate(stub_delivery, monkeypatch):
    monkeypatch.setattr(notifier, "is_within_trading_hours", lambda: False)
    sent = notifier.notify_entry(_signal(direction="LONG", score=90.0), min_score=80.0)
    assert sent is False
    assert stub_delivery["telegram"] == []


def _record(direction="LONG") -> SignalRecord:
    r = SignalRecord()
    r.symbol = "BTCUSDT"
    r.direction = direction
    r.strategy = "breakout"
    r.entry = 100.0
    r.stop = 97.0
    r.target = 106.0
    r.risk_pct = 3.0
    r.reward_pct = 6.0
    r.score = 85.0
    r.timestamp = "2024-01-01T00:00:00Z"
    return r


def test_notify_exit_always_fires_regardless_of_hours(stub_delivery):
    update = {
        "result": "TARGET_HIT", "max_favorable_excursion_pct": 6.5,
        "max_adverse_excursion_pct": 1.2, "holding_time_minutes": 220,
        "closed_at": dt.datetime(2024, 1, 1, 4, 0, tzinfo=dt.timezone.utc),
    }
    notifier.notify_exit(_record(), update)
    assert len(stub_delivery["telegram"]) == 1
    assert "SÄLJ NU" in stub_delivery["telegram"][0]
    assert "TARGET HIT" in stub_delivery["telegram"][0]


def test_notify_exit_skips_short_direction(stub_delivery):
    update = {
        "result": "STOP_HIT", "max_favorable_excursion_pct": 0.5,
        "max_adverse_excursion_pct": 3.0, "holding_time_minutes": 60,
        "closed_at": dt.datetime(2024, 1, 1, 1, 0, tzinfo=dt.timezone.utc),
    }
    notifier.notify_exit(_record(direction="SHORT"), update)
    assert stub_delivery["telegram"] == []
