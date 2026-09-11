"""CRUD layer over the trade journal (section 17) — the only place that
writes SignalRecord/BacktestRun rows, so persistence logic stays in one
place.
"""
from __future__ import annotations

import dataclasses
import json

from sqlalchemy import select

from app.db import BacktestRun, SignalRecord, get_session
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
        session.commit()


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
        stmt = select(SignalRecord).where(SignalRecord.result != "OPEN")
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

    wins = [r for r in closed if r.result == "TARGET_HIT"]
    losses = [r for r in closed if r.result == "STOP_HIT"]

    def signed_return(r: SignalRecord) -> float:
        pct = r.reward_pct if r.result == "TARGET_HIT" else -r.risk_pct
        return pct if r.direction == "LONG" else pct  # risk/reward already direction-adjusted

    returns = [signed_return(r) for r in closed]
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
            if r.result == "TARGET_HIT":
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
        "by_regime": by_regime,
        "by_strategy": by_strategy,
        "note": None,
    }
