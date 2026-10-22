# D-05 DECISION MEMO: lock drift and in-place hash replacement (input to Kevin's decision; not the decision)

> **AI methods review, not independent human peer review; recommendations for Kevin, not approvals.**
> Author: Quantitative Methodology & Statistical Audit Lead (Grok Bot, Methods Reviewer role). Written 2026-10-22, about 04:35 UTC.
> **Base:** branch head `273406208abe439cbad960567f32822b870c43b5` ("Publish provisional 2024 matched-year engine and engineering fixes", author Kevin Mannion, 2026-10-21 23:55 −0400). Remote head re-checked with `git ls-remote` before writing. Parent commits: `e45eb8766263eed52f6d7894e3464f8ffea76094` and `fb58ddc045976d844c6da1fca99ed1f9f108bb85`. **Research version:** Core R2.5 (STATUS.txt header).
> **Status:** the Coordinator has escalated **re-lock vs revert** to Kevin. This memo is input to that decision.
> **Kevin's provisional preference, as reported by the Coordinator (not confirmed by me):** keep the useful engineering fixes, create versioned v2 integrity manifests rather than revert, and implement nothing until this memo is complete and names any scientific-methodology implications.
> **Labels:** **VERIFIED** = I ran or read it myself (command, hash or file:line cited). **HYPOTHESIS** = not yet shown by evidence I checked.
> **Implementers:** only Kevin or Cursor may change the repo. Items marked **[K/C]** are implementable only by Kevin or Cursor.

---

## 0. One-paragraph summary
- Three changes share one pattern: hash-locked or locked-package files were changed in place without a recorded decision.
  1. **D-05 (e45eb87):** two locked core_r24 scripts were changed and their `RELEASE_FILE_HASHES.json` entries overwritten in place. The housing input check was also loosened.
  2. **run_joint (2734062):** the locked engine `src/run_joint.py` was changed and its hash replaced in place.
  3. **Pillar-lock drift (2734062):** three files inside the locked September 2026 pillar packages were changed, and **no** pillar manifest was updated. Four manifests now disagree with the files, and `verify_release.py` cannot detect it.
- **No frozen numeric result is changed** (VERIFIED, §5).
- Every engineering change I traced preserves the computed values on default inputs (VERIFIED for R2.4 national; §3).
- Two items carry methodology implications and belong to Kevin:
  - the matched-year FMR schedule (12 HUD reevaluation areas, §3 C4);
  - publishing the provisional 17.6839565% figure while its own committed readiness record says NO-GO (§3 C5; rule-6 escalation).

---

## 1. VERIFIED FACTS

### 1.1 What changed, per file (old → new hash, commit, diff lines)

| # | File | Locked by | Original hash (commit) | Intermediate | Current hash at 2734062 | Changed in | Manifest updated? |
|---|---|---|---|---|---|---|---|
| 1 | `core_r24/reproduce_from_raw.py` | `core_r24/RELEASE_FILE_HASHES.json` | `c6783be3d70798b2d253e75e3941098d01d7e48fe94bdf42c352c566283ea481` (fb58ddc) | — | `6b41f2e01dfc1e959ddc3bfcc8e6776a3c3ab1bcfcee500d935d4644e3c5755e` | e45eb87 | **in place** (old value gone from HEAD) |
| 2 | `core_r24/rebuild_raw_person_caches.py` | same | `d9a20f2e0fb0e99f5437c15af76dd78fa65dd5610d676f3baca134d3e16128e5` (fb58ddc) | — | `97d51efa6d6b2cf762dc84e7fcd74f0fbecdfed82e8510e3c67ab1e238640769` | e45eb87 | **in place** |
| 3 | `core_r24/src/run_joint.py` | same | `030cb0ae0baed16770e198a0c9f2353180ad3ccb55e6483d37b1c11dd3a24034` (fb58ddc = e45eb87) | — | `a34951b135936ddf539f0c33d7f3a331e10a4e59dc204889bde14f31792cce0e` | 2734062 | **in place** |
| 4 | `core_r24/PUMS_ARCHIVE_LOCK.json`, `tools/pums_archive.py`, `tests/test_pums_archive.py` | same | (absent at fb58ddc) | — | `998c85b1…`, `c34d7906…`, `fb3597fa…` | e45eb87 (added; 35 → 38 entries) | added in place, no version |
| 5 | `research/september2026_core_r2/housing/verify.py` | INTEGRITY_MANIFEST, SOURCE_HASHES, housing/PACKAGE_MANIFEST (Lock_v1) | `25fcc7fd7104bbb7df90bcfc585ffd81fa984590b9e6f971542f10b1d1ec146e` (fb58ddc = e45eb87) | — | `7145ea914761…` | 2734062 | **no** (manifests still say `25fcc7fd…`) |
| 6 | `research/september2026_core_r2/transportation/run_standard.py` | INTEGRITY_MANIFEST, transportation/SOURCE_HASHES (Lock_v1) | `d9f4c2aadd999accd17b558f1de30e4935a4606a5b718722ef249a291b349b74` | — | `70a5262c6bdd…` | 2734062 | **no** |
| 7 | `research/september2026_core_r2/transportation/test_standard.py` | same | `acdcd54297ac22edbc2eac14210233faebcc3ddfed9ed6464aa944832b68e9d6` | — | `95302c98bf9d…` | 2734062 | **no** |

Evidence:
- Rows 1–4: `git diff fb58ddc e45eb87 -- core_r24/RELEASE_FILE_HASHES.json`, which shows 2 lines replaced and 3 lines added (35 → 38 entries, verified by JSON parse). Row 3: `git diff e45eb87 2734062 -- core_r24/RELEASE_FILE_HASHES.json`, one line, `030cb0ae…` → `a34951b1…`.
- `RELEASE_FILE_HASHES.json` file hash by commit:

| Commit | SHA-256 |
|---|---|
| fb58ddc | `49871df6d998…` |
| e45eb87 | `4f6825d7678f…` |
| 2734062 | `6cd769e02202…` |

- Rows 5–7: `git show <c>:<file> | sha256sum`.
- Manifests: the original values were read from `git show fb58ddc:research/september2026_core_r2/INTEGRITY_MANIFEST.json`.
- Every pillar manifest file is byte-identical at fb58ddc, e45eb87 and 2734062:

| Manifest | SHA-256 |
|---|---|
| INTEGRITY_MANIFEST | `a0de5589…` |
| SOURCE_HASHES | `29e8aa72…` |
| housing/PACKAGE_MANIFEST | `5ecf44ae…` |
| transportation/SOURCE_HASHES | `e4fe0a48…` |
| LOCK_REGISTER | `be3388d7…` |

**Diff lines:**
- **D-05 scripts (e45eb87):**
  - `reproduce_from_raw.py`: fb58ddc `:38-42` hash-checked housing, person_a, person_b, geography and prices against fixed container hashes. e45eb87 `:43` calls `person_zip_args()`, `:44` calls `verify_housing_zip()`, and `:46` drops housing and person from the fixed-hash loop.
  - `rebuild_raw_person_caches.py`: fb58ddc `:50` required exactly 2 ZIPs. e45eb87 `:50-58` replaces this with a basename set check that runs after the caches are written.
- **Loosened housing check (e45eb87 `core_r24/tools/pums_archive.py:73-90`):**
  - `:77-78` accepts the housing ZIP if its container hash matches.
  - Otherwise `:79-90` accepts **any** ZIP whose `psam_husa/b.csv` inner hashes match the lock.
  - At fb58ddc only the exact container `8281008e…` was accepted.
- **run_joint (2734062 `core_r24/src/run_joint.py`):**
  - `:26` adds parameters `food_column`, `cost_labels`, `share_metric`, `scenario_label` and `audit_status`.
  - `:27-30` adds a guard refusing `results/national_R22`.
  - `:32` renames the food column to `food_cost`; `:57` and `:75` use it.
  - `:97-98` parameterizes the labels.
  - `:108-110` writes three new audit keys (`food_column`, `transport_annual`, `share_metric`).
- **Pillar scripts (2734062):**
  - `housing/verify.py`: lines 1–24 (the computation) are unchanged except the import line. The unconditional writes (old `:25-28`) became compare-only (`:36-42`), with writing only under `--write-tracked` (`:43-45`).
  - `transportation/run_standard.py`: the computation moved into `compute_scenarios()` with identical statements. It is compare-only (`:32-34`), with `--write-tracked` at `:35-36`.
  - `test_standard.py`: adds before/after hash assertions plus `LOCKED='19cc412e…'`. No assertion was removed.

### 1.2 Pillar manifests now mismatch; `verify_release.py` cannot see it
- My manifest re-hash at 2734062 (python over the tracked files):

| Manifest | Mismatched entries |
|---|---|
| INTEGRITY_MANIFEST.json (40 entries) | `housing/verify.py`, `transportation/run_standard.py`, `transportation/test_standard.py` |
| SOURCE_HASHES.json | `housing/verify.py` |
| housing/PACKAGE_MANIFEST.json | `verify.py` |
| transportation/SOURCE_HASHES.json | `run_standard.py`, `test_standard.py` |

  This matches the Engineer's `findings/reproducer/2026-10-22_2734062_step1.md` §1 (VERIFIED by my own re-hash).
- `research/september2026_core_r2/verify_release.py` (unchanged since fb58ddc; full text `:1-17`):
  - It runs the pillar unit tests (`:4-9`) and asserts four LOCK_REGISTER properties (`:10-14`).
  - **It opens no hash manifest.** It therefore returns all-True at 2734062 (VERIFIED: I ran it in scratch `r2734_check/tree`).
  - **Finding LD-1:** the release acceptance test cannot detect lock drift.
- The Engineer's F3b_v2 wrapper, applied to 2734062 in scratch, **does** detect it: `tools/check_pillars.py` exits 1 with the four manifest mismatches above, 0 regenerated differences and `tracked_unchanged: true` (VERIFIED, `scratch/methods-reviewer/r2734_check/cp_stack.out`).

### 1.3 Outputs unchanged (all VERIFIED)
- **Pillar outputs:** `transport_reference_2026_09.csv` (`19cc412e…`), housing `executed_results.csv` and `audit.json` are not in `git diff e45eb87 2734062`, and they match their manifest entries.
- **R2.4 national at 2734062**, from the Engineer's sealed evidence `evidence_2734062_step1/`:
  - `sha256sum -c SHA256SUMS`: 0 non-OK of 62 files.
  - SHA256SUMS sha256 `355d3d339b9e…`.
  - `run_output/national/common_cohort_results.csv` = `2734f11e…`, identical to e45eb87 and to my own runs.
- **My targeted check:**
  - `src/run_joint.py` from e45eb87 and from 2734062, run directly on identical caches, produced **byte-identical** CSVs: `04308e57…` and `f15b9fb0…` for both (scratch `r2734_check/rj_e45`, `rj_out`). So the refactor is byte-neutral.
  - Its `audit.json` gains exactly the three keys above. Every other key is equal.
- **Side observation (VERIFIED):** running `run_joint.py` directly, without the `OPENBLAS/OMP/MKL_NUM_THREADS=1` environment that `reproduce_from_raw.py:37` sets, gives last-digit differences against the documented run: max 3.8e-11 headline, 3.6e-12 replicates. All are within atol 1e-7 of national_R22 (max 1.8e-11).
  - HYPOTHESIS: the cause is thread-count-dependent floating-point summation.
  - This affects byte-identity claims, not tolerance claims.
- **Frozen files:** national_R22 `common_cohort_results.csv` `6778c312…`, `replicate_results.csv` `6d42ff33…` and `audit.json` `975cc72d…` are unchanged at 2734062 (RELEASE_FILE_HASHES entries unchanged; verify_package PASS 38/38 in scratch).

### 1.4 Guard coverage (VERIFIED)
- `run_joint.run()` refuses `results/national_R22` and any subdirectory of it (my scratch call).
- It does **not** protect `results/rebuilt_from_raw` or `results/synthetic`.
- It runs `out.mkdir` (`:31`) before reading any input.
- The Engineer's sealed step-1 evidence also shows the following: `reproduce_from_raw.py --output …/national_R22` writes about 170 MB of git-ignored person caches into `national_R22/derived_person_caches/` **before** run_joint refuses. The frozen files keep their hashes.

---

## 2. HYPOTHESES (not established)
- H-a: the loosened housing check (row 4 / §1.1) admits no wrong data in practice. The inner-CSV SHA-256 pins the content, so a re-zipped identical CSV is equivalent. A ZIP with *extra* `psam_hus*` members would still be ingested by `run_joint` at e45eb87 and 2734062; F1_v2 closes that.
- H-b: the threading cause in §1.3.
- H-c: the matched-year FMR-schedule effect is about +0.01 to +0.02 pp (Data Scout estimate). It stays a hypothesis until the Engineer's sensitivity run lands; it had not landed when I wrote this.

---

## 3. THE THREE CLASSES

### (A) Original release locks that must stay immutable
Values below are at **fb58ddc** unless noted. fb58ddc is the earliest commit on which I reviewed every lock. `d658c08`/`eec7c46` are the recorded recovery points; RELEASE_FILE_HASHES last changed before fb58ddc at eec7c46.
- `core_r24/RELEASE_FILE_HASHES.json` as of fb58ddc (sha256 `49871df6d998…`, 35 entries). Key lines:
  - `reproduce_from_raw.py` `c6783be3…`
  - `rebuild_raw_person_caches.py` `d9a20f2e…`
  - `src/run_joint.py` `030cb0ae…`
  - `verify_package.py` `1a414de8…`
  - `results/national_R22/common_cohort_results.csv` `6778c312…`, `replicate_results.csv` `6d42ff33…`, `audit.json` `975cc72d…`
  - all `inputs/*`, e.g. `source_2024_2026.csv` `90bc39d1…`, `puma_fmr_screened.csv` `210a7ec6…`
- Also: **e45eb87's** `RELEASE_FILE_HASHES.json` (`4f6825d7…`, 38 entries), which is itself already a rewritten version.
- `research/september2026_core_r2/INTEGRITY_MANIFEST.json` `a0de5589…` (40 entries, incl. `housing/verify.py` `25fcc7fd…`, `transportation/run_standard.py` `d9f4c2aa…`, `transportation/test_standard.py` `acdcd542…`).
- `SOURCE_HASHES.json` `29e8aa72…`, `housing/PACKAGE_MANIFEST.json` `5ecf44ae…`, `transportation/SOURCE_HASHES.json` `e4fe0a48…`, `LOCK_REGISTER.json` `be3388d7…`. These are unchanged since fb58ddc and must stay so.
- **Recommendation:** keep each of these files byte-identical forever. Where a file was already rewritten (RELEASE_FILE_HASHES at e45eb87 and 2734062), restore the original values **additively**, as `core_r24/RELEASE_FILE_HASHES_v1_fb58ddc.json` (a verbatim copy of the fb58ddc blob) plus `RELEASE_FILE_HASHES_HISTORY.json`, rather than by editing the current file again. **[K/C]**

### (B) New versioned v2 locks for engineering-only changes
| File | Old hash | New hash | Commit | Engineering-only justification | Class |
|---|---|---|---|---|---|
| `core_r24/reproduce_from_raw.py` | c6783be3 → 6b41f2e0 | F1_v2: `b1e3a414…` | e45eb87, then F1_v2 | Accepts the official Census `csv_pus.zip` by inner-CSV hash; F1_v2 adds pre-validation, staging and refusal of non-empty output. Same arithmetic; byte-identical outputs (VERIFIED) | B |
| `core_r24/rebuild_raw_person_caches.py` | d9a20f2e → 97d51efa | F1_v2: `7b66a0a8…` | e45eb87, then F1_v2 | Member-set validation and content-keyed checkpoints; same ingestion loop and formulas (VERIFIED, caches `9ca1e3d2…` identical) | B |
| `core_r24/tools/pums_archive.py`, `PUMS_ARCHIVE_LOCK.json`, tests | new | F1_v2: `4d1e6055…` | e45eb87, then F1_v2 | Verification tooling only | B |
| `core_r24/verify_package.py` | 1a414de8 | F1_v2 manifest diff: `4d5df332…` | proposed | Manifest selection. **But it changes the acceptance gate's default target; see §6.** | **B only with conditions, otherwise C** |
| `research/september2026_core_r2/housing/verify.py` | 25fcc7fd | 7145ea91 | 2734062 | Writes become compare-only; computation lines 1–24 unchanged; stronger checks (it now fails on any difference) | B (but it is inside a locked package; see C2) |
| `transportation/run_standard.py` | d9f4c2aa | 70a5262c | 2734062 | Same computation, refactored into a function; compare-only | B (C2) |
| `transportation/test_standard.py` | acdcd542 | 95302c98 | 2734062 | Adds assertions only | B (C2) |
| `core_r24/src/run_joint.py` | 030cb0ae | a34951b1 | 2734062 | Default path is byte-identical (VERIFIED). **However, it adds scientific parameters (food column, labels, share metric, status) used by the matched-year engine.** | **C1** |

### (C) Tests or calculations whose scientific definition changed or may have changed
- **C1: run_joint parameterization (2734062).**
  - Behavior-preserving on defaults: **VERIFIED**. Byte-identical CSVs, e45eb87 vs 2734062, same caches; national at 2734062 = `2734f11e…`.
  - The locked engine is now also the matched-year engine, through `food_column='thrifty_2024annual'`, `transport_annual=6870.67`, new labels and `audit_status`. The "locked R2.4 engine" therefore now has a second scientific use.
  - Schema: three added keys in audit.json. This is acceptable as additive, but national_R22/audit.json (`975cc72d…`) cannot be regenerated byte-identically by the new code. It never could be in practice, because input paths differ (VERIFIED: the pre-patch documented output was already `a15ee8eb…` ≠ `975cc72d…`).
  - **Kevin decides:** whether the matched-year use of the R2.4 engine needs its own spec lock, and whether the engine re-hash goes to v2 (recommended) or stays in place.
- **C2: pillar scripts inside the locked Lock_v1 packages (2734062).**
  - Computations and outputs are unchanged: **VERIFIED** (diff reading; outputs unchanged; compare-only runs pass).
  - Scientific definition unchanged: **VERIFIED** by diff (only I/O changed).
  - But the files belong to packages whose LOCK_REGISTER (`:6-7`) names external `…_Lock_v1.zip` archives. The tracked package no longer matches its manifests, and therefore no longer matches the archived lock.
  - This is the F3b design that Kevin reportedly put on HOLD/NO-GO; it is now implemented on the public branch.
  - **Kevin decides:** re-lock as `…_Lock_v2` (new manifests, keep v1) or revert the three files.
- **C3: test_standard assertions.** Strengthened, not weakened: **VERIFIED** (`git diff e45eb87 2734062 -- …/test_standard.py` shows one import line replaced and assertions added). No other existing test file had an assertion removed between fb58ddc and 2734062: **VERIFIED** (`git diff --stat fb58ddc 2734062 -- '*test*.py'` shows 498 insertions and 1 deletion, the import line).
- **C4: matched-year FMR schedule (12 HUD reevaluation areas).** **Methodology.** See §7. Kevin decides.
- **C5: publication of the matched-year figure.** STATUS and README Track E NO-GO were replaced in place, and the committed `RESEARCH_READINESS.json` (2734062) says `"publish_17_7_percent": "NO-GO"`. See REVIEW.md §R4 and the rule-6 escalation. Kevin decides.

---

## 4. ALTERNATIVES AND CONSEQUENCES

| Option | What | Frozen results | Reproducibility from official Census files | verify_package / verify_release | F1_v2 | Record preservation |
|---|---|---|---|---|---|---|
| **A. Re-lock via versioned v2** (Kevin's reported preference) | (1) Restore the original values additively: `RELEASE_FILE_HASHES_v1_fb58ddc.json` (verbatim fb58ddc blob) + `RELEASE_FILE_HASHES_HISTORY.json` (fb58ddc → e45eb87 → 2734062 → v2). (2) Leave the current `RELEASE_FILE_HASHES.json` (2734062 state, `6cd769e0…`) untouched from now on. (3) Add `core_r24/RELEASE_FILE_HASHES_v2.json` for the F1_v2 tree, **rebased on 2734062**: the Engineer's v2 (`763d698c…`) still pins `run_joint.py 030cb0ae…` and v1 `4f6825d7…` and FAILS 2/41 at 2734062 (VERIFIED, `r2734_check/vp_stack.log`). (4) Pillars: add `research/september2026_core_r2/LOCK_v2/{INTEGRITY_MANIFEST,SOURCE_HASHES,housing_PACKAGE_MANIFEST,transportation_SOURCE_HASHES}_v2.json` listing the 3 changed files, and keep the v1 manifests byte-identical. (5) Extend acceptance so it checks the v2 pillar manifests (the F3b_v2 wrapper, or a new `verify_release_v2.py`); the locked `verify_release.py` itself is not edited. (6) A Kevin-dated decision entry in ERRATA/ITERATION_REGISTER ratifying D-05, the run_joint change and the pillar changes as engineering-only. | Unchanged | Kept (the official-zip path stays) | v1 verification of the **original** release needs the original code: check out fb58ddc and run its own verify_package (documented). v2 PASS on the new tree. Pillar drift becomes detectable. | Applies after rebase of the manifest diff (hardening and test diffs apply cleanly at 2734062; VERIFIED `git apply --check`) | **Best**: nothing further rewritten; past in-place edits are documented, not undone |
| **B. Revert** scripts and hashes to fb58ddc (and the pillar scripts to Lock_v1) | New commit restoring the old file bytes and old hash lines | Unchanged | **Lost**: fb58ddc code rejects official `csv_pus.zip` (H-01 returns; VERIFIED in the baseline). Matched-year engine loses its run_joint parameters (C1), so `results/matched2024_provisional` can no longer be regenerated | v1 PASS again; F1_v2 must be redone on the old base | Must be rebuilt | A revert is itself another in-place rewrite of RELEASE_FILE_HASHES (git history keeps everything) |
| **C. Ratify in place** with a written rationale | Keep current files; add an ERRATA entry recording old → new hashes and reasons; update the pillar manifests in place | Unchanged | Kept | verify_release still blind (unless fixed); RELEASE_FILE_HASHES keeps being edited in place on every change | F1_v2 would also re-hash in place | **Weakest**: repeats the pattern Kevin's rule forbids |
| **D. Hybrid (recommended form of A)** | A for core_r24 and the pillars; **plus** treat C1 and C4 as methodology items needing separate Kevin sign-off before v2 is issued; **plus** additive restoration of the fb58ddc manifest copy | Unchanged | Kept | As A; acceptance runs v1-on-original-code and v2-on-new-tree in CI-style tests | As A | As A |
| E. Defer | Do nothing until the matched-year questions settle | Unchanged | Kept | Pillar drift remains undetected and verify_release stays green | Blocked | Drift continues |

---

## 5. RECOMMENDATION (AI methods review, not independent peer review; for Kevin's decision)
**Option D: A plus explicit methodology sign-offs.** In order:
1. **[K/C]** Freeze the originals additively:
   - `RELEASE_FILE_HASHES_v1_fb58ddc.json`, a verbatim copy of `git show fb58ddc:core_r24/RELEASE_FILE_HASHES.json`, sha256 `49871df6…`;
   - a history file covering all three in-place edits;
   - stop editing `RELEASE_FILE_HASHES.json`.
2. **[K/C]** Retire or guard `core_r24/tools/refresh_release_hashes.py`. It reads at `:5` and **writes in place** at `:23` (VERIFIED). It must refuse to write any existing manifest, or write only a new versioned file.
3. **[K/C]** Issue pillar `LOCK_v2` manifests for the three 2734062 pillar files. Make acceptance check v1 and v2 manifests, through the F3b_v2 wrapper rebased on 2734062 or a new verifier. The locked `verify_release.py` stays unedited.
4. **[K/C]** Rebase `F1_v2_manifest_v2.diff` onto 2734062, so that v2 pins `run_joint.py a34951b1…` and RELEASE_FILE_HASHES `6cd769e0…`. Make `--manifest` an allowlist (see §6).
5. **Kevin decision (methodology):**
   - C1: does the matched-year use of the R2.4 engine need its own spec lock?
   - C4: the FMR schedule.
   - C5: the publication-status contradiction.
   Do not issue v2 hashes for anything that encodes an unapproved scientific choice.

---

## 6. Does any proposed change relax a validation gate? (Kevin forbids it)
| Item | Relaxes a gate? | Evidence |
|---|---|---|
| e45eb87 housing input check (D-05) | **YES, formally.** It accepts ZIPs whose container hash differs, if the inner CSVs match (VERIFIED, `pums_archive.py:77-90` at e45eb87). Content-equivalent in intent (HYPOTHESIS H-a) | needs Kevin's ratification or revert |
| e45eb87 person input check | **YES, formally**, same mechanism, but it is what makes official-zip reproduction possible | Kevin |
| verify_package default switch to v2 (F1_v2 manifest diff `verify_package.py:9`) | **YES.** The documented acceptance command (`README.md:86` `python core_r24/verify_package.py`; STATUS/ITERATION records cite "verify_package PASS N hashes") silently changes target. Worse, `--manifest` accepts **any** path: with an empty manifest `{}` it printed `PASS: all 0 … files match` and exited 0 (VERIFIED, `f1v3_check/vp_abs.log`) | Condition: no default (explicit `--manifest` required), allowlist `{RELEASE_FILE_HASHES.json, RELEASE_FILE_HASHES_v2.json}`, refuse manifests with fewer entries than v1, and pin v2's own sha256 in an ERRATA/STATUS line **[K/C]** |
| `refresh_release_hashes.py` | **YES (latent).** It can rewrite the gate's reference in place (VERIFIED `:5,:23`) | Separate Kevin item |
| 2734062 pillar compare-only scripts | **No.** They now fail on any difference, which is stricter (VERIFIED diff) | — |
| 2734062 `test_standard.py` | **No.** Assertions were added, none removed (VERIFIED diff) | — |
| Any other test, fb58ddc..2734062 | **No** assertion removed (VERIFIED `--stat`: 1 deletion = import line) | — |
| 2734062 Track E STATUS gate lines | **YES, effectively.** `EXECUTE_NATIONAL_PERCENTAGE_THIS_ROUND: NO-GO` was replaced with "executed as labeled provisional only" without a dated decision record. The committed `RESEARCH_READINESS.json` keeps `publish_17_7_percent: NO-GO` | rule-6 escalation; Kevin |
| F1_v2 hardening | **No.** It is stricter; the 15 tests show it (VERIFIED) | — |
| F1_v2 test-lock env override `HESI_PUMS_LOCK_FOR_TESTS` (direct rebuild only) | **YES, narrowly.** With the variable set, a direct `rebuild_raw_person_caches.py` run accepted non-Census bytes and printed "SOURCE VERIFIED" (VERIFIED, `f1v2_check/neg/override.log`); the documented path ignores it | Condition: confine to tests (e.g. require `--test-lock` together with an explicit `HESI_TESTING=1`, and never print "SOURCE VERIFIED") **[K/C]** |
| F3b_v2 wrapper | **No.** Read-only; it adds detection | — |

---

## 7. Matched-year FMR schedule (C4), summary (details in REVIEW.md §R5)
- **VERIFIED from the source, my own fetch:**
  - Federal Register 89 FR 66127 (doc 2024-18002, published 2024-08-14, `federalregister.gov` full text sha256 `9eed1d3b…`), lines 42–44: "Implementation Date of Revised FMRs: October 1, 2024, unless HUD receives a valid request for reevaluation of specific area FMRs".
  - Section V(3): "Areas where valid reevaluation requests are submitted may continue to use FY 2024 FMRs … HUD will post a list … of the areas requesting reevaluations where FY 2024 FMRs remain in effect."
  - **The FR notice itself does not list the 12 areas.** The list is HUD's posted PDF.
- **VERIFIED from HUD PDFs.** My curl got HTTP 202 with an empty body (bot block), so I read the Data Scout's sealed copies: `Reevaluation-Requests-for-FY2025-Fair-Market-Rents.pdf` `da05ca00…` and `FY-2025-FMR-Areas-Without-Reevaluation-Data.pdf` `e5910b86…`. Their SHA256SUMS check gives 0 failures. Their contents:
  - "Areas Where Fiscal Year 2024 Fair Market Rents … Remain in Effect as of October 1, 2024": Becker MN, Boston-Cambridge-Quincy MA-NH, Butler AL, Crow Wing MN, Cullman AL, Kauai HI, New York NY HUD Metro, Pike AL, Portland-Vancouver-Hillsboro OR-WA, San Luis Obispo CA, Santa Maria-Santa Barbara CA, Santa Rosa CA.
  - A second notice: 7 of these began FY2025 "Effective January 13, 2025"; the other 5 kept FY2024.
- **VERIFIED in the code:** `prepare_2024_cost_inputs.py:104-108` (comment and day constants 70/204/92) applies FY2025-original to all areas from 2024-10-01. `HISTORICAL_ALIGNMENT_PROTOCOL.md:21` says the same. `git grep -i reevaluat 2734062` finds nothing, so the simplification is **undocumented**.
- **Correct schedule for calendar 2024:**
  - FY2024 original from 2024-01-01 to 2024-03-10 (all areas; caveat: FY2024's own reevaluation list was not obtained, Data Scout F-2, BLOCKED).
  - FY2024 revised from 2024-03-11 to 2024-09-30 (Honolulu revised; all others identical).
  - From 2024-10-01 to 2024-12-31: **FY2025 original everywhere except the 12 listed areas, which stay on FY2024 (revised) for all 92 days.**
- **Size:** HYPOTHESIS (+0.01 to +0.02 pp; the direction is upward, because FY2024 > FY2025 in every affected area per the Data Scout's comparison log). This is about 0.2–0.4 sampling SE (SE 0.053 pp) and far smaller than the stated model sensitivities (−0.13 to +0.44 pp). It does not change "about 17.7%". It does change the 9-significant-figure value locked at atol 1e-7.

- **Effective date of the FY2025 revised FMRs, 2025-04-27 vs 2025-04-28.**
  - VERIFIED: 90 FR 14158 (published 2025-03-28; my federalregister.gov fetch `fr/2025-05345.txt`, sha256 `b25defc3…`) line 35 says: "DATES: The revised FY 2025 FMRs are effective on April 28, 2025." The API field `effective_on` is `2025-04-28`.
  - The repo uses **2025-04-27** in four places: `ITERATION_NOTES.txt:683`, `HISTORICAL_ALIGNMENT_PROTOCOL.md:22`, `SOURCE_REGISTER.json:74` and `prepare_2024_cost_inputs.py:83`. **2025-04-28** appears nowhere in the 2734062 tree (`git grep`).
  - HUD's fmr.html (Data Scout's sealed copy, sha256 `bbfb7904…`) shows both: "[Effective April 28, 2025]" (L1023, 2025 Documents) and "[Effective April 27, 2025]" (L1055, 2025 Data).
  - **Supported date: 2025-04-28** (the Federal Register is authoritative). The 04-27 date matches HUD's data-page label.
  - Impact: metadata only. FY2025 revised is outside calendar 2024 and not in the default (PROTOCOL:22), so there is no numeric effect (VERIFIED by reading `prepare_2024_cost_inputs.py:83`, a SOURCE_REGISTER dict entry).
  - Fix: additive erratum. **[K/C]**
- **Size compared with the stated uncertainty:**
  - Stated model sensitivities (`MODEL_VS_SAMPLING_UNCERTAINTY.md:28-33`): FY2024-revised-only gives 17.54959% (−0.134 pp); FY2025-original-only gives 18.12042% (+0.436 pp); no car gives 13.05558%.
  - Sampling 90% interval: 17.5966%–17.7714%; SE 0.000531 (`EXECUTION_REPORT.json:14`).
  - The hypothesized +0.01 to +0.02 pp falls well inside both.

---

## 8. Kevin's 8 requirements vs the remediation proposed so far
Covers the F1_v2 stack (hardening + valid-input test + manifest v2), F3b_v2, the verify_package default and refresh_release_hashes.

| # | Requirement | Status | Evidence | Acceptance criteria (exact commands) |
|---|---|---|---|---|
| 1 | Original release verified consistently with its original code and manifest | **Partly met** | VERIFIED: e45eb87's own `verify_package.py` passes 38/38 at e45eb87. No procedure verifies **fb58ddc's** release with fb58ddc code, and the original fb58ddc manifest values exist only in git history | `git worktree add /tmp/v1 fb58ddc && cd /tmp/v1/core_r24 && python verify_package.py` must exit 0 with "35 … match". Repeat for e45eb87 (38). Record both logs. Committed `RELEASE_FILE_HASHES_v1_fb58ddc.json` must satisfy `cmp <(git show fb58ddc:core_r24/RELEASE_FILE_HASHES.json) core_r24/RELEASE_FILE_HASHES_v1_fb58ddc.json` |
| 2 | Changed scripts get v2 manifests; original evidence never silently rewritten | **Partly met** | VERIFIED: the F1_v2 stack leaves v1 byte-identical (`4f6825d7…` before and after). But 2734062 itself rewrote v1 in place (run_joint), the pillar manifests are not versioned, and the v2 diff is stale against 2734062 (FAIL 2/41) | After rebase: `sha256sum core_r24/RELEASE_FILE_HASHES.json` = `6cd769e02202…` (the 2734062 value) before and after applying; `python verify_package.py --manifest RELEASE_FILE_HASHES_v2.json` exit 0; pillar `LOCK_v2/*.json` exist and the v1 manifests' sha256 equal the §3(A) values; `refresh_release_hashes.py` refuses to overwrite (`python core_r24/tools/refresh_release_hashes.py; test $? -ne 0 && git diff --quiet core_r24/RELEASE_FILE_HASHES.json`) |
| 3 | Release verifier checks every applicable pillar integrity manifest | **Not met at 2734062; proposed by F3b_v2** | VERIFIED: verify_release opens no manifest; F3b_v2 checks 6 manifests and catches drift at 2734062 | `python tools/check_pillars.py` must exit 1 on 2734062 as is (drift), and exit 0 after LOCK_v2 is issued and the wrapper reads the v2 manifests. The wrapper's own files must be covered by a manifest (they sit outside core_r24, so v1/v2 do not cover them; VERIFIED). Add a root-level `TOOLS_MANIFEST.json` or include them in a pillar v2 manifest |
| 4 | Protected output paths rejected before any cache, directory or intermediate is written | **Not met** at 2734062 (caches written into national_R22 before refusal; rebuilt_from_raw unguarded; run_joint mkdir before reading). F1_v2 refuses non-empty output and stages in `.NAME.partial-PID`, but does not reject protected paths up front. The Engineer's `F6_output_guard_ON_HOLD_on2734062.diff` exists; **not reviewed here** | In scratch: `python core_r24/reproduce_from_raw.py --housing csv_hus.zip --person-official csv_pus.zip --output core_r24/results/national_R22` and the same with `results/rebuilt_from_raw` and `results/synthetic` must exit non-zero **before** `SOURCE VERIFIED`, with `find core_r24/results -newer <stamp> \| wc -l` = 0 including `git status --ignored` |
| 5 | Tests cover both v1 and v2 verification paths | **Partly met** | VERIFIED manually: v1 on patched → FAIL 4/38; v2 → PASS 41/41. No automated test asserts both | A test in `core_r24/tests/` that runs `verify_package.py --manifest RELEASE_FILE_HASHES.json` on a temp copy of the tree and expects a non-zero exit listing exactly the changed files, then expects `--manifest RELEASE_FILE_HASHES_v2.json` to exit 0, plus a negative test that `--manifest /tmp/empty.json` is refused |
| 6 | All frozen national results unchanged | **Met** | VERIFIED: national_R22 hashes unchanged at 2734062; e45eb87 final-tree and 2734062 national runs within 1e-7 (max 4.32e-11 / 9.09e-12); tolerance defined at `reproduce_from_raw.py:24,27` (`atol=1e-7, rtol=0`) and README `:95` | `python core_r24/verify_package.py --manifest RELEASE_FILE_HASHES_v2.json` exit 0 (it includes `--check-existing results/rebuilt_from_raw`); `sha256sum core_r24/results/national_R22/*` equal to v1 entries; documented national run report `status: PASS` |
| 7 | Matched-year provisional figure reproduces on the final patched code | **Not yet shown** (HYPOTHESIS). The Engineer is reproducing it; ARTIFACT_LOCK is self-consistent (VERIFIED: 14/14 listed files match). Its food-cache builder `rebuild_matched_food_cache.py:62` uses a **path-keyed** checkpoint and `:73` reads every `psam_pus*` member, so N7/N9 recur on this path (VERIFIED by reading). F1_v2 does not cover it | On the final tree: run the commands in `REPRODUCER_HANDOFF.md` into an empty directory; compare with `ARTIFACT_LOCK.json` at `metric_atol=1e-7`, `frame_exact`, 80 replicates; plus rerun with the corrected FMR schedule as a separately labeled sensitivity |
| 8 | BLS hash resolved from file evidence; dependency completeness verified | **Partly met** | BLS: VERIFIED that the committed factors file is `9349e525…`, the register still says `01eee553…`, and substituting the operator path reproduces `01eee553…`. My own BLS API fetch (2026-10-22 03:58Z) equals the reconstructed bundle `bb68500e…` except `responseTime`. 2734062 added a test of `source_sha256` but **did not fix the register** (F2 pending). Dependencies: 2734062 adds openpyxl/xlrd without upper bounds and without pytest (root unittest fails without pytest, per the Engineer's sealed step-1 log) | `sha256sum research/september2026_income_nowcast/factor_sources/BLS_ANNUAL_FACTORS.json` equals the SOURCE_REGISTER entry; in a fresh venv `pip install -r requirements.txt -r requirements-dev.txt && python -m pytest -q tests && (cd core_r24 && python -m unittest discover -s tests)` exit 0 |

---

## 9. Items only Kevin or Cursor can implement **[K/C]**
1. The choice among options A–E (recommended: D).
2. The additive v1 copy and history file.
3. The pillar LOCK_v2.
4. Rebasing manifest v2, plus the allowlist and no-default rule for `verify_package`.
5. Retiring or guarding `refresh_release_hashes.py`.
6. The F6 output guard (after review).
7. Methodology decisions C1, C4, C5.
8. F2 register fix.
9. Pytest in a dev requirements file.
10. README text (F1 item 6).

---

## ADDENDUM to C4 (FMR schedule) and §7/§8 (written 2026-10-22, about 04:55 UTC, base `273406208abe`)
> **AI methods review, not independent human peer review; recommendations for Kevin, not approvals.**
> Additive only: nothing above has been edited.
> Inputs:
> - the Engineer's sealed `findings/reproducer/2026-10-22_2734062_step4_fmr_sensitivity.md` and `…_step5_bls_deps.md`;
> - `evidence_2734062_step4/` and `evidence_2734062_step5/`;
> - the committed `results/matched2024_provisional/` at 2734062.
>
> The Engineer's runs are AI-operated reproductions on a separate machine.

### C4-A1. Checking the sealed evidence
| Item | Status | Evidence |
|---|---|---|
| Step 4 seal | **VERIFIED** | `sha256sum evidence_2734062_step4/SHA256SUMS` = `575eda0687cc5a79…`, matching the report; `sha256sum -c` gives 66 entries, 0 failures |
| Step 5 seal | **VERIFIED** | `deac0fd2fd96bc7f…`, matching the report; 62 entries, 0 failures |
| Reading A headline 0.17697484646106504 (17.6974846%) | **VERIFIED** | Recomputed by me from `run_SENS_A/calendar_2024_dayweight/common_cohort_results.csv` |
| Reading B headline 0.1769868758677428 (17.6986876%) | **VERIFIED** | Same, from `run_SENS_B_noWestchester/…` |
| Delta vs the committed 0.17683956520767094 | **VERIFIED**: A +0.013528 pp, B +0.014731 pp | My subtraction against committed `matched2024_provisional/calendar_2024_dayweight/common_cohort_results.csv` |
| Delta / SE (committed SE 0.0005312962) | **VERIFIED**: A 0.2546, B 0.2773 (= 0.25–0.28) | My arithmetic |
| All 80 replicate deltas positive | **VERIFIED**: A +1.134e-4 to +1.573e-4; B +1.247e-4 to +1.661e-4 | My pairing of replicate rows (sensitivity vs committed) |
| SDR SE of the paired delta | **VERIFIED**: A 1.671e-5, B 1.577e-5 (4/80 Σ formula) | Same; matches `logs/compare_sens.json` |
| The sensitivity runs used the stated code and schedule (138 county geos changed; baseline tables byte-equal to committed) | **HYPOTHESIS** (consistent with the sealed logs `logs/build_sensitivity.json`, but not rerun by me) | — |
| Tract inputs: the runs use AI-derived tract inputs, because the operator files are not shipped. The baseline built the same way reproduces the committed share with 0.0 diff | **HYPOTHESIS for me** (the Engineer reports VERIFIED in step 3) | — |
| **PUMA count is 102, not 103** | **VERIFIED**: `logs/puma_count_reconciliation.txt` shows Butler 01013 and Pike 01109 both map to PUMA `0102500`, so the per-area sum of 103 counts it twice | **Correction (additive):** wherever this review or the Data Scout says 103 affected PUMAs, read **102**. In reading B, 95 PUMAs change (Westchester's 7 PUMAs are excluded) |
| Correction to §7 "FY2024 > FY2025 in every affected area" | **VERIFIED wrong for Westchester.** `logs/build_sensitivity.json`: the NY HMFA geos had FY24 2BR $2,752 or $2,352 (Westchester Statutory Exception Area), vs FY25 $2,580. So for Westchester, FY24 < FY25 | The net direction is still upward under both readings (VERIFIED above) |

### C4-A2. Westchester: reading A or B?
- **VERIFIED from the FY2025 notice itself** (my fetch, `fr/2024-18002.txt` L180-184): "Pursuant to section 107(a) of HOTMA … for FY 2025, HUD is adding Westchester County, NY to the New York, NY HUD Metropolitan Fair Market Rent Area."
  - So in FY2024 Westchester was its own "Westchester County, NY Statutory Exception Area" (2BR $2,352). In FY2025 it is inside the NY HMFA (2BR $2,580).
- **VERIFIED, 89 FR 66132–66133 §V.A(1),(3):**
  - "(1) … The area's PHA or, in multi-jurisdictional areas, PHA(s) representing at least half of the voucher tenants in the FMR area, must agree that the reevaluation is necessary."
  - "(3) Areas where valid reevaluation requests are submitted may continue to use FY 2024 FMRs, or may use the FY 2025 FMRs. Commenters should indicate whether they wish to maintain the FY 2024 or implement the FY 2025 FMR during the revaluation period … HUD will post a list … of the areas requesting reevaluations where FY 2024 FMRs remain in effect."
- **VERIFIED, HUD list (sealed PDF `da05ca00…`):** it names "New York, NY HUD Metro FMR Area" under "Fiscal Year 2024 Fair Market Rents … Remain in Effect as of October 1, 2024". **It does not mention Westchester.**
- **Not obtainable today:** HUD's FY2025 FMR documentation page for Westchester (`fmrs/FY2025_code/2025summary.odn?fips=3611999999…`), and HUD's FMR pages generally.
  - My curl got **HTTP 202 with 0 bytes** (bot block). I did not work around it.
  - That page, or a HUD PIH notice or letter to the Westchester PHAs, is the document that would settle the question.
- **Conclusion:**
  - The sources **cannot settle it** (HYPOTHESIS either way).
  - The request was filed against the FY2025 area, which includes Westchester. "FY 2024 FMRs remain in effect" for that area is ambiguous for a county whose FY2024 FMR came from a *different* FY2024 area.
  - **Reading A** (Westchester keeps its own FY2024 SEA FMR) is the literal "prior FMR for this geography" reading.
  - **Reading B** (Westchester follows FY2025, since it was not part of the FY2024 NY area) is the area-membership reading.
  - §V.A(3)'s "may continue … or may use" also means the operative FMR depended on what the requestor elected. The HUD list records that election only at the area level.
- **Recommendation (AI review):** report **both readings as a range, +0.0135 to +0.0147 pp**. If one value must be used, use **reading A (+0.0135 pp)**: it is the smaller departure from the published record, and the conservative choice for an erratum. Both readings give the same rounded result, about 17.7%.

### C4-A3. FMR treatment: recommendation (AI recommendation, not independent peer review; Kevin decides; [K/C] implements)
1. Keep `results/matched2024_provisional/` and its `ARTIFACT_LOCK.json` byte-identical, as the record.
2. Now: add an **additive erratum** (text below) to `ERRATA.txt`, with a pointer from `MODEL_VS_SAMPLING_UNCERTAINTY.md` added as a new line, not a rewrite of existing lines. Same erratum: effective date of FY2025 revised = **2025-04-28** (90 FR 14158), not 2025-04-27; metadata only.
3. Before the figure leaves PROVISIONAL: a **versioned corrected rerun** in a new directory (e.g. `results/matched2024_provisional_v2_reeval/`) with its own lock. It needs:
   - a protocol amendment (new dated section in `HISTORICAL_ALIGNMENT_PROTOCOL.md`) stating the reevaluation-area rule and the Westchester choice;
   - Kevin's dated decision.
4. Do this only once the tract-input L13 gap is closed (operator tract files, or committed builders with public URLs). Otherwise the corrected rerun is not externally reproducible either.
5. Until then, report "about 17.7%" and not the 9-significant-figure value.

### C4-A4. Draft erratum (ready to paste; for Kevin's approval; not applied)
```
E13 (2026-10-22). Matched-year 2024 PROVISIONAL figure: FMR schedule discrepancy for HUD reevaluation areas.
Discrepancy: The calendar_2024_dayweight housing schedule applies FY2025 original FMRs to every area from
2024-10-01 (HISTORICAL_ALIGNMENT_PROTOCOL.md lines 19-22; prepare_2024_cost_inputs.py lines 104-108). Under
89 FR 66127, Section V.A(3), and HUD's posted list "Reevaluation Requests for FY2025 Fair Market Rents",
FY2024 FMRs remained in effect on 2024-10-01 in 12 areas: Becker County MN; Boston-Cambridge-Quincy MA-NH HUD
Metro FMR Area; Butler County AL; Crow Wing County MN; Cullman County AL; Kauai County HI; New York NY HUD
Metro FMR Area; Pike County AL; Portland-Vancouver-Hillsboro OR-WA MSA; San Luis Obispo-Paso Robles-Arroyo
Grande CA MSA; Santa Maria-Santa Barbara CA MSA; Santa Rosa CA MSA. Seven of these switched to FY2025 on
2025-01-13 and the other five kept FY2024 until the revised FY2025 FMRs (90 FR 14158, effective 2025-04-28),
so FY2024 FMRs applied in all 12 areas for 2024-10-01 to 2024-12-31.
Schedule that matches the FMRs in effect: 2024-01-01 to 2024-03-10 FY2024 original; 2024-03-11 to 2024-09-30
FY2024 revised; 2024-10-01 to 2024-12-31 FY2025 original, except FY2024 in the 12 areas above. Westchester
County NY (added to the New York HMFA in FY2025) is ambiguous in the HUD sources; both treatments are shown.
Sensitivity (scratch computational run, not a corrected estimate): applying FY2024 FMRs in the 12 areas for
Q4 2024 raises the modeled share from 0.176840 to 0.176975 (Westchester at its FY2024 FMR) or 0.176987
(Westchester at FY2025), i.e. +0.0135 to +0.0147 percentage points, which is 0.25 to 0.28 of one sampling
standard error (0.053 pp) and inside the published 90% sampling interval (17.60% to 17.77%). The shift is
positive in all 80 replicate weights. 102 of 2,350 complete PUMAs are affected. Under this schedule the
published figure therefore understates the modeled share by about 0.014 percentage points.
Record: the published 17.6839565% and all files in results/matched2024_provisional/ are kept unchanged as
the record and remain PROVISIONAL. A versioned corrected rerun, with its own lock and a dated protocol
amendment, is planned before the figure leaves PROVISIONAL. Report this figure as about 17.7%.
Also corrected: the FY2025 revised FMR effective date is 2025-04-28 (90 FR 14158), not 2025-04-27 as written
in HISTORICAL_ALIGNMENT_PROTOCOL.md line 22, SOURCE_REGISTER.json line 74, prepare_2024_cost_inputs.py line 83
and ITERATION_NOTES.txt line 683. This date is outside calendar 2024 and does not affect any result.
```
- The draft has no "validated", "measured" or "independent" wording (checked by reading).
- "Scratch computational run" describes the Engineer's run accurately.

### C4-A5. BLS register hash (F2 scope; requirement 8)
- **VERIFIED:** `git grep -n 01eee553 273406208abe` gives exactly 3 citations:

| # | File | Line | Field |
|---|---|---|---|
| 1 | `research/september2026_income_nowcast/SOURCE_REGISTER.json` | 6 | `"BLS_ANNUAL_FACTORS.json": "01eee553…"` |
| 2 | `research/september2026_income_nowcast/reports/INCOME_NOWCAST_VALIDATION_REPORT.json` | 1702 | `"factor_file_sha256"` |
| 3 | `research/september2026_income_nowcast/reports/PHASE3_DATA_SOURCE_ACQUISITION_REPORT.json` | 36 | `"sha256"` |

- **VERIFIED:** the committed factors file is `9349e525…`.
  - Substituting `$HESI_OPERATOR_HOME` → `/Users/kevinmannion` reproduces `01eee553…`. The Engineer's step 5 shows this, and it matches my earlier F2 check.
  - The Engineer reports that no blob in the history (284 blobs) hashes to `01eee553`. HYPOTHESIS for me: I did not re-hash the history.
- **Hash-locked? VERIFIED none of the 3 is.** Their sha256 values are `17970bac…`, `c3f5cc4d…` and `d8ed169a…`. `git grep` of each hash at 2734062 finds no manifest, and no test pins them. (`tests/test_engineering_stabilization.py:25-27` reads only `GO_NOGO.json`.)
  - But files 2 and 3 are **historical evidence reports** (the nowcast validation run that produced the NO-GO, and the data-acquisition report). Under the record-preservation rule they must not be rewritten.
- **Recommendation (AI review):** F2 should **cover all 3 by a single additive ERRATA entry** stating that `01eee553…` is the pre-substitution hash and that the committed file is `9349e525…`.
  - Edit only `SOURCE_REGISTER.json`, the live register, and keep the old value visible, e.g. by adding a `"BLS_ANNUAL_FACTORS.json_pre_path_substitution_sha256": "01eee553…"` field beside the corrected one. Alternatively, leave it unedited and add a superseding register file.
  - **Do not edit the two reports.**
  - Optionally add a test that checks the register against the file bytes. **[K/C]**

### C4-A6. Dependencies (requirement 8)
- **Pytest is the only missing third-party dependency.** HYPOTHESIS for me: the Engineer's sealed step 5 (AST scan of 68 files and a fresh-venv run of 20 test files) shows it, and the seal checks out, but I did not rerun it.
- Without pytest, `tests/test_synthetic_pipeline.py` errors and `tests/test_hesi.py` collects 0 tests.
- When pytest is added to a dev requirements file (the Engineer's `F4_requirements_dev_pytest_on2734062.diff` proposes `requirements-dev.txt`), the **dependency half of requirement 8 is met**, subject to:
  - `pip install -r requirements.txt -r requirements-dev.txt && python -m pytest -q tests` exit 0 in a fresh venv.
- The **BLS half** stays open until the C4-A5 erratum lands.
- Requirement 8 status therefore stays **partly met**, with a clear path. **[K/C]**

### C4-A7. Rule-6 status after this addendum
- **No new rule-6 item.** The FMR discrepancy now has a verified size: small against sampling error, beyond the lock tolerance. It is a disclosure and methodology item for Kevin, already escalated as C4.
- The earlier escalations are unchanged:
  - matched-year NO-GO overridden without a dated decision (C5);
  - pillar-lock drift;
  - in-place hash replacements.

### C4-A8 (2026-10-22, about 06:00 UTC): Decision 2 supersedes the forward-looking parts of C4-A3/C4-A4
> **AI methods review, not independent human peer review.** Additive note; C4-A3 and C4-A4 are kept as written.
- The decisions file `/workspace/hesi-team/decisions/2026-10-22_formal_governance_decisions.md` (sha256 `090a6306…28f8`, VERIFIED), recorded by the Coordinator as Kevin's decisions, says:
  - "2024 HUD FMR schedule: NOT APPROVED yet"
  - "Do not change the accepted scientific definition or replace the current provisional calculation without separate review."
- Therefore:
  - the C4-A4 erratum sentence "A versioned corrected rerun … is planned" and C4-A3 step 3 are **not authorized plans**. A rerun would need a separate review first.
  - The "correct schedule" wording in C4-A4 and §7 should be read as "the schedule matching the FMRs HUD lists as in effect". It is **not** an approved schedule.
- The neutral record of original vs alternative outcomes is in `proposals/2026-10-22_remediation/FMR_OUTCOMES.md`, with a placeholder for the Data Scout's pending effective-date findings.
- Numbering note: "C4-A5" in this memo is already the BLS section (above). The FMR record is therefore C4-A8 plus FMR_OUTCOMES.md.
- Erratum numbering: E12 (F2), E13 (FMR draft) and E-TE1 (Track E draft) are all unapplied placeholders. Cursor assigns final numbers at apply time.

### C4-A9 (2026-10-22, about 06:30 UTC): Westchester correction (additive; C4-A1…A4 not rewritten)
> **AI methods review, not independent human peer review.**
- **VERIFIED** from the Engineer's sealed step-4 scripts and built county tables (details in `FMR_OUTCOMES.md` §4.3):
  - Reading A uses Westchester's own FY24 SEA FMR ($2,352) for Q4. **A = the Data Scout's W1.**
  - Reading B leaves Westchester at **FY2025 original ($2,580)** for Q4. B is **not** the Data Scout's W2 (NY HMFA FY24, $2,752).
  - **The W2 sensitivity has not been run.**
- **Corrections:**
  - **C4-A1**, row "Correction to §7": the FY24 < FY25 statement holds for Westchester under W1. Under W2, Westchester's Q4 rent (the NY HMFA FY24 value, $2,752) would be above FY25 original ($2,580).
  - **C4-A2:** "Reading B … is the area-membership reading" is **wrong**. The area-membership reading is W2, which is untested. Reading B corresponds to Westchester not being postponed at all, which contradicts the Data Scout's VERIFIED point that it was postponed with New York.
  - **C4-A2 recommendation:** "report both readings as a range, +0.0135 to +0.0147 pp". That range **does not bound W2**. W2 is expected above +0.0147 pp, about +0.0156 pp by linear extrapolation (HYPOTHESIS). Until a W2 run exists, any range is incomplete.
  - **C4-A4 erratum draft:** "both treatments are shown" and "+0.0135 to +0.0147 percentage points" are **incomplete**. If the erratum is ever used, it must either include a W2 result or say that the W2 treatment was not computed. Per C4-A8 and Decision 2, the erratum's rerun sentence is not an authorized plan.
- The Engineer's schedule otherwise matches the verified calendar-2024 dates:
  - day weights 70/204/92;
  - FY24 revised from 2024-03-11;
  - FY24 in all 12 areas for Q4;
  - FY25 original elsewhere from 2024-10-01;
  - the 2025 switch dates are irrelevant to 2024.
- Open items:
  - the Honolulu FY23 hold for Jan–Mar 2024 (BLOCKED in sources; the Engineer used FY24 original);
  - W2.

### C4-A10 (2026-10-22, about 06:45 UTC): C-W2 landed (additive; earlier C4 text not rewritten)
> **AI methods review, not independent human peer review.**
- The C-family sensitivity range now spans **+0.0135 to +0.0157 pp** across readings A (C-W1, +0.013528), B (W0, +0.014731) and **C-W2 (+0.015711)**, i.e. 0.25–0.30 SE.
  - All three have 80/80 replicate deltas positive.
  - VERIFIED from sealed evidence `evidence_2734062_step4_w2/` (SHA256SUMS `117a1ba6…`, 40 files OK) and step 4; details in `FMR_OUTCOMES.md` §6.
- Ordering: O < A < B < C-W2.
- This replaces, for reporting purposes, the incomplete range "+0.0135 to +0.0147" in C4-A2/C4-A4 (see C4-A9). It does not replace any published figure.
- The FMR schedule is not approved, and Westchester remains BLOCKED pending HUD.
