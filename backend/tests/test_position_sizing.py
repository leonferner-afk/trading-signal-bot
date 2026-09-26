"""Unit tests for the fixed-fractional position sizing model."""
from __future__ import annotations

from app.risk.position_sizing import compute_position_size


def test_basic_sizing_matches_hand_calculation():
    # Entry 100, stop 95 -> 5% risk distance. Risking 1% of a $1000
    # portfolio = $10 risk budget -> position size = $10 / 0.05 = $200.
    size = compute_position_size(entry=100, stop=95, portfolio_size_usd=1000, risk_per_trade_pct=1.0)
    assert size.risk_amount_usd == 10.0
    assert size.position_size_usd == 200.0
    assert size.units == 2.0
    assert size.position_pct_of_portfolio == 20.0


def test_tighter_stop_means_larger_position_for_same_risk():
    tight = compute_position_size(entry=100, stop=99, portfolio_size_usd=1000, risk_per_trade_pct=1.0)
    wide = compute_position_size(entry=100, stop=90, portfolio_size_usd=1000, risk_per_trade_pct=1.0)
    assert tight.position_size_usd > wide.position_size_usd


def test_position_size_never_exceeds_portfolio():
    # An extremely tight stop would imply a huge (leveraged) position —
    # capped at the full portfolio instead.
    size = compute_position_size(entry=100, stop=99.99, portfolio_size_usd=1000, risk_per_trade_pct=5.0)
    assert size.position_size_usd <= 1000.0


def test_degenerate_zero_distance_does_not_crash():
    size = compute_position_size(entry=100, stop=100, portfolio_size_usd=1000, risk_per_trade_pct=1.0)
    assert size.position_size_usd == 0.0
    assert size.units == 0.0


def test_position_is_capped_by_max_share_and_free_capital():
    # 1% stop at 1% risk would be 100% of the portfolio; capped at 25%.
    size = compute_position_size(entry=100, stop=99, portfolio_size_usd=10000, risk_per_trade_pct=1.0, max_position_pct=25)
    assert size.position_size_usd == 2500.0
    assert size.risk_amount_usd == 25.0  # the actual risk, smaller than the 1% budget
    # Only $1000 free -> only $1000 position.
    size = compute_position_size(entry=100, stop=95, portfolio_size_usd=10000, risk_per_trade_pct=1.0,
                                 max_position_pct=25, available_usd=1000)
    assert size.position_size_usd == 1000.0 and size.units == 10.0
