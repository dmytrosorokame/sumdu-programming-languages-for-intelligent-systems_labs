"""Unit tests for the PC Diagnostic Expert System."""
import unittest
import pandas as pd
from knowledge_base import DiagnosticSystem, SYMPTOM_CATEGORIES, SECONDARY_SYMPTOMS, RULES_DATA


class TestDiagnosticSystem(unittest.TestCase):
    """Tests for the inference engine."""

    def setUp(self):
        self.engine = DiagnosticSystem()

    def test_knowledge_base_loaded(self):
        """Knowledge base should contain 20 rules."""
        self.assertEqual(len(self.engine.knowledge_base), 20)

    def test_knowledge_base_columns(self):
        """DataFrame must have the required columns."""
        expected = {"rule_id", "symptom_1", "symptom_2", "diagnosis", "recommendation"}
        self.assertEqual(set(self.engine.knowledge_base.columns), expected)

    def test_diagnose_power_supply(self):
        """Rule 1: PC not turning on + no lights -> Power supply failure."""
        result = self.engine.diagnose("pc_not_turning_on", "no_lights")
        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]["diagnosis"], "Power supply failure")

    def test_diagnose_ram_failure(self):
        """Rule 5: blue screen + random BSOD -> RAM failure."""
        result = self.engine.diagnose("blue_screen", "random_bsod")
        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]["diagnosis"], "RAM failure")

    def test_diagnose_malware(self):
        """Rule 6: slow performance + high CPU -> Malware or background processes."""
        result = self.engine.diagnose("slow_performance", "high_cpu_usage")
        self.assertEqual(len(result), 1)
        self.assertIn("Malware", result.iloc[0]["diagnosis"])

    def test_diagnose_hdd_failing(self):
        """Rule 11: strange noises + clicking HDD -> Hard drive failing."""
        result = self.engine.diagnose("strange_noises", "clicking_hdd")
        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]["diagnosis"], "Hard drive failing")

    def test_diagnose_dns_issue(self):
        """Rule 16: internet not working + connected no internet -> DNS or router issue."""
        result = self.engine.diagnose("internet_not_working", "wifi_connected_no_internet")
        self.assertEqual(len(result), 1)
        self.assertIn("DNS", result.iloc[0]["diagnosis"])

    def test_no_match(self):
        """Non-existent symptom pair returns empty result."""
        result = self.engine.diagnose("nonexistent", "fake_symptom")
        self.assertTrue(result.empty)

    def test_all_categories_have_secondary(self):
        """Every primary symptom should have secondary options defined."""
        for key in SYMPTOM_CATEGORIES:
            self.assertIn(key, SECONDARY_SYMPTOMS)
            self.assertGreater(len(SECONDARY_SYMPTOMS[key]), 0)

    def test_all_rules_are_reachable(self):
        """Every rule should be reachable by some primary+secondary pair."""
        df = self.engine.knowledge_base
        for _, row in df.iterrows():
            s1, s2 = row["symptom_1"], row["symptom_2"]
            self.assertIn(s1, SYMPTOM_CATEGORIES, f"Rule {row['rule_id']}: unknown primary symptom")
            self.assertIn(s2, SECONDARY_SYMPTOMS.get(s1, {}), f"Rule {row['rule_id']}: unknown secondary symptom")

    def test_recommendations_not_empty(self):
        """Every rule must have a non-empty recommendation."""
        for rec in RULES_DATA["recommendation"]:
            self.assertTrue(len(rec.strip()) > 0)


if __name__ == "__main__":
    unittest.main()
