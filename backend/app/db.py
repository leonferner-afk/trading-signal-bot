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


_engine = create_engine(f"sqlite:///{settings.db_path}", future=True)
SessionLocal = sessionmaker(bind=_engine, expire_on_commit=False, future=True)


def init_db() -> None:
    Base.metadata.create_all(_engine)


def get_session() -> Session:
    return SessionLocal()
