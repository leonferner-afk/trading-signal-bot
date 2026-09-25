"""The live policy: which scanner signals become an actual BUY
notification, and the backtest evidence quoted alongside each one.

The rule set is deliberately small and mirrors a named policy in
app.research, so every BUY can quote how that exact rule set performed
historically (from evidence.json, refreshed weekly by the research
workflow). Anything the scanner finds that the policy doesn't admit is
still listed in the daily report as "bevakning" (watch), never pushed as
a buy.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path

from app.scoring.score import Signal
from app.strategies import breakout, momentum, reversal

STRATEGY_MODULES = {"breakout": breakout, "momentum": momentum, "reversal": reversal}


@dataclass(frozen=True)
class LivePolicy:
    research_name: str
    strategies: tuple[str, ...]
    min_score: float
    require_spy_above_200: bool
    require_stock_above_200: bool
    exit_style: str = "fixed"

    def strategy_modules(self) -> list:
        return [STRATEGY_MODULES[name] for name in self.strategies]

    def admits(self, signal: Signal) -> tuple[bool, str]:
        if signal.direction != "LONG":
            return False, "endast köp (long) skickas"
        if signal.strategy not in self.strategies:
            return False, f"strategin {signal.strategy} saknar stöd i backtesten"
        if signal.score < self.min_score:
            return False, f"score {signal.score:.0f} < {self.min_score:.0f}"
        if self.require_spy_above_200 and not signal.context.get("spy_above_200"):
            return False, "marknaden (SPY) under sitt 200-dagars snitt"
        if self.require_stock_above_200 and not signal.context.get("stock_above_200"):
            return False, "aktien under sitt 200-dagars snitt"
        return True, "ok"


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    return default if not value else value.strip().lower() in ("1", "true", "yes")


def active_policy() -> LivePolicy:
    """Defaults are set from the research results (see README, "Evidence");
    each knob can be overridden via env for experimentation."""
    # Research (10y, ~200 stocks): reversal did worse than random entry, and
    # scores >= 80 had negative expectancy (over-extended entries), while
    # score >= 70 with both trend filters was the best policy overall and
    # out-of-sample. See README "Evidence".
    strategies = tuple(
        s.strip() for s in (os.getenv("POLICY_STRATEGIES") or "breakout,momentum").split(",") if s.strip() in STRATEGY_MODULES
    )
    min_score = float(os.getenv("POLICY_MIN_SCORE") or "70")
    spy = _env_bool("POLICY_REQUIRE_SPY_ABOVE_200", True)
    stock = _env_bool("POLICY_REQUIRE_STOCK_ABOVE_200", True)
    return LivePolicy(
        research_name=research_policy_name(min_score, spy, stock),
        strategies=strategies,
        min_score=min_score,
        require_spy_above_200=spy,
        require_stock_above_200=stock,
    )


def research_policy_name(min_score: float, spy: bool, stock: bool, rs_min: float = 0.0, near_high_min: float = 0.0) -> str:
    """Single naming scheme shared by research and the live policy, so a
    live rule set can always find its own backtest row."""
    parts = [f"score>={min_score:g}"] if min_score > 0 else []
    if spy:
        parts.append("SPY>200d")
    if stock:
        parts.append("stock>200d")
    if rs_min > 0:
        parts.append(f"RS>={rs_min:g}")
    if near_high_min > 0:
        parts.append(f"high52>={near_high_min:g}")
    return " & ".join(parts) or "all"


def load_evidence(path: str | None = None) -> dict | None:
    path = path or os.getenv("EVIDENCE_PATH", "evidence.json")
    try:
        return json.loads(Path(path).read_text())
    except (OSError, ValueError):
        return None


def evidence_for(evidence: dict | None, strategy: str, policy: LivePolicy) -> dict | None:
    """Historical stats for this strategy under this exact policy, in the
    shape the notifier quotes. None if research hasn't covered it."""
    if not evidence:
        return None
    for row in evidence.get("policies", []):
        if row["group"] == strategy and row["policy"] == policy.research_name and row.get("exit", "fixed") == policy.exit_style:
            overall, oos = row["overall"], row.get("out_of_sample") or {}
            if not overall.get("n"):
                return None
            years = (evidence.get("meta") or {}).get("years", "?")
            symbols = (evidence.get("meta") or {}).get("symbols_ok", "?")
            return {
                "label": f"backtest {years} år, {symbols} aktier, samma regler",
                "n": overall["n"],
                "win_rate": overall["win_rate"],
                "avg_r": overall["avg_r"],
                "avg_ret_pct": overall["avg_ret_pct"],
                "avg_hold_bars": overall["avg_hold_bars"],
                "oos_n": oos.get("n", 0),
                "oos_avg_r": oos.get("avg_r"),
            }
    return None
