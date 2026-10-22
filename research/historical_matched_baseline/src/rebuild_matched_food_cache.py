"""Rebuild ACS 2024 person food sums using 2024 Thrifty annual-mean cells.

Does not price September 2026 food. Does not write core_r24 caches or national_R22.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "core_r24" / "src"))
from food_model import age_key, load_prices  # noqa: E402

CATEGORIES = [("Child", 1), ("Child", 2), ("Child", 4), ("Child", 6), ("Child", 9)] + [
    (s, a) for s in ("Male", "Female") for a in (12, 14, 19, 20, 51, 71)
]


def lookup(catalog, year, month, group, age):
    sex = None if group == "Child" else group
    g, band = age_key(age, sex, "thrifty")
    key = (year, month, "thrifty", g, band)
    if key in catalog:
        return catalog[key]
    if band == "14-19 years":
        alt = (year, month, "thrifty", g, "14-18 years")
        if alt in catalog:
            return catalog[alt]
    raise KeyError(key)


def annual_mean_vector(catalog, year=2024):
    values = []
    for group, age in CATEGORIES:
        months = [lookup(catalog, year, month, group, age) for month in range(1, 13)]
        if len(months) != 12:
            raise ValueError(f"Need 12 months for {group} {age}")
        values.append(sum(months) / 12.0)
    return np.array(values, dtype=float)


def rebuild(person_zips, prices, out, year=2024):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    catalog, issues = load_prices(prices)
    conflicts = [i for i in issues if i["type"] == "conflicting_duplicate" and i["key"][0] == year]
    if conflicts:
        raise ValueError("Conflicting USDA keys for matched year")
    value = annual_mean_vector(catalog, year)
    foods = []
    comps = []
    count = 0
    for file in person_zips:
        tag = hashlib.sha256((str(Path(file).resolve()) + f"|thrifty_{year}annual").encode()).hexdigest()[:12]
        fp = out / ("food_part_" + tag + ".pkl")
        cp = out / ("composition_part_" + tag + ".pkl")
        if fp.exists() and cp.exists():
            foods.append(pd.read_pickle(fp))
            comps.append(pd.read_pickle(cp))
            print("Resumed", file, flush=True)
            continue
        filefoods = []
        filecomps = []
        with zipfile.ZipFile(file) as z:
            members = [n for n in z.namelist() if Path(n).name.lower().startswith("psam_pus") and n.lower().endswith(".csv")]
            if not members:
                raise ValueError("Missing person CSV " + str(file))
            for member in members:
                for d in pd.read_csv(z.open(member), usecols=["SERIALNO", "AGEP", "SEX", "RELSHIPP"], dtype={"SERIALNO": str}, chunksize=175000):
                    age = d.AGEP.to_numpy()
                    sex = d.SEX.to_numpy()
                    rel = d.RELSHIPP.to_numpy()
                    cat = np.select(
                        [age == 1, (age >= 2) & (age <= 3), (age >= 4) & (age <= 5), (age >= 6) & (age <= 8), (age >= 9) & (age <= 11)],
                        [0, 1, 2, 3, 4],
                        default=-1,
                    )
                    for ix, sexcode in enumerate((1, 2)):
                        for j, (lo, hi) in enumerate([(12, 13), (14, 18), (19, 19), (20, 50), (51, 70), (71, 120)]):
                            cat[(age >= lo) & (age <= hi) & (sex == sexcode)] = 5 + ix * 6 + j
                    if ((cat < 0) & (age != 0)).any():
                        raise ValueError("Unknown person category")
                    food = pd.DataFrame(
                        {
                            "SERIALNO": d.SERIALNO,
                            "thrifty_2024annual": np.where(cat >= 0, value[np.maximum(cat, 0)], 0),
                            "n_person": 1,
                            "n_infant": (age == 0).astype("int8"),
                        }
                    )
                    filefoods.append(food.groupby("SERIALNO", sort=False)[["thrifty_2024annual", "n_person", "n_infant"]].sum())
                    comp = pd.DataFrame(
                        {
                            "SERIALNO": d.SERIALNO,
                            "adult": (age >= 18).astype("int8"),
                            "partner": np.isin(rel, [21, 22, 23, 24]).astype("int8"),
                            "male_child": ((age < 18) & (sex == 1)).astype("int8"),
                            "female_child": ((age < 18) & (sex == 2)).astype("int8"),
                            "young_child": (age < 6).astype("int8"),
                            "child": (age < 18).astype("int8"),
                        }
                    )
                    filecomps.append(
                        comp.groupby("SERIALNO", sort=False)[["adult", "partner", "male_child", "female_child", "young_child", "child"]].sum()
                    )
                    count += len(d)
        onefood = pd.concat(filefoods).groupby(level=0).sum()
        onecomp = pd.concat(filecomps).groupby(level=0).sum()
        onefood.to_pickle(fp)
        onecomp.to_pickle(cp)
        foods.append(onefood)
        comps.append(onecomp)
        print("Checkpoint", file, "persons:", count, flush=True)
    food = pd.concat(foods).groupby(level=0).sum()
    comp = pd.concat(comps).groupby(level=0).sum()
    food.to_pickle(out / "acs2024_food_person_aggregates.pkl")
    comp.to_pickle(out / "acs2024_person_composition.pkl")
    summary = {"person_rows": count, "households_food": len(food), "households_composition": len(comp), "food_column": "thrifty_2024annual", "year": year}
    print("SUMMARY", json.dumps(summary), flush=True)
    return summary


def main():
    a = argparse.ArgumentParser()
    a.add_argument("--person-zips", nargs="+", required=True)
    a.add_argument("--prices", default=str(ROOT / "core_r24/inputs/source_2024_2026.csv"))
    a.add_argument("--out", required=True)
    x = a.parse_args()
    rebuild(x.person_zips, x.prices, x.out)


if __name__ == "__main__":
    main()
