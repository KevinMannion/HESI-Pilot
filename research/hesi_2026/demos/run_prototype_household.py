#!/usr/bin/env python3
"""Run single-household HESI reviewer prototype v0.1 (synthetic scenarios only)."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from prototype_runner import load_scenario_file, run_reviewer_prototype, write_reviewer_prototype_run


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="HESI reviewer prototype v0.1 (single synthetic household)")
    parser.add_argument(
        "--scenario",
        required=True,
        type=Path,
        help="Path to scenario JSON (fixtures/prototype_scenarios/*.json)",
    )
    parser.add_argument(
        "--out",
        required=True,
        type=Path,
        help="Output directory for audit.json and manifests",
    )
    parser.add_argument("--run-id", default=None, help="Optional run identifier")
    args = parser.parse_args(argv)

    scenario_path = args.scenario.resolve()
    scenario = load_scenario_file(scenario_path)
    run_id = args.run_id or f"{scenario.get('scenario_id', 'run')}_prototype"

    payload = run_reviewer_prototype(scenario, repo_root=ROOT.parents[1])
    paths = write_reviewer_prototype_run(args.out, payload, run_id=run_id)

    summary = {
        "scenario_id": payload["scenario_id"],
        "reviewer_prototype_status": payload["reviewer_prototype"]["status"],
        "provisional_resources_to_essential_ratio": payload["reviewer_prototype"].get(
            "provisional_resources_to_essential_ratio"
        ),
        "canonical_calculation_sha256": payload["canonical_calculation_sha256"],
        "output_files": {k: str(v) for k, v in paths.items()},
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
