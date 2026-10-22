# fb58ddc as historical v1: verification (question (a))
> **AI methods review, not independent human peer review.** Read-only. Nothing in the repo, the frozen results, the gates or the original manifests was changed. No agent was messaged.
> - Written 2026-10-22, about 06:15 UTC (system clock 06:09 UTC at start of writing). Author: Methods Reviewer (Grok Bot).
> - Base under review: `273406208abe439cbad960567f32822b870c43b5`. Clone: `/workspace/hesi-team/clones/methods-reviewer/` (clean, `git status --porcelain` = 0 lines).
> - Authority: `decisions/2026-10-22_spec_questions_resolved.md`, sha256 **`9e6f1b757e6c7424dc23f4b53466811e194a1e2b3e26707499bb360352f96800`** (VERIFIED with `sha256sum`; matches its `.sha256` companion, `sha256sum -c` → OK). **Recorded by the Coordinator as Kevin's resolution.** Its wording: "Use fb58ddc as the historical baseline, conditional on verifying that its file contents and hashes correspond to the intended original evidence. Document any earlier changes rather than rewriting history."
> - Labels: VERIFIED (command, hash or file cited) / HYPOTHESIS.

## 0. Verdict
**PASS, with documented earlier changes. No material conflict for the scientific evidence.** One sub-check is **BLOCKED** (comparison with the external release ZIPs, which are not on this box).

- **PASS (VERIFIED).** At `fb58ddc045976d844c6da1fca99ed1f9f108bb85`, every hash in every release manifest recomputes from the committed file bytes:

| Manifest at fb58ddc | Manifest sha256 | Entries recomputed | Mismatches |
|---|---|---|---|
| `core_r24/RELEASE_FILE_HASHES.json` | `49871df6d998cbc1dbfd71c14bb84631474de1a7ef1cddf4db6ecc21739d2e96` (git blob `6e560d6b82`) | 35 | 0 |
| `research/september2026_core_r2/INTEGRITY_MANIFEST.json` | `a0de55896313e4fa53a75ec775e4e6c7c8482765852daea4bad3e19305bf9908` | 40 | 0 |
| `…/SOURCE_HASHES.json` | `29e8aa72e1d973c8…` | 24 | 0 |
| `…/housing/PACKAGE_MANIFEST.json` | `5ecf44ae52c364dc…` | 15 | 0 |
| `…/transportation/SOURCE_HASHES.json` | `e4fe0a480661642c…` | 10 | 0 |

  - Method: `scratch/methods-reviewer/fb58_v1/v1check.py` (sha256 `b63fd3d7…`). It hashes `git show <commit>:<path>` for every entry. Output: `v1check.out` (`1a056afa…`).
  - Runtime check: on a `git archive fb58ddc` export, fb58ddc's own `core_r24/verify_package.py` printed "PASS: all 35 source/result package files match release hashes" and "PASS: regression tests and reproduced national results" (6 metrics, 80 replicates, `frame_exact: true`), exit 0 (`verify_package_fb58ddc.log`, `2c35481c…`). fb58ddc's `research/september2026_core_r2/verify_release.py` exited 0 with all four entries true (`verify_release_fb58ddc.log`, `85cd59fa…`).
  - This is an AI-operated reproduction on a separate machine, not independent reproduction.
- **Documented earlier change (VERIFIED). fb58ddc's `RELEASE_FILE_HASHES.json` is the second committed state of that file, not the first.**
  - It was rewritten in place at `eec7c46` (§2), before fb58ddc. fb58ddc itself did not touch it: its blob equals eec7c46's (`6e560d6b82`).
  - The rewrite changed no hash of any result, input, lock or formula file. It was recorded at the time in `ITERATION_REGISTER.txt` and `ITERATION_NOTES.txt`.
  - It must be **documented** in the v1 lineage, which the Engineer's proposed HISTORY file currently omits (§4). That documentation is all the resolution asks for.
- **Why I judge this not a material conflict:**
  - The "intended original evidence" is the frozen R2.4 national results, the locked inputs, the person/housing locks and the pillar specifications. All of them are byte-identical at d658c08 (first import), eec7c46 and fb58ddc (VERIFIED: `git diff --stat d658c08 fb58ddc -- core_r24/results core_r24/inputs research/september2026_core_r2` is empty).
  - The eec7c46 differences are a test-fixture format change and an I/O-only loader in `run_joint.py` (§2).
  - **This is a judgment (HYPOTHESIS).** If Kevin regards the d658c08 R2.4-import manifest as "the original", the answer changes. In that case the CSV fixtures and run_joint `030cb0ae…` would not be v1, and `c5ac44d0…` (34 entries) would be. I do **not** re-request the approval (the resolution says not to "unless new evidence creates a material conflict"). I only flag it so the choice is informed.
- **BLOCKED (VERIFIED as unavailable).** `ITERATION_REGISTER.txt` says d658c08 imported a "byte-identical Core R2.4 package" ("34/34 RELEASE_FILE_HASHES.json matches after fixture restore"). `LOCK_REGISTER.json` names the external pillar packages `HESI_Science_v52_September2026_Current_Food.zip`, `HESI_Housing_September2026_Scoped_Methodology_Lock_v1.zip` and `HESI_Transportation_September2026_12000mi_Lock_v1.zip`.
  - None of these ZIPs is on this box: `find / -xdev` by name found none.
  - So the step "git d658c08 = the externally released package" cannot be checked here. Only Kevin can supply those archives **[K]**.

## 1. Lineage of the v1 manifest (VERIFIED, `git log --all -- core_r24/RELEASE_FILE_HASHES.json` and `git show <c>:<f> | sha256sum`)
| Commit | Date (−0400) | Message | RELEASE_FILE_HASHES.json sha256 | Entries | Change type |
|---|---|---|---|---|---|
| `d658c08cf425873b5dea6c0cf6fdbb537446db6a` | 2026-10-21 20:21 | Integrate Core R2.4 research and September 2026 pillar references | `c5ac44d0263e5bb2fe84dd6c4259dc6d78dbba573e632c967bb2740c04b877b3` | 34 | created (R2.4 import) |
| `55b61ea08e2cf2983d9e7404bce9af6c50ca007a` | 20:35 | Record Core R2.5 clean-environment national reproduction evidence | same `c5ac44d0…` | 34 | none |
| `eec7c46aea22989fbbcd5e966aa4f0fab49e35d6` | 20:49 | Rebuild HUD and USDA sources and repair portable fixtures | `49871df6…` | 35 | **in-place rewrite** (§2) |
| `fb58ddc045976d844c6da1fca99ed1f9f108bb85` | 22:22 | Publish R2.5 research checkpoint on the integration branch. | same `49871df6…` | 35 | none (**chosen v1**) |
| `e45eb8766263eed52f6d7894e3464f8ffea76094` | 22:54 | Document methods review findings and repair official PUMS ingestion | `4f6825d7678f5b304ba9ba9652a3ffd363cdd9b67f2bde6a14778fdeadaa84e8` | 38 | **in-place rewrite** (D-05) |
| `273406208abe439cbad960567f32822b870c43b5` | 23:55 | Publish provisional 2024 matched-year engine and engineering fixes | `6cd769e022023437d360a25c333a3062c7dde9f7a5ef946165e7ba37376862f4` | 38 | **in-place rewrite** (D-05, run_joint) |

- At **every** commit above, the manifest matches its own tree (0 mismatches; `v1check.out`).
- The four pillar manifests and `LOCK_REGISTER.json` (`be3388d7…`) are **byte-identical at all six commits** (git blobs `ef74a5254b`, `2dff33f9fe`, `88a5322e42`, `8c311caa30`, `caa4371877`). At 2734062 they no longer match 3 changed pillar scripts (`housing/verify.py`, `transportation/run_standard.py`, `transportation/test_standard.py`; D-05 C2, re-confirmed in `v1check.out`).
- Every commit listed is on `origin/hesi/core-r25-integration` (VERIFIED, `git branch -r --contains`).

## 2. The pre-fb58ddc rewrite at eec7c46 (VERIFIED by key-wise diff of the two JSON objects and `git diff d658c08 eec7c46`)
| Entry | d658c08 (`c5ac44d0…`) | eec7c46 = fb58ddc (`49871df6…`) | Nature |
|---|---|---|---|
| `src/run_joint.py` | `7ddc26586a026e12eeacc2356e04a73bf5f534f207aefe2f41870b7dd81785b0` | `030cb0ae0baed16770e198a0c9f2353180ad3ccb55e6483d37b1c11dd3a24034` | changed: adds `load_person_table()` (CSV or pickle) and replaces two `pd.read_pickle` calls (`run_joint.py:16-29` at eec7c46). The docstring says "I/O only; does not change joint formulas". By reading, no arithmetic line changed (VERIFIED: diff is +12/−2, all in loading) |
| `fixtures/synthetic_food.pkl` | `306ca346…` | — | removed (file deleted; NumPy-2 pickle failed on NumPy 1.26.4) |
| `fixtures/synthetic_composition.pkl` | `f5f6547f…` | — | removed (same reason) |
| `fixtures/synthetic_food.csv` | — | `ef41d6e6…` | added (7 households, CSV replacement) |
| `fixtures/synthetic_composition.csv` | — | `f789fb01…` | added |
| `tests/test_run_joint_synthetic.py` | — | `e784a148…` | added (live run_joint test on both NumPy majors) |
| all other 29 entries, including every `results/national_R22/*`, `results/rebuilt_from_raw/*`, `results/synthetic/*`, `inputs/*`, `reproduce_from_raw.py` `c6783be3…`, `rebuild_raw_person_caches.py` `d9a20f2e…`, `verify_package.py` `1a414de8…` | unchanged | unchanged | key order was re-sorted alphabetically (cosmetic) |

- **How it was recorded at the time (VERIFIED):**
  - `ITERATION_NOTES.txt` at eec7c46 says "RELEASE_FILE_HASHES.json refreshed to 35 files (CSV fixtures + new test; pickle hashes dropped)" and "PASS: verify_package.py 35/35".
  - `ITERATION_REGISTER.txt` at eec7c46 says "replaced NumPy-2 pickle fixtures with CSV; added load_person_table I/O in run_joint.py … Formulas, eligibility, and published R2.4 result files unchanged".
  - The tool that wrote it, `core_r24/tools/refresh_release_hashes.py`, was added in the same commit (`:5` reads, `:23` writes the manifest in place). It is the same mechanism later used at e45eb87 and 2734062 (CH-03).
- **Evidence that the frozen results did not depend on the change (VERIFIED):** the clean-environment national reproduction committed at 55b61ea, **before** the rewrite, already passed against `national_R22` (`core_r24/reproduction_runs/2026-10-21_clean_env/verify_package.txt`: `status PASS, metrics_compared 6, replicates_compared 80, frame_exact true`). eec7c46's register line reports the same after the repair.
- **What remains HYPOTHESIS:** that `7ddc2658…` is byte-identical to the run_joint inside the external R2.4 ZIP. That is BLOCKED (§0).

## 3. In-place rewrites of v1 after fb58ddc (fb58ddc..273406208abe) (VERIFIED, key-wise diff and `git diff -U0 fb58ddc 273406208abe -- core_r24/RELEASE_FILE_HASHES.json`)
| # | Commit | Line at 2734062 | Entry | Old (fb58ddc) | New | Kind |
|---|---|---|---|---|---|---|
| 1 | e45eb87 | 13 | `rebuild_raw_person_caches.py` | `d9a20f2e0fb0e99f…` | `97d51efa6d6b2cf7…` | value replaced in place |
| 2 | e45eb87 | 14 | `reproduce_from_raw.py` | `c6783be3d70798b2…` | `6b41f2e01dfc1e95…` | value replaced in place |
| 3 | e45eb87 | 37 | `PUMS_ARCHIVE_LOCK.json` | — | `998c85b16785…` | entry added |
| 4 | e45eb87 | 38 | `tools/pums_archive.py` | — | `c34d790642dd…` | entry added |
| 5 | e45eb87 | 39 | `tests/test_pums_archive.py` | — | `fb3597fad615…` | entry added |
| 6 | 2734062 | 30 | `src/run_joint.py` | `030cb0ae0baed167…` (unchanged at e45eb87) | `a34951b135936ddf…` | value replaced in place |

- No entry was removed in fb58ddc..2734062.
- This matches D-05_DECISION.md §1.1 and SUPERSEDED records. No new rewrite was found beyond those already documented.

## 4. Gaps in the proposed lineage record (VERIFIED by reading `proposals/2026-10-22_remediation/integrity_v2/09_v1_fb58ddc_manifest_restore_history.diff`)
- The Engineer's proposed `RELEASE_FILE_HASHES_v1_fb58ddc.json` is a verbatim copy of fb58ddc's manifest (git blob id in the diff header = `6e560d6b82…` = fb58ddc's blob; VERIFIED). **Good.**
- The proposed `RELEASE_FILE_HASHES_HISTORY.json` starts at fb58ddc. **It omits the d658c08 state (`c5ac44d0…`, 34 entries) and the eec7c46 in-place refresh.** Required addition (CH-18): a first lineage entry with
  - commit `d658c08…`, sha256 `c5ac44d0…`, 34 entries, role "R2.4 import manifest";
  - the eec7c46 transition: the six entry changes in §2, tool `tools/refresh_release_hashes.py`, and pointers to the ITERATION_REGISTER/NOTES text.

## 5. Other history edits before fb58ddc (VERIFIED; governance record, not hash-locked)
`ITERATION_REGISTER.txt` declares itself "Append-only" (`:4` at fb58ddc). Before fb58ddc it was edited in place:
- **55b61ea:** deleted d658c08's lines 55-56 ("Not demonstrated: clean-environment national rerun; independent external reproduction; scientific validation; HUD/USDA upstream reconstruction." and "Git: branch … NO COMMIT. NO PUSH. NO PR."). The replacement line records commit d658c08.
- **eec7c46:** replaced one "Git:" line (added the 55b61ea SHA).
- **ITERATION_NOTES.txt at 55b61ea:** 98 lines deleted. These included the d658c08 integration note's header, its change table and its results table ("2024 pilot thrifty national share | 10.301% …", "R2.4 share below three costs | 18.9918% …"). By line-matching, those lines no longer appear verbatim in the 55b61ea file.
- All of this text survives in git history (`git show d658c08:ITERATION_NOTES.txt`).
- No number was changed. But this is the same "rewrite instead of append" pattern as D-05, and it predates fb58ddc. **Recommendation (AI):** a single ERRATA/HISTORY note listing these pre-fb58ddc edits, with pointers to d658c08. **Do not** restore the text by editing the files.

## 6. New observation found while preparing (b) (VERIFIED by reading; low severity)
- `research/historical_matched_baseline/src/validate_matched_inputs.py:135` appends the gate `output_dir_not_national_R22` with status **constant `True`**. It performs no check.
- The committed frozen `matched2024_provisional/INPUT_VALIDATION.json:133-135` records it as PASS.
- **In the committed run, the condition did hold.** `run_matched_national.py:50-52` refuses `national_R22` before `validate()` is reached. So this is not a false claim about that run.
- But a gate that cannot fail is misleading for any other caller. Proposed fix: CH-21 (compute it from the actual output path; a tightening). The frozen JSON stays untouched.

## 7. Housing archive structure (input to (b); VERIFIED on the official `csv_hus.zip`, sha256 `8281008e53de98f0…` = lock `r24_locked_zip_sha256.housing_csv_hus.zip`)
| Member | Uncompressed bytes | CRC-32 | Data rows | STATE codes | Columns |
|---|---|---|---|---|---|
| `psam_husa.csv` | 495,752,055 | `0x021460c8` (= lock 34889928) | 827,133 | 25 (01…28) | 241 |
| `psam_husb.csv` | 481,732,465 | `0x68086bd7` (= lock 1745382359) | 804,836 | 26 (29…56) | 241 |
| `ACS2024_PUMS_README.pdf` | 103,658 | `0xda7203f4` | — | — | — |

- The two CSVs together hold 1,631,969 rows and 51 state codes (50 states + DC; disjoint sets). That equals `national_R22/audit.json` `raw_rows: 1631969` (VERIFIED).
- `run_joint.py:43` reads `SERIALNO, STATE, PUMA, TYPEHUGQ, NP, WGTP, HINCP, ADJINC, TEN, WGTP1…WGTP80`.
- There is **no split variant** of the housing archive (lock has only the official container).
- There is **no housing cache**: run_joint streams the ZIP (`:44-47`).
- **Current behaviour at 2734062 (VERIFIED by probe):** `scratch/methods-reviewer/hus_probe/hus_probe.log` (`34256331…`). It used the committed `pums_archive.py` (`c34d7906…`, equal to its v1 hash) with a synthetic lock and a non-matching container, so the inner-hash path runs.
  - `verify_housing_zip` **accepts**:
    - an extra `psam_husc.csv`;
    - a duplicate `psam_husa.csv` in a subfolder;
    - the same name twice with a bad copy first;
    - an unrelated `notes.csv`.
  - It **rejects** a missing member and a bad hash.
  - For the accepted duplicate and extra cases, `run_joint.py:45` would read **every** `psam_hus*` CSV, including the extra or duplicate one. This double-counts or adds households.
  - The official container is unaffected (exact bytes). The risk applies only to a re-containered archive. Tested by N-59…N-66 (ACCEPTANCE_TESTS A4).

---

## Dated note 2026-10-22 (about 06:40 UTC): baseline status (additive)
> AI methods review, not independent human peer review. Authority: `decisions/2026-10-22_final_remediation_priorities.md`, sha256 `d8555f09e7990ae1edb8433480c8378e548878d02358d6f1deeb6019f27f01c0` (VERIFIED), the Coordinator's record of Kevin's priorities: "Accept fb58ddc as the verified Git historical baseline, but retain the original release ZIP comparison as BLOCKED … Do not claim original distribution-byte verification is complete."

- **fb58ddc is the VERIFIED Git baseline** (§0, §1: manifests recompute 35/40/24/15/10 with 0 mismatches; the snapshot's own verifiers pass).
- **The release-ZIP comparison is BLOCKED.** The external R2.4 package and the pillar Lock_v1 ZIPs are not available. **The original distribution bytes are NOT verified.** The "PASS" in §0 refers to Git objects only.
- **The decision register now lists the resolution** (`decisions/DECISION_REGISTER.md`, sha256 `a41961d2…6e70`, VERIFIED). DC-07's register half is satisfied; its closure-record half waits for CH-16 (ACCEPTANCE_TESTS A5.0).
