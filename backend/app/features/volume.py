"""Volume-based features: relative volume, spikes, and trend.

These exist because volume confirmation is one of the independent factors
the spec requires (a breakout on thin volume is not the same signal as one
on 3x average volume).
"""
from __future__ import annotations

import pandas as pd


def relative_volume(df: pd.DataFrame, lookback: int = 20) -> pd.Series:
    """Current bar volume divided by the trailing average (excluding the
    current bar) — > 1.0 means above-average participation."""
    avg_volume = df["volume"].shift(1).rolling(window=lookback, min_periods=lookback).mean()
    return df["volume"] / avg_volume.replace(0, pd.NA)


def is_volume_spike(rel_volume: pd.Series, threshold: float = 2.0) -> pd.Series:
    return rel_volume >= threshold


def volume_trend(df: pd.DataFrame, short: int = 5, long: int = 20) -> pd.Series:
    """Ratio of short-term to long-term average volume — rising means
    participation is building, not just a single-bar spike."""
    short_avg = df["volume"].rolling(window=short, min_periods=short).mean()
    long_avg = df["volume"].rolling(window=long, min_periods=long).mean()
    return short_avg / long_avg.replace(0, pd.NA)


def compute_volume_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["rel_volume_20"] = relative_volume(out, 20)
    out["volume_spike"] = is_volume_spike(out["rel_volume_20"])
    out["volume_trend"] = volume_trend(out)
    return out
