"""Summarize AI news using Claude API."""

import os

import anthropic
from dotenv import load_dotenv

load_dotenv()


def summarize_news(items: list[dict]) -> str:
    """Send news items to Claude and get a structured daily AI news summary."""
    if not items:
        return "No se encontraron noticias relevantes de AI para hoy."

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

    prompt = f"""Analiza las siguientes noticias sobre Inteligencia Artificial recopiladas hoy de Google News, Reddit y Hacker News. Generá un resumen completo en español.

El resumen debe tener estas secciones:

## 🔥 Trending del Día
Las 3-5 noticias o temas más importantes/virales del día en AI. Incluí los links.

## 📰 Resumen de Novedades
Un resumen organizado por categorías (nuevos modelos, regulación, productos, investigación, herramientas, etc.) de todas las novedades relevantes.

## 🏆 Posts Más Destacados
Los 5 posts/artículos con más engagement, indicando fuente, título y link.

## 📊 Tendencias Generales
Un párrafo sobre hacia dónde se mueve la industria según las noticias del día.

Sé conciso pero informativo. Escribí en español argentino.

---

NOTICIAS RECOPILADAS:

{items_text}"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )

    return message.content[0].text
