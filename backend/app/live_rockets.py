"""Earnings rockets, live — PAPER ONLY until they prove themselves.

Exactly the research rule (app.rockets, variant PAPER_PARAMS): a company
beat analysts' EPS estimate by a wide margin, the stock rose sharply from
the close before the report to the close of the second session after it,
confirmed by heavy volume, in a stock that was already a relative-strength
leader (same 6-month percentile app.rotation ranks by). The bot then
follows the position as if bought at the next open, with a 25% trailing
stop on closes and at most 60 sessions — without anyone risking money.
Every month of this is data the backtest never saw.

This is the strictest variant research has tested (2026-10-06): better win
rate, average trade and drawdown than the looser variants it replaced, but
it still hasn't cleared every pre-registered gate (the edge over random
entries in the same stocks isn't statistically significant yet, and it
leans on a handful of its best trades) — which is exactly why this stays
paper-only rather than real money.
"""
from __future__ import annotations

import logging
import math
from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from app.data.stock_client import DataUnavailable, StockClient
from app.journal import repository as journal
from app.rockets import EARNINGS_MAX_HOLD, EARNINGS_TRAIL, EarningsParams, eligible, event_features
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


def rocket_evidence(evidence: dict | None, params: EarningsParams = PAPER_PARAMS) -> dict | None:
    for v in ((evidence or {}).get("rockets") or {}).get("variants", []):
        if v.get("name") == params.name and v.get("trades", {}).get("n"):
            return {"n": v["trades"]["n"], "avg_ret_pct": v["trades"]["avg_ret_pct"], "win_rate": v["trades"]["win_rate"],
                    "random_avg_pct": v["random_entries"].get("avg_ret_pct"),
                    "t": (v.get("excess_all") or {}).get("t_month"),
                    "cagr_pct": v["portfolio"].get("cagr_pct"), "max_drawdown_pct": v["portfolio"].get("max_drawdown_pct")}
    return None


def format_rocket_buy(r: dict, ev: dict | None) -> str:
    lines = [
        f"🚀 RAKET (papper — köp inte) — {r['symbol']}",
        f"Rapport: slog analytikernas vinstförväntning med {r['surprise_pct']:+.0f}%, aktien {r['reaction'] * 100:+.0f}% på två dagar.",
        f"Boten följer den som om den köptes vid öppning (senaste stängning {r['last_close']:g}) och 'säljer' när den stänger "
        f"{EARNINGS_TRAIL * 100:g}% under sin högsta nivå, eller efter {EARNINGS_MAX_HOLD} handelsdagar.",
    ]
    if ev:
        lines.append(f"Backtest ({ev['n']} affärer): snitt {ev['avg_ret_pct']:+.1f}% per affär, {ev['win_rate'] * 100:.0f}% vinnare — "
                     f"slumpköp i samma aktier {ev['random_avg_pct']:+.1f}%. Skillnaden är inte statistiskt säkerställd, "
                     "därför bara papper.")
    lines.append("Pappersperioden ska visa om fördelen håller på data som testet aldrig sett.")
    return "\n".join(lines)


def format_rocket_close(record, update: dict) -> str:
    how = "stängde 25 % under toppen" if update["result"] == "ROCKET_TRAIL" else f"{EARNINGS_MAX_HOLD} dagar har gått"
    return (f"🚀 RAKET (papper) avslutad — {record.symbol}: {update['return_pct']:+.1f}% efter avgifter på "
            f"{update.get('holding_bars', '?')} handelsdagar ({how}). Bäst under perioden "
            f"{update.get('max_favorable_excursion_pct', 0):+.0f}%.")


def build_rocket_section(day: RocketDay | None, open_rockets: list[tuple], closed: list[dict], summary: dict,
                         ev: dict | None) -> list[str]:
    lines = ["", "## 🚀 Raketer — papperstrading (köp inte)"]
    if day is not None:
        lines.append(f"Kontrollerade {day.checked} aktier: {day.candidates} steg ≥ {PAPER_PARAMS.min_reaction * 100:g}% på två dagar, "
                     f"{len(day.new)} efter en rapport som slog förväntningarna."
                     + (f" Saknar rapportdata: {', '.join(day.no_report)}." if day.no_report else ""))
        for r in day.new:
            lines.append(f"- **{r['symbol']}** — ny: rapport {r['surprise_pct']:+.0f}% mot förväntan, aktien {r['reaction'] * 100:+.0f}% på två dagar.")
    for e in closed:
        lines.append(f"- {e['symbol']} avslutad: {e['return_pct']:+.1f}% på {e.get('holding_bars', '?')} dagar.")
    if open_rockets:
        lines += ["", "| Raket | 'Köpt' | Senast | Resultat | Dagar |", "|---|---|---|---|---|"]
        for record, mark in open_rockets:
            if not mark or mark.get("fill_price") is None:
                lines.append(f"| {record.symbol} | nästa öppning | {mark['last_close'] if mark else '?'} | — | 0 |")
            else:
                lines.append(f"| {record.symbol} | {mark['fill_price']:g} | {mark['last_close']:g} | {mark['unrealized_pct']:+.1f}% | "
                             f"{mark['sessions_held']} |")
    if summary.get("n"):
        lines.append(f"\nPapper hittills: {summary['n']} avslutade, {summary['win_rate'] * 100:.0f}% vinnare, snitt "
                     f"{summary['avg_ret_pct']:+.1f}% per raket"
                     + (f" — backtest {ev['avg_ret_pct']:+.1f}%, slumpköp {ev['random_avg_pct']:+.1f}%." if ev else "."))
    else:
        lines.append("\nInga avslutade pappersraketer ännu.")
    return lines
