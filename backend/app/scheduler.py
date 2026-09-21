"""Background scheduler: the two loops that make notifications happen
without you having to click anything.

  - entry_scan_loop:   every SCAN_LOOP_MINUTES, scans the watchlist for
                        new "köp nu" setups (same pipeline as the manual
                        Run Scan button).
  - exit_monitor_loop: every MONITOR_LOOP_MINUTES, checks every OPEN
                        signal against fresh, finer-grained price data and
                        fires "sälj nu" the moment one resolves.

Both loops always run once the app starts, but each cycle re-reads the
*effective* settings (env + any dashboard Settings-tab override) before
deciding whether to actually do anything — so flipping "Enable scheduler"
off/on, or changing the cadence, in the Settings tab takes effect within
one short poll, no restart needed. When disabled, each loop just polls
every 60s to notice re-enablement rather than doing real work.

A single bad cycle (a network blip, a temporarily unreachable exchange)
is logged and the loop keeps going — it never crashes the app or stops
watching your open positions.
"""
from __future__ import annotations

import asyncio
import logging

from app.data.stock_client import DataUnavailable
from app.pipeline import record_and_notify_signals
from app.runtime_settings import get_effective_settings
from app.scanner.scanner import run_scan

logger = logging.getLogger("tradingbot.scheduler")

_DISABLED_POLL_SECONDS = 60
_tasks: list[asyncio.Task] = []


async def _entry_scan_loop() -> None:
    while True:
        live = get_effective_settings()
        if not live.enable_scheduler:
            await asyncio.sleep(_DISABLED_POLL_SECONDS)
            continue
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
        await asyncio.sleep(max(1, get_effective_settings().scan_loop_minutes) * 60)


async def _exit_monitor_loop() -> None:
    from app.paper_trading.simulator import run_paper_trading_update

    while True:
        live = get_effective_settings()
        if not live.enable_scheduler:
            await asyncio.sleep(_DISABLED_POLL_SECONDS)
            continue
        try:
            summary = await asyncio.to_thread(run_paper_trading_update)
            if summary["updated"]:
                logger.info("Scheduled exit check: %s", summary["updated"])
        except DataUnavailable as exc:
            logger.warning("Scheduled exit check skipped — market data unavailable: %s", exc)
        except Exception:
            logger.exception("Scheduled exit-monitor cycle failed unexpectedly — will retry next cycle.")
        await asyncio.sleep(max(1, get_effective_settings().monitor_loop_minutes) * 60)


def start() -> None:
    live = get_effective_settings()
    logger.info(
        "Scheduler loops starting (currently %s). Entry scan every %dm, exit monitor every %dm when enabled — "
        "toggle live from the dashboard Settings tab.",
        "ENABLED" if live.enable_scheduler else "disabled",
        live.scan_loop_minutes, live.monitor_loop_minutes,
    )
    _tasks.append(asyncio.create_task(_entry_scan_loop()))
    _tasks.append(asyncio.create_task(_exit_monitor_loop()))


def stop() -> None:
    for task in _tasks:
        task.cancel()
    _tasks.clear()
