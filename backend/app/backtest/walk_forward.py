"""Train/validation/out-of-sample split and walk-forward analysis
(sections 11-12).

Both operate on the trades produced by ONE continuous, causal
`run_backtest` pass over the full history — never by re-running the
backtest on truncated slices. Truncating the price history per split
would either reintroduce look-ahead (if indicator warmup borrowed data
from outside the slice) or corrupt the warmup period at the start of each
split; bucketing trades by entry time after a single causal run avoids
both problems while still answering the real question each split exists
for: does the edge hold on data the strategy logic was not "shaped
around" (train), on a held-out middle period (validation), and on the
most recent, never-touched period (out-of-sample)?

The strategies in this codebase are fixed, rule-based logic — there is no
parameter fitting step, so "training" here means nothing is tuned on that
slice; it exists purely so train-period performance can be compared
against validation/out-of-sample performance to catch a rule set that
only happens to work on one historical stretch.
"""
from __future__ import annotations

from dataclasses import dataclass

from app.backtest.engine import Trade
from app.backtest.metrics import NOT_PROFITABLE_AFTER_COSTS, PROFITABLE, BacktestMetrics, compute_metrics

TRAIN_FRACTION = 0.6
VALIDATION_FRACTION = 0.2
# remaining 0.2 is out-of-sample


@dataclass
class SplitResult:
    train: BacktestMetrics
    validation: BacktestMetrics
    out_of_sample: BacktestMetrics
    reliable: bool
    reliability_reason: str


def train_validation_oos_split(trades: list[Trade]) -> SplitResult:
    if not trades:
        empty = compute_metrics([])
        return SplitResult(
            train=empty, validation=empty, out_of_sample=empty,
            reliable=False, reliability_reason="No trades were generated over the requested period.",
        )

    ordered = sorted(trades, key=lambda t: t.entry_time)
    n = len(ordered)
    train_end = int(n * TRAIN_FRACTION)
    val_end = train_end + int(n * VALIDATION_FRACTION)

    train_trades = ordered[:train_end]
    val_trades = ordered[train_end:val_end]
    oos_trades = ordered[val_end:]

    train_metrics = compute_metrics(train_trades)
    val_metrics = compute_metrics(val_trades)
    oos_metrics = compute_metrics(oos_trades)

    reliable, reason = _assess_reliability(train_metrics, val_metrics, oos_metrics)

    return SplitResult(
        train=train_metrics, validation=val_metrics, out_of_sample=oos_metrics,
        reliable=reliable, reliability_reason=reason,
    )


def _assess_reliability(train: BacktestMetrics, validation: BacktestMetrics, oos: BacktestMetrics) -> tuple[bool, str]:
    if oos.classification == "INSUFFICIENT_DATA" or validation.classification == "INSUFFICIENT_DATA":
        return False, "Not enough validation/out-of-sample trades to assess reliability (need >= 20 each)."

    if train.classification == PROFITABLE and oos.classification != PROFITABLE:
        return False, (
            f"Profitable in-sample (expectancy {train.expectancy_pct}%) but "
            f"{oos.classification.replace('_', ' ').lower()} out-of-sample (expectancy {oos.expectancy_pct}%) "
            "— likely overfit to the training period."
        )

    if oos.classification != PROFITABLE:
        return False, f"Out-of-sample result is {oos.classification.replace('_', ' ').lower()} after fees and slippage."

    if train.win_rate and oos.win_rate and abs(train.win_rate - oos.win_rate) > 0.25:
        return False, (
            f"Win rate degrades sharply out-of-sample ({train.win_rate:.0%} train vs {oos.win_rate:.0%} OOS) "
            "— edge is not stable."
        )

    return True, "Out-of-sample performance is consistent with training/validation — no overfitting signal detected."


@dataclass
class WalkForwardWindow:
    window_index: int
    start: str
    end: str
    metrics: BacktestMetrics


@dataclass
class WalkForwardResult:
    windows: list[WalkForwardWindow]
    consistent: bool
    consistency_reason: str


def walk_forward_analysis(trades: list[Trade], num_windows: int = 5) -> WalkForwardResult:
    """Slices the trade timeline into `num_windows` consecutive,
    non-overlapping windows (TRAIN -> TEST -> MOVE WINDOW, applied here as
    sequential out-of-sample windows over fixed rule-based logic) and
    reports whether the edge holds across all of them."""
    if not trades:
        return WalkForwardResult(windows=[], consistent=False, consistency_reason="No trades to analyze.")

    ordered = sorted(trades, key=lambda t: t.entry_time)
    n = len(ordered)
    if n < num_windows * 5:
        return WalkForwardResult(
            windows=[], consistent=False,
            consistency_reason=f"Only {n} trades total — need at least {num_windows * 5} for a {num_windows}-window walk-forward.",
        )

    window_size = n // num_windows
    windows: list[WalkForwardWindow] = []
    for w in range(num_windows):
        start_idx = w * window_size
        end_idx = n if w == num_windows - 1 else (w + 1) * window_size
        chunk = ordered[start_idx:end_idx]
        if not chunk:
            continue
        metrics = compute_metrics(chunk)
        windows.append(
            WalkForwardWindow(
                window_index=w + 1,
                start=chunk[0].entry_time.isoformat(),
                end=chunk[-1].entry_time.isoformat(),
                metrics=metrics,
            )
        )

    profitable_windows = sum(1 for w in windows if w.metrics.classification == PROFITABLE)
    consistent = profitable_windows >= max(1, int(len(windows) * 0.6))
    reason = (
        f"{profitable_windows}/{len(windows)} windows profitable after costs "
        f"({'edge appears stable over time' if consistent else 'edge does not hold consistently over time — flag as unreliable'})."
    )
    return WalkForwardResult(windows=windows, consistent=consistent, consistency_reason=reason)
