"""Unit tests for StockClient's provider priority and failure handling —
no network calls; `yf.Ticker` and `httpx.get` are monkeypatched with each
of their known response shapes.

For daily bars, the order is Twelve Data (if configured) -> Stooq ->
Yahoo (yfinance) — see the comment on `get_klines` in stock_client.py for
why. Intraday bars go to Yahoo only, since neither fallback has intraday
history.
"""
from __future__ import annotations

import datetime as dt
import types

import pandas as pd
import pytest

from app.data.stock_client import DataUnavailable, StockClient


def _make_client(**overrides) -> StockClient:
    defaults = dict(max_retries=2, backoff=0.0, min_interval=0.0)
    defaults.update(overrides)
    return StockClient(**defaults)


def _valid_yf_dataframe(rows: int = 5) -> pd.DataFrame:
    dates = pd.date_range(end=dt.datetime.now(dt.timezone.utc), periods=rows, freq="D")
    return pd.DataFrame(
        {"Open": 1.0, "High": 2.0, "Low": 0.5, "Close": 1.5, "Volume": 1000},
        index=pd.DatetimeIndex(dates, name="Date"),
    )


class _FakeTicker:
    def __init__(self, queue: list):
        self._queue = queue

    def history(self, period, interval, auto_adjust):
        item = self._queue.pop(0)
        if isinstance(item, Exception):
            raise item
        return item


def _patch_ticker(monkeypatch, queue: list):
    monkeypatch.setattr(
        "app.data.stock_client.yf.Ticker",
        lambda symbol, session=None: _FakeTicker(queue),
    )


def _patch_ticker_unreachable(monkeypatch):
    def _unexpected_call(symbol, session=None):
        raise AssertionError("yfinance should not be called when Stooq already succeeded")

    monkeypatch.setattr("app.data.stock_client.yf.Ticker", _unexpected_call)


class _FakeHttpResponse:
    def __init__(self, text: str = "", status_ok: bool = True, json_data=None):
        self.text = text
        self._status_ok = status_ok
        self._json_data = json_data

    def raise_for_status(self):
        if not self._status_ok:
            raise RuntimeError("http error")

    def json(self):
        return self._json_data


def _no_api_key(monkeypatch):
    monkeypatch.setattr("app.data.stock_client.settings", types.SimpleNamespace(twelvedata_api_key=""))


def _valid_stooq_csv() -> str:
    return "Date,Open,High,Low,Close,Volume\n2024-01-01,1.0,2.0,0.5,1.5,1000\n2024-01-02,1.1,2.1,0.6,1.6,1100\n"


def _patch_stooq_success(monkeypatch):
    monkeypatch.setattr(
        "app.data.stock_client.httpx.get",
        lambda url, params, headers, timeout, follow_redirects: _FakeHttpResponse(_valid_stooq_csv()),
    )


def _patch_stooq_failure(monkeypatch, text: str = "No data"):
    monkeypatch.setattr(
        "app.data.stock_client.httpx.get",
        lambda url, params, headers, timeout, follow_redirects: _FakeHttpResponse(text),
    )


def test_stooq_is_tried_first_for_daily_bars_and_yfinance_is_skipped(monkeypatch):
    _patch_ticker_unreachable(monkeypatch)
    _patch_stooq_success(monkeypatch)
    client = _make_client()
    df = client.get_klines("AAPL", "1d", limit=5)
    assert not df.empty
    assert list(df["close"]) == [1.5, 1.6]


def test_stooq_request_includes_required_date_range_params(monkeypatch):
    # Stooq's CSV endpoint 404s without d1/d2 — regression guard for that.
    captured = {}

    def _fake_get(url, params, headers, timeout, follow_redirects):
        captured.update(params)
        return _FakeHttpResponse(_valid_stooq_csv())

    monkeypatch.setattr("app.data.stock_client.httpx.get", _fake_get)
    client = _make_client()
    client.get_klines("AAPL", "1d", limit=5)
    assert captured["s"] == "aapl.us"
    assert captured["i"] == "d"
    assert len(captured["d1"]) == 8  # YYYYMMDD
    assert len(captured["d2"]) == 8


def test_falls_back_to_yfinance_when_stooq_fails_for_daily(monkeypatch):
    _patch_stooq_failure(monkeypatch)
    _patch_ticker(monkeypatch, [_valid_yf_dataframe()])
    client = _make_client()
    df = client.get_klines("AAPL", "1d", limit=5)
    assert not df.empty


def test_yfinance_retries_before_giving_up_on_intraday(monkeypatch):
    # First attempt fails (transient empty response), second succeeds —
    # must not give up after just one failed attempt. Intraday bypasses
    # Stooq entirely, so this exercises yfinance's own retry loop directly.
    queue = [RuntimeError("empty response for AAPL 5m"), _valid_yf_dataframe()]
    _patch_ticker(monkeypatch, queue)
    client = _make_client()
    df = client.get_klines("AAPL", "5m", limit=5)
    assert not df.empty
    assert queue == []


def test_no_stooq_call_for_intraday_intervals(monkeypatch):
    def _unexpected_stooq_call(*args, **kwargs):
        raise AssertionError("stooq should never be called for intraday intervals")

    monkeypatch.setattr("app.data.stock_client.httpx.get", _unexpected_stooq_call)
    _patch_ticker(monkeypatch, [RuntimeError("empty"), RuntimeError("empty")])
    client = _make_client()
    with pytest.raises(DataUnavailable):
        client.get_klines("AAPL", "5m", limit=5)


def test_raises_dataunavailable_when_both_providers_fail(monkeypatch):
    _patch_stooq_failure(monkeypatch)
    _patch_ticker(monkeypatch, [RuntimeError("empty"), RuntimeError("empty")])
    client = _make_client()
    with pytest.raises(DataUnavailable):
        client.get_klines("AAPL", "1d", limit=5)


def _valid_twelvedata_json() -> dict:
    return {
        "status": "ok",
        "values": [
            # Twelve Data returns newest-first — deliberately out of order
            # here to exercise the ascending-sort fix.
            {"datetime": "2024-01-02", "open": "1.1", "high": "2.1", "low": "0.6", "close": "1.6", "volume": "1100"},
            {"datetime": "2024-01-01", "open": "1.0", "high": "2.0", "low": "0.5", "close": "1.5", "volume": "1000"},
        ],
    }


def test_twelvedata_tried_first_when_configured_and_others_skipped(monkeypatch):
    monkeypatch.setattr("app.data.stock_client.settings", types.SimpleNamespace(twelvedata_api_key="fake-key"))
    _patch_ticker_unreachable(monkeypatch)

    def _fake_get(url, **kwargs):
        if "twelvedata" not in url:
            raise AssertionError("stooq should not be called when Twelve Data succeeds")
        return _FakeHttpResponse(json_data=_valid_twelvedata_json())

    monkeypatch.setattr("app.data.stock_client.httpx.get", _fake_get)
    client = _make_client()
    df = client.get_klines("AAPL", "1d", limit=5)
    # Ascending despite the provider's newest-first order.
    assert list(df["close"]) == [1.5, 1.6]


def test_twelvedata_not_called_without_api_key(monkeypatch):
    _no_api_key(monkeypatch)
    _patch_stooq_success(monkeypatch)
    client = _make_client()
    df = client.get_klines("AAPL", "1d", limit=5)
    assert not df.empty  # Stooq served it directly, twelvedata never in the mix


def test_falls_back_to_stooq_when_twelvedata_fails(monkeypatch):
    monkeypatch.setattr("app.data.stock_client.settings", types.SimpleNamespace(twelvedata_api_key="fake-key"))

    def _fake_get(url, **kwargs):
        if "twelvedata" in url:
            return _FakeHttpResponse(json_data={"status": "error", "message": "rate limit"})
        return _FakeHttpResponse(text=_valid_stooq_csv())

    monkeypatch.setattr("app.data.stock_client.httpx.get", _fake_get)
    client = _make_client()
    df = client.get_klines("AAPL", "1d", limit=5)
    assert not df.empty
