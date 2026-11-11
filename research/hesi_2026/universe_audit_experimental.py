"""Experimental universe audit (reporting only; does not change legacy classify rules)."""
from __future__ import annotations

from typing import Any, Mapping

from policies import DEFAULT_UNIVERSE_POLICIES, UniversePolicies
from universe import accumulate_universe, classify_household, tenure_label

# Categories legacy engine excludes today; flagged as potential dossier re-admission targets (not applied).
POTENTIAL_READMISSION_LABELS = {
    "geography_excluded": "dossier_fractional_puma_unimplemented",
    "composition_excluded": "dossier_rderive_person_records_unimplemented",
    "over4_excluded": "dossier_five_plus_fmr_rule_unimplemented",
    "infant_excluded": "dossier_infant_pricing_unimplemented",
}


def _occupied_tenure_ledger(records: list[Mapping[str, Any]]) -> dict[str, float]:
    weights = {k: 0.0 for k in ("owner", "renter", "rent_free", "other_tenure")}
    for rec in records:
        w = float(rec["weight"])
        label = tenure_label(int(rec["ten"]))
        weights[label] += w
    return weights


def build_experimental_universe_audit(
    records: list[Mapping[str, Any]],
    *,
    policies: UniversePolicies | None = None,
    weight_tolerance: float = 1e-6,
) -> dict[str, Any]:
    """Run legacy ledger, plus experimental re-admission diagnostics (synthetic / research only)."""
    policies = policies or DEFAULT_UNIVERSE_POLICIES
    ledger, tenure_included = accumulate_universe(records, policies=policies)
    tenure_all_occupied = _occupied_tenure_ledger(records)

    excluded_by_bucket: dict[str, float] = {
        "geography_excluded": ledger.geography_excluded_weight,
        "composition_excluded": ledger.composition_excluded_weight,
        "over4_excluded": ledger.over4_excluded_weight,
        "infant_excluded": ledger.infant_excluded_weight,
    }
    potential_readmission_weight = sum(excluded_by_bucket.values())
    parts_sum = (
        ledger.included_weight
        + ledger.geography_excluded_weight
        + ledger.composition_excluded_weight
        + ledger.over4_excluded_weight
        + ledger.infant_excluded_weight
    )
    reconciliation_ok = abs(parts_sum - ledger.occupied_weight) <= weight_tolerance
    tenure_included_sum = sum(tenure_included.weights.values())
    tenure_included_ok = abs(tenure_included_sum - ledger.included_weight) <= weight_tolerance
    tenure_occupied_sum = sum(tenure_all_occupied.values())
    tenure_occupied_ok = abs(tenure_occupied_sum - ledger.occupied_weight) <= weight_tolerance

    per_record_flags: list[dict[str, Any]] = []
    for rec in records:
        geo_ok = bool(rec.get("geography_complete", False))
        comp_ok = bool(rec.get("composition_valid", True))
        bucket = classify_household(
            rec, policies=policies, geography_ok=geo_ok, composition_ok=comp_ok
        )
        entry = {
            "bucket": bucket,
            "weight": float(rec["weight"]),
            "tenure": tenure_label(int(rec["ten"])),
        }
        if bucket != "included":
            entry["potential_readmission_label"] = POTENTIAL_READMISSION_LABELS.get(bucket)
        per_record_flags.append(entry)

    return {
        "status": "EXPERIMENTAL_AUDIT_ONLY",
        "legacy_policies": {
            "infant_policy": policies.infant_policy.value,
            "bedroom_policy": policies.bedroom_policy.value,
            "geography_policy": policies.geography_policy.value,
        },
        "weights": {
            "occupied": ledger.occupied_weight,
            "included_legacy": ledger.included_weight,
            "excluded_total": potential_readmission_weight,
            "excluded_by_bucket": excluded_by_bucket,
            "potential_readmission_weight_reported_not_applied": potential_readmission_weight,
        },
        "tenure_all_occupied": tenure_all_occupied,
        "tenure_included_legacy": dict(tenure_included.weights),
        "reconciliation": {
            "partition_sums_to_occupied": reconciliation_ok,
            "tenure_included_sums_to_included": tenure_included_ok,
            "tenure_occupied_sums_to_occupied": tenure_occupied_ok,
            "partition_parts_sum": parts_sum,
            "occupied_weight": ledger.occupied_weight,
        },
        "per_record_flags": per_record_flags,
        "limitations": [
            "Does not re-admit excluded households",
            "No fractional PUMA imputation",
            "Does not replace core_r24 run_joint universe",
        ],
    }
