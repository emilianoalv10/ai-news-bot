"""Summarize AI news using Claude API."""

import os

import anthropic
from dotenv import load_dotenv

load_dotenv()


def summarize_news(items: list[dict]) -> str:
    """Send news items to Claude and get a top 5 trending AI news."""
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

Generate ONLY a Top 5 Trending list in English. Use this EXACT format (plain text, no markdown headers, ready to post on a corporate social network):

🔥 Top 5 AI Trending Today

1. [Title] - Brief 2-3 sentence summary. [link]

2. [Title] - Brief 2-3 sentence summary. [link]

3. [Title] - Brief 2-3 sentence summary. [link]

4. [Title] - Brief 2-3 sentence summary. [link]

5. [Title] - Brief 2-3 sentence summary. [link]

Rules:
- Keep it concise and professional
- Include the actual URL/link for each news item
- Pick the 5 most important/viral topics
- No markdown formatting, just plain text with emojis
- End with a single line: #AI #ArtificialIntelligence #Trending

---

COLLECTED NEWS:

{items_text}"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )

    return message.content[0].text
