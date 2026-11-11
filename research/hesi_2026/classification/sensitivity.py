"""Sensitivity reporting for provisional tier and affordability-boundary changes."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from classification.provisional_five_tier import (
    AFFORDABILITY_BOUNDARY_RATIO,
    ProvisionalClassificationResult,
    ProvisionalTierThresholds,
    classify_provisional_five_tier,
)


@dataclass(frozen=True)
class ClassificationSensitivityDelta:
    household_id: str
    assumption_set_before: str
    assumption_set_after: str
    status_before: str
    status_after: str
    affordability_ratio_before: float | None
    affordability_ratio_after: float | None
    crossed_affordability_boundary: bool
    tier_before: int | None
    tier_after: int | None
    crossed_tier_boundary: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "household_id": self.household_id,
            "assumption_set_before": self.assumption_set_before,
            "assumption_set_after": self.assumption_set_after,
            "status_before": self.status_before,
            "status_after": self.status_after,
            "affordability_ratio_before": self.affordability_ratio_before,
            "affordability_ratio_after": self.affordability_ratio_after,
            "crossed_affordability_boundary": self.crossed_affordability_boundary,
            "affordability_boundary_r": AFFORDABILITY_BOUNDARY_RATIO,
            "tier_before": self.tier_before,
            "tier_after": self.tier_after,
            "crossed_tier_boundary": self.crossed_tier_boundary,
        }


def _affordability_side(ratio: float | None) -> str | None:
    if ratio is None:
        return None
    if ratio < AFFORDABILITY_BOUNDARY_RATIO:
        return "below"
    if ratio > AFFORDABILITY_BOUNDARY_RATIO:
        return "above"
    return "on_boundary"


def compare_classifications(
    *,
    household_id: str,
    before: ProvisionalClassificationResult,
    after: ProvisionalClassificationResult,
    assumption_set_before: str = "baseline",
    assumption_set_after: str = "variant",
) -> ClassificationSensitivityDelta:
    side_b = _affordability_side(before.affordability_ratio)
    side_a = _affordability_side(after.affordability_ratio)
    crossed_afford = bool(
        side_b and side_a and side_b != side_a and not (side_b == "on_boundary" and side_a == "on_boundary")
    )
    tier_b = before.tier_number
    tier_a = after.tier_number
    crossed_tier = tier_b is not None and tier_a is not None and tier_b != tier_a
    return ClassificationSensitivityDelta(
        household_id=household_id,
        assumption_set_before=assumption_set_before,
        assumption_set_after=assumption_set_after,
        status_before=before.status,
        status_after=after.status,
        affordability_ratio_before=before.affordability_ratio,
        affordability_ratio_after=after.affordability_ratio,
        crossed_affordability_boundary=crossed_afford,
        tier_before=tier_b,
        tier_after=tier_a,
        crossed_tier_boundary=crossed_tier,
    )


def rerun_household_under_assumptions(
    record: Mapping[str, Any],
    *,
    assumption_label: str,
    disposable_usd: float | None = None,
    costs: Mapping[str, Any] | Sequence[Any] | None = None,
    tier_thresholds: ProvisionalTierThresholds | None,
) -> ProvisionalClassificationResult:
    """Reclassify one household under alternate disposable and/or cost assumptions."""
    d = float(disposable_usd if disposable_usd is not None else record["disposable_usd"])
    cost_input = costs if costs is not None else record["costs"]
    result = classify_provisional_five_tier(
        disposable_usd=d,
        costs=cost_input,
        tier_thresholds=tier_thresholds,
    )
    return result


def sweep_assumption_variants(
    records: Sequence[Mapping[str, Any]],
    variants: Sequence[Mapping[str, Any]],
) -> list[ClassificationSensitivityDelta]:
    """
    Each record: household_id, disposable_usd, costs, tier_thresholds (optional).
    Each variant: label, and optional overrides disposable_usd, costs, tier_thresholds.
    Compares baseline record vs each variant for tier / affordability-boundary flips.
    """
    deltas: list[ClassificationSensitivityDelta] = []
    for rec in records:
        hid = str(rec.get("household_id", "unknown"))
        base = classify_provisional_five_tier(
            disposable_usd=float(rec["disposable_usd"]),
            costs=rec["costs"],
            tier_thresholds=rec.get("tier_thresholds"),
        )
        for var in variants:
            d = float(var["disposable_usd"]) if "disposable_usd" in var else float(rec["disposable_usd"])
            costs = var.get("costs", rec["costs"])
            th = var.get("tier_thresholds", rec.get("tier_thresholds"))
            after = classify_provisional_five_tier(disposable_usd=d, costs=costs, tier_thresholds=th)
            deltas.append(
                compare_classifications(
                    household_id=hid,
                    before=base,
                    after=after,
                    assumption_set_before="baseline",
                    assumption_set_after=str(var.get("label", "variant")),
                )
            )
    return deltas


def summarize_sensitivity(deltas: Sequence[ClassificationSensitivityDelta]) -> dict[str, Any]:
    return {
        "households_compared": len({d.household_id for d in deltas}),
        "comparisons": len(deltas),
        "affordability_boundary_flips": sum(1 for d in deltas if d.crossed_affordability_boundary),
        "tier_boundary_flips": sum(1 for d in deltas if d.crossed_tier_boundary),
        "national_weights_applied": False,
        "confidence_intervals": None,
        "scientific_tolerance": None,
    }
