"""Write AUDIT_MANIFEST on scratch outputs; compare CSV hashes to frozen reference without writing frozen dirs."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
sys.path.insert(0, str(REPO / "research" / "hesi_2026"))
from audit.manifest import build_audit_manifest, sha256_file, write_audit_manifest  # noqa: E402
from protected_paths import assert_output_allowed  # noqa: E402

FROZEN_CSV = {
    "national_R22": ROOT / "results/national_R22/common_cohort_results.csv",
}


def git_head() -> str | None:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO, text=True).strip()
    except subprocess.CalledProcessError:
        return None


def compare_csv_hash(scratch_csv: Path, frozen_csv: Path, atol_message: str) -> dict:
    if not scratch_csv.is_file():
        return {"status": "MISSING_SCRATCH_CSV", "detail": str(scratch_csv)}
    if not frozen_csv.is_file():
        return {"status": "MISSING_FROZEN_REFERENCE", "detail": str(frozen_csv)}
    got = sha256_file(scratch_csv)
    want = sha256_file(frozen_csv)
    return {
        "status": "PASS" if got == want else "HASH_MISMATCH",
        "scratch_sha256": got,
        "frozen_sha256": want,
        "note": atol_message,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="Emit audit provenance manifest on scratch output only")
    ap.add_argument("--output-dir", type=Path, required=True, help="Scratch directory (never frozen results)")
    ap.add_argument(
        "--compare-target",
        default="national_R22",
        help="Frozen label for hash comparison (CSV only; does not modify frozen tree)",
    )
    ap.add_argument("--run-id", default=None)
    a = ap.parse_args()
    out = assert_output_allowed(a.output_dir, "regenerate_audit_metadata --output-dir")
    out.mkdir(parents=True, exist_ok=True)
    run_id = a.run_id or datetime.now(timezone.utc).strftime("audit_%Y%m%dT%H%M%SZ")
    parity = "NOT_CHECKED"
    frozen_hashes = {}
    scratch_csv = out / "common_cohort_results.csv"
    if a.compare_target in FROZEN_CSV and scratch_csv.is_file():
        cmp = compare_csv_hash(scratch_csv, FROZEN_CSV[a.compare_target], "hash-only; numeric parity via reproduce --check-existing")
        parity = cmp["status"]
        frozen_hashes["common_cohort_results.csv"] = cmp
    manifest = build_audit_manifest(
        run_id=run_id,
        output_dir=out,
        comparison_target=a.compare_target,
        git_commit=git_head(),
        parity_status=parity,
        extra={"frozen_reference_hashes": frozen_hashes},
    )
    write_audit_manifest(out, manifest)
    print(json.dumps({"status": "WROTE", "path": str(out / "AUDIT_MANIFEST.json"), "parity_status": parity}, indent=2))


if __name__ == "__main__":
    main()
