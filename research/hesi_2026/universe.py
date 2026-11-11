"""Household-universe accounting: exhaustive exclusion weights and ACS tenure classes."""
from __future__ import annotations

from dataclasses import dataclass, field
from math import ceil
from typing import Any, Mapping

from policies import BedroomPolicy, GeographyPolicy, InfantPolicy, UniversePolicies

# ACS housing tenure (TEN): 1 owned with mortgage, 2 owned free and clear, 3 rented, 4 occupied without rent
TENURE_OWNER = {1, 2}
TENURE_RENTER = {3}
TENURE_RENT_FREE = {4}


def tenure_label(ten: int) -> str:
    if ten in TENURE_OWNER:
        return "owner"
    if ten in TENURE_RENTER:
        return "renter"
    if ten in TENURE_RENT_FREE:
        return "rent_free"
    return "other_tenure"


def required_bedrooms(adults: int, children: int, partners: int) -> int:
    if adults < 1:
        raise ValueError("at least one adult required")
    if partners > adults:
        raise ValueError("invalid couple count")
    return adults - min(partners, 1) + ceil(children / 2)


@dataclass
class ExclusionLedger:
    geography_excluded_weight: float = 0.0
    composition_excluded_weight: float = 0.0
    over4_excluded_weight: float = 0.0
    infant_excluded_weight: float = 0.0
    included_weight: float = 0.0
    occupied_weight: float = 0.0
    reasons: dict[str, int] = field(default_factory=dict)

    def reconcile(self, tolerance: float = 1e-6) -> None:
        parts = (
            self.geography_excluded_weight
            + self.composition_excluded_weight
            + self.over4_excluded_weight
            + self.infant_excluded_weight
            + self.included_weight
        )
        if abs(parts - self.occupied_weight) > tolerance:
            raise ValueError(
                f"exclusion ledger does not sum to occupied_weight: {parts} != {self.occupied_weight}"
            )


@dataclass
class TenureLedger:
    weights: dict[str, float] = field(default_factory=dict)
    joint_cost_weighted: dict[str, float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for key in ("owner", "renter", "rent_free", "other_tenure"):
            self.weights.setdefault(key, 0.0)
            self.joint_cost_weighted.setdefault(key, 0.0)

    def add(self, ten: int, weight: float, monthly_joint: float) -> None:
        label = tenure_label(ten)
        self.weights[label] += weight
        self.joint_cost_weighted[label] += weight * monthly_joint

    def reconcile_included(self, included_weight: float, tolerance: float = 1e-6) -> None:
        if abs(sum(self.weights.values()) - included_weight) > tolerance:
            raise ValueError("tenure weights do not sum to included_weight")


def classify_household(
    record: Mapping[str, Any],
    *,
    policies: UniversePolicies,
    geography_ok: bool,
    composition_ok: bool,
) -> str:
    """Return exclusion bucket name or 'included'."""
    policies.validate()
    if not geography_ok:
        if policies.geography_policy != GeographyPolicy.COMPLETE_UNAMBIGUOUS_ONLY:
            raise NotImplementedError("non-default geography policy")
        return "geography_excluded"
    if not composition_ok:
        return "composition_excluded"
    adults = int(record["adults"])
    children = int(record["children"])
    partners = int(record["partners"])
    np_persons = int(record["np"])
    n_infant = int(record.get("n_infant", 0))
    if adults + children != np_persons:
        return "composition_excluded"
    br = required_bedrooms(adults, children, partners)
    if br > 4:
        if policies.bedroom_policy == BedroomPolicy.EXCLUDE_OVER_FOUR:
            return "over4_excluded"
        raise NotImplementedError(policies.bedroom_policy.value)
    if n_infant > 0:
        if policies.infant_policy == InfantPolicy.EXCLUDE_UNPRICED:
            return "infant_excluded"
        raise NotImplementedError(policies.infant_policy.value)
    return "included"


def accumulate_universe(
    records: list[Mapping[str, Any]],
    *,
    policies: UniversePolicies | None = None,
) -> tuple[ExclusionLedger, TenureLedger]:
    policies = policies or UniversePolicies()
    policies.validate()
    ledger = ExclusionLedger()
    tenure = TenureLedger()
    for rec in records:
        w = float(rec["weight"])
        ledger.occupied_weight += w
        geo_ok = bool(rec.get("geography_complete", False))
        comp_ok = bool(rec.get("composition_valid", True))
        bucket = classify_household(rec, policies=policies, geography_ok=geo_ok, composition_ok=comp_ok)
        if bucket == "included":
            ledger.included_weight += w
            monthly_joint = float(rec.get("monthly_joint_cost", 0.0))
            tenure.add(int(rec["ten"]), w, monthly_joint)
        else:
            attr = f"{bucket}_weight"
            setattr(ledger, attr, getattr(ledger, attr) + w)
            ledger.reasons[bucket] = ledger.reasons.get(bucket, 0) + 1
    ledger.reconcile()
    if ledger.included_weight > 0:
        tenure.reconcile_included(ledger.included_weight)
    return ledger, tenure
