"""Rocket rules on SYNTHETIC inputs only (no network): event detection,
the trailing exit, and the comparison with random entries. Says nothing
about real performance."""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from app import rockets as rk


def _df(closes, volumes=None, highs=None, lows=None):
    closes = np.asarray(closes, float)
    n = len(closes)
    return pd.DataFrame({"open": closes, "high": highs if highs is not None else closes * 1.01,
                         "low": lows if lows is not None else closes * 0.99, "close": closes,
                         "volume": volumes if volumes is not None else np.full(n, 1e6)})


def test_rocket_day_needs_jump_volume_strong_close_and_liquidity():
    closes = [20.0] * 25 + [23.2]                      # +16% on the last day
    vols = [1e6] * 25 + [5e6]                          # 5x volume
    highs = np.array(closes) * 1.01
    lows = np.array(closes) * 0.99
    highs[-1], lows[-1] = 23.3, 21.0                   # closed near the day's high
    f = rk.event_features(_df(closes, vols, highs, lows))
    assert rk.is_rocket(f, 0.08).iloc[-1] and rk.is_rocket(f, 0.15).iloc[-1]
    assert not rk.is_rocket(f, 0.17).iloc[-1]
    # Same jump but it closed at the day's low -> sellers won, not a rocket.
    lows2 = lows.copy(); highs2 = highs.copy(); highs2[-1] = 26.0; lows2[-1] = 23.1
    assert not rk.is_rocket(rk.event_features(_df(closes, vols, highs2, lows2)), 0.08).iloc[-1]
    # Normal volume -> not a rocket.
    assert not rk.is_rocket(rk.event_features(_df(closes, [1e6] * 26, highs, lows)), 0.08).iloc[-1]
    # Penny stock / illiquid -> not a rocket.
    cheap = [c / 10 for c in closes]
    assert not rk.is_rocket(rk.event_features(_df(cheap, vols, highs / 10, lows / 10)), 0.08).iloc[-1]


def test_trailing_exit_lets_winners_run_and_sells_next_open():
    #          signal  fill 100  up...        peak 150   falls 25% -> 112 (<= 112.5)   exit at next open
    closes = np.array([90, 100, 120, 150, 140, 112, 110, 108.0])
    opens = np.array([90, 100, 110, 130, 150, 139, 111, 109.0])
    k, price, reason = rk.trailing_exit(opens, closes, 0, trail=0.25)
    assert (k, price, reason) == (6, 111.0, "trail")
    # Data ends before the exit is known -> not counted yet.
    assert rk.trailing_exit(opens[:6], closes[:6], 0, trail=0.25) is None


def test_time_exit_after_max_hold():
    closes = np.full(60, 100.0)
    k, price, reason = rk.trailing_exit(closes, closes, 0, trail=0.25, max_hold=40)
    assert reason == "time" and k == 41  # held sessions 1..40, sold at the next open


def test_monthly_excess_against_random_entries():
    months = [f"2025-{m:02d}-10" for m in range(1, 9)]
    rockets = pd.DataFrame({"date": months, "ret_pct": [5, 3, 8, 4, 6, 2, 7, 5]})
    base = pd.DataFrame({"date": months, "ret_pct": [1, 1, 2, 0, 1, 1, 2, 1]})
    ex = rk.monthly_excess(rockets, base)
    assert ex["months"] == 8 and ex["avg_excess_pct"] == pytest.approx(3.875) and ex["t_month"] > 2


def test_gates_require_every_check():
    spy_tv, spy = {"cagr_pct": 14.0, "sharpe": 0.8}, {"cagr_pct": 15.0}
    good = {"portfolio_train_val": {"cagr_pct": 20.0, "sharpe": 0.9}, "portfolio": {"max_drawdown_pct": -40.0},
            "excess_train_val": {"t_month": 2.5}, "excess_largecap": {"avg_excess_pct": 0.4},
            "without_top3": {"cagr_pct": 16.0}}
    assert rk.rocket_gates(good, spy_tv, spy)["passes"]
    lucky = {**good, "without_top3": {"cagr_pct": 5.0}}
    assert rk.rocket_gates(lucky, spy_tv, spy)["checks"]["without_top3_beats_spy"] is False
    crashy = {**good, "portfolio": {"max_drawdown_pct": -70.0}}
    assert not rk.rocket_gates(crashy, spy_tv, spy)["passes"]
