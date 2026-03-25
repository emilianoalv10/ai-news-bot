"""Summarize AI tweets using Claude API."""

import os

import anthropic
from dotenv import load_dotenv

load_dotenv()


def summarize_tweets(tweets: list[dict]) -> str:
    """Send tweets to Claude and get a structured daily AI news summary."""
    if not tweets:
        return "No hay tweets relevantes de AI para hoy."

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not set in .env")

    client = anthropic.Anthropic(api_key=api_key)

    tweets_text = "\n\n".join(
        f"@{t['username']} ({t['likes']}❤️ {t['retweets']}🔁):\n{t['text']}"
        for t in tweets
    )

    prompt = f"""Analiza los siguientes tweets sobre Inteligencia Artificial del día de hoy y generá un resumen en español.

El resumen debe tener estas secciones:

## 🔥 Trending del Día
Las 3-5 noticias o temas más importantes/virales del día en AI.

## 📰 Resumen de Novedades
Un resumen organizado por categorías (nuevos modelos, regulación, productos, investigación, etc.) de todas las novedades relevantes.

## 🧵 Tweets Destacados
Los 3-5 tweets más interesantes con el @usuario y un breve contexto.

## 📊 Tendencias Generales
Un párrafo breve sobre hacia dónde se mueve la industria según las noticias del día.

---

TWEETS:

{tweets_text}"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )

    return message.content[0].text
