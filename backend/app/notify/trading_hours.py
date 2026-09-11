""""Quiet hours" gate for ENTRY ("köp nu") notifications only.

Exit ("sälj nu") alerts never go through this gate — once you're in a
position, you want to know it closed no matter what time it is. This only
decides whether a *new* entry alert is worth waking you up for right now;
the underlying signal is still saved to the journal either way, so nothing
is lost, only the notification is deferred.

Uses the stdlib `zoneinfo` (Python 3.9+) — no extra dependency.
"""
from __future__ import annotations

import datetime as dt
from zoneinfo import ZoneInfo

from app.config import settings

_DAY_CODES = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]


def _parse_hhmm(value: str) -> dt.time:
    hour, minute = value.strip().split(":")
    return dt.time(hour=int(hour), minute=int(minute))


def is_within_trading_hours(
    now_utc: dt.datetime | None = None,
    *,
    enabled: bool | None = None,
    start: str | None = None,
    end: str | None = None,
    timezone_name: str | None = None,
    days: tuple[str, ...] | None = None,
) -> bool:
    """True if entry notifications should be sent right now. Always True
    when the gate is disabled (the default — crypto trades 24/7, so there
    is no gate unless the user explicitly configures one).

    Every parameter defaults to the live config (`app.config.settings`);
    they're only exposed so tests can exercise specific configurations
    without mutating global settings.
    """
    enabled = settings.trading_hours_enabled if enabled is None else enabled
    if not enabled:
        return True

    timezone_name = timezone_name or settings.trading_hours_timezone
    now_utc = now_utc or dt.datetime.now(dt.timezone.utc)
    try:
        local_now = now_utc.astimezone(ZoneInfo(timezone_name))
    except Exception:
        # A misconfigured timezone must never silently suppress every
        # notification — fail open.
        return True

    days = days if days is not None else settings.trading_days
    day_code = _DAY_CODES[local_now.weekday()]
    if day_code not in days:
        return False

    start_t = _parse_hhmm(start or settings.trading_hours_start)
    end_t = _parse_hhmm(end or settings.trading_hours_end)
    now_t = local_now.time()

    if start_t <= end_t:
        return start_t <= now_t <= end_t
    # Overnight window (e.g. 22:00 -> 04:00).
    return now_t >= start_t or now_t <= end_t
