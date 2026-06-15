import sys
sys.path.insert(0, '/workspaces/lexwatch')

import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional
from rich.console import Console
from config import config

console = Console()

class RegulatoryUpdate(BaseModel):
    id: str
    title: str
    summary: str
    url: str
    source: str
    jurisdiction: str
    category: str
    published_date: str
    raw_content: Optional[str] = ""
    impact_level: Optional[str] = None
    affected_departments: Optional[List[str]] = None
    status: str = "NEW"

class ScraperAgent:
    def __init__(self):
        self.sources = config.REGULATORY_SOURCES
        self.updates: List[RegulatoryUpdate] = []

    def scrape_rss_feed(self, source: dict) -> List[RegulatoryUpdate]:
        updates = []
        try:
            console.print(f"[cyan]🔍 Scraping: {source['name']}...[/cyan]")
            feed = feedparser.parse(source["rss"])

            for i, entry in enumerate(feed.entries[:5]):
                update_id = f"{source['jurisdiction']}_{source['category']}_{i}_{datetime.now().strftime('%Y%m%d')}"

                summary = ""
                if hasattr(entry, "summary"):
                    summary = BeautifulSoup(entry.summary, "html.parser").get_text()
                elif hasattr(entry, "description"):
                    summary = BeautifulSoup(entry.description, "html.parser").get_text()

                published = ""
                if hasattr(entry, "published"):
                    published = entry.published
                else:
                    published = datetime.now().isoformat()

                update = RegulatoryUpdate(
                    id=update_id,
                    title=entry.get("title", "No Title"),
                    summary=summary[:500],
                    url=entry.get("link", source["url"]),
                    source=source["name"],
                    jurisdiction=source["jurisdiction"],
                    category=source["category"],
                    published_date=published,
                )
                updates.append(update)
                console.print(f"[green]  ✓ Found: {update.title[:60]}[/green]")

        except Exception as e:
            console.print(f"[red]  ✗ Error scraping {source['name']}: {str(e)}[/red]")

        return updates

    def run(self) -> List[RegulatoryUpdate]:
        console.print("\n[bold yellow]🚀 LexWatch Scraper Agent Starting...[/bold yellow]\n")
        all_updates = []

        for source in self.sources:
            updates = self.scrape_rss_feed(source)
            all_updates.extend(updates)

        self.updates = all_updates
        console.print(f"\n[bold green]✅ Scraper complete! Found {len(all_updates)} regulatory updates.[/bold green]\n")
        return all_updates

if __name__ == "__main__":
    agent = ScraperAgent()
    updates = agent.run()
    for u in updates:
        console.print(f"[white]{u.source}[/white] | [yellow]{u.title[:80]}[/yellow]")