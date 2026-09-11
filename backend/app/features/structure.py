"""Price-action / market-structure features: swing points, support &
resistance, breakout detection, and trend structure (higher highs / higher
lows vs. lower highs / lower lows).

All of this is computed strictly on data available up to (and including)
each bar — no forward-looking lookback — so it stays valid inside the
backtester without introducing look-ahead bias.
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def swing_points(df: pd.DataFrame, window: int = 3) -> pd.DataFrame:
    """A bar is a swing high/low if it is the max/min within +/- window bars.

    Uses a centered rolling window, so a swing point is only confirmed
    `window` bars after it occurs — this is intentional (it mirrors how a
    trader would actually recognize a swing) and callers must not treat
    the most recent `window` bars' swing flags as final.
    """
    highs = df["high"]
    lows = df["low"]
    is_swing_high = highs == highs.rolling(window=2 * window + 1, center=True).max()
    is_swing_low = lows == lows.rolling(window=2 * window + 1, center=True).min()
    return pd.DataFrame({"swing_high": is_swing_high.fillna(False), "swing_low": is_swing_low.fillna(False)})


def rolling_range(df: pd.DataFrame, lookback: int = 20) -> pd.DataFrame:
    """Simple, always-causal support/resistance proxy: the highest high and
    lowest low over the trailing `lookback` bars, EXCLUDING the current bar
    so a breakout can be measured against the prior range."""
    prior_high = df["high"].shift(1).rolling(window=lookback, min_periods=lookback).max()
    prior_low = df["low"].shift(1).rolling(window=lookback, min_periods=lookback).min()
    return pd.DataFrame({"range_high": prior_high, "range_low": prior_low})


def breakout_signal(df: pd.DataFrame, lookback: int = 20) -> pd.DataFrame:
    """Flags a bar whose close breaks above/below the prior N-bar range,
    plus how far (in %) beyond the level the close pushed."""
    rng = rolling_range(df, lookback)
    breakout_up = df["close"] > rng["range_high"]
    breakout_down = df["close"] < rng["range_low"]
    pct_beyond_high = (df["close"] - rng["range_high"]) / rng["range_high"].replace(0, np.nan)
    pct_beyond_low = (rng["range_low"] - df["close"]) / rng["range_low"].replace(0, np.nan)
    return pd.DataFrame(
        {
            "range_high": rng["range_high"],
            "range_low": rng["range_low"],
            "breakout_up": breakout_up,
            "breakout_down": breakout_down,
            "pct_beyond_high": pct_beyond_high,
            "pct_beyond_low": pct_beyond_low,
        }
    )


def consolidation_flag(df: pd.DataFrame, lookback: int = 20, max_width_pct: float = 0.05) -> pd.Series:
    """True when the prior `lookback`-bar range is unusually tight relative
    to price — a precondition for a "consolidation breakout" setup."""
    rng = rolling_range(df, lookback)
    width_pct = (rng["range_high"] - rng["range_low"]) / df["close"].replace(0, np.nan)
    return width_pct <= max_width_pct


def trend_structure(df: pd.DataFrame, window: int = 3, lookback_points: int = 4) -> pd.Series:
    """Classifies recent swing-point structure as UPTREND (higher highs and
    higher lows), DOWNTREND (lower highs and lower lows), or MIXED.

    Only uses swing points that are fully confirmed (i.e. at least `window`
    bars old) at each point in time, so this stays causal.
    """
    swings = swing_points(df, window)
    highs = df["high"].where(swings["swing_high"]).shift(window)
    lows = df["low"].where(swings["swing_low"]).shift(window)

    recent_highs = highs.dropna()
    recent_lows = lows.dropna()

    out = pd.Series("MIXED", index=df.index, dtype="object")
    for ts in df.index:
        h = recent_highs.loc[:ts].tail(lookback_points)
        l = recent_lows.loc[:ts].tail(lookback_points)
        if len(h) >= 2 and len(l) >= 2 and h.is_monotonic_increasing and l.is_monotonic_increasing:
            out.loc[ts] = "UPTREND"
        elif len(h) >= 2 and len(l) >= 2 and h.is_monotonic_decreasing and l.is_monotonic_decreasing:
            out.loc[ts] = "DOWNTREND"
    return out


def compute_structure_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    swings = swing_points(out)
    out["swing_high"] = swings["swing_high"]
    out["swing_low"] = swings["swing_low"]

    brk = breakout_signal(out)
    out["range_high"] = brk["range_high"]
    out["range_low"] = brk["range_low"]
    out["breakout_up"] = brk["breakout_up"]
    out["breakout_down"] = brk["breakout_down"]
    out["pct_beyond_high"] = brk["pct_beyond_high"]
    out["pct_beyond_low"] = brk["pct_beyond_low"]

    out["consolidating"] = consolidation_flag(out)
    out["trend_structure"] = trend_structure(out)
    return out
