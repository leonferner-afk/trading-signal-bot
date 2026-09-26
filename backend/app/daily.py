"""The once-a-day job (run by GitHub Actions after the US close):

  1. download the whole universe in a few batched requests
  2. resolve open positions (target / stop / time exit) -> SÄLJ notices
  3. scan for new setups; the live policy decides which become KÖP
  4. respect position limits (max open, max new per day, one per stock)
  5. write a Markdown report and deliver it (GitHub issue + Telegram)

Everything the report states comes from real data or the journal; a
symbol that couldn't be fetched is listed as skipped, never guessed.
"""
from __future__ import annotations

import datetime as dt
import logging
from dataclasses import dataclass, field
from pathlib import Path

from app.config import settings
from app.data.stock_client import DataUnavailable, StockClient
from app.db import init_db
from app.journal import repository as journal
from app.notify import github_issue, telegram_client
from app.notify.notifier import notify_entry
from app.paper_trading.simulator import SKIPPED_GAP, current_mark, run_paper_trading_update
from app.policy import LivePolicy, active_policy, evidence_for, load_evidence
from app.risk.position_sizing import PositionSize, compute_position_size
from app.runtime_settings import get_effective_settings
from app.scanner.scanner import ANCHOR_SYMBOL, ScanResult, run_scan
from app.scoring.score import Signal

logger = logging.getLogger("tradingbot.daily")

MIN_POSITION_PCT = 2.0      # smaller than this isn't worth the fixed costs
MAX_SESSION_AGE_DAYS = 5    # latest bar older than this -> data is stale


@dataclass
class DailyOutcome:
    ok: bool
    report_markdown: str
    buys: list[Signal] = field(default_factory=list)
    exits: list[dict] = field(default_factory=list)
    issue_url: str | None = None


def select_buys(
    signals: list[Signal],
    policy: LivePolicy,
    open_symbols: set[str],
    open_count: int,
    committed_usd: float = 0.0,
) -> tuple[list[tuple[Signal, PositionSize]], list[tuple[Signal, str]]]:
    """Best candidates first (by the policy's rank); each signal either
    becomes a BUY with a concrete size, or goes on the watch list with the
    reason it wasn't bought. Sizes respect the per-position cap and the
    capital still free after the positions already open (`committed_usd`)."""
    live = get_effective_settings()
    portfolio = live.portfolio_size_usd
    free = max(0.0, portfolio - committed_usd)
    slots = min(max(0, settings.max_open_positions - open_count), settings.max_new_buys_per_day)
    buys: list[tuple[Signal, PositionSize]] = []
    watch: list[tuple[Signal, str]] = []
    for signal in sorted(signals, key=lambda s: (policy.rank_key(s), s.score), reverse=True):
        admitted, reason = policy.admits(signal)
        if not admitted:
            watch.append((signal, reason))
            continue
        if signal.symbol in open_symbols:
            watch.append((signal, "redan en öppen position i aktien"))
            continue
        if len(buys) >= slots:
            watch.append((signal, "max antal positioner/köp per dag nått"))
            continue
        size = compute_position_size(signal.entry, signal.stop, portfolio, live.risk_per_trade_pct,
                                     settings.max_position_pct, available_usd=free)
        if size.position_size_usd < portfolio * MIN_POSITION_PCT / 100:
            watch.append((signal, "inte tillräckligt med fritt kapital"))
            continue
        free -= size.position_size_usd
        buys.append((signal, size))
    return buys, watch


def committed_capital(open_records) -> float:
    """Capital tied up in open positions, sized the way they were advised."""
    live = get_effective_settings()
    return sum(
        compute_position_size(r.entry, r.stop, live.portfolio_size_usd, live.risk_per_trade_pct,
                              settings.max_position_pct).position_size_usd
        for r in open_records
    )


def session_date(df) -> str | None:
    if df is None or df.empty:
        return None
    return df["close_time"].iloc[-1].tz_convert("America/New_York").strftime("%Y-%m-%d")


def _fmt_money(value: float) -> str:
    return f"${value:,.0f}"


def build_report(
    today: str,
    scan: ScanResult,
    policy: LivePolicy,
    buys: list[tuple[Signal, PositionSize]],
    buy_evidence: dict[str, dict | None],
    watch: list[tuple[Signal, str]],
    exits: list[dict],
    open_positions: list[tuple],
    performance: dict,
    evidence_available: bool,
    session: str | None = None,
    new_session: bool = True,
) -> str:
    live = get_effective_settings()
    market = {True: "över", False: "under", None: "okänt"}[scan.spy_above_200]
    real_exits = [e for e in exits if e["result"] != SKIPPED_GAP]
    lines = [
        f"# Tradingbot {today}",
        "",
        f"**Marknaden:** SPY {market} sitt 200-dagars snitt · trend {scan.market_wide_risk}",
        f"**Portfölj:** {_fmt_money(live.portfolio_size_usd)}, risk {live.risk_per_trade_pct:g}% per affär · "
        f"{len(open_positions)}/{settings.max_open_positions} öppna positioner",
        "",
        f"**Senaste handelsdag i datan:** {session or 'okänd'}",
        "",
        f"## 🟢 KÖP ({len(buys)})",
    ]
    if not new_session:
        lines.append("Ingen ny handelsdag sedan förra körningen (helgdag eller omkörning) — inga nya signaler.")
    elif not buys:
        lines.append("Inga nya köp idag — inget klarade kvalitetskraven. Det är ett korrekt resultat; alla dagar har inte en bra affär.")
    for signal, size in buys:
        ev = buy_evidence.get(signal.symbol)
        lines += [
            "",
            f"### {signal.symbol} — {signal.strategy}, score {signal.score:.0f}/100",
            f"- **Köp** vid öppning (senaste stängning {signal.entry:g})",
            f"- **Stop-loss** {signal.stop:g} (−{signal.risk_pct:.1f}%) — lägg som stop-order direkt",
            f"- **Mål** {signal.target:g} (+{signal.reward_pct:.1f}%) — lägg som limit-säljorder direkt",
            f"- **Storlek** ≈ {int(size.units) if size.units >= 1 else round(size.units, 3)} st ({_fmt_money(size.position_size_usd)}, "
            f"{size.position_pct_of_portfolio:.0f}% av portföljen) → max förlust vid stop ≈ {_fmt_money(size.risk_amount_usd)}",
            f"- **Varför:** " + "; ".join(signal.reasons),
        ]
        if ev:
            oos = f", senaste perioden {ev['oos_avg_r']:+.2f}R ({ev['oos_n']} st)" if ev.get("oos_n") else ""
            lines.append(f"- **Historik** ({ev['label']}): {ev['n']} affärer, {ev['win_rate'] * 100:.0f}% vinnare, "
                         f"snitt {ev['avg_r']:+.2f}R{oos}")
        if signal.warning:
            lines.append(f"- ⚠ {signal.warning}")
        lines.append("- Öppnar aktien under stop-nivån: köp inte, signalen är redan ogiltig.")

    lines += ["", f"## 🔴 SÄLJ ({len(real_exits)})"]
    if not real_exits:
        lines.append("Inga positioner stängdes.")
    labels = {"TARGET_HIT": "✅ mål nått", "STOP_HIT": "🛑 stop", "TIME_EXIT": "⏱ tid ute — sälj vid öppning"}
    for e in real_exits:
        r = f" ({e['r_multiple']:+.2f}R)" if e.get("r_multiple") is not None else ""
        lines.append(f"- **{e['symbol']}** {labels.get(e['result'], e['result'])}: {e['return_pct']:+.1f}%{r}, "
                     f"köpt {e['fill_price']:g} → {e['exit_price']:g}, {e.get('holding_bars', '?')} handelsdagar")
    for e in (e for e in exits if e["result"] == SKIPPED_GAP):
        lines.append(f"- {e['symbol']}: öppnade under stop-nivån ({e['fill_price']:g}) — köptes aldrig.")

    lines += ["", f"## 📊 Öppna positioner ({len(open_positions)})"]
    if open_positions:
        lines += ["| Aktie | Köpt | Senast | Resultat | Stop | Mål | Dagar |", "|---|---|---|---|---|---|---|"]
        for record, mark in open_positions:
            if not mark or mark.get("fill_price") is None:
                lines.append(f"| {record.symbol} | köps vid nästa öppning | {mark['last_close']:g} | — | {record.stop:g} | {record.target:g} | 0 |"
                             if mark else f"| {record.symbol} | ? | data saknas | — | {record.stop:g} | {record.target:g} | ? |")
                continue
            lines.append(f"| {record.symbol} | {mark['fill_price']:g} | {mark['last_close']:g} | {mark['unrealized_pct']:+.1f}% | "
                         f"{record.stop:g} | {record.target:g} | {mark['sessions_held']} |")
    else:
        lines.append("Inga öppna positioner.")

    if watch:
        lines += ["", f"## 👀 Bevakning ({len(watch)})", "Hittades av skannern men blev inte köp:"]
        for signal, reason in watch[:15]:
            lines.append(f"- {signal.symbol} ({signal.strategy}, score {signal.score:.0f}) — {reason}")

    lines += ["", "## 📈 Resultat hittills (papperstrading, riktiga fyllnadspriser)"]
    if performance.get("closed_total"):
        avg_r = performance.get("average_r")
        lines.append(
            f"{performance['closed_total']} stängda affärer · {performance['win_rate'] * 100:.0f}% vinnare · "
            f"snitt {performance['average_return_pct']:+.2f}% per affär"
            + (f" · {avg_r:+.2f}R i snitt, totalt {performance['total_r']:+.1f}R" if avg_r is not None else "")
        )
    else:
        lines.append("Inga stängda affärer ännu.")

    lines += [
        "",
        "---",
        f"Skannade {len(scan.watchlist)} aktier ({len(scan.skipped)} hoppades över p.g.a. datafel). "
        f"Regler: strategier {', '.join(policy.strategies)}, score ≥ {policy.min_score:g}"
        + (", SPY över 200d" if policy.require_spy_above_200 else "")
        + (", aktien över 200d" if policy.require_stock_above_200 else "")
        + ("" if evidence_available else " · (backtest-statistik saknas tills forskningen körts)")
        + ".",
        "Boten handlar aldrig åt dig. Historik är ingen garanti — varje affär kan förlora.",
    ]
    return "\n".join(lines)


def run_daily(report_dir: str | Path = "reports") -> DailyOutcome:
    init_db()
    live = get_effective_settings()
    policy = active_policy()
    evidence = load_evidence()
    now = dt.datetime.now(dt.timezone.utc)
    today = now.strftime("%Y-%m-%d")

    client = StockClient()
    open_before = journal.get_open_signals()
    universe = [s for s in live.watchlist if s != ANCHOR_SYMBOL]
    client.prefetch(sorted(set(universe + [r.symbol for r in open_before] + [ANCHOR_SYMBOL])), "1d", limit=400)

    # Which market session does today's data end on? Same session as the
    # last processed run -> nothing new happened (US holiday, manual re-run):
    # positions are still checked, but no new signals are issued.
    try:
        session = session_date(client.get_klines(ANCHOR_SYMBOL, "1d", limit=400))
    except DataUnavailable:
        session = None
    last_session = journal.last_processed_session()
    new_session = session is not None and session != last_session
    stale = session is None or (now.date() - dt.date.fromisoformat(session)).days > MAX_SESSION_AGE_DAYS

    exits = run_paper_trading_update(client=client)["updated"]
    if new_session and not stale:
        scan = run_scan(universe, "1d", client=client, strategies=policy.strategy_modules())
    else:
        scan = ScanResult(scanned_at=now.isoformat(), watchlist=universe, market_wide_risk="UNKNOWN", signals=[],
                          spy_above_200=None)
    ok = not stale and (not new_session or (scan.spy_above_200 is not None and len(scan.skipped) < max(10, len(universe) // 2)))

    open_now = journal.get_open_signals()
    buys, watch = select_buys(scan.signals, policy, {r.symbol for r in open_now}, len(open_now), committed_capital(open_now))
    buy_evidence: dict[str, dict | None] = {}
    for signal, size in buys:
        ev = evidence_for(evidence, signal.strategy, policy)
        buy_evidence[signal.symbol] = ev
        journal.save_signal(signal, ev)
        notify_entry(signal, ev, min_score=0, size=size)

    open_positions = [(r, current_mark(client, r)) for r in journal.get_open_signals()]
    report = build_report(today, scan, policy, buys, buy_evidence, watch, exits, open_positions,
                          journal.performance_summary(), evidence is not None, session, new_session)
    if stale:
        report = (f"> ⚠ **Marknadsdatan är inaktuell** (senaste handelsdag: {session or 'saknas'}) — inga nya signaler idag. "
                  "Kontrollera datakällan om detta upprepas.\n\n") + report
    elif not ok:
        report = "> ⚠ **Datakvaliteten var för dålig idag** (för många aktier kunde inte hämtas) — resultatet nedan är ofullständigt.\n\n" + report

    out = Path(report_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{today}.md").write_text(report, encoding="utf-8")
    (out / "latest.md").write_text(report, encoding="utf-8")

    issue_url = None
    real_exits = [e for e in exits if e["result"] != SKIPPED_GAP]
    if buys or real_exits or not ok:
        parts = ([f"KÖP {', '.join(s.symbol for s, _ in buys)}"] if buys else []) + \
                ([f"SÄLJ {', '.join(e['symbol'] for e in real_exits)}"] if real_exits else [])
        title = f"📈 {today}: " + (" · ".join(parts) if parts else "⚠ datafel, kontrollera körningen")
        issue_url = github_issue.publish(title, report)
        if telegram_client.is_configured() and not buys and not real_exits:
            telegram_client.send_message(title)

    if new_session and ok:
        journal.record_bot_run(session, len(buys), len(real_exits))
    logger.info("daily: session %s (new=%s, stale=%s), %d buys, %d exits, %d watch, %d skipped symbols, issue=%s",
                session, new_session, stale, len(buys), len(real_exits), len(watch), len(scan.skipped), issue_url)
    return DailyOutcome(ok=ok, report_markdown=report, buys=[s for s, _ in buys], exits=exits, issue_url=issue_url)
