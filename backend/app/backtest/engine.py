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

    raw_entry_price = float(df["open"].iloc[entry_index])
    entry_price = _apply_costs(raw_entry_price, direction, "entry", fee_bps, slippage_bps)
    entry_time = df["close_time"].iloc[entry_index - 1] if entry_index > 0 else df["open_time"].iloc[entry_index]

    mfe = 0.0
    mae = 0.0

    last_index = min(entry_index + max_holding_bars, len(df) - 1)
    for j in range(entry_index, last_index + 1):
        bar = df.iloc[j]
        high, low = float(bar["high"]), float(bar["low"])

        favorable = (high - raw_entry_price) if direction == "LONG" else (raw_entry_price - low)
        adverse = (raw_entry_price - low) if direction == "LONG" else (high - raw_entry_price)
        mfe = max(mfe, favorable / raw_entry_price * 100)
        mae = max(mae, adverse / raw_entry_price * 100)

        stop_hit = low <= stop if direction == "LONG" else high >= stop
        target_hit = high >= target if direction == "LONG" else low <= target

        if stop_hit:
            exit_raw = stop
            exit_price = _apply_costs(exit_raw, direction, "exit", fee_bps, slippage_bps)
            return_pct = (
                (exit_price - entry_price) / entry_price * 100
                if direction == "LONG"
                else (entry_price - exit_price) / entry_price * 100
            )
            return Trade(
                symbol="", strategy="", direction=direction,
                entry_time=entry_time, entry_price=entry_price,
                exit_time=bar["close_time"], exit_price=exit_price,
                stop=stop, target=target, result="STOP_HIT",
                return_pct=round(return_pct, 4), holding_bars=j - entry_index + 1,
                holding_minutes=(bar["close_time"] - entry_time).total_seconds() / 60.0,
                max_favorable_excursion_pct=round(mfe, 4), max_adverse_excursion_pct=round(mae, 4),
            )
        if target_hit:
            exit_raw = target
            exit_price = _apply_costs(exit_raw, direction, "exit", fee_bps, slippage_bps)
            return_pct = (
                (exit_price - entry_price) / entry_price * 100
                if direction == "LONG"
                else (entry_price - exit_price) / entry_price * 100
            )
            return Trade(
                symbol="", strategy="", direction=direction,
                entry_time=entry_time, entry_price=entry_price,
                exit_time=bar["close_time"], exit_price=exit_price,
                stop=stop, target=target, result="TARGET_HIT",
                return_pct=round(return_pct, 4), holding_bars=j - entry_index + 1,
                holding_minutes=(bar["close_time"] - entry_time).total_seconds() / 60.0,
                max_favorable_excursion_pct=round(mfe, 4), max_adverse_excursion_pct=round(mae, 4),
            )

    # Neither stop nor target hit within the holding window: close at the
    # last bar's close (a real, if unresolved, exit) — this is a genuine
    # TIME_EXIT outcome, not a fabricated one.
    last_bar = df.iloc[last_index]
    exit_raw = float(last_bar["close"])
    exit_price = _apply_costs(exit_raw, direction, "exit", fee_bps, slippage_bps)
    return_pct = (
        (exit_price - entry_price) / entry_price * 100
        if direction == "LONG"
        else (entry_price - exit_price) / entry_price * 100
    )
    return Trade(
        symbol="", strategy="", direction=direction,
        entry_time=entry_time, entry_price=entry_price,
        exit_time=last_bar["close_time"], exit_price=exit_price,
        stop=stop, target=target, result="TIME_EXIT",
        return_pct=round(return_pct, 4), holding_bars=last_index - entry_index + 1,
        holding_minutes=(last_bar["close_time"] - entry_time).total_seconds() / 60.0,
        max_favorable_excursion_pct=round(mfe, 4), max_adverse_excursion_pct=round(mae, 4),
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
