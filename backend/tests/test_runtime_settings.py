"""Unit tests for DB-backed settings overrides — isolated in-memory DB."""
from __future__ import annotations

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import app.db as db
from app.runtime_settings import get_effective_settings, update_settings_overrides


@pytest.fixture(autouse=True)
def isolated_db(monkeypatch):
    engine = create_engine("sqlite:///:memory:", future=True)
    db.Base.metadata.create_all(engine)
    monkeypatch.setattr(db, "SessionLocal", sessionmaker(bind=engine, expire_on_commit=False, future=True))
    yield


def test_defaults_come_from_env_settings_when_no_overrides():
    live = get_effective_settings()
    assert live.overridden_fields == ()
    assert live.enable_scheduler is False  # env default in this environment


def test_override_persists_and_is_reported():
    update_settings_overrides(enable_scheduler=True, scan_loop_minutes=15)
    live = get_effective_settings()
    assert live.enable_scheduler is True
    assert live.scan_loop_minutes == 15
    assert "enable_scheduler" in live.overridden_fields
    assert "scan_loop_minutes" in live.overridden_fields


def test_watchlist_list_is_converted_and_back():
    update_settings_overrides(watchlist=["btcusdt", "ethusdt "])
    live = get_effective_settings()
    assert live.watchlist == ("BTCUSDT", "ETHUSDT")


def test_clearing_override_falls_back_to_default():
    update_settings_overrides(enable_scheduler=True)
    assert get_effective_settings().enable_scheduler is True
    update_settings_overrides(enable_scheduler=None)
    live = get_effective_settings()
    assert live.enable_scheduler is False
    assert "enable_scheduler" not in live.overridden_fields


def test_unknown_field_rejected():
    with pytest.raises(ValueError):
        update_settings_overrides(not_a_real_field=123)


def test_portfolio_defaults_are_sane_when_unset():
    live = get_effective_settings()
    assert live.portfolio_size_usd == 1000.0
    assert live.risk_per_trade_pct == 1.0
