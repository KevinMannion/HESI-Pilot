"""Resolve Grok register local_path values to host data roots (hesi-data and scratch)."""
from __future__ import annotations

import os
from pathlib import Path

REGISTER_DATA_PREFIX = "/workspace/hesi-data/"
REGISTER_SCRATCH_PREFIX = "/workspace/scratch/"


def hesi_data_root() -> Path | None:
    env = os.environ.get("HESI_DATA_ROOT", "").strip()
    if env:
        p = Path(env).expanduser()
        if p.is_dir():
            return p.resolve()
    for candidate in (
        Path.home() / "hesi-data",
        Path("/workspace/hesi-data"),
    ):
        if candidate.is_dir():
            return candidate.resolve()
    return None


def hesi_scratch_root() -> Path | None:
    env = os.environ.get("HESI_SCRATCH_ROOT", "").strip()
    if env:
        p = Path(env).expanduser()
        if p.is_dir():
            return p.resolve()
    candidate = Path("/workspace/scratch")
    if candidate.is_dir():
        return candidate.resolve()
    return None


def resolve_register_local_path(local_path: str) -> Path | None:
    if not local_path or not str(local_path).strip():
        return None
    lp = str(local_path).strip()
    if lp.startswith(REGISTER_DATA_PREFIX):
        root = hesi_data_root()
        if root is None:
            return None
        rel = lp[len(REGISTER_DATA_PREFIX) :]
        candidate = (root / rel).resolve()
        return candidate if candidate.is_file() else None
    if lp.startswith(REGISTER_SCRATCH_PREFIX):
        root = hesi_scratch_root()
        if root is None:
            return None
        rel = lp[len(REGISTER_SCRATCH_PREFIX) :]
        candidate = (root / rel).resolve()
        return candidate if candidate.is_file() else None
    p = Path(lp)
    if p.is_file():
        return p.resolve()
    return None
