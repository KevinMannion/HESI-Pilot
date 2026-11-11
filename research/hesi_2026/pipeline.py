"""Single-household integration: costs → disposable → adequacy → audit."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from audit.schema import AUDIT_SCHEMA_VERSION, audit_v2_skeleton
from components.base import MissingStatus
from components.registry import default_six_component_registry
from policies import DEFAULT_UNIVERSE_POLICIES
from resources.disposable import disposable_from_fixture
from universe import classify_household, tenure_label

SIX_COMPONENT_NAMES = (
    "housing",
    "food",
    "transportation",
    "healthcare",
    "childcare",
    "other_necessities",
)


class AdequacyError(RuntimeError):
    pass


def sum_priced_essential(costs: list) -> tuple[float | None, list[str], float | None]:
    """Return (full_six_component_total or None, blockers, partial_three_component_total or None)."""
    total = 0.0
    blockers: list[str] = []
    partial_three = 0.0
    partial_ok = True
    for c in costs:
        if c.missing_status != MissingStatus.PRICED or c.annual_usd is None:
            blockers.append(f"{c.component}:{c.missing_status.value}")
            if c.component in ("housing", "food", "transportation"):
                partial_ok = False
            continue
        if not c.policy_approved:
            blockers.append(f"{c.component}:policy_not_approved")
        total += c.annual_usd
        if c.component in ("housing", "food", "transportation"):
            partial_three += c.annual_usd
    if blockers:
        return None, blockers, (partial_three if partial_ok and partial_three > 0 else None)
    return total, [], partial_three if partial_three > 0 else None


def run_household_pipeline(
    household: Mapping[str, Any],
    *,
    cost_context: Mapping[str, Any] | None = None,
    use_policyengine: bool = False,
) -> dict[str, Any]:
    policies = DEFAULT_UNIVERSE_POLICIES
    policies.validate()
    bucket = classify_household(
        household,
        policies=policies,
        geography_ok=bool(household.get("geography_complete", False)),
        composition_ok=bool(household.get("composition_valid", True)),
    )
    if bucket != "included":
        raise AdequacyError(f"household not in included universe: {bucket}")

    costs = [c.price(household, context=cost_context) for c in default_six_component_registry()]
    essential_annual, blockers, partial_three = sum_priced_essential(costs)

    if use_policyengine:
        from resources.policyengine_ty2026 import disposable_from_policyengine

        disposable = disposable_from_policyengine(household)
    else:
        disposable = disposable_from_fixture(household)

    adequacy: dict[str, Any] = {
        "computable": False,
        "essential_annual_usd": essential_annual,
        "disposable_annual_usd": disposable.annual_disposable_usd,
        "ratio": None,
        "blockers": list(blockers),
        "partial_three_component_annual_usd": partial_three,
        "partial_three_component_labeled": "PROVISIONAL_NOT_SIX_COMPONENT_HESI",
        "unpriced_components": [c.to_dict() for c in costs if c.missing_status != MissingStatus.PRICED],
    }

    if partial_three and disposable.annual_disposable_usd is not None:
        adequacy["partial_three_component_ratio"] = disposable.annual_disposable_usd / partial_three

    if essential_annual is not None and disposable.annual_disposable_usd is not None:
        if essential_annual <= 0:
            raise AdequacyError("essential_annual must be positive")
        adequacy["ratio"] = disposable.annual_disposable_usd / essential_annual
        adequacy["computable"] = bool(disposable.policy_approved) and not blockers
        if not adequacy["computable"]:
            adequacy["blockers"].append("production_adequacy_requires_approved_policies")

    audit = audit_v2_skeleton()
    audit["frame"] = {
        "universe_bucket": bucket,
        "weight": float(household.get("weight", 1.0)),
        "tenure": tenure_label(int(household.get("ten", 3))),
    }
    audit["essential_costs"] = [c.to_dict() for c in costs]
    audit["disposable_resources"] = disposable.to_dict()
    audit["adequacy"] = adequacy
    audit["policies"] = {
        "infant_policy": policies.infant_policy.value,
        "bedroom_policy": policies.bedroom_policy.value,
        "geography_policy": policies.geography_policy.value,
    }
    audit["provenance"] = {
        "pipeline": "research.hesi_2026.pipeline",
        "synthetic_only": True,
    }
    audit["limitations"] = [
        "Synthetic fixture path only",
        "Six-component vector incomplete until healthcare/childcare/other approved",
        "Does not validate national 2026 HESI estimate",
    ]
    return {"audit": audit, "adequacy": adequacy}


def write_pipeline_result(output_dir: Path, payload: dict[str, Any]) -> Path:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    audit_path = output_dir / "audit.json"
    audit_path.write_text(json.dumps(payload["audit"], indent=2) + "\n")
    pipe_path = output_dir / "pipeline_result.json"
    pipe_path.write_text(json.dumps(payload, indent=2) + "\n")
    return audit_path
