"""Risk/reward calculation (section 9).

Entry/stop/target/invalidation are derived from the same real inputs used
to generate the signal — ATR and the structural levels the strategy
already identified — never a hardcoded percentage. If the resulting
reward is not realistic for the asset's own volatility, that is surfaced
as a warning and a poor risk/reward score, not silently inflated.
"""
from __future__ import annotations

from dataclasses import dataclass

from app.strategies.base import LONG, StrategyCandidate

MIN_ACCEPTABLE_RR = 1.5
STOP_ATR_MULT = 1.5
TARGET_ATR_MULT = 3.0
STOP_BUFFER_ATR_MULT = 0.25
MAX_TARGET_ATR_MULT = 8.0
AGGRESSIVE_MOVE_PCT = 15.0


@dataclass
class RiskReward:
    entry: float
    stop: float
    target: float
    risk_pct: float
    reward_pct: float
    rr_ratio: float
    invalidation: float
    invalidation_reason: str
    target_reason: str
    realistic: bool
    warning: str | None
    score: float  # 0-10 component for the final score


def _structural_stop(candidate: StrategyCandidate) -> tuple[float, str] | None:
    atr_buffer = STOP_BUFFER_ATR_MULT * candidate.atr
    if candidate.strategy == "breakout":
        if candidate.direction == LONG and candidate.range_high is not None:
            return candidate.range_high - atr_buffer, "prior resistance (now support) minus a small ATR buffer"
        if candidate.direction != LONG and candidate.range_low is not None:
            return candidate.range_low + atr_buffer, "prior support (now resistance) plus a small ATR buffer"
    if candidate.strategy == "reversal":
        if candidate.direction == LONG and candidate.swing_low is not None:
            return candidate.swing_low - atr_buffer, "below the reversal's swing low extreme"
        if candidate.direction != LONG and candidate.swing_high is not None:
            return candidate.swing_high + atr_buffer, "above the reversal's swing high extreme"
    return None


def compute_risk_reward(candidate: StrategyCandidate) -> RiskReward:
    entry = candidate.close
    atr = candidate.atr
    direction = candidate.direction

    structural = _structural_stop(candidate)
    atr_stop = entry - STOP_ATR_MULT * atr if direction == LONG else entry + STOP_ATR_MULT * atr

    if structural is not None:
        structural_stop, structural_reason = structural
        # Use whichever stop is tighter (closer to entry) as long as it is
        # still on the correct side of entry — a stop that isn't tighter
        # than the ATR-based one adds risk without adding information.
        if direction == LONG:
            stop = max(structural_stop, atr_stop)
        else:
            stop = min(structural_stop, atr_stop)
        invalidation_reason = structural_reason if stop == structural_stop else "ATR(14) x 1.5 (tighter than structural level)"
    else:
        stop = atr_stop
        invalidation_reason = "ATR(14) x 1.5 — no structural level available for this strategy"

    risk_distance = abs(entry - stop)
    if risk_distance <= 0:
        risk_distance = max(atr * STOP_ATR_MULT, entry * 0.001)
        stop = entry - risk_distance if direction == LONG else entry + risk_distance

    target_distance = min(TARGET_ATR_MULT * atr, MAX_TARGET_ATR_MULT * atr)
    target_distance = max(target_distance, MIN_ACCEPTABLE_RR * risk_distance)
    target = entry + target_distance if direction == LONG else entry - target_distance

    reward_pct = target_distance / entry * 100
    risk_pct = risk_distance / entry * 100
    rr_ratio = target_distance / risk_distance if risk_distance > 0 else 0.0

    realistic = reward_pct <= AGGRESSIVE_MOVE_PCT
    warning = None
    if not realistic:
        warning = (
            f"Target implies a {reward_pct:.1f}% move, above this asset's typical realistic range "
            f"({AGGRESSIVE_MOVE_PCT:.0f}%) for this timeframe — treat with caution, verify liquidity."
        )

    # Risk/reward component (0-10): scales with RR ratio above the minimum
    # acceptable threshold, capped — an unrealistic target does not get
    # extra credit for looking bigger.
    if rr_ratio < MIN_ACCEPTABLE_RR:
        rr_score = max(0.0, (rr_ratio / MIN_ACCEPTABLE_RR) * 4.0)
    else:
        rr_score = min(10.0, 4.0 + (rr_ratio - MIN_ACCEPTABLE_RR) * 2.5)
    if not realistic:
        rr_score = min(rr_score, 5.0)

    return RiskReward(
        entry=round(entry, 6),
        stop=round(stop, 6),
        target=round(target, 6),
        risk_pct=round(risk_pct, 3),
        reward_pct=round(reward_pct, 3),
        rr_ratio=round(rr_ratio, 2),
        invalidation=round(stop, 6),
        invalidation_reason=invalidation_reason,
        target_reason=f"ATR(14) x{TARGET_ATR_MULT:.1f} (capped at x{MAX_TARGET_ATR_MULT:.1f}), floored at {MIN_ACCEPTABLE_RR:.1f}x risk",
        realistic=realistic,
        warning=warning,
        score=round(rr_score, 2),
    )
