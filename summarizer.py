"""Summarize AI news using Claude API."""

import os

import anthropic
from dotenv import load_dotenv

load_dotenv()


def summarize_news(items: list[dict]) -> str:
    """Send news items to Claude and get a top 5 AI news summary in English."""
    if not items:
        return "No relevant AI news found today."

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not set in .env")

    client = anthropic.Anthropic(api_key=api_key)

    items_text = "\n\n".join(
        f"[{item.get('source', 'Unknown')}] {item['title']}\n"
        f"{item.get('text', '')}\n"
        f"URL: {item.get('url', 'N/A')} | "
        f"Score: {item.get('score', 'N/A')} | Comments: {item.get('comments', 'N/A')}"
        for item in items
    )

    prompt = f"""Analyze the following AI news collected today from Google News, Reddit, and Hacker News.

Generate a summary in English with EXACTLY this format:

## 🔥 Top 5 AI News of the Day

For each of the 5 most important/viral news items:
1. **[Title]** - Brief 2-3 sentence summary explaining why it matters. (Source: [source]) [link]
2. ...
3. ...
4. ...
5. ...

## 📊 Industry Trends
One short paragraph about where the AI industry is heading based on today's news.

Keep it concise, professional, and engaging. This will be posted on Viva Engage (corporate social network).

---

COLLECTED NEWS:

{items_text}"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    )

    return message.content[0].text
