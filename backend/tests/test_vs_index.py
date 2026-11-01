"""Bot-vs-SPY comparison on SYNTHETIC inputs only (no network): slot
accounting, quarter splits and the report lines. Says nothing about real
performance."""
from __future__ import annotations

import datetime as dt

import pandas as pd
import pytest

from app.db import SignalRecord
from app.vs_index import Trade, bot_curve, compare, comparison_lines, trades_from_records


def _times(days: list[str]) -> pd.DatetimeIndex:
    return pd.DatetimeIndex([pd.Timestamp(f"{d}T20:00:00Z") for d in days])


def test_bot_curve_marks_open_trades_and_banks_closed_ones_per_slot():
    times = _times(["2026-09-25", "2026-09-26", "2026-09-29", "2026-09-30"])
    closes = {"A": pd.Series([100.0, 110.0, 120.0, 130.0], index=times)}
    trades = [Trade("A", times[1], 100.0, times[3], -10.0)]     # filled day 1, sold at day 3's open for -10 %
    curve = bot_curve(trades, closes, times, max_positions=2)
    assert list(curve) == pytest.approx([1.0, 1.05, 1.10, 0.95])


def test_compare_splits_by_calendar_quarter_against_spy():
    times = _times(["2026-09-25", "2026-09-30", "2026-10-01", "2026-10-30"])
    spy = pd.Series([100.0, 102.0, 101.0, 105.06], index=times)
    closes = {"A": pd.Series([50.0, 55.0, 55.0, 44.0], index=times)}
    trades = [Trade("A", times[0], 50.0, None, None)]
    c = compare(trades, closes, spy, times[0], max_positions=1)
    assert c.bot_pct == pytest.approx(-12.0) and c.spy_pct == pytest.approx(5.06)
    (q3, b3, s3, n3), (q4, b4, s4, n4) = c.quarters
    assert (q3, n3, q4, n4) == ("2026 K3", "från 2026-09-25", "2026 K4", "pågår")
    assert b3 == pytest.approx(10.0) and s3 == pytest.approx(2.0)
    assert b4 == pytest.approx(44 / 55 * 100 - 100) and s4 == pytest.approx(105.06 / 102 * 100 - 100)


def test_records_become_trades_from_their_fill_bar():
    times = _times(["2026-09-25", "2026-09-26", "2026-09-29"])
    bars = {"A": pd.DataFrame({"open": [10.0, 11.0, 12.0], "close": [10.0, 11.5, 12.5], "close_time": times}),
            "B": pd.DataFrame({"open": [5.0], "close": [5.0], "close_time": times[:1]})}

    def rec(symbol, ts, result="OPEN", ret=None, closed=None, fill=None):
        return SignalRecord(symbol=symbol, timestamp=ts, result=result, return_pct=ret, closed_at=closed, fill_price=fill)

    trades = trades_from_records([
        rec("A", "2026-09-25T20:00:00+00:00"),                                   # open, fills at 11
        rec("A", "2026-09-25T20:00:00+00:00", "ROTATION_EXIT", -5.0, dt.datetime(2026, 9, 29, 20), 11.0),
        rec("B", "2026-09-25T20:00:00+00:00"),                                   # not filled yet
    ], bars)
    assert [(t.fill, t.exit_time is None) for t in trades] == [(11.0, True), (11.0, False)]
    assert trades[1].realized_pct == -5.0


def test_report_lines_show_the_split_and_the_quarter_table():
    times = _times(["2026-09-25", "2026-10-30"])
    c = compare([], {}, pd.Series([100.0, 110.0], index=times), times[0], max_positions=8)
    text = "\n".join(comparison_lines(c, bot_share_pct=25))
    assert "rotationen **+0.0 %** · SPY **+10.0 %**" in text
    assert "25 % bot / 75 % S&P 500-fond: **+7.5 %**" in text
    assert "| 2026 K4 (pågår) | +0.0 % | +10.0 % | -10.0 |" in text
    assert "Ingen jämförelse" in "\n".join(comparison_lines(None, 25))
