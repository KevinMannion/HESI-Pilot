"""Versioned AUDIT_MANIFEST for scratch runs (never overwrites frozen results)."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def build_audit_manifest(
    *,
    run_id: str,
    output_dir: Path,
    comparison_target: str,
    git_commit: str | None,
    parity_status: str,
    extra: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    output_dir = Path(output_dir)
    manifest: dict[str, Any] = {
        "run_id": run_id,
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "audit_schema_version": "hesi_audit_v2",
        "output_dir": str(output_dir.resolve()),
        "comparison_target": comparison_target,
        "git_commit": git_commit,
        "parity_status": parity_status,
        "frozen_reference_hashes": {},
        "files_written": [],
    }
    for name in ("audit.json", "AUDIT_MANIFEST.json", "pipeline_result.json"):
        p = output_dir / name
        if p.is_file():
            manifest["files_written"].append({"path": name, "sha256": sha256_file(p)})
    if extra:
        manifest.update(extra)
    return manifest


def write_audit_manifest(output_dir: Path, manifest: dict[str, Any]) -> Path:
    dest = Path(output_dir) / "AUDIT_MANIFEST.json"
    dest.write_text(json.dumps(manifest, indent=2) + "\n")
    return dest
