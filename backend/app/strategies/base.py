"""Shared strategy contract.

Each strategy inspects the last fully-closed bar of an already
feature-enriched OHLCV dataframe and either finds no setup (returns None)
or returns a `StrategyCandidate` carrying raw, bounded factor scores for
the three data-driven components of the final score (momentum, volume,
structure). The scoring engine (app.scoring.score) later adds the
regime-fit, catalyst and risk/reward components and produces the final
0-100 score — strategies never see or invent that final number themselves.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd

LONG = "LONG"
SHORT = "SHORT"


@dataclass
class StrategyCandidate:
    strategy: str
    symbol: str
    direction: str
    timestamp: pd.Timestamp
    close: float
    atr: float
    reasons: list[str]
    # Raw, bounded component scores (see app.scoring.score for the weights
    # applied to each). Each strategy computes these from the specific
    # features its own logic depends on — never a blanket "use everything".
    momentum_score: float  # 0-25
    volume_score: float  # 0-20
    structure_score: float  # 0-20
    # Reference levels used later for risk/reward + invalidation.
    range_high: float | None = None
    range_low: float | None = None
    swing_high: float | None = None
    swing_low: float | None = None
    debug_features: dict = field(default_factory=dict)


def last_closed_bar(df: pd.DataFrame) -> pd.Series | None:
    if df.empty:
        return None
    return df.iloc[-1]


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))
