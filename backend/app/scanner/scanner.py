"""Scanner orchestrator (sections 1, 14, 16):

    MARKET SCAN -> CANDIDATES -> MULTI-FACTOR ANALYSIS -> RISK/REWARD
    -> QUALITY FILTER -> RANKING -> SIGNAL or NO TRADE

Runs the full pipeline for every symbol in the watchlist, using one
strategy per symbol (the highest-scoring one) so a single asset never
produces duplicate alerts in the same scan. Any symbol whose data is
unavailable or stale is skipped and reported, never guessed at.
"""
from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, field

import pandas as pd

from app.config import settings
from app.data.binance_client import BinanceClient, DataUnavailable
from app.data.news_client import NewsResult, fetch_news
from app.features.indicators import compute_indicator_set
from app.features.structure import compute_structure_features
from app.features.volume import compute_volume_features
from app.regime.classifier import compute_regime_features, latest_snapshot, market_wide_risk_regime
from app.scoring.score import NO_TRADE, Signal, build_signal
from app.strategies import breakout, momentum, reversal

STRATEGIES = (breakout, momentum, reversal)
ANCHOR_SYMBOL = "BTCUSDT"


@dataclass
class SkippedSymbol:
    symbol: str
    reason: str


@dataclass
class ScanResult:
    scanned_at: str
    watchlist: list[str]
    market_wide_risk: str
    signals: list[Signal]
    skipped: list[SkippedSymbol] = field(default_factory=list)
    no_trade_summary: list[dict] = field(default_factory=list)

    @property
    def has_signals(self) -> bool:
        return len(self.signals) > 0


def _drop_unclosed_bar(df: pd.DataFrame, interval_seconds: int) -> pd.DataFrame:
    now = dt.datetime.now(dt.timezone.utc)
    return df[df["close_time"] <= now]


def _check_freshness(df: pd.DataFrame) -> str | None:
    if df.empty:
        return "no data returned"
    last_close_time = df["close_time"].iloc[-1]
    age_seconds = (dt.datetime.now(dt.timezone.utc) - last_close_time).total_seconds()
    if age_seconds > settings.max_data_age_seconds:
        return f"stale data — last closed candle is {age_seconds:.0f}s old (max {settings.max_data_age_seconds}s)"
    return None


def enrich(df: pd.DataFrame) -> pd.DataFrame:
    df = compute_indicator_set(df)
    df = compute_volume_features(df)
    df = compute_structure_features(df)
    df = compute_regime_features(df)
    return df


def scan_symbol(client: BinanceClient, symbol: str, interval: str) -> tuple[pd.DataFrame | None, str | None]:
    try:
        raw = client.get_klines(symbol, interval, limit=300)
    except DataUnavailable as exc:
        return None, str(exc)

    raw = _drop_unclosed_bar(raw, 0)
    freshness_issue = _check_freshness(raw)
    if freshness_issue:
        return None, freshness_issue

    if len(raw) < 210:
        return None, f"insufficient history for reliable indicators ({len(raw)} bars)"

    return enrich(raw), None


def run_scan(watchlist: list[str] | None = None, interval: str | None = None) -> ScanResult:
    watchlist = watchlist or list(settings.watchlist)
    interval = interval or settings.scan_interval
    scanned_at = dt.datetime.now(dt.timezone.utc).isoformat()

    skipped: list[SkippedSymbol] = []
    signals: list[Signal] = []
    no_trade_summary: list[dict] = []

    with BinanceClient() as client:
        anchor_df, anchor_error = scan_symbol(client, ANCHOR_SYMBOL, interval)
        anchor_snapshot = latest_snapshot(anchor_df) if anchor_df is not None else None
        market_wide_risk = market_wide_risk_regime(anchor_snapshot)

        symbols_to_scan = watchlist if ANCHOR_SYMBOL in watchlist else [ANCHOR_SYMBOL] + watchlist

        for symbol in symbols_to_scan:
            if symbol == ANCHOR_SYMBOL and anchor_df is not None:
                df, error = anchor_df, anchor_error
            elif symbol == ANCHOR_SYMBOL:
                df, error = None, anchor_error
            else:
                df, error = scan_symbol(client, symbol, interval)

            if error is not None or df is None:
                skipped.append(SkippedSymbol(symbol=symbol, reason=error or "unknown error"))
                continue

            snapshot = latest_snapshot(df)
            if snapshot is None:
                skipped.append(SkippedSymbol(symbol=symbol, reason="regime could not be determined (insufficient warmup)"))
                continue

            best_signal: Signal | None = None
            best_candidate_score = -1.0
            attempted_reasons: list[str] = []

            for strategy_module in STRATEGIES:
                candidate = strategy_module.generate(df, symbol)
                if candidate is None:
                    continue
                news: NewsResult = fetch_news(symbol) if settings.cryptopanic_api_key else NewsResult(
                    symbol=symbol, available=False, reason="CRYPTOPANIC_API_KEY not configured"
                )
                signal = build_signal(candidate, snapshot, news, market_wide_risk)
                attempted_reasons.append(f"{candidate.strategy}: score {signal.score:.1f}/100 ({signal.tier})")
                if signal.score > best_candidate_score:
                    best_candidate_score = signal.score
                    best_signal = signal

            if best_signal is None:
                no_trade_summary.append({"symbol": symbol, "reason": "no strategy found a qualifying setup", "regime": snapshot.label})
                continue

            if best_signal.tier == NO_TRADE:
                no_trade_summary.append(
                    {"symbol": symbol, "reason": f"best candidate scored {best_signal.score:.1f}/100 (below watch threshold)", "regime": snapshot.label}
                )
                continue

            signals.append(best_signal)

    signals.sort(key=lambda s: s.score, reverse=True)

    return ScanResult(
        scanned_at=scanned_at,
        watchlist=watchlist,
        market_wide_risk=market_wide_risk,
        signals=signals,
        skipped=skipped,
        no_trade_summary=no_trade_summary,
    )
