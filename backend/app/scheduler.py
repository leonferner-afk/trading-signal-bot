"""Background scheduler: the two loops that make notifications happen
without you having to click anything.

  - entry_scan_loop:   every SCAN_LOOP_MINUTES, scans the watchlist for
                        new "köp nu" setups (same pipeline as the manual
                        Run Scan button).
  - exit_monitor_loop: every MONITOR_LOOP_MINUTES, checks every OPEN
                        signal against fresh, finer-grained price data and
                        fires "sälj nu" the moment one resolves.

Off by default (ENABLE_SCHEDULER=false) so importing/testing the app never
silently starts network loops. A single bad cycle (a network blip, a
temporarily unreachable exchange) is logged and the loop keeps going —
it never crashes the app or stops watching your open positions.
"""
from __future__ import annotations

import asyncio
import logging

from app.config import settings
from app.data.binance_client import DataUnavailable
from app.pipeline import record_and_notify_signals
from app.scanner.scanner import run_scan

logger = logging.getLogger("sagoton.scheduler")

_tasks: list[asyncio.Task] = []


async def _entry_scan_loop() -> None:
    while True:
        try:
            # run_scan/record_and_notify_signals are synchronous (blocking
            # HTTP + DB calls) — offload to a thread so a slow scan cycle
            # never stalls the FastAPI event loop / dashboard requests.
            result = await asyncio.to_thread(run_scan)
            outcomes = await asyncio.to_thread(record_and_notify_signals, result.signals)
            logger.info(
                "Scheduled scan: %d signal(s) found, %d notified/journaled: %s",
                len(result.signals), len(outcomes), outcomes,
            )
        except DataUnavailable as exc:
            logger.warning("Scheduled scan skipped — market data unavailable: %s", exc)
        except Exception:
            logger.exception("Scheduled scan cycle failed unexpectedly — will retry next cycle.")
        await asyncio.sleep(settings.scan_loop_minutes * 60)


async def _exit_monitor_loop() -> None:
    from app.paper_trading.simulator import run_paper_trading_update

    while True:
        try:
            summary = await asyncio.to_thread(run_paper_trading_update)
            if summary["updated"]:
                logger.info("Scheduled exit check: %s", summary["updated"])
        except DataUnavailable as exc:
            logger.warning("Scheduled exit check skipped — market data unavailable: %s", exc)
        except Exception:
            logger.exception("Scheduled exit-monitor cycle failed unexpectedly — will retry next cycle.")
        await asyncio.sleep(settings.monitor_loop_minutes * 60)


def start() -> None:
    if not settings.enable_scheduler:
        logger.info("Scheduler disabled (ENABLE_SCHEDULER=false) — scans only run when triggered manually.")
        return
    logger.info(
        "Starting scheduler: entry scan every %dm, exit monitor every %dm.",
        settings.scan_loop_minutes, settings.monitor_loop_minutes,
    )
    _tasks.append(asyncio.create_task(_entry_scan_loop()))
    _tasks.append(asyncio.create_task(_exit_monitor_loop()))


def stop() -> None:
    for task in _tasks:
        task.cancel()
    _tasks.clear()
