"""Session-wide test setup: points the app's DB engine at a throwaway
in-memory SQLite database with all tables created, so any test that
transitively calls `get_effective_settings()` (trading_hours, notifier,
scoring, scanner) finds a real `app_settings` table instead of hitting
whatever `DB_PATH` resolves to on disk. Individual test files that need
full isolation between tests (e.g. dedupe/runtime-settings tests) still
swap in their own fresh in-memory engine via their own fixtures — this
just guarantees a working baseline for everything else.
"""
from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import app.db as db

_engine = create_engine("sqlite:///:memory:", future=True)
db.Base.metadata.create_all(_engine)
db._engine = _engine
db.SessionLocal = sessionmaker(bind=_engine, expire_on_commit=False, future=True)
