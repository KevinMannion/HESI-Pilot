"""2026 input manifest verification harness (abort on mismatch; never writes frozen dirs)."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

MANIFEST_VERSION = "hesi_input_manifest_2026_v1"
REPO = Path(__file__).resolve().parents[3]
DEFAULT_MANIFEST = Path(__file__).resolve().parent / "input_manifest_2026.json"


class ManifestVerifyError(RuntimeError):
    pass


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _load_manifest(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ManifestVerifyError(f"missing manifest file: {path}")
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as e:
        raise ManifestVerifyError(f"malformed manifest JSON: {path}") from e
    if not isinstance(data, dict):
        raise ManifestVerifyError("manifest root must be an object")
    if data.get("manifest_version") != MANIFEST_VERSION:
        raise ManifestVerifyError(
            f"unsupported manifest_version: {data.get('manifest_version')!r} (want {MANIFEST_VERSION})"
        )
    pins = data.get("pins")
    if not isinstance(pins, dict) or not pins:
        raise ManifestVerifyError("manifest pins must be a non-empty object")
    for key, meta in pins.items():
        if not isinstance(meta, dict):
            raise ManifestVerifyError(f"pin {key!r} metadata must be an object")
        if "rel_path" not in meta or "sha256" not in meta:
            raise ManifestVerifyError(f"pin {key!r} missing rel_path or sha256")
        if not isinstance(meta["sha256"], str) or len(meta["sha256"]) != 64:
            raise ManifestVerifyError(f"pin {key!r} sha256 must be 64 hex chars")
    return data


def verify_input_manifest(
    manifest_path: Path | None = None,
    *,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    """Verify every required pin exists on disk and matches sha256. Returns verification report."""
    manifest_path = Path(manifest_path or DEFAULT_MANIFEST)
    repo_root = Path(repo_root or REPO)
    data = _load_manifest(manifest_path)
    pins: dict[str, Any] = data["pins"]
    verified: dict[str, str] = {}
    skipped_optional: list[str] = []
    for key, meta in sorted(pins.items()):
        required = bool(meta.get("required", True))
        rel = str(meta["rel_path"])
        want = str(meta["sha256"]).lower()
        path = repo_root / rel
        if not path.is_file():
            if required:
                raise ManifestVerifyError(f"required input missing: {key} -> {path}")
            skipped_optional.append(key)
            continue
        got = _sha256_file(path)
        if got != want:
            raise ManifestVerifyError(f"hash mismatch {key}: got {got} want {want} ({path})")
        verified[key] = got
    report = {
        "manifest_version": MANIFEST_VERSION,
        "manifest_path": str(manifest_path.resolve()),
        "verified_count": len(verified),
        "verified_pins": verified,
        "skipped_optional_missing": skipped_optional,
        "status": "PASS",
    }
    return report


def verify_input_manifest_or_abort(manifest_path: Path | None = None) -> dict[str, Any]:
    return verify_input_manifest(manifest_path)
