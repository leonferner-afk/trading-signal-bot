"""Shared "what to do with a fresh scan result" logic, used by both the
manual `/api/scan` endpoint and the background scheduler so they behave
identically — dedupe, journal, notify.
"""
from __future__ import annotations

import logging

from app.journal import repository as journal_repo
from app.notify.notifier import notify_entry
from app.scanner.scanner import ScanResult
from app.scoring.score import Signal

logger = logging.getLogger("sagoton.pipeline")


def historical_probability_for(symbol: str, strategy: str) -> dict | None:
    import json

    runs = journal_repo.list_backtest_runs(limit=50)
    for run in runs:
        if run.symbol == symbol and run.strategy == strategy:
            split = json.loads(run.split_json)
            oos = split.get("out_of_sample") or {}
            if oos.get("num_trades", 0) >= 20:
                timing = json.loads(run.timing_pattern_json) if run.timing_pattern_json else {}
                return {
                    "similar_setups": oos["num_trades"],
                    "target_hit_rate": oos.get("win_rate") or 0,
                    "average_return_pct": oos.get("expectancy_pct") or 0,
                    "average_holding_minutes": oos.get("average_holding_minutes"),
                    "common_hours_utc": timing.get("common_hours_utc"),
                }
    return None


def record_and_notify_signals(signals: list[Signal]) -> list[dict]:
    """For each qualifying signal: skip it if an identical setup is
    already OPEN (avoids duplicate "köp nu" alerts for the same position
    every scan cycle), otherwise journal it and attempt an entry
    notification. Returns a summary per signal for logging/API responses.
    """
    outcomes = []
    for signal in signals:
        if journal_repo.has_open_signal(signal.symbol, signal.strategy, signal.direction):
            outcomes.append({"symbol": signal.symbol, "strategy": signal.strategy, "action": "skipped_duplicate_open"})
            continue

        historical = historical_probability_for(signal.symbol, signal.strategy)
        journal_repo.save_signal(signal, historical)
        notified = notify_entry(signal, historical)
        outcomes.append(
            {
                "symbol": signal.symbol,
                "strategy": signal.strategy,
                "action": "notified" if notified else "journaled_only",
            }
        )
    return outcomes
