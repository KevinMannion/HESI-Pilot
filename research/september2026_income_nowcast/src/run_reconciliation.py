"""CLI: R2.4 frame + 2024 ACS source reconciliation. No national 2026 affordability share."""
import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from r24_frame import build_frame
from reconcile_sources import aggregate_person_income, reconcile


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--housing", required=True)
    p.add_argument("--person-a", required=True)
    p.add_argument("--person-b", required=True)
    p.add_argument("--food-cache", required=True)
    p.add_argument("--composition-cache", required=True)
    p.add_argument("--geography", required=True)
    p.add_argument("--out", required=True)
    a = p.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    frame_info = build_frame(
        a.housing,
        a.food_cache,
        a.composition_cache,
        a.geography,
        out / "r24_eligibility_frame.pkl",
    )
    (out / "r24_frame_check.json").write_text(json.dumps(frame_info, indent=2) + "\n")
    person_hh, person_meta = aggregate_person_income([a.person_a, a.person_b])
    (out / "person_income_meta.json").write_text(json.dumps(person_meta, indent=2) + "\n")
    person_hh.to_pickle(out / "person_income_by_serialno.pkl")
    report = reconcile(
        out / "r24_eligibility_frame.pkl",
        person_hh,
        out / "household_income_sources_r24_frame.pkl",
        out / "HOUSEHOLD_INCOME_RECONCILIATION_REPORT.json",
    )
    print(json.dumps({k: report[k] for k in ("r24_frame_rows", "r24_frame_weight", "residual_vs_components", "national_affordability_nowcast_executed")}, indent=2))


if __name__ == "__main__":
    main()
