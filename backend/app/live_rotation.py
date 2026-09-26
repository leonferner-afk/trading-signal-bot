"""The daily run in momentum-rotation mode: the exact rule tested in
app.research (app.rotation.decide), applied to today's close.

Features are computed the way the research panel computes them: 6-month
(126-session) return ranked as a percentile across the whole universe,
close above the 200-day simple average, SPY above its own 200-day average.
A stock without a bar for the latest session gets no features today — a
holding is then kept and it can't be bought (never decided on a guess).
"""
from __future__ import annotations

import datetime as dt
import logging
from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd

from app.data.stock_client import DataUnavailable, StockClient
from app.journal import repository as journal
from app.notify import github_issue, telegram_client
from app.notify.notifier import notify_rotation_buy, notify_rotation_sell
from app.paper_trading.simulator import ROTATION_EXIT, SKIPPED_GAP, current_mark, run_paper_trading_update
from app.risk.position_sizing import PositionSize
from app.rotation import RS_LOOKBACK, RotationParams, decide
from app.runtime_settings import get_effective_settings
from app.scanner.scanner import ANCHOR_SYMBOL, _drop_unclosed_bar

logger = logging.getLogger("tradingbot.rotation")

MIN_POSITION_PCT = 2.0


@dataclass
class Features:
    session_close: pd.Timestamp
    spy_above_200: bool
    rs: dict[str, float]
    above_200: dict[str, bool]
    ret_6m: dict[str, float]
    last_close: dict[str, float]
    skipped: dict[str, str] = field(default_factory=dict)


def _above_200(close: pd.Series) -> bool:
    return bool(len(close) >= 200 and close.iloc[-1] > close.iloc[-200:].mean())


def market_features(client: StockClient, universe: list[str], spy: pd.DataFrame) -> Features:
    spy = _drop_unclosed_bar(spy, 0)
    session_close = spy["close_time"].iloc[-1]
    ret_6m, above, last_close, skipped = {}, {}, {}, {}
    for symbol in universe:
        try:
            df = _drop_unclosed_bar(client.get_klines(symbol, "1d", limit=400), 0)
        except DataUnavailable as exc:
            skipped[symbol] = str(exc)
            continue
        if df.empty or df["close_time"].iloc[-1] != session_close:
            skipped[symbol] = "ingen stängning för senaste handelsdagen"
            continue
        close = df["close"].astype(float)
        last_close[symbol] = float(close.iloc[-1])
        above[symbol] = _above_200(close)
        if len(close) > RS_LOOKBACK:
            ret_6m[symbol] = float(close.iloc[-1] / close.iloc[-1 - RS_LOOKBACK] - 1)
    rs = pd.Series(ret_6m, dtype=float).rank(pct=True).to_dict() if ret_6m else {}
    return Features(session_close, _above_200(spy["close"].astype(float)), rs, above, ret_6m, last_close, skipped)


def rotation_evidence(evidence: dict | None, params: RotationParams) -> dict | None:
    """Backtest numbers for exactly this rule set, from the research universe
    that corresponds to the live one: large caps live <-> the 2015 large-cap
    group (hindsight-free); the full list <-> 'all'."""
    import os

    from app.policy import DEFAULT_ROTATION_UNIVERSE

    name = (os.getenv("ROTATION_UNIVERSE") or DEFAULT_ROTATION_UNIVERSE).strip().lower()
    try:
        r = evidence["universes"]["all" if name == "all" else "largecap_2015"]["rotation"]
    except (KeyError, TypeError):
        return None
    if not r:
        return None
    for c in r["configs"]:
        if c["name"] == params.name and c["full"].get("trades"):
            f = c["full"]
            years = (evidence.get("meta") or {}).get("years", "?")
            return {
                "label": f"backtest {f['years']:g} år på storbolag valda 2015, samma regler",
                "cagr_pct": f["cagr_pct"], "max_drawdown_pct": f["max_drawdown_pct"], "sharpe": f["sharpe"],
                "win_rate": f["win_rate"] or 0.0, "avg_trade_pct": f["avg_trade_pct"] or 0.0, "avg_days": f["avg_days"] or 0.0,
                "spy_cagr_pct": r["spy"]["cagr_pct"], "spy_max_drawdown_pct": r["spy"]["max_drawdown_pct"],
                "oos_cagr_pct": c["oos"].get("cagr_pct"), "spy_oos_cagr_pct": r["spy_oos"].get("cagr_pct"),
            }
    return None


GATE_LABELS = {
    "train_val_sharpe_beats_spy": "slår inte SPY riskjusterat",
    "ranking_beats_random": "rangordningen slår inte slumpvis val",
    "without_best_stock_beats_spy": "vilar på en enda aktie",
    "drawdown_close_to_spy": "för stora nedgångar",
}


def gate_status(evidence: dict | None, params: RotationParams) -> str | None:
    """A warning when the latest research no longer supports the live rule
    (checked weekly against the pre-registered gates), else None."""
    sel = (evidence or {}).get("rotation_selection")
    if not sel:
        return None
    mine = next((g for g in sel.get("gates", []) if g["name"] == params.name), None)
    if mine is None:
        return "⚠ Den senaste forskningen har inte testat exakt de här reglerna."
    if not mine["passes"]:
        failed = ", ".join(GATE_LABELS.get(k, k) for k, ok in mine["checks"].items() if not ok)
        best = sel.get("chosen")
        return (f"⚠ Reglerna klarar inte forskningens förhandsbestämda krav ({failed}). "
                + (f"Forskningens val just nu: {best}." if best else
                   "Ingen testad variant har slagit att bara äga en S&P 500-fond riskjusterat — se signalerna som ett aktivt "
                   "alternativ med ungefär indexlik historik, inte som en bevisad fördel."))
    return None


def equal_weight_size(price: float, portfolio: float, params: RotationParams, free: float) -> PositionSize:
    target = portfolio / params.max_positions
    notional = max(0.0, min(target, free))
    risk = notional * params.stop_pct if params.stop_pct else notional
    return PositionSize(portfolio_size_usd=portfolio, risk_per_trade_pct=round(risk / portfolio * 100, 2) if portfolio else 0.0,
                        risk_amount_usd=round(risk, 2), position_size_usd=round(notional, 2),
                        position_pct_of_portfolio=round(notional / portfolio * 100, 2) if portfolio else 0.0,
                        units=round(notional / price, 8) if price else 0.0)


@dataclass
class RotationDay:
    buys: list[tuple[str, PositionSize]]
    sells: list[tuple[object, str, dict | None]]     # (record, reason, mark)
    closed: list[dict]                              # positions closed since last run (fills known)
    next_up: list[str]
    features: Features | None


def run_rotation_day(client: StockClient, universe: list[str], spy: pd.DataFrame, params: RotationParams,
                     evidence: dict | None, market_wide_risk: str, act: bool) -> RotationDay:
    """`act=False` (no new session / stale data): positions are still
    checked, but no new decisions are made."""
    closed = run_paper_trading_update(client=client)["updated"]
    if not act:
        return RotationDay([], [], closed, [], None)

    live = get_effective_settings()
    features = market_features(client, universe, spy)
    timestamp = features.session_close.isoformat()
    open_records = [r for r in journal.get_open_signals() if r.strategy == journal.ROTATION]
    holding = [r for r in open_records if r.exit_signal_at is None]
    sells, buys = decide([r.symbol for r in holding], features.rs, features.above_200, features.spy_above_200, params)

    by_symbol = {r.symbol: r for r in holding}
    sell_rows = []
    for symbol, reason in sells:
        record = by_symbol[symbol]
        journal.mark_exit_signal(record.id, timestamp, reason)
        mark = current_mark(client, record)
        notify_rotation_sell(record, reason, mark)
        sell_rows.append((record, reason, mark))

    portfolio = live.portfolio_size_usd
    kept = len(holding) - len(sells)
    free = portfolio - kept * portfolio / params.max_positions
    ev = rotation_evidence(evidence, params)
    buy_rows = []
    for symbol in buys:
        price = features.last_close[symbol]
        size = equal_weight_size(price, portfolio, params, free)
        if size.position_size_usd < portfolio * MIN_POSITION_PCT / 100:
            continue
        free -= size.position_size_usd
        info = {"rs": features.rs[symbol], "ret_6m": features.ret_6m[symbol], "last_close": price,
                "universe": len(features.rs)}
        journal.save_rotation_buy(symbol, timestamp, price, price * (1 - params.stop_pct) if params.stop_pct else 0.0,
                                  info, market_wide_risk, ev)
        notify_rotation_buy(symbol, info, size, params, ev, gate_status(evidence, params))
        buy_rows.append((symbol, size))

    # The next strongest eligible names (for the report only).
    bought = {s for s, _ in buy_rows} | {r.symbol for r in holding}
    ranked = sorted((s for s, v in features.rs.items() if v >= params.entry_rs and features.above_200.get(s) and s not in bought),
                    key=lambda s: features.rs[s], reverse=True)
    return RotationDay(buy_rows, sell_rows, closed, ranked[:8], features)


def build_rotation_report(today: str, session: str | None, new_session: bool, params: RotationParams, day: RotationDay,
                          open_positions: list[tuple], performance: dict, evidence: dict | None, universe_size: int) -> str:
    live = get_effective_settings()
    f = day.features
    market = "okänt" if f is None else ("över" if f.spy_above_200 else "under")
    lines = [
        f"# Tradingbot {today}",
        "",
        f"**Marknaden:** SPY {market} sitt 200-dagars snitt"
        + (" — inga nya köp förrän den är över igen" if f is not None and not f.spy_above_200 else ""),
        f"**Strategi:** momentum-rotation — {params.name}",
        f"**Portfölj:** ${live.portfolio_size_usd:,.0f} · {len(open_positions)}/{params.max_positions} innehav · "
        f"senaste handelsdag i datan: {session or 'okänd'}",
        "",
    ] + ([f"> {gate_status(evidence, params)}", ""] if gate_status(evidence, params) else []) + [
        f"## 🟢 KÖP ({len(day.buys)})",
    ]
    if not new_session:
        lines.append("Ingen ny handelsdag sedan förra körningen (helgdag eller omkörning) — inga nya beslut.")
    elif not day.buys:
        lines.append("Inga nya köp idag." + (" Alla platser är fyllda." if len(open_positions) >= params.max_positions else ""))
    for symbol, size in day.buys:
        shares = int(size.units) if size.units >= 1 else round(size.units, 3)
        lines.append(f"- **{symbol}** — +{f.ret_6m[symbol] * 100:.0f}% på 6 mån (starkare än {f.rs[symbol] * 100:.0f}% av "
                     f"{len(f.rs)} aktier). Köp vid öppning, ≈ {shares} st (${size.position_size_usd:,.0f})"
                     + (f", stop-order {params.stop_pct * 100:g}% under köppriset" if params.stop_pct else "") + ".")

    lines += ["", f"## 🔴 SÄLJ ({len(day.sells)})"]
    if not day.sells:
        lines.append("Inga säljsignaler idag.")
    for record, reason, mark in day.sells:
        pnl = f" ({mark['unrealized_pct']:+.1f}% hittills)" if mark and mark.get("unrealized_pct") is not None else ""
        lines.append(f"- **{record.symbol}** — sälj vid öppning: {reason}{pnl}.")
    finished = [e for e in day.closed if e["result"] != SKIPPED_GAP]
    if finished:
        lines += ["", "Avslutade sedan förra rapporten:"]
        for e in finished:
            how = "såld vid öppning" if e["result"] == ROTATION_EXIT else "stop-order utlöst"
            lines.append(f"- {e['symbol']}: {how}, {e['return_pct']:+.1f}% efter avgifter "
                         f"(köpt {e['fill_price']:g} → {e['exit_price']:g}, {e.get('holding_bars', '?')} handelsdagar)")

    lines += ["", f"## 📊 Innehav ({len(open_positions)}/{params.max_positions})"]
    if open_positions:
        lines += ["| Aktie | Köpt | Senast | Resultat | Rel. styrka nu | Dagar |", "|---|---|---|---|---|---|"]
        for record, mark in open_positions:
            rs_now = f"{f.rs[record.symbol] * 100:.0f}%" if f is not None and record.symbol in f.rs else "—"
            status = " (säljs vid öppning)" if record.exit_signal_at else ""
            if not mark or mark.get("fill_price") is None:
                lines.append(f"| {record.symbol}{status} | köps vid nästa öppning | {mark['last_close']:g} | — | {rs_now} | 0 |"
                             if mark else f"| {record.symbol} | ? | data saknas | — | {rs_now} | ? |")
                continue
            lines.append(f"| {record.symbol}{status} | {mark['fill_price']:g} | {mark['last_close']:g} | {mark['unrealized_pct']:+.1f}% | "
                         f"{rs_now} | {mark['sessions_held']} |")
    else:
        lines.append("Inga innehav.")

    if day.next_up:
        lines += ["", "## 👀 Näst på tur", "Starkast av de som uppfyller köpreglerna men inte fick plats: " + ", ".join(day.next_up) + "."]

    lines += ["", "## 📈 Resultat hittills (papperstrading, riktiga fyllnadspriser, avgifter inräknade)"]
    if performance.get("closed_total"):
        lines.append(f"{performance['closed_total']} stängda affärer · {performance['win_rate'] * 100:.0f}% vinnare · "
                     f"snitt {performance['average_return_pct']:+.2f}% per affär")
    else:
        lines.append("Inga stängda affärer ännu.")

    ev = rotation_evidence(evidence, params)
    lines += ["", "---"]
    if ev:
        lines.append(f"Backtest av exakt dessa regler ({ev['label']}): {ev['cagr_pct']:+.1f}%/år, största nedgång {ev['max_drawdown_pct']:.0f}% "
                     f"— SPY samma period {ev['spy_cagr_pct']:+.1f}%/år, största nedgång {ev['spy_max_drawdown_pct']:.0f}%.")
    skipped = len(f.skipped) if f is not None else 0
    lines += [
        f"Universum: {universe_size} aktier ({skipped} utan data idag).",
        "Boten handlar aldrig åt dig. Historik är ingen garanti — varje affär kan förlora.",
    ]
    return "\n".join(lines)
