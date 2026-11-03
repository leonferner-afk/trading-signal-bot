"""A hypothetical, informational-only SEK tracker: "if you'd put 10 000 kr
into this exact live rotation strategy on day one, what would it be worth
today?" No real money is involved — this exists purely so a Swedish user
can follow the strategy's real performance in kronor without opening an
account.

It mirrors the live bot's own sizing exactly: every new buy is sized at
1/max_positions of a FIXED capital figure (app.live_rotation.bot_capital),
never of compounding equity (see app/live_rotation.py). The kronor analogue
of that is: each of `max_positions` slots is permanently worth
base_sek/max_positions at par. A slot's value only moves while it holds a
position — mark-to-market if still open, banked once closed — and an
empty or not-yet-filled slot sits at exactly par (0 kr change). Summing
every rotation trade ever taken (open or closed) against that par value
gives today's total, with no separate compounding step to get wrong.

USD/SEK is applied per position, entry-to-now (or entry-to-exit for a
closed trade), so the number reflects what a Swedish investor's kronor
actually did — not just the US-dollar stock move. A position whose FX
rate can't be found is reported, never guessed at (excluded from the
total rather than assumed flat).

Restart (`since`): "a fresh stake put in at this session close, holding
what the bot holds then". Trades that closed by then are left out;
positions already held are counted from their close at `since` (and FX at
`since`) instead of their original fill; later trades count as usual.

Lekpott (`pot_pct`): that share of the stake follows the bot's lekpott
rockets instead of the rotation, one app.rockets.WEIGHT slot per rocket,
same fixed-slot accounting.

Index fund (`index_pct`): that share of the stake sits in an S&P 500 fund
the bot never touches (BOT_SHARE_PCT's remainder), tracked as SPY from the
start close to now in kronor (`index_sek_pct`). The same number gives the
comparison "the whole stake in the index". The lekpott and rotation share
the rest.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd

from app.db import SignalRecord
from app.rockets import WEIGHT as POT_WEIGHT

FX_SYMBOL = "USDSEK=X"


def to_utc(value) -> pd.Timestamp:
    ts = pd.Timestamp(value)
    return ts.tz_localize("UTC") if ts.tzinfo is None else ts.tz_convert("UTC")


def fx_rate_on(fx: pd.DataFrame, timestamp: pd.Timestamp) -> float | None:
    """The latest USD/SEK close at or before `timestamp`; None if the
    history doesn't go back that far (never guessed forward)."""
    if fx is None or fx.empty:
        return None
    before = fx[fx["close_time"] <= timestamp]
    return float(before["close"].iloc[-1]) if not before.empty else None


@dataclass
class PositionOutcome:
    symbol: str
    status: str                       # "pending" | "open" | "closed"
    usd_return_pct: float | None
    fx_entry: float | None
    fx_now: float | None
    sek_return_pct: float | None      # None -> FX unknown, excluded from the total
    kind: str = "rotation"            # "rotation" | "lekpott"
    entry_price: float | None = None  # USD: the fill (or the close at a restart)
    last_price: float | None = None   # USD: the last close, or the exit price once closed
    invested_sek: float | None = None # the position's fixed kronor slot
    sell_signaled: bool = False       # sell decided, fills at the next open
    record_id: int | None = None


@dataclass
class HypotheticalResult:
    base_sek: float
    max_positions: int
    total_sek: float
    delta_sek: float
    delta_pct: float
    positions: list[PositionOutcome] = field(default_factory=list)
    fx_missing: int = 0
    pot_pct: float = 0.0
    index_pct: float = 0.0
    index_sek_pct: float | None = None    # SPY in kronor since the start; None = unknown
    fund_symbol: str = "SPY"              # what the fund part holds
    fund_sek_pct: float | None = None     # the fund part's move in kronor (= index_sek_pct when it is SPY)


FUND_NAMES = {"SPY": "S&P 500-fond", "QQQ": "Nasdaq 100-fond"}


def fund_name(symbol: str) -> str:
    return FUND_NAMES.get(symbol, f"{symbol}-fond")


def evaluate_position(record: SignalRecord, mark: dict | None, fx: pd.DataFrame, now: pd.Timestamp) -> PositionOutcome:
    """`mark` is `current_mark(client, record)` for an OPEN record (None or
    without a fill yet -> "pending": signalled but the market hasn't
    opened again since, so nothing has happened to this slot)."""
    entry_ts = to_utc(record.timestamp)
    if record.result == "OPEN":
        if mark is None or mark.get("fill_price") is None:
            return PositionOutcome(record.symbol, "pending", None, None, None, None,
                                   last_price=(mark or {}).get("last_close"))
        fx_entry, fx_now = fx_rate_on(fx, entry_ts), fx_rate_on(fx, now)
        usd_r, status, entry, last = mark["unrealized_pct"], "open", mark["fill_price"], mark.get("last_close")
    else:
        fx_entry, fx_now = fx_rate_on(fx, entry_ts), fx_rate_on(fx, to_utc(record.closed_at))
        usd_r, status, entry, last = record.return_pct, "closed", record.fill_price, record.exit_price
    if usd_r is None or fx_entry is None or fx_now is None:
        return PositionOutcome(record.symbol, status, usd_r, fx_entry, fx_now, None, entry_price=entry, last_price=last)
    sek_r = ((1 + usd_r / 100) * (fx_now / fx_entry) - 1) * 100
    return PositionOutcome(record.symbol, status, usd_r, fx_entry, fx_now, round(sek_r, 3), entry_price=entry, last_price=last)


def evaluate_rebased(record: SignalRecord, mark: dict | None, fx: pd.DataFrame, now: pd.Timestamp,
                     since: pd.Timestamp, base_close: float | None) -> PositionOutcome:
    """A position already held at the restart: counted from its close at
    `since` (and USD/SEK then) to now, or to its exit if it has since closed."""
    fx_base = fx_rate_on(fx, since)
    if record.result == "OPEN":
        last, fx_now, status = (mark or {}).get("last_close"), fx_rate_on(fx, now), "open"
    else:
        last, fx_now, status = record.exit_price, fx_rate_on(fx, to_utc(record.closed_at)), "closed"
    if not base_close or last is None:
        return PositionOutcome(record.symbol, status, None, fx_base, fx_now, None, entry_price=base_close, last_price=last)
    usd_r = (last / base_close - 1) * 100
    if fx_base is None or fx_now is None:
        return PositionOutcome(record.symbol, status, round(usd_r, 3), fx_base, fx_now, None,
                               entry_price=base_close, last_price=last)
    sek_r = ((1 + usd_r / 100) * (fx_now / fx_base) - 1) * 100
    return PositionOutcome(record.symbol, status, round(usd_r, 3), fx_base, fx_now, round(sek_r, 3),
                           entry_price=base_close, last_price=last)


def hypothetical_value(records: list[SignalRecord], marks: dict[str, dict | None], fx: pd.DataFrame,
                       base_sek: float = 10000.0, max_positions: int = 8,
                       now: pd.Timestamp | None = None, since: pd.Timestamp | None = None,
                       base_closes: dict[str, float] | None = None, pot_records: list[SignalRecord] = (),
                       pot_marks: dict[int, dict | None] | None = None, pot_pct: float = 0.0,
                       index_pct: float = 0.0, index_sek_pct: float | None = None,
                       fund_symbol: str = "SPY", fund_sek_pct: float | None = None) -> HypotheticalResult:
    """`records`: every rotation SignalRecord ever created (open or
    closed) — a slot's par value is untouched until its own trade resolves,
    so replaying the whole history is equivalent to (and simpler than)
    tracking running slot state day by day. `marks` by symbol for open
    rotation records, `pot_marks` by record id for open lekpott rockets.
    `pot_pct` is a share of the managed part (the stake minus `index_pct`).
    The `index_pct` part sits in `fund_symbol` and moves by `fund_sek_pct`
    (default: the S&P 500's `index_sek_pct`, which stays the comparison)."""
    if fund_symbol == "SPY" and fund_sek_pct is None:
        fund_sek_pct = index_sek_pct
    now = now or pd.Timestamp.now(tz="UTC")
    managed = base_sek * (1 - index_pct / 100)
    slot = managed * (1 - pot_pct / 100) / max_positions
    pot_slot = managed * pot_pct / 100 * POT_WEIGHT
    positions = []

    def add(p: PositionOutcome, r: SignalRecord, kind: str) -> None:
        p.kind = kind
        p.invested_sek = round(pot_slot if kind == "lekpott" else slot, 2)
        p.sell_signaled = r.result == "OPEN" and bool(r.exit_signal_at)
        p.record_id = r.id
        positions.append(p)

    for r in records:
        if since is not None and r.result != "OPEN" and r.closed_at is not None and to_utc(r.closed_at) <= since:
            continue
        if since is not None and to_utc(r.timestamp) < since:
            add(evaluate_rebased(r, marks.get(r.symbol), fx, now, since, (base_closes or {}).get(r.symbol)), r, "rotation")
        else:
            add(evaluate_position(r, marks.get(r.symbol), fx, now), r, "rotation")
    for r in pot_records:
        add(evaluate_position(r, (pot_marks or {}).get(r.id), fx, now), r, "lekpott")
    delta = sum((pot_slot if p.kind == "lekpott" else slot) * p.sek_return_pct / 100
                for p in positions if p.sek_return_pct is not None)
    missing = sum(1 for p in positions if p.status != "pending" and p.sek_return_pct is None)
    if index_pct:
        if fund_sek_pct is None:
            missing += 1
        else:
            delta += base_sek * index_pct / 100 * fund_sek_pct / 100
    total = base_sek + delta
    return HypotheticalResult(base_sek, max_positions, round(total, 2), round(delta, 2),
                              round(delta / base_sek * 100, 2) if base_sek else 0.0, positions, missing, pot_pct,
                              index_pct, None if index_sek_pct is None else round(index_sek_pct, 3),
                              fund_symbol, None if fund_sek_pct is None else round(fund_sek_pct, 3))


def _fmt_kr(value: float) -> str:
    return f"{value:,.0f}".replace(",", " ")


def _position_parts(positions: list[PositionOutcome]) -> str:
    parts = []
    for p in positions:
        if p.sek_return_pct is None:
            parts.append(f"{p.symbol} (kurs saknas)")
        else:
            s = "+" if p.sek_return_pct >= 0 else ""
            parts.append(f"{p.symbol} {s}{p.sek_return_pct:.1f}%" + ("" if p.status == "open" else " (stängd)"))
    return ", ".join(parts)


def format_hypothetical_message(result: HypotheticalResult, since: str) -> str:
    sign = "+" if result.delta_sek >= 0 else ""
    lines = [f"💰 Hypotetiska {_fmt_kr(result.base_sek)} kr (sedan {since}): **{_fmt_kr(result.total_sek)} kr** "
             f"({sign}{_fmt_kr(result.delta_sek)} kr, {sign}{result.delta_pct:.1f}%)"]
    rotation = [p for p in result.positions if p.kind == "rotation" and p.status in ("open", "closed")]
    pot = [p for p in result.positions if p.kind == "lekpott" and p.status in ("open", "closed")]
    index_sek = result.base_sek * result.index_pct / 100
    if result.index_pct:
        move = "kurs saknas" if result.fund_sek_pct is None else f"{result.fund_sek_pct:+.1f}%"
        lines.append(f"{fund_name(result.fund_symbol)} {_fmt_kr(index_sek)} kr: {move}")
    managed = result.base_sek - index_sek
    if managed <= 0:
        pass
    elif result.pot_pct or result.index_pct:
        rot_sek = managed * (1 - result.pot_pct / 100)
        lines.append(f"Rotation {_fmt_kr(rot_sek)} kr: " + (_position_parts(rotation) or "inga innehav ännu"))
        if result.pot_pct:
            lines.append(f"Lekpott {_fmt_kr(managed - rot_sek)} kr: " + (_position_parts(pot) or "inga raketer ännu"))
    elif rotation:
        lines.append(_position_parts(rotation))
    if result.index_sek_pct is not None:
        lines.append(f"Jämförelse: hela {_fmt_kr(result.base_sek)} kr i S&P 500 hade varit "
                     f"{_fmt_kr(result.base_sek * (1 + result.index_sek_pct / 100))} kr.")
    pending = [p.symbol for p in result.positions if p.status == "pending"]
    if pending:
        lines.append(f"Väntar på första öppning: {', '.join(pending)}.")
    if result.fx_missing:
        lines.append(f"({result.fx_missing} position(er) saknar kurs eller valutakurs och räknas inte med ännu.)")
    return "\n".join(lines)


def rocket_portfolio_sek(taken: list[SignalRecord], marks: dict[int, dict | None], fx: pd.DataFrame,
                         base_sek: float = 10000.0, now: pd.Timestamp | None = None) -> tuple[float, int]:
    """app.rocket_portfolio in kronor: (value, positions without a rate yet).
    `taken` = app.rocket_portfolio.admitted(...), `marks` by record id."""
    now = now or pd.Timestamp.now(tz="UTC")
    delta, missing = 0.0, 0
    for r in taken:
        p = evaluate_position(r, marks.get(r.id), fx, now)
        if p.status == "pending":
            continue
        if p.sek_return_pct is None:
            missing += 1
            continue
        delta += base_sek * POT_WEIGHT * p.sek_return_pct / 100
    return round(base_sek + delta, 2), missing


def trade_rows(records: list[SignalRecord], kind: str, bars: dict[str, pd.DataFrame], mark_of) -> list[dict]:
    """Every trade as a broker would list it: when it was bought (the first
    session after the signal, at its open) and at what price, and — once
    closed — when it was sold, at what price and with what result (USD,
    after fees). `mark_of(record)` gives the open position's current mark.
    Dates are the session's date; nothing unknown is filled in."""
    rows = []
    for r in records:
        df = bars.get(r.symbol)
        after = df[df["close_time"] > to_utc(r.timestamp)] if df is not None else None
        buy_date = str(after["close_time"].iloc[0])[:10] if after is not None and not after.empty else None
        if r.result == "OPEN":
            m = mark_of(r) or {}
            buy_price = m.get("fill_price")
            status = "open" if buy_price is not None else "pending"
            if status == "pending":
                buy_date = None
            rows.append({"id": r.id, "symbol": r.symbol, "kind": kind, "status": status,
                         "signal_date": r.timestamp[:10], "buy_date": buy_date, "buy_price": buy_price,
                         "last_price": m.get("last_close"), "unrealized_pct": m.get("unrealized_pct"),
                         "sell_signal_date": (r.exit_signal_at or "")[:10] or None, "sell_reason": r.exit_reason,
                         "sell_date": None, "sell_price": None, "return_pct": None})
        else:
            rows.append({"id": r.id, "symbol": r.symbol, "kind": kind, "status": "closed",
                         "signal_date": r.timestamp[:10], "buy_date": buy_date, "buy_price": r.fill_price,
                         "last_price": r.exit_price, "unrealized_pct": None,
                         "sell_signal_date": (r.exit_signal_at or "")[:10] or None, "sell_reason": r.exit_reason,
                         "sell_date": str(r.closed_at)[:10] if r.closed_at else None, "sell_price": r.exit_price,
                         "return_pct": None if r.return_pct is None else round(r.return_pct, 2)})
    return rows


def _kr_signed(value: float) -> str:
    return ("+" if value >= 0 else "−") + _fmt_kr(abs(value)) + " kr"


def _pct_sv(value: float | None) -> str:
    return "–" if value is None else (f"{value:+.1f} %").replace("-", "−").replace(".", ",")


def depot_notice(payload: dict, session: str, previous_session: str | None) -> str:
    """The owner's Telegram message for one trading day, in kronor, from the
    tracker payload (cmd_hypothetical's JSON): orders for the next open, sales
    filled since the previous notice, and the depot's value. Paper only."""
    trades = {t["id"]: t for t in payload.get("trades", [])}
    positions = [p for p in payload.get("positions", []) if (p.get("invested_sek") or 0) > 0]
    lines = [f"📱 Min depå (papper) — handelsdag {session}"]
    events = []
    for p in positions:
        t = trades.get(p.get("id"), {})
        gain = None if p.get("value_sek") is None else p["value_sek"] - p["invested_sek"]
        if p["status"] == "pending":
            events.append(f"🟢 KÖP {p['symbol']} vid nästa öppning · {_fmt_kr(p['invested_sek'])} kr")
        elif p["status"] == "open" and p.get("sell_signaled"):
            now = "" if gain is None else f" · nu {_fmt_kr(p['value_sek'])} kr ({_kr_signed(gain)}, {_pct_sv(p.get('sek_return_pct'))})"
            events.append(f"🔴 SÄLJ {p['symbol']} vid nästa öppning{now}" + (f" — {t['sell_reason']}" if t.get("sell_reason") else ""))
        elif (p["status"] == "closed" and gain is not None and t.get("sell_date")
              and (previous_session is None or t["sell_date"] > previous_session)):
            events.append(f"✅ Sålt {p['symbol']}: {_kr_signed(gain)} ({_pct_sv(p.get('sek_return_pct'))})")
    rockets = payload.get("rockets") or {}
    for r in rockets.get("rows", []):
        gain = None if r.get("value_sek") is None else r["value_sek"] - r["invested_sek"]
        if r["status"] == "pending":
            events.append(f"🚀 RAKET KÖP {r['symbol']} vid nästa öppning · {_fmt_kr(r['invested_sek'])} kr")
        elif r["status"] == "open" and r.get("sell_signaled"):
            events.append(f"🚀 RAKET SÄLJ {r['symbol']} vid nästa öppning"
                          + ("" if gain is None else f" · nu {_kr_signed(gain)} ({_pct_sv(r.get('sek_return_pct'))})"))
        elif (r["status"] == "closed" and gain is not None and r.get("sell_date")
              and (previous_session is None or r["sell_date"] > previous_session)):
            events.append(f"🚀 Raket såld {r['symbol']}: {_kr_signed(gain)} ({_pct_sv(r.get('sek_return_pct'))})")
    lines += events or ["Inga köp eller sälj idag."]
    lines.append(f"Depå: {_fmt_kr(payload['total_sek'])} kr · sedan start {payload.get('since', '')}: "
                 f"{_kr_signed(payload['delta_sek'])} ({_pct_sv(payload.get('delta_pct'))})")
    if rockets.get("value_sek") is not None:
        lines.append(f"Raketkassan (hög risk): {_fmt_kr(rockets['value_sek'])} kr "
                     f"({_kr_signed(rockets['value_sek'] - rockets['base_sek'])})")
    if payload.get("index_sek_pct") is not None:
        lines.append(f"Allt i S&P 500 hade varit {_fmt_kr(payload['base_sek'] * (1 + payload['index_sek_pct'] / 100))} kr.")
    lines.append("Papper — inga riktiga pengar. Ingen vinst är lovad.")
    return "\n".join(lines)


def rocket_rows(taken: list[SignalRecord], marks: dict[int, dict | None], fx: pd.DataFrame, base_sek: float,
                trades: list[dict], now: pd.Timestamp | None = None) -> dict:
    """The rocket portfolio (app.rocket_portfolio, paper) as a kronor account:
    each rocket a fixed slot of base_sek * WEIGHT, with buy/sell dates and
    prices from `trades` (trade_rows of the same records). Same numbers as
    rocket_portfolio_sek."""
    now = now or pd.Timestamp.now(tz="UTC")
    slot = round(base_sek * POT_WEIGHT, 2)
    by_id = {t["id"]: t for t in trades}
    rows = []
    for r in taken:
        p = evaluate_position(r, marks.get(r.id), fx, now)
        value = None if p.sek_return_pct is None else round(slot * (1 + p.sek_return_pct / 100), 2)
        if p.status == "pending":
            value = slot
        rows.append({**by_id.get(r.id, {"id": r.id, "symbol": r.symbol}), "status": p.status, "invested_sek": slot,
                     "value_sek": value, "sek_return_pct": p.sek_return_pct, "entry_price": p.entry_price,
                     "last_price": p.last_price, "sell_signaled": r.result == "OPEN" and bool(r.exit_signal_at)})
    value, _ = rocket_portfolio_sek(taken, marks, fx, base_sek, now)
    return {"base_sek": base_sek, "value_sek": value, "slot_sek": slot, "since": taken[0].timestamp[:10] if taken else None,
            "rows": rows}
