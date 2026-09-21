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
    # Market data provider (Yahoo Finance via `yfinance` — no API key
    # required, the only zero-cost option covering thousands of US
    # tickers). See app/data/stock_client.py for why.
    request_timeout_seconds: float = float(os.getenv("HTTP_TIMEOUT_SECONDS", "10"))
    max_retries: int = int(os.getenv("HTTP_MAX_RETRIES", "2"))
    retry_backoff_seconds: float = float(os.getenv("HTTP_RETRY_BACKOFF_SECONDS", "0.5"))
    min_request_interval_seconds: float = float(os.getenv("HTTP_MIN_INTERVAL_SECONDS", "0.15"))

    # How stale a candle close can be before the scanner refuses to score
    # it. Daily bars are timestamped at the trading day's date (not the
    # actual 4pm ET close), and markets are closed weekends/holidays, so
    # this needs several days of slack, unlike crypto's 24/7 5-minute one.
    max_data_age_seconds: int = int(os.getenv("MAX_DATA_AGE_SECONDS", str(5 * 24 * 3600)))

    # Starting watchlist — liquid, historically volatile US growth/momentum
    # names spanning several sectors (semis/AI, EV, biotech, fintech,
    # crypto-adjacent, cybersecurity, space), meant as an editable starting
    # point (change it in Settings), not a curated "best picks"
    # endorsement. Widened from an initial ~24 to ~50 names to meaningfully
    # increase the odds of catching a rare large mover somewhere in the
    # list, while staying liquid enough for reliable daily data — still a
    # watchlist, not the whole market, at $0 data budget; see README.
    watchlist: tuple[str, ...] = field(
        default_factory=lambda: tuple(
            _split_csv(
                os.getenv(
                    "WATCHLIST",
                    "NVDA,TSLA,AMD,PLTR,SMCI,MSTR,COIN,SOFI,RBLX,DKNG,CVNA,UPST,"
                    "AFRM,HOOD,RIVN,MARA,RIOT,IONQ,ARM,CRWD,NET,SNOW,SHOP,ROKU,"
                    "MU,MRVL,ON,MRNA,NVAX,CRSP,NTLA,NIO,LI,XPEV,ENPH,PLUG,FSLR,"
                    "SQ,OKTA,RKLB,CHWY,ETSY,W,CLSK,HUT,AI,SOUN,BBAI,BEAM,EDIT",
                )
            )
        )
    )
    # Daily bars — this is a swing/position-trade caller (weeks-to-months
    # horizon hunting large moves), not an intraday scalper.
    scan_interval: str = os.getenv("SCAN_INTERVAL", "1d")

    # Quality filter / ranking thresholds (section 8).
    score_watch_min: float = float(os.getenv("SCORE_WATCH_MIN", "70"))
    score_high_quality_min: float = float(os.getenv("SCORE_HIGH_QUALITY_MIN", "80"))
    score_exceptional_min: float = float(os.getenv("SCORE_EXCEPTIONAL_MIN", "90"))
    notify_min_score: float = float(os.getenv("NOTIFY_MIN_SCORE", "80"))

    # Costs applied in every backtest/paper trade — a strategy that is only
    # profitable before these is not profitable.
    fee_bps: float = float(os.getenv("FEE_BPS", "10"))          # 0.10% per fill (taker)
    slippage_bps: float = float(os.getenv("SLIPPAGE_BPS", "5"))  # 0.05% per fill

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
    enable_scheduler: bool = os.getenv("ENABLE_SCHEDULER", "false").lower() == "true"
    scan_loop_minutes: int = int(os.getenv("SCAN_LOOP_MINUTES", "60"))
    monitor_loop_minutes: int = int(os.getenv("MONITOR_LOOP_MINUTES", "60"))
    # Candle granularity used to monitor already-open positions for a
    # stop/target hit. Same as the entry timeframe by default (daily) —
    # intraday precision doesn't add much for a multi-week swing position.
    monitor_kline_interval: str = os.getenv("MONITOR_KLINE_INTERVAL", "1d")

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

    db_path: str = os.getenv("DB_PATH", "tradingbot.db")


settings = Settings()
