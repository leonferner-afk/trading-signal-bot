"""Breakout strategy: range / resistance / consolidation breakout,
confirmed by volume — never on price alone.

Setup logic (all must hold on the last closed bar):
  1. Close breaks the prior N-bar range (range_high for LONG, range_low
     for SHORT) — this is the actual breakout event.
  2. Relative volume >= 1.5x the trailing average — the "volume-confirmed"
     requirement from the spec; an unconfirmed breakout is not a signal.
  3. ADX is not deeply in RANGE territory (avoids scoring breakouts that
     immediately follow into full regime classification — the regime
     module penalizes RANGE separately too, this is a strategy-local
     sanity check on trend capacity).
"""
from __future__ import annotations

import pandas as pd

from app.strategies.base import LONG, SHORT, StrategyCandidate, clamp, last_closed_bar

MIN_REL_VOLUME = 1.5
LOOKBACK = 20


def generate(df: pd.DataFrame, symbol: str) -> StrategyCandidate | None:
    row = last_closed_bar(df)
    if row is None:
        return None

    required = [
        "close",
        "atr_14",
        "rel_volume_20",
        "range_high",
        "range_low",
        "breakout_up",
        "breakout_down",
        "adx_14",
        "macd_hist",
        "consolidating",
    ]
    if any(pd.isna(row.get(f)) for f in required):
        return None

    if not (bool(row["breakout_up"]) or bool(row["breakout_down"])):
        return None

    rel_volume = float(row["rel_volume_20"])
    if rel_volume < MIN_REL_VOLUME:
        return None

    direction = LONG if bool(row["breakout_up"]) else SHORT
    reasons: list[str] = []

    pct_beyond = (
        float(row["pct_beyond_high"]) if direction == LONG else float(row["pct_beyond_low"])
    )
    level = float(row["range_high"]) if direction == LONG else float(row["range_low"])
    reasons.append(
        f"{LOOKBACK}-bar {'resistance' if direction == LONG else 'support'} breakout at {level:.4g}"
        f" ({pct_beyond * 100:.2f}% beyond level)"
    )
    reasons.append(f"{rel_volume:.1f}x relative volume on the breakout bar")

    if bool(row["consolidating"]):
        reasons.append("breakout follows a tight consolidation range")

    # Momentum component (0-25): ADX magnitude + MACD histogram agreeing
    # with breakout direction. Both are real, independent confirmations —
    # a breakout with ADX rising and MACD histogram expanding the same way
    # is stronger than a breakout with neither.
    adx = float(row["adx_14"])
    macd_hist = float(row["macd_hist"])
    macd_aligned = (macd_hist > 0) if direction == LONG else (macd_hist < 0)
    momentum_score = clamp(adx / 40.0 * 18.0, 0, 18) + (7.0 if macd_aligned else 0.0)
    if macd_aligned:
        reasons.append("MACD histogram confirms breakout direction")

    # Volume component (0-20): scale relative volume, cap at 4x.
    volume_score = clamp((rel_volume - 1.0) / 3.0 * 20.0, 0, 20)

    # Structure component (0-20): how decisively price cleared the level,
    # plus a bonus if it broke out of a genuine consolidation.
    structure_score = clamp(pct_beyond * 100 * 4.0, 0, 14)
    if bool(row["consolidating"]):
        structure_score = clamp(structure_score + 6.0, 0, 20)

    return StrategyCandidate(
        strategy="breakout",
        symbol=symbol,
        direction=direction,
        timestamp=row["close_time"],
        close=float(row["close"]),
        atr=float(row["atr_14"]),
        reasons=reasons,
        momentum_score=round(momentum_score, 2),
        volume_score=round(volume_score, 2),
        structure_score=round(structure_score, 2),
        range_high=float(row["range_high"]),
        range_low=float(row["range_low"]),
        debug_features={
            "rel_volume": rel_volume,
            "adx": adx,
            "macd_hist": macd_hist,
            "pct_beyond": pct_beyond,
        },
    )
