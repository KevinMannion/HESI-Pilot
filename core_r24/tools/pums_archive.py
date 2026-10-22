"""Verify ACS PUMS ZIP containers at ZIP and inner-CSV layers. Does not weaken checksums."""
from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path

LOCK_PATH = Path(__file__).resolve().parents[1] / "PUMS_ARCHIVE_LOCK.json"
REQUIRED_PERSON_CSV = ("psam_pusa.csv", "psam_pusb.csv")
REQUIRED_HOUSING_CSV = ("psam_husa.csv", "psam_husb.csv")


def load_lock(path=LOCK_PATH):
    return json.loads(Path(path).read_text())


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_zip_member(zip_path, member):
    h = hashlib.sha256()
    with zipfile.ZipFile(zip_path) as z:
        with z.open(member) as f:
            for chunk in iter(lambda: f.read(8 * 1024 * 1024), b""):
                h.update(chunk)
    return h.hexdigest()


def csv_members(zip_path, prefix):
    with zipfile.ZipFile(zip_path) as z:
        names = [n for n in z.namelist() if Path(n).name.lower().startswith(prefix) and n.lower().endswith(".csv")]
    return names


def verify_split_person_zips(part1, part2, lock=None):
    lock = lock or load_lock()
    got = {"person_part_1": sha256_file(part1), "person_part_2": sha256_file(part2)}
    exp = lock["r24_locked_zip_sha256"]
    if got["person_part_1"] != exp["person_part_1"] or got["person_part_2"] != exp["person_part_2"]:
        raise RuntimeError(f"INPUT HASH MISMATCH split person ZIPs: {got} != {exp['person_part_1']}/{exp['person_part_2']}")
    return {"mode": "split_zips", "zip_sha256": got, "status": "PASS"}


def verify_official_person_zip(path, lock=None):
    lock = lock or load_lock()
    members = csv_members(path, "psam_pus")
    bases = {Path(n).name.lower(): n for n in members}
    missing = [n for n in REQUIRED_PERSON_CSV if n not in bases]
    if missing:
        raise RuntimeError(f"Official person ZIP missing inner CSV {missing}")
    inner = {}
    for name in REQUIRED_PERSON_CSV:
        digest = sha256_zip_member(path, bases[name])
        expected = lock["inner_csv_sha256"][name]
        if digest != expected:
            raise RuntimeError(f"INNER CSV HASH MISMATCH {name}: {digest} != {expected}")
        inner[name] = digest
    return {
        "mode": "official_combined_zip",
        "zip_sha256": sha256_file(path),
        "inner_csv_sha256": inner,
        "status": "PASS",
        "note": "ZIP-level hash may differ from split archives; inner CSV hashes are the content lock.",
    }


def verify_housing_zip(path, lock=None):
    lock = lock or load_lock()
    digest = sha256_file(path)
    expected = lock["r24_locked_zip_sha256"]["housing_csv_hus.zip"]
    if digest == expected:
        return {"mode": "housing_zip_sha256", "zip_sha256": digest, "status": "PASS"}
    members = csv_members(path, "psam_hus")
    bases = {Path(n).name.lower(): n for n in members}
    inner = {}
    for name in REQUIRED_HOUSING_CSV:
        if name not in bases:
            raise RuntimeError(f"Housing ZIP missing {name} and ZIP SHA-256 mismatch: {digest} != {expected}")
        got = sha256_zip_member(path, bases[name])
        exp = lock["inner_csv_sha256"][name]
        if got != exp:
            raise RuntimeError(f"INNER CSV HASH MISMATCH {name}: {got} != {exp}")
        inner[name] = got
    return {"mode": "housing_inner_csv", "zip_sha256": digest, "inner_csv_sha256": inner, "status": "PASS"}


def person_zip_args(official=None, part1=None, part2=None, lock=None):
    """Return the path list to pass to rebuild_raw_person_caches.py after verification."""
    lock = lock or load_lock()
    if official and not (part1 or part2):
        verify_official_person_zip(official, lock)
        return [str(Path(official).resolve())]
    if part1 and part2 and not official:
        verify_split_person_zips(part1, part2, lock)
        return [str(Path(part1).resolve()), str(Path(part2).resolve())]
    raise ValueError("Provide either --person-official csv_pus.zip or both split person ZIPs")
