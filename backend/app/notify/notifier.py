"""Signal notification — "KÖP NU" on entry, "SÄLJ NU" on exit (section 15,
extended per user request).

Delivery is console logging + Telegram + an optional generic webhook.
Nothing in this module (or anywhere else in the system) places an order —
it notifies; a human decides.

Only LONG signals generate "KÖP NU" / "SÄLJ NU" alerts. This is a
spot/long-only accumulation workflow (buy, hold, sell into strength) —
a SHORT signal doesn't fit that framing (there's nothing to "sell" that
was never bought), so SHORT candidates still show up in the dashboard and
journal but do not push a Telegram alert. If you trade on margin/futures
and want SHORT alerts too, that's a small follow-up change.

The entry alert respects the optional "quiet hours" gate
(app.notify.trading_hours) — the exit alert never does, since once you're
in a position you want to know it closed regardless of the hour.
"""
from __future__ import annotations

import datetime as dt
import logging

import httpx

from app.config import settings
from app.db import SignalRecord
from app.notify import telegram_client
from app.notify.trading_hours import is_within_trading_hours
from app.scoring.score import Signal

logger = logging.getLogger("tradingbot.notify")


def _format_holding_duration(minutes: float) -> str:
    hours, mins = divmod(int(round(minutes)), 60)
    if hours and mins:
        return f"{hours}h {mins}m"
    if hours:
        return f"{hours}h"
    return f"{mins}m"


def format_entry_message(signal: Signal, historical_probability: dict | None = None) -> str:
    lines = [
        "🟢 KÖP NU",
        "",
        f"ASSET: {signal.symbol}",
        f"Score: {signal.score:.0f}/100 ({signal.tier.replace('_', ' ')}, {signal.strategy})",
        "",
        f"Entry: {signal.entry:g}",
        f"Target: {signal.target:g}  (+{signal.reward_pct:.2f}%)",
        f"Stop: {signal.stop:g}  (-{signal.risk_pct:.2f}%)",
        f"R/R: {signal.rr_ratio:.2f}",
        "",
        "Varför:",
    ]
    lines += [f"• {reason}" for reason in signal.reasons]
    lines += [
        "",
        f"Ogiltigförklaras vid: {signal.invalidation:g} ({signal.invalidation_reason})",
    ]

    if historical_probability and historical_probability.get("similar_setups"):
        hp = historical_probability
        lines.append("")
        lines.append(
            f"Historik: {hp['similar_setups']} liknande setups, target träffat {hp['target_hit_rate']:.0%}, "
            f"snittavkastning {hp['average_return_pct']:+.2f}%"
        )
        if hp.get("average_holding_minutes"):
            lines.append(f"Förväntad hålltid: ~{_format_holding_duration(hp['average_holding_minutes'])} (historiskt snitt)")
        if hp.get("common_hours_utc"):
            hours = ", ".join(f"{h:02d}:00" for h in hp["common_hours_utc"])
            lines.append(f"Vanligast vid (UTC): {hours}")
    else:
        lines += ["", "Ingen backtest på fil ännu för denna strategi/symbol — hålltid okänd."]

    if signal.warning:
        lines += ["", f"⚠ {signal.warning}"]

    lines += ["", "Jag bevakar nu den här positionen automatiskt och skickar SÄLJ NU när target eller stop nås."]
    return "\n".join(lines)


_RESULT_LABEL = {
    "TARGET_HIT": "✅ TARGET HIT",
    "STOP_HIT": "🛑 STOP HIT",
    "EXPIRED": "⏱ TID UTE (varken target eller stop nått)",
}


def format_exit_message(record: SignalRecord, update: dict) -> str:
    result = update["result"]
    if result == "TARGET_HIT":
        pnl = f"+{record.reward_pct:.2f}%"
    elif result == "STOP_HIT":
        pnl = f"-{record.risk_pct:.2f}%"
    else:
        mfe = update.get("max_favorable_excursion_pct") or 0.0
        mae = update.get("max_adverse_excursion_pct") or 0.0
        pnl = f"bäst +{mfe:.2f}% / sämst -{mae:.2f}% under perioden"

    lines = [
        "🔴 SÄLJ NU",
        "",
        f"ASSET: {record.symbol}",
        f"Resultat: {_RESULT_LABEL.get(result, result)} ({pnl})",
        f"Höll i: {_format_holding_duration(update['holding_time_minutes'])}",
        f"Max favorable/adverse excursion: +{update['max_favorable_excursion_pct']:.2f}% / -{update['max_adverse_excursion_pct']:.2f}%",
        "",
        f"Ursprunglig signal: {record.strategy}, score {record.score:.0f}/100, köpsignal {record.timestamp}",
    ]
    return "\n".join(lines)


def _deliver(message: str) -> None:
    logger.info("\n%s", message)
    telegram_client.send_message(message)
    if settings.notify_webhook_url:
        try:
            httpx.post(settings.notify_webhook_url, json={"text": message}, timeout=10.0)
        except httpx.HTTPError as exc:
            logger.warning("Failed to deliver webhook notification: %s", exc)


def notify_entry(signal: Signal, historical_probability: dict | None = None, *, min_score: float | None = None) -> bool:
    """Sends "KÖP NU" for a LONG signal at/above NOTIFY_MIN_SCORE, subject
    to the quiet-hours gate. Returns True if a delivery attempt was made
    (not necessarily that it succeeded — Telegram delivery failures are
    logged, not raised). `min_score` overrides settings.notify_min_score —
    exposed for tests, production callers should omit it."""
    min_score = settings.notify_min_score if min_score is None else min_score
    if signal.direction != "LONG":
        return False
    if signal.score < min_score:
        return False
    if not is_within_trading_hours():
        logger.info("Entry signal for %s suppressed by quiet-hours gate (still saved to journal).", signal.symbol)
        return False

    _deliver(format_entry_message(signal, historical_probability))
    return True


def notify_exit(record: SignalRecord, update: dict) -> None:
    """Sends "SÄLJ NU" the moment an open position resolves. Never gated
    by quiet hours — an open position closing is news you want regardless
    of the time."""
    if record.direction != "LONG":
        return
    _deliver(format_exit_message(record, update))


# Backwards-compatible aliases used by earlier call sites / external scripts.
format_signal_message = format_entry_message
notify = notify_entry
