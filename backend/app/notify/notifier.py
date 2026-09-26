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


def _evidence_line(evidence: dict | None) -> list[str]:
    if not evidence:
        return ["Historik: ingen backtest-statistik tillgänglig för den här typen av signal ännu."]
    if "n" in evidence:
        line = (
            f"Historik ({evidence.get('label', 'backtest')}): {evidence['n']} affärer, "
            f"{evidence['win_rate'] * 100:.0f}% vinnare, snitt {evidence['avg_r']:+.2f}R per affär"
        )
        if evidence.get("oos_n"):
            line += f" (senaste perioden: {evidence['oos_avg_r']:+.2f}R på {evidence['oos_n']} affärer)"
        return [line, "Historik är ingen garanti — varje enskild affär kan förlora."]
    if evidence.get("similar_setups"):  # older per-symbol backtest shape
        return [
            f"Historik: {evidence['similar_setups']} liknande setups, target träffat {evidence['target_hit_rate']:.0%}, "
            f"snittavkastning {evidence['average_return_pct']:+.2f}%"
        ]
    return []


def format_entry_message(signal: Signal, historical_probability: dict | None = None, size=None) -> str:
    from app.config import settings
    from app.risk.position_sizing import compute_position_size
    from app.runtime_settings import get_effective_settings

    live = get_effective_settings()
    if size is None:
        size = compute_position_size(signal.entry, signal.stop, live.portfolio_size_usd, live.risk_per_trade_pct,
                                     settings.max_position_pct)
    shares = int(size.units) if size.units >= 1 else round(size.units, 3)

    lines = [
        f"🟢 KÖP NU — {signal.symbol}",
        f"Strategi: {signal.strategy} · Score {signal.score:.0f}/100",
        "",
        f"Köp vid börsens öppning (senaste stängning {signal.entry:g})",
        f"Stop-loss: {signal.stop:g} (-{signal.risk_pct:.1f}%) ← lägg som stop-order direkt vid köp",
        f"Mål: {signal.target:g} (+{signal.reward_pct:.1f}%) ← lägg som limit-säljorder direkt vid köp",
        f"R/R: {signal.rr_ratio:.1f} · Säljs senast efter 90 handelsdagar om inget nås",
        "",
        f"Storlek: {shares} st ≈ ${size.position_size_usd:,.0f} ({size.position_pct_of_portfolio:.0f}% av portföljen) "
        f"→ max förlust vid stop ≈ ${size.risk_amount_usd:,.0f} "
        f"({size.risk_amount_usd / live.portfolio_size_usd * 100 if live.portfolio_size_usd else 0:.1f}% av ${live.portfolio_size_usd:,.0f})",
        "",
        "Varför:",
    ]
    lines += [f"• {reason}" for reason in signal.reasons]
    lines += [""] + _evidence_line(historical_probability)
    if signal.warning:
        lines += ["", f"⚠ {signal.warning}"]
    lines += ["", "Om aktien öppnar under stop-nivån: köp inte — signalen är då redan ogiltig."]
    return "\n".join(lines)


_RESULT_LABEL = {
    "TARGET_HIT": "✅ TARGET HIT",
    "STOP_HIT": "🛑 STOP HIT",
    "TIME_EXIT": "⏱ TID UTE",
    "EXPIRED": "⏱ TID UTE",
}


def format_exit_message(record: SignalRecord, update: dict) -> str:
    result = update["result"]
    ret = update.get("return_pct")
    r_mult = update.get("r_multiple")
    if ret is not None:
        pnl = f"{ret:+.1f}%" + (f" ({r_mult:+.1f}R)" if r_mult is not None else "")
    elif result == "TARGET_HIT":
        pnl = f"+{record.reward_pct:.1f}%"
    elif result == "STOP_HIT":
        pnl = f"-{record.risk_pct:.1f}%"
    else:
        pnl = f"bäst +{update.get('max_favorable_excursion_pct') or 0:.1f}% under perioden"

    lines = [
        f"🔴 SÄLJ NU — {record.symbol}",
        f"Resultat: {_RESULT_LABEL.get(result, result)} {pnl}",
    ]
    if update.get("fill_price") and update.get("exit_price"):
        lines.append(f"Köpt {update['fill_price']:g} → sålt {update['exit_price']:g}")
    if update.get("holding_bars"):
        lines.append(f"Hölls {update['holding_bars']} handelsdagar")
    else:
        lines.append(f"Höll i: {_format_holding_duration(update['holding_time_minutes'])}")
    if result in ("TARGET_HIT", "STOP_HIT"):
        lines.append("Om du lade stop-/limit-ordern vid köpet är detta redan utfört — annars: sälj nu.")
    else:
        lines.append("Varken mål eller stop nåddes inom 90 handelsdagar: sälj vid öppning.")
    lines.append(f"Signal: {record.strategy}, score {record.score:.0f}/100, {str(record.timestamp)[:10]}")
    return "\n".join(lines)


def _deliver(message: str) -> None:
    logger.info("\n%s", message)
    telegram_client.send_message(message)
    if settings.notify_webhook_url:
        try:
            httpx.post(settings.notify_webhook_url, json={"text": message}, timeout=10.0)
        except httpx.HTTPError as exc:
            logger.warning("Failed to deliver webhook notification: %s", exc)


def notify_entry(signal: Signal, historical_probability: dict | None = None, *, min_score: float | None = None, size=None) -> bool:
    """Sends "KÖP NU" for a LONG signal at/above NOTIFY_MIN_SCORE, subject
    to the quiet-hours gate. Returns True if a delivery attempt was made
    (not necessarily that it succeeded — Telegram delivery failures are
    logged, not raised). `min_score` overrides settings.notify_min_score —
    exposed for tests, production callers should omit it."""
    from app.runtime_settings import get_effective_settings

    min_score = get_effective_settings().notify_min_score if min_score is None else min_score
    if signal.direction != "LONG":
        return False
    if signal.score < min_score:
        return False
    if not is_within_trading_hours():
        logger.info("Entry signal for %s suppressed by quiet-hours gate (still saved to journal).", signal.symbol)
        return False

    _deliver(format_entry_message(signal, historical_probability, size))
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
