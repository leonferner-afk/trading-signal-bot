"""Evidence research: would the BUY signals this bot sends have made money
on real history, after realistic costs, compared with (a) buying random
stocks from the same list on the same days and (b) just holding SPY?

Built to be hard to fool:
  - signal at a daily close -> filled at the next session's open; stop and
    target are the levels the user is told; a gap through the stop fills at
    the open; a setup already invalidated at the next open is not taken
  - rows keep raw fill/exit prices, so every statistic can be recomputed at
    any cost level; the primary level (COST_BPS_PRIMARY per side) reflects a
    Swedish retail account trading US stocks (courtage + FX conversion +
    slippage), with a sensitivity grid around it
  - per-trade t-statistics are computed over MONTHLY averages, because trades
    opened in the same month share the same market and are not independent
  - every rule is compared with the random-entry baseline under the same
    filters (the only fair test of timing/selection edge on a hand-built
    universe), month by month
  - portfolio simulation is marked to market DAILY, caps every position at
    MAX_POSITION_PCT of equity, never uses leverage, and is compared with
    40 simulations that pick randomly from the same eligible candidates, so
    "the ranking adds value" is tested rather than assumed
  - everything is also run on LARGECAP_2015 alone — stocks chosen by size a
    decade ago, not by what happened since — as a control for the
    survivorship / hindsight bias of a universe written today
  - the train / validation / out-of-sample split is by date; the live
    configuration must be chosen on train+validation only
"""
from __future__ import annotations

import json
import logging
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from app import rockets as rk
from app import rotation as rot
from app.backtest.engine import MAX_HOLDING_BARS_DEFAULT, resolve_exit
from app.config import settings
from app.data.news_client import NewsResult
from app.data.stock_client import DataUnavailable, StockClient
# Row filters shared with the live policy: below MIN_ATR_PCT a "mover" isn't
# moving (e.g. a pending cash takeover); tighter stops than MIN_STOP_DIST_PCT
# are noise and blow up position sizes.
from app.policy import MAX_STOP_DIST_PCT, MIN_ATR_PCT, MIN_STOP_DIST_PCT, research_policy_name
from app.regime.classifier import RISK_NEUTRAL, RISK_OFF, RISK_ON, TREND_DOWN, TREND_UP, latest_snapshot
from app.risk.risk_reward import STOP_ATR_MULT, TARGET_ATR_MULT
from app.scanner.scanner import ANCHOR_SYMBOL, enrich
from app.scoring.score import build_signal
from app.strategies import breakout, momentum
from app.universe import LARGECAP_2015

logger = logging.getLogger("tradingbot.research")

WARMUP_BARS = 210
BASELINE_EVERY_N_BARS = 5
RS_LOOKBACK = 126           # ~6 months
HIGH_LOOKBACK = 252         # ~52 weeks
WIDE_STOP_ATR_MULT = 2.5
COST_BPS_PRIMARY = 20.0     # per side: ~0.15% courtage from a USD account + ~0.05% slippage
COST_BPS_GRID = (20.0, 40.0, 70.0)   # 40 = trading from a SEK account (FX conversion every trade)
MAX_OPEN = 8
MAX_NEW_PER_DAY = 3
RISK_PCT = 1.0
MAX_POSITION_PCT = 25.0
RANDOM_RUNS = 40
STRATEGIES = {"breakout": breakout, "momentum": momentum}
EXITS = ("fixed", "wide")
_NO_NEWS = NewsResult(symbol="", available=False, reason="not used in research")

# (min_score, SPY>200d, stock>200d, RS percentile min, close/52w-high min)
POLICY_GRID = [
    (0, False, False, 0, 0),
    (0, True, True, 0, 0),
    (0, True, True, 0.8, 0),
    (0, True, True, 0.8, 0.9),
    (70, True, True, 0, 0),
    (70, True, True, 0.8, 0),
]

# (label, candidate group, policy params, rank column)
PORTFOLIO_CONFIGS = [
    ("random picks (reference)", "baseline_random", (0, False, False, 0, 0), "rand"),
    ("random picks, trend filter", "baseline_random", (0, True, True, 0, 0), "rand"),
    ("RS leaders, trend filter", "baseline_random", (0, True, True, 0.8, 0), "rs"),
    ("RS leaders near 52w high", "baseline_random", (0, True, True, 0.8, 0.9), "rs"),
    ("signals score>=70, trend", "combined", (70, True, True, 0, 0), "score"),
    ("signals score>=70, trend, RS top 20%", "combined", (70, True, True, 0.8, 0), "rs"),
    ("signals, trend, RS top 20%", "combined", (0, True, True, 0.8, 0), "rs"),
    ("signals, trend, RS top 20%, near 52w high", "combined", (0, True, True, 0.8, 0.9), "rs"),
]


ROTATION_GRID = [
    rot.RotationParams(max_positions=n, exit_rs=x, regime_exit=r, stop_pct=sp, max_new_per_day=MAX_NEW_PER_DAY)
    for n in (5, 8) for x in (0.5, 0.7) for r in (False, True) for sp in (0.0, 0.2)
] + [
    # Three well-documented refinements of the live rule, added as a set
    # before any of them was tested (kept few on purpose: every extra
    # variant raises the odds of a lucky winner).
    rot.RotationParams(max_positions=8, exit_rs=0.5, max_new_per_day=MAX_NEW_PER_DAY, momentum="12-1"),
    rot.RotationParams(max_positions=8, exit_rs=0.5, max_new_per_day=8, rebalance="monthly"),
    rot.RotationParams(max_positions=8, exit_rs=0.5, max_new_per_day=MAX_NEW_PER_DAY, momentum="6m_vol"),
]
ROTATION_RANDOM_RUNS = 20


def _session_dates(df: pd.DataFrame) -> np.ndarray:
    return df["close_time"].dt.tz_convert("America/New_York").dt.strftime("%Y-%m-%d").to_numpy()


def market_context(spy: pd.DataFrame) -> dict:
    """Session date -> (market-wide risk label, SPY above its 200-day SMA)."""
    context = {}
    for date, trend, close, sma200 in zip(_session_dates(spy), spy["trend_regime"], spy["close"], spy["sma_200"]):
        risk = RISK_ON if trend == TREND_UP else RISK_OFF if trend == TREND_DOWN else RISK_NEUTRAL
        context[date] = (risk, bool(pd.notna(sma200) and close > sma200))
    return context


def net_return_pct(fill, exit_raw, cost_bps):
    c = cost_bps / 10000.0
    return (exit_raw * (1 - c) / (fill * (1 + c)) - 1) * 100


def r_multiple(fill, exit_raw, planned_entry, stop, cost_bps):
    """P&L per share in units of the *planned* risk (notified entry -> stop),
    since that's what the position was sized from."""
    c = cost_bps / 10000.0
    return (exit_raw * (1 - c) - fill * (1 + c)) / (planned_entry - stop)


def _long_preconditions(df: pd.DataFrame) -> dict[str, np.ndarray]:
    """Cheap necessary conditions for each strategy's LONG setup, so the
    full `generate()` only runs on bars that could possibly qualify."""
    return {
        "breakout": df["breakout_up"].fillna(False).astype(bool).to_numpy(),
        "momentum": ((df["ema_9"] > df["ema_21"]) & (df["ema_21"] > df["ema_50"])).to_numpy(),
    }


def symbol_rows(symbol: str, df: pd.DataFrame, market: dict) -> tuple[list[dict], int, pd.Series]:
    """Every LONG candidate each strategy produced on this symbol, plus the
    random-entry baseline, each simulated independently under both exit
    styles. Returns (rows, gap-skipped count, 6-month return by date)."""
    n = len(df)
    opens, highs, lows, closes = (df[c].to_numpy(dtype=float) for c in ("open", "high", "low", "close"))
    atr = df["atr_14"].to_numpy(dtype=float)
    dates = _session_dates(df)
    above_200 = (df["close"] > df["sma_200"]).to_numpy()
    atr_pct = atr / closes * 100
    near_high = (df["close"] / df["high"].rolling(HIGH_LOOKBACK, min_periods=RS_LOOKBACK).max()).to_numpy()
    ret_6m = pd.Series((df["close"] / df["close"].shift(RS_LOOKBACK) - 1).to_numpy(), index=dates)
    rows: list[dict] = []
    gap_skipped = 0

    def add(strategy: str, i: int, planned_entry: float, stop: float, target: float, score: float) -> None:
        nonlocal gap_skipped
        if not (atr_pct[i] >= MIN_ATR_PCT):
            return
        risk, spy_up = market.get(dates[i], (RISK_NEUTRAL, False))
        context = {"score": score, "market_risk": risk, "spy_above_200": spy_up, "stock_above_200": bool(above_200[i]),
                   "atr_pct": float(atr_pct[i]), "near_high": float(near_high[i])}
        for exit_kind, s in (("fixed", stop), ("wide", planned_entry - WIDE_STOP_ATR_MULT * atr[i])):
            dist = (planned_entry - s) / planned_entry * 100
            if not MIN_STOP_DIST_PCT <= dist <= MAX_STOP_DIST_PCT:
                continue
            exit_ = resolve_exit(opens, highs, lows, closes, i + 1, "LONG", s, target, MAX_HOLDING_BARS_DEFAULT)
            if exit_ is None:
                gap_skipped += exit_kind == "fixed"
                continue
            rows.append({
                "symbol": symbol, "strategy": strategy, "exit": exit_kind, "date": dates[i], "i": i,
                "entry_date": dates[i + 1], "exit_i": exit_.index, "exit_date": dates[exit_.index],
                "result": exit_.result, "fill": float(opens[i + 1]), "exit_raw": float(exit_.raw_price),
                "planned_entry": planned_entry, "stop": s, "stop_dist_pct": dist, "hold_bars": exit_.index - i,
                **context,
            })

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
            signal = build_signal(candidate, snapshot, _NO_NEWS, risk, tier_thresholds=(
                settings.score_exceptional_min, settings.score_high_quality_min, settings.score_watch_min))
            add(name, i, signal.entry, signal.stop, signal.target, signal.score)

    for i in range(WARMUP_BARS, n - 1, BASELINE_EVERY_N_BARS):
        if math.isfinite(atr[i]) and atr[i] > 0:
            add("baseline_random", i, closes[i], closes[i] - STOP_ATR_MULT * atr[i], closes[i] + TARGET_ATR_MULT * atr[i], float("nan"))
    return rows, gap_skipped, ret_6m


def attach_relative_strength(rows: pd.DataFrame, returns: dict[str, pd.Series], column: str = "rs") -> pd.DataFrame:
    """Cross-sectional percentile (0-1) of each symbol's 6-month return
    among `returns`' symbols on that date — 1.0 = strongest."""
    wide = pd.DataFrame(returns)
    pct = wide.rank(axis=1, pct=True).stack().rename(column)
    pct.index.names = ["date", "symbol"]
    return rows.merge(pct.reset_index(), on=["date", "symbol"], how="left")


def with_costs(rows: pd.DataFrame, cost_bps: float) -> pd.DataFrame:
    return rows.assign(
        ret_pct=net_return_pct(rows["fill"], rows["exit_raw"], cost_bps),
        r_multiple=r_multiple(rows["fill"], rows["exit_raw"], rows["planned_entry"], rows["stop"], cost_bps),
    )


def policy_mask(d: pd.DataFrame, min_score, spy, stock, rs_min, near_high_min, rs_col: str = "rs") -> pd.Series:
    mask = pd.Series(True, index=d.index)
    if min_score > 0:
        mask &= d["score"] >= min_score
    if spy:
        mask &= d["spy_above_200"].astype(bool)
    if stock:
        mask &= d["stock_above_200"].astype(bool)
    if rs_min > 0:
        mask &= d[rs_col] >= rs_min
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


def _monthly_t(values: pd.Series, months: pd.Series) -> tuple[float | None, int]:
    by_month = values.groupby(months).mean().dropna()
    if len(by_month) < 3 or by_month.std(ddof=1) == 0:
        return None, len(by_month)
    return float(by_month.mean() / by_month.std(ddof=1) * math.sqrt(len(by_month))), len(by_month)


def summarize(trades: pd.DataFrame) -> dict:
    if trades.empty:
        return {"n": 0}
    r = trades["r_multiple"]
    ret = trades["ret_pct"]
    gains, losses = ret[ret > 0].sum(), -ret[ret <= 0].sum()
    t_month, months = _monthly_t(r, trades["date"].str[:7])
    return {
        "n": int(len(trades)),
        "months": months,
        "win_rate": round(float((ret > 0).mean()), 4),
        "avg_ret_pct": round(float(ret.mean()), 3),
        "avg_r": round(float(r.mean()), 4),
        "median_r": round(float(r.median()), 4),
        "t_month": round(t_month, 2) if t_month is not None else None,
        "profit_factor": round(float(gains / losses), 3) if losses > 0 else None,
        "big_winners_pct": round(float((ret >= 50).mean()), 4),
        "avg_hold_bars": round(float(trades["hold_bars"].mean()), 1),
    }


def excess_vs_baseline(policy: pd.DataFrame, baseline: pd.DataFrame) -> dict:
    """Month-by-month difference in mean R between the rule's trades and
    random entries under the same non-score filters."""
    if policy.empty or baseline.empty:
        return {"months": 0}
    p = policy.groupby(policy["date"].str[:7])["r_multiple"].mean()
    b = baseline.groupby(baseline["date"].str[:7])["r_multiple"].mean()
    diff = (p - b).dropna()
    if len(diff) < 3 or diff.std(ddof=1) == 0:
        return {"months": int(len(diff))}
    return {"months": int(len(diff)), "avg_excess_r": round(float(diff.mean()), 4),
            "t_month": round(float(diff.mean() / diff.std(ddof=1) * math.sqrt(len(diff))), 2)}


@dataclass
class SplitDates:
    validation_start: str
    oos_start: str


def split_dates(all_rows: pd.DataFrame) -> SplitDates:
    dates = pd.to_datetime(all_rows["date"]).sort_values()
    span = dates.iloc[-1] - dates.iloc[0]
    return SplitDates(str((dates.iloc[0] + span * 0.6).date()), str((dates.iloc[0] + span * 0.8).date()))


def select_group(rows: pd.DataFrame, group: str) -> pd.DataFrame:
    if group == "combined":
        chosen = rows[rows["strategy"].isin(list(STRATEGIES))]
        # Live behavior: the highest-scoring strategy wins a symbol-day.
        return chosen.sort_values("score", ascending=False).drop_duplicates(["symbol", "i", "exit"])
    return rows[rows["strategy"] == group]


def evaluate_trades(rows: pd.DataFrame, splits: SplitDates, rs_col: str) -> list[dict]:
    out = []
    for exit_kind in EXITS:
        rx = rows[rows["exit"] == exit_kind]
        baseline = select_group(rx, "baseline_random")
        for group in ("breakout", "momentum", "combined", "baseline_random"):
            grp = select_group(rx, group)
            for params in POLICY_GRID:
                if group == "baseline_random" and params[0] > 0:
                    continue
                taken = take_positions(grp[policy_mask(grp, *params, rs_col=rs_col)])
                if taken.empty:
                    continue
                base_taken = take_positions(baseline[policy_mask(baseline, 0, *params[1:], rs_col=rs_col)])
                in_sample = taken[taken["date"] < splits.oos_start]
                out.append({
                    "group": group, "exit": exit_kind, "policy": research_policy_name(*params),
                    "overall": summarize(taken),
                    "train_val": summarize(in_sample),
                    "out_of_sample": summarize(taken[taken["date"] >= splits.oos_start]),
                    "excess_vs_random": excess_vs_baseline(taken, base_taken) if group != "baseline_random" else None,
                    "avg_r_by_year": taken.groupby(taken["date"].str[:4])["r_multiple"].mean().round(3).to_dict(),
                })
    return out


class PriceBook:
    """Daily closes per symbol, for marking open positions to market."""

    def __init__(self, closes: dict[str, pd.Series]):
        self._closes = {s: dict(zip(c.index, c.to_numpy(dtype=float))) for s, c in closes.items()}

    def close(self, symbol: str, date: str, fallback: float) -> float:
        return self._closes.get(symbol, {}).get(date, fallback)


def simulate_portfolio(trades: pd.DataFrame, rank_col: str, calendar: list[str], prices: PriceBook, cost_bps: float,
                       start: str | None = None, end: str | None = None, rng: np.random.Generator | None = None,
                       weight: float | None = None, max_open: int = MAX_OPEN, max_new: int = MAX_NEW_PER_DAY) -> dict:
    """Day-by-day portfolio marked to market at every close.

    Each candidate row is a trade that would be entered at the open of
    `entry_date`; on each day the best `rank_col` candidates are bought
    (at most MAX_NEW_PER_DAY, at most MAX_OPEN held, one position per
    symbol), each sized so hitting its stop loses RISK_PCT of equity,
    capped at MAX_POSITION_PCT of equity and at free cash. `rng` replaces
    the ranking with a random order (the randomization test)."""
    c = cost_bps / 10000.0
    days = [d for d in calendar if (start is None or d >= start) and (end is None or d < end)]
    if trades.empty or len(days) < 20:
        return {"trades": 0}
    trades = trades[(trades["entry_date"] >= days[0]) & (trades["entry_date"] <= days[-1])]
    if rng is not None:
        trades = trades.assign(_rank=rng.random(len(trades)))
        rank_col = "_rank"
    # Sort once (day ascending, rank descending, NaN rank last) and walk plain
    # arrays — this runs hundreds of times per research job.
    trades = trades.sort_values(["entry_date", rank_col], ascending=[True, False], kind="mergesort", na_position="last")
    t_day = trades["entry_date"].to_numpy()
    t_sym = trades["symbol"].to_numpy()
    t_fill = trades["fill"].to_numpy(dtype=float)
    t_exit_date = trades["exit_date"].to_numpy()
    t_exit_raw = trades["exit_raw"].to_numpy(dtype=float)
    t_stop = trades["stop_dist_pct"].to_numpy(dtype=float)
    t_r = trades["r_multiple"].to_numpy(dtype=float)
    t_ret = trades["ret_pct"].to_numpy(dtype=float)
    day_keys, day_first = np.unique(t_day, return_index=True)
    day_slices = {d: (int(a), int(b)) for d, a, b in zip(day_keys, day_first, list(day_first[1:]) + [len(t_day)])}

    cash, equity = 1.0, 1.0
    positions: dict[str, dict] = {}
    curve, invested_share = [], []
    results_r, results_ret = [], []
    for day in days:
        new_today = 0
        lo, hi = day_slices.get(day, (0, 0))
        for k in range(lo, hi):
            if len(positions) >= max_open or new_today >= max_new:
                break
            symbol = t_sym[k]
            if symbol in positions:
                continue
            notional = (min(equity * weight, cash) if weight is not None
                        else min(equity * RISK_PCT / t_stop[k], equity * MAX_POSITION_PCT / 100, cash))
            if notional < equity * 0.02:
                continue
            cash -= notional
            positions[symbol] = {"shares": notional / (t_fill[k] * (1 + c)), "exit_date": t_exit_date[k],
                                 "exit_raw": t_exit_raw[k], "last": t_fill[k], "r": t_r[k], "ret": t_ret[k]}
            new_today += 1
        for symbol in [s for s, p in positions.items() if p["exit_date"] <= day]:
            p = positions.pop(symbol)
            cash += p["shares"] * p["exit_raw"] * (1 - c)
            results_r.append(p["r"])
            results_ret.append(p["ret"])
        market_value = 0.0
        for symbol, p in positions.items():
            p["last"] = prices.close(symbol, day, p["last"])
            market_value += p["shares"] * p["last"]
        equity = cash + market_value
        curve.append(equity)
        invested_share.append(market_value / equity if equity > 0 else 0.0)
    for p in positions.values():  # still open at the end: marked at their last close
        results_r.append(p["r"])
        results_ret.append(p["ret"])
    return _curve_stats(np.array(curve), len(days), results_r, results_ret, float(np.mean(invested_share)))


def _curve_stats(curve: np.ndarray, n_days: int, results_r, results_ret, exposure: float | None) -> dict:
    years = n_days / 252.0
    daily = np.diff(curve) / curve[:-1]
    dd = float((curve / np.maximum.accumulate(curve) - 1).min())
    vol = float(daily.std(ddof=1) * math.sqrt(252)) if len(daily) > 1 else float("nan")
    stats = {
        "cagr_pct": round((curve[-1] ** (1 / years) - 1) * 100, 2) if curve[-1] > 0 else -100.0,
        "max_drawdown_pct": round(dd * 100, 1),
        "vol_pct": round(vol * 100, 1),
        "sharpe": round(float(daily.mean() / daily.std(ddof=1) * math.sqrt(252)), 2) if len(daily) > 1 and daily.std() > 0 else None,
        "years": round(years, 1),
    }
    if results_r is not None:
        stats.update({
            "trades": len(results_r),
            "trades_per_year": round(len(results_r) / years, 1),
            "win_rate": round(float(np.mean(np.array(results_ret) > 0)), 3) if results_ret else None,
            "avg_r": round(float(np.nanmean(results_r)), 3) if results_r else None,
            "exposure_pct": round(exposure * 100, 0),
        })
    return stats


def benchmark(closes: pd.Series, start: str | None = None, end: str | None = None) -> dict:
    c = closes[(closes.index >= (start or "")) & ((closes.index < end) if end else True)]
    return _curve_stats(c.to_numpy(dtype=float) / float(c.iloc[0]), len(c), None, None, None)


def portfolio_results(rows: pd.DataFrame, spy_closes: pd.Series, prices: PriceBook, splits: SplitDates,
                      rs_col: str, cost_bps: float, exit_kind: str = "fixed", random_runs: int = RANDOM_RUNS) -> list[dict]:
    first = str(rows["entry_date"].min())
    calendar = [d for d in spy_closes.index if d >= first]
    rng = np.random.default_rng(7)
    rows = with_costs(rows[rows["exit"] == exit_kind], cost_bps).assign(rand=lambda d: rng.random(len(d)))
    out = []
    for label, group, params, rank in PORTFOLIO_CONFIGS:
        eligible = select_group(rows, group)
        eligible = eligible[policy_mask(eligible, *params, rs_col=rs_col)]
        if rank == "rs":
            eligible = eligible.assign(rs=eligible[rs_col])
        full = simulate_portfolio(eligible, rank, calendar, prices, cost_bps)
        entry = {
            "label": label, "group": group, "policy": research_policy_name(*params), "rank": rank,
            "full": full,
            "train_val": simulate_portfolio(eligible, rank, calendar, prices, cost_bps, end=splits.oos_start),
            "oos": simulate_portfolio(eligible, rank, calendar, prices, cost_bps, start=splits.oos_start),
        }
        if rank != "rand" and random_runs and full.get("trades"):
            sims = [simulate_portfolio(eligible, rank, calendar, prices, cost_bps, rng=np.random.default_rng(100 + k))
                    for k in range(random_runs)]
            random_cagr = np.array([s["cagr_pct"] for s in sims if s.get("trades")])
            entry["random_rank_median_cagr"] = round(float(np.median(random_cagr)), 2)
            entry["rank_percentile"] = round(float((random_cagr < full["cagr_pct"]).mean()), 2)
        out.append(entry)
    return out


def segment_stats(sim: dict, start: str | None = None, end: str | None = None) -> dict:
    """Curve and trade statistics of one simulation restricted to [start, end)."""
    d = np.array(sim["dates"])
    m = np.ones(len(d), bool)
    if start:
        m &= d >= start
    if end:
        m &= d < end
    if m.sum() < 20:
        return {"trades": 0}
    curve = sim["curve"][m] / sim["curve"][m][0]
    stats = _curve_stats(curve, int(m.sum()), None, None, None)
    trades = [t for t in sim["trades"] if (not start or t["entry"] >= start) and (not end or t["entry"] < end)]
    rets = np.array([t["ret_pct"] for t in trades])
    stats.update({
        "trades": len(trades),
        "trades_per_year": round(len(trades) / stats["years"], 1) if stats["years"] else None,
        "win_rate": round(float((rets > 0).mean()), 3) if len(rets) else None,
        "avg_trade_pct": round(float(rets.mean()), 2) if len(rets) else None,
        "avg_days": round(float(np.mean([t["days"] for t in trades])), 1) if trades else None,
        "exposure_pct": round(float(sim["exposure"][m].mean()) * 100, 0),
    })
    return stats


def yearly_returns(dates: list[str], curve: np.ndarray) -> dict[str, float]:
    """Calendar-year return (%) from a daily equity curve (partial first/last years included)."""
    s = pd.Series(np.asarray(curve, dtype=float), index=pd.Index(dates).str[:4])
    out, prev = {}, None
    for year, values in s.groupby(level=0, sort=True):
        start = prev if prev is not None else values.iloc[0]
        out[year] = round((values.iloc[-1] / start - 1) * 100, 1)
        prev = values.iloc[-1]
    return out


# Pre-registered selection rule for the live rotation (decided before the
# hindsight-free results were seen). Evaluated on the 2015 large-cap group,
# train+validation period only; OOS is reported, never used to choose.
GATE_MIN_RANDOM_PERCENTILE = 0.9
GATE_MAX_EXTRA_DRAWDOWN_PCT = 10.0


def rotation_gates(block: dict) -> list[dict]:
    spy_tv, spy = block["spy_train_val"], block["spy"]
    out = []
    for c in block["configs"]:
        tv, full, wt = c["train_val"], c["full"], c.get("without_top") or {}
        checks = {
            "train_val_sharpe_beats_spy": (tv.get("sharpe") or -9) > (spy_tv.get("sharpe") or 0),
            "ranking_beats_random": (c.get("rank_percentile") or 0) >= GATE_MIN_RANDOM_PERCENTILE,
            "without_best_stock_beats_spy": (wt.get("cagr_pct") if wt else -99) >= spy["cagr_pct"],
            "drawdown_close_to_spy": full["max_drawdown_pct"] >= spy["max_drawdown_pct"] - GATE_MAX_EXTRA_DRAWDOWN_PCT,
        }
        out.append({"name": c["name"], "passes": all(checks.values()), "checks": checks,
                    "train_val_sharpe": tv.get("sharpe"), "trades_per_year": full.get("trades_per_year")})
    return out


def select_rotation(block: dict | None) -> dict:
    if not block:
        return {"chosen": None, "gates": []}
    gates = rotation_gates(block)
    passing = [g for g in gates if g["passes"]]
    if not passing:
        return {"chosen": None, "gates": gates}
    best = max(g["train_val_sharpe"] for g in passing)
    # Within 0.03 Sharpe of the best, prefer fewer trades (less cost, less work).
    near = [g for g in passing if g["train_val_sharpe"] >= best - 0.03]
    chosen = min(near, key=lambda g: (g["trades_per_year"] or 0, -g["train_val_sharpe"]))
    return {"chosen": chosen["name"], "gates": gates}


def rotation_results(panel: rot.Panel, splits: SplitDates, spy_closes: pd.Series,
                     random_runs: int = ROTATION_RANDOM_RUNS, rebuild=None) -> dict:
    """`rebuild(symbols)` builds the panel for a subset of symbols — used to
    re-run each rule set without its single most profitable stock (an edge
    that rests on one name is not an edge)."""
    if len(panel.dates) < rot.RS_LOOKBACK + 200 + 60 or not panel.symbols:
        return None
    configs = []
    first = None
    for params in ROTATION_GRID:
        sim = rot.simulate(panel, params, COST_BPS_PRIMARY)
        first = first or sim["dates"][0]
        entry = {
            "name": params.name, "params": params.__dict__,
            "full": segment_stats(sim),
            "train_val": segment_stats(sim, end=splits.oos_start),
            "oos": segment_stats(sim, start=splits.oos_start),
            "cost_sensitivity": {f"{b:g}": segment_stats(rot.simulate(panel, params, b)) for b in COST_BPS_GRID if b != COST_BPS_PRIMARY},
            "by_year": yearly_returns(sim["dates"], sim["curve"]),
        }
        if rebuild is not None and sim["trades"]:
            by_symbol: dict[str, float] = {}
            for t in sim["trades"]:
                by_symbol[t["symbol"]] = by_symbol.get(t["symbol"], 0.0) + t["ret_pct"]
            top = max(by_symbol, key=by_symbol.get)
            without = rot.simulate(rebuild([x for x in panel.symbols if x != top]), params, COST_BPS_PRIMARY)
            entry["without_top"] = {"symbol": top, **{k: v for k, v in segment_stats(without).items()
                                                        if k in ("cagr_pct", "max_drawdown_pct", "sharpe")}}
        if random_runs:
            sims = [rot.simulate(panel, params, COST_BPS_PRIMARY, rng=np.random.default_rng(500 + k)) for k in range(random_runs)]
            rand_full = np.array([segment_stats(x)["cagr_pct"] for x in sims])
            rand_tv = np.array([segment_stats(x, end=splits.oos_start).get("sharpe") or 0.0 for x in sims])
            entry["random_median_cagr"] = round(float(np.median(rand_full)), 2)
            entry["rank_percentile"] = round(float((rand_full < entry["full"]["cagr_pct"]).mean()), 2)
            entry["rank_percentile_train_val_sharpe"] = round(float((rand_tv < (entry["train_val"].get("sharpe") or 0.0)).mean()), 2)
        configs.append(entry)
    start_i = panel.dates.index(first)
    ew = {"dates": panel.dates[start_i:], "curve": rot.equal_weight_benchmark(panel, start_i),
          "exposure": np.ones(len(panel.dates) - start_i), "trades": []}
    return {
        "start": first,
        "spy": benchmark(spy_closes, first), "spy_train_val": benchmark(spy_closes, first, splits.oos_start),
        "spy_oos": benchmark(spy_closes, splits.oos_start),
        "equal_weight": segment_stats(ew), "equal_weight_train_val": segment_stats(ew, end=splits.oos_start),
        "equal_weight_oos": segment_stats(ew, start=splits.oos_start),
        "spy_by_year": yearly_returns(list(spy_closes.index[spy_closes.index >= first]),
                                      spy_closes[spy_closes.index >= first].to_numpy(dtype=float)),
        "equal_weight_by_year": yearly_returns(ew["dates"], ew["curve"]),
        "configs": configs,
    }


def rocket_results(raw: dict[str, pd.DataFrame], largecap: set[str], spy_closes: pd.Series, prices: PriceBook,
                   splits: SplitDates, earnings: dict[str, pd.DataFrame] | None = None) -> dict:
    """Every rocket variant: per-trade vs random entries in the same stocks,
    an equal-weight portfolio (10 slots of 10%), the 2015 large-cap control,
    a without-top-3-stocks rerun and the pre-registered gates."""
    dates = {s: _session_dates(df) for s, df in raw.items()}
    frames = {s: df for s, df in raw.items() if {"high", "volume"} <= set(df.columns)}
    first = min(d[21] for d in dates.values() if len(d) > 21)
    calendar = [d for d in spy_closes.index if d >= first]
    spy = {"full": benchmark(spy_closes, first), "train_val": benchmark(spy_closes, first, splits.oos_start),
           "oos": benchmark(spy_closes, splits.oos_start)}
    baselines: dict[float, pd.DataFrame] = {}
    variants = []

    def portfolio(rows: pd.DataFrame, start=None, end=None, rng=None) -> dict:
        return simulate_portfolio(rows, "volume_ratio", calendar, prices, COST_BPS_PRIMARY, start, end, rng,
                                  weight=rk.WEIGHT, max_open=rk.MAX_OPEN, max_new=rk.MAX_NEW_PER_DAY)

    def evaluate(name: str, param_dict: dict, rows: list[dict], base: pd.DataFrame) -> dict:
        if not rows or base.empty:
            return {"name": name, "trades": {"n": 0}}
        t = rk.with_costs(pd.DataFrame(rows), COST_BPS_PRIMARY)
        tv, oos = t[t["date"] < splits.oos_start], t[t["date"] >= splits.oos_start]
        base_tv = base[base["date"] < splits.oos_start]
        lc, base_lc = t[t["symbol"].isin(largecap)], base[base["symbol"].isin(largecap)]
        top3 = t.groupby("symbol")["ret_pct"].sum().nlargest(3).index.tolist()
        entry = {
            "name": name, "params": param_dict,
            "trades": rk.trade_summary(t), "trades_train_val": rk.trade_summary(tv), "trades_oos": rk.trade_summary(oos),
            "random_entries": rk.trade_summary(base),
            "excess_all": rk.monthly_excess(t, base), "excess_train_val": rk.monthly_excess(tv, base_tv),
            "excess_largecap": rk.monthly_excess(lc, base_lc), "largecap_trades": rk.trade_summary(lc),
            "portfolio": portfolio(t), "portfolio_train_val": portfolio(t, end=splits.oos_start),
            "portfolio_oos": portfolio(t, start=splits.oos_start),
            "random_portfolio": portfolio(base.assign(volume_ratio=np.random.default_rng(11).random(len(base)))),
            "without_top3": {"symbols": top3, **{k: v for k, v in portfolio(t[~t["symbol"].isin(top3)]).items()
                                                 if k in ("cagr_pct", "sharpe", "max_drawdown_pct")}},
            "by_year": t.groupby(t["date"].str[:4])["ret_pct"].mean().round(2).to_dict(),
        }
        entry["gates"] = rk.rocket_gates(entry, spy["train_val"], spy["full"])
        return entry

    if earnings:
        base_e = [r for s in earnings if s in frames for r in rk.earnings_baseline_rows(s, frames[s], dates[s])]
        base_e = rk.with_costs(pd.DataFrame(base_e), COST_BPS_PRIMARY) if base_e else pd.DataFrame()
        for ep in rk.EARNINGS_GRID:
            rows = [r for s, e in earnings.items() if s in frames for r in rk.earnings_rows(s, frames[s], dates[s], e, ep)]
            variants.append(evaluate(ep.name, ep.__dict__, rows, base_e))

    for params in rk.GRID:
        if params.trail not in baselines:
            base = [r for s, df in frames.items() for r in rk.symbol_rows(s, df, dates[s], params, baseline=True)]
            baselines[params.trail] = rk.with_costs(pd.DataFrame(base), COST_BPS_PRIMARY) if base else pd.DataFrame()
        base = baselines[params.trail]
        rows = [r for s, df in frames.items() for r in rk.symbol_rows(s, df, dates[s], params, baseline=False)]
        variants.append(evaluate(params.name, params.__dict__, rows, base))
    passing = [v for v in variants if v.get("gates", {}).get("passes")]
    chosen = max(passing, key=lambda v: v["portfolio_train_val"].get("sharpe") or -9)["name"] if passing else None
    return {"start": first, "spy": spy, "variants": variants, "chosen": chosen}


def _rocket_markdown(r: dict) -> list[str]:
    spy = r["spy"]
    lines = ["", f"## Rockets (from {r['start']}, {COST_BPS_PRIMARY:g} bps per side, 10 slots x 10%, max 3 new per day)", "",
             f"Rocket day: close >= +jump vs previous close, volume >= {rk.VOLUME_MULT:g}x the 20-day average, close in the top "
             f"quarter of the day's range, price >= ${rk.MIN_PRICE:g}, 20-day dollar volume >= ${rk.MIN_DOLLAR_VOLUME / 1e6:g}M. "
             f"Buy next open; sell next open after a close more than `trail` below the highest close, or after {rk.MAX_HOLD} sessions. "
             "'Random' = same stocks, same liquidity filter, same exit, random dates.",
             "", f"SPY: {spy['full']['cagr_pct']:+.1f}%/yr, max DD {spy['full']['max_drawdown_pct']:.0f}%, Sharpe {_fmt(spy['full']['sharpe'], '.2f')} "
             f"· train+val {spy['train_val']['cagr_pct']:+.1f}%/yr, Sharpe {_fmt(spy['train_val']['sharpe'], '.2f')}",
             "", "| variant | trades | win% | avg trade | median | ≥+50% | worst | random avg | excess vs random t (train+val) | "
             "2015 large caps excess | CAGR | max DD | Sharpe | train+val CAGR / Sharpe | OOS CAGR | random-entry portfolio CAGR | without top 3 |",
             "|---|" + "---|" * 16]
    for v in r["variants"]:
        t = v["trades"]
        if not t.get("n"):
            lines.append(f"| {v['name']} | 0 |" + " |" * 15)
            continue
        p, tv, o, rp, w = v["portfolio"], v["portfolio_train_val"], v["portfolio_oos"], v["random_portfolio"], v["without_top3"]
        ex, lc = v["excess_train_val"], v["excess_largecap"]
        lines.append(
            f"| {v['name']} | {t['n']} | {t['win_rate'] * 100:.0f} | {t['avg_ret_pct']:+.1f}% | {t['median_ret_pct']:+.1f}% | "
            f"{t['big_winners_pct'] * 100:.1f}% | {t['worst_pct']:+.0f}% | {v['random_entries'].get('avg_ret_pct', 0):+.1f}% | "
            f"{_fmt(ex.get('avg_excess_pct'), '+.2f')}% ({_fmt(ex.get('t_month'), '.2f')}) | "
            f"{_fmt(lc.get('avg_excess_pct'), '+.2f')}% (n={v['largecap_trades'].get('n', 0)}) | "
            f"{_fmt(p.get('cagr_pct'), '+.1f')}% | {_fmt(p.get('max_drawdown_pct'), '.0f')}% | {_fmt(p.get('sharpe'), '.2f')} | "
            f"{_fmt(tv.get('cagr_pct'), '+.1f')}% / {_fmt(tv.get('sharpe'), '.2f')} | {_fmt(o.get('cagr_pct'), '+.1f')}% | "
            f"{_fmt(rp.get('cagr_pct'), '+.1f')}% | {_fmt(w.get('cagr_pct'), '+.1f')}% |")
    lines += ["", f"Pre-registered gates: excess vs random entries t >= {rk.GATE_MIN_T:g} (train+val); portfolio beats SPY on "
                  f"train+val CAGR and Sharpe; positive excess among 2015 large caps; CAGR without the 3 best stocks >= SPY's; "
                  f"max drawdown >= {rk.GATE_MAX_DRAWDOWN:g}%.", "",
              f"**Chosen: {r['chosen'] or 'none — no rocket variant passed every gate'}**", "",
              "| variant | passes | failed gates |", "|---|---|---|"]
    for v in r["variants"]:
        g = v.get("gates")
        if g:
            lines.append(f"| {v['name']} | {'✅' if g['passes'] else '❌'} | "
                         f"{', '.join(k for k, ok in g['checks'].items() if not ok) or '—'} |")
    return lines


def _fmt(value, spec: str, missing: str = "—") -> str:
    return missing if value is None or (isinstance(value, float) and math.isnan(value)) else format(value, spec)


def to_markdown(results: dict) -> str:
    meta, splits = results["meta"], results["splits"]
    lines = [
        "# Strategy research",
        "",
        f"{meta['symbols_ok']} symbols with data ({meta['symbols_failed']} failed), {meta['years']} years of daily bars. "
        f"Control group: {meta['largecap_symbols']} stocks that were already large caps in 2015. "
        f"Primary cost {COST_BPS_PRIMARY:g} bps per side (USD account: courtage + slippage; 40 bps ≈ trading from a SEK account). "
        f"Validation from {splits['validation_start']}, out-of-sample (OOS) from {splits['oos_start']}. "
        f"Setups invalidated at the next open (skipped): {meta['gap_skipped']}.",
        "",
        f"Portfolio: max {MAX_OPEN} positions, max {MAX_NEW_PER_DAY} new per day, {RISK_PCT:g}% risk per trade, "
        f"max {MAX_POSITION_PCT:g}% of equity per position, no leverage, marked to market daily. "
        f"'vs random' = share of {meta['random_runs']} random-order portfolios from the same eligible trades that this ranking beat.",
    ]
    for universe in ("all", "largecap_2015"):
        u = results["universes"][universe]
        spy, spy_oos, spy_tv = u["spy"], u["spy_oos"], u["spy_train_val"]
        lines += [
            "",
            f"## Portfolio — universe: {universe}",
            "",
            f"SPY buy-and-hold: {spy['cagr_pct']:+.1f}%/yr, max DD {spy['max_drawdown_pct']:.0f}%, Sharpe {spy['sharpe']} · "
            f"train+val Sharpe {spy_tv['sharpe']} · OOS {spy_oos['cagr_pct']:+.1f}%/yr, Sharpe {spy_oos['sharpe']}",
            "",
            "| rule set | trades/yr | exposure | win% | avgR | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe | vs random |",
            "|---|---|---|---|---|---|---|---|---|---|---|---|",
        ]
        for c in u["portfolio"]:
            f, tv, o = c["full"], c["train_val"], c["oos"]
            if not f.get("trades"):
                lines.append(f"| {c['label']} | 0 | | | | | | | | | | |")
                continue
            lines.append(
                f"| {c['label']} | {f['trades_per_year']} | {f['exposure_pct']:.0f}% | {f['win_rate'] * 100:.0f} | {f['avg_r']:+.2f} | "
                f"{f['cagr_pct']:+.1f}% | {f['max_drawdown_pct']:.0f}% | {_fmt(f['sharpe'], '.2f')} | {_fmt(tv.get('sharpe'), '.2f')} | "
                f"{_fmt(o.get('cagr_pct'), '+.1f')}% | {_fmt(o.get('sharpe'), '.2f')} | {_fmt(c.get('rank_percentile'), '.0%')} |"
            )
        lines += ["", "Cost sensitivity (full-period CAGR / Sharpe):", "",
                  "| rule set | " + " | ".join(f"{b:g} bps" for b in COST_BPS_GRID) + " |",
                  "|---|" + "---|" * len(COST_BPS_GRID)]
        for label, by_cost in u["cost_sensitivity"].items():
            lines.append(f"| {label} | " + " | ".join(
                f"{_fmt(s.get('cagr_pct'), '+.1f')}% / {_fmt(s.get('sharpe'), '.2f')}" for s in by_cost) + " |")
        lines += ["", "Exit variant (stop 2.5 x ATR instead of 1.5 x ATR / structural):", "",
                  "| rule set | CAGR | max DD | Sharpe | OOS Sharpe |", "|---|---|---|---|---|"]
        for c in u["portfolio_wide"]:
            f, o = c["full"], c["oos"]
            if f.get("trades"):
                lines.append(f"| {c['label']} | {f['cagr_pct']:+.1f}% | {f['max_drawdown_pct']:.0f}% | {_fmt(f['sharpe'], '.2f')} | {_fmt(o.get('sharpe'), '.2f')} |")
        lines += ["", f"### Per trade — universe: {universe} (one position per symbol, t over monthly means)", "",
                  "| group | exit | policy | n | win% | avgR | medR | t | excess vs random (t) | ≥+50% | OOS n | OOS avgR |",
                  "|---|---|---|---|---|---|---|---|---|---|---|---|"]
        for row in u["per_trade"]:
            o, oos, ex = row["overall"], row["out_of_sample"], row["excess_vs_random"] or {}
            lines.append(
                f"| {row['group']} | {row['exit']} | {row['policy']} | {o['n']} | {o['win_rate'] * 100:.0f} | {o['avg_r']:+.3f} | "
                f"{o['median_r']:+.2f} | {_fmt(o['t_month'], '.2f')} | "
                f"{_fmt(ex.get('avg_excess_r'), '+.3f')} ({_fmt(ex.get('t_month'), '.2f')}) | {o['big_winners_pct'] * 100:.1f}% | "
                f"{oos.get('n', 0)} | {_fmt(oos.get('avg_r'), '+.3f')} |"
            )
    for universe in ("all", "largecap_2015"):
        r = results["universes"][universe].get("rotation")
        if not r:
            continue
        lines += [
            "",
            f"## Momentum rotation — universe: {universe} (from {r['start']}, {COST_BPS_PRIMARY:g} bps per side)",
            "",
            "| benchmark | CAGR | max DD | Sharpe | train+val Sharpe | OOS CAGR | OOS Sharpe |",
            "|---|---|---|---|---|---|---|",
        ]
        for label, full, tv, oos in (("SPY buy-and-hold", r["spy"], r["spy_train_val"], r["spy_oos"]),
                                     ("equal-weight universe (no costs)", r["equal_weight"], r["equal_weight_train_val"], r["equal_weight_oos"])):
            lines.append(f"| {label} | {full['cagr_pct']:+.1f}% | {full['max_drawdown_pct']:.0f}% | {_fmt(full['sharpe'], '.2f')} | "
                         f"{_fmt(tv.get('sharpe'), '.2f')} | {_fmt(oos.get('cagr_pct'), '+.1f')}% | {_fmt(oos.get('sharpe'), '.2f')} |")
        lines += ["", "| rule set | trades/yr | exposure | win% | avg trade | avg days | CAGR | max DD | Sharpe | train+val Sharpe | "
                  "OOS CAGR | OOS Sharpe | vs random | CAGR @" + " / @".join(f"{b:g}" for b in COST_BPS_GRID if b != COST_BPS_PRIMARY) + " bps | without best stock |", "|---|" + "---|" * 14]
        for c in r["configs"]:
            f, tv, o = c["full"], c["train_val"], c["oos"]
            cs = c["cost_sensitivity"]
            lines.append(
                f"| {c['name']} | {_fmt(f.get('trades_per_year'), '.0f')} | {_fmt(f.get('exposure_pct'), '.0f')}% | "
                f"{_fmt(f.get('win_rate') and f['win_rate'] * 100, '.0f')} | {_fmt(f.get('avg_trade_pct'), '+.1f')}% | {_fmt(f.get('avg_days'), '.0f')} | "
                f"{f['cagr_pct']:+.1f}% | {f['max_drawdown_pct']:.0f}% | {_fmt(f['sharpe'], '.2f')} | {_fmt(tv.get('sharpe'), '.2f')} | "
                f"{_fmt(o.get('cagr_pct'), '+.1f')}% | {_fmt(o.get('sharpe'), '.2f')} | {_fmt(c.get('rank_percentile'), '.0%')} | "
                + " / ".join(f"{_fmt(v.get('cagr_pct'), '+.1f')}%" for v in cs.values()) + " | "
                + (f"{c['without_top']['symbol']}: {c['without_top']['cagr_pct']:+.1f}%, Sharpe {_fmt(c['without_top']['sharpe'], '.2f')} |"
                   if c.get("without_top") else "— |")
            )
    sel = results.get("rotation_selection") or {}
    lc = results["universes"]["largecap_2015"].get("rotation")
    if lc:
        lines += ["", "## Rotation: pre-registered selection (2015 large caps, train+validation only)", "",
                  f"Gates: train+val Sharpe > SPY's, ranking beats >= {GATE_MIN_RANDOM_PERCENTILE:.0%} of random selections, "
                  f"CAGR without the single best stock >= SPY's, max drawdown at most {GATE_MAX_EXTRA_DRAWDOWN_PCT:g} points worse than SPY's.",
                  "", f"**Chosen: {sel.get('chosen') or 'none — no rule set passed every gate'}**", "",
                  "| rule set | passes | train+val Sharpe | failed gates |", "|---|---|---|---|"]
        for g in sel.get("gates", []):
            failed = ", ".join(k for k, ok in g["checks"].items() if not ok) or "—"
            lines.append(f"| {g['name']} | {'✅' if g['passes'] else '❌'} | {_fmt(g['train_val_sharpe'], '.2f')} | {failed} |")
        years = sorted(lc["spy_by_year"])
        lines += ["", f"Calendar-year returns (2015 large caps, {COST_BPS_PRIMARY:g} bps per side):", "",
                  "| | " + " | ".join(years) + " |", "|---|" + "---|" * len(years),
                  "| SPY | " + " | ".join(_fmt(lc["spy_by_year"].get(y), '+.0f') + "%" for y in years) + " |",
                  "| equal-weight group | " + " | ".join(_fmt(lc["equal_weight_by_year"].get(y), '+.0f') + "%" for y in years) + " |"]
        for c in lc["configs"]:
            if c["name"] == sel.get("chosen") or not sel.get("chosen"):
                lines.append(f"| {c['name']} | " + " | ".join(_fmt(c["by_year"].get(y), '+.0f') + "%" for y in years) + " |")
    if results.get("rockets"):
        lines += _rocket_markdown(results["rockets"])
    lines += ["", "## Mean R by year (all universe, fixed exit)", ""]
    years = sorted({y for row in results["universes"]["all"]["per_trade"] for y in row["avg_r_by_year"]})
    lines += ["| group | policy | " + " | ".join(years) + " |", "|---|---|" + "---|" * len(years)]
    for row in results["universes"]["all"]["per_trade"]:
        if row["exit"] == "fixed" and row["group"] in ("combined", "baseline_random"):
            lines.append(f"| {row['group']} | {row['policy']} | " + " | ".join(
                _fmt(row["avg_r_by_year"].get(y), '+.2f') for y in years) + " |")
    return "\n".join(lines)


def run_research(symbols: list[str], years: int = 10, out_dir: str | Path = "research_output", random_runs: int = RANDOM_RUNS) -> dict:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    limit = 252 * years
    symbols = [s.upper() for s in dict.fromkeys(symbols) if s.upper() != ANCHOR_SYMBOL]

    with StockClient() as client:
        client.prefetch(sorted(set(symbols + [ANCHOR_SYMBOL])), "1d", limit=limit)
        spy = enrich(client.get_klines(ANCHOR_SYMBOL, "1d", limit=limit))
        market = market_context(spy)
        spy_closes = pd.Series(spy["close"].to_numpy(dtype=float), index=_session_dates(spy))
        spy_frame = pd.DataFrame({"close": spy["close"].to_numpy(dtype=float)}, index=_session_dates(spy))

        all_rows: list[dict] = []
        returns: dict[str, pd.Series] = {}
        closes: dict[str, pd.Series] = {}
        ohlc: dict[str, pd.DataFrame] = {}
        raw_frames: dict[str, pd.DataFrame] = {}
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
            rows, skipped, ret_6m = symbol_rows(symbol, enrich(df), market)
            all_rows.extend(rows)
            returns[symbol] = ret_6m
            closes[symbol] = pd.Series(df["close"].to_numpy(dtype=float), index=_session_dates(df))
            ohlc[symbol] = pd.DataFrame({c: df[c].to_numpy(dtype=float) for c in ("open", "low", "close")}, index=_session_dates(df))
            raw_frames[symbol] = df
            gap_skipped += skipped
            if n % 25 == 0:
                logger.info("research: %d/%d symbols done, %d candidate rows so far", n, len(symbols), len(all_rows))

    largecap = [s for s in LARGECAP_2015 if s in returns]
    frame = attach_relative_strength(pd.DataFrame(all_rows), returns, "rs")
    frame = attach_relative_strength(frame, {s: returns[s] for s in largecap}, "rs_largecap")
    frame["largecap"] = frame["symbol"].isin(largecap)
    frame.to_csv(out / "candidate_rows.csv.gz", index=False)

    splits = split_dates(frame)
    prices = PriceBook(closes)
    results = {"splits": splits.__dict__, "universes": {}}
    for universe, subset, rs_col in (("all", frame, "rs"), ("largecap_2015", frame[frame["largecap"]], "rs_largecap")):
        members = sorted(returns) if universe == "all" else largecap
        rotation = rotation_results(rot.build_panel(ohlc, spy_frame, members), splits, spy_closes, random_runs and ROTATION_RANDOM_RUNS,
                                    rebuild=lambda syms: rot.build_panel(ohlc, spy_frame, syms))
        primary = with_costs(subset, COST_BPS_PRIMARY)
        portfolio = portfolio_results(subset, spy_closes, prices, splits, rs_col, COST_BPS_PRIMARY, "fixed", random_runs)
        sensitivity = {}
        for label, group, params, rank in PORTFOLIO_CONFIGS:
            if rank == "rand":
                continue
            by_cost = []
            for bps in COST_BPS_GRID:
                eligible = select_group(with_costs(subset[subset["exit"] == "fixed"], bps), group)
                eligible = eligible[policy_mask(eligible, *params, rs_col=rs_col)]
                if rank == "rs":
                    eligible = eligible.assign(rs=eligible[rs_col])
                first = str(subset["entry_date"].min())
                by_cost.append(simulate_portfolio(eligible, rank, [d for d in spy_closes.index if d >= first], prices, bps))
            sensitivity[label] = by_cost
        results["universes"][universe] = {
            "spy": benchmark(spy_closes, str(subset["entry_date"].min())),
            "spy_train_val": benchmark(spy_closes, str(subset["entry_date"].min()), splits.oos_start),
            "spy_oos": benchmark(spy_closes, splits.oos_start),
            "portfolio": portfolio,
            "portfolio_wide": portfolio_results(subset, spy_closes, prices, splits, rs_col, COST_BPS_PRIMARY, "wide", 0),
            "cost_sensitivity": sensitivity,
            "per_trade": evaluate_trades(primary, splits, rs_col),
            "rotation": rotation,
        }

    earnings, earnings_failed = rk.fetch_earnings(sorted(raw_frames))
    logger.info("research: earnings history for %d symbols (%d without)", len(earnings), len(earnings_failed))
    results["rockets"] = rocket_results(raw_frames, set(largecap), spy_closes, prices, splits, earnings)
    results["rockets"]["earnings_coverage"] = {"symbols": len(earnings), "missing": len(earnings_failed)}
    results["rotation_selection"] = select_rotation(results["universes"]["largecap_2015"].get("rotation"))
    results["meta"] = {
        "symbols_ok": len(returns), "symbols_failed": len(failed), "failed": failed, "years": years,
        "largecap_symbols": len(largecap), "gap_skipped": gap_skipped,
        "candidates": int((frame["exit"] == "fixed").sum()), "cost_bps_primary": COST_BPS_PRIMARY, "random_runs": random_runs,
    }
    # Backwards-compatible flat list the live policy reads its evidence from.
    results["policies"] = results["universes"]["all"]["per_trade"]
    (out / "evidence.json").write_text(json.dumps(results, indent=2, default=str))
    (out / "research.md").write_text(to_markdown(results))
    return results
