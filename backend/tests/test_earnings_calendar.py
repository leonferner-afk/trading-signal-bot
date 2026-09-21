"""Unit tests for earnings-date awareness — no network calls; the
yfinance `.calendar` property is monkeypatched with each of its known
response shapes."""
from __future__ import annotations

import datetime as dt

import pytest

from app.data.earnings_calendar import earnings_warning, next_earnings_date


class _FakeTicker:
    def __init__(self, calendar):
        self.calendar = calendar


def test_next_earnings_date_from_dict_shape(monkeypatch):
    future = dt.date.today() + dt.timedelta(days=10)
    monkeypatch.setattr(
        "app.data.earnings_calendar.yf.Ticker",
        lambda symbol: _FakeTicker({"Earnings Date": [future, future + dt.timedelta(days=1)]}),
    )
    assert next_earnings_date("AAPL") == future


def test_next_earnings_date_ignores_past_dates(monkeypatch):
    past = dt.date.today() - dt.timedelta(days=5)
    monkeypatch.setattr(
        "app.data.earnings_calendar.yf.Ticker",
        lambda symbol: _FakeTicker({"Earnings Date": [past]}),
    )
    assert next_earnings_date("AAPL") is None


def test_next_earnings_date_returns_none_on_missing_calendar(monkeypatch):
    monkeypatch.setattr("app.data.earnings_calendar.yf.Ticker", lambda symbol: _FakeTicker(None))
    assert next_earnings_date("AAPL") is None


def test_next_earnings_date_returns_none_on_exception(monkeypatch):
    def boom(symbol):
        raise RuntimeError("network down")

    monkeypatch.setattr("app.data.earnings_calendar.yf.Ticker", boom)
    assert next_earnings_date("AAPL") is None


def test_earnings_warning_fires_within_window(monkeypatch):
    soon = dt.date.today() + dt.timedelta(days=5)
    monkeypatch.setattr("app.data.earnings_calendar.next_earnings_date", lambda symbol: soon)
    warning = earnings_warning("AAPL", window_days=30)
    assert warning is not None
    assert soon.isoformat() in warning


def test_earnings_warning_silent_outside_window(monkeypatch):
    far = dt.date.today() + dt.timedelta(days=90)
    monkeypatch.setattr("app.data.earnings_calendar.next_earnings_date", lambda symbol: far)
    assert earnings_warning("AAPL", window_days=30) is None


def test_earnings_warning_silent_when_date_unknown(monkeypatch):
    # None must mean "unknown", not "confirmed clear" — either way the
    # function stays silent (additive-only contract).
    monkeypatch.setattr("app.data.earnings_calendar.next_earnings_date", lambda symbol: None)
    assert earnings_warning("AAPL") is None
