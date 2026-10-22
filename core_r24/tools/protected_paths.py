"""Fail-closed guards for frozen scientific output directories."""
from __future__ import annotations

from pathlib import Path

CORE = Path(__file__).resolve().parents[1]
REPO = CORE.parent
PROTECTED_RELATIVE = (
    "results/national_R22",
    "results/rebuilt_from_raw",
    "results/synthetic",
)


def protected_directories():
    return (
        *((CORE / rel).resolve() for rel in PROTECTED_RELATIVE),
        (REPO / "research/historical_matched_baseline/results/matched2024_provisional").resolve(),
    )


def frozen_scientific_files():
    return {
        (REPO / "results.csv").resolve(),
        (REPO / "audit.json").resolve(),
        (REPO / "manifest.json").resolve(),
    }


def assert_output_allowed(path, label="output"):
    path = Path(path).resolve()
    if path in frozen_scientific_files():
        raise RuntimeError(f"PROTECTED OUTPUT PATH: {label} {path} is a frozen scientific file.")
    for frozen in protected_directories():
        if path == frozen or frozen in path.parents:
            raise RuntimeError(
                f"PROTECTED OUTPUT PATH: {label} {path} is inside frozen scientific directory {frozen}. "
                "Refuse before creating directories or caches."
            )
    return path
