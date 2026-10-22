"""Hash provisional 2024 execution outputs. Does not touch national_R22."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

PIPE = Path(__file__).resolve().parents[1]
ROOT = PIPE.parents[1]
OUT = PIPE / "results" / "matched2024_provisional"
LOCK = OUT / "ARTIFACT_LOCK.json"

FROZEN_R22 = "6778c312f052cc9442d2adcee1d1c6c7c47a4459a9f31548f1cc8acacfe8cac7"
INCLUDE = {
    "INPUT_VALIDATION.json",
    "EXECUTION_REPORT.json",
    "VALIDATION_GATES.json",
    "SOURCE_MANIFEST.json",
    "MATCHED_YEAR_NATIONAL_REPORT.md",
    "calendar_2024_dayweight/audit.json",
    "calendar_2024_dayweight/common_cohort_results.csv",
    "calendar_2024_dayweight/replicate_results.csv",
    "fy24_revised_only/audit.json",
    "fy24_revised_only/common_cohort_results.csv",
    "fy24_revised_only/replicate_results.csv",
    "fy25_original_from_2024_10_01/audit.json",
    "fy25_original_from_2024_10_01/common_cohort_results.csv",
    "fy25_original_from_2024_10_01/replicate_results.csv",
}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def build():
    files = {}
    for rel in sorted(INCLUDE):
        path = OUT / rel
        files[rel] = {"sha256": sha256(path), "size_bytes": path.stat().st_size}
    r22 = ROOT / "core_r24/results/national_R22/common_cohort_results.csv"
    return {
        "object": "2024 matched-year provisional execution freeze",
        "label": "PROVISIONAL_NOT_SCIENTIFICALLY_VALIDATED",
        "do_not_publish_without_approval": True,
        "national_R22_untouched": sha256(r22) == FROZEN_R22,
        "national_R22_sha256": sha256(r22),
        "acceptance": {
            "metric_atol": 1e-7,
            "frame_exact": True,
            "n_sdr_replicates": 80,
            "sdr_formula": "se = sqrt((4/80) * sum_r (x_r - x)^2)",
        },
        "files": files,
    }


def main():
    report = build()
    LOCK.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"n_files": len(report["files"]), "r22_untouched": report["national_R22_untouched"]}, indent=2))


if __name__ == "__main__":
    main()
