import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from groq import Groq
from typing import List, Dict
from rich.console import Console
from agents.scraper_agent import RegulatoryUpdate
from agents.classifier_agent import ClassificationResult
from config import config

console = Console()

INTERNAL_POLICIES = [
    {
        "id": "POL-001",
        "title": "Anti-Money Laundering (AML) Policy",
        "department": "Compliance",
        "last_updated": "2024-01-15",
        "content": "All transactions above $10,000 must be reported. Customer due diligence required for all new accounts. Suspicious activity must be reported within 24 hours."
    },
    {
        "id": "POL-002",
        "title": "Credit Risk Management Policy",
        "department": "Risk",
        "last_updated": "2024-03-20",
        "content": "Credit exposure limits must not exceed 25% of capital base. All credit decisions above $500,000 require senior risk committee approval. Monthly stress testing required."
    },
    {
        "id": "POL-003",
        "title": "Mortgage Lending Policy",
        "department": "Operations",
        "last_updated": "2023-11-10",
        "content": "Loan-to-value ratio must not exceed 80%. Income verification required for all applicants. Maximum debt-to-income ratio of 43%."
    },
    {
        "id": "POL-004",
        "title": "Digital Asset and Cryptocurrency Policy",
        "department": "Compliance",
        "last_updated": "2024-02-28",
        "content": "Cryptocurrency transactions must comply with FATF travel rule. All digital asset custody arrangements require board approval. Stablecoin exposure limited to 5% of portfolio."
    },
    {
        "id": "POL-005",
        "title": "Capital Adequacy Policy",
        "department": "Finance",
        "last_updated": "2023-12-01",
        "content": "Tier 1 capital ratio must be maintained above 12% at all times. AT1 instruments subject to quarterly review. Capital buffer requirements must meet Basel III standards."
    },
    {
        "id": "POL-006",
        "title": "Market Risk Policy",
        "department": "Risk",
        "last_updated": "2024-01-30",
        "content": "Value at Risk limits set at 95% confidence interval. Money market fund exposure capped at 15% of total assets. Daily mark-to-market reporting required."
    }
]

class PolicyMatch:
    def __init__(self, policy_id, policy_title, conflict_level, gap_description, recommended_action):
        self.policy_id = policy_id
        self.policy_title = policy_title
        self.conflict_level = conflict_level
        self.gap_description = gap_description
        self.recommended_action = recommended_action

    def __repr__(self):
        return f"PolicyMatch(policy={self.policy_id}, conflict={self.conflict_level})"


class PolicyMatcherAgent:
    def __init__(self):
        self.client = Groq(api_key=config.GROQ_API_KEY)
        self.model = "llama-3.3-70b-versatile"
        self.policies = INTERNAL_POLICIES

    def match_update_to_policies(self, update, classification):
        console.print(f"[cyan]🔍 Matching policies for: {update.title[:50]}...[/cyan]")

        policies_text = json.dumps(self.policies, indent=2)

        prompt = f"""You are LexWatch Policy Matcher, an AI agent that identifies gaps between new regulatory updates and existing internal company policies.

REGULATORY UPDATE:
- Title: {update.title}
- Source: {update.source}
- Impact Level: {classification.impact_level}
- Summary: {classification.summary}
- Action Required: {classification.action_required}
- Affected Departments: {', '.join(classification.affected_departments)}

INTERNAL COMPANY POLICIES:
{policies_text}

Analyze which internal policies are affected by this regulatory update.
Respond with a JSON array only, no other text:
[
  {{
    "policy_id": "POL-XXX",
    "policy_title": "Policy Title",
    "conflict_level": "HIGH|MEDIUM|LOW|NONE",
    "gap_description": "One sentence describing the gap or conflict",
    "recommended_action": "One sentence on what needs to be updated"
  }}
]

Only include policies actually relevant to this update. If none affected, return: []"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a regulatory compliance expert. Always respond with valid JSON only, no markdown, no explanation."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.1
            )

            text = response.choices[0].message.content.strip()

            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()

            matches_data = json.loads(text)
            matches = []

            for m in matches_data:
                match = PolicyMatch(
                    policy_id=m.get("policy_id", ""),
                    policy_title=m.get("policy_title", ""),
                    conflict_level=m.get("conflict_level", "LOW"),
                    gap_description=m.get("gap_description", ""),
                    recommended_action=m.get("recommended_action", "")
                )
                matches.append(match)
                color = {"HIGH": "red", "MEDIUM": "yellow", "LOW": "blue", "NONE": "green"}.get(match.conflict_level, "white")
                console.print(f"  [{color}]⚡ {match.conflict_level} conflict[/{color}] → {match.policy_title}")

            if not matches:
                console.print("  [green]✓ No policy conflicts detected[/green]")

            return matches

        except Exception as e:
            console.print(f"[red]  ✗ Policy matching error: {str(e)}[/red]")
            return []

    def run(self, updates, classifications):
        console.print("\n[bold yellow]📋 LexWatch Policy Matcher Starting...[/bold yellow]\n")
        all_matches = {}

        for update, classification in zip(updates, classifications):
            matches = self.match_update_to_policies(update, classification)
            if matches:
                all_matches[update.id] = matches

        total_conflicts = sum(len(m) for m in all_matches.values())
        console.print(f"\n[bold green]✅ Policy matching complete! Found {total_conflicts} policy conflicts.[/bold green]\n")
        return all_matches


if __name__ == "__main__":
    from agents.scraper_agent import ScraperAgent
    from agents.classifier_agent import ClassifierAgent

    scraper = ScraperAgent()
    updates = scraper.run()

    classifier = ClassifierAgent()
    classifications = classifier.run(updates)

    matcher = PolicyMatcherAgent()
    all_matches = matcher.run(updates, classifications)

    console.print("\n[bold white]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold white]")
    console.print("[bold white]📊 LEXWATCH POLICY CONFLICT REPORT[/bold white]")
    console.print("[bold white]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold white]\n")

    for update_id, matches in all_matches.items():
        update = next((u for u in updates if u.id == update_id), None)
        if update:
            console.print(f"[bold cyan]📌 {update.title[:70]}[/bold cyan]")
            for match in matches:
                color = {"HIGH": "red", "MEDIUM": "yellow", "LOW": "blue", "NONE": "green"}.get(match.conflict_level, "white")
                console.print(f"  [{color}]● {match.conflict_level}[/{color}] {match.policy_title}")
                console.print(f"    Gap: {match.gap_description}")
                console.print(f"    Action: {match.recommended_action}\n")