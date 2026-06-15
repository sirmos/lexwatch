import sys
sys.path.insert(0, '/workspaces/lexwatch')

import anthropic
from typing import List
from rich.console import Console
from agents.scraper_agent import RegulatoryUpdate
from config import config

console = Console()

class ClassificationResult:
    def __init__(self, update_id: str, impact_level: str, affected_departments: List[str], 
                 summary: str, action_required: str, reasoning: str):
        self.update_id = update_id
        self.impact_level = impact_level
        self.affected_departments = affected_departments
        self.summary = summary
        self.action_required = action_required
        self.reasoning = reasoning

    def __repr__(self):
        return (f"ClassificationResult(id={self.update_id}, "
                f"impact={self.impact_level}, "
                f"departments={self.affected_departments})")

class ClassifierAgent:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
        self.model = "claude-sonnet-4-6"

    def classify(self, update: RegulatoryUpdate) -> ClassificationResult:
        console.print(f"[cyan]🧠 Classifying: {update.title[:60]}...[/cyan]")

        prompt = f"""You are LexWatch, an enterprise regulatory compliance AI agent.

Analyze this regulatory update and return a structured classification.

REGULATORY UPDATE:
- Source: {update.source}
- Jurisdiction: {update.jurisdiction}
- Category: {update.category}
- Title: {update.title}
- Summary: {update.summary}
- URL: {update.url}
- Date: {update.published_date}

Your task:
1. Assess the IMPACT LEVEL: CRITICAL, HIGH, MEDIUM, or LOW
   - CRITICAL: Immediate action required, heavy penalties possible, affects core business
   - HIGH: Action required within 30 days, significant operational changes needed
   - MEDIUM: Action required within 90 days, moderate process adjustments
   - LOW: Informational, no immediate action required

2. Identify AFFECTED DEPARTMENTS from: Legal, Risk, Compliance, Operations, Finance
   (can be multiple)

3. Write a 2-sentence EXECUTIVE SUMMARY for a compliance officer

4. Describe the SPECIFIC ACTION REQUIRED in 1 sentence

5. Explain your REASONING in 1 sentence

Respond in EXACTLY this format, nothing else:
IMPACT: [level]
DEPARTMENTS: [comma-separated list]
SUMMARY: [2 sentences]
ACTION: [1 sentence]
REASONING: [1 sentence]"""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )

            response = message.content[0].text
            lines = response.strip().split('\n')

            impact = "MEDIUM"
            departments = ["Compliance"]
            summary = update.summary[:200]
            action = "Review and assess impact on current policies."
            reasoning = "Standard regulatory update requiring review."

            for line in lines:
                if line.startswith("IMPACT:"):
                    impact = line.replace("IMPACT:", "").strip()
                elif line.startswith("DEPARTMENTS:"):
                    dept_str = line.replace("DEPARTMENTS:", "").strip()
                    departments = [d.strip() for d in dept_str.split(",")]
                elif line.startswith("SUMMARY:"):
                    summary = line.replace("SUMMARY:", "").strip()
                elif line.startswith("ACTION:"):
                    action = line.replace("ACTION:", "").strip()
                elif line.startswith("REASONING:"):
                    reasoning = line.replace("REASONING:", "").strip()

            result = ClassificationResult(
                update_id=update.id,
                impact_level=impact,
                affected_departments=departments,
                summary=summary,
                action_required=action,
                reasoning=reasoning
            )

            color = {"CRITICAL": "red", "HIGH": "yellow", 
                    "MEDIUM": "blue", "LOW": "green"}.get(impact, "white")
            console.print(f"  [{color}]● {impact}[/{color}] → {', '.join(departments)}")
            return result

        except Exception as e:
            console.print(f"[red]  ✗ Classification error: {str(e)}[/red]")
            return ClassificationResult(
                update_id=update.id,
                impact_level="MEDIUM",
                affected_departments=["Compliance"],
                summary=update.summary[:200],
                action_required="Manual review required.",
                reasoning="Automated classification failed."
            )

    def run(self, updates: List[RegulatoryUpdate]) -> List[ClassificationResult]:
        console.print("\n[bold yellow]🧠 LexWatch Classifier Agent Starting...[/bold yellow]\n")
        results = []
        for update in updates:
            result = self.classify(update)
            update.impact_level = result.impact_level
            update.affected_departments = result.affected_departments
            results.append(result)

        console.print(f"\n[bold green]✅ Classification complete! {len(results)} updates classified.[/bold green]\n")
        return results