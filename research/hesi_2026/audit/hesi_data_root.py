"""Resolve Grok register local_path values (/workspace/hesi-data/...) to a host data root."""
from __future__ import annotations

import os
from pathlib import Path

REGISTER_PATH_PREFIX = "/workspace/hesi-data/"


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


def resolve_register_local_path(local_path: str) -> Path | None:
    if not local_path or not str(local_path).strip():
        return None
    lp = str(local_path).strip()
    root = hesi_data_root()
    if lp.startswith(REGISTER_PATH_PREFIX):
        if root is None:
            return None
        rel = lp[len(REGISTER_PATH_PREFIX) :]
        return (root / rel).resolve()
    p = Path(lp)
    if p.is_file():
        return p.resolve()
    return None
