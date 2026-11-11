"""Provisional five-tier affordability classification (engineering only; not science-approved)."""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

from components.base import EssentialCostResult, MissingStatus

# Six-cost letters: H, F, T, M (healthcare), K (childcare), O (other essentials).
SIX_COST_KEYS: tuple[str, ...] = (
    "housing",
    "food",
    "transportation",
    "healthcare",
    "childcare",
    "other_necessities",
)
SIX_COST_LETTERS: dict[str, str] = {
    "housing": "H",
    "food": "F",
    "transportation": "T",
    "healthcare": "M",
    "childcare": "K",
    "other_necessities": "O",
}

TIER_LABELS: tuple[str, ...] = (
    "extremely_financially_insecure",
    "financially_insecure",
    "financially_vulnerable",
    "financially_secure",
    "extremely_financially_secure",
)

TIER_LABELS_DISPLAY: tuple[str, ...] = (
    "Extremely financially insecure",
    "Financially insecure",
    "Financially vulnerable",
    "Financially secure",
    "Extremely financially secure",
)

AFFORDABILITY_BOUNDARY_RATIO = 1.0


class ProvisionalClassificationError(ValueError):
    pass


@dataclass(frozen=True)
class ProvisionalTierThresholds:
    """Four ascending boundaries on R=D/C separating five tiers (engineering / test only)."""

    boundary_r_tier_1_2: float
    boundary_r_tier_2_3: float
    boundary_r_tier_3_4: float
    boundary_r_tier_4_5: float
    policy_approved: bool = False
    label: str = "provisional_unapproved_engineering"

    def validate(self) -> None:
        b = (
            self.boundary_r_tier_1_2,
            self.boundary_r_tier_2_3,
            self.boundary_r_tier_3_4,
            self.boundary_r_tier_4_5,
        )
        for x in b:
            if not math.isfinite(x):
                raise ProvisionalClassificationError("tier boundary must be finite")
        if not (b[0] < b[1] < b[2] < b[3]):
            raise ProvisionalClassificationError("tier boundaries must be strictly increasing")
        if self.policy_approved:
            raise ProvisionalClassificationError("provisional tier thresholds cannot be policy_approved")

    def as_tuple(self) -> tuple[float, float, float, float]:
        self.validate()
        return (
            self.boundary_r_tier_1_2,
            self.boundary_r_tier_2_3,
            self.boundary_r_tier_3_4,
            self.boundary_r_tier_4_5,
        )


@dataclass(frozen=True)
class ProvisionalClassificationResult:
    status: str  # "complete" | "unresolved"
    disposable_d_usd: float
    total_essential_c_usd: float | None
    annual_surplus_usd: float | None
    affordability_ratio: float | None
    tier_number: int | None
    tier_code: str | None
    tier_label_display: str | None
    component_annual_usd: dict[str, float] = field(default_factory=dict)
    blockers: tuple[str, ...] = ()
    scientific_approval: str = "not_approved"
    tier_thresholds_approved: bool = False
    national_headline_eligible: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "disposable_d_usd": self.disposable_d_usd,
            "total_essential_c_usd": self.total_essential_c_usd,
            "annual_surplus_usd": self.annual_surplus_usd,
            "affordability_ratio": self.affordability_ratio,
            "tier_number": self.tier_number,
            "tier_code": self.tier_code,
            "tier_label_display": self.tier_label_display,
            "component_annual_usd": dict(self.component_annual_usd),
            "blockers": list(self.blockers),
            "scientific_approval": self.scientific_approval,
            "tier_thresholds_approved": self.tier_thresholds_approved,
            "national_headline_eligible": self.national_headline_eligible,
            "affordability_boundary_r": AFFORDABILITY_BOUNDARY_RATIO,
        }


def _extract_priced_components(
    costs: Mapping[str, Any] | Sequence[EssentialCostResult | Mapping[str, Any]],
) -> tuple[dict[str, float] | None, tuple[str, ...]]:
    blockers: list[str] = []
    out: dict[str, float] = {}
    if isinstance(costs, Mapping):
        for key in SIX_COST_KEYS:
            if key not in costs:
                blockers.append(f"missing_component:{key}")
                continue
            val = costs[key]
            if isinstance(val, (int, float)):
                if not math.isfinite(float(val)) or float(val) < 0:
                    blockers.append(f"invalid_amount:{key}")
                else:
                    out[key] = float(val)
            else:
                blockers.append(f"invalid_shape:{key}")
        return (out if not blockers and len(out) == 6 else None, tuple(blockers))

    by_name: dict[str, Mapping[str, Any]] = {}
    for row in costs:
        if isinstance(row, EssentialCostResult):
            by_name[row.component] = row.to_dict()
        elif isinstance(row, Mapping):
            by_name[str(row.get("component", ""))] = row
    for key in SIX_COST_KEYS:
        row = by_name.get(key)
        if row is None:
            blockers.append(f"missing_component:{key}")
            continue
        status = row.get("missing_status")
        if status != MissingStatus.PRICED.value and status != MissingStatus.PRICED:
            blockers.append(f"{key}:{status}")
            continue
        annual = row.get("annual_usd")
        if annual is None:
            blockers.append(f"{key}:missing_annual_usd")
            continue
        amt = float(annual)
        if not math.isfinite(amt) or amt < 0:
            blockers.append(f"invalid_amount:{key}")
            continue
        out[key] = amt
    if blockers:
        return None, tuple(blockers)
    return out, ()


def assign_tier_from_ratio(
    affordability_ratio: float,
    thresholds: ProvisionalTierThresholds,
) -> tuple[int, str, str]:
    thresholds.validate()
    b = thresholds.as_tuple()
    r = affordability_ratio
    if r < b[0]:
        n = 1
    elif r < b[1]:
        n = 2
    elif r < b[2]:
        n = 3
    elif r < b[3]:
        n = 4
    else:
        n = 5
    return n, TIER_LABELS[n - 1], TIER_LABELS_DISPLAY[n - 1]


def classify_provisional_five_tier(
    *,
    disposable_usd: float,
    costs: Mapping[str, Any] | Sequence[EssentialCostResult | Mapping[str, Any]],
    tier_thresholds: ProvisionalTierThresholds | None = None,
) -> ProvisionalClassificationResult:
    """Fail-closed six-cost classification; tiers require explicit unapproved thresholds."""
    if not math.isfinite(disposable_usd):
        return ProvisionalClassificationResult(
            status="unresolved",
            disposable_d_usd=disposable_usd,
            total_essential_c_usd=None,
            annual_surplus_usd=None,
            affordability_ratio=None,
            tier_number=None,
            tier_code=None,
            tier_label_display=None,
            blockers=("nonfinite_disposable",),
        )

    priced, blockers = _extract_priced_components(costs)
    if priced is None:
        return ProvisionalClassificationResult(
            status="unresolved",
            disposable_d_usd=disposable_usd,
            total_essential_c_usd=None,
            annual_surplus_usd=None,
            affordability_ratio=None,
            tier_number=None,
            tier_code=None,
            tier_label_display=None,
            blockers=blockers,
        )

    total_c = round(sum(priced[k] for k in SIX_COST_KEYS), 2)
    if total_c <= 0:
        return ProvisionalClassificationResult(
            status="unresolved",
            disposable_d_usd=disposable_usd,
            total_essential_c_usd=total_c,
            annual_surplus_usd=None,
            affordability_ratio=None,
            tier_number=None,
            tier_code=None,
            tier_label_display=None,
            component_annual_usd=priced,
            blockers=("zero_or_negative_essential_total",),
        )

    surplus = round(disposable_usd - total_c, 2)
    ratio = round(disposable_usd / total_c, 6)

    tier_n = tier_code = tier_disp = None
    tier_blockers: list[str] = []
    if tier_thresholds is None:
        tier_blockers.append("tier_thresholds_not_supplied")
    else:
        try:
            tier_thresholds.validate()
            tier_n, tier_code, tier_disp = assign_tier_from_ratio(ratio, tier_thresholds)
        except ProvisionalClassificationError as e:
            tier_blockers.append(str(e))

    return ProvisionalClassificationResult(
        status="complete",
        disposable_d_usd=disposable_usd,
        total_essential_c_usd=total_c,
        annual_surplus_usd=surplus,
        affordability_ratio=ratio,
        tier_number=tier_n,
        tier_code=tier_code,
        tier_label_display=tier_disp,
        component_annual_usd=priced,
        blockers=tuple(tier_blockers),
        tier_thresholds_approved=bool(tier_thresholds.policy_approved) if tier_thresholds else False,
    )


def classify_from_audit(
    audit: Mapping[str, Any],
    *,
    tier_thresholds: ProvisionalTierThresholds | None = None,
) -> ProvisionalClassificationResult:
    disposable = audit.get("disposable_resources") or {}
    d = disposable.get("annual_disposable_usd")
    if d is None:
        return ProvisionalClassificationResult(
            status="unresolved",
            disposable_d_usd=float("nan"),
            total_essential_c_usd=None,
            annual_surplus_usd=None,
            affordability_ratio=None,
            tier_number=None,
            tier_code=None,
            tier_label_display=None,
            blockers=("missing_disposable",),
        )
    costs = audit.get("essential_costs") or []
    return classify_provisional_five_tier(
        disposable_usd=float(d),
        costs=costs,
        tier_thresholds=tier_thresholds,
    )
