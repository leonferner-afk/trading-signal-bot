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


def test_restart_counts_held_positions_from_the_restart_close_and_drops_older_trades():
    since = to_utc("2026-10-26T20:00:00Z")
    fx = _fx([("2026-09-01", 9.50), ("2026-10-26", 9.40), ("2026-10-28", 9.40)])
    old_closed = _record("LRCX", "2026-09-26T20:00:00Z", result="ROTATION_EXIT", return_pct=-16.0,
                         closed_at=dt.datetime(2026, 10, 16, 13, 30))                 # closed before the restart: ignored
    held = _record("AMD", "2026-09-26T20:00:00Z")                                     # held at restart: from 500 -> 550
    sold_after = _record("HOOD", "2026-10-01T20:00:00Z", result="ROTATION_EXIT", return_pct=-22.0,
                         closed_at=dt.datetime(2026, 10, 27, 13, 30))
    sold_after.exit_price = 90.0                                                      # restart close 100 -> sold at 90
    new = _record("LLY", "2026-10-26T20:00:00Z")                                      # bought after the restart, as usual
    marks = {"AMD": {"fill_price": 624.9, "last_close": 550.0, "unrealized_pct": -12.0},
             "LLY": {"fill_price": 1000.0, "last_close": 1050.0, "unrealized_pct": 5.0}}
    result = hypothetical_value([old_closed, held, sold_after, new], marks, fx, base_sek=10000.0, max_positions=8,
                                now=to_utc("2026-10-28T20:00:00Z"), since=since, base_closes={"AMD": 500.0, "HOOD": 100.0})
    by = {p.symbol: p for p in result.positions}
    assert "LRCX" not in by
    assert by["AMD"].sek_return_pct == pytest.approx(10.0)       # 550/500, FX flat since the restart
    assert by["HOOD"].sek_return_pct == pytest.approx(-10.0)
    assert by["LLY"].sek_return_pct == pytest.approx((1.05 * (9.40 / 9.40) - 1) * 100)
    slot = 10000.0 / 8
    assert result.delta_sek == pytest.approx(slot * (0.10 - 0.10 + 0.05), abs=0.01)


def test_restart_with_lekpott_splits_the_stake_and_sizes_rockets_from_the_pot():
    since = to_utc("2026-10-26T20:00:00Z")
    fx = _fx([("2026-10-26", 9.40), ("2026-10-30", 9.40)])
    rocket = _record("RKT", "2026-10-28T20:00:00Z")
    rocket.id, rocket.strategy, rocket.tier = 7, "rocket_paper", "POT"
    result = hypothetical_value([], {}, fx, base_sek=10000.0, max_positions=8, now=to_utc("2026-10-30T20:00:00Z"),
                                since=since, pot_records=[rocket],
                                pot_marks={7: {"fill_price": 20.0, "last_close": 25.0, "unrealized_pct": 25.0}}, pot_pct=20.0)
    # Pot = 2 000 kr, one rocket = 10 % of the pot = 200 kr, +25 % -> +50 kr.
    assert result.delta_sek == pytest.approx(50.0, abs=0.01)
    msg = format_hypothetical_message(result, since="2026-10-26")
    assert "Hypotetiska 10 000 kr (sedan 2026-10-26): **10 050 kr**" in msg
    assert "Rotation 8 000 kr: inga innehav ännu" in msg and "Lekpott 2 000 kr: RKT +25.0%" in msg


def test_index_share_tracks_spy_in_kronor_and_sizes_rotation_from_the_rest():
    fx = _fx([("2026-09-25", 10.0), ("2026-09-29", 10.0)])
    record = _record("AMD", "2026-09-26T20:00:00Z")
    mark = {"fill_price": 100.0, "last_close": 120.0, "unrealized_pct": 20.0, "sessions_held": 2}
    # 75 % in the index (+4 %), 25 % rotation in 8 slots: one slot of 312.5 kr at +20 %.
    result = hypothetical_value([record], {"AMD": mark}, fx, base_sek=10000, max_positions=8, now=NOW,
                                index_pct=75.0, index_sek_pct=4.0)
    assert result.delta_sek == pytest.approx(7500 * 0.04 + 312.5 * 0.20)
    message = format_hypothetical_message(result, "2026-09-26")
    assert "S&P 500-fond 7 500 kr: +4.0%" in message
    assert "Rotation 2 500 kr: AMD +20.0%" in message
    assert "hela 10 000 kr i S&P 500 hade varit 10 400 kr" in message


def test_unknown_index_move_is_excluded_not_guessed():
    fx = _fx([("2026-09-25", 10.0)])
    result = hypothetical_value([], {}, fx, base_sek=10000, index_pct=75.0, index_sek_pct=None, now=NOW)
    assert result.total_sek == 10000 and result.fx_missing == 1
    assert "kurs saknas" in format_hypothetical_message(result, "2026-09-26")


def test_trade_rows_list_buys_and_sells_like_a_broker():
    from app.hypothetical import trade_rows

    days = pd.bdate_range("2026-10-26", periods=5)
    bars = pd.DataFrame({"close_time": (days.tz_localize("America/New_York") + pd.Timedelta(hours=16)).tz_convert("UTC")})
    closed = _record("NOW", "2026-10-26T20:00:00Z", result="ROTATION_EXIT", return_pct=-31.5,
                     closed_at=dt.datetime(2026, 10, 29, 20, 0))
    closed.fill_price, closed.exit_price, closed.exit_reason = 151.92, 109.13, "aktien stängde under sitt 200-dagars snitt"
    held = _record("LLY", "2026-10-27T20:00:00Z")
    held.exit_signal_at = "2026-10-29T20:00:00+00:00"
    waiting = _record("TMO", "2026-10-30T20:00:00Z")
    marks = {"LLY": {"fill_price": 1273.5, "last_close": 1417.54, "unrealized_pct": 11.3}, "TMO": {"fill_price": None, "last_close": 690.0}}
    rows = {r["symbol"]: r for r in trade_rows([closed, held, waiting], "rotation", {s: bars for s in ("NOW", "LLY", "TMO")},
                                               lambda r: marks.get(r.symbol))}
    assert rows["NOW"]["status"] == "closed"
    assert (rows["NOW"]["buy_date"], rows["NOW"]["buy_price"], rows["NOW"]["sell_date"], rows["NOW"]["sell_price"]) == \
        ("2026-10-27", 151.92, "2026-10-29", 109.13)
    assert rows["NOW"]["return_pct"] == -31.5 and "200-dagars" in rows["NOW"]["sell_reason"]
    assert rows["LLY"]["status"] == "open" and rows["LLY"]["buy_date"] == "2026-10-28" and rows["LLY"]["sell_signal_date"] == "2026-10-29"
    assert rows["TMO"]["status"] == "pending" and rows["TMO"]["buy_date"] is None and rows["TMO"]["buy_price"] is None


def test_positions_carry_prices_and_their_kronor_slot():
    fx = _fx([("2026-09-26", 9.50), ("2026-09-29", 9.50)])
    rec = _record("AMD", "2026-09-26T20:00:00Z")
    rec.id = 3
    result = hypothetical_value([rec], {"AMD": {"fill_price": 100.0, "last_close": 110.0, "unrealized_pct": 10.0}}, fx,
                                base_sek=10000.0, max_positions=8, now=NOW, index_pct=75.0, index_sek_pct=0.0)
    p = result.positions[0]
    assert (p.entry_price, p.last_price, p.invested_sek, p.record_id, p.sell_signaled) == (100.0, 110.0, 312.5, 3, False)


def test_depot_notice_lists_orders_and_new_sales_in_kronor():
    from app.hypothetical import depot_notice

    payload = {
        "base_sek": 10000.0, "total_sek": 10093.75, "delta_sek": 93.75, "delta_pct": 0.94, "since": "2026-11-02",
        "index_sek_pct": 0.5,
        "positions": [
            {"id": 1, "symbol": "AMD", "status": "closed", "invested_sek": 1250.0, "value_sek": 1307.5, "sek_return_pct": 4.6},
            {"id": 3, "symbol": "INTC", "status": "closed", "invested_sek": 1250.0, "value_sek": 1000.0, "sek_return_pct": -20.0},
            {"id": 14, "symbol": "PLTR", "status": "open", "invested_sek": 1250.0, "value_sek": 1210.0,
             "sek_return_pct": -3.2, "sell_signaled": True},
            {"id": 99, "symbol": "AMGN", "status": "pending", "invested_sek": 1307.5, "value_sek": None},
            {"id": 15, "symbol": "TDOC", "status": "open", "invested_sek": 0.0, "value_sek": 0.0, "sell_signaled": True},
        ],
        "trades": [
            {"id": 1, "sell_date": "2026-11-05"}, {"id": 3, "sell_date": "2026-11-03"},
            {"id": 14, "sell_reason": "relativ styrka föll"}, {"id": 99}, {"id": 15},
        ],
    }
    text = depot_notice(payload, "2026-11-05", "2026-11-04")
    assert "🟢 KÖP AMGN vid nästa öppning · 1 308 kr" in text
    assert "🔴 SÄLJ PLTR vid nästa öppning · nu 1 210 kr (−40 kr, −3,2 %) — relativ styrka föll" in text
    assert "✅ Sålt AMD: +58 kr (+4,6 %)" in text
    assert "INTC" not in text and "TDOC" not in text          # sold before the last notice; not in the depot
    assert "Depå: 10 094 kr" in text and "+94 kr (+0,9 %)" in text and "10 050 kr" in text
    quiet = depot_notice({**payload, "positions": []}, "2026-11-06", "2026-11-05")
    assert "Inga köp eller sälj idag." in quiet


def test_fund_part_can_hold_another_index_while_spy_stays_the_comparison():
    from app.hypothetical import format_hypothetical_message, hypothetical_value

    res = hypothetical_value([], {}, None, base_sek=10000.0, index_pct=100.0, index_sek_pct=-1.0,
                             fund_symbol="QQQ", fund_sek_pct=5.0)
    assert res.total_sek == 10500.0 and res.fund_symbol == "QQQ" and res.index_sek_pct == -1.0
    text = format_hypothetical_message(res, "2026-11-02")
    assert "Nasdaq 100-fond 10 000 kr: +5.0%" in text and "Rotation" not in text
    assert "hela 10 000 kr i S&P 500 hade varit 9 900 kr" in text
    # Unknown fund price: the part is reported missing, not guessed.
    assert hypothetical_value([], {}, None, index_pct=100.0, index_sek_pct=1.0, fund_symbol="QQQ").fx_missing == 1
