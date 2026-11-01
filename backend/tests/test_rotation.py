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


def test_max_per_sector_caps_how_many_buys_come_from_the_same_sector():
    # AMD, INTC, MU are all "semis"; JPM is "financials"; AAPL is "megacap_tech"
    # (see app.universe._GROUPS). Highest RS first: AMD, INTC, MU, JPM, AAPL.
    rs = {"AMD": 0.99, "INTC": 0.97, "MU": 0.95, "JPM": 0.9, "AAPL": 0.85}
    above = dict.fromkeys(rs, True)
    capped = RotationParams(max_positions=5, max_new_per_day=5, max_per_sector=2)
    sells, buys = decide([], rs, above, True, capped)
    assert buys == ["AMD", "INTC", "JPM", "AAPL"]   # MU skipped: semis already holds 2 (AMD, INTC)

    # The cap also applies against existing holdings, not just today's buys.
    sells, buys = decide(["AMD", "INTC"], rs, above, True, capped)
    assert buys == ["JPM", "AAPL"]   # MU still skipped, semis already full at 2

    # max_per_sector=0 (default) never filters.
    uncapped = RotationParams(max_positions=5, max_new_per_day=5)
    assert decide([], rs, above, True, uncapped)[1] == ["AMD", "INTC", "MU", "JPM", "AAPL"]


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


MA50 = RotationParams(max_positions=3, max_new_per_day=3, ma50_exit=True)
MA50_EXT = RotationParams(max_positions=3, max_new_per_day=3, ma50_exit=True, ma50_after_extension=0.3)


def test_ma50_exit_sells_below_the_50_day_and_never_on_missing_data():
    rs = {"A": 0.9, "B": 0.9, "C": 0.9}
    above = dict.fromkeys(rs, True)
    sells, _ = decide(["A", "B", "C"], rs, above, True, MA50, above_50={"A": False, "B": True})
    assert [s for s, _ in sells] == ["A"]               # C: 50-day unknown -> kept
    assert "50-dagars" in sells[0][1]
    # Off by default: the same inputs sell nothing.
    assert decide(["A", "B", "C"], rs, above, True, P, above_50={"A": False})[0] == []


def test_ma50_exit_after_extension_needs_the_holding_to_have_run_first():
    rs = {"A": 0.9, "B": 0.9}
    above = dict.fromkeys(rs, True)
    below50 = {"A": False, "B": False}
    sells, _ = decide(["A", "B"], rs, above, True, MA50_EXT, above_50=below50, extended={"A": True, "B": False})
    assert [s for s, _ in sells] == ["A"] and "30% över" in sells[0][1]


def test_ma50_exit_only_buys_above_the_50_day():
    rs = {"X": 0.99, "Y": 0.95, "Z": 0.9}
    above = dict.fromkeys(rs, True)
    _, buys = decide([], rs, above, True, MA50, above_50={"X": False, "Y": True})
    assert buys == ["Y"]                                 # X below its 50-day, Z unknown
    assert decide([], rs, above, True, RotationParams(max_positions=3, max_new_per_day=3))[1] == ["X", "Y", "Z"]


def test_ma50_variants_are_named_for_the_evidence_lookup():
    assert MA50.name.endswith("sell below 50d")
    assert MA50_EXT.name.endswith("sell below 50d after +30% over 200d")


def test_simulation_ma50_exit_tracks_extension_since_the_fill():
    # A bought at day 1's open; closes run to +40 % over the 200-day (ext 0.4)
    # on day 2, then it closes below its 50-day on day 3 -> sold at day 4's open.
    closes = {"A": [100, 100, 140, 120, 120, 120]}
    rs = {"A": [0.9] * 6}
    panel = _panel(closes, rs)
    panel.above_50 = np.array([[True], [True], [True], [False], [False], [False]])
    panel.ext_200 = np.array([[0.0], [0.0], [0.4], [0.2], [0.2], [0.2]])
    params = RotationParams(max_positions=1, ma50_exit=True, ma50_after_extension=0.3)
    sim = _simulate_from_zero(panel, params, 0)
    assert len(sim["trades"]) == 1 and sim["trades"][0]["exit"] == "d004"
    assert "50-dagars" in sim["trades"][0]["reason"]

    # Never extended by 30 % -> the 50-day exit doesn't apply, the stock is held.
    panel.ext_200 = np.full((6, 1), 0.2)
    assert _simulate_from_zero(panel, params, 0)["trades"] == []


def test_live_ma50_features_match_the_research_panel():
    from app.live_rotation import market_features
    from app.rotation import build_panel

    n = 330
    dates = pd.bdate_range("2024-01-01", periods=n)
    close_time = (dates.tz_localize("America/New_York") + pd.Timedelta(hours=16)).tz_convert("UTC")
    rng = np.random.default_rng(7)
    frames, research = {}, {}
    for k, s in enumerate(["SPY", "A", "B", "C"]):
        c = 100 * np.exp(np.cumsum(rng.normal(0.001 * k, 0.02, n)))
        frames[s] = pd.DataFrame({"open": c, "high": c, "low": c, "close": c, "volume": 1.0, "close_time": close_time})
        research[s] = pd.DataFrame({"open": c, "low": c, "close": c}, index=dates.strftime("%Y-%m-%d"))

    class Client:
        def get_klines(self, symbol, interval, limit=500):
            return frames[symbol].tail(limit)

    symbols = ["A", "B", "C"]
    panel = build_panel(research, research["SPY"], symbols)
    decided = close_time[n - 40].isoformat()     # held since 40 sessions ago
    f = market_features(Client(), symbols, frames["SPY"], "6m", {"B": decided})
    assert f.above_50 == {s: bool(panel.above_50[-1, j]) for j, s in enumerate(panel.symbols)}
    j = panel.symbols.index("B")
    assert f.max_ext_200 == {"B": pytest.approx(float(np.nanmax(panel.ext_200[n - 39:, j])))}


def test_policy_reads_the_ma50_variant_from_env(monkeypatch):
    from app.policy import active_rotation_params

    monkeypatch.setenv("ROTATION_MA50_EXIT", "true")
    monkeypatch.setenv("ROTATION_MA50_AFTER_EXTENSION", "0.3")
    assert active_rotation_params().name == "top8, in RS>=0.8, out RS<0.5, sell below 50d after +30% over 200d"
