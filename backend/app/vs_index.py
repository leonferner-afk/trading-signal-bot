"""The bot against the index: what the live rotation returned since it
started, next to SPY over exactly the same days, per calendar quarter.

This is the yardstick that matters. A single day or week says nothing
about a momentum strategy (the backtest had whole years at 0 % and -4 %),
so the daily report shows the comparison the owner judges it by: the
rotation vs simply holding SPY, quarter by quarter.

Accounting mirrors the live sizing (app.live_rotation.bot_capital): each of
`max_positions` slots is a fixed 1/max_positions of the rotation capital,
never compounding. A trade adds nothing before its fill (the open after the
buy decision), its mark-to-market at each close while open (last close vs
fill, no sell fee yet), and its realized return after fees from its exit
session on. Empty slots sit in cash at 0 %. SPY is held from the close of
the first buy decision, without costs or dividends beyond the adjusted
closes the data source gives.

Only the ~400 daily bars the bot downloads are available, so after about
1.5 years the comparison starts at the oldest bar both series cover.
"""
from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from app.data.stock_client import DataUnavailable


def to_utc(value) -> pd.Timestamp:
    ts = pd.Timestamp(value)
    return ts.tz_localize("UTC") if ts.tzinfo is None else ts.tz_convert("UTC")


@dataclass(frozen=True)
class Trade:
    symbol: str
    fill_time: pd.Timestamp            # close_time of the fill session
    fill: float
    exit_time: pd.Timestamp | None     # close_time of the exit session (None = open)
    realized_pct: float | None         # after fees, once closed


def trades_from_records(records: list, bars: dict[str, pd.DataFrame]) -> list[Trade]:
    """`bars[symbol]`: daily bars with open/close/close_time. Records whose
    order hasn't filled yet (or never did) are left out."""
    out = []
    for r in records:
        df = bars.get(r.symbol)
        closed = r.result != "OPEN"
        if closed and (r.return_pct is None or r.closed_at is None):
            continue                     # never filled (e.g. skipped gap)
        if df is None or df.empty:
            continue
        after = df[df["close_time"] > to_utc(r.timestamp)]
        if after.empty:
            continue
        fill = float(r.fill_price) if r.fill_price else float(after["open"].iloc[0])
        out.append(Trade(r.symbol, after["close_time"].iloc[0], fill,
                         to_utc(r.closed_at) if closed else None, float(r.return_pct) if closed else None))
    return out


def bot_curve(trades: list[Trade], closes: dict[str, pd.Series], times: pd.DatetimeIndex, max_positions: int) -> pd.Series:
    """Rotation value (1.0 = start capital) at each close in `times`.
    `closes[symbol]`: close indexed by close_time."""
    weight = 1.0 / max_positions
    total = pd.Series(0.0, index=times)
    for t in trades:
        contrib = pd.Series(0.0, index=times)
        held = times >= t.fill_time
        if t.exit_time is not None:
            done = times >= t.exit_time
            contrib[done] = t.realized_pct / 100
            held &= ~done
        if held.any():
            c = closes.get(t.symbol)
            if c is not None and not c.empty:
                marks = c.reindex(c.index.union(times)).ffill().reindex(times)
                contrib[held] = (marks[held] / t.fill - 1).fillna(0.0)
        total += contrib
    return 1.0 + weight * total


def _quarter(ts: pd.Timestamp) -> str:
    return f"{ts.year} K{(ts.month - 1) // 3 + 1}"


@dataclass
class Comparison:
    start: pd.Timestamp
    end: pd.Timestamp
    bot_pct: float
    spy_pct: float
    quarters: list[tuple[str, float, float, str]]   # (label, bot %, spy %, note: "" | "från …" | "pågår")


def compare(trades: list[Trade], closes: dict[str, pd.Series], spy_close: pd.Series, start: pd.Timestamp,
            max_positions: int) -> Comparison | None:
    """`spy_close` indexed by close_time; `start` = the first buy decision's close."""
    spy_close = spy_close.sort_index()
    if (spy_close.index <= start).any():
        spy_close = spy_close[spy_close.index >= spy_close.index[spy_close.index <= start].max()]
    if len(spy_close) < 2:
        return None
    times = pd.DatetimeIndex(spy_close.index)
    bot = bot_curve(trades, closes, times, max_positions)
    spy = spy_close / spy_close.iloc[0]
    labels = [_quarter(t) for t in times]
    ends = [k for k in range(len(labels)) if k == len(labels) - 1 or labels[k + 1] != labels[k]]
    quarters, prev = [], 0
    for k in ends:
        if k == 0:
            continue                     # the start close is the only bar of its quarter
        note = "pågår" if k == len(labels) - 1 else (f"från {times[0]:%Y-%m-%d}" if labels[k] == labels[0] else "")
        quarters.append((labels[k], (bot.iloc[k] / bot.iloc[prev] - 1) * 100, (spy.iloc[k] / spy.iloc[prev] - 1) * 100, note))
        prev = k
    return Comparison(times[0], times[-1], (bot.iloc[-1] - 1) * 100, (spy.iloc[-1] - 1) * 100, quarters)


def build_comparison(records: list, client, spy: pd.DataFrame, max_positions: int) -> Comparison | None:
    if not records or spy is None or spy.empty:
        return None
    bars = {}
    for symbol in {r.symbol for r in records}:
        try:
            bars[symbol] = client.get_klines(symbol, "1d", limit=400)
        except DataUnavailable:
            continue
    trades = trades_from_records(records, bars)
    closes = {s: df.set_index("close_time")["close"].astype(float) for s, df in bars.items() if not df.empty}
    spy_close = spy.set_index("close_time")["close"].astype(float)
    return compare(trades, closes, spy_close, to_utc(records[0].timestamp), max_positions)


def comparison_lines(c: Comparison | None, bot_share_pct: float) -> list[str]:
    lines = ["", "## ⚖️ Mot index (SPY) — måttstocken som räknas"]
    if c is None:
        return lines + ["Ingen jämförelse ännu (inga fyllda affärer eller SPY-data saknas)."]
    diff = c.bot_pct - c.spy_pct
    lines.append(f"Sedan {c.start:%Y-%m-%d}: rotationen **{c.bot_pct:+.1f} %** · SPY **{c.spy_pct:+.1f} %** · "
                 f"skillnad **{diff:+.1f} procentenheter**.")
    share = min(max(bot_share_pct, 0.0), 100.0)
    if share < 100:
        mix = share / 100 * c.bot_pct + (1 - share / 100) * c.spy_pct
        lines.append(f"Med fördelningen {share:g} % bot / {100 - share:g} % S&P 500-fond: **{mix:+.1f} %** under samma tid.")
    if c.quarters:
        lines += ["", "| Kvartal | Rotationen | SPY | Skillnad |", "|---|---|---|---|"]
        for label, b, s, note in c.quarters:
            lines.append(f"| {label}{f' ({note})' if note else ''} | {b:+.1f} % | {s:+.1f} % | {b - s:+.1f} |")
    lines.append("\nBedöm boten över 1–2 år mot SPY, inte på enskilda dagar eller veckor. Öppna innehav räknas till "
                 "senaste stängning (utan säljavgift), tomma platser som kontanter.")
    return lines
