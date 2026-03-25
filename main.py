#!/usr/bin/env python3
"""AI News Bot - Top 5 AI trending, sent via email."""

import argparse
from datetime import datetime, timezone

from rich.console import Console
from rich.panel import Panel

from sources import fetch_all_sources
from summarizer import summarize_news
from email_sender import send_email
from config import MAX_ITEMS_FOR_SUMMARY

console = Console()


def run_summary(send: bool = False):
    """Fetch news, generate top 5, and optionally send by email."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    console.print(Panel(f"[bold cyan]AI News Bot[/] - {today}", subtitle="Fetching AI news..."))

    # Step 1: Fetch from all sources
    console.print("\n[bold green]Collecting news...[/]")
    items = fetch_all_sources()
    items = items[:MAX_ITEMS_FOR_SUMMARY]

    console.print(f"\n✅ Found [bold]{len(items)}[/] relevant news items.\n")

    if not items:
        console.print("[yellow]No relevant AI news found today.[/]")
        return

    # Step 2: Generate top 5 with Claude
    with console.status("[bold green]Generating Top 5 with Claude..."):
        summary = summarize_news(items)

    # Step 3: Display
    console.print(Panel(summary, title=f"📋 Top 5 AI Trending - {today}", border_style="cyan"))

    # Step 4: Send email
    if send:
        with console.status("[bold green]Sending email..."):
            try:
                send_email(summary, today)
                console.print("\n✅ Email sent!")
            except ValueError as e:
                console.print(f"\n[red]❌ Config error: {e}[/]")
            except Exception as e:
                console.print(f"\n[red]❌ Failed to send email: {e}[/]")
    else:
        console.print("\n💡 Use [bold]--send[/] to send via email.")


def main():
    parser = argparse.ArgumentParser(description="AI News Bot - Top 5 AI Trending")
    parser.add_argument("--send", action="store_true", help="Send summary via email")
    parser.add_argument("--schedule", action="store_true", help="Run daily at 09:00 UTC")
    args = parser.parse_args()

    if args.schedule:
        import schedule
        import time

        console.print("[bold]Schedule mode.[/] Running daily at 09:00 UTC.\n")
        schedule.every().day.at("09:00").do(run_summary, send=args.send)
        run_summary(send=args.send)

        while True:
            schedule.run_pending()
            time.sleep(60)
    else:
        run_summary(send=args.send)


if __name__ == "__main__":
    main()
