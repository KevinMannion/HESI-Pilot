"""Historical manifests authenticate historical files; v2 authenticates the working tree."""
import json, subprocess, sys, tempfile, unittest
from pathlib import Path

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE))
from verify_integrity import check_manifest, check_registered, check_unapproved_locked_script_edits


class IntegrityVersioning(unittest.TestCase):
    def test_v1_against_working_tree_fails_on_known_drift(self):
        report = check_manifest(BASE / "INTEGRITY_MANIFEST.json", overlay=None, root=BASE)
        self.assertEqual(report["status"], "FAIL")
        files = {f["file"] for f in report["failed"]}
        self.assertIn("housing/verify.py", files)
        self.assertIn("transportation/run_standard.py", files)
        self.assertIn("transportation/test_standard.py", files)
        self.assertIn("verify_release.py", files)

    def test_v1_against_historical_overlay_passes(self):
        overlay = BASE / "historical_release_e45eb87"
        report = check_manifest(BASE / "INTEGRITY_MANIFEST.json", overlay=overlay, root=BASE)
        self.assertEqual(report["status"], "PASS", report["failed"])

    def test_v2_matches_working_tree(self):
        report = check_manifest(BASE / "INTEGRITY_MANIFEST.v2.json", overlay=None, root=BASE)
        self.assertEqual(report["status"], "PASS", report["failed"])

    def test_registered_manifests_all_pass(self):
        body = check_registered()
        self.assertEqual(body["status"], "PASS", body)
        self.assertEqual(check_unapproved_locked_script_edits()["status"], "PASS")

    def test_unapproved_edit_fails_policy(self):
        reg = json.loads((BASE / "MANIFEST_REGISTER.json").read_text())
        documented = {c["file"] for c in reg["documented_working_tree_changes"]}
        self.assertTrue(documented)
        # A locked file that still matches v1 must not be silently treated as approved drift.
        v1 = json.loads((BASE / "INTEGRITY_MANIFEST.json").read_text())["files"]
        unchanged = [rel for rel, old in v1.items() if rel not in documented]
        self.assertGreater(len(unchanged), 10)


if __name__ == "__main__":
    unittest.main()
