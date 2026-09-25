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
from app.data.earnings_calendar import earnings_warning
from app.data.news_client import NewsResult
from app.data.stock_client import DataUnavailable, StockClient
from app.features.indicators import compute_indicator_set
from app.features.structure import compute_structure_features
from app.features.volume import compute_volume_features
from app.regime.classifier import compute_regime_features, latest_snapshot, market_wide_risk_regime
from app.scoring.score import NO_TRADE, Signal, build_signal
from app.strategies import breakout, momentum, reversal

STRATEGIES = (breakout, momentum, reversal)
# SPY (S&P 500 ETF) as the market-wide risk anchor — the standard equity
# proxy for broad risk appetite, same role BTC played for the crypto
# version of this scanner.
ANCHOR_SYMBOL = "SPY"


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
    spy_above_200: bool | None = None

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


def scan_symbol(client: StockClient, symbol: str, interval: str) -> tuple[pd.DataFrame | None, str | None]:
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


def _above_sma200(df: pd.DataFrame) -> bool:
    row = df.iloc[-1]
    return bool(pd.notna(row.get("sma_200")) and float(row["close"]) > float(row["sma_200"]))


def run_scan(
    watchlist: list[str] | None = None,
    interval: str | None = None,
    *,
    client: StockClient | None = None,
    strategies=None,
    long_only: bool = True,
) -> ScanResult:
    """Scans the universe and keeps the best-scoring setup per symbol.
    `strategies` restricts which strategy modules may produce signals (the
    live policy passes only the ones research supports); `long_only`
    ignores SHORT setups so a short can never crowd out a long on the same
    symbol for a long-only trader."""
    from app.runtime_settings import get_effective_settings

    watchlist = watchlist or list(get_effective_settings().watchlist)
    interval = interval or settings.scan_interval
    strategies = strategies or STRATEGIES
    scanned_at = dt.datetime.now(dt.timezone.utc).isoformat()

    skipped: list[SkippedSymbol] = []
    signals: list[Signal] = []
    no_trade_summary: list[dict] = []

    client = client or StockClient()
    symbols_to_scan = watchlist if ANCHOR_SYMBOL in watchlist else [ANCHOR_SYMBOL] + watchlist
    client.prefetch(symbols_to_scan, interval, limit=300)

    anchor_df, anchor_error = scan_symbol(client, ANCHOR_SYMBOL, interval)
    anchor_snapshot = latest_snapshot(anchor_df) if anchor_df is not None else None
    market_wide_risk = market_wide_risk_regime(anchor_snapshot)
    spy_above_200 = _above_sma200(anchor_df) if anchor_df is not None else None

    for symbol in symbols_to_scan:
        if symbol == ANCHOR_SYMBOL:
            continue
        df, error = scan_symbol(client, symbol, interval)
        if error is not None or df is None:
            skipped.append(SkippedSymbol(symbol=symbol, reason=error or "unknown error"))
            continue

        snapshot = latest_snapshot(df)
        if snapshot is None:
            skipped.append(SkippedSymbol(symbol=symbol, reason="regime could not be determined (insufficient warmup)"))
            continue

        best_signal: Signal | None = None
        for strategy_module in strategies:
            candidate = strategy_module.generate(df, symbol)
            if candidate is None or (long_only and candidate.direction != "LONG"):
                continue
            # No stock news provider is wired up: catalyst honestly scores 0.
            news = NewsResult(symbol=symbol, available=False, reason="no stock news provider configured")
            signal = build_signal(candidate, snapshot, news, market_wide_risk)
            if best_signal is None or signal.score > best_signal.score:
                best_signal = signal

        if best_signal is None:
            no_trade_summary.append({"symbol": symbol, "reason": "no strategy found a qualifying setup", "regime": snapshot.label})
            continue
        if best_signal.tier == NO_TRADE:
            no_trade_summary.append(
                {"symbol": symbol, "reason": f"best candidate scored {best_signal.score:.1f}/100 (below watch threshold)", "regime": snapshot.label}
            )
            continue

        best_signal.context = {
            "stock_above_200": _above_sma200(df),
            "spy_above_200": spy_above_200,
            "last_close": float(df["close"].iloc[-1]),
            "atr_pct": round(float(df["atr_14"].iloc[-1] / df["close"].iloc[-1] * 100), 2),
        }
        # Additive only — no warning never means "confirmed no earnings".
        if best_signal.direction == "LONG":
            earnings_note = earnings_warning(symbol)
            if earnings_note:
                best_signal.reasons.append(f"⚠ {earnings_note}")
                best_signal.warning = f"{best_signal.warning} | {earnings_note}" if best_signal.warning else earnings_note
                best_signal.context["earnings_soon"] = True

        signals.append(best_signal)

    signals.sort(key=lambda s: s.score, reverse=True)

    return ScanResult(
        scanned_at=scanned_at,
        watchlist=watchlist,
        market_wide_risk=market_wide_risk,
        signals=signals,
        skipped=skipped,
        no_trade_summary=no_trade_summary,
        spy_above_200=spy_above_200,
    )
