import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import uuid
from datetime import datetime
from typing import List, Dict
from rich.console import Console
from rich.table import Table
from agents.scraper_agent import RegulatoryUpdate
from agents.classifier_agent import ClassificationResult
from agents.policy_matcher import PolicyMatch

console = Console()

class LexWatchCase:
    def __init__(self, update, classification, matches):
        self.case_id = f"LW-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:6].upper()}"
        self.created_at = datetime.now().isoformat()
        self.status = "OPEN"
        self.update = update
        self.classification = classification
        self.policy_matches = matches
        self.assigned_to = self._assign_owner()
        self.priority = self._set_priority()
        self.stages = self._define_stages()
        self.current_stage = 0
        self.audit_trail = []
        self._log("Case created by LexWatch Scraper Agent")

    def _assign_owner(self):
        dept_map = {
            "Legal": "legal-team@company.com",
            "Risk": "risk-team@company.com",
            "Compliance": "compliance-team@company.com",
            "Operations": "ops-team@company.com",
            "Finance": "finance-team@company.com"
        }
        primary_dept = self.classification.affected_departments[0] if self.classification.affected_departments else "Compliance"
        return dept_map.get(primary_dept, "compliance-team@company.com")

    def _set_priority(self):
        priority_map = {
            "CRITICAL": 1,
            "HIGH": 2,
            "MEDIUM": 3,
            "LOW": 4
        }
        return priority_map.get(self.classification.impact_level, 3)

    def _define_stages(self):
        return [
            {
                "stage": 1,
                "name": "Intake & Classification",
                "actor": "LexWatch AI Agent",
                "status": "COMPLETED",
                "description": "Regulatory update detected, classified and policy gaps identified"
            },
            {
                "stage": 2,
                "name": "Legal Review",
                "actor": "Legal Team",
                "status": "PENDING",
                "description": "Legal team reviews regulatory update and confirms applicability"
            },
            {
                "stage": 3,
                "name": "Risk Assessment",
                "actor": "Risk Team",
                "status": "PENDING",
                "description": "Risk team assesses business impact and exposure"
            },
            {
                "stage": 4,
                "name": "Policy Update",
                "actor": "Compliance Team",
                "status": "PENDING",
                "description": "Compliance team drafts policy updates to address gaps"
            },
            {
                "stage": 5,
                "name": "Senior Approval",
                "actor": "Chief Compliance Officer",
                "status": "PENDING",
                "description": "CCO reviews and approves all policy changes"
            },
            {
                "stage": 6,
                "name": "Implementation",
                "actor": "Operations Team",
                "status": "PENDING",
                "description": "Operations implements approved policy changes across systems"
            },
            {
                "stage": 7,
                "name": "Case Closed",
                "actor": "LexWatch AI Agent",
                "status": "PENDING",
                "description": "All changes verified, case closed and archived"
            }
        ]

    def _log(self, action):
        self.audit_trail.append({
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "stage": self.stages[self.current_stage]["name"] if self.current_stage < len(self.stages) else "Closed"
        })

    def advance_stage(self, approver="System"):
        if self.current_stage < len(self.stages) - 1:
            self.stages[self.current_stage]["status"] = "COMPLETED"
            self.current_stage += 1
            self.stages[self.current_stage]["status"] = "IN_PROGRESS"
            self._log(f"Stage advanced by {approver}")
            return True
        return False

    def to_dict(self):
        return {
            "case_id": self.case_id,
            "created_at": self.created_at,
            "status": self.status,
            "priority": self.priority,
            "impact_level": self.classification.impact_level,
            "title": self.update.title,
            "source": self.update.source,
            "jurisdiction": self.update.jurisdiction,
            "assigned_to": self.assigned_to,
            "affected_departments": self.classification.affected_departments,
            "summary": self.classification.summary,
            "action_required": self.classification.action_required,
            "policy_conflicts": len(self.policy_matches),
            "current_stage": self.stages[self.current_stage]["name"],
            "stages": self.stages,
            "audit_trail": self.audit_trail
        }


class CaseManagerAgent:
    def __init__(self):
        self.cases: List[LexWatchCase] = []

    def create_case(self, update, classification, matches):
        case = LexWatchCase(update, classification, matches)
        self.cases.append(case)
        priority_colors = {1: "red", 2: "yellow", 3: "blue", 4: "green"}
        color = priority_colors.get(case.priority, "white")
        console.print(f"  [{color}]📁 Case {case.case_id}[/{color}] → {case.stages[0]['name']} → Assigned to {case.assigned_to}")
        return case

    def run(self, updates, classifications, all_matches):
        console.print("\n[bold yellow]📁 LexWatch Case Manager Starting...[/bold yellow]\n")

        for update, classification in zip(updates, classifications):
            matches = all_matches.get(update.id, [])
            if classification.impact_level in ["CRITICAL", "HIGH"] or matches:
                self.create_case(update, classification, matches)

        console.print(f"\n[bold green]✅ Case Manager complete! {len(self.cases)} cases created.[/bold green]\n")
        return self.cases

    def display_dashboard(self):
        table = Table(title="🏛️ LEXWATCH CASE DASHBOARD", style="bold")
        table.add_column("Case ID", style="cyan", no_wrap=True)
        table.add_column("Priority", style="bold")
        table.add_column("Impact", style="bold")
        table.add_column("Title", max_width=40)
        table.add_column("Stage", style="yellow")
        table.add_column("Assigned To", style="green")
        table.add_column("Conflicts", justify="center")

        priority_labels = {1: "🔴 CRITICAL", 2: "🟡 HIGH", 3: "🔵 MEDIUM", 4: "🟢 LOW"}

        for case in sorted(self.cases, key=lambda x: x.priority):
            table.add_row(
                case.case_id,
                priority_labels.get(case.priority, "MEDIUM"),
                case.classification.impact_level,
                case.update.title[:40],
                case.stages[case.current_stage]["name"],
                case.assigned_to.split("@")[0],
                str(len(case.policy_matches))
            )

        console.print(table)

    def save_cases(self, filepath="data/cases.json"):
        cases_data = [c.to_dict() for c in self.cases]
        with open(filepath, 'w') as f:
            json.dump(cases_data, f, indent=2)
        console.print(f"[green]💾 Cases saved to {filepath}[/green]")


if __name__ == "__main__":
    from agents.scraper_agent import ScraperAgent
    from agents.classifier_agent import ClassifierAgent
    from agents.policy_matcher import PolicyMatcherAgent

    scraper = ScraperAgent()
    updates = scraper.run()

    classifier = ClassifierAgent()
    classifications = classifier.run(updates)

    matcher = PolicyMatcherAgent()
    all_matches = matcher.run(updates, classifications)

    manager = CaseManagerAgent()
    cases = manager.run(updates, classifications, all_matches)

    manager.display_dashboard()
    manager.save_cases()