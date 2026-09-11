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


@dataclass(frozen=True)
class Settings:
    # Market data provider (Binance public REST — no API key required for
    # market data). Base URL is configurable so a mirror/region endpoint
    # can be swapped in without a code change.
    binance_base_url: str = os.getenv("BINANCE_BASE_URL", "https://api.binance.com")
    request_timeout_seconds: float = float(os.getenv("HTTP_TIMEOUT_SECONDS", "10"))
    max_retries: int = int(os.getenv("HTTP_MAX_RETRIES", "3"))
    retry_backoff_seconds: float = float(os.getenv("HTTP_RETRY_BACKOFF_SECONDS", "1.0"))
    min_request_interval_seconds: float = float(os.getenv("HTTP_MIN_INTERVAL_SECONDS", "0.15"))

    # How stale a candle close can be before the scanner refuses to score it.
    max_data_age_seconds: int = int(os.getenv("MAX_DATA_AGE_SECONDS", "300"))

    # Watchlist for the single supported market (crypto spot, via Binance).
    watchlist: tuple[str, ...] = field(
        default_factory=lambda: tuple(
            _split_csv(
                os.getenv(
                    "WATCHLIST",
                    "BTCUSDT,ETHUSDT,SOLUSDT,BNBUSDT,XRPUSDT,ADAUSDT,DOGEUSDT,AVAXUSDT",
                )
            )
        )
    )
    scan_interval: str = os.getenv("SCAN_INTERVAL", "1h")

    # Quality filter / ranking thresholds (section 8).
    score_watch_min: float = float(os.getenv("SCORE_WATCH_MIN", "70"))
    score_high_quality_min: float = float(os.getenv("SCORE_HIGH_QUALITY_MIN", "80"))
    score_exceptional_min: float = float(os.getenv("SCORE_EXCEPTIONAL_MIN", "90"))
    notify_min_score: float = float(os.getenv("NOTIFY_MIN_SCORE", "80"))

    # Costs applied in every backtest/paper trade — a strategy that is only
    # profitable before these is not profitable.
    fee_bps: float = float(os.getenv("FEE_BPS", "10"))          # 0.10% per fill (taker)
    slippage_bps: float = float(os.getenv("SLIPPAGE_BPS", "5"))  # 0.05% per fill

    # Optional news catalyst provider (CryptoPanic). If unset, the news
    # module explicitly reports "no data" rather than assuming anything.
    cryptopanic_api_key: str | None = os.getenv("CRYPTOPANIC_API_KEY") or None

    # Optional outbound webhook (Slack/Discord-compatible) for notifications.
    notify_webhook_url: str | None = os.getenv("NOTIFY_WEBHOOK_URL") or None

    # Telegram delivery for "KÖP NU" / "SÄLJ NU" alerts — the primary
    # notification channel. Both must be set for anything to send; missing
    # either one just logs a warning and skips delivery, it never blocks
    # the rest of the system.
    telegram_bot_token: str | None = os.getenv("TELEGRAM_BOT_TOKEN") or None
    telegram_chat_id: str | None = os.getenv("TELEGRAM_CHAT_ID") or None

    # Background scheduler: off by default so importing/testing the app
    # never silently starts network loops. Two separate cadences —
    # entries don't need to be checked as often as open positions do.
    enable_scheduler: bool = os.getenv("ENABLE_SCHEDULER", "false").lower() == "true"
    scan_loop_minutes: int = int(os.getenv("SCAN_LOOP_MINUTES", "30"))
    monitor_loop_minutes: int = int(os.getenv("MONITOR_LOOP_MINUTES", "5"))
    # Finer candle granularity used ONLY to monitor already-open positions
    # for a stop/target hit — independent of the (usually higher)
    # timeframe each strategy evaluates entries on.
    monitor_kline_interval: str = os.getenv("MONITOR_KLINE_INTERVAL", "5m")

    # Optional "quiet hours" gate on ENTRY ("köp nu") notifications only —
    # exit ("sälj nu") alerts always fire regardless, since once you're in
    # a position you want to know it closed no matter the hour. Off by
    # default (crypto trades 24/7, so there's no gate unless you ask for
    # one). Days are lowercase 3-letter, comma-separated.
    trading_hours_enabled: bool = os.getenv("TRADING_HOURS_ENABLED", "false").lower() == "true"
    trading_hours_start: str = os.getenv("TRADING_HOURS_START", "09:00")
    trading_hours_end: str = os.getenv("TRADING_HOURS_END", "22:00")
    trading_hours_timezone: str = os.getenv("TRADING_HOURS_TIMEZONE", "Europe/Stockholm")
    trading_days: tuple[str, ...] = field(
        default_factory=lambda: tuple(
            d.strip().lower()
            for d in os.getenv("TRADING_DAYS", "mon,tue,wed,thu,fri,sat,sun").split(",")
            if d.strip()
        )
    )

    db_path: str = os.getenv("DB_PATH", "sagoton.db")


settings = Settings()
