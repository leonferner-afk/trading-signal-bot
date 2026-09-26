"""Momentum rotation ("trendledare"): hold the strongest stocks in the
universe while they stay strong and in an uptrend, sell them when they stop
being either.

The research showed that stop/target swing trades lose to buying the index,
mostly because tight stops are hit by ordinary noise, while *which* stocks
were held — the relative-strength leaders in an uptrend — was where the
edge sat. This rule set keeps the selection and replaces the exits.

`decide()` is the whole rule and is shared by the research simulation and
the live daily run, so the live bot does exactly what was tested:

  at each close, using only data up to that close:
    SELL a holding if its stock closed below its 200-day average, or its
         6-month relative strength fell below `exit_rs`, or (optionally)
         the market (SPY) closed below its 200-day average
    BUY  (only while SPY is above its 200-day average) the highest-RS
         stocks above their own 200-day average with RS >= `entry_rs`,
         into free slots, at most `max_new_per_day` per day
  orders are filled at the next session's open; an optional protective
  stop (`stop_pct` below the fill) is a standing stop order
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class RotationParams:
    max_positions: int = 8
    entry_rs: float = 0.8
    exit_rs: float = 0.5
    regime_exit: bool = False
    stop_pct: float = 0.0          # 0 = no protective stop order
    max_new_per_day: int = 3

    @property
    def name(self) -> str:
        parts = [f"top{self.max_positions}", f"in RS>={self.entry_rs:g}", f"out RS<{self.exit_rs:g}"]
        if self.regime_exit:
            parts.append("sell all when SPY<200d")
        if self.stop_pct:
            parts.append(f"stop -{self.stop_pct * 100:g}%")
        return ", ".join(parts)


def decide(
    holdings: list[str],
    rs: dict[str, float],
    above_200: dict[str, bool],
    spy_above_200: bool,
    params: RotationParams,
    rng: np.random.Generator | None = None,
) -> tuple[list[tuple[str, str]], list[str]]:
    """Returns (sells as (symbol, reason), buys in priority order).

    A holding with no data today is kept (never sold on a guess). `rng`
    replaces the RS ranking of buy candidates with a random order — the
    research's test of whether the ranking itself adds anything."""
    sells: list[tuple[str, str]] = []
    for symbol in holdings:
        if params.regime_exit and not spy_above_200:
            sells.append((symbol, "marknaden (SPY) stängde under sitt 200-dagars snitt"))
        elif symbol not in rs or symbol not in above_200:
            continue
        elif not above_200[symbol]:
            sells.append((symbol, "aktien stängde under sitt 200-dagars snitt"))
        elif rs[symbol] < params.exit_rs:
            sells.append((symbol, f"relativ styrka föll till {rs[symbol] * 100:.0f}% (gräns {params.exit_rs * 100:.0f}%)"))

    if not spy_above_200:
        return sells, []
    selling = {s for s, _ in sells}
    kept = [s for s in holdings if s not in selling]
    slots = min(params.max_positions - len(kept), params.max_new_per_day)
    if slots <= 0:
        return sells, []
    held = set(holdings)
    candidates = [s for s, value in rs.items()
                  if s not in held and above_200.get(s) and value is not None and value >= params.entry_rs]
    if rng is not None:
        rng.shuffle(candidates)
    else:
        candidates.sort(key=lambda s: rs[s], reverse=True)
    return sells, candidates[:slots]


# --------------------------------------------------------------------------
# Research simulation (daily, marked to market, next-open fills, costs)
# --------------------------------------------------------------------------

RS_LOOKBACK = 126


@dataclass
class Panel:
    """Aligned (session date x symbol) matrices on the market calendar."""
    dates: list[str]
    symbols: list[str]
    open: np.ndarray
    low: np.ndarray
    close: np.ndarray      # forward-filled for marking (max 5 sessions)
    rs: np.ndarray         # cross-sectional percentile of the 6-month return, NaN if unknown
    above_200: np.ndarray  # bool
    has_bar: np.ndarray    # bool: a real bar exists that day (no forward-fill)
    spy_above_200: np.ndarray


def build_panel(frames: dict[str, pd.DataFrame], spy: pd.DataFrame, symbols: list[str]) -> Panel:
    """`frames[symbol]` / `spy`: DataFrames indexed by session date with
    open/low/close. Every feature at row t uses data up to t only."""
    dates = list(spy.index)
    symbols = [s for s in symbols if s in frames]

    def matrix(column: str) -> pd.DataFrame:
        return pd.DataFrame({s: frames[s][column] for s in symbols}).reindex(dates)

    close_raw = matrix("close")
    close = close_raw.ffill(limit=5)
    ret_6m = close_raw / close_raw.shift(RS_LOOKBACK) - 1
    rs = ret_6m.rank(axis=1, pct=True)
    sma200 = close_raw.rolling(200, min_periods=200).mean()
    above = (close_raw > sma200)
    spy_close = spy["close"]
    spy_above = (spy_close > spy_close.rolling(200, min_periods=200).mean()).to_numpy()
    return Panel(dates, symbols, matrix("open").to_numpy(float), matrix("low").to_numpy(float), close.to_numpy(float),
                 rs.to_numpy(float), above.to_numpy(bool), close_raw.notna().to_numpy(), spy_above)


def simulate(panel: Panel, params: RotationParams, cost_bps: float, start: str | None = None,
             rng: np.random.Generator | None = None) -> dict:
    """Runs the rotation from `start` (after warm-up) to the end. Returns the
    equity curve (by date) and the closed-trade list."""
    c = cost_bps / 10000.0
    first = max(RS_LOOKBACK + 200, 0)
    if start:
        first = max(first, next((i for i, d in enumerate(panel.dates) if d >= start), len(panel.dates)))
    cash, equity = 1.0, 1.0
    positions: dict[int, dict] = {}   # column -> {shares, fill, entry_i, stop}
    pending_sells: dict[int, str] = {}
    pending_buys: list[int] = []
    curve, dates, exposure, trades = [], [], [], []
    col = {s: j for j, s in enumerate(panel.symbols)}

    def close_position(j: int, price: float, i: int, reason: str) -> None:
        nonlocal cash
        p = positions.pop(j)
        cash += p["shares"] * price * (1 - c)
        trades.append({"symbol": panel.symbols[j], "entry": panel.dates[p["entry_i"]], "exit": panel.dates[i],
                       "ret_pct": (price * (1 - c) / (p["fill"] * (1 + c)) - 1) * 100, "days": i - p["entry_i"],
                       "reason": reason})

    for i in range(first, len(panel.dates)):
        # 1) orders decided at the previous close fill at today's open
        for j, reason in list(pending_sells.items()):
            price = panel.open[i, j]
            if j in positions and np.isfinite(price):
                close_position(j, price, i, reason)
            if j not in positions:
                pending_sells.pop(j)
        budget = equity / params.max_positions
        for j in pending_buys:
            price = panel.open[i, j]
            if j in positions or not np.isfinite(price) or len(positions) >= params.max_positions:
                continue
            notional = min(budget, cash)
            if notional < equity * 0.02:
                continue
            cash -= notional
            positions[j] = {"shares": notional / (price * (1 + c)), "fill": price, "entry_i": i,
                            "stop": price * (1 - params.stop_pct) if params.stop_pct else None}
        pending_buys = []
        # 2) standing protective stops during the day
        for j in [j for j, p in positions.items() if p["stop"] is not None]:
            low, o = panel.low[i, j], panel.open[i, j]
            if np.isfinite(low) and low <= positions[j]["stop"]:
                close_position(j, min(positions[j]["stop"], o) if np.isfinite(o) else positions[j]["stop"], i, "stop")
        # 3) mark to market at the close
        value = sum(p["shares"] * panel.close[i, j] for j, p in positions.items() if np.isfinite(panel.close[i, j]))
        equity = cash + value
        curve.append(equity)
        dates.append(panel.dates[i])
        exposure.append(value / equity if equity > 0 else 0.0)
        # 4) decide tomorrow's orders from today's close
        # Only buy candidates and holdings can be affected by decide(), so
        # only they are passed (identical result, far faster).
        row_rs = panel.rs[i]
        relevant = set(np.flatnonzero((row_rs >= params.entry_rs) & panel.above_200[i]).tolist()) | set(positions)
        rs_today = {panel.symbols[j]: float(row_rs[j]) for j in relevant if np.isfinite(row_rs[j])}
        above_today = {panel.symbols[j]: bool(panel.above_200[i, j]) for j in relevant if panel.has_bar[i, j]}
        sells, buys = decide([panel.symbols[j] for j in positions], rs_today, above_today,
                             bool(panel.spy_above_200[i]), params, rng)
        pending_sells.update({col[s]: reason for s, reason in sells})
        pending_buys = [col[s] for s in buys]

    return {"dates": dates, "curve": np.array(curve), "exposure": np.array(exposure), "trades": trades}


def equal_weight_benchmark(panel: Panel, start_index: int) -> np.ndarray:
    """Cost-free, daily-rebalanced equal-weight holding of every stock in
    the panel — what the universe itself returned, selection-free."""
    close = np.where(panel.has_bar, panel.close, np.nan)
    with np.errstate(invalid="ignore", divide="ignore"):
        daily = close[1:] / close[:-1] - 1
    mean = np.nanmean(np.where(np.isfinite(daily), daily, np.nan), axis=1)
    mean = np.nan_to_num(mean[start_index:], nan=0.0)
    return np.concatenate([[1.0], np.cumprod(1 + mean)])
