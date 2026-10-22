"""M4 scored implementation vs declared gate text; CES AWE is not AHE times hours."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASE3 = (ROOT / "src" / "run_phase3_validation.py").read_text()
GATES = json.loads((ROOT / "reports" / "VALIDATION_GATES.json").read_text())
FACTORS = json.loads((ROOT / "factor_sources" / "BLS_ANNUAL_FACTORS.json").read_text())
GO = json.loads((ROOT / "reports" / "GO_NOGO.json").read_text())


class M4Spec(unittest.TestCase):
    def test_scored_m4_freezes_semp_and_intp(self):
        self.assertIn('m4["SEMP"] = semp', PHASE3)
        self.assertIn('m4["INTP"] = intp', PHASE3)
        self.assertIn("BEA proprietors/interest not acquired", PHASE3)
        self.assertIn('m4["WAGP"] = np.where(pos_w, wagp * awe, wagp)', PHASE3)

    def test_gates_file_describes_bea_m4_and_was_not_rewritten(self):
        text = GATES["models"]["M4_source_specific"]
        self.assertIn("BEA proprietors", text)
        self.assertIn("BEA personal interest+dividends", text)
        self.assertTrue(GATES["loosening_policy"].startswith("These thresholds will not be relaxed after"))

    def test_go_nogo_unchanged(self):
        self.assertEqual(GO["decision"], "NO-GO")
        self.assertFalse(GO["national_2026_adequacy_share_published"])


class CESSeries(unittest.TestCase):
    def test_awe_is_not_ahe_times_hours_annual_means(self):
        ahe = FACTORS["series"]["CES0500000003"]["annual"]
        awe = FACTORS["series"]["CES0500000011"]["annual"]
        hours = FACTORS["series"]["CES0500000007"]["annual"]
        constructed = (ahe["2024"]["mean"] / ahe["2023"]["mean"]) * (hours["2024"]["mean"] / hours["2023"]["mean"])
        published_awe = awe["2024"]["mean"] / awe["2023"]["mean"]
        self.assertGreater(abs(constructed - published_awe), 1e-6)
        self.assertIn("weekly earnings", FACTORS["series"]["CES0500000011"]["title"].lower())
        self.assertIn("hourly earnings", FACTORS["series"]["CES0500000003"]["title"].lower())
        self.assertIn("total private", FACTORS["series"]["CES0500000003"]["title"].lower())


if __name__ == "__main__":
    unittest.main()
