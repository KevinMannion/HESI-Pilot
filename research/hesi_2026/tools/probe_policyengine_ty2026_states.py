#!/usr/bin/env python3
"""Scratch-only TY2026 parameter probe for 51 jurisdictions. Not legal verification."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

STATES = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS",
    "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC",
    "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY",
]
TAX_YEAR = "2026"


def probe_state(state: str) -> dict:
    from policyengine_us import Simulation

    situation = {
        "people": {
            "person": {
                "age": {TAX_YEAR: 35},
                "employment_income": {TAX_YEAR: 50000},
            }
        },
        "households": {"household": {"members": ["person"], "state_code": {TAX_YEAR: state}}},
        "marital_units": {"marital_unit": {"members": ["person"]}},
        "tax_units": {"tax_unit": {"members": ["person"]}},
        "spm_units": {"spm_unit": {"members": ["person"]}},
    }
    sim = Simulation(situation=situation)
    return {
        "state": state,
        "employment_income": float(sim.calculate("employment_income", TAX_YEAR)[0]),
        "adjusted_gross_income_person": float(sim.calculate("adjusted_gross_income_person", TAX_YEAR)[0]),
        "income_tax": float(sim.calculate("income_tax", TAX_YEAR)[0]),
        "status": "calculated",
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, required=True, help="Scratch JSON output path")
    args = ap.parse_args()
    out = {}
    for st in STATES:
        try:
            out[st] = probe_state(st)
        except Exception as e:
            out[st] = {"state": st, "status": "error", "error": f"{type(e).__name__}: {e}"}
    payload = {
        "package": "policyengine-us==2.116.17",
        "tax_year": TAX_YEAR,
        "disclaimer": "computational probe only",
        "jurisdictions": out,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({"wrote": str(args.output), "ok": sum(1 for v in out.values() if v.get("status") == "calculated")}, indent=2))


if __name__ == "__main__":
    main()
