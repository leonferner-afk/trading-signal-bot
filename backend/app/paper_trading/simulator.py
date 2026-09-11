"""Paper trading (section 13).

Every signal that clears the quality filter is logged automatically (via
`app.journal.repository.save_signal`, called from the scanner/API layer).
This module is the other half: it walks REAL subsequent market data for
each still-open signal and records what actually happened — target hit,
stop hit, or still running — with maximum favorable/adverse excursion and
holding time. It never estimates or assumes an outcome; a symbol whose
fresh data cannot be fetched is left OPEN and reported as "could not be
updated", not silently marked as a win.
"""
from __future__ import annotations

import datetime as dt

import pandas as pd

from app.config import settings
from app.data.binance_client import BinanceClient, DataUnavailable
from app.db import SignalRecord

EXPIRY_HOURS = 48


def _parse_timestamp(value: str) -> dt.datetime:
    ts = pd.Timestamp(value)
    if ts.tzinfo is None:
        ts = ts.tz_localize("UTC")
    return ts.to_pydatetime()


def evaluate_open_signal(client: BinanceClient, record: SignalRecord, interval: str) -> dict | None:
    """Returns an update dict (result/mfe/mae/holding_minutes/closed_at) if
    the signal resolved or expired, or None if it should stay OPEN /
    could not be checked."""
    entry_time = _parse_timestamp(record.timestamp)
    now = dt.datetime.now(dt.timezone.utc)
    age_hours = (now - entry_time).total_seconds() / 3600.0

    try:
        limit = min(1000, max(50, int(age_hours * 2) + 20))
        df = client.get_klines(record.symbol, interval, limit=limit)
    except DataUnavailable:
        return None

    df = df[df["close_time"] > pd.Timestamp(entry_time)]
    if df.empty:
        return None

    mfe = 0.0
    mae = 0.0
    for _, bar in df.iterrows():
        high, low = float(bar["high"]), float(bar["low"])
        favorable = (high - record.entry) if record.direction == "LONG" else (record.entry - low)
        adverse = (record.entry - low) if record.direction == "LONG" else (high - record.entry)
        mfe = max(mfe, favorable / record.entry * 100)
        mae = max(mae, adverse / record.entry * 100)

        stop_hit = low <= record.stop if record.direction == "LONG" else high >= record.stop
        target_hit = high >= record.target if record.direction == "LONG" else low <= record.target

        if stop_hit:
            holding_minutes = (bar["close_time"] - pd.Timestamp(entry_time)).total_seconds() / 60.0
            return {
                "result": "STOP_HIT", "max_favorable_excursion_pct": round(mfe, 4),
                "max_adverse_excursion_pct": round(mae, 4), "holding_time_minutes": round(holding_minutes, 1),
                "closed_at": bar["close_time"].to_pydatetime(),
            }
        if target_hit:
            holding_minutes = (bar["close_time"] - pd.Timestamp(entry_time)).total_seconds() / 60.0
            return {
                "result": "TARGET_HIT", "max_favorable_excursion_pct": round(mfe, 4),
                "max_adverse_excursion_pct": round(mae, 4), "holding_time_minutes": round(holding_minutes, 1),
                "closed_at": bar["close_time"].to_pydatetime(),
            }

    if age_hours >= EXPIRY_HOURS:
        last_bar_time = df["close_time"].iloc[-1]
        holding_minutes = (last_bar_time - pd.Timestamp(entry_time)).total_seconds() / 60.0
        return {
            "result": "EXPIRED", "max_favorable_excursion_pct": round(mfe, 4),
            "max_adverse_excursion_pct": round(mae, 4), "holding_time_minutes": round(holding_minutes, 1),
            "closed_at": last_bar_time.to_pydatetime(),
        }

    return None


def run_paper_trading_update(interval: str | None = None) -> dict:
    """Checks every OPEN signal against fresh market data and closes any
    that have resolved. Returns a summary of what changed."""
    from app.journal.repository import close_signal, get_open_signals

    interval = interval or settings.scan_interval
    open_records = get_open_signals()
    updated = []
    unavailable = []

    with BinanceClient() as client:
        for record in open_records:
            update = evaluate_open_signal(client, record, interval)
            if update is None:
                unavailable.append(record.symbol)
                continue
            close_signal(
                record.id,
                update["result"],
                update["max_favorable_excursion_pct"],
                update["max_adverse_excursion_pct"],
                update["holding_time_minutes"],
                update["closed_at"],
            )
            updated.append({"id": record.id, "symbol": record.symbol, **{k: v for k, v in update.items() if k != "closed_at"}})

    return {"checked": len(open_records), "updated": updated, "still_open_or_unavailable": unavailable}
