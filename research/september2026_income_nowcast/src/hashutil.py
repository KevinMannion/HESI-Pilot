import hashlib
from pathlib import Path


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(8 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def require_hash(path, expected, label):
    path = Path(path)
    got = sha256_file(path)
    if got != expected:
        raise SystemExit(f"HASH MISMATCH {label}: {got} != {expected}")
    return got
