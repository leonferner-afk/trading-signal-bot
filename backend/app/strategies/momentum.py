"""Momentum strategy: acceleration + relative strength + volume-backed
trend continuation.

Setup logic (all must hold on the last closed bar):
  1. EMA stack aligned with direction (9 > 21 > 50 for LONG, mirrored for
     SHORT) — an actual established trend, not a single green candle.
  2. RSI in the continuation zone (55-75 long / 25-45 short) — strong but
     not so extreme it is due for mean reversion.
  3. MACD histogram positive and expanding in the trend direction
     (acceleration, not just direction).
  4. ADX >= 20 (there is a trend to continue at all).
  5. Volume trend (short/long average ratio) >= 1.0 — participation is
     building, not fading.
"""
from __future__ import annotations

import pandas as pd

from app.strategies.base import LONG, SHORT, StrategyCandidate, clamp, last_closed_bar

MIN_ADX = 20.0


def generate(df: pd.DataFrame, symbol: str) -> StrategyCandidate | None:
    if len(df) < 2:
        return None
    row = last_closed_bar(df)
    prev = df.iloc[-2]

    required = [
        "close",
        "atr_14",
        "ema_9",
        "ema_21",
        "ema_50",
        "rsi_14",
        "macd_hist",
        "adx_14",
        "volume_trend",
        "rel_volume_20",
        "vwap",
    ]
    if any(pd.isna(row.get(f)) for f in required) or pd.isna(prev.get("macd_hist")):
        return None

    ema9, ema21, ema50 = float(row["ema_9"]), float(row["ema_21"]), float(row["ema_50"])
    rsi = float(row["rsi_14"])
    macd_hist = float(row["macd_hist"])
    prev_macd_hist = float(prev["macd_hist"])
    adx = float(row["adx_14"])
    volume_trend = float(row["volume_trend"])
    rel_volume = float(row["rel_volume_20"])

    bullish_stack = ema9 > ema21 > ema50
    bearish_stack = ema9 < ema21 < ema50
    accelerating_up = macd_hist > 0 and macd_hist > prev_macd_hist
    accelerating_down = macd_hist < 0 and macd_hist < prev_macd_hist

    direction: str | None = None
    if bullish_stack and 55 <= rsi <= 75 and accelerating_up:
        direction = LONG
    elif bearish_stack and 25 <= rsi <= 45 and accelerating_down:
        direction = SHORT

    if direction is None:
        return None
    if adx < MIN_ADX:
        return None
    if volume_trend < 1.0:
        return None

    reasons = [
        f"EMA9/21/50 stack aligned {direction.lower()} ({ema9:.4g}/{ema21:.4g}/{ema50:.4g})",
        f"RSI(14) at {rsi:.1f} — strong but not exhausted",
        "MACD histogram accelerating in trend direction",
        f"ADX(14) at {adx:.1f} confirms an active trend",
        f"Volume trend ratio {volume_trend:.2f} — participation building",
    ]

    # Momentum (0-25): RSI positioning within its continuation band +
    # MACD acceleration magnitude + ADX strength.
    rsi_mid = 65 if direction == LONG else 35
    rsi_component = clamp(10 - abs(rsi - rsi_mid) / 2.0, 0, 10)
    accel_component = clamp(abs(macd_hist - prev_macd_hist) / max(abs(prev_macd_hist), 1e-9) * 5, 0, 8)
    adx_component = clamp((adx - MIN_ADX) / 30.0 * 7.0, 0, 7)
    momentum_score = rsi_component + accel_component + adx_component

    # Volume (0-20): trend ratio + relative volume on the confirming bar.
    volume_score = clamp((volume_trend - 1.0) * 12.0, 0, 12) + clamp((rel_volume - 1.0) * 8.0, 0, 8)

    # Structure (0-20): distance from VWAP in the trend direction (trading
    # with value, not against it) plus how cleanly the EMAs are separated.
    vwap = float(row["vwap"])
    vwap_component = clamp(((row["close"] - vwap) / vwap * 100) * 3, 0, 10) if direction == LONG else clamp(
        ((vwap - row["close"]) / vwap * 100) * 3, 0, 10
    )
    separation = abs(ema9 - ema50) / ema50 * 100
    separation_component = clamp(separation * 4, 0, 10)
    structure_score = vwap_component + separation_component

    return StrategyCandidate(
        strategy="momentum",
        symbol=symbol,
        direction=direction,
        timestamp=row["close_time"],
        close=float(row["close"]),
        atr=float(row["atr_14"]),
        reasons=reasons,
        momentum_score=round(momentum_score, 2),
        volume_score=round(volume_score, 2),
        structure_score=round(structure_score, 2),
        swing_high=None,
        swing_low=None,
        debug_features={
            "rsi": rsi,
            "adx": adx,
            "macd_hist": macd_hist,
            "volume_trend": volume_trend,
        },
    )
