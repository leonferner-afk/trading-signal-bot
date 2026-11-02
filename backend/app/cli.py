"""Command-line entry points, used by the GitHub Actions workflows.

    python -m app.cli research      [--years 10] [--out research_output]
    python -m app.cli daily         [--report-dir reports]
    python -m app.cli hypothetical  [--base-sek 10000] [--out hypothetical.json]
"""
from __future__ import annotations

import argparse
import logging
import os
import sys


def _append_step_summary(markdown: str) -> None:
    path = os.environ.get("GITHUB_STEP_SUMMARY")
    if path:
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(markdown + "\n")


def cmd_research(args: argparse.Namespace) -> int:
    from app.db import init_db
    from app.research import run_research
    from app.universe import research_universe

    init_db()
    symbols = [s.strip() for s in args.symbols.split(",") if s.strip()] or list(research_universe())
    results = run_research(symbols, years=args.years, out_dir=args.out)
    report = open(os.path.join(args.out, "research.md"), encoding="utf-8").read()
    print(report)
    _append_step_summary(report)
    return 0 if results["policies"] else 1


def cmd_daily(args: argparse.Namespace) -> int:
    from app.daily import run_daily

    outcome = run_daily(report_dir=args.report_dir)
    print(outcome.report_markdown)
    _append_step_summary(outcome.report_markdown)
    return 0 if outcome.ok else 1


def cmd_dashboard(args: argparse.Namespace) -> int:
    """Rebuilds the public status page (GitHub Pages) from the run's files."""
    from pathlib import Path

    from app.dashboard import build_site

    page = build_site(Path(args.state), Path(args.out))
    print(f"Status page: {page}" if page else "No hypothetical.json yet — no status page built.")
    return 0


def cmd_hypothetical(args: argparse.Namespace) -> int:
    """Prints (and optionally writes as JSON) "if you'd put base-sek kronor
    (default 10 000) into the live rotation on day one" — informational only, no real money.
    See app/hypothetical.py for exactly what it does and doesn't assume."""
    import json

    from app.data.stock_client import DataUnavailable, StockClient
    from app.db import init_db
    from app.hypothetical import FX_SYMBOL, format_hypothetical_message, hypothetical_value, to_utc, trade_rows
    from app.journal import repository as journal
    from app.live_rotation import _bot_share_pct, bot_capital, rocket_pot_capital
    from app.paper_trading.simulator import current_mark
    from app.policy import active_rotation_params

    init_db()
    from app.rocket_portfolio import admitted

    records = journal.rotation_records()
    pot_records = journal.rocket_pot_records()
    rocket_taken = admitted(journal.rocket_records())
    if not records and not pot_records:
        message = "Inga rotation-affärer i journalen ännu."
        print(message)
        _append_step_summary(message)
        return 0

    since_ts = to_utc(args.since) if args.since else None
    # Positions already held at the restart are counted from their close then.
    held_at_restart = [r for r in records if since_ts is not None and to_utc(r.timestamp) < since_ts
                       and (r.result == "OPEN" or (r.closed_at is not None and to_utc(r.closed_at) > since_ts))]
    open_records = [r for r in records if r.result == "OPEN"]
    open_pot = [r for r in pot_records if r.result == "OPEN"]
    open_rockets = [r for r in rocket_taken if r.result == "OPEN"]
    with StockClient() as client:
        client.prefetch(sorted({r.symbol for r in records + pot_records + open_rockets}) + [FX_SYMBOL], "1d", limit=400)
        rocket_marks = {r.id: current_mark(client, r) for r in open_rockets}
        marks = {r.symbol: current_mark(client, r) for r in open_records}
        pot_marks = {r.id: current_mark(client, r) for r in open_pot}
        base_closes = {}
        for r in held_at_restart:
            try:
                bars = client.get_klines(r.symbol, "1d", limit=400)
            except DataUnavailable:
                continue
            before = bars[bars["close_time"] <= since_ts]
            if not before.empty:
                base_closes[r.symbol] = float(before["close"].iloc[-1])
        trade_bars = {}
        for symbol in {r.symbol for r in records + pot_records}:
            try:
                trade_bars[symbol] = client.get_klines(symbol, "1d", limit=400)
            except DataUnavailable:
                pass
        try:
            fx = client.get_klines(FX_SYMBOL, "1d", limit=400)
        except DataUnavailable:
            fx = None
        try:
            spy = client.get_klines("SPY", "1d", limit=400)
        except DataUnavailable:
            spy = None

    # The index-fund part: SPY in kronor from the start close to the latest close.
    start_ts = since_ts or to_utc((records or pot_records)[0].timestamp)
    index_sek_pct = None
    if spy is not None and not spy.empty and fx is not None:
        from app.hypothetical import fx_rate_on

        before = spy[spy["close_time"] <= start_ts]
        fx0, fx1 = fx_rate_on(fx, start_ts), fx_rate_on(fx, spy["close_time"].iloc[-1])
        if not before.empty and fx0 and fx1:
            index_sek_pct = ((float(spy["close"].iloc[-1]) / float(before["close"].iloc[-1])) * (fx1 / fx0) - 1) * 100

    params = active_rotation_params()
    managed = bot_capital() + rocket_pot_capital()
    pot_pct = rocket_pot_capital() / managed * 100 if managed > 0 else 0.0
    result = hypothetical_value(records, marks, fx, base_sek=args.base_sek, max_positions=params.max_positions,
                                since=since_ts, base_closes=base_closes, pot_records=pot_records, pot_marks=pot_marks,
                                pot_pct=pot_pct, index_pct=100.0 - _bot_share_pct(), index_sek_pct=index_sek_pct)
    since = args.since[:10] if args.since else (records or pot_records)[0].timestamp[:10]
    message = format_hypothetical_message(result, since)
    rocket_sek = None
    if rocket_taken:
        from app.hypothetical import _fmt_kr, rocket_portfolio_sek

        rocket_sek, rocket_missing = rocket_portfolio_sek(rocket_taken, rocket_marks, fx, args.base_sek)
        message += (f"\n🚀 Raketportfölj (papper, på kul) sedan {rocket_taken[0].timestamp[:10]}: "
                    f"{_fmt_kr(args.base_sek)} kr → **{_fmt_kr(rocket_sek)} kr** "
                    f"({(rocket_sek / args.base_sek - 1) * 100:+.1f}%)"
                    + (f" ({rocket_missing} utan valutakurs ännu)" if rocket_missing else ""))
    print(message)
    _append_step_summary(message)

    if args.out:
        payload = {
            "base_sek": result.base_sek, "total_sek": result.total_sek, "delta_sek": result.delta_sek,
            "delta_pct": result.delta_pct, "since": since, "fx_missing": result.fx_missing, "message": message,
            "rocket_paper_sek": rocket_sek,
            "pot_pct": round(pot_pct, 2), "index_pct": result.index_pct, "index_sek_pct": result.index_sek_pct,
            "positions": [
                {"symbol": p.symbol, "kind": p.kind, "status": p.status, "usd_return_pct": p.usd_return_pct,
                 "sek_return_pct": p.sek_return_pct, "id": p.record_id, "entry_price": p.entry_price,
                 "last_price": p.last_price, "invested_sek": p.invested_sek, "sell_signaled": p.sell_signaled,
                 "value_sek": None if p.sek_return_pct is None or p.invested_sek is None
                 else round(p.invested_sek * (1 + p.sek_return_pct / 100), 2)}
                for p in result.positions
            ],
            "trades": trade_rows(records, "rotation", trade_bars, lambda r: marks.get(r.symbol))
                      + trade_rows(pot_records, "lekpott", trade_bars, lambda r: pot_marks.get(r.id)),
        }
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2)
    return 0


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    parser = argparse.ArgumentParser(prog="tradingbot")
    sub = parser.add_subparsers(dest="command", required=True)

    research = sub.add_parser("research", help="backtest every strategy across the universe")
    research.add_argument("--years", type=int, default=10)
    research.add_argument("--out", default="research_output")
    research.add_argument("--symbols", default="", help="comma-separated; default = research universe (scan universe + 2015 large caps)")
    research.set_defaults(func=cmd_research)

    daily = sub.add_parser("daily", help="scan, update open positions, report and notify")
    daily.add_argument("--report-dir", default="reports")
    daily.set_defaults(func=cmd_daily)

    hypothetical = sub.add_parser("hypothetical", help="informational: what a fixed SEK stake in the live rotation would be worth today")
    hypothetical.add_argument("--base-sek", type=float, default=10000.0)
    hypothetical.add_argument("--since", default="", help="restart: a session close (ISO, UTC); empty = from the first trade")
    hypothetical.add_argument("--out", default="", help="optional path to write a JSON summary")
    hypothetical.set_defaults(func=cmd_hypothetical)

    dashboard = sub.add_parser("dashboard", help="rebuild the public status page from the bot-state files")
    dashboard.add_argument("--state", required=True, help="checked-out bot-state directory")
    dashboard.add_argument("--out", required=True, help="where to write index.html")
    dashboard.set_defaults(func=cmd_dashboard)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
