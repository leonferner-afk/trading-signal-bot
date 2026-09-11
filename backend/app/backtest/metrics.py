"""Backtest performance metrics (section 11) — every number here is
computed directly from a list of `Trade` objects that already include
fees and slippage. There is no "before costs" view: a strategy that only
looks profitable pre-cost is reported as NOT_PROFITABLE_AFTER_COSTS.
"""
from __future__ import annotations

import math
from collections import Counter
from dataclasses import dataclass

from app.backtest.engine import Trade

NOT_PROFITABLE_AFTER_COSTS = "NOT_PROFITABLE_AFTER_COSTS"
PROFITABLE = "PROFITABLE_AFTER_COSTS"
INSUFFICIENT_DATA = "INSUFFICIENT_DATA"


@dataclass
class BacktestMetrics:
    num_trades: int
    win_rate: float | None
    average_win_pct: float | None
    average_loss_pct: float | None
    expectancy_pct: float | None
    profit_factor: float | None
    max_drawdown_pct: float | None
    sharpe_per_trade: float | None
    average_holding_minutes: float | None
    return_after_costs_pct: float | None  # sum of per-trade returns (already cost-adjusted)
    classification: str

    def to_dict(self) -> dict:
        return {
            "num_trades": self.num_trades,
            "win_rate": self.win_rate,
            "average_win_pct": self.average_win_pct,
            "average_loss_pct": self.average_loss_pct,
            "expectancy_pct": self.expectancy_pct,
            "profit_factor": self.profit_factor,
            "max_drawdown_pct": self.max_drawdown_pct,
            "sharpe_per_trade": self.sharpe_per_trade,
            "average_holding_minutes": self.average_holding_minutes,
            "return_after_costs_pct": self.return_after_costs_pct,
            "classification": self.classification,
        }


MIN_TRADES_FOR_CLASSIFICATION = 20


def compute_metrics(trades: list[Trade]) -> BacktestMetrics:
    if not trades:
        return BacktestMetrics(
            num_trades=0, win_rate=None, average_win_pct=None, average_loss_pct=None,
            expectancy_pct=None, profit_factor=None, max_drawdown_pct=None,
            sharpe_per_trade=None, average_holding_minutes=None, return_after_costs_pct=None,
            classification=INSUFFICIENT_DATA,
        )

    returns = [t.return_pct for t in trades]
    wins = [r for r in returns if r > 0]
    losses = [r for r in returns if r <= 0]

    win_rate = len(wins) / len(returns)
    avg_win = sum(wins) / len(wins) if wins else 0.0
    avg_loss = sum(losses) / len(losses) if losses else 0.0
    expectancy = sum(returns) / len(returns)
    gross_profit = sum(wins)
    gross_loss = abs(sum(losses))
    profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else (float("inf") if gross_profit > 0 else None)

    equity = []
    running = 0.0
    for r in returns:
        running += r
        equity.append(running)
    peak = float("-inf")
    max_dd = 0.0
    for value in equity:
        peak = max(peak, value)
        max_dd = min(max_dd, value - peak)

    mean_r = expectancy
    variance = sum((r - mean_r) ** 2 for r in returns) / len(returns)
    std_r = math.sqrt(variance)
    sharpe = (mean_r / std_r) if std_r > 0 else None

    avg_holding = sum(t.holding_minutes for t in trades) / len(trades)
    return_after_costs = sum(returns)

    if len(trades) < MIN_TRADES_FOR_CLASSIFICATION:
        classification = INSUFFICIENT_DATA
    elif expectancy is not None and expectancy > 0 and (profit_factor is None or profit_factor > 1.0):
        classification = PROFITABLE
    else:
        classification = NOT_PROFITABLE_AFTER_COSTS

    return BacktestMetrics(
        num_trades=len(trades),
        win_rate=round(win_rate, 4),
        average_win_pct=round(avg_win, 4),
        average_loss_pct=round(avg_loss, 4),
        expectancy_pct=round(expectancy, 4),
        profit_factor=round(profit_factor, 4) if profit_factor not in (None, float("inf")) else profit_factor,
        max_drawdown_pct=round(max_dd, 4),
        sharpe_per_trade=round(sharpe, 4) if sharpe is not None else None,
        average_holding_minutes=round(avg_holding, 1),
        return_after_costs_pct=round(return_after_costs, 4),
        classification=classification,
    )


def entry_hour_timing_pattern(trades: list[Trade], top_n: int = 3, min_trades: int = 20) -> dict:
    """Real, backtest-derived answer to "roughly when does this setup tend
    to trigger" — a histogram of each trade's entry hour (UTC), reduced to
    the top `top_n` most common hours. Requires at least `min_trades` to
    say anything (a pattern from a handful of trades isn't a pattern, it's
    noise) — returns {} rather than a misleading result below that."""
    if len(trades) < min_trades:
        return {}
    hours = [t.entry_time.hour for t in trades]
    counts = Counter(hours)
    common = [hour for hour, _ in counts.most_common(top_n)]
    return {
        "common_hours_utc": sorted(common),
        "based_on_trades": len(trades),
        "hour_histogram_utc": dict(sorted(counts.items())),
    }
