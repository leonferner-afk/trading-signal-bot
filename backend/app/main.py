"""FastAPI application wiring the scanner, journal, backtester, paper
trading simulator and notifier together, and serving the dashboard.

Every endpoint here either returns real, computed data or an explicit
empty/error state — nothing is a stub that fabricates numbers.
"""
from __future__ import annotations

import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles

from app.backtest.engine import run_backtest
from app.backtest.metrics import compute_metrics, entry_hour_timing_pattern
from app.backtest.walk_forward import train_validation_oos_split, walk_forward_analysis
from pydantic import BaseModel

from app.config import settings
from app.data.stock_client import DataUnavailable, StockClient
from app.db import init_db
from app.journal import repository as journal_repo
from app.pipeline import historical_probability_for, record_and_notify_signals
from app.runtime_settings import get_effective_settings, update_settings_overrides
from app.scanner.scanner import enrich, run_scan
from app.strategies import breakout, momentum, reversal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("tradingbot.api")

STRATEGY_MODULES = {"breakout": breakout, "momentum": momentum, "reversal": reversal}

app = FastAPI(title="Trading Signal Bot", version="0.1.0")


@app.get("/api/debug/env")
def debug_env() -> dict:
    """Read-only diagnostic: confirms whether an env var actually reached
    this running process, without ever exposing its value. Exists purely
    to debug "I set the variable but the app says it's missing" deploy
    issues from the browser, without digging through host platform logs."""
    import os

    key = os.environ.get("TWELVE_DATA_API_KEY", "")
    return {
        "TWELVE_DATA_API_KEY_present_in_os_environ": bool(key),
        "TWELVE_DATA_API_KEY_length": len(key),
        "settings_twelvedata_api_key_present": bool(settings.twelvedata_api_key),
        "settings_twelvedata_api_key_length": len(settings.twelvedata_api_key),
    }


@app.on_event("startup")
def _startup() -> None:
    init_db()
    from app import scheduler

    scheduler.start()


@app.on_event("shutdown")
def _shutdown() -> None:
    from app import scheduler

    scheduler.stop()


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/api/config")
def get_config() -> dict:
    live = get_effective_settings()
    return {
        "watchlist": list(live.watchlist),
        "scan_interval": settings.scan_interval,
        "score_watch_min": live.score_watch_min,
        "score_high_quality_min": live.score_high_quality_min,
        "score_exceptional_min": live.score_exceptional_min,
        "fee_bps": settings.fee_bps,
        "slippage_bps": settings.slippage_bps,
        "news_configured": False,  # no stock news provider wired up yet — see app/data/news_client.py
        "webhook_configured": settings.notify_webhook_url is not None,
        "telegram_configured": bool(live.telegram_bot_token and live.telegram_chat_id),
        "scheduler_enabled": live.enable_scheduler,
        "scan_loop_minutes": live.scan_loop_minutes,
        "monitor_loop_minutes": live.monitor_loop_minutes,
        "trading_hours_enabled": live.trading_hours_enabled,
        "trading_hours_start": live.trading_hours_start,
        "trading_hours_end": live.trading_hours_end,
        "trading_hours_timezone": live.trading_hours_timezone,
        "trading_days": list(live.trading_days),
        "portfolio_size_usd": live.portfolio_size_usd,
        "risk_per_trade_pct": live.risk_per_trade_pct,
    }


class SettingsUpdate(BaseModel):
    telegram_bot_token: str | None = None
    telegram_chat_id: str | None = None
    watchlist: list[str] | None = None
    notify_min_score: float | None = None
    score_watch_min: float | None = None
    score_high_quality_min: float | None = None
    score_exceptional_min: float | None = None
    enable_scheduler: bool | None = None
    scan_loop_minutes: int | None = None
    monitor_loop_minutes: int | None = None
    trading_hours_enabled: bool | None = None
    trading_hours_start: str | None = None
    trading_hours_end: str | None = None
    trading_hours_timezone: str | None = None
    trading_days: list[str] | None = None
    portfolio_size_usd: float | None = None
    risk_per_trade_pct: float | None = None


@app.get("/api/settings")
def get_settings() -> dict:
    live = get_effective_settings()
    return {
        "telegram_bot_token": live.telegram_bot_token,
        "telegram_chat_id": live.telegram_chat_id,
        "watchlist": list(live.watchlist),
        "notify_min_score": live.notify_min_score,
        "score_watch_min": live.score_watch_min,
        "score_high_quality_min": live.score_high_quality_min,
        "score_exceptional_min": live.score_exceptional_min,
        "enable_scheduler": live.enable_scheduler,
        "scan_loop_minutes": live.scan_loop_minutes,
        "monitor_loop_minutes": live.monitor_loop_minutes,
        "trading_hours_enabled": live.trading_hours_enabled,
        "trading_hours_start": live.trading_hours_start,
        "trading_hours_end": live.trading_hours_end,
        "trading_hours_timezone": live.trading_hours_timezone,
        "trading_days": list(live.trading_days),
        "portfolio_size_usd": live.portfolio_size_usd,
        "risk_per_trade_pct": live.risk_per_trade_pct,
        "overridden_fields": list(live.overridden_fields),
    }


@app.post("/api/settings")
def post_settings(update: SettingsUpdate) -> dict:
    """Only fields present in the request body are changed — a field set
    to null clears that override back to the .env default. Takes effect
    immediately; the scheduler loops pick up cadence/enabled changes
    within ~60s, everything else on the next scan/notification."""
    payload = update.model_dump(exclude_unset=True)
    try:
        update_settings_overrides(**payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return get_settings()


@app.post("/api/scan")
def scan() -> dict:
    from dataclasses import asdict

    from app.risk.position_sizing import compute_position_size

    try:
        result = run_scan()
    except DataUnavailable as exc:
        raise HTTPException(status_code=502, detail=f"Market data unavailable: {exc}") from exc

    notify_outcomes = record_and_notify_signals(result.signals)
    live = get_effective_settings()

    return {
        "scanned_at": result.scanned_at,
        "watchlist": result.watchlist,
        "market_wide_risk": result.market_wide_risk,
        "signal_count": len(result.signals),
        "signals": [
            {
                "symbol": s.symbol,
                "strategy": s.strategy,
                "direction": s.direction,
                "score": s.score,
                "tier": s.tier,
                "entry": s.entry,
                "stop": s.stop,
                "target": s.target,
                "risk_pct": s.risk_pct,
                "reward_pct": s.reward_pct,
                "rr_ratio": s.rr_ratio,
                "invalidation": s.invalidation,
                "invalidation_reason": s.invalidation_reason,
                "reasons": s.reasons,
                "regime_label": s.regime_label,
                "breakdown": s.breakdown.__dict__,
                "warning": s.warning,
                "historical_probability": historical_probability_for(s.symbol, s.strategy),
                "position_size": asdict(compute_position_size(s.entry, s.stop, live.portfolio_size_usd, live.risk_per_trade_pct))
                if s.direction == "LONG" else None,
            }
            for s in result.signals
        ],
        "notify_outcomes": notify_outcomes,
        "no_trade_summary": result.no_trade_summary,
        "skipped": [{"symbol": s.symbol, "reason": s.reason} for s in result.skipped],
        "message": "NO HIGH-CONVICTION SETUPS TODAY." if not result.signals else None,
    }


@app.get("/api/signals/top")
def top_signals(limit: int = Query(10, ge=1, le=50)) -> dict:
    records = journal_repo.list_signals(limit=limit)
    return {
        "signals": [
            {
                "id": r.id,
                "created_at": r.created_at.isoformat(),
                "symbol": r.symbol,
                "strategy": r.strategy,
                "direction": r.direction,
                "entry": r.entry,
                "target": r.target,
                "stop": r.stop,
                "score": r.score,
                "tier": r.tier,
                "market_regime": r.market_regime,
                "result": r.result,
            }
            for r in records
        ]
    }


@app.get("/api/journal")
def journal(limit: int = Query(200, ge=1, le=1000)) -> dict:
    import json

    records = journal_repo.list_signals(limit=limit)
    return {
        "entries": [
            {
                "id": r.id,
                "timestamp": r.timestamp,
                "symbol": r.symbol,
                "direction": r.direction,
                "entry": r.entry,
                "target": r.target,
                "stop": r.stop,
                "score": r.score,
                "strategy": r.strategy,
                "market_regime": r.market_regime,
                "features": json.loads(r.features_json),
                "news": json.loads(r.news_json),
                "historical_probability": json.loads(r.historical_probability_json),
                "result": r.result,
                "max_favorable_excursion": r.max_favorable_excursion_pct,
                "max_adverse_excursion": r.max_adverse_excursion_pct,
                "holding_time_minutes": r.holding_time_minutes,
            }
            for r in records
        ]
    }


@app.get("/api/performance")
def performance() -> dict:
    return journal_repo.performance_summary()


@app.get("/api/performance/equity-curve")
def equity_curve() -> dict:
    return {"points": journal_repo.equity_curve()}


@app.post("/api/paper-trading/update")
def paper_trading_update() -> dict:
    from app.paper_trading.simulator import run_paper_trading_update

    return run_paper_trading_update()


@app.post("/api/backtest/run")
def backtest_run(
    symbol: str = Query(...),
    strategy: str = Query(..., description="breakout | momentum | reversal"),
    interval: str = Query("1d"),
    limit: int = Query(1000, ge=210, le=1000),
) -> dict:
    if strategy not in STRATEGY_MODULES:
        raise HTTPException(status_code=400, detail=f"Unknown strategy '{strategy}'. Choose from {list(STRATEGY_MODULES)}.")

    try:
        with StockClient() as client:
            raw = client.get_klines(symbol, interval, limit=limit)
    except DataUnavailable as exc:
        raise HTTPException(status_code=502, detail=f"Market data unavailable: {exc}") from exc

    df = enrich(raw)
    trades = run_backtest(df, STRATEGY_MODULES[strategy], symbol, settings.fee_bps, settings.slippage_bps)
    split = train_validation_oos_split(trades)
    walk_forward = walk_forward_analysis(trades)

    split_dict = {
        "train": split.train.to_dict(),
        "validation": split.validation.to_dict(),
        "out_of_sample": split.out_of_sample.to_dict(),
        "reliable": split.reliable,
        "reliability_reason": split.reliability_reason,
    }
    wf_dict = {
        "windows": [
            {"window_index": w.window_index, "start": w.start, "end": w.end, "metrics": w.metrics.to_dict()}
            for w in walk_forward.windows
        ],
        "consistent": walk_forward.consistent,
        "consistency_reason": walk_forward.consistency_reason,
    }

    timing_pattern = entry_hour_timing_pattern(split.out_of_sample_trades or [])

    journal_repo.save_backtest_run(
        symbol=symbol, interval=interval, strategy=strategy,
        start=str(df["close_time"].iloc[0]), end=str(df["close_time"].iloc[-1]),
        split=split_dict, walk_forward=wf_dict,
        reliable=split.reliable, reliability_reason=split.reliability_reason,
        timing_pattern=timing_pattern,
    )

    overall = compute_metrics(trades)

    return {
        "symbol": symbol, "strategy": strategy, "interval": interval,
        "bars_analyzed": len(df),
        "period": {"start": str(df["close_time"].iloc[0]), "end": str(df["close_time"].iloc[-1])},
        "fees_slippage": {"fee_bps": settings.fee_bps, "slippage_bps": settings.slippage_bps},
        "overall": overall.to_dict(),
        "split": split_dict,
        "walk_forward": wf_dict,
        "timing_pattern": timing_pattern,
    }


@app.get("/api/backtest/runs")
def backtest_runs() -> dict:
    import json

    runs = journal_repo.list_backtest_runs()
    return {
        "runs": [
            {
                "id": r.id,
                "created_at": r.created_at.isoformat(),
                "symbol": r.symbol,
                "strategy": r.strategy,
                "interval": r.interval,
                "start": r.start,
                "end": r.end,
                "split": json.loads(r.split_json),
                "reliable": r.reliable,
                "reliability_reason": r.reliability_reason,
            }
            for r in runs
        ]
    }


_frontend_dir = Path(__file__).resolve().parent.parent / "frontend"
if _frontend_dir.exists():
    app.mount("/", StaticFiles(directory=str(_frontend_dir), html=True), name="frontend")
