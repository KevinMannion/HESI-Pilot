"""Release gates for national headline and six-component completeness."""

NATIONAL_HEADLINE_ENABLED = False

PRODUCTION_REQUIREMENTS = (
    "six_components_priced_and_policy_approved",
    "disposable_resources_approved_vintage",
    "household_universe_policies_approved",
    "no_reserved_holdout_inspection",
)


def production_headline_allowed() -> bool:
    return NATIONAL_HEADLINE_ENABLED


def reserved_holdout_inspection_enforced() -> bool:
    """CPS ASEC 2026 reserved validation policy is fail-closed in official entry points."""
    from audit.reserved_validation_policy import DESIGNATION_PRIOR_EXPOSURE

    return DESIGNATION_PRIOR_EXPOSURE == "PRIOR_EXPOSURE_RESTRICTED_VALIDATION"


def six_component_complete(cost_dicts: list[dict]) -> tuple[bool, list[str]]:
    needed = {"housing", "food", "transportation", "healthcare", "childcare", "other_necessities"}
    got = {c["component"] for c in cost_dicts if c.get("missing_status") == "priced"}
    missing = sorted(needed - got)
    approved = [c["component"] for c in cost_dicts if c.get("policy_approved")]
    blockers = []
    if missing:
        blockers.append(f"unpriced:{','.join(missing)}")
    for name in needed:
        if name in got and name not in approved:
            blockers.append(f"unapproved:{name}")
    return not blockers and not missing, blockers
