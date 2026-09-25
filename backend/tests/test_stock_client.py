"""StockClient provider order, batch cache and failure handling — no
network; `yf.download`, `yf.Ticker` and `httpx.get` are monkeypatched."""
from __future__ import annotations

import types

import pandas as pd
import pytest

from app.data.stock_client import DataUnavailable, StockClient, normalize_frame


def _client() -> StockClient:
    return StockClient(max_retries=2, backoff=0.0, min_interval=0.0)


def _yahoo_frame(rows: int = 5, start: str = "2026-09-14", scale: float = 1.0) -> pd.DataFrame:
    idx = pd.date_range(start, periods=rows, freq="B", tz="America/New_York")
    return pd.DataFrame(
        {"Open": 1.0 * scale, "High": 2.0 * scale, "Low": 0.5 * scale, "Close": 1.5 * scale, "Volume": 1000},
        index=idx,
    )


class _Ticker:
    def __init__(self, queue: list):
        self._queue = queue

    def history(self, period, interval, auto_adjust):
        item = self._queue.pop(0)
        if isinstance(item, Exception):
            raise item
        return item


def _patch_ticker(monkeypatch, queue: list) -> None:
    monkeypatch.setattr("app.data.stock_client.yf.Ticker", lambda symbol: _Ticker(queue))


def _forbid_ticker(monkeypatch) -> None:
    def _boom(symbol):
        raise AssertionError("per-symbol fetch should not happen when the batch cache covers it")

    monkeypatch.setattr("app.data.stock_client.yf.Ticker", _boom)


def test_daily_close_time_is_the_new_york_session_close():
    frame = normalize_frame(_yahoo_frame(1, start="2026-09-24"), "1d", 5)
    assert frame["close_time"].iloc[-1] == pd.Timestamp("2026-09-24 20:00", tz="UTC")


def test_prefetch_serves_get_klines_from_cache(monkeypatch):
    batch = pd.concat({"AAPL": _yahoo_frame(), "MSFT": _yahoo_frame(scale=2)}, axis=1)
    monkeypatch.setattr("app.data.stock_client.yf.download", lambda *a, **k: batch)
    _forbid_ticker(monkeypatch)
    client = _client()
    assert client.prefetch(["AAPL", "MSFT"], "1d", limit=300) == {}
    assert client.get_klines("MSFT", "1d", limit=300)["close"].iloc[-1] == 3.0


def test_symbol_missing_from_batch_falls_back_to_single_fetch(monkeypatch):
    empty = _yahoo_frame() * float("nan")
    batch = pd.concat({"AAPL": _yahoo_frame(), "DEAD": empty}, axis=1)
    monkeypatch.setattr("app.data.stock_client.yf.download", lambda *a, **k: batch)
    client = _client()
    missing = client.prefetch(["AAPL", "DEAD"], "1d", limit=300)
    assert list(missing) == ["DEAD"]
    _patch_ticker(monkeypatch, [_yahoo_frame(scale=3)])
    assert client.get_klines("DEAD", "1d", limit=300)["close"].iloc[-1] == 4.5


def test_yfinance_retries_before_giving_up(monkeypatch):
    queue = [RuntimeError("transient"), _yahoo_frame()]
    _patch_ticker(monkeypatch, queue)
    assert not _client().get_klines("AAPL", "1d", limit=5).empty
    assert queue == []


def test_unavailable_without_fallback_key(monkeypatch):
    monkeypatch.setattr("app.data.stock_client.settings", types.SimpleNamespace(twelvedata_api_key=""))
    _patch_ticker(monkeypatch, [RuntimeError("blocked"), RuntimeError("blocked")])
    with pytest.raises(DataUnavailable):
        _client().get_klines("AAPL", "1d", limit=5)


class _Resp:
    def __init__(self, payload):
        self._payload = payload

    def raise_for_status(self):
        pass

    def json(self):
        return self._payload


def test_twelvedata_fallback_sorted_oldest_first(monkeypatch):
    monkeypatch.setattr("app.data.stock_client.settings", types.SimpleNamespace(twelvedata_api_key="k"))
    _patch_ticker(monkeypatch, [RuntimeError("blocked"), RuntimeError("blocked")])
    payload = {
        "status": "ok",
        "values": [  # newest first, as the API returns them
            {"datetime": "2026-09-24", "open": "2", "high": "3", "low": "1", "close": "2.5", "volume": "10"},
            {"datetime": "2026-09-23", "open": "1", "high": "2", "low": "0.5", "close": "1.5", "volume": "10"},
        ],
    }
    monkeypatch.setattr("app.data.stock_client.httpx.get", lambda *a, **k: _Resp(payload))
    df = _client().get_klines("AAPL", "1d", limit=5)
    assert list(df["close"]) == [1.5, 2.5]


def test_intraday_never_uses_daily_fallback(monkeypatch):
    monkeypatch.setattr("app.data.stock_client.settings", types.SimpleNamespace(twelvedata_api_key="k"))
    _patch_ticker(monkeypatch, [RuntimeError("blocked"), RuntimeError("blocked")])

    def _boom(*a, **k):
        raise AssertionError("daily fallback must not serve intraday requests")

    monkeypatch.setattr("app.data.stock_client.httpx.get", _boom)
    with pytest.raises(DataUnavailable):
        _client().get_klines("AAPL", "5m", limit=5)
