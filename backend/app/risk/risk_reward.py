"""Risk/reward calculation (section 9).

Entry/stop/target/invalidation are derived from the same real inputs used
to generate the signal — ATR and the structural levels the strategy
already identified — never a hardcoded percentage. If the resulting
reward is unrealistically large, that is surfaced as a warning and a
poor risk/reward score, not silently inflated.

Tuned for the swing/position-trade concept (daily bars, a
few-weeks-to-a-few-months holding window, hunting for a handful of large
moves rather than many small ones) — not the old intraday-crypto scalping
calibration:

  - TARGET_ATR_MULT is wide (10x the daily ATR) so a genuinely volatile
    setup can size a target in the "could double in a month" range this
    system is meant to hunt for (a stock with a ~10%/day ATR times 10 =
    a 100% target) — real target_distance is always exactly this multiple
    of ATR in practice (the MIN_ACCEPTABLE_RR floor and MAX_TARGET_ATR_MULT
    ceiling exist as safety bounds but, given how tightly STOP_ATR_MULT
    keeps risk_distance, don't bind under normal inputs).
  - "Is this target realistic" is a fixed cap on the implied % move
    (AGGRESSIVE_MOVE_PCT). Since target size scales with the asset's own
    ATR%, this cap naturally only fires for the most extreme, penny-stock-
    grade volatility — a deliberately high bar, not a limit on ordinary
    big-mover targets.
"""
from __future__ import annotations

from dataclasses import dataclass

from app.strategies.base import LONG, StrategyCandidate

MIN_ACCEPTABLE_RR = 1.5
STOP_ATR_MULT = 1.5
TARGET_ATR_MULT = 10.0
STOP_BUFFER_ATR_MULT = 0.25
MAX_TARGET_ATR_MULT = 30.0
# A ~1-month-horizon target above this implied % move gets flagged — set
# high on purpose (this system is explicitly hunting rare, large moves),
# it only catches the most extreme cases (roughly: an 8%+ single-day ATR).
AGGRESSIVE_MOVE_PCT = 80.0


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
        atr_pct_daily = atr / entry * 100
        warning = (
            f"Target implies a {reward_pct:.1f}% move (this stock's own ATR is {atr_pct_daily:.1f}%/day) — "
            f"above this system's {AGGRESSIVE_MOVE_PCT:.0f}% caution threshold. Extremely volatile setups like "
            f"this are exactly what can produce a huge winner, but also carry the most liquidity/gap risk — "
            f"verify both before sizing in."
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
