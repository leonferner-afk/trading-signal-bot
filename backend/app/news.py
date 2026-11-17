"""News check for rockets — information only, it never changes a buy or sell.

The owner asked (2026-11-17) for news and social-media context, to judge
whether a rocket looks like a one-day spike. Whether such context improves
the rule can't be backtested (no affordable history of posts), so it is shown
next to each rocket and nothing more:

  * the latest company headlines from Finnhub's free company-news endpoint
    (needs the FINNHUB_API_KEY secret; without it: no headlines, said so);
  * how many Reddit posts from the last 24 hours mention the ticker in the
    title (Reddit's public search, no key; rough, and None when Reddit
    refuses the request).

Every failure is reported as missing data, never guessed.
"""
from __future__ import annotations

import datetime as dt
import logging
import os
import re

import httpx

logger = logging.getLogger("tradingbot.news")

FINNHUB_NEWS = "https://finnhub.io/api/v1/company-news"
REDDIT_SEARCH = "https://www.reddit.com/search.json"
USER_AGENT = "trading-signal-bot/1.0 (paper-trading research; github.com/leonferner-afk/trading-signal-bot)"


def headlines(symbol: str, today: dt.date, client: httpx.Client, limit: int = 3, days: int = 4) -> list[dict] | None:
    """Newest company headlines (Finnhub). None = no key or the request failed."""
    key = os.environ.get("FINNHUB_API_KEY", "").strip()
    if not key:
        return None
    try:
        res = client.get(FINNHUB_NEWS, params={"symbol": symbol, "from": str(today - dt.timedelta(days=days)),
                                               "to": str(today), "token": key}, timeout=15)
        res.raise_for_status()
        items = res.json()
    except (httpx.HTTPError, ValueError) as exc:
        logger.warning("Finnhub news for %s failed: %s", symbol, exc)
        return None
    if not isinstance(items, list):
        return None
    items = sorted((i for i in items if i.get("headline")), key=lambda i: i.get("datetime") or 0, reverse=True)
    out, seen = [], set()
    for i in items:
        title = i["headline"].strip()
        if title.lower() in seen:
            continue
        seen.add(title.lower())
        out.append({"headline": title[:160], "source": (i.get("source") or "")[:40], "url": i.get("url") or "",
                    "date": dt.datetime.fromtimestamp(i["datetime"], dt.timezone.utc).strftime("%Y-%m-%d")
                    if i.get("datetime") else None})
        if len(out) >= limit:
            break
    return out


def reddit_mentions(symbol: str, client: httpx.Client) -> int | None:
    """Posts in the last 24 h whose title names the ticker (as $SYM or the bare
    word). Rough: Reddit's search is fuzzy. None when Reddit refuses."""
    try:
        res = client.get(REDDIT_SEARCH, params={"q": symbol, "sort": "new", "t": "day", "limit": 100},
                         headers={"User-Agent": USER_AGENT}, timeout=15)
        res.raise_for_status()
        posts = res.json()["data"]["children"]
    except (httpx.HTTPError, ValueError, KeyError, TypeError) as exc:
        logger.warning("Reddit search for %s failed: %s", symbol, exc)
        return None
    pattern = re.compile(rf"(?<![A-Za-z0-9])\$?{re.escape(symbol)}(?![A-Za-z0-9])")
    return sum(1 for p in posts if pattern.search((p.get("data") or {}).get("title") or ""))


def news_for(symbols: list[str], today: dt.date | None = None) -> dict[str, dict]:
    """{symbol: {"headlines": [...] | None, "reddit_24h": int | None, "checked": date}}."""
    today = today or dt.datetime.now(dt.timezone.utc).date()
    out = {}
    with httpx.Client() as client:
        for sym in sorted(set(symbols)):
            out[sym] = {"headlines": headlines(sym, today, client), "reddit_24h": reddit_mentions(sym, client),
                        "checked": str(today)}
    return out
