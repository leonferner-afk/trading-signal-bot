import numpy as np
import pandas as pd

from app.bot_research import SYMBOLS, evaluate, report, simulate, stats, trend


def _market(n=900, seed=1):
    rng = np.random.default_rng(seed)
    idx = pd.bdate_range("2018-01-01", periods=n)
    closes = pd.DataFrame({s: 100 * np.cumprod(1 + rng.normal(0.0003, 0.01, n)) for s in SYMBOLS}, index=idx)
    closes["BIL"] = 100 * np.cumprod(np.full(n, 1.0001))
    return closes.shift(1).fillna(closes.iloc[0]), closes        # open = previous close


def test_buy_and_hold_tracks_the_asset_after_the_entry_fee():
    opens, closes = _market()
    res = simulate("x", opens, closes, lambda c: "SPY", fee_bps=10)
    assert res.switches == 1
    expected = closes["SPY"].iloc[-1] / opens["SPY"].iloc[1] * (1 - 0.001)
    assert abs(res.equity.iloc[-1] - expected) < 1e-9
    assert res.equity.iloc[0] == 1.0                              # cash until the first open after the decision


def test_trend_filter_moves_to_bills_below_the_average_and_trades_next_open():
    idx = pd.bdate_range("2020-01-01", periods=320)
    up = np.linspace(100, 200, 220)
    down = np.linspace(200, 80, 100)
    spy = np.concatenate([up, down])
    closes = pd.DataFrame({"SPY": spy, "BIL": np.full(320, 100.0)}, index=idx)
    res = simulate("t", closes, closes, trend("SPY", window=200), fee_bps=0)
    assert res.switches >= 2                                       # in to SPY, later out to bills
    assert res.equity.iloc[-1] > spy[-1] / spy[1]                  # stepped aside for part of the fall


def test_stats_and_report_run_end_to_end():
    opens, closes = _market()
    s = stats(pd.Series([1.0, 1.1, 0.99, 1.2], index=pd.bdate_range("2020-01-01", periods=4)))
    assert round(s["max_dd"], 1) == -10.0
    res = evaluate(opens, closes)
    text = report(res)
    assert "S&P 500 + trendfilter" in text and "Vinnare enligt kraven" in text and res["table"][0]["qualifies"] is None
