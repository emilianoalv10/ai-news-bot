"""Twitter client to fetch AI-related tweets."""

import os
from datetime import datetime, timedelta, timezone

import tweepy
from dotenv import load_dotenv

from config import (
    MAX_RESULTS_PER_QUERY,
    MIN_LIKES,
    MIN_RETWEETS,
    SEARCH_QUERIES,
    MAX_TWEETS_FOR_SUMMARY,
)

load_dotenv()


def get_client() -> tweepy.Client:
    """Create an authenticated Twitter API v2 client."""
    bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
    if not bearer_token:
        raise ValueError("TWITTER_BEARER_TOKEN not set in .env")
    return tweepy.Client(bearer_token=bearer_token)


def fetch_ai_tweets() -> list[dict]:
    """Fetch today's AI-related tweets from Twitter."""
    client = get_client()
    since = datetime.now(timezone.utc) - timedelta(hours=24)

    all_tweets = []

    for query in SEARCH_QUERIES:
        full_query = f"{query} lang:en -is:retweet"
        try:
            response = client.search_recent_tweets(
                query=full_query,
                max_results=MAX_RESULTS_PER_QUERY,
                start_time=since.isoformat(),
                tweet_fields=["created_at", "public_metrics", "author_id"],
                user_fields=["username", "name"],
                expansions=["author_id"],
            )
        except tweepy.TooManyRequests:
            print(f"  Rate limited on query: {query}, skipping...")
            continue
        except tweepy.TwitterServerError:
            print(f"  Server error on query: {query}, skipping...")
            continue

        if not response.data:
            continue

        # Build author lookup
        users = {u.id: u for u in (response.includes.get("users", []))}

        for tweet in response.data:
            metrics = tweet.public_metrics or {}
            likes = metrics.get("like_count", 0)
            retweets = metrics.get("retweet_count", 0)

            if likes < MIN_LIKES and retweets < MIN_RETWEETS:
                continue

            author = users.get(tweet.author_id)
            username = author.username if author else "unknown"

            all_tweets.append({
                "id": tweet.id,
                "text": tweet.text,
                "username": username,
                "likes": likes,
                "retweets": retweets,
                "created_at": str(tweet.created_at),
            })

    # Deduplicate by tweet id
    seen = set()
    unique = []
    for t in all_tweets:
        if t["id"] not in seen:
            seen.add(t["id"])
            unique.append(t)

    # Sort by engagement (likes + retweets) descending
    unique.sort(key=lambda t: t["likes"] + t["retweets"], reverse=True)

    return unique[:MAX_TWEETS_FOR_SUMMARY]
