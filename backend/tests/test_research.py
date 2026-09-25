"""Research mechanics on SYNTHETIC inputs only (no network): trailing
exits, relative-strength ranking, policy filtering and the portfolio
simulation's bookkeeping. Says nothing about real strategy performance."""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from app.research import attach_relative_strength, policy_mask, resolve_trailing_exit, simulate_portfolio, take_positions


def test_trailing_exit_lets_a_winner_run_then_trails_it_out():
    # Up 10% a day for 5 days, then a -30% day.
    closes = np.array([100, 100, 110, 121, 133, 146, 102.0])
    opens = np.concatenate([[100.0], closes[:-1]])
    highs, lows = closes * 1.01, np.minimum(opens, closes) * 0.99
    exit_ = resolve_trailing_exit(opens, highs, lows, closes, 1, initial_stop=95.0, trail_pct=0.15, max_hold=50)
    assert exit_.result == "TRAIL_STOP"
    # Trailing level after day 5's high (146*1.01) is ~125; day 6 gaps below it and fills at the open.
    assert exit_.raw_price == pytest.approx(min(146 * 1.01 * 0.85, opens[6]))
    assert exit_.raw_price > 120  # kept most of the run instead of a fixed small target


def test_trailing_exit_initial_stop_and_gap_invalidation():
    opens = np.array([100, 94, 90.0])
    assert resolve_trailing_exit(opens, opens * 1.01, opens * 0.99, opens, 1, 95.0, 0.1, 10) is None
    opens = np.array([100, 100, 93.0])
    closes = np.array([100, 99, 92.0])
    exit_ = resolve_trailing_exit(opens, opens * 1.005, closes * 0.99, closes, 1, 95.0, 0.1, 10)
    assert exit_.result == "STOP_HIT" and exit_.raw_price == 93.0  # gapped through the stop


def test_relative_strength_is_a_cross_sectional_percentile():
    returns = {
        "A": pd.Series([0.10, 0.50], index=["2025-01-02", "2025-01-03"]),
        "B": pd.Series([0.20, 0.10], index=["2025-01-02", "2025-01-03"]),
    }
    rows = pd.DataFrame({"symbol": ["A", "B", "A"], "date": ["2025-01-02", "2025-01-02", "2025-01-03"]})
    out = attach_relative_strength(rows, returns).set_index(["symbol", "date"])["rs"]
    assert out[("B", "2025-01-02")] == 1.0 and out[("A", "2025-01-02")] == 0.5 and out[("A", "2025-01-03")] == 1.0


def _trades(rows: list[dict]) -> pd.DataFrame:
    base = {"score": 75.0, "spy_above_200": True, "stock_above_200": True, "rs": 0.9, "near_high": 0.95,
            "stop_dist_pct": 5.0, "r_multiple": 1.0, "ret_pct": 5.0, "hold_bars": 3}
    return pd.DataFrame([{**base, **r} for r in rows])


def test_policy_mask_and_one_position_per_symbol():
    d = _trades([
        {"symbol": "A", "i": 1, "exit_i": 5, "date": "2025-01-01"},
        {"symbol": "A", "i": 3, "exit_i": 8, "date": "2025-01-03"},   # still in the first trade -> skipped
        {"symbol": "A", "i": 6, "exit_i": 9, "date": "2025-01-06"},   # after exit -> taken
        {"symbol": "B", "i": 2, "exit_i": 4, "date": "2025-01-02", "rs": 0.5},
    ])
    assert list(policy_mask(d, 70, True, True, 0.8, 0)) == [True, True, True, False]
    taken = take_positions(d[policy_mask(d, 70, True, True, 0.8, 0)])
    assert sorted(taken["i"]) == [1, 6]


def test_portfolio_sizes_by_risk_and_caps_positions():
    d = _trades([
        {"symbol": s, "date": "2025-01-02", "exit_date": "2025-02-03", "ret_pct": 10.0, "score": score}
        for s, score in (("A", 90), ("B", 80), ("C", 70), ("D", 60))
    ])
    res = simulate_portfolio(d, "score", max_open=8, max_new=3, risk_pct=1.0)
    # 3 new buys max per day; each sized 1% risk / 5% stop = 20% of equity; +10% each -> +6% total.
    assert res["trades"] == 3
    assert res["total_return_pct"] == pytest.approx(6.0)
