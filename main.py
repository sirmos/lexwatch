import sys
sys.path.insert(0, '/workspaces/lexwatch')

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from datetime import datetime

from agents.scraper_agent import ScraperAgent
from agents.classifier_agent import ClassifierAgent
from agents.policy_matcher import PolicyMatcherAgent
from agents.case_manager import CaseManagerAgent

console = Console()

def print_banner():
    banner = Text()
    banner.append("⚖️  LEXWATCH\n", style="bold cyan")
    banner.append("AI-Powered Regulatory Compliance Agent\n", style="bold white")
    banner.append("Built on UiPath Maestro Case + Groq LLM\n", style="dim")
    banner.append(f"Run started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", style="dim")
    console.print(Panel(banner, border_style="cyan", padding=(1, 4)))

def print_summary(updates, classifications, all_matches, cases):
    console.print("\n[bold cyan]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold cyan]")
    console.print("[bold white]📊 LEXWATCH EXECUTION SUMMARY[/bold white]")
    console.print("[bold cyan]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold cyan]\n")

    console.print(f"[white]🔍 Regulatory updates scraped:[/white] [bold cyan]{len(updates)}[/bold cyan]")
    console.print(f"[white]🧠 Updates classified:[/white]        [bold cyan]{len(classifications)}[/bold cyan]")

    critical = sum(1 for c in classifications if c.impact_level == "CRITICAL")
    high = sum(1 for c in classifications if c.impact_level == "HIGH")
    medium = sum(1 for c in classifications if c.impact_level == "MEDIUM")
    low = sum(1 for c in classifications if c.impact_level == "LOW")

    console.print(f"[white]📈 Impact breakdown:[/white]")
    console.print(f"   [red]● CRITICAL: {critical}[/red]")
    console.print(f"   [yellow]● HIGH:     {high}[/yellow]")
    console.print(f"   [blue]● MEDIUM:   {medium}[/blue]")
    console.print(f"   [green]● LOW:      {low}[/green]")

    total_conflicts = sum(len(m) for m in all_matches.values())
    console.print(f"\n[white]⚡ Policy conflicts detected:[/white] [bold red]{total_conflicts}[/bold red]")
    console.print(f"[white]📁 Cases created in Maestro:[/white]  [bold yellow]{len(cases)}[/bold yellow]")

    dept_counts = {}
    for c in classifications:
        for dept in c.affected_departments:
            dept_counts[dept] = dept_counts.get(dept, 0) + 1

    console.print(f"\n[white]🏢 Department workload:[/white]")
    for dept, count in sorted(dept_counts.items(), key=lambda x: x[1], reverse=True):
        console.print(f"   [cyan]{dept}:[/cyan] {count} updates")

    console.print(f"\n[white]💾 Cases saved to:[/white] [green]data/cases.json[/green]")
    console.print(f"[white]🕐 Completed at:[/white]   [green]{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/green]")
    console.print("\n[bold cyan]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold cyan]")
    console.print("[bold green]✅ LexWatch run complete. All cases ready for human review.[/bold green]")
    console.print("[bold cyan]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold cyan]\n")

def run():
    print_banner()

    # Stage 1: Scrape regulatory sources
    console.print("\n[bold white]STAGE 1: REGULATORY INTELLIGENCE GATHERING[/bold white]")
    console.print("[dim]Scraping live regulatory sources...[/dim]\n")
    scraper = ScraperAgent()
    updates = scraper.run()

    # Stage 2: Classify each update
    console.print("\n[bold white]STAGE 2: AI CLASSIFICATION[/bold white]")
    console.print("[dim]Classifying updates by impact and department...[/dim]\n")
    classifier = ClassifierAgent()
    classifications = classifier.run(updates)

    # Stage 3: Match against internal policies
    console.print("\n[bold white]STAGE 3: POLICY GAP ANALYSIS[/bold white]")
    console.print("[dim]Cross-referencing against internal policies...[/dim]\n")
    matcher = PolicyMatcherAgent()
    all_matches = matcher.run(updates, classifications)

    # Stage 4: Create Maestro cases
    console.print("\n[bold white]STAGE 4: MAESTRO CASE CREATION[/bold white]")
    console.print("[dim]Creating cases and routing to teams...[/dim]\n")
    manager = CaseManagerAgent()
    cases = manager.run(updates, classifications, all_matches)

    # Display dashboard
    manager.display_dashboard()

    # Save cases
    manager.save_cases()

    # Print summary
    print_summary(updates, classifications, all_matches, cases)

if __name__ == "__main__":
    run()