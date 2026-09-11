"""Unit tests against SYNTHETIC fixtures — verifying formulas only, never
presented as real market results (see tests/fixtures.py docstring)."""
from __future__ import annotations

import numpy as np
import pandas as pd

from app.features.indicators import atr, ema, rsi, sma, true_range
from tests.fixtures import make_synthetic_ohlcv


def test_sma_matches_manual_mean():
    series = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype=float)
    result = sma(series, 3)
    assert np.isnan(result.iloc[1])
    assert result.iloc[2] == 2.0  # mean(1,2,3)
    assert result.iloc[-1] == 9.0  # mean(8,9,10)


def test_ema_reacts_faster_than_sma_to_a_jump():
    series = pd.Series([10.0] * 20 + [20.0] * 10)
    ema_result = ema(series, 5)
    sma_result = sma(series, 5)
    # Right after the jump, EMA should have moved further toward the new
    # value than a plain SMA of the same length.
    idx = 22
    assert abs(ema_result.iloc[idx] - 20.0) < abs(sma_result.iloc[idx] - 20.0)


def test_rsi_is_100_when_only_gains():
    series = pd.Series(range(1, 30), dtype=float)  # strictly increasing
    result = rsi(series, 14)
    assert result.iloc[-1] == 100.0


def test_rsi_is_bounded_0_100():
    df = make_synthetic_ohlcv(n=200)
    result = rsi(df["close"], 14).dropna()
    assert (result >= 0).all() and (result <= 100).all()


def test_true_range_uses_prev_close():
    df = pd.DataFrame(
        {
            "high": [10, 12, 11],
            "low": [8, 9, 9.5],
            "close": [9, 11.5, 10],
        }
    )
    tr = true_range(df)
    # Bar 1: max(high-low, |high-prevclose|, |low-prevclose|)
    # = max(12-9=3, |12-9|=3, |9-9|=0) = 3
    assert tr.iloc[1] == 3


def test_atr_is_positive_and_smoothed():
    df = make_synthetic_ohlcv(n=100, volatility=1.0)
    result = atr(df, 14).dropna()
    assert (result > 0).all()
