"""Rocket ("raket") research: stocks that jump on heavy volume after news
or earnings, bought at the next open and held while they keep going.

A rocket day is a session where the stock
  - closed at least `min_jump` above the previous close,
  - on at least VOLUME_MULT x its average volume of the previous 20 sessions,
  - closed in the top quarter of the day's range (buyers held on),
  - trades at >= MIN_PRICE with >= MIN_DOLLAR_VOLUME average daily turnover
    (keeps out the penny stocks where pump-and-dumps live).
Documented background: post-earnings-announcement drift — large positive
surprises tend to keep drifting up for weeks.

Every rule decides at a close and trades at the next open, like the rest
of the bot: buy at the open after the rocket day; sell at the open after a
close more than `trail` below the highest close since entry (the fill
counts as the first high), or after MAX_HOLD sessions.

The fair test is against RANDOM entries in the SAME stocks with the SAME
exit rule: free data lacks delisted small caps, so the stock list itself is
too flattering, but that bias hits the random entries just as hard — only
the rocket timing is what's measured.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
import pandas as pd

VOLUME_MULT = 3.0
MIN_CLOSE_LOCATION = 0.75
MIN_PRICE = 5.0
MIN_DOLLAR_VOLUME = 5e6
MAX_HOLD = 40            # sessions (~2 months)
BASELINE_EVERY = 5
MAX_OPEN = 10
MAX_NEW_PER_DAY = 3
WEIGHT = 0.10            # each position = 1/10 of the rocket pot


@dataclass(frozen=True)
class RocketParams:
    min_jump: float = 0.08
    trail: float = 0.25

    @property
    def name(self) -> str:
        return f"jump>={self.min_jump * 100:g}%, trail {self.trail * 100:g}%"


GRID = [RocketParams(j, t) for j in (0.08, 0.15) for t in (0.15, 0.25)]


def event_features(df: pd.DataFrame) -> pd.DataFrame:
    """Per-session rocket features, each using data up to that session only."""
    close, volume = df["close"].astype(float), df["volume"].astype(float)
    high, low = df["high"].astype(float), df["low"].astype(float)
    prev_avg_vol = volume.rolling(20, min_periods=20).mean().shift(1)
    rng = (high - low).replace(0, np.nan)
    return pd.DataFrame({
        "jump": close / close.shift(1) - 1,
        "volume_ratio": volume / prev_avg_vol,
        "close_location": (close - low) / rng,
        "dollar_volume": (close * volume).rolling(20, min_periods=20).mean().shift(1),
        "close": close,
    }, index=df.index)


def is_rocket(f: pd.DataFrame, min_jump: float) -> pd.Series:
    return ((f["jump"] >= min_jump) & (f["volume_ratio"] >= VOLUME_MULT) & (f["close_location"] >= MIN_CLOSE_LOCATION)
            & (f["close"] >= MIN_PRICE) & (f["dollar_volume"] >= MIN_DOLLAR_VOLUME)).fillna(False)


def eligible(f: pd.DataFrame) -> pd.Series:
    """Liquidity filter alone — what random baseline entries must also pass."""
    return ((f["close"] >= MIN_PRICE) & (f["dollar_volume"] >= MIN_DOLLAR_VOLUME)).fillna(False)


def trailing_exit(opens: np.ndarray, closes: np.ndarray, signal_i: int, trail: float,
                  max_hold: int = MAX_HOLD) -> tuple[int, float, str] | None:
    """Buy at the open after `signal_i`; returns (exit index, exit price,
    reason) or None if the exit isn't known yet (data ends first)."""
    entry = signal_i + 1
    if entry >= len(opens) or not math.isfinite(opens[entry]):
        return None
    peak = opens[entry]
    for k in range(entry, len(closes)):
        c = closes[k]
        if not math.isfinite(c):
            continue
        peak = max(peak, c)
        held = k - entry + 1
        reason = "trail" if c <= peak * (1 - trail) else ("time" if held >= max_hold else None)
        if reason:
            if k + 1 >= len(opens) or not math.isfinite(opens[k + 1]):
                return None
            return k + 1, float(opens[k + 1]), reason
    return None


def symbol_rows(symbol: str, df: pd.DataFrame, dates: np.ndarray, params: RocketParams, baseline: bool) -> list[dict]:
    """Rocket trades (or, with `baseline`, random-date trades under the same
    liquidity filter and exit) for one stock."""
    f = event_features(df)
    opens, closes = df["open"].to_numpy(float), df["close"].to_numpy(float)
    if baseline:
        ok = eligible(f).to_numpy()
        idx = [i for i in range(21, len(df) - 1, BASELINE_EVERY) if ok[i]]
    else:
        idx = np.flatnonzero(is_rocket(f, params.min_jump).to_numpy()).tolist()
    rows = []
    for i in idx:
        ex = trailing_exit(opens, closes, i, params.trail)
        if ex is None:
            continue
        k, price, reason = ex
        fill = float(opens[i + 1])
        rows.append({
            "symbol": symbol, "date": dates[i], "entry_date": dates[i + 1], "exit_date": dates[k], "i": i, "exit_i": k,
            "fill": fill, "exit_raw": price, "reason": reason, "hold_bars": k - i - 1,
            "jump": float(f["jump"].iloc[i]), "volume_ratio": float(f["volume_ratio"].iloc[i]),
            # Research's portfolio simulator sizes by stop distance; rockets are
            # equal weight, expressed through `weight` there instead.
            "stop_dist_pct": params.trail * 100,
        })
    return rows


def with_costs(rows: pd.DataFrame, cost_bps: float) -> pd.DataFrame:
    c = cost_bps / 10000.0
    ret = (rows["exit_raw"] * (1 - c) / (rows["fill"] * (1 + c)) - 1) * 100
    return rows.assign(ret_pct=ret, r_multiple=ret / (rows["stop_dist_pct"]))


def monthly_excess(trades: pd.DataFrame, baseline: pd.DataFrame) -> dict:
    """Month-by-month mean net return of rocket trades minus random entries
    in the same stocks; t-statistic over months."""
    if trades.empty or baseline.empty:
        return {"months": 0}
    a = trades.groupby(trades["date"].str[:7])["ret_pct"].mean()
    b = baseline.groupby(baseline["date"].str[:7])["ret_pct"].mean()
    diff = (a - b).dropna()
    if len(diff) < 6 or diff.std(ddof=1) == 0:
        return {"months": int(len(diff))}
    return {"months": int(len(diff)), "avg_excess_pct": round(float(diff.mean()), 3),
            "t_month": round(float(diff.mean() / diff.std(ddof=1) * math.sqrt(len(diff))), 2)}


def trade_summary(t: pd.DataFrame) -> dict:
    if t.empty:
        return {"n": 0}
    r = t["ret_pct"]
    return {"n": int(len(t)), "win_rate": round(float((r > 0).mean()), 3), "avg_ret_pct": round(float(r.mean()), 2),
            "median_ret_pct": round(float(r.median()), 2), "big_winners_pct": round(float((r >= 50).mean()), 4),
            "worst_pct": round(float(r.min()), 1), "best_pct": round(float(r.max()), 1),
            "avg_hold": round(float(t["hold_bars"].mean()), 1)}


# Pre-registered gates (fixed before any rocket result was seen). Stricter
# than the rotation's because free small-cap data flatters every test.
GATE_MIN_T = 2.0
GATE_MAX_DRAWDOWN = -50.0


def rocket_gates(entry: dict, spy_tv: dict, spy_full: dict) -> dict:
    tv, full = entry["portfolio_train_val"], entry["portfolio"]
    checks = {
        "beats_random_entries_same_stocks": (entry["excess_train_val"].get("t_month") or 0) >= GATE_MIN_T,
        "beats_spy_train_val": ((tv.get("cagr_pct") or -99) > (spy_tv.get("cagr_pct") or 0)
                                and (tv.get("sharpe") or -9) > (spy_tv.get("sharpe") or 0)),
        "holds_in_2015_largecaps": (entry["excess_largecap"].get("avg_excess_pct") or -1) > 0,
        "without_top3_beats_spy": (entry.get("without_top3", {}).get("cagr_pct") or -99) >= spy_full["cagr_pct"],
        "drawdown_tolerable": (full.get("max_drawdown_pct") or -100) >= GATE_MAX_DRAWDOWN,
    }
    return {"passes": all(checks.values()), "checks": checks}
