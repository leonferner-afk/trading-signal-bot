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

from app.rotation import RotationParams
from app.scoring.score import Signal
from app.strategies import breakout, momentum, reversal

STRATEGY_MODULES = {"breakout": breakout, "momentum": momentum, "reversal": reversal}

# Must equal app.research's row filters (asserted in tests).
MIN_ATR_PCT = 1.0
MIN_STOP_DIST_PCT = 0.5
MAX_STOP_DIST_PCT = 25.0


@dataclass(frozen=True)
class LivePolicy:
    research_name: str
    strategies: tuple[str, ...]
    min_score: float
    require_spy_above_200: bool
    require_stock_above_200: bool
    rs_min: float = 0.0          # cross-sectional 6-month return percentile (0-1)
    near_high_min: float = 0.0   # close / 52-week high
    rank_by: str = "score"       # "score" or "rs": which candidates win limited slots
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
        # Same preconditions every research row had to meet — the evidence
        # says nothing about setups outside them.
        atr_pct = signal.context.get("atr_pct")
        if atr_pct is None or atr_pct < MIN_ATR_PCT:
            return False, f"för låg volatilitet (ATR {atr_pct}% < {MIN_ATR_PCT:g}%)"
        if not MIN_STOP_DIST_PCT <= signal.risk_pct <= MAX_STOP_DIST_PCT:
            return False, f"stop-avstånd {signal.risk_pct:.1f}% utanför {MIN_STOP_DIST_PCT:g}–{MAX_STOP_DIST_PCT:g}%"
        if self.rs_min > 0:
            rs = signal.context.get("rs")
            if rs is None or rs < self.rs_min:
                return False, f"relativ styrka {'okänd' if rs is None else f'{rs * 100:.0f}%'} < topp {100 - self.rs_min * 100:.0f}%"
        if self.near_high_min > 0:
            near = signal.context.get("near_high")
            if near is None or near < self.near_high_min:
                return False, f"för långt från 52-veckorshögsta ({'okänt' if near is None else f'{near * 100:.0f}%'})"
        return True, "ok"

    def rank_key(self, signal: Signal) -> float:
        if self.rank_by == "rs":
            return signal.context.get("rs") or 0.0
        return signal.score


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
    rs_min = float(os.getenv("POLICY_RS_MIN") or "0")
    near_high_min = float(os.getenv("POLICY_NEAR_HIGH_MIN") or "0")
    rank_by = (os.getenv("POLICY_RANK_BY") or "score").strip().lower()
    return LivePolicy(
        research_name=research_policy_name(min_score, spy, stock, rs_min, near_high_min),
        strategies=strategies,
        min_score=min_score,
        require_spy_above_200=spy,
        require_stock_above_200=stock,
        rs_min=rs_min,
        near_high_min=near_high_min,
        rank_by=rank_by if rank_by in ("score", "rs") else "score",
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


# Chosen from the research on train+validation data only (see README,
# "Evidence"); each knob can be overridden via env.
DEFAULT_MODE = "rotation"
DEFAULT_ROTATION_UNIVERSE = "largecap"
DEFAULT_ROTATION = RotationParams(max_positions=8, entry_rs=0.8, exit_rs=0.5, regime_exit=False, stop_pct=0.0)


def active_mode() -> str:
    mode = (os.getenv("POLICY_MODE") or DEFAULT_MODE).strip().lower()
    return mode if mode in ("rotation", "swing") else DEFAULT_MODE


def active_rotation_params() -> RotationParams:
    from app.config import settings

    d = DEFAULT_ROTATION
    rebalance = (os.getenv("ROTATION_REBALANCE") or d.rebalance).strip().lower()
    max_positions = int(os.getenv("ROTATION_MAX_POSITIONS") or d.max_positions)
    return RotationParams(
        max_positions=max_positions,
        entry_rs=float(os.getenv("ROTATION_ENTRY_RS") or d.entry_rs),
        exit_rs=float(os.getenv("ROTATION_EXIT_RS") or d.exit_rs),
        regime_exit=_env_bool("ROTATION_REGIME_EXIT", d.regime_exit),
        stop_pct=float(os.getenv("ROTATION_STOP_PCT") or d.stop_pct),
        # Monthly rule sets fill every free slot on the rebalance day (as tested).
        max_new_per_day=max_positions if rebalance == "monthly" else settings.max_new_buys_per_day,
        momentum=(os.getenv("ROTATION_MOMENTUM") or d.momentum).strip(),
        rebalance=rebalance,
    )


def active_rotation_universe() -> tuple[str, ...]:
    from app.universe import rotation_universe

    return rotation_universe((os.getenv("ROTATION_UNIVERSE") or DEFAULT_ROTATION_UNIVERSE).strip().lower())
