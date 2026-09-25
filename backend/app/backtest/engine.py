"""Event-driven backtest engine (section 11).

Design choices made explicitly to avoid the biases the spec calls out:

  - Look-ahead bias: every strategy call at bar i only ever sees
    `df.iloc[:i+1]` — the same view it would have had running live at the
    close of bar i. Indicators themselves are computed once, causally
    (rolling/EWM only look backward), which is why this is safe without
    recomputing them per-bar.
  - Fill realism: a signal generated at the close of bar i is filled at
    the OPEN of bar i+1, not at the signal bar's own close — you cannot
    trade a price after you already know the bar closed there.
  - Costs: every fill pays `fee_bps` and `slippage_bps` (config-driven,
    never zero unless explicitly set to zero) against the trader.
  - Ambiguous bars: if a single bar's range touches both the stop and the
    target, the stop is assumed to have been hit first (the conservative
    assumption a real risk-managed process should make).
  - No survivorship/data-leakage concern here since this always runs on
    one fixed, real symbol's full historical series, not a
    reconstituted universe.

This engine does not decide train/validation/out-of-sample split — that
bucketing happens afterwards, by entry timestamp, in `walk_forward.py` /
the API layer, using this same single causal run's trades.
"""
from __future__ import annotations

import datetime as dt
from dataclasses import dataclass

import pandas as pd

MAX_HOLDING_BARS_DEFAULT = 90  # 90 daily bars ≈ 4-4.5 months — matches the swing/position horizon


@dataclass
class Trade:
    symbol: str
    strategy: str
    direction: str
    entry_time: pd.Timestamp
    entry_price: float
    exit_time: pd.Timestamp
    exit_price: float
    stop: float
    target: float
    result: str  # TARGET_HIT / STOP_HIT / TIME_EXIT
    return_pct: float  # after fees + slippage
    holding_bars: int
    holding_minutes: float
    max_favorable_excursion_pct: float
    max_adverse_excursion_pct: float


def _apply_costs(price: float, direction: str, side: str, fee_bps: float, slippage_bps: float) -> float:
    """side: 'entry' or 'exit'. Slippage always moves the fill against the
    trader; fee is charged as a fraction of notional."""
    bps = (fee_bps + slippage_bps) / 10000.0
    if side == "entry":
        return price * (1 + bps) if direction == "LONG" else price * (1 - bps)
    return price * (1 - bps) if direction == "LONG" else price * (1 + bps)


@dataclass
class Exit:
    index: int
    raw_price: float
    result: str
    mfe_pct: float
    mae_pct: float


def resolve_exit(
    opens, highs, lows, closes,
    entry_index: int,
    direction: str,
    stop: float,
    target: float,
    max_holding_bars: int,
) -> Exit | None:
    """Walks bars from the entry bar onward on plain array-likes (fast
    enough for universe-wide research) and returns where the trade exits.

    Returns None when the entry bar already opens beyond the stop or the
    target: the setup was invalidated (or already paid out) overnight,
    before anyone could act on it, so there is no trade to take.

    A gap through a level fills at that bar's open, not at the level — a
    stop at 95 doesn't save you when the stock opens at 80 after earnings.
    """
    long = direction == "LONG"
    raw_entry = float(opens[entry_index])
    if (long and (raw_entry <= stop or raw_entry >= target)) or (not long and (raw_entry >= stop or raw_entry <= target)):
        return None

    mfe = mae = 0.0
    last_index = min(entry_index + max_holding_bars, len(opens) - 1)
    for j in range(entry_index, last_index + 1):
        o, h, l = float(opens[j]), float(highs[j]), float(lows[j])
        mfe = max(mfe, ((h - raw_entry) if long else (raw_entry - l)) / raw_entry * 100)
        mae = max(mae, ((raw_entry - l) if long else (h - raw_entry)) / raw_entry * 100)
        # Stop is checked first: if one bar spans both levels, assume the
        # worse outcome happened first.
        if (l <= stop) if long else (h >= stop):
            return Exit(j, min(stop, o) if long else max(stop, o), "STOP_HIT", mfe, mae)
        if (h >= target) if long else (l <= target):
            return Exit(j, max(target, o) if long else min(target, o), "TARGET_HIT", mfe, mae)
    # Neither level reached within the holding window: a real exit at the
    # last bar's close, not a fabricated hit.
    return Exit(last_index, float(closes[last_index]), "TIME_EXIT", mfe, mae)


def net_return_pct(raw_entry: float, raw_exit: float, direction: str, fee_bps: float, slippage_bps: float) -> float:
    entry = _apply_costs(raw_entry, direction, "entry", fee_bps, slippage_bps)
    exit_ = _apply_costs(raw_exit, direction, "exit", fee_bps, slippage_bps)
    return (exit_ - entry) / entry * 100 if direction == "LONG" else (entry - exit_) / entry * 100


def simulate_trade(
    df: pd.DataFrame,
    entry_index: int,
    direction: str,
    stop: float,
    target: float,
    fee_bps: float,
    slippage_bps: float,
    max_holding_bars: int,
) -> Trade | None:
    if entry_index >= len(df):
        return None
    exit_ = resolve_exit(
        df["open"].to_numpy(), df["high"].to_numpy(), df["low"].to_numpy(), df["close"].to_numpy(),
        entry_index, direction, stop, target, max_holding_bars,
    )
    if exit_ is None:
        return None

    raw_entry_price = float(df["open"].iloc[entry_index])
    entry_time = df["close_time"].iloc[entry_index - 1] if entry_index > 0 else df["open_time"].iloc[entry_index]
    exit_time = df["close_time"].iloc[exit_.index]
    return Trade(
        symbol="", strategy="", direction=direction,
        entry_time=entry_time,
        entry_price=_apply_costs(raw_entry_price, direction, "entry", fee_bps, slippage_bps),
        exit_time=exit_time,
        exit_price=_apply_costs(exit_.raw_price, direction, "exit", fee_bps, slippage_bps),
        stop=stop, target=target, result=exit_.result,
        return_pct=round(net_return_pct(raw_entry_price, exit_.raw_price, direction, fee_bps, slippage_bps), 4),
        holding_bars=exit_.index - entry_index + 1,
        holding_minutes=(exit_time - entry_time).total_seconds() / 60.0,
        max_favorable_excursion_pct=round(exit_.mfe_pct, 4),
        max_adverse_excursion_pct=round(exit_.mae_pct, 4),
    )


def run_backtest(
    df: pd.DataFrame,
    strategy_module,
    symbol: str,
    fee_bps: float,
    slippage_bps: float,
    warmup_bars: int = 210,
    max_holding_bars: int = MAX_HOLDING_BARS_DEFAULT,
) -> list[Trade]:
    """Runs one strategy over one already feature-enriched OHLCV history,
    bar by bar, and returns every completed trade. Skips bars while an
    equivalent trade is already open (one position at a time per symbol,
    matching how the live scanner also only carries one open signal)."""
    trades: list[Trade] = []
    in_position_until: pd.Timestamp | None = None

    for i in range(warmup_bars, len(df) - 1):
        bar_time = df["close_time"].iloc[i]
        if in_position_until is not None and bar_time <= in_position_until:
            continue

        window = df.iloc[: i + 1]
        candidate = strategy_module.generate(window, symbol)
        if candidate is None:
            continue

        from app.risk.risk_reward import compute_risk_reward

        rr = compute_risk_reward(candidate)
        trade = simulate_trade(
            df, i + 1, candidate.direction, rr.stop, rr.target, fee_bps, slippage_bps, max_holding_bars
        )
        if trade is None:
            continue
        trade.symbol = symbol
        trade.strategy = candidate.strategy
        trades.append(trade)
        in_position_until = trade.exit_time

    return trades
