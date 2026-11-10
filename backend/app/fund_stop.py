"""The owner's paper depot fund (Nasdaq 100) with a trailing stop — the rule
that won the stop-loss backtest (app/bot_research.py, 2008–2026, chosen by
the owner on 2026-11-10 as "best risk-adjusted"):

  * held from the tracker's start close;
  * a close more than `trail` below the highest close since the (re)entry
    -> sell at the next session's open, money waits in kronor (no interest);
  * re-enter at the open after a month-end close above the 200-day average;
  * FEE_BPS on each side.

Replayed from the start on every run from daily bars and USD/SEK, so it needs
no stored state and can always be checked. A signal on the latest close is
reported as pending (it executes at the next open, after the report).
"""
from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd

from app.hypothetical import fx_rate_on

WINDOW = 200


@dataclass
class FundStop:
    value_sek: float | None             # value now, at the latest close (None = data missing)
    holding: bool                       # in the fund (True) or in kronor after a stop (False)
    trail: float
    peak_price: float | None = None     # highest close since the last entry (USD)
    stop_price: float | None = None     # a close at or below this sells
    last_price: float | None = None
    pending: str | None = None          # "sell" / "buy" at the next open, signalled on the latest close
    events: list[dict] = field(default_factory=list)

    def as_dict(self) -> dict:
        return {"value_sek": None if self.value_sek is None else round(self.value_sek, 2), "holding": self.holding,
                "trail_pct": round(self.trail * 100, 2),
                "peak_price": self.peak_price, "stop_price": None if self.stop_price is None else round(self.stop_price, 2),
                "last_price": self.last_price, "pending": self.pending, "events": self.events}


def _month_end_flags(days: pd.DatetimeIndex) -> list[bool]:
    """A session is a month-end once the next session is in a new month (the
    latest session is never one yet: its month may continue)."""
    ym = [(d.year, d.month) for d in days]
    return [i + 1 < len(days) and ym[i + 1] != ym[i] for i in range(len(days))]


def simulate(bars: pd.DataFrame, fx: pd.DataFrame, start_ts: pd.Timestamp, stake_sek: float,
             trail: float = 0.15, fee_bps: float = 15.0) -> FundStop:
    """`bars`: the fund's daily bars (finished sessions only), `fx`: USD/SEK."""
    fee = fee_bps / 10000.0
    bars = bars.reset_index(drop=True)
    start = bars.index[bars["close_time"] <= start_ts]
    if len(start) == 0 or fx is None:
        return FundStop(None, True, trail)
    i0 = int(start[-1])
    closes, opens, times = bars["close"].astype(float), bars["open"].astype(float), bars["close_time"]
    days = pd.DatetimeIndex(times.dt.tz_convert("America/New_York").dt.tz_localize(None).dt.normalize())
    month_end = _month_end_flags(days)
    sma = closes.rolling(WINDOW).mean()

    fx0 = fx_rate_on(fx, times.iloc[i0])
    if not fx0:
        return FundStop(None, True, trail)
    units, cash = stake_sek / (closes.iloc[i0] * fx0), 0.0          # bought at the start close, like the tracker
    holding, peak, pending, events = True, closes.iloc[i0], None, []
    for i in range(i0 + 1, len(bars)):
        rate = fx_rate_on(fx, times.iloc[i])
        if not rate:
            return FundStop(None, holding, trail)
        day = str(days[i].date())
        if pending == "sell":
            cash = units * opens.iloc[i] * rate * (1 - fee)
            units, holding = 0.0, False
            events.append({"type": "sell", "date": day, "price": round(float(opens.iloc[i]), 2), "value_sek": round(cash, 2)})
        elif pending == "buy":
            units = cash * (1 - fee) / (opens.iloc[i] * rate)
            cash, holding, peak = 0.0, True, opens.iloc[i]
            events.append({"type": "buy", "date": day, "price": round(float(opens.iloc[i]), 2),
                           "value_sek": round(units * opens.iloc[i] * rate, 2)})
        pending = None
        c = closes.iloc[i]
        if holding:
            peak = max(peak, c)
            if c <= peak * (1 - trail):
                pending = "sell"
                events.append({"type": "sell_signal", "date": day, "price": round(float(c), 2),
                               "peak": round(float(peak), 2)})
        elif month_end[i] and pd.notna(sma.iloc[i]) and c > sma.iloc[i]:
            pending = "buy"
            events.append({"type": "buy_signal", "date": day, "price": round(float(c), 2),
                           "sma200": round(float(sma.iloc[i]), 2)})
    last_rate = fx_rate_on(fx, times.iloc[-1])
    value = units * closes.iloc[-1] * last_rate if holding else cash
    return FundStop(value, holding, trail, peak_price=round(float(peak), 2) if holding else None,
                    stop_price=float(peak) * (1 - trail) if holding else None,
                    last_price=round(float(closes.iloc[-1]), 2), pending=pending, events=events)
