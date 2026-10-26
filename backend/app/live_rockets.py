"""Earnings rockets, live — on paper, and with real money only inside an
explicitly configured high-risk "lekpott" (ROCKET_POT_PCT).

Exactly the research rule (app.rockets, variant PAPER_PARAMS): a company
beat analysts' EPS estimate by a wide margin, the stock rose sharply from
the close before the report to the close of the second session after it,
confirmed by heavy volume, in a stock that was already a relative-strength
leader (same 6-month percentile app.rotation ranks by). The position is
bought at the next open and sold at the open after a close 25% below its
highest close, or after 60 sessions. Every month of this is data the
backtest never saw.

This is the strictest variant research has tested: better win rate,
average trade and drawdown than the looser variants it replaced, but it
still hasn't cleared every pre-registered gate (the edge over random entries
in the same stocks isn't statistically significant). By default it stays
paper-only. The owner chose (2026-10-26) to run a 20% lekpott on it anyway,
sized exactly like the research portfolio and paused at -30%; every pot
message says plainly that the rule is unproven.
"""
from __future__ import annotations

import json
import logging
import math
from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from app.data.stock_client import DataUnavailable, StockClient
from app.journal import repository as journal
from app.risk.position_sizing import whole_shares
from app.rockets import (EARNINGS_MAX_HOLD, EARNINGS_TRAIL, MAX_NEW_PER_DAY, MAX_OPEN, WEIGHT, EarningsParams,
                         eligible, event_features)
from app.rotation import RS_LOOKBACK
from app.scanner.scanner import _drop_unclosed_bar

logger = logging.getLogger("tradingbot.rockets")

PAPER_PARAMS = EarningsParams(min_surprise_pct=20.0, min_reaction=0.10, min_volume_ratio=2.0, min_rs=0.8)


def latest_surprise(symbol: str, before: pd.Timestamp, not_before: pd.Timestamp) -> tuple[float, pd.Timestamp] | None:
    """EPS surprise (%) of a report announced in [not_before, before), from
    Yahoo. None if there's no such report or no surprise figure yet."""
    import yfinance as yf

    try:
        df = yf.Ticker(symbol).get_earnings_dates(limit=8)
    except Exception as exc:  # yfinance raises many types
        logger.warning("earnings lookup failed for %s: %s", symbol, exc)
        return None
    if df is None or df.empty:
        return None
    col = next((c for c in df.columns if "Surprise" in c), None)
    if col is None:
        return None
    for ts, value in df[col].items():
        ts = pd.Timestamp(ts)
        ts = ts.tz_localize("America/New_York") if ts.tzinfo is None else ts
        if not_before <= ts < before and value is not None and math.isfinite(float(value)):
            return float(value), ts
    return None


@dataclass
class RocketDay:
    new: list[dict] = field(default_factory=list)
    checked: int = 0
    candidates: int = 0
    no_report: list[str] = field(default_factory=list)


def find_rockets(client: StockClient, universe: list[str], session_close: pd.Timestamp,
                 params: EarningsParams = PAPER_PARAMS, surprise_lookup=latest_surprise) -> RocketDay:
    """Price + volume + relative-strength filter on every stock first
    (cheap, no network beyond the price data already fetched), the earnings
    lookup only for the few survivors. Signal session d1 = today's session;
    the report must fall between the close of d1-2 and the close of d1-1
    (so d1-1 is the first session to react), exactly as in the research.

    Relative strength is a cross-sectional percentile computed over the
    whole universe checked today (app.rotation's own 6-month definition),
    so it means the same thing live as it did in the backtest. A stock
    without 6+ months of history has unknown RS and is never guessed at."""
    day = RocketDay()
    open_symbols = {r.symbol for r in journal.get_open_signals() if r.strategy == journal.ROCKET_PAPER}
    candidates: dict[str, dict] = {}
    ret_6m: dict[str, float] = {}
    for symbol in universe:
        try:
            df = _drop_unclosed_bar(client.get_klines(symbol, "1d", limit=400), 0)
        except DataUnavailable:
            continue
        if len(df) < 25 or df["close_time"].iloc[-1] != session_close:
            continue
        day.checked += 1
        closes = df["close"].to_numpy(float)
        if len(df) > RS_LOOKBACK:
            ret_6m[symbol] = float(closes[-1] / closes[-1 - RS_LOOKBACK] - 1)
        reaction = closes[-1] / closes[-3] - 1
        if reaction < params.min_reaction or not bool(eligible(event_features(df)).iloc[-1]):
            continue
        if params.min_volume_ratio > 0:
            vol_ratio = event_features(df)["volume_ratio"].to_numpy(float)
            best_vol = np.nanmax(vol_ratio[-2:])
            if not (np.isfinite(best_vol) and best_vol >= params.min_volume_ratio):
                continue
        candidates[symbol] = {"reaction": float(reaction), "last_close": float(closes[-1]), "close_time": df["close_time"]}

    rs = pd.Series(ret_6m, dtype=float).rank(pct=True) if ret_6m else pd.Series(dtype=float)
    for symbol, c in candidates.items():
        if params.min_rs > 0:
            rs_val = rs.get(symbol)
            if rs_val is None or rs_val < params.min_rs:
                continue
        day.candidates += 1
        ct = c["close_time"]
        found = surprise_lookup(symbol, before=ct.iloc[-2], not_before=ct.iloc[-3])
        if found is None:
            day.no_report.append(symbol)
            continue
        surprise, announced = found
        if surprise <= params.min_surprise_pct or symbol in open_symbols:
            continue
        day.new.append({"symbol": symbol, "reaction": c["reaction"], "surprise_pct": surprise,
                        "announced": announced.isoformat(), "last_close": c["last_close"],
                        "timestamp": session_close.isoformat()})
    day.new.sort(key=lambda r: r["surprise_pct"], reverse=True)
    return day


# --------------------------------------------------------------------------
# Lekpott: the same rule with real money, sized exactly like the research
# portfolio (WEIGHT of the pot per rocket, at most MAX_OPEN open and
# MAX_NEW_PER_DAY new). The user chose this knowing the rule is unproven.
# --------------------------------------------------------------------------


@dataclass
class RocketPot:
    capital: float              # 0 = no pot, rockets are paper-only
    return_pct: float = 0.0     # pot result so far, % of the pot (closed banked, open marked)
    open_count: int = 0
    paused: bool = False
    pause_pct: float = 30.0

    @property
    def slot_usd(self) -> float:
        return self.capital * WEIGHT

    @property
    def value_usd(self) -> float:
        return self.capital * (1 + self.return_pct / 100)


def pot_return_pct(records: list, marks: dict) -> float:
    """Each pot rocket is a fixed WEIGHT slot of the pot (no compounding, as
    in the research): closed ones count their realized return, open ones
    their last close vs the fill, not-yet-filled ones nothing."""
    total = 0.0
    for r in records:
        if r.result == "OPEN":
            m = marks.get(r.id) or {}
            if m.get("unrealized_pct") is not None:
                total += WEIGHT * m["unrealized_pct"]
        elif r.return_pct is not None:
            total += WEIGHT * r.return_pct
    return total


def rocket_pot_state(mark) -> RocketPot:
    """`mark(record)` -> current_mark dict. Pauses the pot (sticky) the first
    time its result reaches -pause_pct; it stays paused until resumed on purpose."""
    from app.config import settings
    from app.live_rotation import rocket_pot_capital

    capital = rocket_pot_capital()
    if capital <= 0:
        return RocketPot(0.0)
    records = journal.rocket_pot_records()
    marks = {r.id: mark(r) for r in records if r.result == "OPEN"}
    ret = pot_return_pct(records, marks)
    paused = journal.rocket_pot_paused_at() is not None
    if not paused and ret <= -settings.rocket_pot_pause_pct:
        journal.set_rocket_pot_paused(pd.Timestamp.now(tz="UTC").isoformat())
        paused = True
    return RocketPot(capital, ret, sum(r.result == "OPEN" for r in records), paused, settings.rocket_pot_pause_pct)


def allocate_pot(new: list[dict], pot: RocketPot) -> None:
    """Sizes today's rockets (already sorted, biggest surprise first) from the
    pot: whole shares of one slot each. Anything that can't be bought stays
    paper, with the reason in r["paper_reason"]."""
    if pot.capital <= 0:
        return
    open_count, added = pot.open_count, 0
    for r in new:
        if pot.paused:
            r["paper_reason"] = f"lekpotten är pausad ({pot.return_pct:+.0f} %, gräns -{pot.pause_pct:g} %)"
        elif open_count >= MAX_OPEN:
            r["paper_reason"] = f"lekpotten har redan {MAX_OPEN} raketer"
        elif added >= MAX_NEW_PER_DAY:
            r["paper_reason"] = f"högst {MAX_NEW_PER_DAY} nya raketer per dag"
        else:
            shares, cost = whole_shares(pot.slot_usd, r["last_close"])
            if not shares:
                r["paper_reason"] = f"en aktie kostar mer än dubbla platsens storlek (${pot.slot_usd:,.0f})"
                continue
            r["pot_shares"], r["pot_usd"] = shares, cost
            open_count += 1
            added += 1


def pot_sell_signal(df: pd.DataFrame, record) -> str | None:
    """Why an open pot rocket must be sold at the next open, judged at the
    last close in `df` — app.rockets.trailing_exit's rule (close 25% below
    the highest close since the fill, or 60 sessions held). None = keep."""
    signal_at = pd.Timestamp(record.timestamp)
    signal_at = signal_at.tz_localize("UTC") if signal_at.tzinfo is None else signal_at
    bars = df[df["close_time"] >= signal_at]
    if len(bars) < 2:
        return None
    opens, closes = bars["open"].to_numpy(float), bars["close"].to_numpy(float)
    peak = max(opens[1], float(np.nanmax(closes[1:])))
    held = len(bars) - 1
    if closes[-1] <= peak * (1 - EARNINGS_TRAIL):
        return f"stängde {(1 - closes[-1] / peak) * 100:.0f} % under sin högsta stängning ({peak:g})"
    if held >= EARNINGS_MAX_HOLD:
        return f"{EARNINGS_MAX_HOLD} handelsdagar har gått"
    return None


def check_pot_sells(client: StockClient, session_close: pd.Timestamp) -> list[tuple]:
    """Open pot rockets whose sell rule triggered at today's close: marked
    (once) and returned as (record, reason, last_close) so the user can sell
    at the next open. Paper rockets need no alert; the simulator closes them."""
    out = []
    for record in journal.rocket_pot_records():
        if record.result != "OPEN" or record.exit_signal_at:
            continue
        try:
            df = _drop_unclosed_bar(client.get_klines(record.symbol, "1d", limit=400), 0)
        except DataUnavailable:
            continue
        if df.empty or df["close_time"].iloc[-1] != session_close:
            continue
        reason = pot_sell_signal(df, record)
        if reason:
            journal.mark_exit_signal(record.id, session_close.isoformat(), reason)
            out.append((record, reason, float(df["close"].iloc[-1])))
    return out


def format_pot_sell(record, reason: str, last_close: float) -> str:
    shares = json.loads(record.features_json or "{}").get("pot_shares")
    return (f"🔴 SÄLJ NU (lekpott) — {record.symbol}" + (f", {shares} st" if shares else "")
            + f": sälj vid öppning. Aktien {reason}. Senaste stängning {last_close:g}.")


def rocket_evidence(evidence: dict | None, params: EarningsParams = PAPER_PARAMS) -> dict | None:
    for v in ((evidence or {}).get("rockets") or {}).get("variants", []):
        if v.get("name") == params.name and v.get("trades", {}).get("n"):
            return {"n": v["trades"]["n"], "avg_ret_pct": v["trades"]["avg_ret_pct"], "win_rate": v["trades"]["win_rate"],
                    "random_avg_pct": v["random_entries"].get("avg_ret_pct"),
                    "t": (v.get("excess_all") or {}).get("t_month"),
                    "cagr_pct": v["portfolio"].get("cagr_pct"), "max_drawdown_pct": v["portfolio"].get("max_drawdown_pct")}
    return None


def _evidence_line(ev: dict | None) -> str | None:
    if not ev:
        return None
    return (f"Backtest ({ev['n']} affärer): snitt {ev['avg_ret_pct']:+.1f}% per affär, {ev['win_rate'] * 100:.0f}% vinnare — "
            f"slumpköp i samma aktier {ev['random_avg_pct']:+.1f}%. Skillnaden är inte statistiskt säkerställd.")


def format_rocket_buy(r: dict, ev: dict | None) -> str:
    report = (f"Rapport: slog analytikernas vinstförväntning med {r['surprise_pct']:+.0f}%, "
              f"aktien {r['reaction'] * 100:+.0f}% på två dagar.")
    exit_rule = (f"stänger {EARNINGS_TRAIL * 100:g}% under sin högsta stängning, eller efter {EARNINGS_MAX_HOLD} handelsdagar")
    if r.get("pot_shares"):
        lines = [
            f"🚀 RAKET (lekpott, hög risk) — KÖP {r['symbol']}",
            report,
            f"Köp vid öppning: {r['pot_shares']} st ≈ ${r['pot_usd']:,.0f} (senaste stängning {r['last_close']:g}).",
            f"Boten säger till när du ska sälja: när aktien {exit_rule}. Flytta aldrig säljgränsen.",
        ]
        if _evidence_line(ev):
            lines.append(_evidence_line(ev))
        lines.append("⚠ Regeln är inte bevisad. Köp bara för lekpottens pengar — de kan försvinna helt.")
        return "\n".join(lines)
    lines = [
        f"🚀 RAKET (papper — köp inte) — {r['symbol']}",
        report,
        f"Boten följer den som om den köptes vid öppning (senaste stängning {r['last_close']:g}) och 'säljer' när den {exit_rule}.",
    ]
    if r.get("paper_reason"):
        lines.append(f"Bara papper idag: {r['paper_reason']}.")
    if _evidence_line(ev):
        lines.append(_evidence_line(ev) + " Därför bara papper.")
    lines.append("Pappersperioden ska visa om fördelen håller på data som testet aldrig sett.")
    return "\n".join(lines)


def format_rocket_close(record, update: dict) -> str:
    how = "stängde 25 % under toppen" if update["result"] == "ROCKET_TRAIL" else f"{EARNINGS_MAX_HOLD} dagar har gått"
    label = "lekpott" if record.tier == journal.ROCKET_POT_TIER else "papper"
    return (f"🚀 RAKET ({label}) avslutad — {record.symbol}: {update['return_pct']:+.1f}% efter avgifter på "
            f"{update.get('holding_bars', '?')} handelsdagar ({how}). Bäst under perioden "
            f"{update.get('max_favorable_excursion_pct', 0):+.0f}%.")


def pot_lines(pot: RocketPot, sells: list[tuple]) -> list[str]:
    if pot.capital <= 0:
        return []
    lines = [f"**Lekpott:** ${pot.capital:,.0f} → ${pot.value_usd:,.0f} ({pot.return_pct:+.1f} %) · "
             f"{pot.open_count}/{MAX_OPEN} raketer · ${pot.slot_usd:,.0f} per raket."]
    if pot.paused:
        lines.append(f"> ⏸ **Lekpotten är pausad** — den nådde gränsen -{pot.pause_pct:g} %. Inga nya lekpottsköp förrän "
                     "vi har utvärderat tillsammans; öppna raketer säljs som vanligt.")
    for record, reason, last_close in sells:
        lines.append(f"- 🔴 **SÄLJ {record.symbol} vid öppning** — aktien {reason} (senast {last_close:g}).")
    return lines


def build_rocket_section(day: RocketDay | None, open_rockets: list[tuple], closed: list[dict], summary: dict,
                         ev: dict | None, pot: RocketPot | None = None, pot_sells: list[tuple] = ()) -> list[str]:
    live = pot is not None and pot.capital > 0
    lines = ["", "## 🚀 Raketer — lekpott (hög risk, regeln är inte bevisad)" if live
             else "## 🚀 Raketer — papperstrading (köp inte)"]
    if live:
        lines += pot_lines(pot, pot_sells)
    if day is not None:
        lines.append(f"Kontrollerade {day.checked} aktier: {day.candidates} steg ≥ {PAPER_PARAMS.min_reaction * 100:g}% på två dagar, "
                     f"{len(day.new)} efter en rapport som slog förväntningarna."
                     + (f" Saknar rapportdata: {', '.join(day.no_report)}." if day.no_report else ""))
        for r in day.new:
            what = (f"**KÖP {r['pot_shares']} st ≈ ${r['pot_usd']:,.0f} vid öppning** (lekpott)" if r.get("pot_shares")
                    else "papper" + (f" ({r['paper_reason']})" if r.get("paper_reason") else ""))
            lines.append(f"- **{r['symbol']}** — ny: rapport {r['surprise_pct']:+.0f}% mot förväntan, aktien "
                         f"{r['reaction'] * 100:+.0f}% på två dagar — {what}.")
    for e in closed:
        lines.append(f"- {e['symbol']} avslutad: {e['return_pct']:+.1f}% på {e.get('holding_bars', '?')} dagar.")
    if open_rockets:
        lines += ["", "| Raket | Typ | 'Köpt' | Senast | Resultat | Dagar |", "|---|---|---|---|---|---|"]
        for record, mark in open_rockets:
            kind = "lekpott" if record.tier == journal.ROCKET_POT_TIER else "papper"
            if record.exit_signal_at:
                kind += ", säljs vid öppning"
            if not mark or mark.get("fill_price") is None:
                lines.append(f"| {record.symbol} | {kind} | nästa öppning | {mark['last_close'] if mark else '?'} | — | 0 |")
            else:
                lines.append(f"| {record.symbol} | {kind} | {mark['fill_price']:g} | {mark['last_close']:g} | "
                             f"{mark['unrealized_pct']:+.1f}% | {mark['sessions_held']} |")
    if summary.get("n"):
        lines.append(f"\nPapper hittills: {summary['n']} avslutade, {summary['win_rate'] * 100:.0f}% vinnare, snitt "
                     f"{summary['avg_ret_pct']:+.1f}% per raket"
                     + (f" — backtest {ev['avg_ret_pct']:+.1f}%, slumpköp {ev['random_avg_pct']:+.1f}%." if ev else "."))
    else:
        lines.append("\nInga avslutade pappersraketer ännu.")
    return lines
