#!/usr/bin/env python3
"""AI News Bot - Daily AI news summary from free sources, published to Viva Engage."""

import argparse
from datetime import datetime, timezone

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from sources import fetch_all_sources
from summarizer import summarize_news
from viva_engage import publish_to_viva_engage
from config import MAX_ITEMS_FOR_SUMMARY

console = Console()


def run_summary(publish: bool = False):
    """Fetch news and generate the AI news summary."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    console.print(Panel(
        f"[bold cyan]AI News Bot[/] - {today}",
        subtitle="Fetching AI news...",
    ))

    # Step 1: Fetch from all sources
    console.print("\n[bold green]Collecting news...[/]")
    items = fetch_all_sources()
    items = items[:MAX_ITEMS_FOR_SUMMARY]

    console.print(f"\n✅ Found [bold]{len(items)}[/] relevant news items.\n")

    if not items:
        console.print("[yellow]No relevant AI news found today.[/]")
        return

    # Step 2: Summarize with Claude
    with console.status("[bold green]Generating summary with Claude..."):
        summary = summarize_news(items)

    # Step 3: Display
    console.print(Panel(Markdown(summary), title=f"📋 AI News - {today}", border_style="cyan"))

    # Step 4: Save to file
    filename = f"summaries/summary_{today}.md"
    _save_summary(filename, summary, today)
    console.print(f"\n💾 Summary saved to [bold]{filename}[/]")

    # Step 5: Publish to Viva Engage
    if publish:
        with console.status("[bold green]Publishing to Viva Engage..."):
            try:
                result = publish_to_viva_engage(summary)
                msg_id = result.get("messages", [{}])[0].get("id", "unknown")
                console.print(f"\n✅ Published to Viva Engage! (Message ID: {msg_id})")
            except ValueError as e:
                console.print(f"\n[red]❌ Config error: {e}[/]")
            except Exception as e:
                console.print(f"\n[red]❌ Failed to publish: {e}[/]")
    else:
        console.print("\n💡 Use [bold]--publish[/] to post to Viva Engage.")


def _save_summary(filename: str, summary: str, date: str):
    """Save the summary to a markdown file."""
    import os
    os.makedirs("summaries", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# AI News Summary - {date}\n\n")
        f.write(summary)


def main():
    parser = argparse.ArgumentParser(description="AI News Bot - Daily AI news (free sources)")
    parser.add_argument("--publish", action="store_true", help="Publish summary to Viva Engage")
    parser.add_argument("--schedule", action="store_true", help="Run daily at 09:00 UTC")
    args = parser.parse_args()

    if args.schedule:
        import schedule
        import time

        console.print("[bold]Schedule mode.[/] Running daily at 09:00 UTC.\n")
        schedule.every().day.at("09:00").do(run_summary, publish=args.publish)
        run_summary(publish=args.publish)

        while True:
            schedule.run_pending()
            time.sleep(60)
    else:
        run_summary(publish=args.publish)


if __name__ == "__main__":
    main()
