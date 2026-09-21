"""Market regime classification (section 5).

Two independent axes are classified per bar:
  - trend regime:      TRENDING_UP / TRENDING_DOWN / RANGE / TRANSITIONAL
  - volatility regime:  HIGH_VOLATILITY / NORMAL_VOLATILITY / LOW_VOLATILITY

A third, market-wide axis (RISK_ON / RISK_OFF / NEUTRAL) is derived from
the anchor asset's (SPY, the S&P 500 ETF) own trend regime, since the
broad index's trend is the standard proxy for market-wide risk appetite —
this is a real, if simple, heuristic, not a fabricated signal.

Every strategy then gets a `regime_fit` score (0-10) telling the scoring
engine how well its own logic matches the *current* regime, so e.g. a
breakout strategy is not scored identically in a trending market and in a
choppy, directionless one.
"""
from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

TREND_UP = "TRENDING_UP"
TREND_DOWN = "TRENDING_DOWN"
RANGE = "RANGE"
TRANSITIONAL = "TRANSITIONAL"

VOL_HIGH = "HIGH_VOLATILITY"
VOL_NORMAL = "NORMAL_VOLATILITY"
VOL_LOW = "LOW_VOLATILITY"

RISK_ON = "RISK_ON"
RISK_OFF = "RISK_OFF"
RISK_NEUTRAL = "NEUTRAL"

ADX_TREND_THRESHOLD = 25.0
ADX_RANGE_THRESHOLD = 18.0


@dataclass(frozen=True)
class RegimeSnapshot:
    trend_regime: str
    volatility_regime: str
    adx: float
    atr_pct: float
    atr_pct_percentile: float
    ema_slope_pct: float

    @property
    def label(self) -> str:
        return f"{self.trend_regime} / {self.volatility_regime}"


def classify_trend_regime(df: pd.DataFrame) -> pd.Series:
    adx = df["adx_14"]
    ema_slope = df["ema_50"].pct_change(periods=5)

    trending = adx >= ADX_TREND_THRESHOLD
    ranging = adx <= ADX_RANGE_THRESHOLD

    out = pd.Series(TRANSITIONAL, index=df.index, dtype="object")
    out = out.mask(ranging, RANGE)
    out = out.mask(trending & (ema_slope > 0), TREND_UP)
    out = out.mask(trending & (ema_slope <= 0), TREND_DOWN)
    return out


def classify_volatility_regime(df: pd.DataFrame, lookback: int = 100) -> pd.Series:
    atr_pct = df["atr_pct"]
    percentile = atr_pct.rolling(window=lookback, min_periods=20).apply(
        lambda window: (window.rank(pct=True).iloc[-1]) if len(window.dropna()) > 0 else float("nan"),
        raw=False,
    )
    out = pd.Series(VOL_NORMAL, index=df.index, dtype="object")
    out = out.mask(percentile >= 0.8, VOL_HIGH)
    out = out.mask(percentile <= 0.2, VOL_LOW)
    return out


def compute_regime_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["trend_regime"] = classify_trend_regime(out)
    out["volatility_regime"] = classify_volatility_regime(out)
    out["ema_slope_pct"] = out["ema_50"].pct_change(periods=5)
    return out


def latest_snapshot(df: pd.DataFrame) -> RegimeSnapshot | None:
    if df.empty:
        return None
    row = df.iloc[-1]
    if pd.isna(row.get("adx_14")) or pd.isna(row.get("atr_pct")):
        return None
    atr_pct_series = df["atr_pct"].tail(100).dropna()
    percentile = (
        float((atr_pct_series <= row["atr_pct"]).mean()) if len(atr_pct_series) else float("nan")
    )
    return RegimeSnapshot(
        trend_regime=row.get("trend_regime", TRANSITIONAL),
        volatility_regime=row.get("volatility_regime", VOL_NORMAL),
        adx=float(row["adx_14"]),
        atr_pct=float(row["atr_pct"]),
        atr_pct_percentile=percentile,
        ema_slope_pct=float(row.get("ema_slope_pct", 0.0) or 0.0),
    )


def market_wide_risk_regime(anchor_snapshot: RegimeSnapshot | None) -> str:
    """Derive RISK_ON / RISK_OFF / NEUTRAL from the anchor asset's (SPY)
    trend regime. Returns NEUTRAL if the anchor snapshot is unavailable —
    never guesses."""
    if anchor_snapshot is None:
        return RISK_NEUTRAL
    if anchor_snapshot.trend_regime == TREND_UP:
        return RISK_ON
    if anchor_snapshot.trend_regime == TREND_DOWN:
        return RISK_OFF
    return RISK_NEUTRAL


# Regime fit table: how well each strategy family's edge matches a given
# trend regime, on a 0-10 scale. This is a deliberate, documented mapping
# (not a learned parameter) reflecting each setup's own logic:
#   - breakout needs a regime that can actually trend afterwards; it is
#     penalized hardest in a chopping RANGE (false breakouts).
#   - momentum needs an existing trend to continue.
#   - reversal needs a RANGE/exhaustion context, and is penalized in a
#     strongly trending market (fading a strong trend is low-probability).
_STRATEGY_TREND_FIT = {
    "breakout": {TREND_UP: 9, TREND_DOWN: 9, TRANSITIONAL: 6, RANGE: 3},
    "momentum": {TREND_UP: 10, TREND_DOWN: 10, TRANSITIONAL: 5, RANGE: 2},
    "reversal": {TREND_UP: 3, TREND_DOWN: 3, TRANSITIONAL: 6, RANGE: 9},
}

# Extreme volatility hurts every strategy's execution quality (wider slippage,
# unreliable stops); very low volatility hurts breakout/momentum (no follow
# through) but is neutral for a mean-reversion reversal thesis.
_STRATEGY_VOL_ADJUSTMENT = {
    "breakout": {VOL_HIGH: -1, VOL_NORMAL: 0, VOL_LOW: -2},
    "momentum": {VOL_HIGH: -1, VOL_NORMAL: 0, VOL_LOW: -2},
    "reversal": {VOL_HIGH: -2, VOL_NORMAL: 0, VOL_LOW: 0},
}


def regime_fit_score(strategy_name: str, snapshot: RegimeSnapshot) -> float:
    """0-10 score for how well `strategy_name` fits the current regime."""
    base = _STRATEGY_TREND_FIT.get(strategy_name, {}).get(snapshot.trend_regime, 5)
    adjustment = _STRATEGY_VOL_ADJUSTMENT.get(strategy_name, {}).get(snapshot.volatility_regime, 0)
    return max(0.0, min(10.0, base + adjustment))
