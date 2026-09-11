"""Thin, real Telegram Bot API client for delivering notifications.

Setup (do this once, takes ~2 minutes):
  1. Message @BotFather on Telegram, send /newbot, follow the prompts.
     You'll get a bot token like `123456789:AAF...`.
  2. Message your new bot anything (so it's allowed to message you back).
  3. Fetch https://api.telegram.org/bot<token>/getUpdates in a browser to
     find your numeric chat_id in the response.
  4. Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in .env.

If either is missing, `send_message` returns False and logs a warning —
it never raises, so a Telegram outage can't take down the scanner.
"""
from __future__ import annotations

import logging

import httpx

from app.config import settings

logger = logging.getLogger("sagoton.telegram")

API_BASE = "https://api.telegram.org"


def is_configured() -> bool:
    return bool(settings.telegram_bot_token and settings.telegram_chat_id)


def send_message(text: str, timeout: float = 10.0) -> bool:
    if not is_configured():
        logger.warning("Telegram not configured (TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID missing) — skipping delivery.")
        return False
    url = f"{API_BASE}/bot{settings.telegram_bot_token}/sendMessage"
    try:
        response = httpx.post(
            url,
            json={
                "chat_id": settings.telegram_chat_id,
                "text": text,
                "disable_web_page_preview": True,
            },
            timeout=timeout,
        )
        response.raise_for_status()
        return True
    except (httpx.HTTPError, httpx.TransportError) as exc:
        logger.warning("Telegram delivery failed: %s", exc)
        return False
