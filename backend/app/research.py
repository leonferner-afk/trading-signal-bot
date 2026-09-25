"""Evidence research: how would the BUY signals this bot sends have done
on real history, across the whole universe, after costs — and did they
beat buying at random with the exact same exit rules?

That last comparison is the point. The universe is written today, so it
leans toward stocks that survived and went up; any long strategy looks
good on it. A rule set only shows real timing/selection edge if it beats
the random-entry baseline on the same symbols and dates.

Mechanics mirror live trading:
  - signal at a daily close -> filled at the next session's open, fees and
    slippage both ways
  - stop/target are the levels the user is actually told
  - a gap through the stop fills at the open; a setup already invalidated
    at the next open is not taken
  - one open position per symbol at a time
  - results are split by date into train / validation / out-of-sample
  - two exit styles: "fixed" (stop + fixed target, what the bot sends
    today) and "trail" (same initial stop, no target, a trailing stop
    3 x ATR% under the highest high, moved once per day) — the latter
    lets the rare huge winner run instead of capping it
  - a portfolio simulation (max open positions, max new buys per day,
    1% risk per trade, no leverage) turns per-trade stats into what
    matters: yearly return and worst drawdown, next to SPY buy-and-hold.
"""
from __future__ import annotations

import json
import logging
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from app.backtest.engine import MAX_HOLDING_BARS_DEFAULT, Exit, net_return_pct, resolve_exit
from app.config import settings
from app.data.news_client import NewsResult
from app.data.stock_client import DataUnavailable, StockClient
from app.policy import research_policy_name
from app.regime.classifier import RISK_NEUTRAL, RISK_OFF, RISK_ON, TREND_DOWN, TREND_UP, latest_snapshot
from app.risk.risk_reward import STOP_ATR_MULT, TARGET_ATR_MULT
from app.scanner.scanner import ANCHOR_SYMBOL, enrich
from app.scoring.score import build_signal
from app.strategies import breakout, momentum, reversal

logger = logging.getLogger("tradingbot.research")

WARMUP_BARS = 210
BASELINE_EVERY_N_BARS = 5
RS_LOOKBACK = 126          # ~6 months
HIGH_LOOKBACK = 252        # ~52 weeks
TRAIL_ATR_MULT = 3.0
TRAIL_MAX_HOLD = 250
EXITS = ("fixed", "trail")
STRATEGIES = {"breakout": breakout, "momentum": momentum, "reversal": reversal}
_NO_NEWS = NewsResult(symbol="", available=False, reason="not used in research")

# (min_score, SPY>200d, stock>200d, RS percentile min, close/52w-high min)
POLICY_GRID = [
    (0, False, False, 0, 0),
    (70, False, False, 0, 0),
    (80, False, False, 0, 0),
    (0, True, True, 0, 0),
    (70, True, True, 0, 0),
    (70, True, True, 0.8, 0),
    (0, True, True, 0.8, 0),
    (0, True, True, 0.9, 0),
    (0, True, True, 0.8, 0.9),
    (70, True, True, 0.8, 0.9),
]


def _thresholds() -> tuple[float, float, float]:
    return (settings.score_exceptional_min, settings.score_high_quality_min, settings.score_watch_min)


def _session_dates(df: pd.DataFrame) -> np.ndarray:
    return df["close_time"].dt.tz_convert("America/New_York").dt.strftime("%Y-%m-%d").to_numpy()


def market_context(spy: pd.DataFrame) -> dict:
    """Session date -> (market-wide risk label, SPY above its 200-day SMA)."""
    context = {}
    for date, trend, close, sma200 in zip(_session_dates(spy), spy["trend_regime"], spy["close"], spy["sma_200"]):
        risk = RISK_ON if trend == TREND_UP else RISK_OFF if trend == TREND_DOWN else RISK_NEUTRAL
        context[date] = (risk, bool(pd.notna(sma200) and close > sma200))
    return context


def resolve_trailing_exit(opens, highs, lows, closes, entry_index: int, initial_stop: float, trail_pct: float, max_hold: int) -> Exit | None:
    """Long only. Initial stop until the trailing level (highest high since
    entry x (1 - trail_pct)) rises above it; the level is moved once per
    day after the close, like a stop you raise each evening. Gap-aware."""
    raw_entry = float(opens[entry_index])
    if raw_entry <= initial_stop:
        return None
    stop, highest, mfe, mae = initial_stop, raw_entry, 0.0, 0.0
    last_index = min(entry_index + max_hold, len(opens) - 1)
    for j in range(entry_index, last_index + 1):
        o, h, l = float(opens[j]), float(highs[j]), float(lows[j])
        mfe = max(mfe, (h - raw_entry) / raw_entry * 100)
        mae = max(mae, (raw_entry - l) / raw_entry * 100)
        if l <= stop:
            return Exit(j, min(stop, o), "TRAIL_STOP" if stop > initial_stop else "STOP_HIT", mfe, mae)
        highest = max(highest, h)
        stop = max(stop, highest * (1 - trail_pct))
    return Exit(last_index, float(closes[last_index]), "TIME_EXIT", mfe, mae)


def _row(symbol, strategy, exit_kind, dates, i, opens, planned_entry, stop, exit_, extra) -> dict:
    """R is measured against the *planned* risk (notified entry -> stop),
    because that's what the position was sized from."""
    fill = float(opens[i + 1])
    ret = net_return_pct(fill, exit_.raw_price, "LONG", settings.fee_bps, settings.slippage_bps)
    fill_with_costs = fill * (1 + (settings.fee_bps + settings.slippage_bps) / 10000.0)
    planned_risk = planned_entry - stop
    return {
        "symbol": symbol, "strategy": strategy, "exit": exit_kind, "date": dates[i], "i": i,
        "entry_date": dates[i + 1], "exit_i": exit_.index, "exit_date": dates[exit_.index],
        "result": exit_.result, "ret_pct": ret,
        "r_multiple": (ret / 100 * fill_with_costs) / planned_risk if planned_risk > 0 else float("nan"),
        "stop_dist_pct": planned_risk / planned_entry * 100, "hold_bars": exit_.index - i, **extra,
    }


def _both_exits(symbol, strategy, dates, i, arrays, planned_entry, stop, target, atr_pct, extra) -> tuple[list[dict], bool]:
    opens, highs, lows, closes = arrays
    rows = []
    fixed = resolve_exit(opens, highs, lows, closes, i + 1, "LONG", stop, target, MAX_HOLDING_BARS_DEFAULT)
    if fixed is None:
        return rows, True
    rows.append(_row(symbol, strategy, "fixed", dates, i, opens, planned_entry, stop, fixed, extra))
    trail = resolve_trailing_exit(opens, highs, lows, closes, i + 1, stop, TRAIL_ATR_MULT * atr_pct / 100, TRAIL_MAX_HOLD)
    if trail is not None:
        rows.append(_row(symbol, strategy, "trail", dates, i, opens, planned_entry, stop, trail, extra))
    return rows, False


def _long_preconditions(df: pd.DataFrame) -> dict[str, np.ndarray]:
    """Cheap necessary conditions for each strategy's LONG setup, so the
    full `generate()` only runs on bars that could possibly qualify."""
    return {
        "breakout": df["breakout_up"].fillna(False).astype(bool).to_numpy(),
        "momentum": ((df["ema_9"] > df["ema_21"]) & (df["ema_21"] > df["ema_50"])).to_numpy(),
        "reversal": (df["low"].shift(1) <= df["bb_lower"].shift(1)).fillna(False).to_numpy(),
    }


def symbol_trades(symbol: str, df: pd.DataFrame, market: dict) -> tuple[list[dict], int, pd.Series]:
    """Every LONG candidate each strategy produced on this symbol (plus
    random-entry baseline), each simulated independently under both exit
    styles. Returns (rows, gap-skipped count, 6-month return by date)."""
    n = len(df)
    arrays = tuple(df[c].to_numpy(dtype=float) for c in ("open", "high", "low", "close"))
    closes = arrays[3]
    dates = _session_dates(df)
    above_200 = (df["close"] > df["sma_200"]).to_numpy()
    atr_pct = (df["atr_14"] / df["close"] * 100).to_numpy()
    near_high = (df["close"] / df["high"].rolling(HIGH_LOOKBACK, min_periods=RS_LOOKBACK).max()).to_numpy()
    extension = (df["close"] / df["ema_21"] - 1).to_numpy()
    ret_6m = pd.Series((df["close"] / df["close"].shift(RS_LOOKBACK) - 1).to_numpy(), index=dates)

    def context(i: int, score: float) -> dict:
        risk, spy_up = market.get(dates[i], (RISK_NEUTRAL, False))
        return {"score": score, "market_risk": risk, "spy_above_200": spy_up, "stock_above_200": bool(above_200[i]),
                "atr_pct": float(atr_pct[i]), "near_high": float(near_high[i]), "extension": float(extension[i])}

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
            risk, _ = market.get(dates[i], (RISK_NEUTRAL, False))
            signal = build_signal(candidate, snapshot, _NO_NEWS, risk, tier_thresholds=thresholds)
            new, skipped = _both_exits(symbol, name, dates, i, arrays, signal.entry, signal.stop, signal.target,
                                       atr_pct[i], context(i, signal.score))
            rows += new
            gap_skipped += skipped

    for i in range(WARMUP_BARS, n - 1, BASELINE_EVERY_N_BARS):
        atr = float(df["atr_14"].iloc[i])
        if not math.isfinite(atr) or atr <= 0:
            continue
        stop, target = closes[i] - STOP_ATR_MULT * atr, closes[i] + TARGET_ATR_MULT * atr
        new, _ = _both_exits(symbol, "baseline_random", dates, i, arrays, closes[i], stop, target, atr_pct[i],
                             context(i, float("nan")))
        rows += new
    return rows, gap_skipped, ret_6m


def attach_relative_strength(rows: pd.DataFrame, returns: dict[str, pd.Series]) -> pd.DataFrame:
    """Cross-sectional percentile (0-1) of each symbol's 6-month return
    among all symbols on that date — 1.0 = strongest in the universe."""
    wide = pd.DataFrame(returns)
    pct = wide.rank(axis=1, pct=True).stack().rename("rs")
    pct.index.names = ["date", "symbol"]
    return rows.merge(pct.reset_index(), on=["date", "symbol"], how="left")


def policy_mask(d: pd.DataFrame, min_score, spy, stock, rs_min, near_high_min) -> pd.Series:
    mask = pd.Series(True, index=d.index)
    if min_score > 0:
        mask &= d["score"] >= min_score
    if spy:
        mask &= d["spy_above_200"].astype(bool)
    if stock:
        mask &= d["stock_above_200"].astype(bool)
    if rs_min > 0:
        mask &= d["rs"] >= rs_min
    if near_high_min > 0:
        mask &= d["near_high"] >= near_high_min
    return mask.fillna(False)


def take_positions(candidates: pd.DataFrame) -> pd.DataFrame:
    """One open position per symbol: a new signal is only taken once the
    previous trade on that symbol has exited."""
    if candidates.empty:
        return candidates
    taken = []
    for _, group in candidates.sort_values("i").groupby("symbol", sort=False):
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
        "big_winners_pct": round(float((ret >= 50).mean()), 4),
        "avg_hold_bars": round(float(trades["hold_bars"].mean()), 1),
    }


@dataclass
class SplitDates:
    validation_start: str
    oos_start: str


def split_dates(all_rows: pd.DataFrame) -> SplitDates:
    dates = pd.to_datetime(all_rows["date"]).sort_values()
    span = dates.iloc[-1] - dates.iloc[0]
    return SplitDates(str((dates.iloc[0] + span * 0.6).date()), str((dates.iloc[0] + span * 0.8).date()))


def _select(rows: pd.DataFrame, group: str) -> pd.DataFrame:
    if group == "combined":
        chosen = rows[~rows["strategy"].isin(["baseline_random", "reversal"])]
        # Live behavior: the highest-scoring strategy wins a symbol-day.
        return chosen.sort_values("score", ascending=False).drop_duplicates(["symbol", "i", "exit"])
    return rows[rows["strategy"] == group]


def evaluate(all_rows: pd.DataFrame) -> dict:
    splits = split_dates(all_rows)
    results = {"splits": splits.__dict__, "policies": []}
    for exit_kind in EXITS:
        rows_x = all_rows[all_rows["exit"] == exit_kind]
        for group in ("breakout", "momentum", "reversal", "combined", "baseline_random"):
            rows = _select(rows_x, group)
            for params in POLICY_GRID:
                if group == "baseline_random" and params[0] > 0:
                    continue
                taken = take_positions(rows[policy_mask(rows, *params)])
                if taken.empty:
                    continue
                results["policies"].append({
                    "group": group, "exit": exit_kind, "policy": research_policy_name(*params),
                    "overall": summarize(taken),
                    "train": summarize(taken[taken["date"] < splits.validation_start]),
                    "validation": summarize(taken[(taken["date"] >= splits.validation_start) & (taken["date"] < splits.oos_start)]),
                    "out_of_sample": summarize(taken[taken["date"] >= splits.oos_start]),
                })

    fixed = all_rows[(all_rows["exit"] == "fixed") & (all_rows["strategy"] != "baseline_random")]
    buckets = pd.cut(fixed["score"], [0, 50, 60, 70, 80, 90, 101], right=False)
    results["score_buckets_unlocked"] = [
        {"strategy": s, "bucket": str(b), "n": int(len(g)), "avg_r": round(float(g["r_multiple"].mean()), 4)}
        for (s, b), g in fixed.groupby(["strategy", buckets], observed=True) if len(g)
    ]
    return results


def simulate_portfolio(trades: pd.DataFrame, rank_col: str, start: str | None = None,
                       max_open: int = 8, max_new: int = 3, risk_pct: float = 1.0) -> dict:
    """Day-by-day portfolio: at most `max_open` positions and `max_new` new
    buys per day (best `rank_col` first), each sized so its stop loses
    `risk_pct` of current equity, never more notional than free equity.
    Equity is marked at exits only (realized), so intra-trade drawdowns
    are understated — stated in the report."""
    if start:
        trades = trades[trades["date"] >= start]
    if trades.empty:
        return {"trades": 0}
    by_date = {d: g.sort_values(rank_col, ascending=False) for d, g in trades.groupby("date")}
    exit_days = sorted(set(trades["exit_date"]))
    days = sorted(set(by_date) | set(exit_days))
    equity, peak, max_dd = 1.0, 1.0, 0.0
    open_pos: dict[str, tuple[str, float, float, float]] = {}
    taken_r, taken_ret = [], []
    for day in days:
        for sym, (exit_day, notional, ret, r) in list(open_pos.items()):
            if exit_day <= day:
                equity += notional * ret / 100
                taken_r.append(r)
                taken_ret.append(ret)
                del open_pos[sym]
        peak = max(peak, equity)
        max_dd = min(max_dd, equity / peak - 1)
        new_today = 0
        for row in by_date.get(day, pd.DataFrame()).itertuples(index=False):
            if len(open_pos) >= max_open or new_today >= max_new:
                break
            if row.symbol in open_pos or not row.stop_dist_pct > 0:
                continue
            free = equity - sum(p[1] for p in open_pos.values())
            notional = min(equity * risk_pct / 100 / (row.stop_dist_pct / 100), free)
            if notional < equity * 0.02:
                continue
            open_pos[row.symbol] = (row.exit_date, notional, row.ret_pct, row.r_multiple)
            new_today += 1
    for _, notional, ret, r in open_pos.values():  # still open at the end: marked at their last close
        equity += notional * ret / 100
        taken_r.append(r)
        taken_ret.append(ret)
    years = max((pd.Timestamp(days[-1]) - pd.Timestamp(days[0])).days / 365.25, 1e-9)
    return {
        "trades": len(taken_r),
        "trades_per_year": round(len(taken_r) / years, 1),
        "win_rate": round(float(np.mean(np.array(taken_ret) > 0)), 3) if taken_ret else None,
        "avg_r": round(float(np.nanmean(taken_r)), 3) if taken_r else None,
        "total_return_pct": round((equity - 1) * 100, 1),
        "cagr_pct": round((equity ** (1 / years) - 1) * 100, 2) if equity > 0 else -100.0,
        "max_drawdown_pct_realized": round(max_dd * 100, 1),
        "years": round(years, 1),
    }


def spy_benchmark(spy: pd.DataFrame, start: str | None = None) -> dict:
    dates = _session_dates(spy)
    closes = spy["close"].to_numpy(dtype=float)
    mask = dates >= start if start else np.ones(len(dates), bool)
    mask &= np.arange(len(dates)) >= WARMUP_BARS
    c = closes[mask]
    years = (pd.Timestamp(dates[mask][-1]) - pd.Timestamp(dates[mask][0])).days / 365.25
    dd = (c / np.maximum.accumulate(c) - 1).min()
    return {"cagr_pct": round(((c[-1] / c[0]) ** (1 / years) - 1) * 100, 2), "max_drawdown_pct": round(dd * 100, 1),
            "total_return_pct": round((c[-1] / c[0] - 1) * 100, 1), "years": round(years, 1)}


PORTFOLIO_CONFIGS = [
    # (label, group, policy params, rank column)
    ("random entries (reference)", "baseline_random", (0, False, False, 0, 0), "rand"),
    ("random entries, trend filter", "baseline_random", (0, True, True, 0, 0), "rand"),
    ("RS leaders (top 20%), trend filter", "baseline_random", (0, True, True, 0.8, 0), "rs"),
    ("RS leaders near 52w high", "baseline_random", (0, True, True, 0.8, 0.9), "rs"),
    ("signals score>=70 + trend (current live)", "combined", (70, True, True, 0, 0), "score"),
    ("signals score>=70 + trend + RS top 20%", "combined", (70, True, True, 0.8, 0), "score"),
    ("signals any score + trend + RS top 20%", "combined", (0, True, True, 0.8, 0), "rs"),
]


def portfolio_results(all_rows: pd.DataFrame, spy: pd.DataFrame, splits: dict) -> dict:
    rng = np.random.default_rng(7)
    rows = all_rows.assign(rand=rng.random(len(all_rows)))
    out = {"benchmark_spy": spy_benchmark(spy), "benchmark_spy_oos": spy_benchmark(spy, splits["oos_start"]), "configs": []}
    for label, group, params, rank in PORTFOLIO_CONFIGS:
        for exit_kind in EXITS:
            chosen = _select(rows[rows["exit"] == exit_kind], group)
            chosen = chosen[policy_mask(chosen, *params)]
            out["configs"].append({
                "label": label, "exit": exit_kind, "policy": research_policy_name(*params), "group": group,
                "full": simulate_portfolio(chosen, rank),
                "oos": simulate_portfolio(chosen, rank, start=splits["oos_start"]),
            })
    return out


def _cell(stats: dict, key: str, fmt: str) -> str:
    value = stats.get(key)
    return "—" if value is None or not stats.get("n", stats.get("trades")) else format(value, fmt)


def to_markdown(results: dict, meta: dict) -> str:
    p = results["portfolio"]
    spy, spy_oos = p["benchmark_spy"], p["benchmark_spy_oos"]
    lines = [
        "# Strategy research",
        "",
        f"Universe: {meta['symbols_ok']} symbols with data ({meta['symbols_failed']} failed), {meta['years']} years of daily bars, "
        f"costs {settings.fee_bps:g}+{settings.slippage_bps:g} bps per side. Gap-invalidated setups skipped: {meta['gap_skipped']}. "
        f"Validation from {results['splits']['validation_start']}, out-of-sample (OOS) from {results['splits']['oos_start']}.",
        "",
        "## Portfolio simulation (max 8 open, max 3 new/day, 1% risk per trade, no leverage)",
        "",
        f"SPY buy-and-hold: {spy['cagr_pct']:+.1f}%/yr, max drawdown {spy['max_drawdown_pct']:.0f}% · "
        f"OOS: {spy_oos['cagr_pct']:+.1f}%/yr, max DD {spy_oos['max_drawdown_pct']:.0f}%",
        "",
        "| rule set | exit | trades/yr | win% | avgR | CAGR | max DD* | OOS CAGR | OOS max DD* |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for c in p["configs"]:
        f, o = c["full"], c["oos"]
        if not f.get("trades"):
            continue
        lines.append(
            f"| {c['label']} | {c['exit']} | {f['trades_per_year']} | {f['win_rate'] * 100:.0f} | {f['avg_r']:+.2f} | "
            f"{f['cagr_pct']:+.1f}% | {f['max_drawdown_pct_realized']:.0f}% | "
            + (f"{o['cagr_pct']:+.1f}% | {o['max_drawdown_pct_realized']:.0f}% |" if o.get("trades") else "— | — |")
        )
    lines += ["", "*Drawdown measured on realized equity (at exits), so it understates intra-trade drawdown.", "",
              "## Per-trade results (one position per symbol)", "",
              "| group | exit | policy | n | win% | avgR | t | PF | ≥+50% | OOS n | OOS avgR | OOS PF |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for row in results["policies"]:
        o, oos = row["overall"], row["out_of_sample"]
        lines.append(
            f"| {row['group']} | {row['exit']} | {row['policy']} | {o['n']} | {o['win_rate'] * 100:.0f} | {o['avg_r']:+.3f} | "
            f"{o['t_stat_r']} | {o['profit_factor']} | {o['big_winners_pct'] * 100:.1f}% | {oos.get('n', 0)} | "
            f"{_cell(oos, 'avg_r', '+.3f')} | {_cell(oos, 'profit_factor', '.2f')} |"
        )
    lines += ["", "## Score buckets (fixed exit, every candidate, no position lock)", "", "| strategy | score | n | avgR |", "|---|---|---|---|"]
    for b in results["score_buckets_unlocked"]:
        lines.append(f"| {b['strategy']} | {b['bucket']} | {b['n']} | {b['avg_r']:+.3f} |")
    return "\n".join(lines)


def run_research(symbols: list[str], years: int = 10, out_dir: str | Path = "research_output") -> dict:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    limit = 252 * years
    symbols = [s.upper() for s in symbols if s.upper() != ANCHOR_SYMBOL]

    with StockClient() as client:
        client.prefetch(sorted(set(symbols + [ANCHOR_SYMBOL])), "1d", limit=limit)
        spy = enrich(client.get_klines(ANCHOR_SYMBOL, "1d", limit=limit))
        market = market_context(spy)

        all_rows: list[dict] = []
        returns: dict[str, pd.Series] = {}
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
            rows, skipped, ret_6m = symbol_trades(symbol, enrich(df), market)
            all_rows.extend(rows)
            returns[symbol] = ret_6m
            gap_skipped += skipped
            if n % 25 == 0:
                logger.info("research: %d/%d symbols done, %d candidate rows so far", n, len(symbols), len(all_rows))

    frame = attach_relative_strength(pd.DataFrame(all_rows), returns)
    frame.to_csv(out / "candidate_trades.csv.gz", index=False)
    results = evaluate(frame)
    results["portfolio"] = portfolio_results(frame, spy, results["splits"])
    meta = {"symbols_ok": len(symbols) - len(failed), "symbols_failed": len(failed), "failed": failed,
            "years": years, "gap_skipped": gap_skipped, "candidates": int((frame["exit"] == "fixed").sum())}
    results["meta"] = meta
    (out / "evidence.json").write_text(json.dumps(results, indent=2, default=str))
    (out / "research.md").write_text(to_markdown(results, meta))
    return results
