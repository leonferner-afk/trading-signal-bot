"""Effective runtime settings = env-var defaults (`app.config.settings`)
with any DB-stored overrides layered on top.

This is the ONE place day-to-day, user-editable config is read from —
Telegram credentials, watchlist, score thresholds, trading hours,
scheduler cadence, and position-sizing — so the Settings tab can change
any of it live, without a restart or touching `.env`. `.env` stays the
fallback for anything the user hasn't explicitly overridden via the
dashboard, and remains the only place secrets are provisioned initially.
"""
from __future__ import annotations

from dataclasses import dataclass

from app.config import settings as env_settings
from app.db import AppSettingsRow, get_session

OVERRIDABLE_FIELDS = (
    "telegram_bot_token", "telegram_chat_id", "watchlist_csv",
    "notify_min_score", "score_watch_min", "score_high_quality_min", "score_exceptional_min",
    "enable_scheduler", "scan_loop_minutes", "monitor_loop_minutes",
    "trading_hours_enabled", "trading_hours_start", "trading_hours_end",
    "trading_hours_timezone", "trading_days_csv",
    "portfolio_size_usd", "risk_per_trade_pct",
)


@dataclass(frozen=True)
class EffectiveSettings:
    telegram_bot_token: str | None
    telegram_chat_id: str | None
    watchlist: tuple[str, ...]
    notify_min_score: float
    score_watch_min: float
    score_high_quality_min: float
    score_exceptional_min: float
    enable_scheduler: bool
    scan_loop_minutes: int
    monitor_loop_minutes: int
    trading_hours_enabled: bool
    trading_hours_start: str
    trading_hours_end: str
    trading_hours_timezone: str
    trading_days: tuple[str, ...]
    portfolio_size_usd: float
    risk_per_trade_pct: float
    overridden_fields: tuple[str, ...]


def _get_or_create_row(session) -> AppSettingsRow:
    row = session.get(AppSettingsRow, 1)
    if row is None:
        row = AppSettingsRow(id=1)
        session.add(row)
        session.commit()
    return row


def get_effective_settings() -> EffectiveSettings:
    with get_session() as session:
        row = _get_or_create_row(session)
        overridden = tuple(f for f in OVERRIDABLE_FIELDS if getattr(row, f) is not None)

        return EffectiveSettings(
            telegram_bot_token=row.telegram_bot_token or env_settings.telegram_bot_token,
            telegram_chat_id=row.telegram_chat_id or env_settings.telegram_chat_id,
            watchlist=tuple(row.watchlist_csv.split(",")) if row.watchlist_csv else env_settings.watchlist,
            notify_min_score=row.notify_min_score if row.notify_min_score is not None else env_settings.notify_min_score,
            score_watch_min=row.score_watch_min if row.score_watch_min is not None else env_settings.score_watch_min,
            score_high_quality_min=row.score_high_quality_min if row.score_high_quality_min is not None else env_settings.score_high_quality_min,
            score_exceptional_min=row.score_exceptional_min if row.score_exceptional_min is not None else env_settings.score_exceptional_min,
            enable_scheduler=row.enable_scheduler if row.enable_scheduler is not None else env_settings.enable_scheduler,
            scan_loop_minutes=row.scan_loop_minutes if row.scan_loop_minutes is not None else env_settings.scan_loop_minutes,
            monitor_loop_minutes=row.monitor_loop_minutes if row.monitor_loop_minutes is not None else env_settings.monitor_loop_minutes,
            trading_hours_enabled=row.trading_hours_enabled if row.trading_hours_enabled is not None else env_settings.trading_hours_enabled,
            trading_hours_start=row.trading_hours_start or env_settings.trading_hours_start,
            trading_hours_end=row.trading_hours_end or env_settings.trading_hours_end,
            trading_hours_timezone=row.trading_hours_timezone or env_settings.trading_hours_timezone,
            trading_days=tuple(row.trading_days_csv.split(",")) if row.trading_days_csv else env_settings.trading_days,
            portfolio_size_usd=row.portfolio_size_usd if row.portfolio_size_usd is not None else env_settings.portfolio_size_usd,
            risk_per_trade_pct=row.risk_per_trade_pct if row.risk_per_trade_pct is not None else env_settings.risk_per_trade_pct,
            overridden_fields=overridden,
        )


def update_settings_overrides(**kwargs) -> EffectiveSettings:
    """Sets or clears overrides. Pass a value to override that field, or
    None/"" to clear the override and fall back to the .env default.
    Unknown keys are rejected loudly rather than silently ignored."""
    unknown = set(kwargs) - set(OVERRIDABLE_FIELDS) - {"watchlist", "trading_days"}
    if unknown:
        raise ValueError(f"Unknown settings field(s): {sorted(unknown)}")

    if "watchlist" in kwargs:
        wl = kwargs.pop("watchlist")
        kwargs["watchlist_csv"] = ",".join(s.strip().upper() for s in wl if s.strip()) if wl else None
    if "trading_days" in kwargs:
        days = kwargs.pop("trading_days")
        kwargs["trading_days_csv"] = ",".join(d.strip().lower() for d in days if d.strip()) if days else None

    with get_session() as session:
        row = _get_or_create_row(session)
        for field, value in kwargs.items():
            setattr(row, field, value if value != "" else None)
        import datetime as dt

        row.updated_at = dt.datetime.now(dt.timezone.utc)
        session.add(row)
        session.commit()

    return get_effective_settings()
