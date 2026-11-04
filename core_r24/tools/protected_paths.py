"""Fail-closed guards for frozen scientific output directories."""
from __future__ import annotations

import shutil
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


def forbidden_output_zones():
    """Git metadata and core source trees must never receive reproduction output."""
    return (
        (REPO / ".git").resolve(),
        (CORE / "src").resolve(),
        (CORE / "tools").resolve(),
    )


def _unsafe_reason(path, label):
    path = Path(path)
    resolved = path.resolve()
    if path.is_symlink():
        return (
            f"UNSAFE OUTPUT: {label} {path} is a symlink resolving to {resolved}. "
            "Refuse before creating, deleting, copying, or promoting outputs."
        )
    roots = (REPO.resolve(), CORE.resolve())
    protected = tuple(protected_directories())
    zones = tuple(forbidden_output_zones())
    files = frozen_scientific_files()
    for candidate in (path, resolved):
        cand = candidate if candidate.is_absolute() else candidate.resolve()
        if cand in files:
            return f"PROTECTED OUTPUT PATH: {label} {cand} is a frozen scientific file."
        if cand in roots:
            return f"PROTECTED OUTPUT PATH: {label} {cand} is the repository or core package root."
        for zone in zones:
            if cand == zone or zone in cand.parents:
                return (
                    f"PROTECTED OUTPUT PATH: {label} {cand} is inside forbidden output zone {zone}. "
                    "Refuse before creating, deleting, copying, or promoting outputs."
                )
        for frozen in protected:
            if cand == frozen or frozen in cand.parents:
                return (
                    f"PROTECTED OUTPUT PATH: {label} {cand} is inside frozen scientific directory {frozen}. "
                    "Refuse before creating directories or caches."
                )
            if cand in frozen.parents:
                return (
                    f"PROTECTED OUTPUT PATH: {label} {cand} is an ancestor of frozen scientific directory {frozen}. "
                    "Recursive delete would remove protected artifacts."
                )
    return None


def assert_output_allowed(path, label="output"):
    reason = _unsafe_reason(path, label)
    if reason:
        raise RuntimeError(reason)
    return Path(path).resolve()


def promote_staging_to_output(staging, dest, label="output"):
    """Copy staging to dest. Never shutil.rmtree a user-supplied directory."""
    staging = Path(staging)
    dest = Path(dest)
    assert_output_allowed(dest, label)
    if dest.exists() and dest.is_symlink():
        raise RuntimeError(f"UNSAFE OUTPUT: {label} {dest} is a symlink; refuse to promote through it.")
    if dest.exists() and dest.is_file():
        raise RuntimeError(f"UNSAFE OUTPUT: {label} {dest} is a file, not an empty scratch directory.")
    if dest.exists() and dest.is_dir():
        remaining = [p for p in dest.iterdir()]
        if remaining:
            raise RuntimeError(
                f"UNSAFE OUTPUT: {label} {dest} is a nonempty directory the script does not own; "
                "refusing recursive delete."
            )
        dest.rmdir()
    assert_output_allowed(dest, label)
    if not staging.is_dir():
        raise RuntimeError(f"UNSAFE OUTPUT: staging {staging} is missing")
    shutil.copytree(staging, dest)
    return dest
