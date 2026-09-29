"""The hypothetical SEK tracker on SYNTHETIC inputs only (no network):
per-position FX conversion, par-value accounting for empty/closed/pending
slots, and the formatted message. Says nothing about real performance."""
from __future__ import annotations

import datetime as dt

import pandas as pd
import pytest

from app.db import SignalRecord
from app.hypothetical import (
    evaluate_position,
    fx_rate_on,
    format_hypothetical_message,
    hypothetical_value,
    to_utc,
)

NOW = pd.Timestamp("2026-09-29T12:00:00Z")


def _fx(rows: list[tuple[str, float]]) -> pd.DataFrame:
    return pd.DataFrame({"close_time": [to_utc(d) for d, _ in rows], "close": [r for _, r in rows]})


def _record(symbol: str, timestamp: str, result: str = "OPEN", return_pct: float | None = None,
           closed_at: dt.datetime | None = None) -> SignalRecord:
    return SignalRecord(symbol=symbol, direction="LONG", strategy="rotation", timestamp=timestamp, entry=100.0,
                        target=0.0, stop=0.0, risk_pct=0.0, reward_pct=0.0, rr_ratio=0.0, score=0.0, tier="ROTATION",
                        market_regime="x", market_wide_risk="x", features_json="{}", news_json="{}",
                        historical_probability_json="{}", result=result, return_pct=return_pct, closed_at=closed_at)


def test_open_position_converts_usd_gain_through_fx_move():
    fx = _fx([("2026-09-25", 9.40), ("2026-09-29", 9.60)])   # SEK weakened -> boosts a Swedish holder's return
    record = _record("AMD", "2026-09-26T20:00:00Z")
    mark = {"fill_price": 100.0, "last_close": 110.0, "unrealized_pct": 10.0, "sessions_held": 2}
    outcome = evaluate_position(record, mark, fx, NOW)
    assert outcome.status == "open"
    expected = (1.10 * (9.60 / 9.40) - 1) * 100
    assert outcome.sek_return_pct == pytest.approx(expected, abs=1e-3)
    assert outcome.sek_return_pct > outcome.usd_return_pct  # FX added on top of the USD gain here


def test_closed_position_uses_realized_return_and_exit_date_fx():
    fx = _fx([("2026-09-01", 9.50), ("2026-09-20", 9.30)])
    record = _record("MU", "2026-09-01T20:00:00Z", result="TARGET_HIT", return_pct=8.0,
                     closed_at=dt.datetime(2026, 9, 20, 20, 0))  # naive -> must be treated as UTC
    outcome = evaluate_position(record, None, fx, NOW)
    assert outcome.status == "closed"
    assert outcome.sek_return_pct == pytest.approx((1.08 * (9.30 / 9.50) - 1) * 100, abs=1e-3)


def test_pending_position_has_not_started_yet():
    fx = _fx([("2026-09-29", 9.50)])
    record = _record("HOOD", "2026-09-29T20:00:00Z")
    outcome = evaluate_position(record, {"fill_price": None, "last_close": 116.0}, fx, NOW)
    assert outcome.status == "pending" and outcome.sek_return_pct is None


def test_missing_fx_history_is_excluded_not_guessed():
    fx = _fx([("2026-09-28", 9.50)])   # doesn't go back to the entry date
    record = _record("INTC", "2026-09-01T20:00:00Z")
    mark = {"fill_price": 100.0, "last_close": 105.0, "unrealized_pct": 5.0, "sessions_held": 10}
    outcome = evaluate_position(record, mark, fx, NOW)
    assert outcome.fx_entry is None and outcome.sek_return_pct is None
    assert fx_rate_on(fx, to_utc("2026-08-01")) is None


def test_hypothetical_value_pars_empty_and_pending_slots_and_banks_closed_ones():
    fx = _fx([("2026-09-01", 9.50), ("2026-09-20", 9.50), ("2026-09-26", 9.50), ("2026-09-29", 9.50)])  # flat FX
    records = [
        _record("AMD", "2026-09-26T20:00:00Z"),                                     # open, +10%
        _record("MU", "2026-09-01T20:00:00Z", result="TARGET_HIT", return_pct=20.0,  # closed, +20%, banked
               closed_at=dt.datetime(2026, 9, 20, 20, 0)),
        _record("HOOD", "2026-09-29T20:00:00Z"),                                    # pending, no effect
    ]
    marks = {"AMD": {"fill_price": 100.0, "last_close": 110.0, "unrealized_pct": 10.0, "sessions_held": 2},
             "HOOD": {"fill_price": None, "last_close": 116.0}}
    result = hypothetical_value(records, marks, fx, base_sek=1000.0, max_positions=8, now=NOW)
    slot = 1000.0 / 8
    # 5 never-traded slots stay at par (0), HOOD (pending) stays at par (0):
    # only AMD (+10%) and MU (+20%) move the total.
    assert result.total_sek == pytest.approx(1000.0 + slot * 0.10 + slot * 0.20, abs=0.01)
    assert result.delta_sek == pytest.approx(slot * 0.30, abs=0.01)
    assert result.fx_missing == 0


def test_format_message_is_readable_swedish():
    result = hypothetical_value(
        [_record("AMD", "2026-09-26T20:00:00Z")],
        {"AMD": {"fill_price": 100.0, "last_close": 110.0, "unrealized_pct": 10.0, "sessions_held": 2}},
        _fx([("2026-09-26", 9.50), ("2026-09-29", 9.50)]),
        base_sek=1000.0, max_positions=8, now=NOW,
    )
    msg = format_hypothetical_message(result, since="2026-09-26")
    assert "Hypotetiska 1 000 kr" in msg and "AMD +10.0%" in msg and "sedan 2026-09-26" in msg
