"""Rocket paper portfolio on SYNTHETIC journal records (no network): slot
limits, replay order and accounting. Says nothing about real performance."""
from __future__ import annotations

import datetime as dt

import pandas as pd
import pytest

from app.db import SignalRecord
from app.hypothetical import rocket_portfolio_sek, to_utc
from app.rocket_portfolio import admitted, return_pct, summary_line


def _rec(i, ts, result="OPEN", ret=None, closed=None):
    return SignalRecord(id=i, symbol=f"S{i}", strategy="rocket_paper", timestamp=ts, result=result, return_pct=ret,
                        closed_at=closed, tier="PAPER")


def test_at_most_three_new_per_day_and_ten_open():
    day1 = [_rec(i, "2026-10-01T20:00:00+00:00") for i in range(5)]           # only 3 fit on day 1
    later = [_rec(10 + i, f"2026-10-{2 + i:02d}T20:00:00+00:00") for i in range(9)]
    taken = admitted(day1 + later)
    assert [r.id for r in taken[:3]] == [0, 1, 2]
    assert len(taken) == 10                                                    # 10 slots, all still open


def test_a_closed_rocket_frees_its_slot_from_its_exit_on():
    first = [_rec(i, f"2026-10-{1 + i // 3:02d}T20:00:00+00:00") for i in range(9)]
    closed = _rec(9, "2026-10-04T20:00:00+00:00", "ROCKET_TRAIL", -25.0, dt.datetime(2026, 10, 6, 20))
    blocked = _rec(20, "2026-10-05T20:00:00+00:00")                            # 10 open -> no room
    freed = _rec(21, "2026-10-07T20:00:00+00:00")                              # after the exit -> fits
    assert [r.id for r in admitted(first + [closed, blocked, freed])][-2:] == [9, 21]


def test_return_is_ten_percent_per_slot_and_unfilled_counts_nothing():
    taken = [_rec(1, "2026-10-01T20:00:00+00:00", "ROCKET_TIME", 30.0, dt.datetime(2026, 10, 20, 20)),
             _rec(2, "2026-10-01T20:00:00+00:00"), _rec(3, "2026-10-01T20:00:00+00:00")]
    marks = {2: {"unrealized_pct": -10.0, "fill_price": 1.0}, 3: {"unrealized_pct": None, "fill_price": None}}
    assert return_pct(taken, marks) == pytest.approx(0.1 * 30 - 0.1 * 10)
    line = summary_line(taken, marks, base=10000, currency="kr")
    assert "10 000 kr → **10 200 kr** (+2.0 %)" in line and "2 öppna" in line and "1 avslutade (1 vinnare)" in line


def test_kronor_value_applies_usd_sek_per_rocket():
    fx = pd.DataFrame({"close_time": [to_utc("2026-10-01"), to_utc("2026-10-20")], "close": [10.0, 11.0]})
    taken = [_rec(1, "2026-10-01T20:00:00+00:00", "ROCKET_TIME", 0.0, dt.datetime(2026, 10, 20, 20))]
    value, missing = rocket_portfolio_sek(taken, {}, fx, 10000, now=pd.Timestamp("2026-10-21T00:00:00Z"))
    assert value == pytest.approx(10000 + 1000 * 0.10) and missing == 0
