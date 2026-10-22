# ACCEPTANCE TESTS: Decision 2 (run_joint) and Decision 3 (D-05), base 273406208abe
> **AI methods review, not independent human peer review; this is a test specification for Kevin, not an approval.**
> Author: Methods Reviewer (Grok Bot). Written 2026-10-22, about 05:40 UTC.
> - Base: `273406208abe439cbad960567f32822b870c43b5` (Core R2.5).
> - Source of the conditions: `/workspace/hesi-team/decisions/2026-10-22_formal_governance_decisions.md`. Its sha256 is `090a630665aeba727dc3002c95d2607bff8da3849123e2079c976350016828f8` (VERIFIED with `sha256sum`). This equals the value in its companion `.sha256` file (`sha256sum -c` → OK; VERIFIED). The file is read-only (mode `-r--r--r--`; VERIFIED).
> - The decisions in it are **recorded by the Coordinator as Kevin's decisions**. I have not confirmed them with Kevin.
> - Labels: **VERIFIED** (I ran or read it; cited) or **HYPOTHESIS**. **TO BE WRITTEN** = a planned test that does not exist yet. **[K/C]** = only Kevin or Cursor can implement it.
> - Charter: nothing here was applied to the repo. All test files are planned for the final patched tree that Cursor will produce.

## 0. Conditions, quoted exactly from the decisions file
**Decision 2, run_joint:**
- "run_joint.py reuse as an implementation component: CONDITIONAL APPROVAL, provided that historical and current cost vintages are isolated, input selections are explicit, and regression tests establish no cross-contamination."
- "2024 HUD FMR schedule: NOT APPROVED yet."
- "Do not change the accepted scientific definition or replace the current provisional calculation without separate review."

| ID | Condition |
|---|---|
| D2-a | historical and current cost vintages are isolated |
| D2-b | input selections are explicit |
| D2-c | regression tests establish no cross-contamination |
| D2-d | no change to the accepted scientific definition / no replacement of the provisional calculation without separate review |

**Decision 3, D-05:** "FORMALLY APPROVED IN PRINCIPLE: preserve the original release manifests and create new versioned v2 manifests for modified scripts." Mandatory conditions, verbatim:

| ID | Condition |
|---|---|
| C1 | "Historical manifests and prior release evidence remain immutable." |
| C2 | "Verification against a missing, empty or mismatched applicable manifest must FAIL." |
| C3 | "No direct-run bypass of scientific locks." |
| C4 | "No unreviewed in-place hash replacement." |
| C5 | "Protected outputs are rejected before creating caches or intermediates." |
| C6 | "All applicable pillar and core manifests are checked." |
| C7 | "The original and v2 verification paths are explicitly distinguished." |
| C8 | "The final patched code reproduces the frozen R2.4 calculation and all 80 replicates." |
| C9 | "The 2024 matched-year calculation is independently reproduced and its FMR sensitivity investigated." |

The file lists exactly 9 conditions (VERIFIED).

## 1. Common setup (all tests)
```bash
REPO=<path to Cursor's patched working tree>     # final patched code; never the frozen record itself
FINAL=$(git -C "$REPO" rev-parse HEAD)
T=$(mktemp -d); git -C "$REPO" archive "$FINAL" | tar -x -C "$T"     # disposable test copy (S-COPY)
V1=$(mktemp -d); git -C "$REPO" archive fb58ddc | tar -x -C "$V1"   # original release (S-V1)
E1=$(mktemp -d); git -C "$REPO" archive e45eb87 | tar -x -C "$E1"   # first rewritten release (S-E1)
CENSUS=<dir holding csv_pus.zip and csv_hus.zip>                    # official Census 2024 1-year PUMS, hashes per core_r24/PUMS_ARCHIVE_LOCK.json
snap() { (cd "$1" && find . -path ./.git -prune -o -print0 | sort -z | xargs -0 stat -c '%n %s %Y' ; \
          find . -path ./.git -prune -o -type f -print0 | sort -z | xargs -0 sha256sum) > "$2"; }   # S-SNAP
```
- **S-DIGEST [K/C], TO BE WRITTEN:** add `tests/acceptance/REFERENCE_DIGESTS.py`, holding constants copied from D-05_DECISION.md §3(A) and pinned in source code (not read from a writable JSON):

| File | Commit | SHA-256 (VERIFIED by `git show <c>:<f> \| sha256sum`) |
|---|---|---|
| `core_r24/RELEASE_FILE_HASHES.json` | fb58ddc | `49871df6d998cbc1dbfd71c14bb84631474de1a7ef1cddf4db6ecc21739d2e96` |
| same | e45eb87 | `4f6825d7678f5b304ba9ba9652a3ffd363cdd9b67f2bde6a14778fdeadaa84e8` |
| same | 2734062 | `6cd769e022023437d360a25c333a3062c7dde9f7a5ef946165e7ba37376862f4` |
| `research/september2026_core_r2/INTEGRITY_MANIFEST.json` | fb58ddc = 2734062 | `a0de55896313e4fa53a75ec775e4e6c7c8482765852daea4bad3e19305bf9908` |
| `…/SOURCE_HASHES.json` | same | `29e8aa72e1d973c8243b22fc57ec8fd9751d54ad3d13e8f88fece8e1ebfb03f5` |
| `…/housing/PACKAGE_MANIFEST.json` | same | `5ecf44ae52c364dc0ed73808c5b4f7006aa248b72b985ab9eb98eac730f1d4d6` |
| `…/transportation/SOURCE_HASHES.json` | same | `e4fe0a480661642cc6e7224c90a3a6d318c5863e6e097a2deee43a1bdbc7a45a` |
| `…/LOCK_REGISTER.json` | same | `be3388d7596d564cd9d383908bc391655332215cd80f7450c188d256d70d148b` |
| `…/matched2024_provisional/ARTIFACT_LOCK.json` and its 14 listed files | 2734062 | as committed |

  Plus the v2 manifest digests, filled in once, **after** Kevin approves v2.
- **Runner:** `python -m pytest -q tests/acceptance -rA` (TO BE WRITTEN). It requires `pytest` from `requirements-dev.txt` (Engineer's F4 diff).
- **Expected-outcome column:** "must FAIL" means the *system under test* must exit non-zero or refuse. The pytest test itself then **passes**.

## 2. Negative tests (system must FAIL or refuse)
| ID | Command / pytest node (TO BE WRITTEN unless stated) | Fixture | Expected | Covers |
|---|---|---|---|---|
| N-01 | `tests/acceptance/test_manifest_paths.py::test_missing_manifest_fails[v1]`: `rm $T/core_r24/RELEASE_FILE_HASHES.json; python $T/core_r24/verify_package.py --manifest RELEASE_FILE_HASHES.json` | S-COPY | exit≠0, message names the missing manifest; no "PASS" in stdout | C2, C7 |
| N-02 | `…::test_missing_manifest_fails[v2]`, same with `RELEASE_FILE_HASHES_v2.json` | S-COPY | exit≠0 | C2, C7 |
| N-03 | `…::test_empty_manifest_fails[v1-zero_bytes]` and `[v1-empty_object]`: truncate to 0 bytes; or write `{}` | S-COPY | exit≠0 | C2 |
| N-04 | `…::test_empty_manifest_fails[v2-zero_bytes]` and `[v2-empty_object]` | S-COPY | exit≠0 | C2 |
| N-05 | `…::test_partial_manifest_fails[v1]`: delete one entry (e.g. `src/run_joint.py`) from the JSON | S-COPY | exit≠0 (requires completeness against S-DIGEST or a pinned entry list; a partial manifest otherwise "verifies" fewer files) | C2, C6 |
| N-06 | `…::test_partial_manifest_fails[v2]` | S-COPY | exit≠0 | C2, C6 |
| N-07 | `…::test_mismatched_manifest_fails[v1]`: flip one hex char of one entry | S-COPY | exit≠0, names file | C2 |
| N-08 | `…::test_mismatched_manifest_fails[v2]` | S-COPY | exit≠0 | C2 |
| N-09 | `…::test_manifest_flag_rejects_empty_external_file`: `echo '{}' > /tmp/empty.json; python $T/core_r24/verify_package.py --manifest /tmp/empty.json` | S-COPY | exit≠0 ("manifest not in allowlist"). **Currently PASSes with 0 files on the F1_v2 manifest diff** (VERIFIED, `scratch/methods-reviewer/f1v3_check/vp_abs.log`), so this test fails today | C2, C7 |
| N-10 | `…::test_manifest_flag_rejects_copy_outside_repo`: `cp RELEASE_FILE_HASHES_v2.json /tmp/x.json; --manifest /tmp/x.json` | S-COPY | exit≠0 | C2, C7 |
| N-11 | `…::test_no_flag_behaviour`: `python $T/core_r24/verify_package.py` with no flag | S-COPY | Depends on a **Kevin decision** (ruling 1): either exit≠0 ("explicit --manifest required"), or verify v1 and print `MANIFEST v1 (RELEASE_FILE_HASHES.json sha256 …)`. Must **not** silently select v2 | C7 |
| N-12 | `core_r24/tests/test_pums_ingestion_r1v2.py::DirectRebuildValidatesHashesFirst::test_pinned_repo_lock_used_without_override` (exists in the F1_v2 diff) plus new `tests/acceptance/test_direct_run_locks.py::test_rebuild_env_override_refused`: `HESI_PUMS_LOCK_FOR_TESTS=/tmp/fake_lock.json python $T/core_r24/rebuild_raw_person_caches.py <fake zip> --out $T/o` | fake ZIP + fake lock (as in `scratch/methods-reviewer/f1v2_check/neg/`) | exit≠0; `$T/o` does not exist; stdout has no "SOURCE VERIFIED". **Currently accepts the fake input** (VERIFIED, `f1v2_check/neg/override.log`) | C3 |
| N-13 | `test_direct_run_locks.py::test_rebuild_rejects_edited_lock`: edit one inner hash in `$T/core_r24/PUMS_ARCHIVE_LOCK.json`, then run rebuild on genuine Census ZIPs | S-COPY + CENSUS | exit≠0 before any output (lock self-hash check) | C3 |
| N-14 | `test_direct_run_locks.py::test_reproduce_ignores_env_override` | as N-12 | exit≠0 on the fake bytes | C3 |
| N-15 | `test_direct_run_locks.py::test_run_joint_direct_rejects_unlocked_inputs`: `python $T/core_r24/src/run_joint.py` (and `run_matched.py`) with a housing ZIP whose inner CSV hash ≠ lock | S-COPY + synthetic ZIP | exit≠0 before `out.mkdir`. **Today, run_joint does no input verification and runs `out.mkdir` at `:31`** (VERIFIED by reading) | C3, C5 |
| N-16 | `test_direct_run_locks.py::test_matched_food_cache_rejects_duplicate_and_extra_members`: `python $T/research/historical_matched_baseline/src/rebuild_matched_food_cache.py` with a ZIP holding a duplicate `psam_pusa.csv` and an extra `psam_pusz.csv` | crafted ZIPs | exit≠0; output dir absent. **Today `:73` reads every `psam_pus*` member** (VERIFIED by reading) | C3, C5 |
| N-17 | `test_direct_run_locks.py::test_matched_food_cache_checkpoint_keyed_by_content`: rerun with prices ×2 into the same checkpoint dir | crafted prices | food = 2× baseline for every person (recomputed). **Today the checkpoint is path-keyed at `:62`** (VERIFIED by reading) | C3, D2-c |
| N-18 | `test_direct_run_locks.py::test_inventory_of_runnable_scripts`: every `.py` with `__main__` (29 at 2734062; VERIFIED by `git grep -l __main__`) is either (a) lock-verifying, with a test in this file, or (b) listed in `tests/acceptance/NON_SCIENTIFIC_TOOLS.txt` with a reason, reviewed by Kevin | S-COPY | the test fails if a script is unclassified | C3 |
| N-19 | `test_manifest_immutability.py::test_release_hashes_digest[…]`: compare sha256 of `core_r24/RELEASE_FILE_HASHES.json` with S-DIGEST 2734062 (`6cd769e0…`) and of `RELEASE_FILE_HASHES_v1_fb58ddc.json` with `49871df6…`. Fault injection: replace one hash value in the temp copy | S-COPY | the clean copy matches; the injected copy is detected → exit≠0 | C1, C4 |
| N-20 | `test_manifest_immutability.py::test_pillar_manifest_digest[INTEGRITY_MANIFEST,SOURCE_HASHES,housing_PACKAGE_MANIFEST,transportation_SOURCE_HASHES,LOCK_REGISTER]`, with an injected one-value replacement in each | S-COPY | detected → exit≠0 | C1, C4, C6 |
| N-21 | `test_manifest_immutability.py::test_consistent_forgery_detected`: change `src/run_joint.py` **and** its hash in RELEASE_FILE_HASHES.json so they agree | S-COPY | exit≠0 (digest pin catches it) | C4 |
| N-22 | `test_manifest_immutability.py::test_refresh_release_hashes_refuses`: `python $T/core_r24/tools/refresh_release_hashes.py` | S-COPY | exit≠0; `sha256sum` of `RELEASE_FILE_HASHES.json` and `_v2.json` unchanged. **Today it rewrites the file in place** (VERIFIED: `:5` reads, `:23` writes) | C1, C4 |
| N-23 | `test_protected_outputs.py::test_refused_before_any_write[entry, target]`. Entry points: `reproduce_from_raw.py --output`, `rebuild_raw_person_caches.py --out`, `src/run_joint.py out`, `run_matched.py --out`, `run_matched_national.py`, `rebuild_matched_food_cache.py`, `prepare_2024_cost_inputs.py --out`. Targets: `core_r24/results/national_R22`, `core_r24/results/rebuilt_from_raw`, `core_r24/results/synthetic`, `research/historical_matched_baseline/results/matched2024_provisional`, repo root (`results.csv`, `audit.json`, `manifest.json`), plus a subdirectory of each and a symlink to each. Procedure: `snap $T before; <cmd>; snap $T after; diff before after` | S-COPY + CENSUS (or synthetic) | every cmd exits≠0 **and** the snapshot diff is empty, including ignored and new files. **Today caches land in national_R22 before run_joint refuses, and rebuilt_from_raw is unguarded** (VERIFIED, D-05_DECISION §1.4) | C5 |
| N-24 | `test_pillar_verification.py::test_drift_detected_by_release_verifier`: append `# x` to `$T/research/september2026_core_r2/housing/verify.py`; run the **documented release verifier** (Kevin chooses: `python tools/check_pillars.py` or a new `verify_release_v2.py`; the locked `verify_release.py` is not edited) | S-COPY | exit≠0, names the file and manifest | C6 |
| N-25 | `test_pillar_verification.py::test_2734062_drift_without_lock_v2`: run the verifier on an unmodified 2734062 tree, with no LOCK_v2 | `git archive 2734062` | exit≠0 with 4 manifest mismatches (VERIFIED today with the F3b_v2 wrapper, `r2734_check/cp_stack.out`) | C6 |
| N-26 | `test_pillar_verification.py::test_legacy_verify_release_is_not_the_acceptance_gate`: on N-24's drifted copy, `python research/september2026_core_r2/verify_release.py` exits 0 (VERIFIED today: it opens no manifest). The test asserts the README/STATUS acceptance text names the new verifier, not this one | S-COPY | documentation check passes; legacy blindness recorded | C6, C7 |
| N-27 | `test_vintage_isolation.py::test_matched_engine_rejects_2026_geography`: `python run_matched.py --geography core_r24/inputs/puma_fmr_screened.csv …` (FY2026 rents with 2024 food and transport), without an explicit cross-vintage flag | synthetic fixture (see S-VINT) | exit≠0 before `out.mkdir`. **Today it is accepted silently: `run_matched.py:35-48` takes any `--geography`, and the FY2026 and 2024 PUMA tables share an identical header with no vintage field** (VERIFIED, header of both files) | D2-a, D2-b |
| N-28 | `test_vintage_isolation.py::test_run_joint_rejects_mixed_food_rent_vintage[food2026_rent2024, food2024_rent2026, transport2026_food2024]` | S-VINT | exit≠0, unless the caller passes the explicit selection | D2-a, D2-b |
| N-29 | `test_vintage_isolation.py::test_run_joint_requires_explicit_selection`: call `run()` without vintage arguments | S-VINT | either refuses, or the defaults resolve to the documented Track B selection and are written to `audit.json` (`food_column`, `transport_annual`, `geography_sha256`, `cost_vintage`). **Kevin decides which** | D2-b |
| N-30 | `test_tracked_writes.py::test_default_runs_leave_git_clean[script]`: for every `__main__` script runnable with defaults or with only temp-dir args (existing coverage: `tests/test_engineering_stabilization.py::TrackedFileWrites::*`, 3 tests; VERIFIED they exist at 2734062), run in a git checkout copy, then `git status --porcelain --ignored` | `git worktree add $W $FINAL` | empty diff | C1, C5 |
| N-31 | `test_manifest_paths.py::test_v1_code_on_v2_tree_reports_v1`: run fb58ddc's own `verify_package.py` on the final tree | S-V1 code + S-COPY | exit≠0 listing exactly the changed files (proves the paths are distinct) | C7 |

**S-VINT (TO BE WRITTEN) [K/C]:**
- a 3-household synthetic housing ZIP plus food and composition caches with both `thrifty_2026sep` and `thrifty_2024annual` columns;
- two 1-PUMA geography tables carrying a declared `cost_vintage` (sidecar JSON, or a column added in a **new** versioned file; the locked `inputs/puma_fmr_screened.csv` must not be edited).

## 3. Positive tests (system must PASS)
| ID | Command / node | Fixture | Expected | Covers |
|---|---|---|---|---|
| P-01 | `python $T/core_r24/reproduce_from_raw.py --housing $CENSUS/csv_hus.zip --person-official $CENSUS/csv_pus.zip --output $(mktemp -d)/r24` | S-COPY + CENSUS, fresh venv (P-06) | `REPRODUCTION_VERDICT.json` `status: PASS`, `metrics_compared: 6`, `replicates_compared: 80`, `frame_exact: true`. Tolerance `atol=1e-7, rtol=0` on mean, se_sdr, ci90_low and ci90_high for all 6 metrics (`reproduce_from_raw.py:24`), and on every replicate column (`:27`); documented at `README.md:95`. Audit frame equal (`:29`) (VERIFIED lines at 2734062) | C8 |
| P-02 | `tests/acceptance/test_frozen.py::test_frozen_files_unchanged` | S-DIGEST | sha256 of every file in `core_r24/results/national_R22/` (incl. `common_cohort_results.csv` `6778c312…`), `rebuilt_from_raw/`, `matched2024_provisional/` (ARTIFACT_LOCK 14/14) and the root `results.csv`/`audit.json`/`manifest.json` equal the 2734062 values | C1, C8 |
| P-03 | `cd $V1/core_r24 && python verify_package.py` (original code, original manifest) | S-V1 | exit 0, "35" files match. Repeat on `$E1` → 38 | C1, C7 |
| P-04 | `cd $T/core_r24 && python verify_package.py --manifest RELEASE_FILE_HASHES_v2.json` | S-COPY | exit 0; output prints the manifest name and its sha256, which equals S-DIGEST v2 | C7 |
| P-05 | `python $T/tools/check_pillars.py` (or the Kevin-chosen verifier) after LOCK_v2 is issued | S-COPY | exit 0; v1 pillar manifests byte-identical to S-DIGEST; `tracked_unchanged: true` | C6, C1 |
| P-06 | `uv venv -p 3.12 $VENV && $VENV/bin/pip install -r $T/requirements.txt -r $T/requirements-dev.txt && $VENV/bin/pip check && (cd $T && $VENV/bin/python -m pytest -q tests && $VENV/bin/python -m unittest discover -s core_r24/tests && $VENV/bin/python -m unittest discover -s research/historical_matched_baseline/tests)` | fresh venv | all exit 0. Python 3.12; numpy<2 cannot install on 3.13 (Engineer's step 3; HYPOTHESIS for me) | Requirement 8 / dependencies |
| P-07 | `core_r24/tests/test_pums_valid_input_preservation.py` (F1_v2 diff) plus full-data check: caches `acs2024_food_person_aggregates.pkl` = `9ca1e3d2…`, `acs2024_person_composition.pkl` = `4e7c8dbb…` | CENSUS | equal (VERIFIED on the F1_v2 stack at e45eb87, `f1v3_check/run_final.log`) | C8 |
| P-08 | Matched-year reproduction: the commands in `research/historical_matched_baseline/results/matched2024_provisional/REPRODUCER_HANDOFF.md`, run in an empty dir, then compared with `ARTIFACT_LOCK.json` `acceptance`: `metric_atol 1e-7`, `frame_exact`, `n_sdr_replicates 80`, SDR formula as stated | S-COPY + CENSUS + the operator tract files or approved public builders | all metrics within 1e-7; 80/80 replicates; frame equal | C9 (computational part only; see §5) |
| P-09 | `test_vintage_isolation.py::test_explicit_selection_recorded`: Track B run and matched run each write `audit.json` with `cost_vintage`, `food_column`, `transport_annual`, `geography_sha256`, `prices_sha256` | S-VINT | the keys are present and the values are the selected ones | D2-b |
| P-10 | `test_vintage_isolation.py::test_no_cross_contamination`: in one workspace and one checkpoint root, run Track B, then matched, then Track B again (and the reverse order); compare outputs with a solo run of each | S-VINT (fast) and CENSUS (slow, marked `@pytest.mark.slow`) | byte-identical CSVs for each object regardless of order | D2-c |
| P-11 | `test_vintage_isolation.py::test_r24_default_path_unchanged`: run_joint defaults on the synthetic fixture equal `core_r24/tests/test_run_joint_synthetic.py` expectations; full data equals P-01 | fixtures | equal | D2-d, C8 |
| P-12 | `test_fmr_record.py::test_fmr_sensitivity_documented`: the record file (D-05_DECISION §C4-A5 / FMR record) exists, cites both readings, 102 PUMAs and the effective-date issue, **and** `matched2024_provisional/` is unchanged (P-02) | docs | present and unchanged | C9 (second half), D2-d |

## 4. Final gate test: "no gate relaxed"
- **G-01 (runnable today):** `python no_gate_relaxed.py <repo> fb58ddc <FINAL> [approved_exceptions.json]` (script in Appendix A; scratch copy at `scratch/methods-reviewer/acceptance/no_gate_relaxed.py`, sha256 `2244a4378d72…`).
  - Every assertion, threshold, tolerance, gate or hash-check line present in a `.py`, `*GATES.json`, `*CRITERIA.json` or `ARTIFACT_LOCK.json` file at fb58ddc must still be present (whitespace-normalized; count preserved) at FINAL, unless Kevin lists it as an approved exception.
  - Expected: exit 0.
  - **Run today on 2734062 (VERIFIED):** 223 lines scanned; **exit 1, with 1 violation**: `core_r24/rebuild_raw_person_caches.py` `if len(x.person_zips)!=2:raise RuntimeError('Need both Census person archives')` was removed in e45eb87 (D-05; replaced by member-set checks).
  - So G-01 needs either a Kevin-approved exception entry with a rationale, or the check restored.
- **G-02 (semantic, TO BE WRITTEN):** `test_gates.py::test_housing_container_check_not_relaxed`. Line diffing cannot see the D-05 loosened housing check, because the hash-check line survives while housing was removed from its input dict (VERIFIED: fb58ddc `reproduce_from_raw.py:38-42` vs 2734062).
  - Test: build a ZIP with byte-identical inner `psam_hus*.csv` but a different container. fb58ddc code → FAIL; FINAL code → must FAIL, unless Kevin's dated exception ratifies inner-hash acceptance (D-05 §6).
  - Plus a ZIP with an extra `psam_husc.csv` → FINAL must FAIL.
- **G-03 (TO BE WRITTEN):** `test_gates.py::test_thresholds_unchanged`. `atol=1e-7, rtol=0` (`reproduce_from_raw.py:24,27`), ARTIFACT_LOCK `acceptance` block, `VALIDATION_GATES.json` thresholds, and nowcast `GO_NOGO.json` `decision: NO-GO` must equal their 2734062 values. `RESEARCH_READINESS.json` keys asserted by `test_matched_year_checkpoint.py:111-115` must be unchanged.
- **G-04 (TO BE WRITTEN):** `test_gates.py::test_verify_package_default_not_switched`. This is N-11 restated as a gate. Switching the default to v2 is a gate change (ruling 1) → Kevin.

## 5. Conditions that cannot be made fully executable
1. **C9 "independently reproduced".** Under `ITERATION_REGISTER.txt:10`, EXTERNALLY_INDEPENDENTLY_REPRODUCED "requires an independent operator on a separate environment, with commands, input hashes, outputs, and a report attached".
   - An AI-run P-08 is an AI-operated reproduction on a separate machine, not independent reproduction.
   - The test can only **check for the presence** of an external operator's signed report (`test_fmr_record.py::test_external_report_present`, TO BE WRITTEN: report file, operator identity, input hashes and outputs matching ARTIFACT_LOCK).
   - Whether the operator is independent is a human judgment for Kevin (VERIFIED as a definitional limit).
   - P-08 is also **blocked for any outside operator** until `tract_tenure_acs2024.csv` and `tract_to_puma_50states_dc.csv` have public sources or committed builders (L13 / H-01; VERIFIED, no builder in the tree).
2. **C4 "unreviewed".** A test can detect *any* in-place replacement (N-19…N-22). Whether a replacement was "reviewed" needs a dated Kevin decision record.
   - Proposed executable proxy: `test_manifest_immutability.py::test_every_hash_change_has_decision` (TO BE WRITTEN). For every hash value that differs between S-DIGEST and FINAL, an entry must exist in `decisions/` or `ERRATA.txt` naming the file, the old and new hash, and a date. This checks presence, not quality.
3. **D2-d "without separate review".** Executable only as "the frozen provisional files are unchanged" (P-02, G-03). The review itself is human.
4. **C9 "FMR sensitivity investigated".** Executable only as a document-presence check (P-12). Numeric content is cross-checked against the Engineer's sealed `evidence_2734062_step4/` (VERIFIED in D-05 C4-A1).
5. **N-11, N-29.** The expected outcome depends on a pending Kevin choice (explicit flag vs v1 default; refuse vs documented defaults).

## 6. Traceability matrix
| Condition | Tests |
|---|---|
| C1 immutable historical manifests/evidence | N-19, N-20, N-22, N-30, P-02, P-03, P-05, G-03 |
| C2 missing/empty/mismatched manifest → FAIL | N-01…N-10 |
| C3 no direct-run bypass | N-12…N-18 |
| C4 no unreviewed in-place replacement | N-19…N-22, §5.2 proxy |
| C5 protected outputs rejected before writes | N-15, N-16, N-23, N-30 |
| C6 all pillar and core manifests checked | N-05, N-06, N-20, N-24…N-26, P-05 |
| C7 v1 and v2 paths distinguished | N-01, N-02, N-09…N-11, N-26, N-31, P-03, P-04, G-04 |
| C8 frozen R2.4 and 80 replicates | P-01, P-02, P-07, P-11 |
| C9 matched-year reproduction and FMR sensitivity | P-08, P-12, §5.1 external-report presence |
| D2-a vintages isolated | N-27, N-28 |
| D2-b explicit selections | N-27…N-29, P-09 |
| D2-c no cross-contamination | N-17, P-10 |
| D2-d no definition change / no replacement | P-02, P-11, P-12, G-01…G-03 |
| "no gate relaxed" | G-01…G-04 |

**Counts:**

| Type | Count |
|---|---|
| Negative (N) | 31 IDs, about 50 parametrized cases |
| Positive (P) | 12 |
| Gate (G) | 4 |
| Document-presence proxy (§5.1, §5.2) | 2 |
| **Total** | **49 IDs** |

- Already existing at 2734062 or in the Engineer's diffs: N-12 (part), N-30 (part), P-07, plus the existing `test_artifact_lock`.
- Runnable today: G-01.
- Everything else is **TO BE WRITTEN [K/C]**.

**Today's expected status at 2734062, if run now (VERIFIED where cited, otherwise HYPOTHESIS):**
- N-09, N-12, N-15, N-16, N-17, N-22, N-23 and N-27 would fail, meaning the system does not yet refuse.
- G-01 fails with 1 violation.
- P-01 and P-02 pass (VERIFIED earlier).

## Appendix A: `no_gate_relaxed.py` (G-01; read-only, uses `git show`)
```python
"""G-01: every assertion/threshold line present at BASE must still be present (verbatim, whitespace-normalized) at HEAD,
unless listed in an approved-exceptions file. Read-only: uses `git show` only."""
import re, subprocess, sys, json, collections
repo, base, head = sys.argv[1], sys.argv[2], sys.argv[3]
exc = set(json.load(open(sys.argv[4]))) if len(sys.argv) > 4 else set()
PAT = re.compile(r'(raise (RuntimeError|SystemExit|ValueError)|MISMATCH|sys\.exit\(1|!=HASHES|\bassert\w*\b|raise AssertionError|isclose|allclose|atol|rtol|threshold|tolerance|"pass_all_required_for_GO"|_gate\(|gate\()')
def files(rev):
    out = subprocess.run(['git','-C',repo,'ls-tree','-r','--name-only',rev],capture_output=True,text=True,check=True).stdout.split()
    return [f for f in out if f.endswith('.py') or f.endswith('GATES.json') or f.endswith('CRITERIA.json') or f.endswith('ARTIFACT_LOCK.json')]
def lines(rev, f):
    r = subprocess.run(['git','-C',repo,'show',f'{rev}:{f}'],capture_output=True,text=True)
    if r.returncode: return None
    return collections.Counter(' '.join(l.split()) for l in r.stdout.splitlines() if PAT.search(l))
bad = []; nb = 0
for f in files(base):
    b = lines(base, f); h = lines(head, f); nb += sum(b.values())
    if h is None:
        if b: bad.append({'file': f, 'missing_file': True, 'n_assert_lines': sum(b.values())})
        continue
    for line, n in b.items():
        if h[line] < n and f'{f}::{line}' not in exc:
            bad.append({'file': f, 'removed_or_changed': line, 'count_base': n, 'count_head': h[line]})
print(json.dumps({'base': base, 'head': head, 'assert_threshold_lines_at_base': nb, 'violations': bad}, indent=1))
sys.exit(1 if bad else 0)
```

---

# ADDENDUM A2 (2026-10-22, about 06:10 UTC): the five governance answers (D1–D5)
> **AI methods review, not independent human peer review.** Additive: all 49 IDs above are unchanged.
> - **Source:** `/workspace/hesi-team/decisions/2026-10-22_five_governance_answers.md`, sha256 **`6af3bc51ed4a482186839dc38ce540ace37bfdb6867f47c53d31fcc73783a7a0`**. Computed with `sha256sum`. It equals the Coordinator's `6af3bc51…a7a0` and the companion `.sha256` file (VERIFIED). The file is mode `-r--r--r--`.
> - The answers are **recorded by the Coordinator as Kevin's answers** (file and sha256 above). I have not verified them with Kevin.
> - The file "Supplements, and does not replace, 2026-10-22_formal_governance_decisions.md".
> - Base: `273406208abe439cbad960567f32822b870c43b5`.

## A2.0 Where the file's wording differs from the summary I was given
| # | Summary | File (exact wording) | Effect on tests |
|---|---|---|---|
| D1 | "EXTERNALLY_INDEPENDENTLY_REPRODUCED: NO, REPRODUCTION_REVIEW: PENDING optional" | "Use the existing field EXTERNALLY_INDEPENDENTLY_REPRODUCED: NO … If necessary, separately record REPRODUCTION_REVIEW: PENDING … Preserve the exact meaning of each verification status." | Same. **This supersedes** the formal Decision 1 status `EXTERNALLY_REPRODUCED: PENDING` (see A2.4) |
| D2 | split pair or official archive; five rejection cases | adds "**valid structure**, and **complete input coverage**" and "No silent gate relaxation"; "two correctly **authenticated** split person archives" | Adds N-37 (structure) and N-38 (coverage) |
| D3 | D-05 closes on engineering, provenance and AI reproduction | "D-05 may close after the required engineering checks, provenance verification and AI-operated computational reproduction **pass**. Do not equate D-05 closure with independent human scientific validation." | Same |
| D4 | bare verify uses v1 "against the historical snapshot" | "Keep the original v1 verification semantics as the default for the existing package-verification command … Historical v1 verification must reference the historically correct source snapshot, not changed working-tree files. Missing, empty, **malformed**, or mismatched required manifests must fail closed." | The file does not say *which* snapshot is "historically correct" (see A2.5 conflict 2) |
| D5 | official runs refuse implicit inputs | "Official and locked research executions must require explicit source manifests, cost vintage, methodology configuration and designated output location … all effective inputs, software versions, source hashes, methodology choices and output paths must be recorded" | Same |

## A2.1 New tests
**Supersession and refinement notes** (the old tests are kept):
- **D4:** N-11 is **resolved**: its expected outcome is now "bare `verify_package.py` = v1 semantics" (P-15, P-16). N-01…N-08 are refined by N-43 and N-45, which add *malformed*. P-03 is refined by P-15 (snapshot, not a working tree). P-04 is refined by P-17.
- **D5:** N-29 is **resolved** by N-47…N-53, P-18 and P-19.
- **D2:** N-12…N-14 and P-07 are refined by N-32…N-40, P-13 and P-14.
- **D3:** §5.1 is refined by DC-03.

Common setup as §1, plus **S-ZIP**, a fixture generator `tests/acceptance/fixtures/make_person_zips.py` (TO BE WRITTEN). It builds small synthetic CSV pairs with a matching synthetic lock (used only under the test harness) and every malformed variant listed below. Full-size cases use `$CENSUS/csv_pus.zip`, sha256 `afdc6d90…` (`PUMS_ARCHIVE_LOCK.json`; VERIFIED).

### D2: Census person archive validation (every rejection case separate)
For each must-FAIL case, the procedure runs **both entry points**:
- `python $T/core_r24/reproduce_from_raw.py --housing $CENSUS/csv_hus.zip <person args> --output $O`
- `python $T/core_r24/rebuild_raw_person_caches.py --person-zips <zips> --prices $T/core_r24/inputs/source_2024_2026.csv --out $O`

Before and after each run, take `snap $T` and `snap $(dirname $O)`.
- **must-FAIL PASS criterion:** exit≠0, the message names the defect, `$O` does not exist, and both snapshot diffs are empty.
- **Positive PASS criterion:** exit 0, with cache hashes as stated.

| ID | Case | Fixture | Expected | Type | Traces to |
|---|---|---|---|---|---|
| P-13 | Valid **split pair** (`--person-a HESI_Person_Part_1.zip --person-b HESI_Person_Part_2.zip`) | Kevin's original split archives (container sha256 `05a4bdcb…`, `2a891e40…`; VERIFIED in the lock). **Not present on this box** (VERIFIED: filesystem search by name found none) | exit 0; caches `9ca1e3d2…` / `4e7c8dbb…`; national within tolerance (P-01) | positive | D2(a) |
| P-14 | Valid **official combined** `csv_pus.zip` (refines P-07) | CENSUS | exit 0; same caches; report `person_input_mode: official_combined_zip` | positive | D2(b) |
| N-32 | Missing component, official: ZIP with `psam_pusa.csv` only | S-ZIP | must FAIL ("missing psam_pusb.csv") | must-FAIL | D2 "missing components" |
| N-33 | Missing component, split: only `--person-a`; or `--person-b` is a ZIP lacking its CSV | S-ZIP | must FAIL. Arg check exists for the first variant (`reproduce_from_raw.py:41-42`, VERIFIED); direct rebuild TO BE WRITTEN | must-FAIL | D2 "missing components" |
| N-34 | Duplicate members: (a) `psam_pusa.csv` at the root and in a subfolder of one ZIP; (b) the same CSV in both split parts; (c) the same name twice in the ZIP directory | S-ZIP | must FAIL (refines F1_v2 `N7DuplicateMember`) | must-FAIL | D2 "duplicate members" |
| N-35 | Unexpected CSVs: (a) extra `psam_pusc.csv`; (b) extra `other.csv`; (c) a housing CSV (`psam_husa.csv`) inside the person ZIP. Control: the official `ACS2024_PUMS_README.pdf` is accepted (`test_genuine_layout_with_readme_accepted`) | S-ZIP | must FAIL; control PASS | must-FAIL (+ control) | D2 "unexpected CSVs" |
| N-36 | Invalid hashes: (a) one byte changed in `psam_pusb.csv` of an official-layout ZIP; (b) a split container whose hash ≠ lock; (c) a correct ZIP with an edited `PUMS_ARCHIVE_LOCK.json` (lock self-hash) | S-ZIP / CENSUS copy | must FAIL | must-FAIL | D2 "invalid hashes" |
| N-37 | Invalid structure: (a) a non-ZIP file; (b) a truncated ZIP; (c) a ZIP whose member CRC fails; (d) a CSV with a correct name but a missing header column such as `SERIALNO` (synthetic lock) | S-ZIP | must FAIL before output | must-FAIL | D2 "valid structure" |
| N-38 | Incomplete coverage: (a) split pair where part 2 = part 1 (same file twice); (b) official ZIP whose two CSVs together lack one state's rows (synthetic lock declares the expected row count, or a sentinel set) | S-ZIP | must FAIL | must-FAIL | D2 "complete input coverage" |
| N-39 | Reusable failed-run caches: after each of N-32…N-38 (and an interrupted valid run, killed with `kill -9` mid-rebuild), run the valid P-14 into the **same** `--output` / checkpoint root | S-ZIP + CENSUS | the valid run recomputes (no checkpoint marked COMPLETE from the failed run exists; logs show 0 resumed parts); caches equal P-14's (refines N-17 and F1_v2 `N9*`) | must-FAIL (reuse must not happen) | D2 "reusable failed-run caches" |
| N-40 | Mixed mode: `--person-official` together with `--person-a`/`--person-b`, at both entry points | any | must FAIL (exists for `reproduce_from_raw.py:41`, VERIFIED; direct rebuild TO BE WRITTEN) | must-FAIL | D2 "either (a) or (b)" |
| G-06 | No silent gate relaxation for D2. The G-01 violation (`rebuild_raw_person_caches.py`: `if len(x.person_zips)!=2:raise RuntimeError('Need both Census person archives')`, removed in e45eb87) may enter `approved_exceptions.json` **only** with a rationale citing D2 and a pointer to N-32…N-40 and P-13/P-14. The test fails if the exception exists while any of those tests is missing or failing | G-01 script + pytest results JSON | PASS only if all referenced tests pass | no-gate-relaxed | D2 "No silent gate relaxation" |

### D4: verification default and fail-closed behaviour
| ID | Procedure | Expected / PASS criterion | Type | Traces to |
|---|---|---|---|---|
| P-15 | `cd $T/core_r24 && python verify_package.py` (no flag) on a git checkout | Verifies **v1 semantics against the historical snapshot**: reads `RELEASE_FILE_HASHES.json` and every listed file from the snapshot commit `V1_SNAPSHOT` (via `git show V1_SNAPSHOT:core_r24/<rel>`, or a sealed snapshot tarball whose sha256 is pinned in code), not from the working tree. Exit 0; stdout names `v1`, `V1_SNAPSHOT` and the manifest sha256 (`49871df6…` if V1_SNAPSHOT = fb58ddc) | positive | D4 |
| P-16 | As P-15, after editing `$T/core_r24/src/run_joint.py` (append a comment) and `$T/core_r24/RELEASE_FILE_HASHES.json` | Result identical to P-15 (exit 0, same output). The working-tree edits do not affect v1. stdout states "working tree NOT verified by v1; use --manifest v2" | positive | D4 "not changed working-tree files" |
| N-41 | As P-15, but the snapshot is unavailable: shallow clone without `V1_SNAPSHOT`, a `git archive` tree without `.git`, or a deleted or wrong-hash snapshot tarball | must FAIL closed; **no fallback to working-tree files**. PASS: exit≠0, with "historical snapshot unavailable" | must-FAIL | D4 fail closed |
| N-42 | The bare command must never select v2: run P-15 on a tree where `RELEASE_FILE_HASHES_v2.json` exists and matches the working tree | stdout never contains "v2" PASS; exit status is the v1 result | must-FAIL (implicit v2 must not happen) | D4 "explicit selection of v2"; resolves N-11 |
| N-43 | v1 manifest in the snapshot is missing / empty (0 bytes) / `{}` / **malformed** (`{` or a non-object JSON) / mismatched (forged snapshot tarball with one changed hash; pinned tarball digest mismatch) | must FAIL closed (refines N-01, N-03, N-05, N-07) | must-FAIL | D4 |
| N-44 | `--manifest` with anything other than the allowlisted v2 name, e.g. `/tmp/empty.json`, `../x.json`, a symlink to v2 (refines N-09, N-10) | must FAIL | must-FAIL | D4, C2 |
| N-45 | v2 (explicit) manifest missing / empty / `{}` / malformed / partial / mismatched (refines N-02, N-04, N-06, N-08) | must FAIL closed | must-FAIL | D4 |
| N-46 | Required pillar manifests (INTEGRITY_MANIFEST, SOURCE_HASHES, housing PACKAGE_MANIFEST, transportation SOURCE_HASHES, LOCK_REGISTER, and their v2 counterparts) missing / empty / malformed / mismatched, under the release verifier chosen in N-24 | must FAIL closed (refines N-24, N-25) | must-FAIL | D4, C6 |
| P-17 | `python $T/core_r24/verify_package.py --manifest RELEASE_FILE_HASHES_v2.json`, or the separate entry point `verify_package_v2.py` (Kevin or Cursor chooses one; the test covers whichever exists) | exit 0 on the working tree; stdout names v2 and its sha256 (refines P-04) | positive | D4 |
| G-07 | D4 default is not relaxed: compare the bare command's semantics against fb58ddc's `verify_package.py` (`git show fb58ddc:core_r24/verify_package.py`): the same file set (35 at fb58ddc), the same hash comparison, the same regression-test and `--check-existing` steps (`verify_package.py:13-14` at 2734062, VERIFIED) | every v1 check at fb58ddc is still executed by the bare command | no-gate-relaxed | D4, "no gate relaxed" |

### D5: explicit inputs (official/locked vs dev)
"Official" means the documented official entry points: `core_r24/reproduce_from_raw.py` and `research/historical_matched_baseline/src/run_matched_national.py`, plus any run with `--mode official`. Everything else is "dev". HYPOTHESIS: this classification is a spec proposal and needs Kevin or Cursor to confirm it in the spec.

| ID | Procedure | Expected / PASS criterion | Type | Traces to |
|---|---|---|---|---|
| N-47 | Official run without an explicit `--source-manifest` | must FAIL before any write (snapshot diff empty) | must-FAIL | D5 manifests |
| N-48 | Official run without an explicit `--cost-vintage` (e.g. `R24_SEP2026` or `MATCHED_2024`), or with one inconsistent with the geography, food column or transport inputs | must FAIL before any write (refines N-27, N-28) | must-FAIL | D5 cost vintage; D2-a (formal) |
| N-49 | Official run without an explicit `--method-config` (food column, transport annual, bedroom rule, schedule label, share metric), or with a config whose sha256 is not in the source manifest | must FAIL before any write | must-FAIL | D5 methodology configuration |
| N-50 | Official run without an explicit `--output`. Today `reproduce_from_raw.py:35` defaults to `local_reproduction` (VERIFIED) | must FAIL before any write | must-FAIL | D5 designated output |
| N-51 | Official run with an explicit `--output` inside any frozen path (list as in N-23) | must FAIL before any write (see N-23) | must-FAIL | D5, C5 |
| N-52 | **Dev defaults cannot write to any frozen path.** (a) Static: parse every argparse `default=` and every hard-coded output path in all 29 `__main__` scripts (`git grep -l __main__`, VERIFIED count at 2734062); none may resolve inside the frozen list: `core_r24/results/national_R22`, `core_r24/results/rebuilt_from_raw`, `research/historical_matched_baseline/results/matched2024_provisional`, root `results.csv`/`audit.json`/`manifest.json`, every path listed in RELEASE_FILE_HASHES v1/v2, ARTIFACT_LOCK, LOCK_REGISTER and the pillar manifests. (b) Dynamic: run each script with defaults from `cwd` = each frozen dir, with `HOME` pointed into a frozen dir, and with a symlink from the default output location into a frozen dir | (a) zero hits; (b) every run either exits≠0 or writes only outside the frozen set, with frozen-file sha256 unchanged (P-02 digest set) and snapshot diff empty | must-FAIL (writes must not happen) | D5 "Development defaults cannot create or overwrite frozen scientific results"; C5 |
| N-53 | Dev run whose audit artifact cannot be written (output dir made read-only after creation, via the test harness) | the run fails, and no result CSV is published without its audit (outputs are published atomically together with audit.json) | must-FAIL | D5 recording requirement |
| P-18 | Dev run with documented defaults (synthetic fixture S-VINT): `python $T/core_r24/src/run_joint.py <fixture args> $O` | `audit.json` contains, with correct values: `mode: dev`; every effective input path + sha256; `python`, `numpy`, `pandas` versions; `git_commit`; source-manifest sha256 (or `null` with `mode: dev`); methodology choices (`food_column`, `transport_annual`, `cost_labels`, `share_metric`, `scenario_label`, `cost_vintage`); output path | positive | D5 dev recording; D2-b (formal) |
| P-19 | Official run with all explicit inputs (as P-01 plus the new flags) | exit 0; results within tolerance (P-01); `audit.json` `mode: official` and every explicit input recorded | positive | D5 official; C8 |
| G-08 | Official status cannot be obtained through defaults: no CLI default equals `official`, and no dev-mode output carries an official label (`mode: dev` outputs are refused by `verify_package` and `check_results`) | PASS when both hold | no-gate-relaxed | D5 |

### D1 and D3: status labels and milestones (document and no-gate-relaxed checks)
| ID | Procedure | Expected / PASS criterion | Type | Traces to |
|---|---|---|---|---|
| DC-01 | `git grep -n -E 'EXTERNALLY_(INDEPENDENTLY_)?REPRODUCED\|REPRODUCTION_REVIEW' $FINAL -- STATUS.txt README.md ERRATA.txt research/historical_matched_baseline` | Every matched-year status uses `EXTERNALLY_INDEPENDENTLY_REPRODUCED: NO`; `REPRODUCTION_REVIEW: PENDING` appears only as a separate line; **no new field `EXTERNALLY_REPRODUCED`** | document check | D1 |
| G-05 | `git diff 273406208abe $FINAL -- STATUS.txt README.md` has **no removed line** containing a status label, and no added line sets `EXTERNALLY_INDEPENDENTLY_REPRODUCED`, `SCIENTIFICALLY_VALIDATED` or publication to YES/GO | PASS when both hold | no-gate-relaxed | D1 "Do not change the existing field to YES"; charter rule 4 |
| DC-02 | Every new reproduction report JSON or MD (`*REPRODUCTION*`, `EXECUTION_REPORT*`) on the final tree states "AI-operated" when produced by an AI, and does not set `EXTERNALLY_INDEPENDENTLY_REPRODUCED` to true | PASS when both hold | document check | D1, charter rule 4 |
| DC-03 | A D-05 closure record (planned file, e.g. `decisions/D-05_CLOSURE.md` or an ERRATA entry) lists the PASS results of the engineering tests (N-01…N-53, P-01…P-19, G-01…G-08), provenance verification (D-05_DECISION §3(A) digests) and the AI-operated reproduction (P-01, P-08). It names **C9 as a separate open milestone**, with its own criteria (independent human operator per `ITERATION_REGISTER.txt:10`, and external methodological review), and states that publication stays NO-GO | the record exists, and every cited test ID shows PASS in the attached pytest JSON | document check | D3; refines §5.1 |
| G-09 | `research/historical_matched_baseline/tests/test_matched_year_checkpoint.py::Protocol::test_readiness_nogo_public` passes, and `RESEARCH_READINESS.json` is byte-identical to 2734062 (`1369e287…`, VERIFIED) | PASS when both hold | no-gate-relaxed | D3 "Keep formal scientific publication NO-GO"; formal Decision 1 |

## A2.2 Updated counts
| Type | Original 49 | New in A2 | Total |
|---|---|---|---|
| must-FAIL (N) | 31 | 22 (N-32…N-53) | 53 |
| positive (P) | 12 | 7 (P-13…P-19) | 19 |
| no-gate-relaxed (G) | 4 | 5 (G-05…G-09) | 9 |
| document check | 2 (§5.1, §5.2 proxies, unnumbered) | 3 (DC-01…DC-03) | 5 |
| **Total** | **49** | **37** | **86** |

**Status of the old tests:**
- Resolved by A2: N-11, N-29.
- Refined: N-01…N-10, N-12…N-14, N-17, N-24, N-25, N-27, N-28, P-03, P-04, P-07, G-03, §5.1. These all remain in force.

**Traceability additions** (to the §6 matrix):

| Decision | Tests |
|---|---|
| D1 | DC-01, DC-02, G-05 |
| D2 | P-13, P-14, N-32…N-40, G-06 |
| D3 | DC-03, G-09 |
| D4 | P-15…P-17, N-41…N-46, G-07 |
| D5 | N-47…N-53, P-18, P-19, G-08 |

## A2.3 Conditions still not fully executable
- **P-13 (valid split pair):** BLOCKED for the team. Kevin's `HESI_Person_Part_1/2.zip` are not on this box, and re-zipping `csv_pus.zip` cannot reproduce their container hashes (VERIFIED: the lock records container hashes only for the split pair, `pums_archive.py:41-47` at 2734062).
  - Either Kevin or Cursor runs P-13 with the originals **[K/C]**, or Kevin decides that split archives may be authenticated by inner-CSV hashes plus the D2 member checks. That would be a gate change, needing Kevin's decision under "No silent gate relaxation".
- **N-38(b) coverage:** needs an expected per-archive row count or sentinel in a lock. The current lock has inner-file sizes and CRCs but no row count (VERIFIED, `PUMS_ARCHIVE_LOCK.json`). With the inner SHA-256 pinned, coverage of the official CSVs is implied; the synthetic variant needs a declared count.
- **D4 `V1_SNAPSHOT`:** not specified by D4 (A2.5 conflict 2).

## A2.4 Consistency of TRACK_E_CORRECTIVE_DRAFT.md with D1
**Inconsistent (VERIFIED):** the draft uses the new label `EXTERNALLY_REPRODUCED: PENDING` 8 times (`grep -c` = 8), following the formal Decision 1. D1 now says to use the existing field `EXTERNALLY_INDEPENDENTLY_REPRODUCED: NO`, optionally with `REPRODUCTION_REVIEW: PENDING`. A dated note has been appended to that draft (not rewritten).

## A2.5 Conflicts (scientific or governance), stated explicitly
1. **D1 vs the formal Decision 1:** the earlier record lists `EXTERNALLY_REPRODUCED: PENDING`. D1 replaces it with the existing field. D1's file says it "supplements, and does not replace" the earlier record, but on this point it changes it. **Recommendation (AI):** treat D1 as superseding that one status line, and say so in the decision record. No scientific conflict.
2. **D4 "historically correct source snapshot" is undefined.**
   - `RELEASE_FILE_HASHES.json` has three historical states: fb58ddc `49871df6…` (35 entries), e45eb87 `4f6825d7…` (38) and 2734062 `6cd769e0…` (38, with run_joint re-hashed in place) (VERIFIED).
   - The original release is fb58ddc. The 2734062 "v1" file is itself a twice-rewritten version (D-05).
   - If bare verify_package used the HEAD v1 file, it would certify the in-place rewrites as "v1". That conflicts with formal Decision 3 condition 1 ("Historical manifests and prior release evidence remain immutable") and condition 4.
   - **Needs Kevin's explicit choice of V1_SNAPSHOT.** AI recommendation: fb58ddc, with e45eb87 and 2734062 recorded as history.
3. **D2 vs the existing lock:**
   - D2 accepts "correctly authenticated split person archives", but the only authentication the lock supports for splits is the container hash. That is valid, but the team cannot test it (A2.3).
   - D2 says nothing about the **housing** archive, whose check e45eb87 loosened (container hash, otherwise inner hashes, without member-set checks; `pums_archive.py:73-90`).
   - G-02 therefore remains a **separate Kevin item**. D2 does not ratify it.
4. **D3 vs RESEARCH_READINESS.json and formal Decision 3 C9:**
   - No conflict: D-05 closure is engineering-only. Publication stays NO-GO, consistent with `publish_17_7_percent: NO-GO` and `provisional_public_research_release: NO-GO`.
   - But formal C9 ("independently reproduced") is now **moved out** of D-05. Any record that lists C9 as a D-05 closure condition must note the split.
5. **D5 vs the published matched-year run:**
   - `results/matched2024_provisional/` was produced by runs without an explicit cost vintage, source manifest or method config (e.g. `run_matched.py:35` defaults `transport_annual=6870.67`; VERIFIED).
   - Under D5 these are "official/locked research executions" only if Kevin classifies them so. D5 does not invalidate the committed files, which stay preserved.
   - But P-08 (reproduce matched-year on the final code) must run in **official mode** with explicit inputs equal to the original effective inputs. Any difference must be reported, not silently defaulted.

---

# ADDENDUM A3 (2026-10-22, about 07:00 UTC): CH-17, the FY2025-revised effective-date label fix
> **AI methods review, not independent human peer review.** Additive; the 86 IDs above are unchanged.
> - Authority: `decisions/2026-10-22_hud_contact_authorization.md`, sha256 `53bc916d…a639836` (VERIFIED), recorded by the Coordinator as Kevin's order.
> - Base `273406208abe`. Setup as §1. `BASE=273406208abe439cbad960567f32822b870c43b5`.
> - Line references (all VERIFIED correct): `HISTORICAL_ALIGNMENT_PROTOCOL.md:22`, `src/prepare_2024_cost_inputs.py:83`, `SOURCE_REGISTER.json:74`, `ITERATION_NOTES.txt:683`.

| ID | Procedure | Expected / PASS criterion | Type | Traces to |
|---|---|---|---|---|
| N-54 | `git diff --quiet $BASE -- core_r24/RELEASE_FILE_HASHES.json research/september2026_core_r2/LOCK_REGISTER.json research/september2026_core_r2/INTEGRITY_MANIFEST.json research/september2026_core_r2/SOURCE_HASHES.json research/september2026_core_r2/housing/PACKAGE_MANIFEST.json research/september2026_core_r2/transportation/SOURCE_HASHES.json research/historical_matched_baseline/results/matched2024_provisional/ARTIFACT_LOCK.json`. Fault injection: a candidate patch that edits any of these files | clean candidate: exit 0; injected: the test reports FAIL (an in-place v1 edit is detected; refines N-19, N-20) | must-FAIL (injected) | R21; formal D3 c1, c4 |
| N-55 | `test "$(git show HEAD:ITERATION_NOTES.txt \| sed -n 683p)" = "  effective 2025-04-27"` **and** `git diff --numstat $BASE -- ITERATION_NOTES.txt \| awk '$2!=0{exit 1}'` **and** the appended note contains "90 FR 14158" and "Line 683 is kept as written" | all three hold; any deletion or edit of a historical line → FAIL | must-FAIL (history rewrite must not happen) | R20; five-answers Implementation ("Do not rewrite original governance history") |
| N-56 | Diff-scope check: `git diff -U0 $BASE -- <file>` for the three edited files | Protocol: exactly line 22 changed (plus an optional appended sentence on the same bullet). `prepare_2024_cost_inputs.py`: exactly line 83 changed, only within the string value (and an optional trailing comment). `SOURCE_REGISTER.json`: exactly line 74 changed (plus the optional sibling key). Any other changed line → FAIL. `git grep -n '2025-04-27' HEAD` lists only `ITERATION_NOTES.txt:683`, the optional sibling key and the correction notes | must-FAIL (out-of-scope edits) | R20 |
| P-20 | Patched vs unpatched cost-input build, same venv and thread env: `python research/historical_matched_baseline/src/prepare_2024_cost_inputs.py --out $S/base_out` on `$BASE` and `--out $S/patched_out` on the patched tree (`HESI_DOWNLOADS`/`HESI_CLEANREPRO` set; explicit scratch out). Then `diff -r` of every `.csv` and `MATCHED_YEAR_READINESS.json` | **Byte-identical**. `SOURCE_REGISTER.json` differs **only** in the `fy25_revised.effective` value (`jq 'del(.hud.fy25_revised.effective)'`-style comparison equal, or exactly one differing line). The `.csv` outputs also equal the committed `research/historical_matched_baseline/outputs/*` sha256 (REPRODUCER_HANDOFF.md:30-33 and the outputs tree) | positive | R20 |
| P-21 | Patched vs unpatched matched-year run, same environment: `python research/historical_matched_baseline/src/run_matched_national.py --housing $CENSUS/csv_hus.zip --person-official $CENSUS/csv_pus.zip --out $S/{base,patched}_run --cache $S/cache_{base,patched}` | all three scenario `common_cohort_results.csv`, `replicate_results.csv` and `audit.json` byte-identical between base and patched. Against the committed ARTIFACT_LOCK values: within `metric_atol 1e-7`, `frame_exact`, 80 replicates. Byte-identity to the committed author files is **not** required (AI reruns differ by up to about 1.7e-10 even unpatched; VERIFIED in `evidence_2734062_step4_w2`) | positive | R20; formal D2 ("Do not … replace the current provisional calculation") |
| P-22 | After applying the patch and running P-20/P-21: `python /tmp/lockchk.py .` (ARTIFACT_LOCK 14/14 sha256+size) and `python -m pytest -q tests/acceptance/test_frozen.py::test_frozen_files_unchanged` (P-02 set) | 14/14 and P-02 PASS; `git status --porcelain` shows only the declared CH-17 files | positive | R20; formal D3 c1 |
| G-10 | No gate relaxed by CH-17: `python no_gate_relaxed.py . $BASE HEAD` limited to the CH-17 files has zero violations; `prepare_2024_cost_inputs.py` constants `DAYS_FY24_ORIG=70`, `DAYS_FY24_REV=204`, `DAYS_FY25_ORIG=92`, `DAYS_2024=366` (`:105-108`) and the gate list are unchanged | PASS when both hold | no-gate-relaxed | R20, R15 |
| DC-04 | Documentation check: `ERRATA.txt` has an appended entry listing the 4 locations, old `2025-04-27`, new `2025-04-28` and the source (90 FR 14158), and stating no numerical change; `HISTORICAL_ALIGNMENT_PROTOCOL.md:22` carries the dated correction sentence | present | document check | R20 |
| DC-05 | Manifest coverage: a v2 manifest (e.g. `research/historical_matched_baseline/MANIFEST_v2.json`) lists the patched `SOURCE_REGISTER.json`, `prepare_2024_cost_inputs.py` and `HISTORICAL_ALIGNMENT_PROTOCOL.md` with current hashes. HISTORY records old values `f13565156df8…`, `27df706e1a4f…`, `a277a39fd0b9…` (full values from `git show $BASE:<f> \| sha256sum`). No v1 file is edited (N-54) | present and matching | document check | R21, R22 (gap T-4) |

**Updated counts (A3):**

| Type | After A2 | New in A3 | Total |
|---|---|---|---|
| must-FAIL | 53 | 3 (N-54…N-56) | 56 |
| positive | 19 | 3 (P-20…P-22) | 22 |
| no-gate-relaxed | 9 | 1 (G-10) | 10 |
| document check | 5 | 2 (DC-04, DC-05) | 7 |
| **Total** | **86** | **9** | **95** |

**Traceability additions:**

| Requirement | Tests |
|---|---|
| R20 label fix without numeric change | N-55, N-56, P-20, P-21, P-22, G-10, DC-04 |
| R21 v2-only hashes; v1 untouched | N-54, DC-05 |
| R22 historical-baseline manifest coverage (gap T-4) | DC-05 |

- Spec gaps T-1…T-3 remain open (no test yet). T-4 is new and covered by DC-05.
- **HUD-contact authorization:** noted in CURSOR_IMPLEMENTATION_SPEC CH-17.5. No test is defined for an external contact; its provenance-record requirements are a document check for whoever is assigned. Not acted on here.

---

# ADDENDUM A4 (2026-10-22, written about 06:20 UTC): questions (a) and (b) resolved
> **AI methods review, not independent human peer review.** This addendum is additive: the 95 IDs above are unchanged.
> - **Authority:** `decisions/2026-10-22_spec_questions_resolved.md`, sha256 **`9e6f1b757e6c7424dc23f4b53466811e194a1e2b3e26707499bb360352f96800`** (VERIFIED; matches its `.sha256`). It is **recorded by the Coordinator as Kevin's resolution**. Its text:
>   - "(a) Use fb58ddc as the historical baseline, conditional on verifying that its file contents and hashes correspond to the intended original evidence. Document any earlier changes rather than rewriting history."
>   - "(b) Apply equivalent or stronger integrity validation to Census housing archives, accounting for their actual file structure."
> - **Base:** `273406208abe`. Setup is as in §1, plus `V1_SNAPSHOT=fb58ddc045976d844c6da1fca99ed1f9f108bb85`.
> - **Evidence for (a):** `findings/methods-reviewer/2026-10-22_fb58ddc_v1_verification.md`. Verdict: **PASS with documented earlier changes**. The eec7c46 in-place refresh happened before fb58ddc. Comparison with the external ZIPs is BLOCKED.
> - **Timestamp note:** Addendum A3's heading says "about 07:00 UTC". That was an estimate error. A3 was written before 06:00 UTC (file mtime 05:50 UTC). The heading is left as written.

## A4.1 Resolved items (cross-references; nothing deleted)
| Item | Where | Status now |
|---|---|---|
| A2.5 conflict 2 "D4 historically correct snapshot undefined" | A2.5 §2, A2.3 third bullet | **RESOLVED**: V1_SNAPSHOT = fb58ddc (resolution (a)). Verified PASS (findings file §0). Tests P-23, P-24, N-57, N-58, DC-06 |
| P-15's open expected value | A2.1 D4 | **RESOLVED**: the manifest is `49871df6…`, with 35 entries. P-15 is refined by P-23 |
| A2.5 conflict 3, housing half ("D2 says nothing about the housing archive") | A2.5 §3 | **RESOLVED** by resolution (b). Tests N-59…N-66, P-25, P-26, G-11 |
| G-02 "housing container check not relaxed" (TO BE WRITTEN; pending a Kevin decision) | §4 | **RESOLVED and refined by G-11.** Under (b), a re-containered archive whose inner CSVs match the lock and whose member set is exact is accepted. This is equivalent to the person official-archive path (D2(b)). That is my reading (HYPOTHESIS as an interpretation, see A4.5). G-02's second bullet (an extra `psam_husc.csv` must FAIL) is kept and is now N-61(a) |
| "N-36 housing variant (TO BE WRITTEN)" | spec CH-05 | superseded by N-62 |
| Spec §7 items 1 and 3; spec §8 conflict 1; spec R11 "Needs a Kevin decision" | CURSOR_IMPLEMENTATION_SPEC | **RESOLVED**; see the FINAL-FOR-CURSOR section there |

## A4.2 New tests for (a): bare `verify_package` = fb58ddc snapshot
| ID | Procedure | Expected / PASS criterion | Type | Traces to |
|---|---|---|---|---|
| P-23 | `cd $T/core_r24 && python verify_package.py` (no flag) on a full git checkout of FINAL (refines P-15) | exit 0. stdout names `v1`, `fb58ddc045976d844c6da1fca99ed1f9f108bb85`, manifest sha256 `49871df6d998cbc1dbfd71c14bb84631474de1a7ef1cddf4db6ecc21739d2e96`, and "35". The hash pass runs over the snapshot bytes (`git show fb58ddc:core_r24/<rel>`, or a pinned archive whose sha256 is a source constant). The unit-test and `--check-existing results/rebuilt_from_raw` steps (`verify_package.py:13-14` at fb58ddc) run **from the snapshot code**, in a temp export, never on working-tree code. Reference: on a `git archive fb58ddc` export, fb58ddc's own command exits 0 with "PASS: all 35" (VERIFIED, `scratch/methods-reviewer/fb58_v1/verify_package_fb58ddc.log`, `2c35481c…`) | positive | (a); D4; R7 |
| P-24 | Snapshot fidelity recomputation: `python tests/acceptance/v1_snapshot_check.py fb58ddc` (TO BE WRITTEN; reference implementation `scratch/methods-reviewer/fb58_v1/v1check.py`, `b63fd3d7…`). It hashes every entry of the five manifests via `git show` | 35/35, 40/40, 24/24, 15/15, 10/10, with 0 mismatches. The manifest digests equal the pinned constants (`49871df6…`, `a0de5589…`, `29e8aa72…`, `5ecf44ae…`, `e4fe0a48…`) and `LOCK_REGISTER.json` `be3388d7…` (VERIFIED today, `v1check.out`, `1a056afa…`) | positive | (a) "verifying that its file contents and hashes correspond" |
| N-57 | Snapshot substitution: point the bare command at a snapshot whose manifest is (i) d658c08's `c5ac44d0…` (34 entries), (ii) e45eb87's `4f6825d7…`, (iii) 2734062's `6cd769e0…`, or (iv) fb58ddc's manifest with one hex char flipped. Use a test hook that overrides the snapshot ref or archive, available only under the harness | each must FAIL closed ("v1 snapshot digest mismatch"). The pinned digest is `49871df6…` and git blob `6e560d6b82798c1d28b3060d2c553172737f6334` | must-FAIL | (a); D4 fail-closed; R1 |
| N-58 | Working-tree immunity: on FINAL, append a byte to `core_r24/results/national_R22/audit.json` and to `core_r24/src/run_joint.py` in the working tree, then run the bare command | the v1 result is unchanged (exit 0, same stdout as P-23), plus the warning "working tree NOT verified by v1". **Paired run:** `--manifest RELEASE_FILE_HASHES_v2.json` on the same tree must FAIL naming both files. This proves the edit is caught by the v2 path, not ignored everywhere (refines P-16) | must-FAIL (paired v2 run) | D4; R7 |
| DC-06 | Lineage record: `core_r24/RELEASE_FILE_HASHES_HISTORY.json` (or the ERRATA equivalent) lists, in order, d658c08 `c5ac44d0…` (34), eec7c46 = fb58ddc `49871df6…` (35), e45eb87 `4f6825d7…` (38) and 2734062 `6cd769e0…` (38). The eec7c46 transition shows the six entry changes (run_joint `7ddc2658…`→`030cb0ae…`; −2 pkl fixtures; +2 CSV fixtures; +`tests/test_run_joint_synthetic.py`). The record also lists the pre-fb58ddc ITERATION_REGISTER/NOTES edits (findings §5) | all present. The Engineer's current `09_…restore_history.diff` **fails** this test today because it starts at fb58ddc (VERIFIED by reading) | document check | (a) "Document any earlier changes" |

## A4.3 New tests for (b): housing-archive integrity, equivalent to or stronger than the person checks
**Actual housing structure** (VERIFIED, findings §7):
- official `csv_hus.zip`, container sha256 `8281008e…`;
- members `psam_husa.csv` (827,133 rows, 25 STATE codes 01–28) and `psam_husb.csv` (804,836 rows, 26 codes 29–56), each 241 columns, plus `ACS2024_PUMS_README.pdf`;
- inner sha256, CRC and sizes are in `PUMS_ARCHIVE_LOCK.json`;
- no split variant; no housing cache (run_joint streams the ZIP).

**Entry points for every case:**
- `reproduce_from_raw.py --housing`;
- `run_matched_national.py --housing` (via `validate_matched_inputs.py:103`);
- direct `src/run_joint.py --housing-zip` and `run_matched.py`.

**Fixture S-HZIP** (TO BE WRITTEN): `tests/acceptance/fixtures/make_housing_zips.py` builds small synthetic `psam_husa/b.csv` files with the real 241-column header and a synthetic lock (harness only). The lock declares inner hashes, row counts and STATE sets.

**must-FAIL PASS criterion:** exit≠0 before any directory, staging dir or cache is created, with `snap` diffs empty (as in D2).

| ID | Case | Expected | Type | Traces to |
|---|---|---|---|---|
| N-59 | Missing member: (a) no `psam_husb.csv`; (b) no `psam_husa.csv`; (c) an empty ZIP | must FAIL ("missing psam_hus?.csv"). Rejected today by the inner-hash path (VERIFIED probe, `missing.zip`) | must-FAIL | (b) missing |
| N-60 | Duplicate members: (a) `psam_husa.csv` at the root and in `x/`; (b) the same name twice, bad copy first; (c) the same name twice, bad copy last; (d) `psam_husa.csv` and `PSAM_HUSA.CSV` | must FAIL ("duplicate member"). **Today (a) and (b) are ACCEPTED, and `run_joint.py:45` would read the duplicate** (VERIFIED probe, `dup_dir.zip`, `dup_same_badfirst.zip`) | must-FAIL | (b) duplicate |
| N-61 | Unexpected CSVs: (a) extra `psam_husc.csv`; (b) `notes.csv`; (c) a person CSV `psam_pusa.csv` inside the housing ZIP; (d) an unexpected non-CSV member other than `ACS2024_PUMS_README.pdf` (e.g. `x.txt`). Control: the genuine 3-member layout is accepted (P-25) | must FAIL. **Today (a) and (b) are ACCEPTED, and (a) would be read by run_joint** (VERIFIED probe) | must-FAIL | (b) unexpected CSVs (refines G-02 bullet 2) |
| N-62 | Bad hashes: (a) one byte changed in `psam_husb.csv`; (b) an edited `PUMS_ARCHIVE_LOCK.json` (lock self-hash pinned in code, as for person); (c) an official container whose sha256 matches the lock but whose inner CSV has been made to mismatch (impossible for genuine bytes; tests that the inner check runs **even when the container matches**; the Engineer's `01_…diff` does this, VERIFIED by reading diff-file lines 577-580) | must FAIL | must-FAIL | (b) bad hashes; R3 |
| N-63 | Structure: (a) a non-ZIP file; (b) a truncated ZIP; (c) a member CRC failure; (d) a correct name with a header missing any `run_joint.py:43` column (`SERIALNO, STATE, PUMA, TYPEHUGQ, NP, WGTP, HINCP, ADJINC, TEN, WGTP1…80`) (synthetic lock); (e) a header with ≠ 241 columns | must FAIL before output | must-FAIL | (b) structure |
| N-64 | Coverage (synthetic lock declares row counts and STATE sets): (a) `psam_husb.csv` = a copy of `psam_husa.csv`; (b) one STATE code missing from the union; (c) a row count different from the declared count; (d) husa and husb STATE sets overlapping | must FAIL. For the official file, coverage is anchored by the inner sha256 plus the audit check `raw_rows == 1631969` (`national_R22/audit.json`; VERIFIED) | must-FAIL | (b) coverage |
| N-65 | Verify-then-read binding: verification returns the exact member list, and run_joint/run_matched read **only** those members. Test: run `src/run_joint.py` directly with a ZIP that passes the old check but carries `psam_husc.csv` | must FAIL before `out.mkdir` (refines N-15). Today `run_joint.py:44-45` re-selects members independently, with `assert len(members)>=1` (VERIFIED by reading) | must-FAIL | (b) "equivalent or stronger"; R3 |
| N-66 | Failed-run reuse: after each of N-59…N-65 and after an interrupted valid run (`kill -9` during run_joint's housing pass), rerun valid P-25 into the same `--output` and cache root | no staging dir, `COMPLETE.json` or partial `common_cohort_results.csv` from the failed run remains. The valid run recomputes, and its results equal P-25's byte-for-byte. Person checkpoints (D2) are not marked complete by a run that failed on housing | must-FAIL (reuse must not happen) | (b) failed-run cache reuse |
| P-25 | Valid official `csv_hus.zip` (`8281008e…`) with official person input | exit 0. The report shows `zip_sha256_matches_lock: true`, the inner hashes of both CSVs and `members` = the 2 CSVs (+ README). `audit.json` `raw_rows 1631969`. National results within tolerance (P-01) | positive | (b) valid |
| P-26 | Valid re-containered archive: the two genuine CSVs (+/− README) re-zipped (container ≠ `8281008e…`) | exit 0 with `mode: housing_inner_csv`. Results **byte-identical** to P-25 in the same environment. This is the interpretation in A4.5 | positive | (b) "equivalent" (D2(b) analogue) |
| G-11 | Housing no-gate-relaxed (refines G-02): run every N-59…N-65 fixture through fb58ddc's housing check (`reproduce_from_raw.py:38-42` at fb58ddc, container hash only) and FINAL's | every fixture that fb58ddc rejects, FINAL also rejects. The **only** fb58ddc-rejected input FINAL may accept is P-26's re-containered genuine content, and only via the A4.5 interpretation, recorded in `approved_exceptions.json` with a pointer to resolution (b) | no-gate-relaxed | (b); R15 |
| DC-07 | Decision register: `decisions/` (or the team decision register) records (a) and (b) as RESOLVED, citing `9e6f1b75…`. The fb58ddc verification findings file is referenced from D-05 closure (DC-03) | present | document check | resolution "Directions" |

## A4.4 Updated counts
| Type | After A3 | New in A4 | Total |
|---|---|---|---|
| must-FAIL | 56 | 10 (N-57…N-66) | 66 |
| positive | 22 | 4 (P-23…P-26) | 26 |
| no-gate-relaxed | 10 | 1 (G-11) | 11 |
| document check | 7 | 2 (DC-06, DC-07) | 9 |
| **Total** | **95** | **17** | **112** |

- Resolved or refined in A4 (kept in force as history): G-02 (→ G-11, N-61), P-15 (→ P-23), P-16 (→ N-58), N-15 (→ N-65 for housing), the CH-05 "N-36 housing variant" (→ N-62).

**Traceability additions:**

| Requirement | Decision | Tests |
|---|---|---|
| R23 v1 = fb58ddc snapshot, verified; lineage documented | resolution (a); D4 | P-23, P-24, N-57, N-58, DC-06, DC-07 |
| R11 (re-scoped) housing archive validation, equivalent or stronger | resolution (b) | N-59…N-66, P-25, P-26, G-11, DC-07 |
| R24 validation gates must be computed, not constant (new observation) | formal D3 c2 (spirit); R15 | no new ID: CH-21 is covered by an added assertion in G-11's harness (`validate_matched_inputs.validate(...)` called with an output path inside `national_R22` must report the gate FAIL). If Cursor prefers a separate ID, reserve N-67 |

## A4.5 Interpretation and remaining conditions
- **Interpretation (HYPOTHESIS):** I read "equivalent" as allowing a non-official container when the exact member set and the inner hashes match (P-26), as D2(b) does for persons.
  - The stricter reading is that only the official container is accepted. Under it, P-26 flips to must-FAIL and G-11 needs no exception. This choice does not alter any result: P-26 requires byte-identical results.
  - I do not re-request a decision. I flag the reading so that Cursor implements one of the two explicitly.
- **N-64 for the official file** relies on the lock hash plus `raw_rows`. A per-member row count or STATE set in the lock would need a **new versioned lock file** (e.g. `PUMS_ARCHIVE_LOCK_v2.json`). `PUMS_ARCHIVE_LOCK.json` is frozen (§1.1) and must not be edited.
- The external R2.4 and pillar ZIPs are not available, so DC-06 can document lineage only from d658c08 onward (findings §0, BLOCKED) **[K]**.

---

# ADDENDUM A5 (2026-10-22, written about 06:35 UTC): CH-19 and CH-21 release-blocking test audit
> **AI methods review, not independent human peer review.** This addendum is additive: the 112 IDs above are unchanged.
> - **Authority:** `decisions/2026-10-22_final_remediation_priorities.md`, sha256 **`d8555f09e7990ae1edb8433480c8378e548878d02358d6f1deeb6019f27f01c0`** (VERIFIED; matches its `.sha256`). It is the **Coordinator's record of Kevin's priorities**.
> - It says:
>   - "CH-19 and CH-21 are mandatory release-blocking corrections."
>   - "CH-19: require negative tests proving that duplicate, unexpected, missing, or unauthenticated Census housing CSV components are rejected without contaminating caches or results."
>   - "CH-21: replace the hard-coded PASS with a real protected-output validation check. Require negative tests showing rejection occurs before any writes."
>   - "The 112 acceptance tests must be mapped to actual evidence. Report PASS, FAIL, or BLOCKED per test."
> - **Register:** `decisions/DECISION_REGISTER.md`, sha256 **`a41961d2dac1da6db81a8d3c17aff4e15787fa3abae706cef2111dff2b346e70`** (VERIFIED; matches its `.sha256`). It is the Coordinator's record. All five hash prefixes in it match the files (VERIFIED by recomputation).
> - Base `273406208abe`.

## A5.0 DC-07 status
- **Register half: SATISFIED (VERIFIED).** The register lists `2026-10-22_spec_questions_resolved.md` with `9e6f1b757e6c7424…` and status RESOLVED. One file entry covers both (a) and (b).
- **Second half: NOT YET SATISFIED.** That half requires "the fb58ddc verification findings file is referenced from D-05 closure (DC-03)". The closure record (CH-16) does not exist yet. DC-07 stays **open until CH-16 is written**.
- **Observations, not failures:**
  - The register file is writable (`-rw-r--r--`), unlike the decision files (`-r--r--r--`).
  - The 06:23:58Z row was appended after the "Open (not decisions)" paragraph, so it falls outside the Markdown table. This is cosmetic.

## A5.1 Audit of CH-19 tests (N-59…N-66, P-25, P-26, G-11)
| Required by the priorities file | Existing coverage | Gap |
|---|---|---|
| Duplicate CSV, in a subfolder | N-60(a) | **Bundled.** It shares one ID with three other duplicate variants, so it is not a distinct test |
| Duplicate CSV, listed twice | N-60(b), (c) | Bundled |
| Unexpected CSV, `psam_husc.csv`-style | N-61(a) | Bundled with (b)–(d) |
| Unexpected CSV, unrelated | N-61(b) | Bundled |
| Missing CSV | N-59 | Distinct, but its parametrization also covers the empty ZIP. Acceptable |
| Unauthenticated: bad hash | N-62(a) | Bundled |
| Unauthenticated: **absent hash** (the lock has no entry for a member) | **none** | **Missing.** Today `pums_archive.py:86` would raise `KeyError`. That exits≠0, but no test checks that it happens before writes or that the message is a clean refusal |
| Unauthenticated: **re-zip that doesn't match** | N-62 only indirectly | **Missing as a distinct case.** A re-containered archive whose member bytes differ from the lock (e.g. CRLF line endings, re-sorted rows: same content, different bytes) |
| "Without contaminating caches or results": hash **and** mtime snapshots | A4 criterion "snap diffs empty (as in D2)". §1 `snap()` records `%Y` (mtime in **whole seconds**) and sha256, only for `$T` and `dirname $O` | **Three gaps:** (1) second-resolution mtime can miss a same-second rewrite; (2) the external cache roots are not snapshotted (`--cache` of `run_matched_national.py:47`, the person checkpoint root, `local_caches/`); (3) no **pre-populated** valid cache or result exists to detect *modification*, only creation |
| Harness can actually detect a write | none | **Missing:** a positive control that a valid run *does* change the snapshot |

Related observation (VERIFIED by reading; CH-09/CH-08 scope, not CH-19): `run_matched_national.py:61-65` reuses `--cache` person caches whenever the two `.pkl` files merely exist. There is no content key. A contaminated cache would be reused silently, so N-74's snapshot must include `--cache`.

## A5.2 Audit of CH-21 tests
| Required | Existing coverage | Gap |
|---|---|---|
| The gate returns FAIL for a protected output | an assertion inside G-11's harness (A4.4 R24) | **Not a distinct must-FAIL test**; no ID |
| The test can actually fail (it detects a hard-coded PASS) | none | **Missing** (mutation test) |
| Rejection before any write: no output dir created, no `INPUT_VALIDATION.json` written, frozen paths untouched | N-23 / N-51 cover generic protected-path refusal for `run_matched_national.py`, but not through the validation gate | **Missing.** Today `run_matched_national.py:53` runs `mkdir`, and `:56` **writes `INPUT_VALIDATION.json` before** `:57` checks the status (VERIFIED by reading). Every validation failure therefore leaves a directory and a JSON behind |
| The gate is not trivially FAIL | none | **Missing:** a positive control |
| No other constant gate | none | **Missing:** a static scan |

## A5.3 Common harness: `snap_ns` (replaces `snap()` for the A5 tests; §1 `snap()` is kept)
```bash
snap_ns() { out=$1; shift; for root in "$@"; do [ -e "$root" ] || { echo "ABSENT $root"; continue; }
  (cd "$root" && find . -path ./.git -prune -o -print0 | sort -z | \
   xargs -0 stat -c "$root|%n|%F|%s|%.9Y|%.9Z" ; \
   find . -path ./.git -prune -o -type f -print0 | sort -z | xargs -0 sha256sum | sed "s|^|$root|"); done > "$out"; }
```
- **Roots (S-HSNAP):** `$T` (includes every frozen results path), `$(dirname $O)`, `$O` itself (expected ABSENT), the person checkpoint root, `$C` (`--cache`), and `$T/research/historical_matched_baseline/local_caches`.
- **Pre-population:** before each test, `$C` and the checkpoint root are filled with the valid caches from P-25, and `$O.prev/` holds a valid result set. The test can therefore detect *modification*, not only creation.
- **must-FAIL PASS criterion (all A5 N-tests):**
  - exit≠0;
  - the message names the defect;
  - `$O` absent (and `$O.partial*` / staging absent);
  - `diff before after` empty: no path added or removed, and size, mtime (ns), ctime (ns) and sha256 unchanged for every file.
- **Entry points (parametrized):** `reproduce_from_raw.py --housing`, `run_matched_national.py --housing --cache $C --out $O`, `src/run_joint.py --housing-zip` (direct), `run_matched.py` (direct).

## A5.4 New tests
| ID | Case | Expected / PASS criterion | Type | Traces to | Refines |
|---|---|---|---|---|---|
| N-67 | Housing ZIP with `psam_husa.csv` at the root **and** `sub/psam_husa.csv` (genuine husb) | A5.3 criterion. Today: ACCEPTED (VERIFIED probe `dup_dir.zip`) | must-FAIL | priorities CH-19 "duplicate"; (b) | N-60(a) |
| N-68 | Same name `psam_husa.csv` listed twice in the central directory. Parametrized: bad copy first, and bad copy last | A5.3 criterion, both orders. Today: bad-first ACCEPTED, bad-last rejected only through the hash (VERIFIED probe) | must-FAIL | CH-19 "duplicate" | N-60(b,c) |
| N-69 | Extra `psam_husc.csv` (valid header, 1 row) beside genuine husa/husb | A5.3 criterion. Today: ACCEPTED, and `run_joint.py:45` would read it (VERIFIED probe) | must-FAIL | CH-19 "unexpected" | N-61(a) |
| N-70 | Extra unrelated `notes.csv` beside genuine husa/husb | A5.3 criterion. Today: ACCEPTED (VERIFIED probe) | must-FAIL | CH-19 "unexpected" | N-61(b) |
| N-71 | Missing `psam_husb.csv`; parameter: missing `psam_husa.csv` | A5.3 criterion (today rejected by the hash path; the snapshot assertions are new) | must-FAIL | CH-19 "missing" | N-59 |
| N-72 | Unauthenticated, **bad hash**: one byte changed in `psam_husb.csv` | A5.3 criterion | must-FAIL | CH-19 "unauthenticated" | N-62(a) |
| N-73 | Unauthenticated, **absent hash**: a harness lock without the `inner_csv_sha256["psam_husb.csv"]` key; variants with the value `null` or `""`. The archive itself is genuine | A5.3 criterion **and** a clean refusal message ("no lock hash for psam_husb.csv"), not an uncaught `KeyError` traceback | must-FAIL | CH-19 "unauthenticated" | new |
| N-74 | Unauthenticated, **non-matching re-zip**: genuine CSVs re-encoded (CRLF line endings, or rows re-sorted) and re-zipped. Container ≠ `8281008e…`; inner sha256 ≠ lock | A5.3 criterion. The snapshot includes `--cache $C`, pre-populated | must-FAIL | CH-19 "unauthenticated"; (b) | new (contrast: P-26 is an exact-bytes re-zip) |
| N-75 | CH-21 unit: `validate(..., out=X)` for X in `core_r24/results/national_R22`, `…/national_R22/sub`, `core_r24/results/rebuilt_from_raw`, `research/historical_matched_baseline/results/matched2024_provisional`, repo root, and a symlink in `/tmp` pointing to `national_R22`. All other inputs are valid (harness stubs for the archive checks) | the returned report has the gate `output_dir_not_national_R22` (or its renamed successor `output_dir_not_protected`) = **FAIL**, `status` = FAIL, and the gate name appears in `failed`. `validate()` itself performs no filesystem write (snapshot of the cwd and `$T` unchanged) | must-FAIL | CH-21 "real protected-output validation check" | G-11 assertion (A4.4 R24) |
| N-76 | CH-21 end-to-end: `run_matched_national.py --housing $CENSUS/csv_hus.zip --person-official $CENSUS/csv_pus.zip --cache $C --out X`, for each X in N-75 plus `matched2024_provisional` given **without** a trailing path normalisation (e.g. `results/./matched2024_provisional`) | A5.3 criterion. Specifically: no new directory; `INPUT_VALIDATION.json` neither created nor modified anywhere (`matched2024_provisional/INPUT_VALIDATION.json` sha256 and mtime_ns unchanged; ARTIFACT_LOCK 14/14); `$C` unchanged | must-FAIL | CH-21 "rejection occurs before any writes" | N-23, N-51 |
| N-77 | CH-21 ordering: run `run_matched_national.py` with a fresh, non-existent scratch `--out $O` and an input that fails validation for another reason (N-72's archive, or a wrong `source_2024_2026.csv` hash in a harness copy) | `$O` is **not created** and no `INPUT_VALIDATION.json` exists anywhere. The failure report goes to stderr or a log outside every output path. Today `:53` mkdir and `:56` write happen first (VERIFIED by reading), so this fails today | must-FAIL | CH-21; D5 | new |
| N-78 | CH-21 mutation test: in a temp copy, restore the gate to the constant `True` (the 2734062 code at `:135`), then run N-75 and N-76 | the N-75 and N-76 tests **must report FAIL** against the mutant. This proves the tests can fail. The harness records the mutant's exit status | must-FAIL (mutant must be caught) | CH-21 "show it can actually fail" | new |
| P-27 | CH-21 positive control: `validate(..., out=$S/fresh)` and a full `run_matched_national.py --out $S/fresh` with valid inputs | the gate = PASS, `status` PASS; `INPUT_VALIDATION.json` is written only into staging and published with the outputs. Results within ARTIFACT_LOCK tolerance (P-08) | positive | CH-21 (not trivially FAIL) | — |
| P-28 | Harness sensitivity: run a valid P-25 into `$O`, with `snap_ns` before and after | the snapshot diff is **non-empty** (new `$O` files appear). A pre-populated cache file that is intentionally `touch`ed changes the `%.9Y` field. This proves `snap_ns` detects writes and mtime-only changes | positive (control) | CH-19, CH-21 snapshot validity | — |
| G-12 | Static gate scan: AST over every `.py` that builds gate records (`gate(name, cond, …)`, `gates.append(...)`, `"status": "PASS"` literals). No gate condition may be a constant (`True`, `1`, or a literal `"PASS"`). Also, the set of gate names in `validate_matched_inputs.py` at FINAL ⊇ the set at 2734062 (no gate removed; renaming is allowed only with a mapping in `approved_exceptions.json`) | zero constant gates; no gate removed. Today: **1 hit**, `validate_matched_inputs.py:135` (VERIFIED by reading) | no-gate-relaxed | CH-21; R15, R24 | G-11 assertion |

**Supersession (nothing deleted):**
- N-59, N-60, N-61 and N-62(a) remain in force as bundled smoke tests. **N-67…N-74 are the release-blocking distinct tests for CH-19.**
- The CH-21 assertion in G-11's harness is now N-75 + G-12.
- R24 in A4.4 maps to N-75…N-78, P-27, G-12. The reserved "N-67 if Cursor prefers" in A4.4 is **void**; N-67 is now the subfolder duplicate.

## A5.5 Updated counts
| Type | After A4 | New in A5 | Total |
|---|---|---|---|
| must-FAIL | 66 | 12 (N-67…N-78) | 78 |
| positive | 26 | 2 (P-27, P-28) | 28 |
| no-gate-relaxed | 11 | 1 (G-12) | 12 |
| document check | 9 | 0 | 9 |
| **Total** | **112** | **15** | **127** |

**Traceability additions:**

| Requirement | Decision | Change | Tests |
|---|---|---|---|
| R11 (release-blocking) housing components rejected without contaminating caches or results | priorities file; resolution (b) | CH-19 | N-67…N-74, P-28 (harness), plus N-59…N-66, P-25, P-26, G-11 |
| R24 (release-blocking) a real protected-output gate; rejection before any write | priorities file | CH-21 (+ the CH-08 reorder of `run_matched_national.py:53-57`) | N-75…N-78, P-27, P-28, G-12 |
| R25 per-test evidence mapping (PASS/FAIL/BLOCKED) | priorities file | — | `findings/methods-reviewer/CANDIDATE_REVIEW_TEMPLATE.md` |

## A5.6 Dated note (2026-10-22): baseline status
**fb58ddc is the VERIFIED Git baseline:** all five manifests recompute, 35/40/24/15/10 entries with 0 mismatches, and the snapshot's own verifiers pass (`findings/methods-reviewer/2026-10-22_fb58ddc_v1_verification.md`).
- **The comparison with the original release ZIPs is BLOCKED.** The external R2.4 package and the pillar Lock_v1 ZIPs are not available. **The original distribution bytes are therefore NOT verified.**
- No test in this file (including P-23, P-24 and DC-06) may be reported as verifying distribution bytes. They verify Git objects only.
- This is consistent with the priorities file: "Do not claim original distribution-byte verification is complete."
