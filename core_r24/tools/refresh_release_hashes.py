"""Rewrite RELEASE_FILE_HASHES.json for the current working tree (R2.5 package files)."""
import hashlib, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
manifest = json.loads((ROOT / "RELEASE_FILE_HASHES.json").read_text())
# drop removed pickle fixtures; add CSV fixtures if present
for gone in ("fixtures/synthetic_food.pkl", "fixtures/synthetic_composition.pkl"):
    manifest.pop(gone, None)
for added in (
    "fixtures/synthetic_food.csv",
    "fixtures/synthetic_composition.csv",
    "tests/test_run_joint_synthetic.py",
):
    if (ROOT / added).is_file():
        manifest[added] = ""
out = {}
for rel in sorted(manifest):
    path = ROOT / rel
    if not path.is_file():
        raise SystemExit("missing " + rel)
    h = hashlib.sha256(path.read_bytes()).hexdigest()
    out[rel] = h
(ROOT / "RELEASE_FILE_HASHES.json").write_text(json.dumps(out, indent=2) + "\n")
print("wrote", len(out), "hashes")
