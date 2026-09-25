"""Command-line entry points, used by the GitHub Actions workflows.

    python -m app.cli research [--years 10] [--out research_output]
    python -m app.cli daily    [--report-dir reports]
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
    from app.config import settings
    from app.db import init_db
    from app.research import run_research

    init_db()
    symbols = args.symbols.split(",") if args.symbols else list(settings.watchlist)
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


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    parser = argparse.ArgumentParser(prog="tradingbot")
    sub = parser.add_subparsers(dest="command", required=True)

    research = sub.add_parser("research", help="backtest every strategy across the universe")
    research.add_argument("--years", type=int, default=10)
    research.add_argument("--out", default="research_output")
    research.add_argument("--symbols", default="", help="comma-separated; default = configured universe")
    research.set_defaults(func=cmd_research)

    daily = sub.add_parser("daily", help="scan, update open positions, report and notify")
    daily.add_argument("--report-dir", default="reports")
    daily.set_defaults(func=cmd_daily)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
