"""Momentum-rotation rules and simulation on SYNTHETIC inputs only (no
network). Verifies the decision rules and the simulation's bookkeeping,
not real performance."""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from app.rotation import Panel, RotationParams, decide, equal_weight_benchmark, simulate

P = RotationParams(max_positions=3, entry_rs=0.8, exit_rs=0.5, max_new_per_day=2)


def test_sell_reasons_and_missing_data_keeps_the_position():
    rs = {"A": 0.9, "B": 0.3, "C": 0.95}
    above = {"A": True, "B": True, "C": False}
    sells, buys = decide(["A", "B", "C", "D"], rs, above, True, P)
    reasons = dict(sells)
    assert set(reasons) == {"B", "C"}  # D has no data today -> kept, never sold on a guess
    assert "relativ styrka" in reasons["B"] and "200" in reasons["C"]


def test_buys_strongest_eligible_into_free_slots_only_in_bull_market():
    rs = {"H": 0.9, "X": 0.99, "Y": 0.85, "Z": 0.97, "W": 0.7}
    above = {"H": True, "X": True, "Y": True, "Z": False, "W": True}
    sells, buys = decide(["H"], rs, above, True, P)
    assert sells == [] and buys == ["X", "Y"]  # Z below its 200d, W not strong enough; 2 free slots
    assert decide(["H"], rs, above, False, P)[1] == []  # no new buys while SPY < 200d
    regime = RotationParams(max_positions=3, regime_exit=True)
    assert [s for s, _ in decide(["H"], rs, above, False, regime)[0]] == ["H"]


def test_max_new_per_day_and_random_order_uses_same_candidates():
    rs = {s: 0.8 + i / 100 for i, s in enumerate("ABCDEFG")}
    above = dict.fromkeys(rs, True)
    wide = RotationParams(max_positions=10, max_new_per_day=3)
    assert decide([], rs, above, True, wide)[1] == ["G", "F", "E"]
    shuffled = decide([], rs, above, True, wide, rng=np.random.default_rng(1))[1]
    assert len(shuffled) == 3 and set(shuffled) <= set(rs)


def _panel(closes: dict[str, list[float]], rs: dict[str, list[float]], opens=None) -> Panel:
    n = len(next(iter(closes.values())))
    syms = list(closes)
    close = np.array([closes[s] for s in syms], float).T
    open_ = np.array([(opens or closes)[s] for s in syms], float).T
    return Panel(dates=[f"d{i:03d}" for i in range(n)], symbols=syms, open=open_, low=np.minimum(open_, close), close=close,
                 rs=np.array([rs[s] for s in syms], float).T, above_200=np.ones((n, len(syms)), bool),
                 has_bar=np.ones((n, len(syms)), bool), spy_above_200=np.ones(n, bool))


def test_simulation_fills_next_open_and_charges_costs():
    # A is the leader from day 0; bought at day 1's open (110), sold after RS drops on day 3 -> day 4 open (132).
    closes = {"A": [100, 120, 125, 130, 140, 140], "B": [50] * 6}
    opens = {"A": [100, 110, 121, 126, 132, 140], "B": [50] * 6}
    rs = {"A": [0.9, 0.9, 0.9, 0.1, 0.1, 0.1], "B": [0.5] * 6}
    panel = _panel(closes, rs, opens)
    sim = _simulate_from_zero(panel, RotationParams(max_positions=1, exit_rs=0.5), cost_bps=0)
    assert [t["symbol"] for t in sim["trades"]] == ["A"]
    assert sim["trades"][0]["ret_pct"] == pytest.approx((132 / 110 - 1) * 100)
    assert sim["curve"][-1] == pytest.approx(132 / 110)
    costly = _simulate_from_zero(panel, RotationParams(max_positions=1, exit_rs=0.5), cost_bps=40)
    assert costly["curve"][-1] < sim["curve"][-1]


def _simulate_from_zero(panel, params, cost_bps):
    # The production warm-up (6-month RS + 200-day average) is skipped for this tiny panel.
    import app.rotation as rotation

    original = rotation.RS_LOOKBACK
    try:
        rotation.RS_LOOKBACK = -200
        return simulate(panel, params, cost_bps)
    finally:
        rotation.RS_LOOKBACK = original


def test_protective_stop_fills_at_gap_open():
    closes = {"A": [100, 100, 100, 70, 70]}
    opens = {"A": [100, 100, 100, 75, 70]}
    rs = {"A": [0.9] * 5}
    sim = _simulate_from_zero(_panel(closes, rs, opens), RotationParams(max_positions=1, stop_pct=0.2), 0)
    assert sim["trades"][0]["reason"] == "stop" and sim["trades"][0]["ret_pct"] == pytest.approx(-25.0)


def test_equal_weight_benchmark():
    panel = _panel({"A": [100, 110, 121], "B": [100, 90, 81]}, {"A": [0.5] * 3, "B": [0.5] * 3})
    assert list(equal_weight_benchmark(panel, 0)) == pytest.approx([1.0, 1.0, 1.0])


def test_momentum_score_definitions():
    from app.rotation import momentum_score

    close = pd.DataFrame({"A": np.arange(1.0, 301.0)})
    last = len(close) - 1
    assert momentum_score(close, "6m").iloc[-1, 0] == pytest.approx(close.A[last] / close.A[last - 126] - 1)
    assert momentum_score(close, "12-1").iloc[-1, 0] == pytest.approx(close.A[last - 21] / close.A[last - 252] - 1)
    vol = close.A.pct_change().iloc[-126:].std() * np.sqrt(252)
    assert momentum_score(close, "6m_vol").iloc[-1, 0] == pytest.approx((close.A[last] / close.A[last - 126] - 1) / vol)


def test_live_features_rank_exactly_like_the_research_panel():
    """The live bot must rank stocks the way the backtest did, for every variant."""
    from app.live_rotation import market_features
    from app.rotation import MOMENTUM_KINDS, build_panel

    n = 330
    dates = pd.bdate_range("2024-01-01", periods=n)
    close_time = (dates.tz_localize("America/New_York") + pd.Timedelta(hours=16)).tz_convert("UTC")
    rng = np.random.default_rng(3)
    frames, research = {}, {}
    for k, s in enumerate(["SPY", "A", "B", "C", "D", "E"]):
        c = 100 * np.exp(np.cumsum(rng.normal(0.0005 * k, 0.02, n)))
        frames[s] = pd.DataFrame({"open": c, "high": c, "low": c, "close": c, "volume": 1.0, "close_time": close_time})
        research[s] = pd.DataFrame({"open": c, "low": c, "close": c}, index=dates.strftime("%Y-%m-%d"))

    class Client:
        def get_klines(self, symbol, interval, limit=500):
            return frames[symbol].tail(limit)

    symbols = ["A", "B", "C", "D", "E"]
    panel = build_panel(research, research["SPY"], symbols)
    for kind in MOMENTUM_KINDS:
        live = market_features(Client(), symbols, frames["SPY"], kind).rs
        expected = {s: panel.rs_by[kind][-1, j] for j, s in enumerate(panel.symbols)}
        assert live == pytest.approx(expected), kind


def test_monthly_rebalance_only_decides_on_a_months_first_session():
    from app.live_rotation import is_rebalance_session

    monthly = RotationParams(rebalance="monthly")
    assert is_rebalance_session(monthly, "2026-10-01", "2026-09-30")
    assert not is_rebalance_session(monthly, "2026-10-02", "2026-10-01")
    assert is_rebalance_session(monthly, "2026-10-05", "2026-09-29")  # the 1st's run failed -> next run rebalances
    assert is_rebalance_session(RotationParams(), "2026-10-02", "2026-10-01")

    # Simulation: A is the leader all along, but it can only be bought after
    # the first session of a new month.
    closes = {"A": [100.0] * 6, "B": [50.0] * 6}
    rs = {"A": [0.9] * 6, "B": [0.5] * 6}
    panel = _panel(closes, rs)
    panel.dates = ["2026-09-28", "2026-09-29", "2026-09-30", "2026-10-01", "2026-10-02", "2026-10-05"]
    sim = _simulate_from_zero(panel, RotationParams(max_positions=1, rebalance="monthly", max_new_per_day=1), 0)
    assert sim["exposure"][:4].max() == 0 and sim["exposure"][4] > 0   # decided at 10-01's close, filled 10-02
