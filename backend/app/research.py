"""Evidence research: how would the BUY signals this bot sends have done
on real history, across the whole universe, after costs — and did they
beat buying at random with the exact same exit rules?

That last comparison is the point. The universe is written today, so it
leans toward stocks that survived and went up; any long strategy looks
good on it. A strategy only shows real timing edge if it beats the
random-entry baseline on the same symbols and dates.

Mechanics mirror live trading:
  - signal at a daily close -> filled at the next session's open, with fees
    and slippage both ways
  - stop/target are the levels the user is actually told
  - a gap through the stop fills at the open; a setup already invalidated
    at the next open is not taken
  - one open position per symbol+strategy at a time
  - results are split by date into train / validation / out-of-sample
"""
from __future__ import annotations

import json
import logging
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import numpy as np
import pandas as pd

from app.backtest.engine import MAX_HOLDING_BARS_DEFAULT, net_return_pct, resolve_exit
from app.config import settings
from app.data.news_client import NewsResult
from app.data.stock_client import DataUnavailable, StockClient
from app.regime.classifier import RISK_NEUTRAL, RISK_OFF, RISK_ON, TREND_DOWN, TREND_UP, latest_snapshot
from app.risk.risk_reward import STOP_ATR_MULT, TARGET_ATR_MULT
from app.scanner.scanner import ANCHOR_SYMBOL, enrich
from app.scoring.score import build_signal
from app.strategies import breakout, momentum, reversal

logger = logging.getLogger("tradingbot.research")

WARMUP_BARS = 210
BASELINE_EVERY_N_BARS = 5
STRATEGIES = {"breakout": breakout, "momentum": momentum, "reversal": reversal}
_NO_NEWS = NewsResult(symbol="", available=False, reason="not used in research")


def _thresholds() -> tuple[float, float, float]:
    return (settings.score_exceptional_min, settings.score_high_quality_min, settings.score_watch_min)


def _session_dates(df: pd.DataFrame) -> np.ndarray:
    return df["close_time"].dt.tz_convert("America/New_York").dt.date.to_numpy()


def market_context(spy: pd.DataFrame) -> dict:
    """Session date -> (market-wide risk label, SPY above its 200-day SMA)."""
    context = {}
    for date, trend, close, sma200 in zip(_session_dates(spy), spy["trend_regime"], spy["close"], spy["sma_200"]):
        risk = RISK_ON if trend == TREND_UP else RISK_OFF if trend == TREND_DOWN else RISK_NEUTRAL
        context[date] = (risk, bool(pd.notna(sma200) and close > sma200))
    return context


def _long_preconditions(df: pd.DataFrame) -> dict[str, np.ndarray]:
    """Cheap necessary conditions for each strategy's LONG setup, so the
    full `generate()` only runs on bars that could possibly qualify. Each
    is strictly looser than the strategy's own rule; `generate()` still
    makes the real decision."""
    return {
        "breakout": df["breakout_up"].fillna(False).astype(bool).to_numpy(),
        "momentum": ((df["ema_9"] > df["ema_21"]) & (df["ema_21"] > df["ema_50"])).to_numpy(),
        "reversal": (df["low"].shift(1) <= df["bb_lower"].shift(1)).fillna(False).to_numpy(),
    }


def _trade_row(symbol, strategy, date, i, opens, planned_entry, stop, target, exit_, extra) -> dict:
    """R is measured against the *planned* risk (notified entry -> stop),
    because that's what the position was sized from; filling at a
    different open changes the P&L, not the size."""
    fill = float(opens[i + 1])
    ret = net_return_pct(fill, exit_.raw_price, "LONG", settings.fee_bps, settings.slippage_bps)
    fill_with_costs = fill * (1 + (settings.fee_bps + settings.slippage_bps) / 10000.0)
    planned_risk = planned_entry - stop
    r_multiple = (ret / 100 * fill_with_costs) / planned_risk if planned_risk > 0 else float("nan")
    return {
        "symbol": symbol, "strategy": strategy, "date": str(date), "i": i, "exit_i": exit_.index,
        "result": exit_.result, "ret_pct": ret, "r_multiple": r_multiple,
        "hold_bars": exit_.index - i, "target_pct": (target - fill) / fill * 100, **extra,
    }


def symbol_trades(symbol: str, df: pd.DataFrame, market: dict, max_hold: int = MAX_HOLDING_BARS_DEFAULT) -> tuple[list[dict], int]:
    """Every LONG candidate each strategy produced on this symbol (plus
    the random-entry baseline), each simulated independently. Position
    locking is applied later, per policy. Returns (rows, gap-skipped)."""
    n = len(df)
    opens, highs, lows, closes = (df[c].to_numpy(dtype=float) for c in ("open", "high", "low", "close"))
    dates = _session_dates(df)
    above_200 = (df["close"] > df["sma_200"]).to_numpy()
    atr_pct = (df["atr_14"] / df["close"] * 100).to_numpy()
    rows: list[dict] = []
    gap_skipped = 0
    thresholds = _thresholds()

    for name, module in STRATEGIES.items():
        for i in np.flatnonzero(_long_preconditions(df)[name]):
            if i < WARMUP_BARS or i >= n - 1:
                continue
            window = df.iloc[: i + 1]
            candidate = module.generate(window, symbol)
            if candidate is None or candidate.direction != "LONG":
                continue
            snapshot = latest_snapshot(window)
            if snapshot is None:
                continue
            risk, spy_up = market.get(dates[i], (RISK_NEUTRAL, False))
            signal = build_signal(candidate, snapshot, _NO_NEWS, risk, tier_thresholds=thresholds)
            exit_ = resolve_exit(opens, highs, lows, closes, i + 1, "LONG", signal.stop, signal.target, max_hold)
            if exit_ is None:
                gap_skipped += 1
                continue
            rows.append(_trade_row(symbol, name, dates[i], i, opens, signal.entry, signal.stop, signal.target, exit_, {
                "score": signal.score, "market_risk": risk, "spy_above_200": spy_up,
                "stock_above_200": bool(above_200[i]), "atr_pct": float(atr_pct[i]),
            }))

    for i in range(WARMUP_BARS, n - 1, BASELINE_EVERY_N_BARS):
        atr = float(df["atr_14"].iloc[i])
        if not math.isfinite(atr) or atr <= 0:
            continue
        stop, target = closes[i] - STOP_ATR_MULT * atr, closes[i] + TARGET_ATR_MULT * atr
        exit_ = resolve_exit(opens, highs, lows, closes, i + 1, "LONG", stop, target, max_hold)
        if exit_ is None:
            continue
        risk, spy_up = market.get(dates[i], (RISK_NEUTRAL, False))
        rows.append(_trade_row(symbol, "baseline_random", dates[i], i, opens, closes[i], stop, target, exit_, {
            "score": float("nan"), "market_risk": risk, "spy_above_200": spy_up,
            "stock_above_200": bool(above_200[i]), "atr_pct": float(atr_pct[i]),
        }))
    return rows, gap_skipped


Predicate = Callable[[pd.DataFrame], pd.Series]

POLICIES: dict[str, Predicate] = {
    "all": lambda d: pd.Series(True, index=d.index),
    "score>=70": lambda d: d["score"] >= 70,
    "score>=80": lambda d: d["score"] >= 80,
    "score>=80 & mkt!=RISK_OFF": lambda d: (d["score"] >= 80) & (d["market_risk"] != RISK_OFF),
    "SPY>200d": lambda d: d["spy_above_200"],
    "SPY>200d & stock>200d": lambda d: d["spy_above_200"] & d["stock_above_200"],
    "score>=70 & SPY>200d": lambda d: (d["score"] >= 70) & d["spy_above_200"],
    "score>=70 & SPY>200d & stock>200d": lambda d: (d["score"] >= 70) & d["spy_above_200"] & d["stock_above_200"],
    "score>=80 & SPY>200d & stock>200d": lambda d: (d["score"] >= 80) & d["spy_above_200"] & d["stock_above_200"],
}


def take_positions(candidates: pd.DataFrame, lock_keys: list[str]) -> pd.DataFrame:
    """One open position per lock key at a time: a new signal is only
    taken once the previous trade on the same key has exited."""
    if candidates.empty:
        return candidates
    taken = []
    for _, group in candidates.sort_values("i").groupby(lock_keys, sort=False):
        busy_until = -1
        for row in group.itertuples(index=False):
            if row.i <= busy_until:
                continue
            taken.append(row._asdict())
            busy_until = row.exit_i
    return pd.DataFrame(taken)


def summarize(trades: pd.DataFrame) -> dict:
    if trades.empty:
        return {"n": 0}
    r = trades["r_multiple"].dropna()
    ret = trades["ret_pct"]
    gains, losses = ret[ret > 0].sum(), -ret[ret <= 0].sum()
    std = float(r.std(ddof=1)) if len(r) > 1 else float("nan")
    return {
        "n": int(len(trades)),
        "win_rate": round(float((ret > 0).mean()), 4),
        "avg_ret_pct": round(float(ret.mean()), 3),
        "median_ret_pct": round(float(ret.median()), 3),
        "avg_r": round(float(r.mean()), 4) if len(r) else None,
        "t_stat_r": round(float(r.mean() / std * math.sqrt(len(r))), 2) if len(r) > 1 and std > 0 else None,
        "profit_factor": round(float(gains / losses), 3) if losses > 0 else None,
        "target_hit_rate": round(float((trades["result"] == "TARGET_HIT").mean()), 4),
        "avg_hold_bars": round(float(trades["hold_bars"].mean()), 1),
    }


@dataclass
class SplitDates:
    validation_start: str
    oos_start: str


def split_dates(all_rows: pd.DataFrame) -> SplitDates:
    dates = pd.to_datetime(all_rows["date"]).sort_values()
    span = dates.iloc[-1] - dates.iloc[0]
    return SplitDates(
        validation_start=str((dates.iloc[0] + span * 0.6).date()),
        oos_start=str((dates.iloc[0] + span * 0.8).date()),
    )


def evaluate(all_rows: pd.DataFrame) -> dict:
    splits = split_dates(all_rows)
    groups = {name: (all_rows[all_rows["strategy"] == name], ["symbol"]) for name in STRATEGIES}
    groups["combined (best per symbol)"] = (all_rows[all_rows["strategy"] != "baseline_random"], ["symbol"])
    groups["baseline_random"] = (all_rows[all_rows["strategy"] == "baseline_random"], ["symbol"])

    results = {"splits": splits.__dict__, "policies": []}
    for group_name, (rows, lock) in groups.items():
        policies = POLICIES if group_name != "baseline_random" else {
            k: v for k, v in POLICIES.items() if "score" not in k
        }
        for policy_name, predicate in policies.items():
            if rows.empty:
                continue
            chosen = rows[predicate(rows).fillna(False).astype(bool)]
            if group_name.startswith("combined"):
                # Live behavior: the highest-scoring strategy wins a symbol-day.
                chosen = chosen.sort_values("score", ascending=False).drop_duplicates(["symbol", "i"])
            taken = take_positions(chosen, lock)
            if taken.empty:
                continue
            by_period = {
                "train": summarize(taken[taken["date"] < splits.validation_start]),
                "validation": summarize(taken[(taken["date"] >= splits.validation_start) & (taken["date"] < splits.oos_start)]),
                "out_of_sample": summarize(taken[taken["date"] >= splits.oos_start]),
            }
            yearly = taken.assign(year=taken["date"].str[:4]).groupby("year")["r_multiple"].mean().round(3).to_dict()
            results["policies"].append({
                "group": group_name, "policy": policy_name, "overall": summarize(taken),
                **by_period, "avg_r_by_year": yearly,
            })

    scored = all_rows[all_rows["strategy"] != "baseline_random"]
    buckets = pd.cut(scored["score"], [0, 50, 60, 70, 80, 90, 101], right=False)
    results["score_buckets_unlocked"] = [
        {"strategy": s, "bucket": str(b), "n": int(len(g)), "avg_r": round(float(g["r_multiple"].mean()), 4)}
        for (s, b), g in scored.groupby(["strategy", buckets], observed=True) if len(g)
    ]
    return results


def to_markdown(results: dict, meta: dict) -> str:
    lines = [
        "# Strategy research",
        "",
        f"Universe: {meta['symbols_ok']} symbols with data ({meta['symbols_failed']} failed), "
        f"{meta['years']} years of daily bars, costs {settings.fee_bps}+{settings.slippage_bps} bps per side, "
        f"max hold {MAX_HOLDING_BARS_DEFAULT} bars. Gap-invalidated setups skipped: {meta['gap_skipped']}.",
        f"Splits: validation from {results['splits']['validation_start']}, out-of-sample from {results['splits']['oos_start']}.",
        "",
        "avgR = average result in units of the initial risk (entry→stop). With fixed-fractional sizing "
        "(risk 1% per trade), +0.10R ≈ +0.1% of the portfolio per trade.",
        "",
        "| group | policy | n | win% | avgR | t | PF | avg% | OOS n | OOS avgR | OOS PF |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for p in results["policies"]:
        o, oos = p["overall"], p["out_of_sample"]
        lines.append(
            f"| {p['group']} | {p['policy']} | {o['n']} | {o['win_rate']*100:.0f} | {o['avg_r']:+.3f} | "
            f"{o['t_stat_r']} | {o['profit_factor']} | {o['avg_ret_pct']:+.2f} | {oos.get('n', 0)} | "
            f"{oos.get('avg_r', float('nan')) if oos.get('n') else '—'} | {oos.get('profit_factor', '—') if oos.get('n') else '—'} |"
        )
    lines += ["", "## Score buckets (every candidate, no position lock)", "", "| strategy | score | n | avgR |", "|---|---|---|---|"]
    for b in results["score_buckets_unlocked"]:
        lines.append(f"| {b['strategy']} | {b['bucket']} | {b['n']} | {b['avg_r']:+.3f} |")
    return "\n".join(lines)


def run_research(symbols: list[str], years: int = 10, out_dir: str | Path = "research_output") -> dict:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    limit = 252 * years
    symbols = [s.upper() for s in symbols]

    with StockClient() as client:
        client.prefetch(sorted(set(symbols + [ANCHOR_SYMBOL])), "1d", limit=limit)
        spy = enrich(client.get_klines(ANCHOR_SYMBOL, "1d", limit=limit))
        market = market_context(spy)

        all_rows: list[dict] = []
        failed: dict[str, str] = {}
        gap_skipped = 0
        for n, symbol in enumerate(symbols, 1):
            try:
                df = client.get_klines(symbol, "1d", limit=limit)
            except DataUnavailable as exc:
                failed[symbol] = str(exc)
                continue
            if len(df) < WARMUP_BARS + 50:
                failed[symbol] = f"only {len(df)} bars"
                continue
            rows, skipped = symbol_trades(symbol, enrich(df), market)
            all_rows.extend(rows)
            gap_skipped += skipped
            if n % 25 == 0:
                logger.info("research: %d/%d symbols done, %d candidate trades so far", n, len(symbols), len(all_rows))

    frame = pd.DataFrame(all_rows)
    frame.to_csv(out / "candidate_trades.csv.gz", index=False)
    results = evaluate(frame)
    meta = {"symbols_ok": len(symbols) - len(failed), "symbols_failed": len(failed), "failed": failed,
            "years": years, "gap_skipped": gap_skipped, "candidates": len(frame)}
    results["meta"] = meta
    (out / "evidence.json").write_text(json.dumps(results, indent=2, default=str))
    (out / "research.md").write_text(to_markdown(results, meta))
    return results
