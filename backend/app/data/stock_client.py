"""Real market-data client for US stocks.

Primary source: Yahoo Finance via `yfinance` (no key). Verified working
from GitHub Actions runners, which is where the bot runs day to day.
Optional fallback for daily bars: Twelve Data (TWELVE_DATA_API_KEY), an
official key-authenticated API, used only if Yahoo fails for a symbol.

`prefetch()` pulls a whole universe in a handful of batched requests and
caches it, so a scan of hundreds of symbols costs a few HTTP calls rather
than one (or several, with retries) per symbol. `get_klines()` serves from
that cache when it covers the request and falls back to per-symbol fetches
otherwise.

Every bar's `close_time` is the moment that bar actually closed: for daily
and longer bars that's 16:00 America/New_York on the bar's date, not
midnight — otherwise a still-trading session would pass as a finished bar
and the scanner would score half a day's candle.

A symbol that can't be fetched surfaces as `DataUnavailable` — never a
guess, never placeholder data.
"""
from __future__ import annotations

import logging
import math
import time
from dataclasses import dataclass, field

import httpx
import pandas as pd
import yfinance as yf

from app.config import settings

logger = logging.getLogger("tradingbot.data")

REQUIRED_COLUMNS = ["open_time", "open", "high", "low", "close", "volume", "close_time"]

_INTRADAY_MINUTES = {"1m": 1, "2m": 2, "5m": 5, "15m": 15, "30m": 30, "60m": 60, "90m": 90, "1h": 60}
_SHORT_INTRADAY = {"1m", "2m", "5m"}
_MARKET_TZ = "America/New_York"
_BATCH_SIZE = 100


class DataUnavailable(RuntimeError):
    """Raised when real market data cannot be retrieved.

    The rest of the system must treat this as NO SIGNAL, never fall back
    to placeholder or last-known-good data silently.
    """


def _period_for(interval: str, limit: int) -> str:
    """Yahoo takes a calendar period, not a bar count, so we ask for
    comfortably more than `limit` bars need and trim afterwards. Yahoo also
    caps intraday history (60 days for 1-5m, ~2 years for 60-90m)."""
    if interval in _INTRADAY_MINUTES:
        return "60d" if interval in _SHORT_INTRADAY else "730d"
    if interval == "1wk":
        return f"{min(max(2, math.ceil(limit / 45)), 25)}y"
    if interval == "1mo":
        return "25y"
    return f"{min(max(1, math.ceil(limit / 200)), 25)}y"


def _period_years(period: str) -> float:
    if period.endswith("y"):
        return float(period[:-1])
    if period.endswith("d"):
        return float(period[:-1]) / 365.0
    return 0.0


def _close_times(index: pd.Index, interval: str) -> pd.Series:
    """When each bar actually closed, in UTC."""
    idx = pd.DatetimeIndex(index)
    if interval in _INTRADAY_MINUTES:
        if idx.tz is None:
            idx = idx.tz_localize(_MARKET_TZ)
        return pd.Series(idx.tz_convert("UTC") + pd.Timedelta(minutes=_INTRADAY_MINUTES[interval]), index=range(len(idx)))
    # Daily or longer: the bar is labelled by its (first) trading date;
    # it's complete at that session's close. Weekly/monthly bars are
    # labelled by their first day, so their true close is later still —
    # the scanner only uses daily bars, and the freshness check tolerates
    # the difference for the rest.
    dates = idx.tz_localize(None) if idx.tz is not None else idx
    closes = dates.normalize() + pd.Timedelta(hours=16)
    return pd.Series(closes.tz_localize(_MARKET_TZ).tz_convert("UTC"), index=range(len(idx)))


def normalize_frame(raw: pd.DataFrame, interval: str, limit: int) -> pd.DataFrame:
    """Yahoo-shaped OHLCV (DatetimeIndex, Open/High/Low/Close/Volume) ->
    the app's canonical frame, oldest first, last `limit` bars."""
    if raw is None or raw.empty:
        raise RuntimeError("empty response")
    frame = raw.rename(columns=str.lower)[["open", "high", "low", "close", "volume"]].reset_index(drop=True)
    frame["close_time"] = _close_times(raw.index, interval)
    frame["open_time"] = frame["close_time"]
    frame = frame[REQUIRED_COLUMNS].dropna(subset=["open", "high", "low", "close", "volume"])
    frame = frame[(frame["high"] > 0) & (frame["low"] > 0)]
    if frame.empty:
        raise RuntimeError("no usable rows")
    frame = frame.sort_values("close_time").drop_duplicates("close_time", keep="last").tail(limit).reset_index(drop=True)
    return frame.set_index("close_time", drop=False)


def _fetch_twelvedata_daily(symbol: str, limit: int) -> pd.DataFrame:
    """Optional daily-bar fallback when TWELVE_DATA_API_KEY is set."""
    api_key = settings.twelvedata_api_key
    if not api_key:
        raise RuntimeError("no Twelve Data API key configured")
    resp = httpx.get(
        "https://api.twelvedata.com/time_series",
        params={"symbol": symbol.upper(), "interval": "1day", "outputsize": min(max(limit, 1), 5000), "apikey": api_key},
        timeout=15.0,
    )
    resp.raise_for_status()
    payload = resp.json()
    values = payload.get("values")
    if payload.get("status") == "error" or not values:
        raise RuntimeError(f"twelvedata: {payload.get('message', 'no values')}")
    df = pd.DataFrame(values)
    df.index = pd.to_datetime(df.pop("datetime"))
    for col in ("open", "high", "low", "close", "volume"):
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return normalize_frame(df, "1d", limit)


@dataclass
class StockClient:
    max_retries: int = settings.max_retries
    backoff: float = settings.retry_backoff_seconds
    min_interval: float = settings.min_request_interval_seconds
    _cache: dict[tuple[str, str], tuple[float, pd.DataFrame]] = field(default_factory=dict, init=False, repr=False)
    _last_request_at: float = field(default=0.0, init=False, repr=False)

    def __enter__(self) -> "StockClient":
        return self

    def __exit__(self, *exc) -> None:
        pass

    def close(self) -> None:
        pass

    def _throttle(self) -> None:
        wait = self.min_interval - (time.monotonic() - self._last_request_at)
        if wait > 0:
            time.sleep(wait)
        self._last_request_at = time.monotonic()

    def prefetch(self, symbols: list[str], interval: str = "1d", limit: int = 500) -> dict[str, str]:
        """Batch-download `symbols` into the cache. Returns {symbol: reason}
        for any symbol the batch didn't cover — those fall back to a
        per-symbol fetch when requested, so a partial batch is never fatal."""
        period = _period_for(interval, limit)
        wanted = sorted({s.upper() for s in symbols})
        missing: dict[str, str] = {}
        for start in range(0, len(wanted), _BATCH_SIZE):
            chunk = wanted[start:start + _BATCH_SIZE]
            raw = None
            for attempt in range(1, self.max_retries + 1):
                self._throttle()
                try:
                    raw = yf.download(
                        chunk, period=period, interval=interval, group_by="ticker",
                        auto_adjust=True, threads=True, progress=False,
                    )
                    break
                except Exception as exc:  # yfinance raises many types
                    logger.warning("Batch download attempt %d failed: %s", attempt, exc)
                    time.sleep(self.backoff * attempt)
            for symbol in chunk:
                try:
                    if raw is None or symbol not in raw.columns.get_level_values(0):
                        raise RuntimeError("not in batch response")
                    frame = normalize_frame(raw[symbol], interval, limit)
                    self._cache[(symbol, interval)] = (_period_years(period), frame)
                except Exception as exc:
                    missing[symbol] = str(exc)
        if missing:
            logger.info("Prefetch: %d/%d symbols not covered by batch: %s", len(missing), len(wanted), sorted(missing))
        return missing

    def get_klines(self, symbol: str, interval: str, limit: int = 500) -> pd.DataFrame:
        """Recent candles, oldest first, indexed by close_time (UTC)."""
        symbol = symbol.upper()
        period = _period_for(interval, limit)
        cached = self._cache.get((symbol, interval))
        if cached and cached[0] >= _period_years(period):
            return cached[1].tail(limit)

        errors: list[str] = []
        try:
            frame = self._fetch_yfinance(symbol, interval, limit, period)
            self._cache[(symbol, interval)] = (_period_years(period), frame)
            return frame
        except DataUnavailable as exc:
            errors.append(f"yfinance: {exc}")
        if interval == "1d" and settings.twelvedata_api_key:
            try:
                return _fetch_twelvedata_daily(symbol, limit)
            except Exception as exc:
                errors.append(f"twelvedata: {exc}")
        raise DataUnavailable(f"no data for {symbol} {interval} — " + "; ".join(errors))

    def _fetch_yfinance(self, symbol: str, interval: str, limit: int, period: str) -> pd.DataFrame:
        last_error: Exception | None = None
        for attempt in range(1, self.max_retries + 1):
            self._throttle()
            try:
                raw = yf.Ticker(symbol).history(period=period, interval=interval, auto_adjust=True)
                return normalize_frame(raw, interval, limit)
            except Exception as exc:
                last_error = exc
                if attempt < self.max_retries:
                    time.sleep(self.backoff * attempt)
        raise DataUnavailable(f"failed after {self.max_retries} attempts: {last_error}") from last_error
