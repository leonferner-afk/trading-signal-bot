"""Transparent 0-100 signal score (section 8).

Component weights (chosen to sum to 100, each tied to a real, independent
factor — no single indicator can dominate the score):

    Momentum      0-25   from the strategy's own price/indicator logic
    Volume        0-20   relative volume / volume trend confirmation
    Structure     0-20   market structure / breakout / mean-reversion quality
    Market regime 0-15   how well this strategy fits the CURRENT regime
    Catalyst      0-10   fresh, relevant news (0 when no data — never assumed)
    Risk/Reward   0-10   quality of the actual entry/stop/target math

A single strategy signal can score at most 100. Anything below
`score_watch_min` is NO_TRADE by construction — the quality filter drops it
before it ever reaches ranking.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from app.data.news_client import NewsResult, catalyst_score
from app.regime.classifier import RegimeSnapshot, regime_fit_score
from app.risk.risk_reward import RiskReward, compute_risk_reward
from app.strategies.base import StrategyCandidate

MOMENTUM_MAX = 25.0
VOLUME_MAX = 20.0
STRUCTURE_MAX = 20.0
REGIME_MAX = 15.0
CATALYST_MAX = 10.0
RISK_REWARD_MAX = 10.0
TOTAL_MAX = MOMENTUM_MAX + VOLUME_MAX + STRUCTURE_MAX + REGIME_MAX + CATALYST_MAX + RISK_REWARD_MAX
assert TOTAL_MAX == 100.0

NO_TRADE = "NO_TRADE"
WATCH = "WATCH"
HIGH_QUALITY = "HIGH_QUALITY"
EXCEPTIONAL = "EXCEPTIONAL"


@dataclass
class ScoreBreakdown:
    momentum: float
    momentum_max: float
    volume: float
    volume_max: float
    structure: float
    structure_max: float
    regime: float
    regime_max: float
    catalyst: float
    catalyst_max: float
    catalyst_reason: str
    risk_reward: float
    risk_reward_max: float
    total: float
    tier: str


@dataclass
class Signal:
    symbol: str
    strategy: str
    direction: str
    timestamp: str
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
    score: float
    tier: str
    breakdown: ScoreBreakdown
    reasons: list[str]
    regime_label: str
    market_wide_risk: str = "NEUTRAL"
    news_available: bool = False


def tier_for_score(
    score: float,
    *,
    exceptional_min: float | None = None,
    high_quality_min: float | None = None,
    watch_min: float | None = None,
) -> str:
    """Thresholds default to the live effective settings (env + any
    dashboard override); overridable here only so tests don't need to
    touch the DB."""
    if exceptional_min is None or high_quality_min is None or watch_min is None:
        from app.runtime_settings import get_effective_settings

        live = get_effective_settings()
        exceptional_min = exceptional_min if exceptional_min is not None else live.score_exceptional_min
        high_quality_min = high_quality_min if high_quality_min is not None else live.score_high_quality_min
        watch_min = watch_min if watch_min is not None else live.score_watch_min

    if score >= exceptional_min:
        return EXCEPTIONAL
    if score >= high_quality_min:
        return HIGH_QUALITY
    if score >= watch_min:
        return WATCH
    return NO_TRADE


def build_signal(
    candidate: StrategyCandidate,
    regime_snapshot: RegimeSnapshot,
    news: NewsResult,
    market_wide_risk: str = "NEUTRAL",
    *,
    tier_thresholds: tuple[float, float, float] | None = None,
) -> Signal:
    """`tier_thresholds` = (exceptional, high_quality, watch) minimums;
    omit to use the live settings. Research passes them explicitly so a
    million-bar backtest doesn't hit the settings DB on every bar."""
    regime_component = regime_fit_score(candidate.strategy, regime_snapshot) / 10.0 * REGIME_MAX
    catalyst_component, catalyst_reason = catalyst_score(news, candidate.direction)

    rr: RiskReward = compute_risk_reward(candidate)

    momentum = min(candidate.momentum_score, MOMENTUM_MAX)
    volume = min(candidate.volume_score, VOLUME_MAX)
    structure = min(candidate.structure_score, STRUCTURE_MAX)
    risk_reward_component = min(rr.score, RISK_REWARD_MAX)

    total = round(
        momentum + volume + structure + regime_component + catalyst_component + risk_reward_component, 2
    )
    if tier_thresholds is None:
        tier = tier_for_score(total)
    else:
        exceptional_min, high_quality_min, watch_min = tier_thresholds
        tier = tier_for_score(total, exceptional_min=exceptional_min, high_quality_min=high_quality_min, watch_min=watch_min)

    breakdown = ScoreBreakdown(
        momentum=round(momentum, 2),
        momentum_max=MOMENTUM_MAX,
        volume=round(volume, 2),
        volume_max=VOLUME_MAX,
        structure=round(structure, 2),
        structure_max=STRUCTURE_MAX,
        regime=round(regime_component, 2),
        regime_max=REGIME_MAX,
        catalyst=round(catalyst_component, 2),
        catalyst_max=CATALYST_MAX,
        catalyst_reason=catalyst_reason,
        risk_reward=round(risk_reward_component, 2),
        risk_reward_max=RISK_REWARD_MAX,
        total=total,
        tier=tier,
    )

    reasons = list(candidate.reasons)
    reasons.append(f"regime fit: {regime_snapshot.trend_regime} / {regime_snapshot.volatility_regime}")
    if catalyst_component > 0:
        reasons.append(catalyst_reason)

    return Signal(
        symbol=candidate.symbol,
        strategy=candidate.strategy,
        direction=candidate.direction,
        timestamp=candidate.timestamp.isoformat() if hasattr(candidate.timestamp, "isoformat") else str(candidate.timestamp),
        entry=rr.entry,
        stop=rr.stop,
        target=rr.target,
        risk_pct=rr.risk_pct,
        reward_pct=rr.reward_pct,
        rr_ratio=rr.rr_ratio,
        invalidation=rr.invalidation,
        invalidation_reason=rr.invalidation_reason,
        target_reason=rr.target_reason,
        realistic=rr.realistic,
        warning=rr.warning,
        score=total,
        tier=tier,
        breakdown=breakdown,
        reasons=reasons,
        regime_label=regime_snapshot.label,
        market_wide_risk=market_wide_risk,
        news_available=news.available,
    )
