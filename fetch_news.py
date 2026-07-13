"""Fetch recent news headlines for a ticker via Google News RSS (free, no API key)."""

import feedparser
from urllib.parse import quote_plus


def get_news(ticker: str, max_items: int = 5) -> list[dict]:
    """Return recent headlines + sources for a ticker.

    Uses Google News' public RSS search endpoint. No key required.
    Each item has: title, source, published, link
    """
    query = quote_plus(f"{ticker} stock")
    url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"

    try:
        feed = feedparser.parse(url)
        items = []
        for entry in feed.entries[:max_items]:
            items.append({
                "title": entry.get("title", ""),
                "source": entry.get("source", {}).get("title", "") if hasattr(entry, "source") else "",
                "published": entry.get("published", ""),
                "link": entry.get("link", ""),
            })
        return items
    except Exception as e:
        return [{"title": f"(news fetch failed: {e})", "source": "", "published": "", "link": ""}]


def get_all_news(tickers: list[str], max_items: int = 5) -> dict[str, list[dict]]:
    return {t: get_news(t, max_items) for t in tickers}


if __name__ == "__main__":
    for headline in get_news("AAPL"):
        print(headline["title"])
