#!/usr/bin/env python3
"""AI News Bot - Daily AI news summary from Twitter."""

import argparse
import sys
from datetime import datetime, timezone

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from twitter_client import fetch_ai_tweets
from summarizer import summarize_tweets

console = Console()


def run_summary():
    """Fetch tweets and generate the AI news summary."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    console.print(Panel(
        f"[bold cyan]AI News Bot[/] - Resumen del {today}",
        subtitle="Buscando novedades de AI en Twitter...",
    ))

    # Step 1: Fetch tweets
    with console.status("[bold green]Buscando tweets de AI..."):
        tweets = fetch_ai_tweets()

    console.print(f"\n✅ Se encontraron [bold]{len(tweets)}[/] tweets relevantes.\n")

    if not tweets:
        console.print("[yellow]No se encontraron tweets relevantes hoy.[/]")
        return

    # Step 2: Summarize with Claude
    with console.status("[bold green]Generando resumen con Claude..."):
        summary = summarize_tweets(tweets)

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
    parser = argparse.ArgumentParser(description="AI News Bot - Daily AI news from Twitter")
    parser.add_argument("--schedule", action="store_true", help="Run on a daily schedule (every 24h)")
    args = parser.parse_args()

    if args.schedule:
        import schedule
        import time

        console.print("[bold]Modo programado activado.[/] Se ejecutará todos los días a las 09:00 UTC.\n")
        schedule.every().day.at("09:00").do(run_summary)

        # Run once immediately
        run_summary()

        while True:
            schedule.run_pending()
            time.sleep(60)
    else:
        run_summary()


if __name__ == "__main__":
    main()
