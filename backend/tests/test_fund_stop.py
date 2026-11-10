import numpy as np
import pandas as pd

from app.fund_stop import simulate


def _bars(closes, start="2026-01-02"):
    days = pd.bdate_range(start, periods=len(closes))
    ct = (days + pd.Timedelta(hours=16)).tz_localize("America/New_York").tz_convert("UTC")
    closes = np.asarray(closes, float)
    return pd.DataFrame({"open": closes, "close": closes, "close_time": ct})


def _fx(bars, rate=10.0):
    return pd.DataFrame({"close_time": bars["close_time"], "close": rate})


def test_no_stop_while_above_the_trail_value_follows_the_fund():
    b = _bars(np.linspace(100, 120, 30))
    r = simulate(b, _fx(b), b["close_time"].iloc[0], 10000.0, trail=0.15, fee_bps=0)
    assert r.holding and r.pending is None and not r.events
    assert abs(r.value_sek - 12000.0) < 1e-6 and abs(r.stop_price - 120 * 0.85) < 1e-9


def test_stop_signals_on_the_close_and_sells_at_the_next_open():
    closes = [100, 110, 120, 110, 101, 100, 99, 98]          # 101 <= 120 * 0.85 = 102 -> signal at index 4
    b = _bars(closes)
    r = simulate(b, _fx(b), b["close_time"].iloc[0], 10000.0, trail=0.15, fee_bps=0)
    assert [e["type"] for e in r.events] == ["sell_signal", "sell"]
    assert not r.holding and abs(r.value_sek - 10000.0) < 1e-6   # sold at the next open (100) = start value
    # Signal on the very last close only -> pending, not yet sold.
    r2 = simulate(b.iloc[:5], _fx(b), b["close_time"].iloc[0], 10000.0, trail=0.15, fee_bps=0)
    assert r2.holding and r2.pending == "sell"


def test_reenters_after_a_month_end_close_above_the_200_day_average():
    closes = list(np.linspace(50, 150, 260)) + [127] + list(np.linspace(128, 170, 60))   # dip, then new uptrend
    b = _bars(closes, start="2025-01-01")
    start = b["close_time"].iloc[250]
    r = simulate(b, _fx(b), start, 10000.0, trail=0.15, fee_bps=0)
    kinds = [e["type"] for e in r.events]
    assert kinds[:2] == ["sell_signal", "sell"] and "buy" in kinds and r.holding
