"""Execute run_joint.py on portable CSV fixtures. Formula code is not modified here."""
import json, subprocess, sys, tempfile, unittest
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
ATOL = 1e-7

class LiveSyntheticJoint(unittest.TestCase):
    def test_run_joint_matches_saved_synthetic_results(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            cmd = [
                sys.executable,
                str(ROOT / "src" / "run_joint.py"),
                "--housing-zip",
                str(ROOT / "fixtures" / "synthetic_housing.zip"),
                "--food-cache",
                str(ROOT / "fixtures" / "synthetic_food.csv"),
                "--composition-cache",
                str(ROOT / "fixtures" / "synthetic_composition.csv"),
                "--geography",
                str(ROOT / "fixtures" / "synthetic_geography.csv"),
                "--out",
                str(out),
            ]
            subprocess.run(cmd, check=True, cwd=ROOT)
            ref = ROOT / "results" / "synthetic"
            a = pd.read_csv(ref / "common_cohort_results.csv").set_index("metric")
            b = pd.read_csv(out / "common_cohort_results.csv").set_index("metric")
            for metric in a.index:
                for field in ("mean", "se_sdr", "ci90_low", "ci90_high"):
                    self.assertTrue(
                        np.isclose(a.loc[metric, field], b.loc[metric, field], atol=ATOL, rtol=0),
                        f"{metric}.{field}: {a.loc[metric, field]} vs {b.loc[metric, field]}",
                    )
            old = pd.read_csv(ref / "replicate_results.csv")
            new = pd.read_csv(out / "replicate_results.csv")
            for field in old.columns:
                self.assertTrue(
                    np.allclose(old[field], new[field], atol=ATOL, rtol=0),
                    f"replicate column {field}",
                )
            old_frame = json.loads((ref / "audit.json").read_text())["frame"]
            new_frame = json.loads((out / "audit.json").read_text())["frame"]
            self.assertEqual(old_frame, new_frame)

    def test_numpy_major_is_recorded(self):
        major = int(np.__version__.split(".")[0])
        self.assertIn(major, (1, 2), f"unexpected numpy {np.__version__}")

if __name__ == "__main__":
    unittest.main()
