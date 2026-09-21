"""Earnings-date awareness — a real, stock-specific risk crypto never had:
holding a swing position through a scheduled earnings report can gap it
hard in either direction, and that gap can blow straight through a normal
ATR-based stop.

This module only ever ADDS a warning when it finds a real, near-term
scheduled date. It never claims "no earnings coming" when the data is
simply unavailable or ambiguous — `next_earnings_date` returning None
means "unknown", not "confirmed clear", so callers must never treat a
missing warning as a guarantee.
"""
from __future__ import annotations

import datetime as dt
import logging

import pandas as pd
import yfinance as yf

logger = logging.getLogger("tradingbot.earnings")

EARNINGS_WINDOW_DAYS = 30


def next_earnings_date(symbol: str) -> dt.date | None:
    """Best-effort lookup of the next scheduled earnings date. Returns
    None on any failure, missing data, or ambiguity — never guesses."""
    try:
        calendar = yf.Ticker(symbol.upper()).calendar
    except Exception as exc:
        logger.debug("earnings calendar lookup failed for %s: %s", symbol, exc)
        return None

    dates: list[dt.date] = []
    try:
        if isinstance(calendar, dict):
            raw = calendar.get("Earnings Date")
            if isinstance(raw, (list, tuple)):
                dates = [d for d in raw if isinstance(d, dt.date)]
            elif isinstance(raw, dt.date):
                dates = [raw]
        elif calendar is not None and hasattr(calendar, "empty"):
            # Older yfinance versions returned a DataFrame instead of a dict.
            if not calendar.empty and "Earnings Date" in list(calendar.index):
                row = calendar.loc["Earnings Date"]
                values = row.tolist() if hasattr(row, "tolist") else [row]
                for v in values:
                    if isinstance(v, dt.date):
                        dates.append(v)
                    else:
                        try:
                            dates.append(pd.Timestamp(v).date())
                        except (ValueError, TypeError):
                            continue
    except Exception as exc:
        logger.debug("earnings calendar parsing failed for %s: %s", symbol, exc)
        return None

    if not dates:
        return None

    today = dt.date.today()
    future_dates = [d for d in dates if d >= today]
    return min(future_dates) if future_dates else None


def earnings_warning(symbol: str, window_days: int = EARNINGS_WINDOW_DAYS) -> str | None:
    """A caution string if a scheduled earnings date falls within
    `window_days` of today, else None. None here does NOT mean "confirmed
    no earnings soon" — the calendar lookup can fail or simply not have
    data — so this must only ever be used additively (append a warning),
    never to assert a position is clear of earnings risk."""
    next_date = next_earnings_date(symbol)
    if next_date is None:
        return None

    days_away = (next_date - dt.date.today()).days
    if days_away > window_days:
        return None

    return (
        f"Earnings report expected around {next_date.isoformat()} ({days_away}d away) — "
        f"within this position's typical holding window. Expect a possible large gap in "
        f"either direction around that date; account for it in position size and whether "
        f"you're willing to hold through it."
    )
