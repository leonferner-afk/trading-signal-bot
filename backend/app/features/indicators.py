"""Technical indicators used by the scanner — the small, justified set from
the spec (EMA, SMA, VWAP, RSI, MACD, ATR, ADX, Bollinger Bands).

Every function takes/returns plain pandas Series so they compose cleanly
and are independently unit-testable against known reference values.
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def sma(series: pd.Series, length: int) -> pd.Series:
    return series.rolling(window=length, min_periods=length).mean()


def ema(series: pd.Series, length: int) -> pd.Series:
    return series.ewm(span=length, adjust=False, min_periods=length).mean()


def vwap(df: pd.DataFrame) -> pd.Series:
    """Session-cumulative VWAP using typical price, reset daily (UTC)."""
    typical_price = (df["high"] + df["low"] + df["close"]) / 3.0
    tp_vol = typical_price * df["volume"]
    day = df["close_time"].dt.floor("D")
    cum_tp_vol = tp_vol.groupby(day).cumsum()
    cum_vol = df["volume"].groupby(day).cumsum()
    return cum_tp_vol / cum_vol.replace(0, np.nan)


def rsi(series: pd.Series, length: int = 14) -> pd.Series:
    """Wilder's RSI."""
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1 / length, adjust=False, min_periods=length).mean()
    avg_loss = loss.ewm(alpha=1 / length, adjust=False, min_periods=length).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    result = 100 - (100 / (1 + rs))
    return result.where(avg_loss != 0, 100.0)


def macd(
    series: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9
) -> pd.DataFrame:
    fast_ema = ema(series, fast)
    slow_ema = ema(series, slow)
    macd_line = fast_ema - slow_ema
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line
    return pd.DataFrame(
        {"macd": macd_line, "signal": signal_line, "histogram": histogram}
    )


def true_range(df: pd.DataFrame) -> pd.Series:
    prev_close = df["close"].shift(1)
    ranges = pd.concat(
        [
            df["high"] - df["low"],
            (df["high"] - prev_close).abs(),
            (df["low"] - prev_close).abs(),
        ],
        axis=1,
    )
    return ranges.max(axis=1)


def atr(df: pd.DataFrame, length: int = 14) -> pd.Series:
    tr = true_range(df)
    return tr.ewm(alpha=1 / length, adjust=False, min_periods=length).mean()


def adx(df: pd.DataFrame, length: int = 14) -> pd.Series:
    """Wilder's ADX (trend strength, 0-100)."""
    up_move = df["high"].diff()
    down_move = -df["low"].diff()

    plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0.0)
    minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0.0)

    tr = true_range(df)
    tr_smooth = tr.ewm(alpha=1 / length, adjust=False, min_periods=length).mean()

    plus_dm_smooth = pd.Series(plus_dm, index=df.index).ewm(
        alpha=1 / length, adjust=False, min_periods=length
    ).mean()
    minus_dm_smooth = pd.Series(minus_dm, index=df.index).ewm(
        alpha=1 / length, adjust=False, min_periods=length
    ).mean()

    plus_di = 100 * (plus_dm_smooth / tr_smooth.replace(0, np.nan))
    minus_di = 100 * (minus_dm_smooth / tr_smooth.replace(0, np.nan))

    dx = 100 * (plus_di - minus_di).abs() / (plus_di + minus_di).replace(0, np.nan)
    return dx.ewm(alpha=1 / length, adjust=False, min_periods=length).mean()


def bollinger_bands(
    series: pd.Series, length: int = 20, num_std: float = 2.0
) -> pd.DataFrame:
    mid = sma(series, length)
    std = series.rolling(window=length, min_periods=length).std(ddof=0)
    upper = mid + num_std * std
    lower = mid - num_std * std
    width_pct = (upper - lower) / mid.replace(0, np.nan)
    return pd.DataFrame(
        {"mid": mid, "upper": upper, "lower": lower, "width_pct": width_pct}
    )


def compute_indicator_set(df: pd.DataFrame) -> pd.DataFrame:
    """Attach the full indicator set to a copy of the OHLCV dataframe."""
    out = df.copy()
    out["ema_9"] = ema(out["close"], 9)
    out["ema_21"] = ema(out["close"], 21)
    out["ema_50"] = ema(out["close"], 50)
    out["sma_50"] = sma(out["close"], 50)
    out["sma_200"] = sma(out["close"], 200)
    out["vwap"] = vwap(out)
    out["rsi_14"] = rsi(out["close"], 14)

    macd_df = macd(out["close"])
    out["macd"] = macd_df["macd"]
    out["macd_signal"] = macd_df["signal"]
    out["macd_hist"] = macd_df["histogram"]

    out["atr_14"] = atr(out, 14)
    out["atr_pct"] = out["atr_14"] / out["close"]
    out["adx_14"] = adx(out, 14)

    bb = bollinger_bands(out["close"], 20, 2.0)
    out["bb_mid"] = bb["mid"]
    out["bb_upper"] = bb["upper"]
    out["bb_lower"] = bb["lower"]
    out["bb_width_pct"] = bb["width_pct"]

    return out
