"""Unit tests against SYNTHETIC fixtures (see tests/fixtures.py)."""
from __future__ import annotations

from app.data.news_client import NewsResult, catalyst_score
from app.regime.classifier import RegimeSnapshot, regime_fit_score
from app.risk.risk_reward import compute_risk_reward
from app.scoring.score import NO_TRADE, WATCH, build_signal, tier_for_score
from app.strategies.base import LONG, SHORT, StrategyCandidate


def _candidate(**overrides) -> StrategyCandidate:
    defaults = dict(
        strategy="breakout",
        symbol="TESTUSDT",
        direction=LONG,
        timestamp="2024-01-01T00:00:00Z",
        close=100.0,
        atr=2.0,
        reasons=["synthetic test reason"],
        momentum_score=15.0,
        volume_score=15.0,
        structure_score=15.0,
        range_high=98.0,
        range_low=90.0,
    )
    defaults.update(overrides)
    return StrategyCandidate(**defaults)


def test_catalyst_score_is_zero_when_no_news_configured():
    news = NewsResult(symbol="TESTUSDT", available=False, reason="no key")
    score, reason = catalyst_score(news, LONG)
    assert score == 0.0
    assert "no catalyst confirmed" in reason


def test_risk_reward_long_stop_below_entry_target_above():
    candidate = _candidate()
    rr = compute_risk_reward(candidate)
    assert rr.stop < candidate.close < rr.target
    assert rr.rr_ratio >= 1.5  # floored at MIN_ACCEPTABLE_RR by construction


def test_risk_reward_short_stop_above_entry_target_below():
    candidate = _candidate(direction=SHORT, range_high=110.0, range_low=100.0, close=100.0)
    rr = compute_risk_reward(candidate)
    assert rr.target < candidate.close < rr.stop


def test_unrealistic_target_is_flagged_not_hidden():
    # Deliberately huge ATR relative to price to force an outsized target.
    candidate = _candidate(atr=25.0, close=100.0)
    rr = compute_risk_reward(candidate)
    assert rr.reward_pct > 15.0
    assert rr.realistic is False
    assert rr.warning is not None


def test_tier_thresholds():
    assert tier_for_score(95) == "EXCEPTIONAL"
    assert tier_for_score(85) == "HIGH_QUALITY"
    assert tier_for_score(75) == WATCH
    assert tier_for_score(50) == NO_TRADE


def test_build_signal_produces_breakdown_summing_to_total():
    candidate = _candidate()
    snapshot = RegimeSnapshot(
        trend_regime="TRENDING_UP", volatility_regime="NORMAL_VOLATILITY",
        adx=30.0, atr_pct=0.02, atr_pct_percentile=0.5, ema_slope_pct=0.01,
    )
    news = NewsResult(symbol="TESTUSDT", available=False, reason="no key")
    signal = build_signal(candidate, snapshot, news)
    breakdown = signal.breakdown
    total = (
        breakdown.momentum + breakdown.volume + breakdown.structure
        + breakdown.regime + breakdown.catalyst + breakdown.risk_reward
    )
    assert round(total, 2) == signal.score
    assert breakdown.catalyst == 0.0  # no news source configured -> never assumed positive


def test_regime_fit_penalizes_breakout_in_range():
    trending = RegimeSnapshot("TRENDING_UP", "NORMAL_VOLATILITY", 30, 0.02, 0.5, 0.01)
    ranging = RegimeSnapshot("RANGE", "NORMAL_VOLATILITY", 10, 0.02, 0.5, 0.0)
    assert regime_fit_score("breakout", trending) > regime_fit_score("breakout", ranging)
