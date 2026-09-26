"""Position sizing: turns "here's a good setup" into "here's how much to
actually buy" — a fixed-fractional risk model, the standard, conservative
approach (never risk more than a small, fixed % of the portfolio on any
one trade, regardless of how confident the signal looks).

This is advisory math only, computed from numbers you provide (portfolio
size, risk per trade %) — it never executes anything and never assumes a
default portfolio size beyond what's configured in Settings.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PositionSize:
    portfolio_size_usd: float
    risk_per_trade_pct: float
    risk_amount_usd: float
    position_size_usd: float
    position_pct_of_portfolio: float
    units: float


def compute_position_size(
    entry: float, stop: float, portfolio_size_usd: float, risk_per_trade_pct: float,
    max_position_pct: float = 100.0, available_usd: float | None = None,
) -> PositionSize:
    """`max_position_pct` caps one position's share of the portfolio;
    `available_usd` (free capital not tied up in open positions) caps it
    further — the risk budget is then simply not fully used."""
    risk_distance_pct = abs(entry - stop) / entry
    risk_amount_usd = portfolio_size_usd * (risk_per_trade_pct / 100.0)

    if risk_distance_pct <= 0:
        # Degenerate input (entry == stop) — no valid size, don't divide by zero.
        return PositionSize(portfolio_size_usd, risk_per_trade_pct, risk_amount_usd, 0.0, 0.0, 0.0)

    position_size_usd = risk_amount_usd / risk_distance_pct
    # Never suggest risking more notional than the whole portfolio, even
    # if a very tight stop would otherwise imply a leveraged position size.
    position_size_usd = min(position_size_usd, portfolio_size_usd * min(max_position_pct, 100.0) / 100.0)
    if available_usd is not None:
        position_size_usd = max(0.0, min(position_size_usd, available_usd))
    risk_amount_usd = position_size_usd * risk_distance_pct
    units = position_size_usd / entry

    return PositionSize(
        portfolio_size_usd=portfolio_size_usd,
        risk_per_trade_pct=risk_per_trade_pct,
        risk_amount_usd=round(risk_amount_usd, 2),
        position_size_usd=round(position_size_usd, 2),
        position_pct_of_portfolio=round(position_size_usd / portfolio_size_usd * 100, 2) if portfolio_size_usd > 0 else 0.0,
        units=round(units, 8),
    )


def whole_shares(position_usd: float, price: float) -> tuple[int, float]:
    """Most Swedish brokers don't sell fractional US shares: the nearest
    whole number of shares and what that actually costs. (0, 0.0) when even
    one share costs more than twice the intended position — buying it would
    make the position far larger than the rule allows."""
    if price <= 0 or position_usd <= 0 or price > 2 * position_usd:
        return 0, 0.0
    shares = max(1, round(position_usd / price))
    return shares, round(shares * price, 2)
