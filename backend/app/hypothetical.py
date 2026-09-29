"""A hypothetical, informational-only SEK tracker: "if you'd put 1000 kr
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
"""
from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd

from app.db import SignalRecord

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


@dataclass
class HypotheticalResult:
    base_sek: float
    max_positions: int
    total_sek: float
    delta_sek: float
    delta_pct: float
    positions: list[PositionOutcome] = field(default_factory=list)
    fx_missing: int = 0


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


def hypothetical_value(records: list[SignalRecord], marks: dict[str, dict | None], fx: pd.DataFrame,
                       base_sek: float = 1000.0, max_positions: int = 8,
                       now: pd.Timestamp | None = None) -> HypotheticalResult:
    """`records`: every rotation SignalRecord ever created (open or
    closed) — a slot's par value is untouched until its own trade resolves,
    so replaying the whole history is equivalent to (and simpler than)
    tracking running slot state day by day."""
    now = now or pd.Timestamp.now(tz="UTC")
    slot = base_sek / max_positions
    positions = [evaluate_position(r, marks.get(r.symbol), fx, now) for r in records]
    delta = sum(slot * p.sek_return_pct / 100 for p in positions if p.sek_return_pct is not None)
    missing = sum(1 for p in positions if p.status != "pending" and p.sek_return_pct is None)
    total = base_sek + delta
    return HypotheticalResult(base_sek, max_positions, round(total, 2), round(delta, 2),
                              round(delta / base_sek * 100, 2) if base_sek else 0.0, positions, missing)


def _fmt_kr(value: float) -> str:
    return f"{value:,.0f}".replace(",", " ")


def format_hypothetical_message(result: HypotheticalResult, since: str) -> str:
    sign = "+" if result.delta_sek >= 0 else ""
    lines = [f"💰 Hypotetiska {_fmt_kr(result.base_sek)} kr (sedan {since}): **{_fmt_kr(result.total_sek)} kr** "
             f"({sign}{_fmt_kr(result.delta_sek)} kr, {sign}{result.delta_pct:.1f}%)"]
    active = [p for p in result.positions if p.status in ("open", "closed")]
    if active:
        parts = []
        for p in active:
            if p.sek_return_pct is None:
                parts.append(f"{p.symbol} (valutakurs saknas)")
            else:
                s = "+" if p.sek_return_pct >= 0 else ""
                mark = "" if p.status == "open" else " (stängd)"
                parts.append(f"{p.symbol} {s}{p.sek_return_pct:.1f}%{mark}")
        lines.append(", ".join(parts))
    pending = [p.symbol for p in result.positions if p.status == "pending"]
    if pending:
        lines.append(f"Väntar på första öppning: {', '.join(pending)}.")
    if result.fx_missing:
        lines.append(f"({result.fx_missing} position(er) saknar valutakurs och räknas inte med ännu.)")
    return "\n".join(lines)
