import datetime as dt

import httpx

from app.hypothetical import _news_lines
from app.news import headlines, reddit_mentions


def _client(handler):
    return httpx.Client(transport=httpx.MockTransport(handler))


def test_headlines_newest_first_deduplicated_and_none_without_key(monkeypatch):
    monkeypatch.delenv("FINNHUB_API_KEY", raising=False)
    assert headlines("CCL", dt.date(2026, 11, 17), _client(lambda r: httpx.Response(500))) is None
    monkeypatch.setenv("FINNHUB_API_KEY", "test")
    items = [{"headline": "Old news", "source": "A", "datetime": 1_700_000_000},
             {"headline": "Fresh beat", "source": "B", "datetime": 1_800_000_000, "url": "https://x"},
             {"headline": "fresh beat", "source": "C", "datetime": 1_790_000_000}]
    out = headlines("CCL", dt.date(2026, 11, 17), _client(lambda r: httpx.Response(200, json=items)))
    assert [h["headline"] for h in out] == ["Fresh beat", "Old news"] and out[0]["source"] == "B"
    assert headlines("CCL", dt.date(2026, 11, 17), _client(lambda r: httpx.Response(429))) is None


def test_reddit_counts_titles_naming_the_ticker_and_none_when_refused():
    posts = {"data": {"children": [{"data": {"title": "$CCL to the moon"}}, {"data": {"title": "CCL earnings"}},
                                   {"data": {"title": "CCLA is different"}}, {"data": {"title": "nothing"}}]}}
    assert reddit_mentions("CCL", _client(lambda r: httpx.Response(200, json=posts))) == 2
    assert reddit_mentions("CCL", _client(lambda r: httpx.Response(403))) is None


def test_news_lines_in_the_notification():
    lines = _news_lines({"headlines": [{"headline": "Carnival beats", "source": "Reuters"}], "reddit_24h": 12})
    assert lines == ["   📰 Carnival beats (Reuters)", "   💬 Reddit senaste dygnet: 12 inlägg nämner aktien"]
    assert _news_lines(None) == [] and _news_lines({"headlines": [], "reddit_24h": None}) == [
        "   📰 Inga nyhetsrubriker de senaste dagarna."]
