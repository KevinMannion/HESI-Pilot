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
