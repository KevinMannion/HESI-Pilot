"""SHA-256 helper for the 2024 matched-year cost-input pipeline."""
import hashlib
from pathlib import Path


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def file_record(path):
    path = Path(path)
    return {
        "path": str(path),
        "basename": path.name,
        "size_bytes": path.stat().st_size if path.is_file() else None,
        "sha256": sha256(path) if path.is_file() else None,
        "present": path.is_file(),
    }
