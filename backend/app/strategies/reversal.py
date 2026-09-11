"""Reversal strategy — deliberately the strictest of the three, per the
spec ("only when there is strong confirmation").

Setup logic (all must hold):
  1. The PRIOR bar closed outside a Bollinger Band extreme (<= lower band
     for a long reversal, >= upper band for a short reversal) — price
     actually reached an extreme.
  2. The CURRENT bar closes back inside the band — the extreme is being
     rejected, not just touched.
  3. RSI on the prior bar was in oversold/overbought territory (<=30 / >=70)
     — confirms the extreme was real, not band noise.
  4. The current (confirmation) bar shows above-average volume — the
     reversal has participation, not just a quiet drift back.
  5. The confirmation candle's direction agrees with the reversal (a green
     candle for a long reversal, red for a short one).
"""
from __future__ import annotations

import pandas as pd

from app.strategies.base import LONG, SHORT, StrategyCandidate, clamp, last_closed_bar

OVERSOLD = 30.0
OVERBOUGHT = 70.0
MIN_REL_VOLUME = 1.3


def generate(df: pd.DataFrame, symbol: str) -> StrategyCandidate | None:
    if len(df) < 2:
        return None
    row = last_closed_bar(df)
    prev = df.iloc[-2]

    required_row = ["close", "open", "atr_14", "bb_lower", "bb_upper", "rel_volume_20"]
    required_prev = ["close", "bb_lower", "bb_upper", "rsi_14", "low", "high"]
    if any(pd.isna(row.get(f)) for f in required_row) or any(pd.isna(prev.get(f)) for f in required_prev):
        return None

    prev_touched_lower = float(prev["low"]) <= float(prev["bb_lower"])
    prev_touched_upper = float(prev["high"]) >= float(prev["bb_upper"])
    prev_rsi = float(prev["rsi_14"])
    rel_volume = float(row["rel_volume_20"])
    is_green = float(row["close"]) > float(row["open"])
    is_red = float(row["close"]) < float(row["open"])

    direction: str | None = None
    if (
        prev_touched_lower
        and prev_rsi <= OVERSOLD
        and float(row["close"]) > float(row["bb_lower"])
        and is_green
        and rel_volume >= MIN_REL_VOLUME
    ):
        direction = LONG
    elif (
        prev_touched_upper
        and prev_rsi >= OVERBOUGHT
        and float(row["close"]) < float(row["bb_upper"])
        and is_red
        and rel_volume >= MIN_REL_VOLUME
    ):
        direction = SHORT

    if direction is None:
        return None

    extreme_price = float(prev["low"]) if direction == LONG else float(prev["high"])
    band_level = float(prev["bb_lower"]) if direction == LONG else float(prev["bb_upper"])

    reasons = [
        f"Prior bar tagged the Bollinger Band {'lower' if direction == LONG else 'upper'} extreme "
        f"({extreme_price:.4g} vs band {band_level:.4g})",
        f"RSI(14) was {prev_rsi:.1f} on the extreme bar",
        f"Confirmation candle closed back inside the band on {rel_volume:.1f}x relative volume",
        f"{'Bullish' if direction == LONG else 'Bearish'} confirmation candle",
    ]

    # Momentum (0-25): how extreme the RSI reading was (deeper = stronger
    # reversal thesis) plus how decisively price reclaimed the band.
    rsi_extremity = (OVERSOLD - prev_rsi) if direction == LONG else (prev_rsi - OVERBOUGHT)
    rsi_component = clamp(rsi_extremity / 15.0 * 15.0, 0, 15)
    reclaim_pct = (
        (float(row["close"]) - band_level) / band_level * 100
        if direction == LONG
        else (band_level - float(row["close"])) / band_level * 100
    )
    reclaim_component = clamp(reclaim_pct * 10, 0, 10)
    momentum_score = rsi_component + reclaim_component

    # Volume (0-20): confirmation-bar relative volume only — this strategy
    # requires participation on the reversal itself, not a broader trend.
    volume_score = clamp((rel_volume - 1.0) / 2.0 * 20.0, 0, 20)

    # Structure (0-20): distance already reclaimed from the extreme back
    # toward the band midpoint (mean), scaled by ATR so it's comparable
    # across assets.
    atr = float(row["atr_14"])
    distance_reclaimed = abs(float(row["close"]) - extreme_price)
    structure_score = clamp(distance_reclaimed / max(atr, 1e-9) * 10.0, 0, 20)

    return StrategyCandidate(
        strategy="reversal",
        symbol=symbol,
        direction=direction,
        timestamp=row["close_time"],
        close=float(row["close"]),
        atr=atr,
        reasons=reasons,
        momentum_score=round(momentum_score, 2),
        volume_score=round(volume_score, 2),
        structure_score=round(structure_score, 2),
        swing_high=float(prev["high"]) if direction == SHORT else None,
        swing_low=float(prev["low"]) if direction == LONG else None,
        debug_features={
            "prev_rsi": prev_rsi,
            "rel_volume": rel_volume,
            "extreme_price": extreme_price,
        },
    )
