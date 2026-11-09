"""Backtest of simple, well-documented "bots" that trade whole-market ETFs,
as candidates to replace the stock rotation (which lost ~21 % in its first
live month while SPY lost 2.5 %, and never beat SPY risk-adjusted in research).

Every strategy holds exactly one ETF at a time. It decides at each month's
last close and trades at the next session's open, paying FEE_BPS on each
side. Prices are Yahoo's dividend-adjusted daily bars.

Candidates (all fixed before seeing any result):
  * S&P 500, buy and hold (the benchmark)
  * Nasdaq 100, buy and hold (reference: more aggressive index)
  * S&P 500 + 200-day trend filter: SPY above its 200-day average, else T-bills (BIL)
  * Nasdaq 100 + 200-day trend filter: QQQ above its 200-day average, else BIL
  * Dual momentum (Antonacci's GEM): the better 12-month performer of SPY and
    EFA (developed markets ex-US) if it beat T-bills over 12 months, else bonds (AGG)

Pre-registered gate (also printed in the report): a candidate qualifies only
if, over the whole period, its Sharpe ratio is above SPY's AND its maximum
drawdown is smaller than SPY's, AND its Sharpe is above SPY's in each half of
the period separately (so one lucky stretch can't carry it). Among those that
qualify, the highest annual return wins. Nothing qualifying = keep the index.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import pandas as pd

SYMBOLS = ["SPY", "QQQ", "EFA", "AGG", "BIL"]
TRADING_DAYS = 252


@dataclass
class Result:
    name: str
    equity: pd.Series          # daily close-to-close value, starts at 1.0
    switches: int


def _month_ends(index: pd.DatetimeIndex) -> set[pd.Timestamp]:
    s = pd.Series(index, index=index)
    return set(s.groupby([index.year, index.month]).max())


def simulate(name: str, opens: pd.DataFrame, closes: pd.DataFrame, choose, fee_bps: float = 15.0) -> Result:
    """`choose(closes_up_to_today)` -> symbol to hold, evaluated at month-end
    closes; a change is executed at the next day's open."""
    fee = fee_bps / 10000.0
    days = closes.index
    month_ends = _month_ends(days)
    held, units, cash = None, 0.0, 1.0
    pending = None
    values, switches = [], 0
    for i, d in enumerate(days):
        if pending is not None and pending != held:
            if held is not None:
                cash = units * opens.at[d, held] * (1 - fee)
            units = cash * (1 - fee) / opens.at[d, pending]
            held, cash, switches = pending, 0.0, switches + 1
        pending = None
        values.append(units * closes.at[d, held] if held is not None else cash)
        if d in month_ends or i == 0:
            pending = choose(closes.iloc[: i + 1])
    return Result(name, pd.Series(values, index=days), switches)


def simulate_exits(name: str, opens: pd.DataFrame, closes: pd.DataFrame, sym: str = "QQQ", cash: str = "BIL",
                   trail: float = 0.0, take_profit: float = 0.0, fee_bps: float = 15.0, window: int = 200) -> Result:
    """Holds `sym` with a stop-loss and/or take-profit, checked at every close
    and executed at the next open: `trail` = a close that far below the highest
    close since entry, `take_profit` = a close that far above the entry fill.
    After an exit it sits in `cash` and re-enters at a month-end close with
    `sym` above its `window`-day average (the first entry uses the same rule)."""
    fee = fee_bps / 10000.0
    days = closes.index
    month_ends = _month_ends(days)
    held, units, value = None, 0.0, 1.0
    pending, entry_px, peak = None, None, None
    values, switches = [], 0
    for i, d in enumerate(days):
        if pending is not None and pending != held:
            if held is not None:
                value = units * opens.at[d, held] * (1 - fee)
            units = value * (1 - fee) / opens.at[d, pending]
            held, switches = pending, switches + 1
            entry_px = peak = opens.at[d, held] if held == sym else None
        pending = None
        values.append(units * closes.at[d, held] if held is not None else value)
        c = closes.iloc[: i + 1]
        if held == sym:
            px = closes.at[d, sym]
            peak = max(peak, px)
            if (trail and px <= peak * (1 - trail)) or (take_profit and px >= entry_px * (1 + take_profit)):
                pending = cash
        elif d in month_ends and len(c) > max(window, TRADING_DAYS):
            s_ = c[sym]
            pending = sym if s_.iloc[-1] > s_.iloc[-window:].mean() else (cash if held is not None else None)
    return Result(name, pd.Series(values, index=days), switches)


EXIT_VARIANTS = [
    # Owner's question (2026-11-09): stop-loss / take-profit on the Nasdaq 100
    # depot? Fixed before the run; compared with plain buy-and-hold.
    ("Nasdaq 100 + stop −10 %", {"trail": 0.10}),
    ("Nasdaq 100 + stop −15 %", {"trail": 0.15}),
    ("Nasdaq 100 + stop −20 %", {"trail": 0.20}),
    ("Nasdaq 100 + take-profit +20 %", {"take_profit": 0.20}),
    ("Nasdaq 100 + take-profit +30 %", {"take_profit": 0.30}),
    ("Nasdaq 100 + take-profit +50 %", {"take_profit": 0.50}),
    ("Nasdaq 100 + stop −15 % & take-profit +30 %", {"trail": 0.15, "take_profit": 0.30}),
]


def _ret(closes: pd.DataFrame, sym: str, days: int) -> float:
    s = closes[sym]
    return s.iloc[-1] / s.iloc[-1 - days] - 1


def buy_and_hold(sym: str):
    return lambda c: sym


def trend(sym: str, cash: str = "BIL", window: int = 200):
    def choose(c: pd.DataFrame) -> str:
        s = c[sym]
        return sym if s.iloc[-1] > s.iloc[-window:].mean() else cash
    return choose


def dual_momentum(c: pd.DataFrame) -> str:
    us, intl, bills = (_ret(c, s, TRADING_DAYS) for s in ("SPY", "EFA", "BIL"))
    best, best_ret = ("SPY", us) if us >= intl else ("EFA", intl)
    return best if best_ret > bills else "AGG"


STRATEGIES = [
    ("S&P 500 (köp och behåll)", buy_and_hold("SPY")),
    ("Nasdaq 100 (köp och behåll)", buy_and_hold("QQQ")),
    ("S&P 500 + trendfilter", trend("SPY")),
    ("Nasdaq 100 + trendfilter", trend("QQQ")),
    ("Dubbel momentum (USA/världen/räntor)", dual_momentum),
]


def stats(equity: pd.Series) -> dict:
    r = equity.pct_change().dropna()
    years = len(r) / TRADING_DAYS
    cagr = equity.iloc[-1] ** (1 / years) - 1 if years > 0 else 0.0
    sharpe = r.mean() / r.std() * math.sqrt(TRADING_DAYS) if r.std() > 0 else 0.0
    dd = (equity / equity.cummax() - 1).min()
    return {"cagr": cagr * 100, "sharpe": sharpe, "max_dd": dd * 100}


def calendar_returns(equity: pd.Series, freq: str) -> pd.Series:
    """'YE' -> per year, 'ME' -> per month, in percent."""
    last = equity.resample(freq).last()
    first_val = equity.iloc[0]
    return (last / last.shift(1).fillna(first_val) - 1) * 100


def evaluate(opens: pd.DataFrame, closes: pd.DataFrame, fee_bps: float = 15.0) -> dict:
    # Start after a year of history so 12-month and 200-day signals exist.
    start = closes.index[TRADING_DAYS]
    results = []
    for name, choose in STRATEGIES:
        res = simulate(name, opens, closes, lambda c, f=choose: f(c) if len(c) > TRADING_DAYS else None, fee_bps)
        eq = res.equity.loc[start:]
        eq = eq / eq.iloc[0]
        results.append(Result(name, eq, res.switches))
    for name, kw in EXIT_VARIANTS:
        res = simulate_exits(name, opens, closes, fee_bps=fee_bps, **kw)
        eq = res.equity.loc[start:]
        eq = eq / eq.iloc[0]
        results.append(Result(name, eq, res.switches))
    mid = results[0].equity.index[len(results[0].equity) // 2]
    table = []
    for res in results:
        full = stats(res.equity)
        h1 = stats(res.equity.loc[:mid] / res.equity.loc[:mid].iloc[0])
        h2 = stats(res.equity.loc[mid:] / res.equity.loc[mid:].iloc[0])
        table.append({"name": res.name, **full, "sharpe_h1": h1["sharpe"], "sharpe_h2": h2["sharpe"],
                      "cagr_h1": h1["cagr"], "cagr_h2": h2["cagr"], "switches": res.switches,
                      "years": calendar_returns(res.equity, "YE"), "months": calendar_returns(res.equity, "ME"),
                      "equity": res.equity})
    spy = table[0]
    main = table[:len(STRATEGIES)]
    for row in main[1:]:
        row["qualifies"] = (row["sharpe"] > spy["sharpe"] and row["max_dd"] > spy["max_dd"]
                            and row["sharpe_h1"] > spy["sharpe_h1"] and row["sharpe_h2"] > spy["sharpe_h2"])
    spy["qualifies"] = None
    winners = [r for r in main[1:] if r["qualifies"]]
    winner = max(winners, key=lambda r: r["cagr"])["name"] if winners else None
    # Stop/take-profit on Nasdaq 100: the owner chose "best risk-adjusted". A
    # variant must beat plain Nasdaq 100 buy-and-hold on Sharpe over the whole
    # period and in each half; the highest full-period Sharpe among those wins.
    qqq = next(r for r in table if r["name"] == "Nasdaq 100 (köp och behåll)")
    for row in table[len(STRATEGIES):]:
        row["qualifies"] = (row["sharpe"] > qqq["sharpe"] and row["sharpe_h1"] > qqq["sharpe_h1"]
                            and row["sharpe_h2"] > qqq["sharpe_h2"])
    exit_ok = [r for r in table[len(STRATEGIES):] if r["qualifies"]]
    exit_winner = max(exit_ok, key=lambda r: r["sharpe"])["name"] if exit_ok else None
    return {"table": table, "winner": winner, "exit_winner": exit_winner, "n_main": len(STRATEGIES), "start": str(start.date()), "end": str(closes.index[-1].date()),
            "mid": str(mid.date())}


def report(res: dict) -> str:
    t = res["table"]
    lines = [f"# Bot-kandidater: hela marknaden ({res['start']} – {res['end']})", "",
             "Köp/sälj vid nästa öppning efter månadens sista stängning, avgift på varje affär, utdelningar inräknade.",
             "Krav (bestämt innan testet): högre Sharpe än S&P 500 både hela perioden och i varje halva "
             f"(delning {res['mid']}), och mindre största nedgång. Högst årsavkastning bland de godkända vinner.", "",
             "| Strategi | Per år | Största nedgång | Sharpe | Sharpe 1:a/2:a halvan | Byten | Godkänd |",
             "|---|---|---|---|---|---|---|"]
    row_md = lambda r: (f"| {r['name']} | {r['cagr']:+.1f} % | {r['max_dd']:.0f} % | {r['sharpe']:.2f} | "
                        f"{r['sharpe_h1']:.2f} / {r['sharpe_h2']:.2f} | {r['switches']} | "
                        f"{'—' if r['qualifies'] is None else ('✅' if r['qualifies'] else '❌')} |")
    n = res.get("n_main", len(t))
    lines += [row_md(r) for r in t[:n]]
    lines += ["", f"**Vinnare enligt kraven:** {res['winner'] or 'ingen — behåll indexfonden'}", ""]
    if len(t) > n:
        lines += ["## Stop-loss och take-profit på Nasdaq 100", "",
                  "Stopp/mål kollas vid varje stängning och säljs vid nästa öppning; efter en försäljning ligger pengarna i "
                  "räntefond (BIL) och köper tillbaka vid en månadsstängning när Nasdaq 100 ligger över sitt 200-dagars snitt. "
                  "Krav (bestämt innan, ägarens val: bäst riskjusterat): högre Sharpe än Nasdaq 100 köp-och-behåll hela "
                  "perioden och i varje halva; högst Sharpe bland de godkända vinner.", "",
                  "| Strategi | Per år | Största nedgång | Sharpe | Sharpe 1:a/2:a halvan | Byten | Godkänd |",
                  "|---|---|---|---|---|---|---|"]
        qqq = next(r for r in t if r["name"] == "Nasdaq 100 (köp och behåll)")
        lines += [row_md({**qqq, "qualifies": None})] + [row_md(r) for r in t[n:]]
        lines += ["", f"**Bäst riskjusterat:** {res.get('exit_winner') or 'ingen — behåll Nasdaq 100 utan stopp'}", ""]
    t = t[:n]
    lines += [
              "## Per år (%)", "", "| År | " + " | ".join(r["name"] for r in t) + " |",
              "|---|" + "---|" * len(t)]
    for year in t[0]["years"].index:
        lines.append(f"| {year.year} | " + " | ".join(f"{r['years'].get(year, float('nan')):+.1f}" for r in t) + " |")
    lines += ["", "## Senaste 12 månaderna (%)", "", "| Månad | " + " | ".join(r["name"] for r in t) + " |",
              "|---|" + "---|" * len(t)]
    for month in t[0]["months"].index[-12:]:
        lines.append(f"| {month.strftime('%Y-%m')} | " + " | ".join(f"{r['months'].get(month, float('nan')):+.1f}" for r in t) + " |")
    lines += ["", "## 10 000 kr (i dollartermer, utan valutaeffekt) sedan 2026-09-25", ""]
    for r in t:
        eq = r["equity"]
        before = eq.loc[:"2026-09-25"]
        if not before.empty:
            lines.append(f"- {r['name']}: {10000 * eq.iloc[-1] / before.iloc[-1]:,.0f} kr".replace(",", " "))
    lines += ["", "Historik är ingen garanti. Inget av detta är ett löfte om vinst."]
    return "\n".join(lines)


def run(fee_bps: float = 15.0) -> str:
    from app.data.stock_client import StockClient

    opens, closes = {}, {}
    with StockClient() as client:
        for sym in SYMBOLS:
            bars = client.get_klines(sym, "1d", limit=5000)
            idx = pd.DatetimeIndex(bars["close_time"]).tz_convert("America/New_York").normalize().tz_localize(None)
            opens[sym] = pd.Series(bars["open"].values, index=idx)
            closes[sym] = pd.Series(bars["close"].values, index=idx)
    o, c = pd.DataFrame(opens).dropna(), pd.DataFrame(closes).dropna()
    return report(evaluate(o, c, fee_bps))
