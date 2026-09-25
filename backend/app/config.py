"""Runtime configuration, loaded entirely from environment variables.

No secret or endpoint is ever hardcoded here — this is the one place the
rest of the codebase reads configuration from, per the "secrets live in
env vars" requirement.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field


def _split_csv(value: str) -> list[str]:
    return [v.strip().upper() for v in value.split(",") if v.strip()]


def _env(name: str, default: str) -> str:
    """Like os.getenv, but an empty value counts as unset — CI systems pass
    unset secrets/variables through as empty strings."""
    value = os.getenv(name)
    return value if value not in (None, "") else default


def _default_universe() -> tuple[str, ...]:
    from app.universe import default_universe

    return default_universe()


@dataclass(frozen=True)
class Settings:
    # Market data provider (Yahoo Finance via `yfinance` — no API key
    # required, the only zero-cost option covering thousands of US
    # tickers). See app/data/stock_client.py for why.
    request_timeout_seconds: float = float(_env("HTTP_TIMEOUT_SECONDS", "10"))
    max_retries: int = int(_env("HTTP_MAX_RETRIES", "2"))
    retry_backoff_seconds: float = float(_env("HTTP_RETRY_BACKOFF_SECONDS", "0.5"))
    min_request_interval_seconds: float = float(_env("HTTP_MIN_INTERVAL_SECONDS", "0.15"))

    # Optional fallback data source for daily bars (free key at
    # twelvedata.com), used only for symbols Yahoo fails to return.
    twelvedata_api_key: str = _env("TWELVE_DATA_API_KEY", "")

    # How stale the newest *closed* daily bar may be before the scanner
    # refuses to score a symbol. Covers weekends and market holidays.
    max_data_age_seconds: int = int(_env("MAX_DATA_AGE_SECONDS", str(5 * 24 * 3600)))

    # Scan universe: WATCHLIST (comma-separated) if set, otherwise the
    # ~200-stock default in app/universe.py.
    watchlist: tuple[str, ...] = field(
        default_factory=lambda: tuple(_split_csv(os.environ["WATCHLIST"]))
        if os.getenv("WATCHLIST")
        else _default_universe()
    )
    # Daily bars — this is a swing/position-trade caller (weeks-to-months
    # horizon hunting large moves), not an intraday scalper.
    scan_interval: str = _env("SCAN_INTERVAL", "1d")

    # Quality filter / ranking thresholds (section 8).
    score_watch_min: float = float(_env("SCORE_WATCH_MIN", "70"))
    score_high_quality_min: float = float(_env("SCORE_HIGH_QUALITY_MIN", "80"))
    score_exceptional_min: float = float(_env("SCORE_EXCEPTIONAL_MIN", "90"))
    notify_min_score: float = float(_env("NOTIFY_MIN_SCORE", "80"))

    # Costs applied in every backtest/paper trade — a strategy that is only
    # profitable before these is not profitable.
    fee_bps: float = float(_env("FEE_BPS", "10"))          # 0.10% per fill (taker)
    slippage_bps: float = float(_env("SLIPPAGE_BPS", "5"))  # 0.05% per fill

    # No stock news/catalyst provider is wired up yet — see
    # app/data/news_client.py for the (provider-agnostic) scoring logic
    # and where a real source would plug in. Catalyst honestly scores
    # 0/10 with a stated reason until one exists.

    # Optional outbound webhook (Slack/Discord-compatible) for notifications.
    notify_webhook_url: str | None = os.getenv("NOTIFY_WEBHOOK_URL") or None

    # Telegram delivery for "KÖP NU" / "SÄLJ NU" alerts — the primary
    # notification channel. Both must be set for anything to send; missing
    # either one just logs a warning and skips delivery, it never blocks
    # the rest of the system.
    telegram_bot_token: str | None = os.getenv("TELEGRAM_BOT_TOKEN") or None
    telegram_chat_id: str | None = os.getenv("TELEGRAM_CHAT_ID") or None

    # Background scheduler: off by default so importing/testing the app
    # never silently starts network loops. A daily bar doesn't change
    # until the next trading day closes, so — unlike the old intraday
    # crypto cadence (30m/5m) — checking hourly is already more than
    # often enough for both new entries and open-position monitoring;
    # it mainly exists to catch you up promptly after each day's close.
    enable_scheduler: bool = _env("ENABLE_SCHEDULER", "false").lower() == "true"
    scan_loop_minutes: int = int(_env("SCAN_LOOP_MINUTES", "60"))
    monitor_loop_minutes: int = int(_env("MONITOR_LOOP_MINUTES", "60"))
    # Candle granularity used to monitor already-open positions for a
    # stop/target hit. Same as the entry timeframe by default (daily) —
    # intraday precision doesn't add much for a multi-week swing position.
    monitor_kline_interval: str = _env("MONITOR_KLINE_INTERVAL", "1d")

    # Optional "quiet hours" gate on ENTRY ("köp nu") notifications only —
    # exit ("sälj nu") alerts always fire regardless, since once you're in
    # a position you want to know it closed no matter the hour. Off by
    # default (crypto trades 24/7, so there's no gate unless you ask for
    # one). Days are lowercase 3-letter, comma-separated.
    trading_hours_enabled: bool = _env("TRADING_HOURS_ENABLED", "false").lower() == "true"
    trading_hours_start: str = _env("TRADING_HOURS_START", "09:00")
    trading_hours_end: str = _env("TRADING_HOURS_END", "22:00")
    trading_hours_timezone: str = _env("TRADING_HOURS_TIMEZONE", "Europe/Stockholm")
    trading_days: tuple[str, ...] = field(
        default_factory=lambda: tuple(
            d.strip().lower()
            for d in _env("TRADING_DAYS", "mon,tue,wed,thu,fri,sat,sun").split(",")
            if d.strip()
        )
    )

    db_path: str = _env("DB_PATH", "tradingbot.db")

    # Position sizing: fixed-fractional risk. Each BUY is sized so hitting
    # the stop loses RISK_PER_TRADE_PCT of PORTFOLIO_SIZE_USD.
    portfolio_size_usd: float = float(_env("PORTFOLIO_SIZE_USD", "10000"))
    risk_per_trade_pct: float = float(_env("RISK_PER_TRADE_PCT", "1.0"))
    # Never hold more than this many positions at once, and never open more
    # than this many new ones on a single day — the best-scoring go first.
    max_open_positions: int = int(_env("MAX_OPEN_POSITIONS", "8"))
    max_new_buys_per_day: int = int(_env("MAX_NEW_BUYS_PER_DAY", "3"))


settings = Settings()
