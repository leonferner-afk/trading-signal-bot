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

    db_path: str = os.getenv("DB_PATH", "sagoton.db")


settings = Settings()
