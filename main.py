#!/usr/bin/env python3
"""AI News Bot - Daily AI news summary from free sources."""

import argparse
from datetime import datetime, timezone

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from sources import fetch_all_sources
from summarizer import summarize_news
from config import MAX_ITEMS_FOR_SUMMARY

console = Console()


def run_summary():
    """Fetch news and generate the AI news summary."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    console.print(Panel(
        f"[bold cyan]AI News Bot[/] - Resumen del {today}",
        subtitle="Buscando novedades de AI...",
    ))

    # Step 1: Fetch from all sources
    console.print("\n[bold green]Recopilando noticias...[/]")
    items = fetch_all_sources()

    # Limit total items
    items = items[:MAX_ITEMS_FOR_SUMMARY]

    console.print(f"\n✅ Se encontraron [bold]{len(items)}[/] noticias relevantes.\n")

    if not items:
        console.print("[yellow]No se encontraron noticias relevantes hoy.[/]")
        return

    # Step 2: Summarize with Claude
    with console.status("[bold green]Generando resumen con Claude..."):
        summary = summarize_news(items)

    # Step 3: Display
    console.print(Panel(Markdown(summary), title=f"📋 AI News - {today}", border_style="cyan"))

    # Step 4: Save to file
    filename = f"summaries/summary_{today}.md"
    _save_summary(filename, summary, today)
    console.print(f"\n💾 Resumen guardado en [bold]{filename}[/]")


def _save_summary(filename: str, summary: str, date: str):
    """Save the summary to a markdown file."""
    import os
    os.makedirs("summaries", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# AI News Summary - {date}\n\n")
        f.write(summary)


def main():
    parser = argparse.ArgumentParser(description="AI News Bot - Daily AI news (free sources)")
    parser.add_argument("--schedule", action="store_true", help="Run daily at 09:00 UTC")
    args = parser.parse_args()

    if args.schedule:
        import schedule
        import time

        console.print("[bold]Modo programado activado.[/] Se ejecutará todos los días a las 09:00 UTC.\n")
        schedule.every().day.at("09:00").do(run_summary)
        run_summary()

        while True:
            schedule.run_pending()
            time.sleep(60)
    else:
        run_summary()


if __name__ == "__main__":
    main()
