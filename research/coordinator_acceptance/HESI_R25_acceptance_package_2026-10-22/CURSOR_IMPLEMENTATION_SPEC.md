# DRAFT: CURSOR IMPLEMENTATION SPEC, D-05 remediation (base 273406208abe)
> **DRAFT. Not approved for implementation until the Engineer's candidate passes the acceptance tests in `ACCEPTANCE_TESTS.md` (49 original IDs + 37 in Addendum A2 = 86), and Kevin approves.**
> - **AI methods review, not independent human peer review.** This is a specification for Kevin and Cursor, not an approval.
> - Author: Methods Reviewer (Grok Bot). Written 2026-10-22, about 06:25 UTC.
> - Base: `273406208abe439cbad960567f32822b870c43b5` (Core R2.5). All line references are at this commit (VERIFIED with `git show 273406208abe:<file>`).
> - Governing records, both written by the Coordinator and cited as **recorded by the Coordinator as Kevin's decisions/answers** (not verified with Kevin):
>   - `decisions/2026-10-22_formal_governance_decisions.md`, sha256 `090a630665aeba727dc3002c95d2607bff8da3849123e2079c976350016828f8`;
>   - `decisions/2026-10-22_five_governance_answers.md`, sha256 `6af3bc51ed4a482186839dc38ce540ace37bfdb6867f47c53d31fcc73783a7a0`.
>   - Both hashes VERIFIED.
> - Labels: VERIFIED / HYPOTHESIS. **[K/C]** = only Kevin or Cursor can implement. Every change in §3 is **[K/C]**. The Engineer prepares the candidate patch and evidence in scratch only and never pushes (Coordination section of the decisions file).

## 1. Scope
**In scope:**
- D-05 option D: keep the original manifests; add versioned v2 manifests alongside them.
- PUMS ingestion hardening (F1_v2, rebased) as extended by D2.
- `verify_package` per D4.
- Explicit inputs per D5, in `run_joint`, `reproduce_from_raw`, `run_matched`, `run_matched_national` and the matched food-cache builder.
- Protected-output refusal.
- Pillar v2 manifests and a release verifier that checks them.
- `refresh_release_hashes.py` neutralized.
- Dev requirements (pytest).
- The BLS register correction (additive).
- The status corrections per Track E draft + D1.
- The acceptance-test suite.

**Out of scope (explicit exclusions):**
- **No FMR-schedule change of any kind.** The 2024 HUD FMR schedule is "NOT APPROVED yet" (formal Decision 2), and the Westchester W2 sensitivity is **unrun** (VERIFIED, `FMR_OUTCOMES.md` §4.3).
  - No change to `prepare_2024_cost_inputs.py` day weights or areas (`:104-108`, `:185-188`).
  - No change to `HISTORICAL_ALIGNMENT_PROTOCOL.md`.
  - No change to `research/historical_matched_baseline/outputs/*`.
  - The 2025-04-27 label correction is also excluded. It is metadata only (VERIFIED) and belongs to a separate erratum.
- No change to any economic formula, exclusion, weight, cost value, threshold, gate or status value.
- No replacement of 17.6839565%. No new published number.
- No commit, push, merge, PR or release (five answers, Implementation section).

### 1.1 Files that must NOT be touched (byte-identical before and after; tested by P-02, G-03, G-09 and §5)
| Group | Files (sha256 at 273406208abe, prefix; VERIFIED) |
|---|---|
| Frozen R2.4 results | `core_r24/results/national_R22/{common_cohort_results.csv 6778c312…, replicate_results.csv 6d42ff33…, audit.json 975cc72d…}`; `core_r24/results/rebuilt_from_raw/*`; `core_r24/results/synthetic/*` (all listed in v1) |
| Frozen root pilot | `results.csv`, `audit.json`, `manifest.json` |
| Matched-year record | every file in `research/historical_matched_baseline/results/matched2024_provisional/`, including `ARTIFACT_LOCK.json` `d8827804…` (14 files hashed), `RESEARCH_READINESS.json` `1369e287…` and `VALIDATION_GATES.json` `53decbd9…`; `research/historical_matched_baseline/outputs/*` (hashed in `REPRODUCER_HANDOFF.md:30-33`) |
| Locked inputs | `core_r24/inputs/*` (6 files in v1); `core_r24/PUMS_ARCHIVE_LOCK.json` `998c85b1…` |
| Original manifest (v1) | `core_r24/RELEASE_FILE_HASHES.json` `6cd769e0…` (state at 2734062; original fb58ddc state `49871df6…` lives in git history) |
| LOCK_REGISTER and pillar locks | `research/september2026_core_r2/LOCK_REGISTER.json` `be3388d7…`, `INTEGRITY_MANIFEST.json` `a0de5589…`, `SOURCE_HASHES.json` `29e8aa72…`, `housing/PACKAGE_MANIFEST.json` `5ecf44ae…`, `housing/LOCK_DECISION.json` `c5782a13…`, `transportation/SOURCE_HASHES.json` `e4fe0a48…`, `transportation/LOCK_REGISTER.json` `c7c203b6…` |
| Gates and decisions | `research/september2026_income_nowcast/{LOCK_DECISION.json 49c4d138…, reports/GO_NOGO.json 25c4bffd…, reports/VALIDATION_GATES.json 74e09fad…}`; `research/historical_matched_baseline/{VALIDATION_CRITERIA.json 181a1a1b…, FEASIBILITY_GO_NOGO.json 616dfa6b…, MATCHED_YEAR_READINESS.json 6ba5cbe1…}`; tolerances `core_r24/reproduce_from_raw.py:24,27` (`atol=1e-7, rtol=0`) |
| Evidence and history | existing lines of `ERRATA.txt`, `ITERATION_REGISTER.txt` (append-only), `ITERATION_NOTES.txt`; `research/september2026_income_nowcast/reports/*` (incl. `INCOME_NOWCAST_VALIDATION_REPORT.json`, `PHASE3_DATA_SOURCE_ACQUISITION_REPORT.json`); `core_r24/reproduction_runs/**`; git history |
| Pillar package code | `research/september2026_core_r2/**` code files are **not edited further**. The 3 files already changed at 2734062 (D-05 C2) are handled by v2 manifests only |

## 2. Approach: D-05 option D (approved in principle by formal Decision 3, as recorded)
- v1 stays as it is.
- New `*_v2.json` manifests are added **alongside** v1 and are never written over it.
- Every hash change is listed in an additive history file with old hash, new hash, commit and decision reference.
- The bare verification command keeps v1 semantics against the historical snapshot (D4). v2 is selected explicitly.
- Scientific definitions are unchanged. run_joint arithmetic is byte-neutral on defaults (VERIFIED earlier, D-05_DECISION §1.3).

## 3. Changes (all [K/C])
| ID | Files | Current behaviour at 273406208abe (VERIFIED by reading unless noted) | Required behaviour | Tests |
|---|---|---|---|---|
| CH-01 | `core_r24/verify_package.py` | `:5` reads the **working-tree** `RELEASE_FILE_HASHES.json`; `:6-10` stops at the first missing or mismatched file; no manifest selection; `:13-14` runs unit tests and `reproduce_from_raw.py --check-existing results/rebuilt_from_raw`; no handling of empty or malformed manifests (`json.loads` would raise, but `{}` → "PASS: all 0", VERIFIED for the F1_v2 variant) | **Bare command = v1 semantics against `V1_SNAPSHOT`** (D4): read the manifest and every listed file from `git show V1_SNAPSHOT:core_r24/<rel>`, or a pinned snapshot archive; never fall back to the working tree. v2 only via `--manifest RELEASE_FILE_HASHES_v2.json` (allowlist of exactly this name) **or** a separate `verify_package_v2.py`. Missing, empty, `{}`, malformed, partial (entry set ≠ pinned set) or mismatched manifests → exit≠0. Collect all mismatches before exiting. Print the manifest name, version and sha256. Keep `:13-14` steps in both paths | N-01…N-11, N-31, N-41…N-45, P-03, P-04, P-15…P-17, G-04, G-07 |
| CH-02 | NEW `core_r24/RELEASE_FILE_HASHES_v2.json`; NEW `core_r24/RELEASE_FILE_HASHES_HISTORY.json` | v2 exists only as a stale proposal (`F1_v2_manifest_v2.diff`, fails 2/41 at 2734062, VERIFIED) | v2 = hashes of the final candidate tree, including every changed script and v1 itself (`6cd769e0…`). HISTORY lists `reproduce_from_raw.py` c6783be3→6b41f2e0→(v2), `rebuild_raw_person_caches.py` d9a20f2e→97d51efa→(v2), `src/run_joint.py` 030cb0ae→a34951b1→(v2), the +3 e45eb87 entries, and the v1 file states 49871df6→4f6825d7→6cd769e0, each with its commit and decision reference. Pin the v2 sha256 in `verify_package.py` source and in ERRATA | N-19, N-21, P-04, P-17, §5 |
| CH-03 | `core_r24/tools/refresh_release_hashes.py` | `:5` reads and `:23` **writes `RELEASE_FILE_HASHES.json` in place** | Refuse to write any existing manifest (exit≠0). Optionally write a *new* file named `RELEASE_FILE_HASHES_v<N>.json` only if it does not exist | N-22 |
| CH-04 | `core_r24/tools/pums_archive.py`, `core_r24/rebuild_raw_person_caches.py`, `core_r24/reproduce_from_raw.py` (F1_v2 hardening rebased: `F1_v2_pums_ingestion_hardening_on2734062.diff`) | `rebuild_raw_person_caches.py:11` creates `--out` first; `:25-26` resumes path-keyed part checkpoints; `:45,:48` write caches; `:50-58` check basenames **after** writing. `pums_archive.py:50-70` checks only the required inner CSVs, not duplicates or extras; `:41-47` split pair by container hash | Per D2: accept (a) the split pair authenticated against `r24_locked_zip_sha256`, or (b) official `csv_pus.zip` by inner-CSV hashes. In both: required components, unique members, no unexpected CSVs, valid ZIP structure, complete coverage, lock self-hash, all checked **before** any directory or cache is created; content-keyed checkpoints with a COMPLETE marker; failed runs leave nothing reusable; test-lock override confined to the test harness | N-12…N-14, N-32…N-40, P-07, P-13, P-14, G-06 |
| CH-05 | `core_r24/tools/pums_archive.py:73-90` (housing) | Container hash, **or** (if it differs) any ZIP whose `psam_husa/b.csv` inner hashes match. No member-set check (D-05 loosened check) | Add the same member-set and structure checks as CH-04. That is a tightening (VERIFIED as no relaxation by construction). **Whether non-matching containers may be accepted at all remains a separate Kevin decision (G-02)**; D2 covers person archives only | G-02, N-36 (housing variant, TO BE WRITTEN) |
| CH-06 | `core_r24/reproduce_from_raw.py` (D5 official) | `:35` default `--output local_reproduction` (implicit); `:46` fixed geography and prices; no source manifest, cost vintage or method config arguments; `:52` creates the cache dir after source checks but writes into `--output` directly (no staging); protected paths not refused | Official mode: require `--source-manifest`, `--cost-vintage` (`R24_SEP2026`), `--method-config` and `--output`. Validate all of them plus protected-path refusal (all frozen paths in §1.1, subdirectories and symlinks) **before** any write. Stage, then publish atomically with audit | N-23, N-47…N-51, N-53, P-01, P-19 |
| CH-07 | `core_r24/src/run_joint.py` (formal Decision 2 conditions + D5) | `:26` defaults `transport_annual=7264.70`, `food_column='thrifty_2026sep'` and labels; no cost-vintage parameter; `:27-30` guards only `national_R22`; `:31` `out.mkdir` before reading inputs; the geography table has no vintage field (VERIFIED header) | Arithmetic **unchanged** (no edits to `:32-…` computations). Add a `cost_vintage` and `mode` input. Validate that the food column, transport, geography and prices declare the same vintage, unless an explicit cross-vintage selection is passed; refuse otherwise. Run all checks before `mkdir`. Guard every frozen path. Record every effective input, version, hash, choice and path in `audit.json` (additive keys only) | N-15, N-23, N-27…N-29, N-48, N-49, N-52, N-53, P-09…P-11, P-18, P-19, G-08 |
| CH-08 | `research/historical_matched_baseline/src/run_matched_national.py`, `run_matched.py` | **`run_matched_national.py:46` default `--out` = `results/matched2024_provisional` (the frozen record)**; `:50-52` refuses only `national_R22`; `:53` mkdir; **`:56` writes `INPUT_VALIDATION.json` (an ARTIFACT_LOCK-listed file) before validation can fail** (VERIFIED). `run_matched.py:35` default transport 6870.67; `:58` CLI default | Official mode requires `--out` (no default), refuses every frozen path, validates before writing, and passes explicit `cost_vintage=MATCHED_2024`, source manifest and method config through to run_joint. Dev mode default output must lie outside every frozen path | N-23, N-50…N-52, P-08 |
| CH-09 | `research/historical_matched_baseline/src/rebuild_matched_food_cache.py` | `:62` path-keyed checkpoint tag; `:66` resumes; `:73` reads **all** `psam_pus*` members (no duplicate or extra checks); no lock check | Reuse `pums_archive` validation (CH-04) and content-keyed checkpoints | N-16, N-17, N-39 |
| CH-10 | NEW `research/september2026_core_r2/LOCK_v2/{INTEGRITY_MANIFEST_v2, SOURCE_HASHES_v2, housing_PACKAGE_MANIFEST_v2, transportation_SOURCE_HASHES_v2}.json`; NEW release verifier (`tools/check_pillars.py` from `F3b_v2_check_wrapper_on2734062.diff`, or `research/september2026_core_r2/verify_release_v2.py`) | 4 manifests mismatch 3 files changed at 2734062; `verify_release.py:1-17` opens no manifest (VERIFIED). F3b_v2 is on HOLD (earlier report; not mentioned in either decisions file) | v2 pillar manifests list `housing/verify.py` `7145ea91…`, `transportation/run_standard.py` `70a5262c…`, `transportation/test_standard.py` `95302c98…`, with v1 unchanged. The verifier checks v1 (against the snapshot) and v2 (working tree), fail closed. The locked `verify_release.py` is **not edited** | N-20, N-24…N-26, N-46, P-05 |
| CH-11 | NEW `TOOLS_MANIFEST.json` (repo root), or include tools in a v2 manifest | `tools/check_pillars.py`, `tests/test_check_pillars.py` and `.gitignore` sit outside `core_r24`, so no manifest covers them (VERIFIED) | Hash-cover every verifier and acceptance-test file | **none yet: GAP T-1** |
| CH-12 | NEW `requirements-dev.txt` (`pytest`) | pytest missing; `tests/test_synthetic_pipeline.py` errors and `tests/test_hesi.py` collects 0 (Engineer's step 5; HYPOTHESIS for me, seal VERIFIED) | Add pytest with a version pin, e.g. `pytest==9.1.1` as tested by the Engineer | P-06 |
| CH-13 | `research/september2026_income_nowcast/SOURCE_REGISTER.json:6`; `ERRATA.txt` (append) | Register says `01eee553…`; committed file is `9349e525…` (VERIFIED). The reports at `INCOME_NOWCAST_VALIDATION_REPORT.json:1702` and `PHASE3_DATA_SOURCE_ACQUISITION_REPORT.json:36` cite the same stale value | Additive ERRATA entry covering all 3 citations. In the register, add a field with the corrected hash and keep the old value visible (D-05 C4-A5). **Do not edit the two reports** | **none in the suite: GAP T-2** |
| CH-14 | Status docs per `TRACK_E_CORRECTIVE_DRAFT.md` **as amended by its D1 note** | Track E NO-GO lines replaced in place at 2734062; stale lines `STATUS.txt:52`, `README.md:69` | Additions only, using `EXTERNALLY_INDEPENDENTLY_REPRODUCED: NO` plus optional `REPRODUCTION_REVIEW: PENDING` (D1) | DC-01, DC-02, G-05, G-09 |
| CH-15 | NEW `tests/acceptance/**`, `tests/acceptance/REFERENCE_DIGESTS.py`, `tests/acceptance/NON_SCIENTIFIC_TOOLS.txt`, fixtures, `no_gate_relaxed.py` (+ `approved_exceptions.json`, Kevin-signed) | Absent | Implement every TO BE WRITTEN test | all |
| CH-16 | NEW D-05 closure record (`decisions/` or ERRATA entry) and NEW C9 milestone document | Absent | Per D3: lists the passing engineering, provenance and AI-reproduction tests; C9 is a separate open milestone; publication stays NO-GO | DC-03 |

Already implemented at 2734062, so no new change is needed: F3a (`--write-tracked-docs`, `prepare_2024_cost_inputs.py:371,568`) and F5 (VERIFIED, FINAL_PLAN Update 2).

## 4. The nine D3 conditions (formal Decision 3, verbatim) with C9 split out
| Condition | Where met | Closure gate for D-05? |
|---|---|---|
| 1. Historical manifests and prior release evidence remain immutable | §1.1, CH-02, CH-03 | yes |
| 2. Verification against a missing, empty or mismatched applicable manifest must FAIL | CH-01, CH-10 | yes |
| 3. No direct-run bypass of scientific locks | CH-04, CH-07, CH-09; N-18 inventory | yes |
| 4. No unreviewed in-place hash replacement | CH-02 (HISTORY), CH-03; §5 | yes |
| 5. Protected outputs are rejected before creating caches or intermediates | CH-06…CH-09 | yes |
| 6. All applicable pillar and core manifests are checked | CH-01, CH-10, CH-11 | yes |
| 7. The original and v2 verification paths are explicitly distinguished | CH-01 (D4) | yes |
| 8. The final patched code reproduces the frozen R2.4 calculation and all 80 replicates | P-01, P-02, P-07, P-11, P-19 | yes |
| 9a. The 2024 matched-year calculation is reproduced (AI-operated, on the final code) and its FMR sensitivity investigated | P-08, P-12, FMR_OUTCOMES.md | yes. AI-operated computational reproduction is sufficient for D-05 closure per D3 ("D-05 may close after … AI-operated computational reproduction pass") |
| **9b. MILESTONE M-C9 (separate):** human-operated independent reproduction and external methodological review | DC-03 (milestone document); `ITERATION_REGISTER.txt:10` definition | **no**. Its own milestone (D3). Until met: `EXTERNALLY_INDEPENDENTLY_REPRODUCED: NO`, `SCIENTIFICALLY_VALIDATED: NO`, formal publication NO-GO |

- The W2 FMR sensitivity is still unrun.
- "FMR sensitivity investigated" (9a) is met as a documented investigation **with an open item**. Kevin decides whether 9a requires the W2 run before D-05 closes. HYPOTHESIS: the condition's wording does not settle this.

## 5. Expected effect on locked and frozen results: none
- **Expected:** zero byte change to every file in §1.1. No metric changes. R2.4 national within `atol=1e-7, rtol=0` on 6 metrics × 4 fields and 80/80 replicates (`reproduce_from_raw.py:24,27`; README `:95`).
- **Evidence so far:**
  - VERIFIED: the F1_v2 stack at e45eb87 gave max diff 0.0 against pre-patch outputs, caches `9ca1e3d2…`/`4e7c8dbb…`.
  - VERIFIED: the run_joint refactor is byte-neutral.
  - HYPOTHESIS until the final candidate is run: the full candidate.
- **Proof test (run after applying the candidate; all must hold):**
```bash
BASE=273406208abe439cbad960567f32822b870c43b5
# 1. No tracked frozen file changed (empty output required)
git diff --name-only $BASE -- core_r24/results results.csv audit.json manifest.json \
  research/historical_matched_baseline/results research/historical_matched_baseline/outputs \
  core_r24/inputs core_r24/PUMS_ARCHIVE_LOCK.json core_r24/RELEASE_FILE_HASHES.json \
  research/september2026_core_r2/LOCK_REGISTER.json research/september2026_core_r2/INTEGRITY_MANIFEST.json \
  research/september2026_core_r2/SOURCE_HASHES.json research/september2026_core_r2/housing/PACKAGE_MANIFEST.json \
  research/september2026_core_r2/housing/LOCK_DECISION.json research/september2026_core_r2/transportation/SOURCE_HASHES.json \
  research/september2026_core_r2/transportation/LOCK_REGISTER.json research/september2026_income_nowcast/LOCK_DECISION.json \
  research/september2026_income_nowcast/reports research/historical_matched_baseline/VALIDATION_CRITERIA.json \
  research/historical_matched_baseline/FEASIBILITY_GO_NOGO.json research/historical_matched_baseline/MATCHED_YEAR_READINESS.json
# 2. Byte check of the same set, including untracked/ignored writes
python -m pytest -q tests/acceptance/test_frozen.py::test_frozen_files_unchanged          # P-02
# 3. History and evidence files: additions only
git diff --numstat $BASE -- ERRATA.txt ITERATION_REGISTER.txt ITERATION_NOTES.txt STATUS.txt README.md | awk '$2!=0{exit 1}'
# 4. Gates, thresholds and assertions not relaxed
python tests/acceptance/no_gate_relaxed.py . fb58ddc HEAD tests/acceptance/approved_exceptions.json   # G-01
python -m pytest -q tests/acceptance/test_gates.py                                                  # G-02..G-09
# 5. Reproduction on the final code
python core_r24/reproduce_from_raw.py --mode official --housing $CENSUS/csv_hus.zip --person-official $CENSUS/csv_pus.zip \
  --source-manifest core_r24/RELEASE_FILE_HASHES_v2.json --cost-vintage R24_SEP2026 --method-config <cfg> --output $(mktemp -d)/r24   # P-01/P-19
```
- The flags in item 5 are proposed names (HYPOTHESIS); Cursor finalizes them.

## 6. Traceability
| Requirement | Decision(s) | Change | Tests |
|---|---|---|---|
| R1 v1 manifests/evidence immutable | formal D3 c1; five-answers Implementation | CH-02, CH-03, §1.1 | N-19…N-22, N-30, P-02, P-03, G-03 |
| R2 fail closed on missing/empty/malformed/mismatched manifests | formal D3 c2; D4 | CH-01, CH-10 | N-01…N-10, N-41, N-43, N-45, N-46 |
| R3 no direct-run lock bypass | formal D3 c3 | CH-04, CH-07, CH-09 | N-12…N-18 |
| R4 no unreviewed in-place hash replacement | formal D3 c4 | CH-02, CH-03 | N-19…N-22, §5.2 proxy |
| R5 protected outputs refused before writes; dev defaults never write frozen | formal D3 c5; D5 | CH-06…CH-09 | N-15, N-16, N-23, N-30, N-51, N-52 |
| R6 all pillar and core manifests checked | formal D3 c6 | CH-01, CH-10, CH-11 | N-05, N-06, N-20, N-24…N-26, N-46, P-05 (CH-11: **GAP T-1**) |
| R7 v1/v2 paths distinguished; bare = v1 snapshot | formal D3 c7; D4 | CH-01 | N-11, N-31, N-41, N-42, N-44, P-15…P-17, G-04, G-07 |
| R8 frozen R2.4 + 80 replicates reproduce | formal D3 c8 | all | P-01, P-02, P-07, P-11, P-19 |
| R9a matched-year AI reproduction + FMR investigation | formal D3 c9; D3 | — | P-08, P-12 |
| R9b human independent reproduction milestone | D3 | CH-16 | DC-03 (presence only) |
| R10 person archive validation (split or official; 7 rejection classes) | D2 | CH-04 | P-13, P-14, N-32…N-40, G-06 |
| R11 housing archive validation | (none: D2 is person-only) | CH-05 | G-02, N-36 housing variant (TO BE WRITTEN). **Needs a Kevin decision** |
| R12 run_joint vintages isolated, explicit selections, no cross-contamination | formal D2 | CH-07 | N-27…N-29, P-09, P-10 |
| R13 official runs require explicit inputs; dev runs record everything | D5 | CH-06…CH-08 | N-47…N-53, P-18, P-19, G-08 |
| R14 status labels per D1, no promotion; publication NO-GO | D1; D3; formal D1 | CH-14 | DC-01, DC-02, G-05, G-09 |
| R15 no gate relaxed | formal D3 (implied); five answers "No silent gate relaxation" | all | G-01…G-09 |
| R16 dependency completeness | (requirement 8, earlier memo; not in either decisions file) | CH-12 | P-06 |
| R17 BLS register hash | (requirement 8; F2) | CH-13 | **GAP T-2: no test** |
| R18 no FMR-schedule change | formal D2 | exclusion §1 | P-02 (outputs and matched record unchanged), G-01 (`prepare_2024_cost_inputs.py` assertions); **no dedicated test: GAP T-3** |
| R19 no tools/verifier code left uncovered by a manifest | earlier finding MR-R2-1 | CH-11 | **GAP T-1** |

**Gaps:**
- **T-1 (requirement with no test):** CH-11 tools manifest. Proposed: `test_manifest_immutability.py::test_tools_manifest_covers_verifiers` (TO BE WRITTEN). It must fail if any file under `tools/` or `tests/acceptance/`, or `.gitignore`, is missing from a manifest or mismatched.
- **T-2 (requirement with no test):** BLS register. Proposed: `test_bls_register.py::test_register_matches_committed_file`. sha256 of `factor_sources/BLS_ANNUAL_FACTORS.json` must equal the register's corrected field, and the stale value must remain recorded.
- **T-3 (requirement with no test):** FMR exclusion. Proposed: `git diff --quiet $BASE -- research/historical_matched_baseline/src/prepare_2024_cost_inputs.py research/historical_matched_baseline/HISTORICAL_ALIGNMENT_PROTOCOL.md research/historical_matched_baseline/outputs`.
- **Tests with no requirement:** none found. Every N, P, G and DC ID maps to at least one requirement above (VERIFIED by cross-check against the A2.2 traceability list and the §6 matrix of ACCEPTANCE_TESTS.md).

## 7. Items only Kevin or Cursor can implement or decide
1. **[K]** Choose `V1_SNAPSHOT` for D4. The AI recommendation is fb58ddc, the original release; e45eb87 and 2734062 are recorded as history. The bare-command expected output in P-15 depends on this choice.
2. **[K]** Decide whether the matched-year runs count as "official/locked research executions" under D5. This affects how P-08 is run; the committed files are unchanged either way.
3. **[K]** G-02: whether a non-matching housing container may be accepted by inner hashes (the D-05 loosened check). D2 does not cover housing.
4. **[K]** P-13: supply the original `HESI_Person_Part_1/2.zip` for the split-pair positive test. Or decide whether split archives may be authenticated by inner hashes, which would be a gate change.
5. **[K]** Whether condition 9a needs the W2 FMR sensitivity run before D-05 closes.
6. **[K]** Sign `tests/acceptance/approved_exceptions.json`, including the G-01 entry for the removed `len(person_zips)!=2` check, justified under D2 only if N-32…N-40 pass.
7. **[K]** Whether F3b_v2 (`tools/check_pillars.py`) is taken off HOLD as the CH-10 verifier, or replaced by a new `verify_release_v2.py`.
8. **[C]** Implement CH-01…CH-16 in Cursor (canonical environment) from the Engineer's scratch candidate. **[K]** Commit and push only after separate authorization.

## 8. Conflicts with gates, locks or earlier findings (explicit)
1. **D4 vs immutable-history condition.** If "v1" meant the current `RELEASE_FILE_HASHES.json` (2734062, `6cd769e0…`), the bare command would certify the two in-place rewrites (D-05) as the original release. That conflicts with formal D3 conditions 1 and 4. Resolved only by choosing `V1_SNAPSHOT` = fb58ddc (item 7.1).
2. **D1 vs formal Decision 1.** `EXTERNALLY_REPRODUCED: PENDING` is replaced by the existing `EXTERNALLY_INDEPENDENTLY_REPRODUCED: NO` (+ optional `REPRODUCTION_REVIEW: PENDING`). The Track E draft has been noted accordingly. This is governance wording; there is no scientific conflict.
3. **D3 (D-05 closes, publication NO-GO).** Consistent with `RESEARCH_READINESS.json` (`publish_17_7_percent: NO-GO`, `provisional_public_research_release: NO-GO`; VERIFIED unchanged).
   - The readiness file's precondition "Independent computational reproduction … with hashed outputs" (`RESEARCH_READINESS.json:11`) is **not** satisfied by D-05 closure. It sits in milestone M-C9.
   - No conflict, provided no document presents D-05 closure as meeting it.
4. **D5 vs the existing matched-year code.** `run_matched_national.py:46` defaults the output to the frozen record directory, and `:56` writes an ARTIFACT_LOCK-listed file before validation (VERIFIED). A default run today would overwrite `INPUT_VALIDATION.json` in the frozen record. This is a **live data-integrity hazard** at 273406208abe (no evidence it has happened: ARTIFACT_LOCK 14/14 match, VERIFIED earlier). CH-08 fixes it.
5. **D2 and G-01.** The removed two-archive check is not "restored" literally; D2 explicitly rejects "an obsolete requirement for two ZIP containers". The replacement must be equivalent or stronger, which N-32…N-40 test. Without them, the G-01 violation stands as a gate relaxation.
6. **Formal Decision 2 vs the FMR schedule.** The spec excludes any schedule change. Nothing here conflicts. The W2 gap is recorded, not resolved.

---
## Dated note N-2026-10-22T05:40Z: Coordinator rulings on open items (c) and (d) (additive)

Source: a message from the HESI Research Coordinator on 2026-10-22 at about 05:40Z. These are **interpretations by the Coordinator under existing decisions**. They are **not** Kevin's own words. They stay provisional until Kevin confirms them, and nothing above this note is changed.

- **(c) G-01, removal of the "both archives required" check.** Coordinator's ruling: if the D2 tests (N-32 to N-53 and P-13/P-14 as applicable) pass, the protection counts as restored, and no separate exception is needed because D2 authorizes that path. Reviewer note (HYPOTHESIS): this reading is consistent with the D2 text, but it is still an inference that D2 also waives G-01. P-13 cannot be executed on this box until Kevin's split person ZIPs are available. Until P-13 passes, G-01 stays **OPEN**.
- **(d1) Scope of D5.** Coordinator's ruling: matched-year runs that create or feed locked results are "official" under D5. Under this ruling, `run_matched_national.py` is in the scope of CH-08 and the official-mode tests: it must refuse an implicit `--out`, manifest, cost vintage and method config.
- **(d2) Condition 9a.** Coordinator's ruling: 9a requires the C-W2 FMR sensitivity run (Westchester at the NY FY24 FMR, $2,752) under D3 condition 9. D-05 cannot close until C-W2 has been run and recorded. This **does not** approve any change to the FMR schedule; the exclusion above stands.
- **(d3) F3b_v2.** Coordinator's ruling: it stays on HOLD and is not to be used as the pillar verifier in this pass.
- **Still with Kevin:** (a) which v1 snapshot is the historical original (the reviewer recommends `fb58ddc`) and (b) the housing-archive check.

Spec status: **DRAFT**. It is not approved for implementation.

---

## CH-17 (added 2026-10-22, about 07:00 UTC): FY2025-revised effective-date label, 2025-04-27 → 2025-04-28 **[K/C]**
> **AI methods review, not independent human peer review.** Additive item; CH-01…CH-16 are unchanged.
> - **Authority:** `decisions/2026-10-22_hud_contact_authorization.md`, sha256 `53bc916d92955a0e481d389787a4152e85772887fc9e76541c78d0006a639836` (VERIFIED; matches its `.sha256`). It is **recorded by the Coordinator as Kevin's order**: "correct the April 27/28 documentation without altering historical numerical results".
> - **Source of the correct date:** 90 FR 14158, "The revised FY 2025 FMRs are effective on April 28, 2025" (VERIFIED in the Data Scout's sealed `fr/govinfo_FR-2025-03-28_2025-05345.htm`, sha256 `04c15015…`, and in my own fetch).
> - **Scope note:** this item revises my §1 exclusion of the label fix. The fix is now ordered; it is a label correction, not an FMR-schedule change. The schedule exclusion stands.

### CH-17.1 Line references at 273406208abe (all VERIFIED with `git show 273406208abe:<file> | sed -n <n>p`; all four are correct as given)
| # | File:line | Current text | Kind |
|---|---|---|---|
| 1 | `research/historical_matched_baseline/HISTORICAL_ALIGNMENT_PROTOCOL.md:22` | `   - FY2025 **revised** (effective 2025-04-27) is after calendar 2024 and is **not** in the default.` | prose |
| 2 | `research/historical_matched_baseline/src/prepare_2024_cost_inputs.py:83` | `        "effective": "2025-04-27",` inside `HUD_FILES["fy25_revised"]` (`:80-86`) | **a data label, not a comment**. It is copied into the generated source register by `:388` (`rec.update({k: meta[k] …})`) and written at `:569`. It is not read by any computation: day weights are constants `:105-108`, used at `:185-188` |
| 3 | `research/historical_matched_baseline/SOURCE_REGISTER.json:74` | `      "effective": "2025-04-27",` (the `fy25_revised` record) | generated metadata (output of #2 via `--write-tracked-docs`) |
| 4 | `ITERATION_NOTES.txt:683` | `  effective 2025-04-27` (under "HUD FY25 revised FY25_FMRs_revised.xlsx (archived; not in default 2024 schedule)", `:681-683`) | history |

- `git grep -n '2025-04-2[78]\|April 2[78]' 273406208abe` finds exactly these four occurrences, all `2025-04-27`. `2025-04-28` appears nowhere.
- **Hash-lock status (VERIFIED):** none of the four files' sha256 values appears in any manifest at 2734062 (`git grep -l <sha256>` returns nothing). The values are:

| File | sha256 at 2734062 |
|---|---|
| SOURCE_REGISTER.json | `f13565156df8…` |
| prepare_2024_cost_inputs.py | `27df706e1a4f…` |
| HISTORICAL_ALIGNMENT_PROTOCOL.md | `a277a39fd0b9…` |
| ITERATION_NOTES.txt | `4bb38092bed6…` |

- Nor do they appear in `ARTIFACT_LOCK.json`, `SOURCE_MANIFEST.json` or `REPRODUCER_HANDOFF.md`, which hash only inputs and outputs.

### CH-17.2 Required changes
- **#1 Protocol `:22`.** Change `2025-04-27` to `2025-04-28` on that line only, and append a dated sentence after it: "(Corrected 2026-10-22 from 2025-04-27 per 90 FR 14158; label only, no 2024 value affected.)" No other line changes.
- **#2 `prepare_2024_cost_inputs.py:83`.** Change the string value only, to `"effective": "2025-04-28",`. Optionally add a trailing comment `# 90 FR 14158; corrected 2026-10-22`. No other line changes. No logic change.
- **#3 `SOURCE_REGISTER.json:74`.** Change this one value only, by a direct single-line edit. **Do not regenerate the file with `--write-tracked-docs`**: regeneration could change other fields (HYPOTHESIS; it re-records file metadata). The diff must be exactly one line.
  - If Kevin prefers to keep the original value visible, add a sibling key `"effective_as_recorded_2026_10_21": "2025-04-27"` in the same object. That is a 2-line diff, also acceptable.
- **#4 `ITERATION_NOTES.txt`.** Leave **`:683` unchanged**. Append at end of file:
```
2026-10-22 correction (label only): ITERATION_NOTES line 683 records "effective 2025-04-27" for HUD FY25 revised
FY25_FMRs_revised.xlsx. The Federal Register date is 2025-04-28 (90 FR 14158: "The revised FY 2025 FMRs are
effective on April 28, 2025"). HUD's FMR data page labels the file "Effective April 27, 2025". The FY2025
revised file is outside calendar 2024 and not in the default schedule; no 2024 number changes. Line 683 is
kept as written. See ERRATA (CH-17).
```
- **ERRATA.txt:** append an entry listing the four locations, the old and new value, and the source.
- **Manifests (option D):**
  - None of these files is in v1 (VERIFIED), so nothing in v1 may be touched. **No in-place replacement anywhere.**
  - The new hashes of #1–#3, and #4 if covered, go into the **v2 path only**, with old→new pairs in `RELEASE_FILE_HASHES_HISTORY.json` (or the Track E / historical-baseline equivalent).
  - Coverage gap: **no manifest covers `research/historical_matched_baseline/src/` or its docs** (VERIFIED). New gap **T-4**, closed by adding these files to a v2 manifest (e.g. `research/historical_matched_baseline/MANIFEST_v2.json`) and testing it (DC-05).
- **Explicitly not changed:**
  - any output CSV or JSON in `research/historical_matched_baseline/outputs/`;
  - `matched2024_provisional/**`, incl. `REPRODUCER_HANDOFF.md`;
  - `MATCHED_YEAR_READINESS.json` (it does not contain the date; VERIFIED by `git grep`);
  - day weights; the FMR schedule.

### CH-17.3 Acceptance (proof that no numerical output changes)
- **Primary criterion: patched vs unpatched byte-identity, same environment** (P-20, P-21). Run `prepare_2024_cost_inputs.py` and `run_matched_national.py`, with explicit scratch `--out`, on the base tree and on the patched tree with the same venv and thread settings. Every numeric output must be **byte-identical** between the two.
  - This is stricter than ARTIFACT_LOCK's 1e-7 tolerance.
  - Comparison with the committed author outputs uses the lock tolerance instead. AI reruns differ from the author's bytes by up to about 1.7e-10 even unpatched (VERIFIED in `evidence_2734062_step4_w2`, alternative scenarios), so byte-identity to the *committed* files cannot be the criterion.
- **Frozen set:** ARTIFACT_LOCK 14/14 (`d88278045e3e…`) and every §1.1 file unchanged after the patch and the runs (P-22).
- **Diff scope:** exactly the declared lines change, and ITERATION_NOTES has additions only (N-55, N-56).
- **No v1 or pillar manifest touched** (N-54).
- Tests: N-54…N-56, P-20…P-22, G-10, DC-04, DC-05 (ACCEPTANCE_TESTS Addendum A3).

### CH-17.4 Traceability (additive rows to §6)
| Requirement | Decision | Change | Tests |
|---|---|---|---|
| R20 April 27/28 label corrected without altering numerical results | HUD-contact record ("correct the April 27/28 documentation without altering historical numerical results") | CH-17 | N-55, N-56, P-20…P-22, G-10, DC-04 |
| R21 label-fix hashes via v2 only; v1 untouched | formal D3 c1, c4; option D | CH-17, CH-02 | N-54, DC-05 |
| R22 coverage of historical-baseline src/docs by a manifest (gap T-4) | formal D3 c6 | CH-17 (MANIFEST_v2) | DC-05 |

### CH-17.5 HUD-contact authorization (noted, not acted on)
- The record authorizes **contacting HUD**, through the appropriate official HUD channel, with a narrowly scoped professional research inquiry. Its question: for 2024-10-01 to 2024-12-31, whether Westchester County's applicable FMR is its separately published FY2024 FMR ($2,352 2BR) or the New York HUD Metro FY2024 FMR ($2,752 2BR). It asks HUD to identify the controlling notice, effective-date rule, historical dataset or other authoritative documentation.
- Conditions: no private data; no claimed HUD affiliation; retain the exact question, date, recipient, response and links; if direct contact is unavailable, prepare the inquiry and the channel without claiming it was sent. The Coordinator's note says the draft is shown to Kevin, who presses Send.
- **I have not contacted HUD and will not.** The record does not assign the contact to me, and my instructions exclude it.
- **Label collision (VERIFIED by reading the record):** the record's inquiry labels A = $2,352 and B = $2,752. Those are the Data Scout's **W1 and W2**. In the team's sensitivity naming, reading A = W1, but **reading B = W0 ($2,580, FY25 original)**, and $2,752 is **C-W2**. The same record then asks to "record the original, Reading A, Reading B and NY FY2024 cases separately", using the team's naming.
  - Any HUD inquiry text should use "$2,352 (Westchester FY2024 SEA)" and "$2,752 (NY HMFA FY2024)" explicitly, not A/B.

---

# FINAL-FOR-CURSOR (pending candidate verification), dated 2026-10-22, written about 06:25 UTC
> **This section supersedes the DRAFT text above, which is kept unchanged as history.** Where they differ, this section governs. Status: **final for Cursor, pending verification of the Engineer's candidate against `ACCEPTANCE_TESTS.md` (112 IDs after Addendum A4).** Not approved for commit or push: that needs separate authorization by Kevin.
> - **AI methods review, not independent human peer review.** These are recommendations for Kevin and Cursor, not approvals. Labels: VERIFIED / HYPOTHESIS. **[K]** = Kevin only, **[C]** = Cursor (canonical environment), **[K/C]** = either.
> - Base: `273406208abe439cbad960567f32822b870c43b5`. Line references are at this commit unless stated.
> - **Governing records, all written by the Coordinator** (hashes VERIFIED with `sha256sum` against their `.sha256` companions):

| File | sha256 | Cited as |
|---|---|---|
| `decisions/2026-10-22_formal_governance_decisions.md` | `090a630665aeba727dc3002c95d2607bff8da3849123e2079c976350016828f8` | recorded by the Coordinator as Kevin's decisions |
| `decisions/2026-10-22_five_governance_answers.md` | `6af3bc51ed4a482186839dc38ce540ace37bfdb6867f47c53d31fcc73783a7a0` | recorded by the Coordinator as Kevin's answers |
| `decisions/2026-10-22_hud_contact_authorization.md` | `53bc916d92955a0e481d389787a4152e85772887fc9e76541c78d0006a639836` | recorded by the Coordinator as Kevin's order |
| `decisions/2026-10-22_spec_questions_resolved.md` | `9e6f1b757e6c7424dc23f4b53466811e194a1e2b3e26707499bb360352f96800` | recorded by the Coordinator as Kevin's resolution |

> **What the resolution settles:**
> - **(a)** v1 = fb58ddc. Verified **PASS with documented earlier changes** (`findings/methods-reviewer/2026-10-22_fb58ddc_v1_verification.md`).
> - **(b)** Housing archives get validation equivalent to or stronger than person archives.
> - The HUD investigation is a separate methodological track and **must not block** Part 1.
> - All four FMR sensitivity cases are kept, the provisional result is unchanged, and formal publication stays NO-GO.
>
> **Items resolved by that file** (no longer open): DRAFT §7 items 1 and 3; §8 conflict 1; the R11 "Needs a Kevin decision" note; the "Still with Kevin: (a) … (b)" line in the 05:40Z note. See ACCEPTANCE_TESTS A4.1.

## PART 1: Release-integrity engineering blockers (for Cursor) [C]
These block D-05 closure. **None of them changes a formula, input, exclusion, weight, cost value, threshold, gate value, status label or frozen file** (expected effect: zero bytes in DRAFT §1.1; proof in DRAFT §5 plus P-22 and N-54). Details for CH-01…CH-17 are in DRAFT §3 and CH-17; where noted, this table refines them.

| CH | Files (lines at 2734062) | Required change (short) | Tests | Status of Engineer candidate (`integrity_v2/`) |
|---|---|---|---|---|
| CH-01 + **CH-18** | `core_r24/verify_package.py:5-15` | Bare command = v1 semantics against the **fb58ddc snapshot** (**CH-18**: pin commit `fb58ddc045976d844c6da1fca99ed1f9f108bb85`, manifest sha256 `49871df6…` and git blob `6e560d6b82…` as source constants). Run the hash pass **and** the `:13-14` regression steps on snapshot bytes and code, never on the working tree. v2 only via an allowlisted explicit selection or a separate entry point. Fail closed on a missing, empty, `{}`, malformed, partial or mismatched manifest. Collect all mismatches. Print manifest name, version and sha256 | N-01…N-11, N-31, N-41…N-45, **N-57, N-58**, P-03, P-04, P-15…P-17, **P-23, P-24**, G-04, G-07 | `10_verify_package_manifest_v1_default_v2_explicit.diff` exists; not yet verified by me against P-23/N-57/N-58 (HYPOTHESIS) |
| CH-02 + **CH-18** | NEW `core_r24/RELEASE_FILE_HASHES_v1_fb58ddc.json` (verbatim), `…_v2.json`, `…_HISTORY.json` | v1 copy byte-identical to fb58ddc's blob (VERIFIED for the Engineer's `09_…diff` header: blob `6e560d6b82…`). **HISTORY must start at d658c08** (`c5ac44d0…`, 34 entries) and record the eec7c46 refresh (6 entry changes) and the pre-fb58ddc ITERATION_REGISTER/NOTES edits (findings §2, §5). The current `09_…diff` starts at fb58ddc and **fails DC-06** (VERIFIED by reading) | N-19, N-21, P-04, P-17, **DC-06** | partial |
| CH-03 | `core_r24/tools/refresh_release_hashes.py:5,23` | Never overwrite any existing manifest | N-22 | `11_…diff` exists (not verified by me) |
| CH-04 | `core_r24/tools/pums_archive.py`, `rebuild_raw_person_caches.py`, `reproduce_from_raw.py` | D2 person-archive validation; content-keyed checkpoints; validate before any write | N-12…N-14, N-32…N-40, P-07, P-13, P-14, G-06 | `01`, `02`, `03` diffs |
| ~~CH-05~~ → **CH-19** | `core_r24/tools/pums_archive.py:73-90`; `core_r24/src/run_joint.py:44-45`; `research/historical_matched_baseline/src/validate_matched_inputs.py:103`; `run_matched.py` (calls `run_joint.run`) | **CH-19 supersedes CH-05.** Housing validation per resolution (b), adapted to the real structure: exactly `psam_husa.csv` and `psam_husb.csv` (+ optional `ACS2024_PUMS_README.pdf`); no duplicates (case-insensitive, any folder); no other CSV or unexpected member; inner sha256 checked **even when the container matches**; lock self-hash; ZIP/CRC/header structure (241 columns incl. the `run_joint.py:43` columns); coverage (51 STATE codes, 1,631,969 rows, anchored by inner hash and `raw_rows`); **run_joint and run_matched read only the verified member list** (today `run_joint.py:45` re-selects every `psam_hus*`, VERIFIED probe); all checks before any directory or cache; nothing reusable after failure. Container policy follows A4.5 (inner-hash acceptance of an exact member set as the D2(b) analogue, or official-container-only; Cursor implements one explicitly) | **N-59…N-66, P-25, P-26, G-11** (supersede G-02, N-36-housing) | `01_…diff:577-580` adds `_verify_inner` and a member list to housing (VERIFIED by reading); member-set strictness, the read binding and coverage are not yet shown (HYPOTHESIS until tests run) |
| CH-06 | `core_r24/reproduce_from_raw.py:35,46,52` | D5 official mode: explicit inputs, protected-path refusal, staging and atomic publish | N-23, N-47…N-51, N-53, P-01, P-19 | `04_output_guard_F6_folded.diff` |
| CH-07 | `core_r24/src/run_joint.py:26-31` | Vintage isolation; explicit selection; checks before `mkdir`; additive audit keys; arithmetic unchanged | N-15, N-23, N-27…N-29, N-48, N-49, N-52, N-53, P-09…P-11, P-18, P-19, G-08 | pending |
| CH-08 | `research/historical_matched_baseline/src/run_matched_national.py:46,50-56`; `run_matched.py:35,58` | Official-mode `--out` required; refuse frozen paths; validate before writing (live hazard: the `:46` default is the frozen record, VERIFIED) | N-23, N-50…N-52, P-08 | `04` diff (partly) |
| CH-09 | `research/historical_matched_baseline/src/rebuild_matched_food_cache.py:62,66,73` | Reuse CH-04 validation and content-keyed checkpoints | N-16, N-17, N-39 | `05_…diff` |
| CH-10 | NEW `research/september2026_core_r2/LOCK_v2/*` + a release verifier that checks v1 (snapshot) and v2. `verify_release.py` is **not** edited | Pillar v2 manifests for the 3 changed scripts. **F3b_v2 (`tools/check_pillars.py`) stays on HOLD** (Coordinator ruling d3), so the verifier must be a separate `verify_release_v2.py` | N-20, N-24…N-26, N-46, P-05 | `13_pillar_LOCK_v2_verify_release_v2.diff` (not verified by me) |
| CH-11 | NEW tools/verifier manifest | Hash-cover `tools/`, `tests/acceptance/`, `.gitignore`, `verify_release_v2.py`, `LOCK_v2/*` | T-1 test `test_tools_manifest_covers_verifiers` (TO BE WRITTEN) | pending |
| CH-12 | NEW `requirements-dev.txt` | pytest pinned | P-06 | `07` diff |
| CH-13 | `research/september2026_income_nowcast/SOURCE_REGISTER.json:6`; ERRATA (append) | BLS hash correction, additive; the two reports are not edited | T-2 test (TO BE WRITTEN) | `06` diff |
| CH-15 | NEW `tests/acceptance/**` | Implement every TO BE WRITTEN test (112 IDs) | all | pending |
| CH-16 | NEW D-05 closure record + M-C9 milestone document | Per D3; must cite DC-06 lineage and the fb58ddc verification file | DC-03, DC-07 | pending |
| CH-17 | 4 label locations (`HISTORICAL_ALIGNMENT_PROTOCOL.md:22`, `prepare_2024_cost_inputs.py:83`, `SOURCE_REGISTER.json:74`, `ITERATION_NOTES.txt` append only) | Ordered label fix 2025-04-27 → 2025-04-28; byte-identical numeric outputs. Ordered; **not** a D-05 closure blocker, but included in this pass | N-54…N-56, P-20…P-22, G-10, DC-04, DC-05 | pending |
| **CH-20** (T-4) | NEW `research/historical_matched_baseline/MANIFEST_v2.json` | **T-4 is engineering, so it goes here.** Hash-cover `research/historical_matched_baseline/src/*.py`, `HISTORICAL_ALIGNMENT_PROTOCOL.md`, `SOURCE_REGISTER.json`, `VALIDATION_CRITERIA.json`, `FEASIBILITY_GO_NOGO.json`, `MATCHED_YEAR_READINESS.json`, the `outputs/*` files and `tests/*`, with current hashes. The verifier checks it. Nothing in `matched2024_provisional/` is rewritten (its ARTIFACT_LOCK stays) | DC-05; plus N-46-style fail-closed for this manifest (extend N-46's parameter list) | pending |
| **CH-21** | `research/historical_matched_baseline/src/validate_matched_inputs.py:135` | The gate `output_dir_not_national_R22` is constant `True` (VERIFIED). Compute it from the real output path (pass `out` into `validate()`). This tightens a gate and is not a relaxation. The committed `INPUT_VALIDATION.json` is **not** edited. Its PASS was true in that run, because `run_matched_national.py:50-52` refused national_R22 first (VERIFIED) | G-11 harness assertion (A4.4, R24) | pending |

**Restated condition 9a** (D3 condition 9, split as in DRAFT §4). It replaces the DRAFT §4 wording and the "Kevin decides whether 9a requires W2" bullet:
> **9a.** The 2024 matched-year calculation is reproduced by an **AI-operated computational reproduction on the final patched code** (P-08, plus P-21 for CH-17), **and** its FMR sensitivity is documented with the **completed C-W2 run** alongside O, A and B (`FMR_OUTCOMES.md` §6). 9a **does not depend on HUD** or on any answer to the HUD inquiry.

- C-W2 is done: Engineer's sealed `evidence_2734062_step4_w2/`, SHA256SUMS sha256 `117a1ba6766877f214c04300523c86b158e12a17d4b66e533916ccb2900bd5d8`. Its numbers were recomputed by me (VERIFIED, FMR_OUTCOMES §6).
- The remaining 9a work is the final-code reproduction (P-08), which can only run on the final candidate.
- Westchester stays BLOCKED as a *methodological* question (Part 2). That does not block 9a.

**Part 1 exit criterion:** all Part 1 tests PASS on the final candidate, and the DRAFT §5 proof script is clean. G-01 is clean or carries only Kevin-signed exceptions (the `len(person_zips)!=2` entry under D2; the P-26 housing entry if that reading is chosen). P-13 remains [K] (split ZIPs not on this box).

## PART 2: Methodological research (does NOT block Part 1)
| Item | State (VERIFIED unless noted) | Owner / next step |
|---|---|---|
| 2024 HUD FMR schedule | **NOT APPROVED** (formal Decision 2). Four sensitivity cases are kept (FMR_OUTCOMES §6): **O** (published) 17.6839565%; **A** (= C-W1, Westchester FY24 SEA $2,352) 17.6974846%, +0.013528 pp, 0.255 SE, 80/80 positive; **B** (W0, Westchester FY25 original $2,580; outside the Data Scout's options) 17.6986876%, +0.014731 pp, 0.277 SE, 80/80 positive; **C-W2** (Westchester NY HMFA FY24 $2,752) 17.6996675%, +0.015711 pp, 0.296 SE, 80/80 positive. Ordering **O < A < B < C-W2**. Range +0.0135 to +0.0157 pp | No code change in this pass (exclusion stands; T-3 guards it). Any schedule change needs a separate review |
| HUD inquiry: Westchester Oct–Dec 2024 ($2,352 SEA vs $2,752 NY HMFA); Honolulu before 2024-03-11 (FY24 original vs FY23 hold) | Westchester **BLOCKED pending HUD**; Honolulu BLOCKED (no FY2024 reevaluation list found), with small stakes. The Data Scout has a draft and channel ranking in `findings/data-scout/2026-10-22_hud_inquiry_draft.md` (recommended `pprd@hud.gov`; not sent) | **[K]** Nothing goes out under Kevin's name without his approval (resolution text). I have not contacted HUD |
| F3b_v2 `tools/check_pillars.py` | **HOLD** (Coordinator ruling d3). Not the CH-10 verifier | Kevin may revisit later |
| T-4 | **Not methodological.** Moved to Part 1 as CH-20 | — |
| F4 build reproducibility | `build_source_2024_2026.py` output is content-equivalent but not byte-identical to the frozen `inputs/source_2024_2026.csv` (row order). This was pre-existing at fb58ddc (VERIFIED earlier, FINAL_PLAN) | Research or engineering follow-up; not blocking; the frozen input is unchanged |

## PART 3: Scientific publication requirements (after Parts 1 and 2; Kevin's decisions)
| Requirement | State |
|---|---|
| Formal research publication of the 17.68% figure | **NO-GO** (formal Decision 1; `RESEARCH_READINESS.json` `publish_17_7_percent: NO-GO`, sha256 `1369e287…` unchanged; G-09) |
| **9b / milestone M-C9:** human-operated independent reproduction plus external methodological review | **Open.** Definition: `ITERATION_REGISTER.txt:10` ("an independent operator on a separate environment, with commands, input hashes, outputs, and a report attached"). AI reproduction does not count. It is also blocked for outside operators until `tract_tenure_acs2024.csv` and `tract_to_puma_50states_dc.csv` have public sources or committed builders (L13 / H-01) |
| Status labels | `EXTERNALLY_INDEPENDENTLY_REPRODUCED: NO` (D1; never YES on AI reproduction alone), optional `REPRODUCTION_REVIEW: PENDING`, `SCIENTIFICALLY_VALIDATED: NO`. Applied additively via CH-14 (`TRACK_E_CORRECTIVE_DRAFT.md` as amended by its D1 note). Tests DC-01, DC-02, G-05 |
| Erratum / corrective decision for Track E | Per `TRACK_E_CORRECTIVE_DRAFT.md`: computing and pushing 17.68% at 2734062 was a governance deviation from the recorded NO-GO. The calculation and its files are preserved. The erratum must present **all four FMR cases (O, A, B, C-W2)** with headline, delta, SE ratio and replicate signs, the Westchester ambiguity and the 2025-04-28 label correction. It must state that the schedule is not approved and that 17.6839565% is not replaced. Display precision should match the sampling error (90% CI 17.60%–17.77%); 9 significant figures stay only in the locked files |
| Pre-fb58ddc history edits | One ERRATA/HISTORY note (findings §5). Not a publication blocker, but it belongs in the record before any publication |

## Changes to traceability (additive to DRAFT §6 and CH-17.4)
| Requirement | Decision | Change | Tests |
|---|---|---|---|
| R7 (refined) bare = fb58ddc snapshot | D4; resolution (a) | CH-01, CH-18 | + P-23, N-57, N-58 |
| R11 (re-scoped; **no longer needs a Kevin decision**) housing archive validation | resolution (b) | CH-19 (supersedes CH-05) | N-59…N-66, P-25, P-26, G-11 |
| R22 historical-baseline manifest coverage (T-4) | formal D3 c6 | **CH-20** (was CH-17 MANIFEST_v2) | DC-05, N-46 (extended) |
| R23 v1 snapshot verified; lineage documented | resolution (a) | CH-02, CH-18 | P-24, DC-06, DC-07 |
| R24 gates must be computed, not constant | R15 | CH-21 | G-11 harness assertion |

- **Remaining gaps:** T-1 (CH-11) and T-2 (CH-13) still have no written test, only proposed names. T-3 is a proposed `git diff --quiet` check, to be added to CH-15. T-4 is closed by CH-20/DC-05.
- **Tests with no requirement:** none (VERIFIED by cross-check of A2.2, A3 and A4.4 against the rows above).

## Items still only Kevin or Cursor can do (replaces DRAFT §7)
1. **[K]** Supply the original split person ZIPs for P-13, or accept P-13 as untestable here.
2. **[K]** Optionally supply the external R2.4 and pillar Lock_v1 ZIPs, so that d658c08 can be checked against the released packages (findings §0, BLOCKED).
3. **[K]** Sign `approved_exceptions.json` (G-01 `len(person_zips)!=2` under D2; P-26 under A4.5 if that reading is chosen).
4. **[K]** HUD inquiry: approve recipient and text before anything is sent.
5. **[C]** Implement Part 1 from the Engineer's scratch candidate in the canonical environment. **[K]** Commit and push only on separate authorization.
6. **[K]** Part 3 decisions (publication, M-C9 operator, erratum wording).

## Material conflicts / rule-6
- **No material conflict** from (a): fb58ddc's manifests recompute and the frozen evidence is identical back to d658c08 (VERIFIED). The pre-fb58ddc rewrite at eec7c46 is documented, not hidden. Whether that is acceptable as the baseline is a judgment (HYPOTHESIS); I flag it without re-requesting a decision.
- **No new rule-6 item.**
  - The housing acceptance of duplicate or extra members (VERIFIED probe) is the already-escalated D-05 loosened check, now quantified. It cannot affect any committed result produced from the official container (exact bytes).
  - The constant gate (CH-21) did not produce a false PASS in the committed run.

---

## Dated note 2026-10-22 (about 06:40 UTC): CH-19 and CH-21 are RELEASE-BLOCKING; baseline status
> **AI methods review, not independent human peer review.** Additive. The FINAL-FOR-CURSOR section above is unchanged except as stated here.
> - Authority: `decisions/2026-10-22_final_remediation_priorities.md`, sha256 `d8555f09e7990ae1edb8433480c8378e548878d02358d6f1deeb6019f27f01c0` (VERIFIED), the **Coordinator's record of Kevin's priorities**.
> - Register: `decisions/DECISION_REGISTER.md`, sha256 `a41961d2dac1da6db81a8d3c17aff4e15787fa3abae706cef2111dff2b346e70` (VERIFIED), the Coordinator's record.

- **CH-19 (housing-archive validation) is RELEASE-BLOCKING.** It is "mandatory release-blocking" per the priorities file.
  - Release requires PASS on N-67…N-74 (distinct duplicate-in-subfolder, duplicate-listed-twice, `psam_husc.csv`-style, unrelated CSV, missing, bad hash, absent hash, non-matching re-zip). Each test uses the A5.3 hash + mtime(ns) snapshot over the repo copy, output parent, cache roots and frozen paths, with caches pre-populated.
  - Release also requires P-25, P-26 (or its must-FAIL flip under the strict reading, A4.5), P-28 and G-11.
- **CH-21 (protected-output gate) is RELEASE-BLOCKING.**
  - Required behaviour in addition to the CH-21 row: `validate()` receives the output path and computes `output_dir_not_protected` against every frozen path (resolved, including symlinks and subdirectories).
  - `run_matched_national.py` must run validation **before** `:53` `mkdir` and must not write `INPUT_VALIDATION.json` (`:56`) unless validation passed. A failure report goes to stderr or a log outside all output paths. This reorder is shared with CH-08.
  - Release requires PASS on N-75…N-78, P-27 and G-12. N-78, the mutation test, proves the tests catch the old constant `True`.
- **Gaps found in the earlier CH-19/CH-21 tests:** see ACCEPTANCE_TESTS A5.1 and A5.2.
  - Bundled IDs.
  - No absent-hash or non-matching-re-zip case.
  - Second-resolution mtime.
  - External cache roots not snapshotted.
  - No pre-populated caches.
  - No harness-sensitivity control.
  - No distinct CH-21 must-FAIL test.
  - No mutation test.
  - No before-write test for the validation path.
- **Counts:** 127 tests (78 must-FAIL, 28 positive, 12 no-gate-relaxed, 9 document checks).
- **Evidence mapping:** per the priorities file, the candidate review reports PASS, FAIL or BLOCKED **per test ID**, with an evidence path, using `findings/methods-reviewer/CANDIDATE_REVIEW_TEMPLATE.md`.
- **Baseline status:** **fb58ddc is the VERIFIED Git baseline** (`findings/methods-reviewer/2026-10-22_fb58ddc_v1_verification.md`). **The comparison with the original release ZIPs is BLOCKED, so the original distribution bytes are NOT verified.** Nothing in this spec or its tests may claim distribution-byte verification.
- **Not done by me:** the priorities file asks for the Audit Lead's independent review of this spec. That review is pending; this note is not that review.
