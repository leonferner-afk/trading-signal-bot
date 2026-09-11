"""Optional news/catalyst provider (CryptoPanic).

This is intentionally the one component of the system explicitly allowed
to come back empty: catalyst scoring is a small (0-10) part of the total
score specifically so a missing news feed cannot look like a strong "no
catalyst confirmed" negative signal, nor be silently treated as positive.

If CRYPTOPANIC_API_KEY is not configured, `fetch_news` returns a
`NewsResult` with `available=False` and an empty item list — callers MUST
check `available` and must NOT assume good news when it is False.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field

import httpx

from app.config import settings

CRYPTOPANIC_BASE_URL = "https://cryptopanic.com/api/v1/posts/"


@dataclass
class NewsItem:
    title: str
    source: str
    published_at: str  # ISO8601, as reported by the provider
    url: str
    sentiment_votes_positive: int
    sentiment_votes_negative: int


@dataclass
class NewsResult:
    symbol: str
    available: bool
    items: list[NewsItem] = field(default_factory=list)
    reason: str | None = None  # populated when available=False

    def freshest_age_minutes(self, now_ms: int | None = None) -> float | None:
        if not self.items:
            return None
        import datetime as dt

        now = dt.datetime.now(dt.timezone.utc) if now_ms is None else dt.datetime.fromtimestamp(now_ms / 1000, dt.timezone.utc)
        ages = []
        for item in self.items:
            try:
                published = dt.datetime.fromisoformat(item.published_at.replace("Z", "+00:00"))
                ages.append((now - published).total_seconds() / 60.0)
            except ValueError:
                continue
        return min(ages) if ages else None


def fetch_news(symbol: str, timeout: float = 10.0) -> NewsResult:
    """Fetch recent news for the base currency of `symbol` (e.g. BTCUSDT
    -> BTC). Returns available=False (never fabricated items) when no API
    key is configured or the request fails.
    """
    if not settings.cryptopanic_api_key:
        return NewsResult(
            symbol=symbol,
            available=False,
            reason="CRYPTOPANIC_API_KEY not configured — no news data source connected",
        )

    currency = symbol.upper().replace("USDT", "").replace("USD", "").replace("BUSD", "")
    try:
        response = httpx.get(
            CRYPTOPANIC_BASE_URL,
            params={
                "auth_token": settings.cryptopanic_api_key,
                "currencies": currency,
                "kind": "news",
                "public": "true",
            },
            timeout=timeout,
        )
        response.raise_for_status()
        payload = response.json()
    except (httpx.HTTPError, httpx.TransportError, ValueError) as exc:
        return NewsResult(symbol=symbol, available=False, reason=f"news request failed: {exc}")

    results = payload.get("results", [])
    items = [
        NewsItem(
            title=r.get("title", ""),
            source=(r.get("source") or {}).get("title", "unknown"),
            published_at=r.get("published_at", ""),
            url=r.get("url", ""),
            sentiment_votes_positive=int((r.get("votes") or {}).get("positive", 0)),
            sentiment_votes_negative=int((r.get("votes") or {}).get("negative", 0)),
        )
        for r in results
    ]
    return NewsResult(symbol=symbol, available=True, items=items)


def catalyst_score(news: NewsResult, direction: str) -> tuple[float, str]:
    """Convert a NewsResult into the 0-10 catalyst component + a one-line
    explanation. Weighted by recency (fresher = more relevant) and by net
    sentiment agreeing with the trade direction. Absence of data scores 0
    with an explicit reason — never a guessed positive."""
    if not news.available:
        return 0.0, f"no catalyst confirmed ({news.reason})"
    if not news.items:
        return 0.0, "no recent news found for this asset"

    age = news.freshest_age_minutes()
    if age is None:
        return 0.0, "news found but publish times could not be parsed"

    # Recency weight: full weight within 1h, decaying to 0 by 24h.
    recency_weight = max(0.0, 1.0 - age / (24 * 60))
    if recency_weight <= 0:
        return 0.0, f"most recent news is {age / 60:.1f}h old — treated as stale"

    freshest = min(news.items, key=lambda i: i.published_at or "")
    net_sentiment = freshest.sentiment_votes_positive - freshest.sentiment_votes_negative
    sentiment_aligned = (net_sentiment > 0) if direction == "LONG" else (net_sentiment < 0)

    base = 5.0 if sentiment_aligned else 2.0
    score = round(base * recency_weight + min(len(news.items), 5) * 0.4, 2)
    score = max(0.0, min(10.0, score))
    reason = (
        f"fresh catalyst ({age:.0f}m old, source: {freshest.source}, "
        f"sentiment {'supports' if sentiment_aligned else 'does not clearly support'} {direction.lower()})"
    )
    return score, reason
