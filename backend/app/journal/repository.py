"""CRUD layer over the trade journal (section 17) — the only place that
writes SignalRecord/BacktestRun rows, so persistence logic stays in one
place.
"""
from __future__ import annotations

import dataclasses
import json

from sqlalchemy import select

from app.db import BacktestRun, BotRun, SignalRecord, get_session
from app.scoring.score import Signal


def has_open_signal(symbol: str, strategy: str, direction: str) -> bool:
    """True if there is already an OPEN journal entry for this exact
    symbol/strategy/direction combination. Used to avoid re-alerting
    ("köp nu" spam) for a setup that is still active from a previous scan
    — the position is already being watched for its exit."""
    with get_session() as session:
        stmt = select(SignalRecord).where(
            SignalRecord.symbol == symbol,
            SignalRecord.strategy == strategy,
            SignalRecord.direction == direction,
            SignalRecord.result == "OPEN",
        )
        return session.scalars(stmt).first() is not None


def has_open_position(symbol: str) -> bool:
    """True if any strategy already holds an OPEN long on this symbol — the
    bot never tells you to buy the same stock twice at once."""
    with get_session() as session:
        stmt = select(SignalRecord).where(
            SignalRecord.symbol == symbol, SignalRecord.direction == "LONG", SignalRecord.result == "OPEN"
        )
        return session.scalars(stmt).first() is not None


def save_signal(signal: Signal, historical_probability: dict | None = None) -> int:
    with get_session() as session:
        record = SignalRecord(
            timestamp=signal.timestamp,
            symbol=signal.symbol,
            direction=signal.direction,
            strategy=signal.strategy,
            entry=signal.entry,
            target=signal.target,
            stop=signal.stop,
            risk_pct=signal.risk_pct,
            reward_pct=signal.reward_pct,
            rr_ratio=signal.rr_ratio,
            score=signal.score,
            tier=signal.tier,
            market_regime=signal.regime_label,
            market_wide_risk=signal.market_wide_risk,
            features_json=json.dumps(
                {
                    "breakdown": dataclasses.asdict(signal.breakdown),
                    "reasons": signal.reasons,
                    "invalidation": signal.invalidation,
                    "invalidation_reason": signal.invalidation_reason,
                    "target_reason": signal.target_reason,
                    "realistic": signal.realistic,
                    "warning": signal.warning,
                }
            ),
            news_json=json.dumps({"available": signal.news_available}),
            historical_probability_json=json.dumps(historical_probability or {}),
            result="OPEN",
        )
        session.add(record)
        session.commit()
        return record.id


def list_signals(limit: int = 100) -> list[SignalRecord]:
    with get_session() as session:
        stmt = select(SignalRecord).order_by(SignalRecord.created_at.desc()).limit(limit)
        return list(session.scalars(stmt))


def get_open_signals() -> list[SignalRecord]:
    with get_session() as session:
        stmt = select(SignalRecord).where(SignalRecord.result == "OPEN")
        return list(session.scalars(stmt))


def close_signal(
    signal_id: int,
    result: str,
    max_favorable_excursion_pct: float,
    max_adverse_excursion_pct: float,
    holding_time_minutes: float,
    closed_at,
    *,
    fill_price: float | None = None,
    exit_price: float | None = None,
    return_pct: float | None = None,
    r_multiple: float | None = None,
) -> None:
    with get_session() as session:
        record = session.get(SignalRecord, signal_id)
        if record is None:
            return
        record.result = result
        record.max_favorable_excursion_pct = max_favorable_excursion_pct
        record.max_adverse_excursion_pct = max_adverse_excursion_pct
        record.holding_time_minutes = holding_time_minutes
        record.closed_at = closed_at
        record.fill_price = fill_price
        record.exit_price = exit_price
        record.return_pct = return_pct
        record.r_multiple = r_multiple
        session.commit()


def realized_return_pct(record: SignalRecord) -> float:
    """Actual outcome when it was measured from real fills; otherwise the
    planned target/stop distance (older rows, before fills were tracked)."""
    if record.return_pct is not None:
        return record.return_pct
    if record.result == "TARGET_HIT":
        return record.reward_pct
    if record.result == "STOP_HIT":
        return -record.risk_pct
    return 0.0


def save_backtest_run(
    symbol: str,
    interval: str,
    strategy: str,
    start: str,
    end: str,
    split: dict,
    walk_forward: dict,
    reliable: bool,
    reliability_reason: str,
    timing_pattern: dict | None = None,
) -> int:
    with get_session() as session:
        record = BacktestRun(
            symbol=symbol,
            interval=interval,
            strategy=strategy,
            start=start,
            end=end,
            split_json=json.dumps(split),
            walk_forward_json=json.dumps(walk_forward),
            reliable=reliable,
            reliability_reason=reliability_reason,
            timing_pattern_json=json.dumps(timing_pattern or {}),
        )
        session.add(record)
        session.commit()
        return record.id


def list_backtest_runs(limit: int = 50) -> list[BacktestRun]:
    with get_session() as session:
        stmt = select(BacktestRun).order_by(BacktestRun.created_at.desc()).limit(limit)
        return list(session.scalars(stmt))


def performance_summary() -> dict:
    """Aggregate performance strictly from CLOSED signals — an empty
    journal returns an honest empty summary, never fabricated stats."""
    with get_session() as session:
        stmt = select(SignalRecord).where(SignalRecord.result.notin_(("OPEN", "SKIPPED_GAP"))).order_by(SignalRecord.closed_at)
        closed = list(session.scalars(stmt))

    if not closed:
        return {
            "signals_total": 0,
            "closed_total": 0,
            "wins": 0,
            "losses": 0,
            "win_rate": None,
            "average_return_pct": None,
            "expectancy_pct": None,
            "profit_factor": None,
            "max_drawdown_pct": None,
            "by_regime": {},
            "by_strategy": {},
            "note": "No closed signals yet — performance stats require paper-traded or backtested outcomes.",
        }

    returns = [realized_return_pct(r) for r in closed]
    wins = [r for r, ret in zip(closed, returns) if ret > 0]
    losses = [r for r, ret in zip(closed, returns) if ret <= 0]
    r_multiples = [r.r_multiple for r in closed if r.r_multiple is not None]
    gains = [r for r in returns if r > 0]
    lossses = [abs(r) for r in returns if r < 0]

    win_rate = len(wins) / len(closed) if closed else None
    avg_return = sum(returns) / len(returns) if returns else None
    profit_factor = (sum(gains) / sum(lossses)) if lossses and sum(lossses) > 0 else None
    expectancy = avg_return

    equity_curve = []
    running = 0.0
    for r in returns:
        running += r
        equity_curve.append(running)
    peak = float("-inf")
    max_dd = 0.0
    for value in equity_curve:
        peak = max(peak, value)
        max_dd = min(max_dd, value - peak)

    by_regime: dict[str, dict] = {}
    by_strategy: dict[str, dict] = {}
    for r in closed:
        for bucket, key in ((by_regime, r.market_regime), (by_strategy, r.strategy)):
            entry = bucket.setdefault(key, {"count": 0, "wins": 0})
            entry["count"] += 1
            if realized_return_pct(r) > 0:
                entry["wins"] += 1
    for bucket in (by_regime, by_strategy):
        for key, entry in bucket.items():
            entry["win_rate"] = entry["wins"] / entry["count"] if entry["count"] else None

    return {
        "signals_total": len(closed),
        "closed_total": len(closed),
        "wins": len(wins),
        "losses": len(losses),
        "win_rate": round(win_rate, 4) if win_rate is not None else None,
        "average_return_pct": round(avg_return, 3) if avg_return is not None else None,
        "expectancy_pct": round(expectancy, 3) if expectancy is not None else None,
        "profit_factor": round(profit_factor, 3) if profit_factor is not None else None,
        "max_drawdown_pct": round(max_dd, 3),
        "average_r": round(sum(r_multiples) / len(r_multiples), 3) if r_multiples else None,
        "total_r": round(sum(r_multiples), 3) if r_multiples else None,
        "by_regime": by_regime,
        "by_strategy": by_strategy,
        "note": None,
    }


def equity_curve() -> list[dict]:
    """Chronological, per-closed-signal cumulative return series — real
    outcomes only (paper-traded or backtested), plotted as they happened
    over time so the dashboard can show whether the edge is actually
    holding, not just an aggregate number. Empty until signals have closed."""
    with get_session() as session:
        stmt = select(SignalRecord).where(SignalRecord.result.notin_(("OPEN", "SKIPPED_GAP"))).order_by(SignalRecord.closed_at)
        closed = list(session.scalars(stmt))

    points = []
    running = 0.0
    for r in closed:
        pct = realized_return_pct(r)
        running += pct
        points.append(
            {
                "closed_at": r.closed_at.isoformat() if r.closed_at else None,
                "symbol": r.symbol,
                "strategy": r.strategy,
                "result": r.result,
                "trade_return_pct": round(pct, 3),
                "cumulative_return_pct": round(running, 3),
            }
        )
    return points


def last_processed_session() -> str | None:
    with get_session() as session:
        row = session.execute(select(BotRun).order_by(BotRun.session_date.desc()).limit(1)).scalar_one_or_none()
        return row.session_date if row else None


def record_bot_run(session_date: str, buys: int, exits: int) -> None:
    with get_session() as session:
        session.add(BotRun(session_date=session_date, buys=buys, exits=exits))
        session.commit()
