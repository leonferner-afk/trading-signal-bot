"""Real market-data client for Binance's public spot REST API.

No API key is required for the endpoints used here (klines, 24h ticker,
order book depth) — this is genuinely live/historical market data, not a
mock. Every call goes through retries, a timeout, and a minimum interval
between requests to stay well under Binance's public rate limits.

If a request fails after retries, callers get an explicit `DataUnavailable`
exception — never a fabricated candle. The scanner and backtester both
depend on that: missing data must surface as "no data", not as a guess.
"""
from __future__ import annotations

import time
from dataclasses import dataclass

import httpx
import pandas as pd

from app.config import settings

KLINE_COLUMNS = [
    "open_time",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "close_time",
    "quote_asset_volume",
    "num_trades",
    "taker_buy_base_volume",
    "taker_buy_quote_volume",
    "ignore",
]

NUMERIC_COLUMNS = [
    "open",
    "high",
    "low",
    "close",
    "volume",
    "quote_asset_volume",
    "taker_buy_base_volume",
    "taker_buy_quote_volume",
]


class DataUnavailable(RuntimeError):
    """Raised when real market data cannot be retrieved.

    The rest of the system must treat this as NO SIGNAL, never fall back
    to placeholder or last-known-good data silently.
    """


@dataclass
class BinanceClient:
    base_url: str = settings.binance_base_url
    timeout: float = settings.request_timeout_seconds
    max_retries: int = settings.max_retries
    backoff: float = settings.retry_backoff_seconds
    min_interval: float = settings.min_request_interval_seconds

    def __post_init__(self) -> None:
        self._client = httpx.Client(base_url=self.base_url, timeout=self.timeout)
        self._last_request_at = 0.0

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "BinanceClient":
        return self

    def __exit__(self, *exc) -> None:
        self.close()

    def _throttle(self) -> None:
        elapsed = time.monotonic() - self._last_request_at
        wait = self.min_interval - elapsed
        if wait > 0:
            time.sleep(wait)

    def _get(self, path: str, params: dict) -> object:
        last_error: Exception | None = None
        for attempt in range(1, self.max_retries + 1):
            self._throttle()
            try:
                self._last_request_at = time.monotonic()
                response = self._client.get(path, params=params)
                if response.status_code == 429 or response.status_code >= 500:
                    raise httpx.HTTPStatusError(
                        f"retryable status {response.status_code}",
                        request=response.request,
                        response=response,
                    )
                response.raise_for_status()
                return response.json()
            except (httpx.HTTPError, httpx.TransportError) as exc:
                last_error = exc
                if attempt < self.max_retries:
                    time.sleep(self.backoff * attempt)
        raise DataUnavailable(
            f"GET {path} failed after {self.max_retries} attempts: {last_error}"
        ) from last_error

    def get_klines(self, symbol: str, interval: str, limit: int = 500) -> pd.DataFrame:
        """Fetch recent candles. Returns a DataFrame indexed by close_time (UTC)."""
        raw = self._get(
            "/api/v3/klines",
            {"symbol": symbol.upper(), "interval": interval, "limit": limit},
        )
        if not isinstance(raw, list) or not raw:
            raise DataUnavailable(f"empty kline response for {symbol} {interval}")
        df = pd.DataFrame(raw, columns=KLINE_COLUMNS)
        for col in NUMERIC_COLUMNS:
            df[col] = df[col].astype(float)
        df["open_time"] = pd.to_datetime(df["open_time"], unit="ms", utc=True)
        df["close_time"] = pd.to_datetime(df["close_time"], unit="ms", utc=True)
        df["num_trades"] = df["num_trades"].astype(int)
        return df.set_index("close_time", drop=False)

    def get_24h_ticker(self, symbol: str) -> dict:
        raw = self._get("/api/v3/ticker/24hr", {"symbol": symbol.upper()})
        if not isinstance(raw, dict):
            raise DataUnavailable(f"unexpected 24h ticker response for {symbol}")
        return raw

    def get_order_book(self, symbol: str, limit: int = 20) -> dict:
        raw = self._get("/api/v3/depth", {"symbol": symbol.upper(), "limit": limit})
        if not isinstance(raw, dict):
            raise DataUnavailable(f"unexpected order book response for {symbol}")
        return raw

    def server_time_ms(self) -> int:
        raw = self._get("/api/v3/time", {})
        return int(raw["serverTime"])
