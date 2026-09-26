"""Research mechanics on SYNTHETIC inputs only (no network): cost
handling, relative-strength ranking, policy filtering, the per-trade
statistics and the day-by-day portfolio simulation's bookkeeping. Says
nothing about real strategy performance."""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from app.research import (
    MAX_NEW_PER_DAY,
    MAX_POSITION_PCT,
    PriceBook,
    attach_relative_strength,
    excess_vs_baseline,
    net_return_pct,
    policy_mask,
    r_multiple,
    simulate_portfolio,
    split_dates,
    summarize,
    take_positions,
    with_costs,
)


def test_costs_are_charged_on_both_sides():
    assert net_return_pct(100.0, 110.0, 0) == pytest.approx(10.0)
    # 40 bps per side: 110*0.996 / (100*1.004) - 1
    assert net_return_pct(100.0, 110.0, 40) == pytest.approx((110 * 0.996 / 100.4 - 1) * 100)
    # R is measured against the planned risk (entry 100 -> stop 95 = 5/share).
    assert r_multiple(100.0, 110.0, 100.0, 95.0, 0) == pytest.approx(2.0)
    assert r_multiple(100.0, 110.0, 100.0, 95.0, 40) < 2.0
    # A gap-up fill above the planned entry costs R even if the exit is the same.
    assert r_multiple(102.0, 110.0, 100.0, 95.0, 0) == pytest.approx(1.6)


def test_relative_strength_is_a_cross_sectional_percentile():
    returns = {
        "A": pd.Series([0.10, 0.50], index=["2025-01-02", "2025-01-03"]),
        "B": pd.Series([0.20, 0.10], index=["2025-01-02", "2025-01-03"]),
    }
    rows = pd.DataFrame({"symbol": ["A", "B", "A"], "date": ["2025-01-02", "2025-01-02", "2025-01-03"]})
    out = attach_relative_strength(rows, returns).set_index(["symbol", "date"])["rs"]
    assert out[("B", "2025-01-02")] == 1.0 and out[("A", "2025-01-02")] == 0.5 and out[("A", "2025-01-03")] == 1.0
    # A second ranking within a sub-universe goes in its own column.
    sub = attach_relative_strength(rows, {"A": returns["A"]}, "rs_sub")
    assert list(sub["rs_sub"].iloc[[0, 2]]) == [1.0, 1.0] and pd.isna(sub["rs_sub"].iloc[1])  # B not in sub-universe


def _trades(rows: list[dict]) -> pd.DataFrame:
    base = {"score": 75.0, "spy_above_200": True, "stock_above_200": True, "rs": 0.9, "near_high": 0.95,
            "stop_dist_pct": 5.0, "r_multiple": 1.0, "ret_pct": 5.0, "hold_bars": 3,
            "fill": 100.0, "exit_raw": 105.0, "planned_entry": 100.0, "stop": 95.0}
    return pd.DataFrame([{**base, **r} for r in rows])


def test_policy_mask_and_one_position_per_symbol():
    d = _trades([
        {"symbol": "A", "i": 1, "exit_i": 5, "date": "2025-01-01"},
        {"symbol": "A", "i": 3, "exit_i": 8, "date": "2025-01-03"},   # still in the first trade -> skipped
        {"symbol": "A", "i": 6, "exit_i": 9, "date": "2025-01-06"},   # after exit -> taken
        {"symbol": "B", "i": 2, "exit_i": 4, "date": "2025-01-02", "rs": 0.5},
        {"symbol": "C", "i": 2, "exit_i": 4, "date": "2025-01-02", "rs": float("nan")},
    ])
    assert list(policy_mask(d, 70, True, True, 0.8, 0)) == [True, True, True, False, False]
    assert list(policy_mask(d, 80, False, False, 0, 0)) == [False] * 5
    taken = take_positions(d[policy_mask(d, 70, True, True, 0.8, 0)])
    assert sorted(taken["i"]) == [1, 6]


def test_with_costs_recomputes_returns_and_r():
    d = with_costs(_trades([{"symbol": "A", "date": "2025-01-02"}]), 0)
    assert d["ret_pct"].iloc[0] == pytest.approx(5.0) and d["r_multiple"].iloc[0] == pytest.approx(1.0)


def test_monthly_statistics_and_excess_vs_random():
    months = [f"2025-{m:02d}-10" for m in range(1, 7)]
    policy = _trades([{"symbol": "A", "date": d, "r_multiple": r, "ret_pct": r * 5} for d, r in zip(months, [1.0, 0.5, 1.5, 0.8, 1.2, 0.9])])
    base = _trades([{"symbol": "B", "date": d, "r_multiple": r, "ret_pct": r * 5} for d, r in zip(months, [0.2, 0.1, 0.3, 0.0, 0.4, 0.2])])
    s = summarize(policy)
    assert s["n"] == 6 and s["months"] == 6 and s["win_rate"] == 1.0 and s["t_month"] > 3
    ex = excess_vs_baseline(policy, base)
    assert ex["months"] == 6 and ex["avg_excess_r"] == pytest.approx(np.mean([0.8, 0.4, 1.2, 0.8, 0.8, 0.7]), abs=1e-4)
    assert summarize(policy.iloc[:0]) == {"n": 0}


def test_split_dates_are_chronological():
    s = split_dates(pd.DataFrame({"date": ["2015-01-01", "2025-01-01", "2020-01-01"]}))
    assert "2015-01-01" < s.validation_start < s.oos_start < "2025-01-01"


def _calendar(n: int) -> list[str]:
    return [d.strftime("%Y-%m-%d") for d in pd.bdate_range("2025-01-01", periods=n)]


def test_portfolio_caps_new_buys_and_position_size_and_is_marked_to_market():
    cal = _calendar(40)
    # Four candidates on day 1; each has a 2% stop -> 1% risk would mean 50% of
    # equity, so the per-position cap (25%) binds. Exit at +10% on day 30.
    d = _trades([
        {"symbol": s, "entry_date": cal[1], "exit_date": cal[30], "fill": 100.0, "exit_raw": 110.0,
         "stop_dist_pct": 2.0, "score": score}
        for s, score in (("A", 90), ("B", 80), ("C", 70), ("D", 60))
    ])
    # Mid-trade every held stock closes at 80 on day 10 -> a real drawdown that
    # only mark-to-market accounting can see.
    closes = {s: pd.Series([100.0] * 40, index=cal) for s in "ABCD"}
    for s in "ABCD":
        closes[s].iloc[10] = 80.0
    res = simulate_portfolio(d, "score", cal, PriceBook(closes), cost_bps=0)
    assert res["trades"] == MAX_NEW_PER_DAY == 3
    # 3 x 25% invested, each +10% -> +7.5% total over the period.
    total = (1 + 3 * MAX_POSITION_PCT / 100 * 0.10)
    assert res["cagr_pct"] == pytest.approx((total ** (252 / 40) - 1) * 100, abs=0.05)
    # 75% invested falling 20% -> -15% drawdown, although every trade won.
    assert res["max_drawdown_pct"] == pytest.approx(-15.0, abs=0.1)
    assert res["win_rate"] == 1.0


def test_portfolio_one_position_per_symbol_and_costs():
    cal = _calendar(30)
    d = _trades([
        {"symbol": "A", "entry_date": cal[1], "exit_date": cal[5], "stop_dist_pct": 5.0},
        {"symbol": "A", "entry_date": cal[3], "exit_date": cal[8], "stop_dist_pct": 5.0},  # A already held
        {"symbol": "A", "entry_date": cal[6], "exit_date": cal[9], "stop_dist_pct": 5.0},
    ])
    prices = PriceBook({"A": pd.Series([100.0] * 30, index=cal)})
    free = simulate_portfolio(d, "score", cal, prices, cost_bps=0)
    costly = simulate_portfolio(d, "score", cal, prices, cost_bps=40)
    assert free["trades"] == 2
    assert costly["cagr_pct"] < free["cagr_pct"]


def test_random_rank_uses_the_same_candidates():
    cal = _calendar(30)
    d = _trades([{"symbol": s, "entry_date": cal[1], "exit_date": cal[5], "score": sc, "exit_raw": x}
                 for s, sc, x in (("A", 90, 120.0), ("B", 80, 90.0), ("C", 70, 90.0), ("D", 60, 90.0), ("E", 50, 90.0))])
    prices = PriceBook({s: pd.Series([100.0] * 30, index=cal) for s in "ABCDE"})
    ranked = simulate_portfolio(d, "score", cal, prices, 0)
    randomized = [simulate_portfolio(d, "score", cal, prices, 0, rng=np.random.default_rng(k)) for k in range(20)]
    assert ranked["trades"] == 3 and all(r["trades"] == 3 for r in randomized)
    # The best-score pick is the only winner; random order misses it sometimes.
    assert ranked["cagr_pct"] >= max(r["cagr_pct"] for r in randomized)
    assert min(r["cagr_pct"] for r in randomized) < ranked["cagr_pct"]
