"""Real market-data client for US stocks via Yahoo Finance (`yfinance`).

No API key required — this wraps Yahoo Finance's public chart data, which
is genuinely live/historical market data, not a mock. Chosen because it's
the only zero-cost option that covers thousands of US tickers without a
paid plan (Alpha Vantage's free tier allows 25 requests/day — unusable for
scanning a watchlist; Finnhub's free tier no longer includes stock
candles). `yfinance` is unofficial (it scrapes Yahoo's own chart API,
there's no published SLA), so retries + a `DataUnavailable` escape hatch
matter even more here than for an official API — a request that fails
after retries must surface as "no data", never a guess.

If/when this project's budget changes, swapping in a paid provider (e.g.
Polygon.io, Twelve Data) means changing only this file — every other
module talks to it through the same `get_klines(symbol, interval, limit)`
shape used by the (removed) Binance client, and expects the same minimal
set of columns.
"""
from __future__ import annotations

import datetime as dt
import io
import math
import time
from dataclasses import dataclass

import httpx
import pandas as pd
import yfinance as yf
from curl_cffi import requests as curl_requests

from app.config import settings

BROWSER_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)

# yfinance hardcodes a 2014-era Chrome User-Agent on every Yahoo request
# (yfinance.data.YfData.user_agent_headers). Left as-is, that header
# clashes with curl_cffi's modern Chrome TLS fingerprint below — a
# mismatch between what the TLS handshake claims and what the HTTP
# header claims is itself a bot-detection signal. Align it with the
# Chrome version curl_cffi's "chrome" impersonation target presents.
yf.data.YfData.user_agent_headers = {"User-Agent": BROWSER_USER_AGENT}

REQUIRED_COLUMNS = ["open_time", "open", "high", "low", "close", "volume", "close_time"]

_INTRADAY_INTERVALS = {"1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h"}
_SHORT_INTRADAY = {"1m", "2m", "5m"}


class DataUnavailable(RuntimeError):
    """Raised when real market data cannot be retrieved.

    The rest of the system must treat this as NO SIGNAL, never fall back
    to placeholder or last-known-good data silently.
    """


def _period_for(interval: str, limit: int) -> str:
    """Yahoo's history() takes a period/date-range, not a bar count, so we
    request generously more calendar time than `limit` bars need and trim
    afterwards. Yahoo also caps how far back intraday data goes (60 days
    for 1-5m bars, ~2 years for 60-90m bars) regardless of what we ask for."""
    if interval in _INTRADAY_INTERVALS:
        return "60d" if interval in _SHORT_INTRADAY else "730d"
    if interval == "1wk":
        years = min(max(2, math.ceil(limit / 45)), 25)
        return f"{years}y"
    if interval == "1mo":
        return "25y"
    # Daily (and anything else): trading days ≈ 252/year; buffer generously
    # for weekends/holidays already excluded from that count.
    years = min(max(1, math.ceil(limit / 200)), 25)
    return f"{years}y"


def _rows_from_dataframe(df: pd.DataFrame, column_map: dict[str, str], limit: int) -> pd.DataFrame:
    df = df.rename(columns=column_map)
    df["close_time"] = pd.to_datetime(df["close_time"], utc=True)
    df["open_time"] = df["close_time"]
    df = df[REQUIRED_COLUMNS].dropna(subset=["open", "high", "low", "close", "volume"])
    if df.empty:
        raise RuntimeError("no usable rows")
    df = df.tail(limit).reset_index(drop=True)
    return df.set_index("close_time", drop=False)


def _fetch_stooq_daily(symbol: str, limit: int) -> pd.DataFrame:
    """Fallback for daily bars, used only once Yahoo has failed outright.
    Stooq is a completely separate, key-free CSV data source — an
    IP-level block or outage on Yahoo's side doesn't take this down too.
    Daily-only (no intraday history), which matches how this app actually
    scans (1d bars) so the fallback covers the real usage."""
    years = min(max(1, math.ceil(limit / 200)), 25)
    end = dt.date.today()
    start = end - dt.timedelta(days=years * 366)
    params = {
        "s": f"{symbol.lower()}.us",
        "d1": start.strftime("%Y%m%d"),
        "d2": end.strftime("%Y%m%d"),
        "i": "d",
    }
    resp = httpx.get(
        "https://stooq.com/q/d/l/",
        params=params,
        headers={"User-Agent": BROWSER_USER_AGENT},
        timeout=15.0,
        follow_redirects=True,
    )
    resp.raise_for_status()
    text = resp.text.strip()
    if not text or "Date" not in text.splitlines()[0]:
        raise RuntimeError(f"stooq: unexpected response for {symbol}: {text[:200]!r}")
    df = pd.read_csv(io.StringIO(text))
    return _rows_from_dataframe(
        df,
        {"Date": "close_time", "Open": "open", "High": "high", "Low": "low", "Close": "close", "Volume": "volume"},
        limit,
    )


@dataclass
class StockClient:
    max_retries: int = settings.max_retries
    backoff: float = settings.retry_backoff_seconds
    min_interval: float = settings.min_request_interval_seconds

    def __post_init__(self) -> None:
        self._last_request_at = 0.0
        # Yahoo's chart endpoint increasingly blocks/empties requests whose
        # TLS fingerprint doesn't look like a real browser — common on
        # shared cloud-host IPs (Railway, AWS, ...). curl_cffi impersonates
        # Chrome's TLS handshake, which a plain `requests` session can't.
        self._session = curl_requests.Session(impersonate="chrome")

    def __enter__(self) -> "StockClient":
        return self

    def __exit__(self, *exc) -> None:
        pass

    def close(self) -> None:
        pass

    def _throttle(self) -> None:
        elapsed = time.monotonic() - self._last_request_at
        wait = self.min_interval - elapsed
        if wait > 0:
            time.sleep(wait)

    def get_klines(self, symbol: str, interval: str, limit: int = 500) -> pd.DataFrame:
        """Fetch recent candles. Returns a DataFrame indexed by close_time
        (UTC), matching the shape the scanner/backtester expect.

        Yahoo's history index marks each bar by its trading-day (daily+)
        or bar-start (intraday) timestamp with no separate open/close
        split like Binance's kline schema has — `open_time` is set equal
        to `close_time` here since nothing downstream relies on it being
        distinct (see module docstring / the one call site that falls
        back to it, `backtest/engine.py`, only for the otherwise-unused
        very first bar of a series).
        """
        try:
            return self._fetch_yfinance(symbol, interval, limit)
        except DataUnavailable as exc:
            if interval != "1d":
                raise
            try:
                return _fetch_stooq_daily(symbol, limit)
            except Exception as stooq_exc:
                raise DataUnavailable(
                    f"both data providers failed for {symbol} {interval} — yfinance: {exc}; stooq: {stooq_exc}"
                ) from stooq_exc

    def _fetch_yfinance(self, symbol: str, interval: str, limit: int) -> pd.DataFrame:
        period = _period_for(interval, limit)
        last_error: Exception | None = None
        for attempt in range(1, self.max_retries + 1):
            self._throttle()
            try:
                self._last_request_at = time.monotonic()
                ticker = yf.Ticker(symbol.upper(), session=self._session)
                raw = ticker.history(period=period, interval=interval, auto_adjust=True)
                if raw is None or raw.empty:
                    raise RuntimeError(f"empty response for {symbol} {interval}")

                df = raw.reset_index()
                date_col = "Date" if "Date" in df.columns else "Datetime"
                return _rows_from_dataframe(
                    df,
                    {date_col: "close_time", "Open": "open", "High": "high", "Low": "low", "Close": "close", "Volume": "volume"},
                    limit,
                )
            except Exception as exc:  # yfinance surfaces requests/HTTP/JSON errors (and our own empty-response/no-rows signals), not one clean type
                last_error = exc
                if attempt < self.max_retries:
                    time.sleep(self.backoff * attempt)
        raise DataUnavailable(
            f"yfinance fetch for {symbol} {interval} failed after {self.max_retries} attempts: {last_error}"
        ) from last_error
