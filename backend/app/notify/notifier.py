"""Signal notification (section 15).

Formats and delivers a human-readable alert for HIGH_QUALITY/EXCEPTIONAL
signals. Delivery is console logging plus an OPTIONAL outbound webhook —
there is no code path anywhere in this module (or anywhere else in the
system) that places an order. It notifies; a human decides.
"""
from __future__ import annotations

import logging

import httpx

from app.config import settings
from app.scoring.score import Signal

logger = logging.getLogger("sagoton.notify")


def format_signal_message(signal: Signal, historical_probability: dict | None = None) -> str:
    emoji = "🚨" if signal.tier == "EXCEPTIONAL" else "⚠️"
    lines = [
        f"{emoji} {signal.tier.replace('_', ' ')} SETUP",
        "",
        f"ASSET: {signal.symbol}",
        f"Direction: {signal.direction}",
        "",
        f"Entry: {signal.entry:g}",
        "",
        f"Target: {signal.target:g}",
        f"Stop: {signal.stop:g}",
        "",
        f"Potential: +{signal.reward_pct:.2f}%",
        f"Risk: -{signal.risk_pct:.2f}%",
        "",
        f"R/R: {signal.rr_ratio:.2f}",
        "",
        f"Score: {signal.score:.0f}/100 ({signal.strategy})",
        "",
        "Why:",
    ]
    lines += [f"• {reason}" for reason in signal.reasons]
    lines += [
        "",
        f"Invalidation:",
        f"{signal.invalidation:g} ({signal.invalidation_reason})",
        "",
        "Time horizon:",
        "Intraday / 24h",
    ]
    if signal.warning:
        lines += ["", f"⚠ {signal.warning}"]
    if historical_probability and historical_probability.get("similar_setups"):
        lines += [
            "",
            "BACKTEST:",
            f"Similar setups: {historical_probability['similar_setups']}",
            f"Target hit: {historical_probability['target_hit_rate']:.0%}",
            f"Average return: {historical_probability['average_return_pct']:+.2f}%",
        ]
    else:
        lines += ["", "BACKTEST:", "No historical backtest on file for this strategy/symbol yet."]
    if not signal.news_available:
        lines += ["", "(No news data source configured — catalyst score is 0/10, not assumed.)"]
    return "\n".join(lines)


def notify(signal: Signal, historical_probability: dict | None = None) -> None:
    """Delivers a notification for signals at or above NOTIFY_MIN_SCORE.
    Never trades — logs to console and, if configured, posts to a webhook."""
    if signal.score < settings.notify_min_score:
        return

    message = format_signal_message(signal, historical_probability)
    logger.info("\n%s", message)

    if settings.notify_webhook_url:
        try:
            httpx.post(settings.notify_webhook_url, json={"text": message}, timeout=10.0)
        except httpx.HTTPError as exc:
            logger.warning("Failed to deliver webhook notification for %s: %s", signal.symbol, exc)
