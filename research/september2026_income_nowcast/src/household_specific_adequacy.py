"""Household-specific adequacy diagnostic, distinct from G3's uniform-cost proxy.

Does not run a national September 2026 nowcast. Does not write national_R22.
"""
from __future__ import annotations

import numpy as np


FROZEN_R24_MEAN_MONTH = 2894.90805340822


def uniform_threshold_share(monthly_income, weight, threshold=FROZEN_R24_MEAN_MONTH):
    """G3-style proxy: every household compared to the same mean cost."""
    income = np.asarray(monthly_income, dtype=float)
    w = np.asarray(weight, dtype=float)
    if w.sum() <= 0:
        raise ValueError("weights must be positive in total")
    return float((w * (income < threshold)).sum() / w.sum())


def household_specific_share(monthly_income, monthly_cost, weight):
    """Same-household comparison: income vs that household's modeled cost."""
    income = np.asarray(monthly_income, dtype=float)
    cost = np.asarray(monthly_cost, dtype=float)
    w = np.asarray(weight, dtype=float)
    if not (len(income) == len(cost) == len(w)):
        raise ValueError("income, cost, and weight must be aligned")
    if w.sum() <= 0:
        raise ValueError("weights must be positive in total")
    return float((w * (income < cost)).sum() / w.sum())


def backtest_protocol():
    """Declared protocol for a later historical run. Not executed nationally here."""
    return {
        "name": "household_specific_three_cost_backtest",
        "status": "DESIGNED_NOT_NATIONALLY_EXECUTED",
        "universe": "R2.4 eligibility frame of ACS year T (TYPEHUGQ==1, geography/bedroom/infant filters), not the occupied-only G3 universe.",
        "income_origin": "Observed ACS T HINCP*ADJINC/1e6/12",
        "income_projected": "M4_scored overlay of T→T+1 factors on reconstructed sources; labeled PROJECTED not NOWCAST.",
        "cost": "Household-specific food+housing+transport using year-T (or declared year-T+1) modeled schedules, not the $2,894.91 mean.",
        "g3_relationship": "G3 remains a locked diagnostic proxy. Passing or failing G3 is not household-specific HESI validation.",
        "forbidden": [
            "Do not publish a September 2026 national nowcast from this design.",
            "Do not overwrite national_R22 or 18.9918%.",
            "Do not treat the uniform $2,894.91 threshold as household rent/food/car.",
        ],
        "nowcast": "NO-GO",
    }
