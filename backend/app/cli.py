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


def cmd_hypothetical(args: argparse.Namespace) -> int:
    """Prints (and optionally writes as JSON) "if you'd put base-sek kronor
    (default 10 000) into the live rotation on day one" — informational only, no real money.
    See app/hypothetical.py for exactly what it does and doesn't assume."""
    import json

    from app.data.stock_client import DataUnavailable, StockClient
    from app.db import init_db
    from app.hypothetical import FX_SYMBOL, format_hypothetical_message, hypothetical_value, to_utc
    from app.journal import repository as journal
    from app.live_rotation import bot_capital, rocket_pot_capital
    from app.paper_trading.simulator import current_mark
    from app.policy import active_rotation_params

    init_db()
    records = journal.rotation_records()
    pot_records = journal.rocket_pot_records()
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
    with StockClient() as client:
        client.prefetch(sorted({r.symbol for r in open_records + open_pot + held_at_restart}) + [FX_SYMBOL], "1d", limit=400)
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
        try:
            fx = client.get_klines(FX_SYMBOL, "1d", limit=400)
        except DataUnavailable:
            fx = None

    params = active_rotation_params()
    managed = bot_capital() + rocket_pot_capital()
    pot_pct = rocket_pot_capital() / managed * 100 if managed > 0 else 0.0
    result = hypothetical_value(records, marks, fx, base_sek=args.base_sek, max_positions=params.max_positions,
                                since=since_ts, base_closes=base_closes, pot_records=pot_records, pot_marks=pot_marks,
                                pot_pct=pot_pct)
    since = args.since[:10] if args.since else (records or pot_records)[0].timestamp[:10]
    message = format_hypothetical_message(result, since)
    print(message)
    _append_step_summary(message)

    if args.out:
        payload = {
            "base_sek": result.base_sek, "total_sek": result.total_sek, "delta_sek": result.delta_sek,
            "delta_pct": result.delta_pct, "since": since, "fx_missing": result.fx_missing, "message": message,
            "pot_pct": round(pot_pct, 2),
            "positions": [
                {"symbol": p.symbol, "kind": p.kind, "status": p.status, "usd_return_pct": p.usd_return_pct,
                 "sek_return_pct": p.sek_return_pct}
                for p in result.positions
            ],
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

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
