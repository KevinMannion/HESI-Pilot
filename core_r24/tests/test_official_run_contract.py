"""Official research runs require explicit output, vintage, and config."""
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class OfficialRunContract(unittest.TestCase):
    def test_reproduce_without_output_is_rejected_unless_exploratory(self):
        proc = subprocess.run(
            [sys.executable, str(ROOT / "reproduce_from_raw.py"), "--housing", str(ROOT / "fixtures" / "synthetic_housing.zip")],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("--output", proc.stderr)

    def test_matched_national_default_is_not_provisional_dir(self):
        src = (ROOT.parent / "research/historical_matched_baseline/src/run_matched_national.py").read_text()
        self.assertNotIn('default=str(PIPE / "results/matched2024_provisional")', src)
        self.assertIn("Refusing to write matched2024_provisional", src)
        proc = subprocess.run(
            [sys.executable, str(ROOT.parent / "research/historical_matched_baseline/src/run_matched_national.py"), "--housing", "x"],
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("--out", proc.stderr)

    def test_example_official_configs_load(self):
        sys.path.insert(0, str(ROOT / "tools"))
        from official_config import load_official_config

        national = ROOT / "configs/official_r24_sep2026_on_acs2024.json"
        cfg = load_official_config(
            national, engine="national_r24", model_vintage="r24_sep2026_costs_on_acs2024_income"
        )
        self.assertEqual(cfg["scientific_publication"], "NO-GO")
        matched = ROOT.parent / "research/historical_matched_baseline/configs/official_matched2024_provisional_repro.json"
        cfg2 = load_official_config(
            matched, engine="matched_year_2024", model_vintage="matched2024_provisional_repro"
        )
        self.assertEqual(cfg2["transport_annual_usd"], 6870.67)

    def test_reproduce_official_without_config_is_rejected(self):
        proc = subprocess.run(
            [
                sys.executable,
                str(ROOT / "reproduce_from_raw.py"),
                "--housing",
                str(ROOT / "fixtures" / "synthetic_housing.zip"),
                "--output",
                "/tmp/hesi_official_scratch",
                "--model-vintage",
                "r24_sep2026_costs_on_acs2024_income",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("--config", proc.stderr)


if __name__ == "__main__":
    unittest.main()
