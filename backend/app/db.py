"""SQLite persistence via SQLAlchemy (section 17).

Three tables:
  - signals: every signal the scanner produced (score >= WATCH threshold),
    with the full transparent breakdown, so nothing shown on the dashboard
    is reconstructed after the fact.
  - paper_trades: forward-simulated outcomes for each signal (section 13).
  - backtest_runs: persisted results of historical backtests (section 11),
    kept separate from paper trades since they cover different data.
"""
from __future__ import annotations

import datetime as dt
import json

from sqlalchemy import JSON, Boolean, DateTime, Float, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

from app.config import settings


class Base(DeclarativeBase):
    pass


class SignalRecord(Base):
    __tablename__ = "signals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[dt.datetime] = mapped_column(DateTime, default=lambda: dt.datetime.now(dt.timezone.utc))
    timestamp: Mapped[str] = mapped_column(String)
    symbol: Mapped[str] = mapped_column(String, index=True)
    direction: Mapped[str] = mapped_column(String)
    strategy: Mapped[str] = mapped_column(String)
    entry: Mapped[float] = mapped_column(Float)
    target: Mapped[float] = mapped_column(Float)
    stop: Mapped[float] = mapped_column(Float)
    risk_pct: Mapped[float] = mapped_column(Float)
    reward_pct: Mapped[float] = mapped_column(Float)
    rr_ratio: Mapped[float] = mapped_column(Float)
    score: Mapped[float] = mapped_column(Float)
    tier: Mapped[str] = mapped_column(String)
    market_regime: Mapped[str] = mapped_column(String)
    market_wide_risk: Mapped[str] = mapped_column(String)
    features_json: Mapped[str] = mapped_column(JSON)  # full score breakdown + reasons
    news_json: Mapped[str] = mapped_column(JSON)
    historical_probability_json: Mapped[str] = mapped_column(JSON)  # from backtest lookup, if any
    result: Mapped[str] = mapped_column(String, default="OPEN")  # OPEN / TARGET_HIT / STOP_HIT / EXPIRED
    max_favorable_excursion_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    max_adverse_excursion_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    holding_time_minutes: Mapped[float | None] = mapped_column(Float, nullable=True)
    closed_at: Mapped[dt.datetime | None] = mapped_column(DateTime, nullable=True)
    # Realized outcome, measured the way the trade would actually have
    # gone: bought at the open after the signal, sold at the level (or the
    # gap-open through it), fees and slippage included. `entry` above stays
    # the planned price the notification quoted.
    fill_price: Mapped[float | None] = mapped_column(Float, nullable=True)
    exit_price: Mapped[float | None] = mapped_column(Float, nullable=True)
    return_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    r_multiple: Mapped[float | None] = mapped_column(Float, nullable=True)


class BacktestRun(Base):
    __tablename__ = "backtest_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[dt.datetime] = mapped_column(DateTime, default=lambda: dt.datetime.now(dt.timezone.utc))
    symbol: Mapped[str] = mapped_column(String)
    interval: Mapped[str] = mapped_column(String)
    strategy: Mapped[str] = mapped_column(String)
    start: Mapped[str] = mapped_column(String)
    end: Mapped[str] = mapped_column(String)
    split_json: Mapped[str] = mapped_column(JSON)  # {"train": {...}, "validation": {...}, "out_of_sample": {...}}
    walk_forward_json: Mapped[str] = mapped_column(JSON)
    reliable: Mapped[bool] = mapped_column(Boolean)
    reliability_reason: Mapped[str] = mapped_column(String)
    # {"common_hours_utc": [14, 15, 18]} — real entry-hour histogram from
    # this run's own trades, used to tell the user roughly when this setup
    # tends to trigger. Empty/absent until a backtest has been run.
    timing_pattern_json: Mapped[str] = mapped_column(JSON, default="{}")


class AppSettingsRow(Base):
    """Single-row table (id fixed to 1) of user-editable runtime overrides.

    Every column is nullable — NULL means "use the .env / default value".
    This lets day-to-day config (Telegram credentials, watchlist, trading
    hours, thresholds) be changed from the dashboard's Settings tab without
    editing files or restarting the process, while .env stays the
    source of truth for anything the user hasn't explicitly overridden.
    """
    __tablename__ = "app_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)
    updated_at: Mapped[dt.datetime] = mapped_column(DateTime, default=lambda: dt.datetime.now(dt.timezone.utc))

    telegram_bot_token: Mapped[str | None] = mapped_column(String, nullable=True)
    telegram_chat_id: Mapped[str | None] = mapped_column(String, nullable=True)
    watchlist_csv: Mapped[str | None] = mapped_column(String, nullable=True)

    notify_min_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    score_watch_min: Mapped[float | None] = mapped_column(Float, nullable=True)
    score_high_quality_min: Mapped[float | None] = mapped_column(Float, nullable=True)
    score_exceptional_min: Mapped[float | None] = mapped_column(Float, nullable=True)

    enable_scheduler: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    scan_loop_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    monitor_loop_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)

    trading_hours_enabled: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    trading_hours_start: Mapped[str | None] = mapped_column(String, nullable=True)
    trading_hours_end: Mapped[str | None] = mapped_column(String, nullable=True)
    trading_hours_timezone: Mapped[str | None] = mapped_column(String, nullable=True)
    trading_days_csv: Mapped[str | None] = mapped_column(String, nullable=True)

    portfolio_size_usd: Mapped[float | None] = mapped_column(Float, nullable=True)
    risk_per_trade_pct: Mapped[float | None] = mapped_column(Float, nullable=True)


_engine = create_engine(f"sqlite:///{settings.db_path}", future=True)
SessionLocal = sessionmaker(bind=_engine, expire_on_commit=False, future=True)


def init_db() -> None:
    Base.metadata.create_all(_engine)
    _add_missing_columns()


def _add_missing_columns() -> None:
    """`create_all` never alters an existing table, and the bot's SQLite
    file persists across runs — so columns added to a model later are
    added here (nullable, so existing rows stay valid)."""
    from sqlalchemy import inspect, text

    inspector = inspect(_engine)
    with _engine.begin() as conn:
        for table in Base.metadata.sorted_tables:
            existing = {c["name"] for c in inspector.get_columns(table.name)}
            for column in table.columns:
                if column.name not in existing:
                    conn.execute(text(f'ALTER TABLE "{table.name}" ADD COLUMN "{column.name}" {column.type.compile(_engine.dialect)}'))


def get_session() -> Session:
    return SessionLocal()
