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


def evaluate_position(record: SignalRecord, mark: dict | None, fx: pd.DataFrame, now: pd.Timestamp) -> PositionOutcome:
    """`mark` is `current_mark(client, record)` for an OPEN record (None or
    without a fill yet -> "pending": signalled but the market hasn't
    opened again since, so nothing has happened to this slot)."""
    entry_ts = to_utc(record.timestamp)
    if record.result == "OPEN":
        if mark is None or mark.get("fill_price") is None:
            return PositionOutcome(record.symbol, "pending", None, None, None, None)
        fx_entry, fx_now = fx_rate_on(fx, entry_ts), fx_rate_on(fx, now)
        usd_r, status = mark["unrealized_pct"], "open"
    else:
        fx_entry, fx_now = fx_rate_on(fx, entry_ts), fx_rate_on(fx, to_utc(record.closed_at))
        usd_r, status = record.return_pct, "closed"
    if usd_r is None or fx_entry is None or fx_now is None:
        return PositionOutcome(record.symbol, status, usd_r, fx_entry, fx_now, None)
    sek_r = ((1 + usd_r / 100) * (fx_now / fx_entry) - 1) * 100
    return PositionOutcome(record.symbol, status, usd_r, fx_entry, fx_now, round(sek_r, 3))


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
        return PositionOutcome(record.symbol, status, None, fx_base, fx_now, None)
    usd_r = (last / base_close - 1) * 100
    if fx_base is None or fx_now is None:
        return PositionOutcome(record.symbol, status, round(usd_r, 3), fx_base, fx_now, None)
    sek_r = ((1 + usd_r / 100) * (fx_now / fx_base) - 1) * 100
    return PositionOutcome(record.symbol, status, round(usd_r, 3), fx_base, fx_now, round(sek_r, 3))


def hypothetical_value(records: list[SignalRecord], marks: dict[str, dict | None], fx: pd.DataFrame,
                       base_sek: float = 10000.0, max_positions: int = 8,
                       now: pd.Timestamp | None = None, since: pd.Timestamp | None = None,
                       base_closes: dict[str, float] | None = None, pot_records: list[SignalRecord] = (),
                       pot_marks: dict[int, dict | None] | None = None, pot_pct: float = 0.0) -> HypotheticalResult:
    """`records`: every rotation SignalRecord ever created (open or
    closed) — a slot's par value is untouched until its own trade resolves,
    so replaying the whole history is equivalent to (and simpler than)
    tracking running slot state day by day. `marks` by symbol for open
    rotation records, `pot_marks` by record id for open lekpott rockets."""
    now = now or pd.Timestamp.now(tz="UTC")
    slot = base_sek * (1 - pot_pct / 100) / max_positions
    pot_slot = base_sek * pot_pct / 100 * POT_WEIGHT
    positions = []
    for r in records:
        if since is not None and r.result != "OPEN" and r.closed_at is not None and to_utc(r.closed_at) <= since:
            continue
        if since is not None and to_utc(r.timestamp) < since:
            positions.append(evaluate_rebased(r, marks.get(r.symbol), fx, now, since, (base_closes or {}).get(r.symbol)))
        else:
            positions.append(evaluate_position(r, marks.get(r.symbol), fx, now))
    for r in pot_records:
        p = evaluate_position(r, (pot_marks or {}).get(r.id), fx, now)
        p.kind = "lekpott"
        positions.append(p)
    delta = sum((pot_slot if p.kind == "lekpott" else slot) * p.sek_return_pct / 100
                for p in positions if p.sek_return_pct is not None)
    missing = sum(1 for p in positions if p.status != "pending" and p.sek_return_pct is None)
    total = base_sek + delta
    return HypotheticalResult(base_sek, max_positions, round(total, 2), round(delta, 2),
                              round(delta / base_sek * 100, 2) if base_sek else 0.0, positions, missing, pot_pct)


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
    if result.pot_pct:
        rot_sek = result.base_sek * (1 - result.pot_pct / 100)
        lines.append(f"Rotation {_fmt_kr(rot_sek)} kr: " + (_position_parts(rotation) or "inga innehav ännu"))
        lines.append(f"Lekpott {_fmt_kr(result.base_sek - rot_sek)} kr: " + (_position_parts(pot) or "inga raketer ännu"))
    elif rotation:
        lines.append(_position_parts(rotation))
    pending = [p.symbol for p in result.positions if p.status == "pending"]
    if pending:
        lines.append(f"Väntar på första öppning: {', '.join(pending)}.")
    if result.fx_missing:
        lines.append(f"({result.fx_missing} position(er) saknar kurs eller valutakurs och räknas inte med ännu.)")
    return "\n".join(lines)
