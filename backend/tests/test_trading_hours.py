"""Unit tests for the quiet-hours gate — no network, no synthetic market
data needed, just clock math."""
from __future__ import annotations

import datetime as dt

from app.notify.trading_hours import is_within_trading_hours


def test_disabled_gate_is_always_open():
    # Tuesday 03:00 UTC — well outside any normal trading window, but the
    # gate is off, so it must still return True.
    now = dt.datetime(2024, 1, 2, 3, 0, tzinfo=dt.timezone.utc)
    assert is_within_trading_hours(now, enabled=False) is True


def test_within_configured_window():
    # 2024-01-02 is a Tuesday. 12:00 UTC in Europe/Stockholm (winter, UTC+1) = 13:00 local.
    now = dt.datetime(2024, 1, 2, 12, 0, tzinfo=dt.timezone.utc)
    assert is_within_trading_hours(
        now, enabled=True, start="09:00", end="22:00", timezone_name="Europe/Stockholm", days=("tue",)
    ) is True


def test_outside_configured_window():
    # 03:00 UTC = 04:00 local Stockholm — before the 09:00 start.
    now = dt.datetime(2024, 1, 2, 3, 0, tzinfo=dt.timezone.utc)
    assert is_within_trading_hours(
        now, enabled=True, start="09:00", end="22:00", timezone_name="Europe/Stockholm", days=("tue",)
    ) is False


def test_day_not_in_allowed_days():
    # Tuesday, but only Mondays are allowed.
    now = dt.datetime(2024, 1, 2, 12, 0, tzinfo=dt.timezone.utc)
    assert is_within_trading_hours(
        now, enabled=True, start="00:00", end="23:59", timezone_name="UTC", days=("mon",)
    ) is False


def test_overnight_window_wraps_midnight():
    # 23:00 -> 04:00 window; 01:00 local should be inside it.
    now = dt.datetime(2024, 1, 2, 1, 0, tzinfo=dt.timezone.utc)
    assert is_within_trading_hours(
        now, enabled=True, start="23:00", end="04:00", timezone_name="UTC", days=("tue",)
    ) is True
    now_outside = dt.datetime(2024, 1, 2, 12, 0, tzinfo=dt.timezone.utc)
    assert is_within_trading_hours(
        now_outside, enabled=True, start="23:00", end="04:00", timezone_name="UTC", days=("tue",)
    ) is False


def test_bad_timezone_fails_open():
    now = dt.datetime(2024, 1, 2, 3, 0, tzinfo=dt.timezone.utc)
    assert is_within_trading_hours(now, enabled=True, timezone_name="Not/ARealZone") is True
