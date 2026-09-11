"""Unit tests for the journal dedupe helper that stops the same open
setup from re-triggering a "köp nu" alert every scan cycle. Runs against
an isolated in-memory SQLite database, never the real one."""
from __future__ import annotations

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import app.db as db
from app.journal import repository as journal_repo
from app.scoring.score import ScoreBreakdown, Signal


@pytest.fixture(autouse=True)
def isolated_db(monkeypatch):
    engine = create_engine("sqlite:///:memory:", future=True)
    db.Base.metadata.create_all(engine)
    monkeypatch.setattr(db, "SessionLocal", sessionmaker(bind=engine, expire_on_commit=False, future=True))
    yield


def _signal(symbol="BTCUSDT", strategy="breakout", direction="LONG") -> Signal:
    breakdown = ScoreBreakdown(
        momentum=20, momentum_max=25, volume=15, volume_max=20, structure=15, structure_max=20,
        regime=10, regime_max=15, catalyst=0, catalyst_max=10, catalyst_reason="no data",
        risk_reward=5, risk_reward_max=10, total=85, tier="HIGH_QUALITY",
    )
    return Signal(
        symbol=symbol, strategy=strategy, direction=direction, timestamp="2024-01-01T00:00:00Z",
        entry=100.0, stop=97.0, target=106.0, risk_pct=3.0, reward_pct=6.0, rr_ratio=2.0,
        invalidation=97.0, invalidation_reason="x", target_reason="x", realistic=True, warning=None,
        score=85.0, tier="HIGH_QUALITY", breakdown=breakdown, reasons=["test"], regime_label="TRENDING_UP",
    )


def test_no_open_signal_initially():
    assert journal_repo.has_open_signal("BTCUSDT", "breakout", "LONG") is False


def test_has_open_signal_true_after_save():
    journal_repo.save_signal(_signal())
    assert journal_repo.has_open_signal("BTCUSDT", "breakout", "LONG") is True


def test_dedupe_is_scoped_to_symbol_strategy_direction():
    journal_repo.save_signal(_signal(symbol="BTCUSDT", strategy="breakout", direction="LONG"))
    # A different strategy on the same symbol is a distinct setup.
    assert journal_repo.has_open_signal("BTCUSDT", "momentum", "LONG") is False
    # A different symbol entirely.
    assert journal_repo.has_open_signal("ETHUSDT", "breakout", "LONG") is False


def test_dedupe_clears_once_signal_is_closed():
    signal_id = journal_repo.save_signal(_signal())
    assert journal_repo.has_open_signal("BTCUSDT", "breakout", "LONG") is True

    import datetime as dt

    journal_repo.close_signal(signal_id, "TARGET_HIT", 6.0, 1.0, 120.0, dt.datetime.now(dt.timezone.utc))
    assert journal_repo.has_open_signal("BTCUSDT", "breakout", "LONG") is False
