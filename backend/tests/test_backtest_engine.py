"""Unit tests against SYNTHETIC fixtures (see tests/fixtures.py) —
verifying the backtest engine's mechanics (fills, costs, stop-priority,
holding-time cap), not any claim about real strategy performance."""
from __future__ import annotations

import pandas as pd

from app.backtest.engine import _apply_costs, simulate_trade
from app.backtest.metrics import compute_metrics
from app.backtest.walk_forward import train_validation_oos_split, walk_forward_analysis
from tests.fixtures import make_synthetic_ohlcv


def test_apply_costs_moves_fill_against_trader():
    entry_long = _apply_costs(100.0, "LONG", "entry", fee_bps=10, slippage_bps=5)
    assert entry_long > 100.0  # long entry costs more than the raw price
    exit_long = _apply_costs(100.0, "LONG", "exit", fee_bps=10, slippage_bps=5)
    assert exit_long < 100.0  # long exit receives less than the raw price


def test_simulate_trade_hits_target_long():
    df = make_synthetic_ohlcv(n=10, start_price=100.0, trend_per_bar=0.0, volatility=0.01)
    # Force bar 5 to spike well above target.
    df.iloc[5, df.columns.get_loc("high")] = 200.0
    df.iloc[5, df.columns.get_loc("low")] = 99.0
    trade = simulate_trade(
        df, entry_index=1, direction="LONG", stop=95.0, target=110.0,
        fee_bps=0, slippage_bps=0, max_holding_bars=20,
    )
    assert trade is not None
    assert trade.result == "TARGET_HIT"
    assert trade.return_pct > 0


def test_simulate_trade_hits_stop_short():
    df = make_synthetic_ohlcv(n=10, start_price=100.0, trend_per_bar=0.0, volatility=0.01)
    df.iloc[3, df.columns.get_loc("high")] = 130.0  # blows through the short's stop
    df.iloc[3, df.columns.get_loc("low")] = 99.0
    trade = simulate_trade(
        df, entry_index=1, direction="SHORT", stop=120.0, target=80.0,
        fee_bps=0, slippage_bps=0, max_holding_bars=20,
    )
    assert trade is not None
    assert trade.result == "STOP_HIT"
    assert trade.return_pct < 0


def test_simulate_trade_prefers_stop_when_both_hit_same_bar():
    df = make_synthetic_ohlcv(n=5, start_price=100.0, volatility=0.01)
    # A single bar whose range spans both the stop and the target.
    df.iloc[2, df.columns.get_loc("high")] = 115.0
    df.iloc[2, df.columns.get_loc("low")] = 85.0
    trade = simulate_trade(
        df, entry_index=1, direction="LONG", stop=90.0, target=110.0,
        fee_bps=0, slippage_bps=0, max_holding_bars=20,
    )
    assert trade.result == "STOP_HIT"  # conservative assumption


def test_simulate_trade_times_out_without_fabricating_a_hit():
    df = make_synthetic_ohlcv(n=10, start_price=100.0, trend_per_bar=0.0, volatility=0.001)
    trade = simulate_trade(
        df, entry_index=1, direction="LONG", stop=1.0, target=1000.0,
        fee_bps=0, slippage_bps=0, max_holding_bars=3,
    )
    assert trade.result == "TIME_EXIT"
    assert trade.holding_bars == 4  # entry_index..entry_index+max_holding_bars inclusive


def test_metrics_flags_losing_strategy_as_not_profitable():
    from app.backtest.engine import Trade

    losing_trades = [
        Trade(
            symbol="TEST", strategy="test", direction="LONG",
            entry_time=pd.Timestamp("2024-01-01"), entry_price=100, exit_time=pd.Timestamp("2024-01-02"),
            exit_price=95, stop=95, target=110, result="STOP_HIT", return_pct=-5.0,
            holding_bars=5, holding_minutes=300, max_favorable_excursion_pct=1.0, max_adverse_excursion_pct=5.0,
        )
        for _ in range(25)
    ]
    metrics = compute_metrics(losing_trades)
    assert metrics.classification == "NOT_PROFITABLE_AFTER_COSTS"
    assert metrics.win_rate == 0.0


def test_split_and_walk_forward_handle_empty_trades_honestly():
    split = train_validation_oos_split([])
    assert split.reliable is False
    assert split.out_of_sample_trades == []
    wf = walk_forward_analysis([])
    assert wf.consistent is False
    assert wf.windows == []


def test_entry_hour_timing_pattern_requires_minimum_trades():
    from app.backtest.engine import Trade
    from app.backtest.metrics import entry_hour_timing_pattern

    few_trades = [
        Trade(
            symbol="TEST", strategy="test", direction="LONG",
            entry_time=pd.Timestamp("2024-01-01T14:00:00Z"), entry_price=100, exit_time=pd.Timestamp("2024-01-01T16:00:00Z"),
            exit_price=105, stop=95, target=110, result="TARGET_HIT", return_pct=5.0,
            holding_bars=2, holding_minutes=120, max_favorable_excursion_pct=5.0, max_adverse_excursion_pct=0.5,
        )
        for _ in range(5)
    ]
    assert entry_hour_timing_pattern(few_trades, min_trades=20) == {}


def test_entry_hour_timing_pattern_finds_common_hours():
    from app.backtest.engine import Trade
    from app.backtest.metrics import entry_hour_timing_pattern

    trades = []
    # 15 trades entered at hour 14 UTC, 10 at hour 9 UTC — hour 14 should
    # dominate the "common hours" result.
    for hour, count in ((14, 15), (9, 10)):
        for i in range(count):
            trades.append(
                Trade(
                    symbol="TEST", strategy="test", direction="LONG",
                    entry_time=pd.Timestamp(f"2024-01-{(i % 27) + 1:02d}T{hour:02d}:00:00Z"),
                    entry_price=100, exit_time=pd.Timestamp(f"2024-01-{(i % 27) + 1:02d}T{hour + 2:02d}:00:00Z"),
                    exit_price=105, stop=95, target=110, result="TARGET_HIT", return_pct=5.0,
                    holding_bars=2, holding_minutes=120, max_favorable_excursion_pct=5.0, max_adverse_excursion_pct=0.5,
                )
            )
    pattern = entry_hour_timing_pattern(trades, top_n=1, min_trades=20)
    assert pattern["common_hours_utc"] == [14]
    assert pattern["based_on_trades"] == 25
