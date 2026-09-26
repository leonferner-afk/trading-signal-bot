"""Paper trading: follows every BUY signal forward on real market data and
records what actually happened, using exactly the backtest's rules so the
live track record and the research are comparable:

  - bought at the open of the first session after the signal (the earliest
    anyone acting on the notification could buy), fees + slippage included
  - if that open is already below the stop (or above the target) the setup
    never became a trade: SKIPPED_GAP
  - sold at the stop/target, or at the open if the stock gapped through it
  - closed at the close after MAX_HOLDING_BARS sessions if neither level hit

A symbol whose data can't be fetched stays OPEN and is reported as not
updated — an outcome is never assumed.
"""
from __future__ import annotations

import pandas as pd

from app.backtest.engine import MAX_HOLDING_BARS_DEFAULT, net_return_pct, resolve_exit
from app.config import settings
from app.data.stock_client import DataUnavailable, StockClient
from app.db import SignalRecord

SKIPPED_GAP = "SKIPPED_GAP"


def _parse_timestamp(value: str) -> pd.Timestamp:
    ts = pd.Timestamp(value)
    return ts.tz_localize("UTC") if ts.tzinfo is None else ts.tz_convert("UTC")


def _bars_after_signal(client: StockClient, record: SignalRecord) -> tuple[pd.DataFrame, pd.DataFrame] | None:
    try:
        df = client.get_klines(record.symbol, "1d", limit=400)
    except DataUnavailable:
        return None
    return df, df[df["close_time"] > _parse_timestamp(record.timestamp)]


def price_adjustment(df: pd.DataFrame, record: SignalRecord) -> float:
    """Factor by which the data provider has re-based this stock's history
    since the signal (splits; dividend adjustments are tiny): the signal
    bar's close in today's data divided by the entry close we stored. The
    stored stop/target are multiplied by it, so a 10:1 split doesn't read
    as a stop hit. 1.0 when the signal bar can't be found."""
    bar = df[df["close_time"] <= _parse_timestamp(record.timestamp)]
    if bar.empty or not record.entry:
        return 1.0
    factor = float(bar["close"].iloc[-1]) / float(record.entry)
    return factor if factor > 0 and abs(factor - 1) > 1e-4 else 1.0


def evaluate_open_signal(client: StockClient, record: SignalRecord, max_holding_bars: int = MAX_HOLDING_BARS_DEFAULT) -> dict | None:
    """Update dict if the position resolved (or never filled), else None
    (still open, or data unavailable)."""
    bars = _bars_after_signal(client, record)
    if bars is None or bars[1].empty:
        return None
    df, after = bars
    k = price_adjustment(df, record)
    entry, stop, target = record.entry * k, record.stop * k, record.target * k

    opens, highs, lows, closes = (after[c].to_numpy(dtype=float) for c in ("open", "high", "low", "close"))
    fill = float(opens[0])
    exit_ = resolve_exit(opens, highs, lows, closes, 0, record.direction, stop, target, max_holding_bars)

    if exit_ is None:
        return {
            "result": SKIPPED_GAP, "fill_price": round(fill, 4), "exit_price": None, "return_pct": None,
            "r_multiple": None, "max_favorable_excursion_pct": 0.0, "max_adverse_excursion_pct": 0.0,
            "holding_time_minutes": 0.0, "holding_bars": 0, "closed_at": after["close_time"].iloc[0].to_pydatetime(),
        }
    # Ran out of data before the holding cap: still open, not a time exit.
    if exit_.result == "TIME_EXIT" and len(after) <= max_holding_bars:
        return None

    ret = net_return_pct(fill, exit_.raw_price, record.direction, settings.fee_bps, settings.slippage_bps)
    planned_risk = abs(entry - stop)
    fill_with_costs = fill * (1 + (settings.fee_bps + settings.slippage_bps) / 10000.0)
    closed_at = after["close_time"].iloc[exit_.index]
    return {
        "result": exit_.result,
        "fill_price": round(fill, 4),
        "exit_price": round(exit_.raw_price, 4),
        "return_pct": round(ret, 3),
        "r_multiple": round(ret / 100 * fill_with_costs / planned_risk, 3) if planned_risk > 0 else None,
        "max_favorable_excursion_pct": round(exit_.mfe_pct, 3),
        "max_adverse_excursion_pct": round(exit_.mae_pct, 3),
        "holding_time_minutes": round((closed_at - _parse_timestamp(record.timestamp)).total_seconds() / 60.0, 1),
        "holding_bars": exit_.index + 1,
        "closed_at": closed_at.to_pydatetime(),
    }


def current_mark(client: StockClient, record: SignalRecord) -> dict | None:
    """Unrealized state of a still-open position, for the daily report."""
    bars = _bars_after_signal(client, record)
    if bars is None:
        return None
    df, after = bars
    last_close = float(df["close"].iloc[-1])
    if after.empty:
        return {"last_close": last_close, "fill_price": None, "unrealized_pct": None, "sessions_held": 0}
    fill = float(after["open"].iloc[0])
    return {
        "last_close": last_close,
        "fill_price": fill,
        "unrealized_pct": round((last_close - fill) / fill * 100, 2),
        "sessions_held": len(after),
    }


def run_paper_trading_update(interval: str | None = None, client: StockClient | None = None) -> dict:
    """Resolves every OPEN signal against fresh data and fires "SÄLJ NU"
    for each that closed. `interval` is accepted for API compatibility;
    positions are always evaluated on daily bars, like the backtest."""
    from app.journal.repository import close_signal, get_open_signals
    from app.notify.notifier import notify_exit

    open_records = get_open_signals()
    if client is None:
        client = StockClient()
        if open_records:
            client.prefetch([r.symbol for r in open_records], "1d", limit=400)

    updated, unavailable = [], []
    for record in open_records:
        update = evaluate_open_signal(client, record)
        if update is None:
            if _bars_after_signal(client, record) is None:
                unavailable.append(record.symbol)
            continue
        close_signal(
            record.id, update["result"],
            update["max_favorable_excursion_pct"], update["max_adverse_excursion_pct"],
            update["holding_time_minutes"], update["closed_at"],
            fill_price=update["fill_price"], exit_price=update["exit_price"],
            return_pct=update["return_pct"], r_multiple=update["r_multiple"],
        )
        if update["result"] != SKIPPED_GAP:
            notify_exit(record, update)
        updated.append({"id": record.id, "symbol": record.symbol, "strategy": record.strategy,
                        **{k: v for k, v in update.items() if k != "closed_at"}})

    return {"checked": len(open_records), "updated": updated, "still_open_or_unavailable": unavailable}
