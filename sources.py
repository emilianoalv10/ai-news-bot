"""Free news sources: Google News RSS, Reddit, Hacker News."""

import time
from datetime import datetime, timedelta, timezone
from urllib.parse import quote

import feedparser
import requests

from config import (
    GOOGLE_NEWS_QUERIES,
    MAX_PER_SOURCE,
    MIN_REDDIT_SCORE,
    SUBREDDITS,
)

HEADERS = {"User-Agent": "AINewsBot/1.0"}


def fetch_google_news() -> list[dict]:
    """Fetch AI news from Google News RSS (no API key needed)."""
    articles = []

    for query in GOOGLE_NEWS_QUERIES:
        url = f"https://news.google.com/rss/search?q={quote(query)}+when:1d&hl=en&gl=US&ceid=US:en"
        try:
            feed = feedparser.parse(url)
        except Exception as e:
            print(f"  Error fetching Google News for '{query}': {e}")
            continue

        for entry in feed.entries[:10]:
            articles.append({
                "source": "Google News",
                "title": entry.get("title", ""),
                "text": entry.get("summary", entry.get("title", "")),
                "url": entry.get("link", ""),
                "published": entry.get("published", ""),
            })

        time.sleep(0.5)  # Be polite

    # Deduplicate by title
    seen = set()
    unique = []
    for a in articles:
        key = a["title"].lower().strip()
        if key not in seen:
            seen.add(key)
            unique.append(a)

    return unique[:MAX_PER_SOURCE]


def fetch_reddit() -> list[dict]:
    """Fetch top AI posts from Reddit (public JSON, no API key needed)."""
    cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
    posts = []

    for sub in SUBREDDITS:
        url = f"https://www.reddit.com/r/{sub}/hot.json?limit=25"
        try:
            resp = requests.get(url, headers=HEADERS, timeout=10)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            print(f"  Error fetching r/{sub}: {e}")
            continue

        for child in data.get("data", {}).get("children", []):
            post = child.get("data", {})
            score = post.get("score", 0)
            created = datetime.fromtimestamp(post.get("created_utc", 0), tz=timezone.utc)

            if created < cutoff:
                continue
            if score < MIN_REDDIT_SCORE:
                continue

            posts.append({
                "source": f"r/{sub}",
                "title": post.get("title", ""),
                "text": post.get("selftext", "")[:500] or post.get("title", ""),
                "url": f"https://reddit.com{post.get('permalink', '')}",
                "score": score,
                "comments": post.get("num_comments", 0),
                "published": str(created),
            })

        time.sleep(1)  # Reddit rate limit

    posts.sort(key=lambda p: p.get("score", 0), reverse=True)
    return posts[:MAX_PER_SOURCE]


def fetch_hackernews() -> list[dict]:
    """Fetch top AI stories from Hacker News (free API, no key needed)."""
    cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
    ai_keywords = {"ai", "artificial intelligence", "gpt", "llm", "chatgpt", "claude",
                   "gemini", "openai", "anthropic", "machine learning", "deep learning",
                   "neural", "transformer", "diffusion", "generative", "copilot", "model"}

    try:
        resp = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json", timeout=10)
        resp.raise_for_status()
        story_ids = resp.json()[:100]
    except Exception as e:
        print(f"  Error fetching HN top stories: {e}")
        return []

    stories = []
    for sid in story_ids:
        try:
            resp = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{sid}.json", timeout=5)
            item = resp.json()
        except Exception:
            continue

        if not item or item.get("type") != "story":
            continue

        title = item.get("title", "").lower()
        if not any(kw in title for kw in ai_keywords):
            continue

        created = datetime.fromtimestamp(item.get("time", 0), tz=timezone.utc)
        if created < cutoff:
            continue

        stories.append({
            "source": "Hacker News",
            "title": item.get("title", ""),
            "text": item.get("title", ""),
            "url": item.get("url", f"https://news.ycombinator.com/item?id={sid}"),
            "score": item.get("score", 0),
            "comments": item.get("descendants", 0),
            "published": str(created),
        })

    stories.sort(key=lambda s: s.get("score", 0), reverse=True)
    return stories[:MAX_PER_SOURCE]


def fetch_all_sources() -> list[dict]:
    """Fetch news from all free sources."""
    all_items = []

    print("  [1/3] Google News RSS...")
    all_items.extend(fetch_google_news())

    print("  [2/3] Reddit...")
    all_items.extend(fetch_reddit())

    print("  [3/3] Hacker News...")
    all_items.extend(fetch_hackernews())

    return all_items
