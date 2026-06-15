import sys
sys.path.insert(0, '/workspaces/lexwatch')

import unittest
from unittest.mock import MagicMock, patch
from agents.scraper_agent import ScraperAgent, RegulatoryUpdate
from agents.classifier_agent import ClassifierAgent, ClassificationResult
from agents.policy_matcher import PolicyMatcherAgent, PolicyMatch
from agents.case_manager import CaseManagerAgent, LexWatchCase
from datetime import datetime


class TestScraperAgent(unittest.TestCase):

    def test_scraper_returns_list(self):
        """Scraper should return a list of regulatory updates"""
        scraper = ScraperAgent()
        updates = scraper.run()
        self.assertIsInstance(updates, list)

    def test_scraper_returns_regulatory_update_objects(self):
        """Each item should be a RegulatoryUpdate object"""
        scraper = ScraperAgent()
        updates = scraper.run()
        if updates:
            self.assertIsInstance(updates[0], RegulatoryUpdate)

    def test_regulatory_update_has_required_fields(self):
        """RegulatoryUpdate should have all required fields"""
        update = RegulatoryUpdate(
            id="TEST-001",
            title="Test Regulatory Update",
            summary="This is a test summary",
            url="https://example.com",
            source="Test Source",
            jurisdiction="UK",
            category="Financial",
            published_date=datetime.now().isoformat()
        )
        self.assertEqual(update.id, "TEST-001")
        self.assertEqual(update.jurisdiction, "UK")
        self.assertEqual(update.status, "NEW")

    def test_scraper_has_sources_configured(self):
        """Scraper should have regulatory sources configured"""
        scraper = ScraperAgent()
        self.assertGreater(len(scraper.sources), 0)


class TestClassifierAgent(unittest.TestCase):

    def setUp(self):
        """Create a sample update for testing"""
        self.sample_update = RegulatoryUpdate(
            id="TEST-001",
            title="FCA proposes new capital requirements",
            summary="The FCA has proposed new capital requirements for financial institutions",
            url="https://fca.org.uk/test",
            source="FCA",
            jurisdiction="UK",
            category="Financial",
            published_date=datetime.now().isoformat()
        )

    def test_classification_result_structure(self):
        """ClassificationResult should have all required fields"""
        result = ClassificationResult(
            update_id="TEST-001",
            impact_level="HIGH",
            affected_departments=["Legal", "Compliance"],
            summary="Test summary",
            action_required="Test action",
            reasoning="Test reasoning"
        )
        self.assertEqual(result.impact_level, "HIGH")
        self.assertIn("Legal", result.affected_departments)

    def test_impact_levels_are_valid(self):
        """Impact level should be one of the valid options"""
        valid_levels = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
        result = ClassificationResult(
            update_id="TEST-001",
            impact_level="HIGH",
            affected_departments=["Compliance"],
            summary="Test",
            action_required="Test",
            reasoning="Test"
        )
        self.assertIn(result.impact_level, valid_levels)


class TestPolicyMatcherAgent(unittest.TestCase):

    def setUp(self):
        self.sample_update = RegulatoryUpdate(
            id="TEST-001",
            title="New AML requirements from FATF",
            summary="FATF has issued new anti-money laundering requirements",
            url="https://fatf.org/test",
            source="FATF",
            jurisdiction="Global",
            category="AML/CFT",
            published_date=datetime.now().isoformat()
        )
        self.sample_classification = ClassificationResult(
            update_id="TEST-001",
            impact_level="HIGH",
            affected_departments=["Compliance", "Legal"],
            summary="New AML requirements issued",
            action_required="Review and update AML policy",
            reasoning="Directly impacts AML compliance framework"
        )

    def test_policy_matcher_has_policies(self):
        """Policy matcher should have internal policies loaded"""
        matcher = PolicyMatcherAgent()
        self.assertGreater(len(matcher.policies), 0)

    def test_policy_match_structure(self):
        """PolicyMatch should have all required fields"""
        match = PolicyMatch(
            policy_id="POL-001",
            policy_title="AML Policy",
            conflict_level="HIGH",
            gap_description="Policy needs updating",
            recommended_action="Update thresholds"
        )
        self.assertEqual(match.policy_id, "POL-001")
        self.assertEqual(match.conflict_level, "HIGH")


class TestCaseManagerAgent(unittest.TestCase):

    def setUp(self):
        self.sample_update = RegulatoryUpdate(
            id="TEST-001",
            title="Test Regulatory Update",
            summary="Test summary",
            url="https://example.com",
            source="FCA",
            jurisdiction="UK",
            category="Financial",
            published_date=datetime.now().isoformat()
        )
        self.sample_classification = ClassificationResult(
            update_id="TEST-001",
            impact_level="HIGH",
            affected_departments=["Compliance", "Legal"],
            summary="Test summary",
            action_required="Test action",
            reasoning="Test reasoning"
        )
        self.sample_matches = [
            PolicyMatch(
                policy_id="POL-001",
                policy_title="AML Policy",
                conflict_level="HIGH",
                gap_description="Gap found",
                recommended_action="Update policy"
            )
        ]

    def test_case_creation(self):
        """Case manager should create a valid case"""
        case = LexWatchCase(
            self.sample_update,
            self.sample_classification,
            self.sample_matches
        )
        self.assertIsNotNone(case.case_id)
        self.assertTrue(case.case_id.startswith("LW-"))
        self.assertEqual(case.status, "OPEN")

    def test_case_has_seven_stages(self):
        """Each case should have exactly 7 workflow stages"""
        case = LexWatchCase(
            self.sample_update,
            self.sample_classification,
            self.sample_matches
        )
        self.assertEqual(len(case.stages), 7)

    def test_case_first_stage_completed(self):
        """First stage should be completed on creation"""
        case = LexWatchCase(
            self.sample_update,
            self.sample_classification,
            self.sample_matches
        )
        self.assertEqual(case.stages[0]["status"], "COMPLETED")

    def test_case_advance_stage(self):
        """Case should advance through stages"""
        case = LexWatchCase(
            self.sample_update,
            self.sample_classification,
            self.sample_matches
        )
        initial_stage = case.current_stage
        case.advance_stage("Test Approver")
        self.assertEqual(case.current_stage, initial_stage + 1)

    def test_case_audit_trail(self):
        """Case should maintain an audit trail"""
        case = LexWatchCase(
            self.sample_update,
            self.sample_classification,
            self.sample_matches
        )
        self.assertGreater(len(case.audit_trail), 0)

    def test_case_to_dict(self):
        """Case should serialize to dictionary"""
        case = LexWatchCase(
            self.sample_update,
            self.sample_classification,
            self.sample_matches
        )
        case_dict = case.to_dict()
        self.assertIn("case_id", case_dict)
        self.assertIn("status", case_dict)
        self.assertIn("stages", case_dict)
        self.assertIn("audit_trail", case_dict)

    def test_high_impact_creates_case(self):
        """High impact updates should always create cases"""
        manager = CaseManagerAgent()
        cases = manager.run(
            [self.sample_update],
            [self.sample_classification],
            {"TEST-001": self.sample_matches}
        )
        self.assertEqual(len(cases), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)