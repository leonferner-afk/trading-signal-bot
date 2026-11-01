"""The rocket paper portfolio: "if 10 000 kr had followed every rocket call
the bot made, what would it be worth?" Just for fun, no real money.

Sized exactly like the research's rocket portfolio (app.rockets): each
rocket is a fixed WEIGHT slot of the stake (no compounding), at most
MAX_OPEN open at once and MAX_NEW_PER_DAY new per day, taken in the order
the bot called them (biggest earnings surprise first within a day). Calls
that didn't fit are left out, as they would have been with real money.
Returns use the same fills, trailing stop and time limit as the paper
rockets in the journal.
"""
from __future__ import annotations

import pandas as pd

from app.rockets import MAX_NEW_PER_DAY, MAX_OPEN, WEIGHT


def _utc(value) -> pd.Timestamp:
    ts = pd.Timestamp(value)
    return ts.tz_localize("UTC") if ts.tzinfo is None else ts.tz_convert("UTC")


def admitted(records: list) -> list:
    """The calls the portfolio would have taken, replayed in call order.
    A position frees its slot from its exit session on."""
    taken, per_day = [], {}
    for r in records:
        ts = _utc(r.timestamp)
        open_now = [t for t in taken if t.result == "OPEN" or t.closed_at is None or _utc(t.closed_at) > ts]
        day = ts.strftime("%Y-%m-%d")
        if len(open_now) >= MAX_OPEN or per_day.get(day, 0) >= MAX_NEW_PER_DAY:
            continue
        taken.append(r)
        per_day[day] = per_day.get(day, 0) + 1
    return taken


def return_pct(taken: list, marks: dict) -> float:
    """Portfolio result in % of the stake: closed calls their realized return
    (after fees), open ones last close vs fill, unfilled ones nothing.
    `marks` by record id (app.paper_trading.simulator.current_mark)."""
    total = 0.0
    for r in taken:
        if r.result == "OPEN":
            m = marks.get(r.id) or {}
            if m.get("unrealized_pct") is not None:
                total += WEIGHT * m["unrealized_pct"]
        elif r.return_pct is not None:
            total += WEIGHT * r.return_pct
    return total


def summary_line(records: list, marks: dict, base: float = 10000.0, currency: str = "kr") -> str | None:
    taken = admitted(records)
    if not taken:
        return None
    ret = return_pct(taken, marks)
    open_n = sum(r.result == "OPEN" for r in taken)
    closed = [r for r in taken if r.result != "OPEN" and r.return_pct is not None]
    wins = sum(r.return_pct > 0 for r in closed)
    value = f"{base * (1 + ret / 100):,.0f}".replace(",", " ")
    start = f"{base:,.0f}".replace(",", " ")
    return (f"🚀 Raketportfölj (papper, på kul) sedan {_utc(taken[0].timestamp):%Y-%m-%d}: {start} {currency} → "
            f"**{value} {currency}** ({ret:+.1f} %) · {open_n} öppna · {len(closed)} avslutade"
            + (f" ({wins} vinnare)" if closed else "") + f" · {len(records) - len(taken)} signaler fick inte plats.")
