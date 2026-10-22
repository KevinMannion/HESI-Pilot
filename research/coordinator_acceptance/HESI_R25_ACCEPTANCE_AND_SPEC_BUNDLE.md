# HESI R2.5 release integrity: acceptance tests, implementation spec and decision register (transfer bundle)

Exported 2026-10-22T06:39:56Z by the HESI Research Coordinator, from the team workspace. Base commit for the spec: 273406208abe439cbad960567f32822b870c43b5 (hesi/core-r25-integration).

Status: the acceptance tests and spec are the team's FINAL-FOR-CURSOR versions, pending verification of the candidate. They come from AI methods review and AI-operated reproduction, not independent human peer review or external scientific validation. Formal publication remains NO-GO.

Test count: the original 49 IDs plus Addenda A2 to A5 make 127 stable IDs. Kevin's t41u message refers to 112; A5 (CH-19 and CH-21 release-blocking tests N-67 to N-78, P-27, P-28 and G-12) was added afterwards. Nothing was renumbered or deleted.

## Source files (sha256)

```
ba1d84dc129b8ab87d99b47c418052b303e8dee065ab273d706612451e2f2e11  ./2026-10-22_fb58ddc_v1_verification.md
e920114e51bd8c3860f3ee6d3962b098efe8c7d8c337365f314611752439ecfd  ./ACCEPTANCE_TESTS.md
71090b3e90f17d7016218352fb44c34d5b9d02877a5002cc315f59748f2544a9  ./CURSOR_IMPLEMENTATION_SPEC.md
b3424cf028b387bc1f07dc083b74c42222b31b9d1cf78daa8b2c692fd7dbed1f  ./CURSOR_PACKAGE_MANIFEST.md
6fc07b65c1bb833f9bb9ec88a423b523aa08b57f807a84bc39dbe6e1bfc3fbee  ./D-05_DECISION.md
d8555f09e7990ae1edb8433480c8378e548878d02358d6f1deeb6019f27f01c0  ./decisions/2026-10-22_final_remediation_priorities.md
5cfc277bd8e66e113448e5be7004658470774d82d27d9fcfe434cb0dbb249661  ./decisions/2026-10-22_final_remediation_priorities.md.sha256
6af3bc51ed4a482186839dc38ce540ace37bfdb6867f47c53d31fcc73783a7a0  ./decisions/2026-10-22_five_governance_answers.md
d7f39d6341e0dae84a447f969ce71296bc1271348c37c78baaa352778aa13505  ./decisions/2026-10-22_five_governance_answers.md.sha256
090a630665aeba727dc3002c95d2607bff8da3849123e2079c976350016828f8  ./decisions/2026-10-22_formal_governance_decisions.md
2494b357ff44de9724566987b5dcf27311f115a2bfdbcd6808abe7bd1fcdd8bd  ./decisions/2026-10-22_formal_governance_decisions.md.sha256
53bc916d92955a0e481d389787a4152e85772887fc9e76541c78d0006a639836  ./decisions/2026-10-22_hud_contact_authorization.md
9bcd755a43f929ed88cbc13b0d4996b34a02087a252f7411e8449d83bc546c0d  ./decisions/2026-10-22_hud_contact_authorization.md.sha256
9e6f1b757e6c7424dc23f4b53466811e194a1e2b3e26707499bb360352f96800  ./decisions/2026-10-22_spec_questions_resolved.md
19bae408760156a03431ae710084837a7c9ff6f5f89c30b2647f26db4250f134  ./decisions/2026-10-22_spec_questions_resolved.md.sha256
069ba53e101e2aede962b79f7c09da4bf19fb61e4cbf866b48b84255fda4f472  ./decisions/DECISION_REGISTER.md
44b4cbf001e50d56971d1f89f05c61979d62c62df6c120c188878d9fa913f5d1  ./decisions/DECISION_REGISTER.md.sha256
```

---

<!-- BEGIN FILE: decisions/DECISION_REGISTER.md -->

# HESI decision register (index; Coordinator-maintained, append-only)
Created 2026-10-22T06:15:48Z. Each entry points to a read-only decision file and its .sha256. Entries are never edited; status changes are appended.

| Recorded (UTC) | File | sha256 | Scope | Status |
|---|---|---|---|---|
| 2026-10-22T05:14:38Z | 2026-10-22_formal_governance_decisions.md | 090a630665aeba72… | HESI formal research governance decisions, 2026-10-22 | RESOLVED |
| 2026-10-22T05:32:57Z | 2026-10-22_five_governance_answers.md | 6af3bc51ed4a4821… | Kevin Mannion: final responses to five governance questions | RESOLVED |
| 2026-10-22T05:47:37Z | 2026-10-22_hud_contact_authorization.md | 53bc916d92955a0e… | Kevin Mannion: HUD contact authorized (message t35u) | RESOLVED |
| 2026-10-22T06:02:47Z | 2026-10-22_spec_questions_resolved.md | 9e6f1b757e6c7424… | Kevin Mannion: outstanding specification decisions closed (message t38u) | RESOLVED |
| 2026-10-22T06:23:58Z | 2026-10-22_final_remediation_priorities.md | d8555f09e7990ae1… | Kevin Mannion: final remediation priorities (message t41u) | RESOLVED |

Open (not decisions): Westchester FMR assignment UNRESOLVED (HUD track; Kevin sending inquiry himself); FMR schedule NOT approved; formal publication NO-GO.

Correction note (Coordinator, 2026-10-22 ~06:40Z): the t41u row was moved inside the table (it had been appended below the notes). No entry text changed. The file stays writable so rows can be appended, and each version is hashed in DECISION_REGISTER.md.sha256.

<!-- END FILE: decisions/DECISION_REGISTER.md -->

---

<!-- BEGIN FILE: decisions/2026-10-22_formal_governance_decisions.md -->

# HESI formal research governance decisions, 2026-10-22
Recorded by: HESI Research Coordinator, at 2026-10-22T05:14:38Z (UTC), from Kevin Mannion's instruction received 2026-10-22 05:14 UTC (01:14 ET).
Repo state at recording: hesi/core-r25-integration head 273406208abe439cbad960567f32822b870c43b5.
This record is append-only. Prior decisions and Git history are preserved and not rewritten.

## DECISION 1: Track E / 17.68% (17.6839565%, 0.17683956520767094)
The provisional 2024 matched-year national calculation was executed and pushed to the public research branch in 2734062, despite the earlier recorded NO-GO for execution (fb58ddc STATUS: EXECUTE_NATIONAL_PERCENTAGE_THIS_ROUND: NO-GO; NATIONAL_SHARE_COMPUTED: NO; 2734062 RESEARCH_READINESS.json still says publish_17_7_percent: NO-GO and provisional_public_research_release: NO-GO).
This was a research-governance deviation. It is NOT retroactively preauthorized, and prior decisions are not rewritten.
Preserve the calculation and Git history. Do not modify frozen numerical results.
Statuses:
- COMPUTATION_EXECUTED: YES
- PUBLIC_DEVELOPMENT_ARTIFACT_AVAILABLE: YES
- EXTERNALLY_REPRODUCED: PENDING
- SCIENTIFICALLY_VALIDATED: NO
- FORMAL_RESEARCH_PUBLICATION: NO-GO
Action: add a dated corrective decision and an explanatory erratum (to be drafted by the team; implemented by Kevin in Cursor).

## DECISION 2: Scientific methodology
- run_joint.py reuse as an implementation component: CONDITIONAL APPROVAL, provided that historical and current cost vintages are isolated, input selections are explicit, and regression tests establish no cross-contamination.
- 2024 HUD FMR schedule: NOT APPROVED yet. Investigate the effective-date discrepancy and the FY2025-everywhere simplification (the 12 reevaluation areas); document the corrected and original outcomes; present the numerical sensitivity.
- Do not change the accepted scientific definition or replace the current provisional calculation without separate review.

## DECISION 3: D-05
FORMALLY APPROVED IN PRINCIPLE: preserve the original release manifests and create new versioned v2 manifests for modified scripts.
Mandatory conditions:
1. Historical manifests and prior release evidence remain immutable.
2. Verification against a missing, empty or mismatched applicable manifest must FAIL.
3. No direct-run bypass of scientific locks.
4. No unreviewed in-place hash replacement.
5. Protected outputs are rejected before creating caches or intermediates.
6. All applicable pillar and core manifests are checked.
7. The original and v2 verification paths are explicitly distinguished.
8. The final patched code reproduces the frozen R2.4 calculation and all 80 replicates.
9. The 2024 matched-year calculation is independently reproduced and its FMR sensitivity investigated.
The Audit Lead translates these into explicit acceptance tests before implementation is approved.

## Coordination
- Cursor remains the canonical software engineering environment. The Engineer may prepare patches and evidence, but never pushes competing implementations into the repository.
- Cursor receives one consolidated, reviewed implementation specification.
- No automatic push, merge, PR or formal scientific release. Escalate any change that could alter published numerical results.
- Deliverable: one consolidated GO/NO-GO report after verification.

<!-- END FILE: decisions/2026-10-22_formal_governance_decisions.md -->

---

<!-- BEGIN FILE: decisions/2026-10-22_five_governance_answers.md -->

# Kevin Mannion: final responses to five governance questions
Recorded: 2026-10-22T05:32:57Z (decision received 2026-10-22 ~05:32Z, message t32u). Remote branch head at recording: 273406208abe. Supplements, and does not replace, 2026-10-22_formal_governance_decisions.md.

## Decision 1: Status label
Use the existing field EXTERNALLY_INDEPENDENTLY_REPRODUCED: NO for the 2024 matched-year calculation. If necessary, separately record REPRODUCTION_REVIEW: PENDING to indicate active work. Do not change the existing field to YES based solely on AI-operated computational reproduction. Preserve the exact meaning of each verification status.

## Decision 2: Census person archive validation
Restore equivalent or stronger protection, not an obsolete requirement for two ZIP containers. Accept either (a) two correctly authenticated split person archives, or (b) one official Census combined person archive. In both cases require the expected person CSV components, correct hashes, unique members, valid structure, and complete input coverage. Reject missing components, duplicate members, unexpected CSVs, invalid hashes and reusable failed-run caches. No silent gate relaxation.

## Decision 3: Human independent reproduction
Separate human-operated independent reproduction and external methodological review into their own milestone. D-05 may close after the required engineering checks, provenance verification and AI-operated computational reproduction pass. Do not equate D-05 closure with independent human scientific validation. Keep formal scientific publication NO-GO.

## Decision 4: Verification default
Keep the original v1 verification semantics as the default for the existing package-verification command. Require explicit selection of v2 for the current release candidate, or use a clearly separate v2 verification entry point. Historical v1 verification must reference the historically correct source snapshot, not changed working-tree files. Missing, empty, malformed, or mismatched required manifests must fail closed.

## Decision 5: Implicit inputs
Official and locked research executions must require explicit source manifests, cost vintage, methodology configuration and designated output location. Exploratory development runs may accept documented defaults, but all effective inputs, software versions, source hashes, methodology choices and output paths must be recorded in their audit artifacts. Development defaults cannot create or overwrite frozen scientific results.

## Implementation
Incorporate into ACCEPTANCE_TESTS.md and the consolidated Cursor specification. Engineer tests the final proposed implementation against all applicable acceptance conditions. Audit Lead independently reviews the completed candidate (AI review, not independent human review). Cursor remains the canonical implementation environment. Do not rewrite original governance history, original release manifests, frozen scientific results, or validation gates. Do not commit, push, merge or formally publish without separate authorization. Return a single consolidated implementation package for Cursor, with no additional routine approval questions unless a genuine scientific conflict remains.

<!-- END FILE: decisions/2026-10-22_five_governance_answers.md -->

---

<!-- BEGIN FILE: decisions/2026-10-22_spec_questions_resolved.md -->

# Kevin Mannion: outstanding specification decisions closed (message t38u)
Recorded: 2026-10-22T06:02:47Z. Base 273406208abe. Status: RESOLVED.

## D-05 historical v1: RESOLVED
Use fb58ddc as the historical baseline, conditional on verifying that its file contents and hashes correspond to the intended original evidence. Document any earlier changes rather than rewriting history.

## Housing archive: RESOLVED (APPROVED)
Apply equivalent or stronger integrity validation to Census housing archives, accounting for their actual file structure.

## Directions
Record both in the decision register, mark RESOLVED, and incorporate into the acceptance tests. Do not request these approvals again unless new evidence creates a material conflict. The HUD investigation is a separate methodological track and must not block the release-integrity implementation specification. The Westchester FMR assignment remains unresolved: keep all four sensitivity cases, leave the original provisional result unchanged, and keep formal publication NO-GO. Next: finalize the consolidated Cursor implementation specification and acceptance tests; deliver exact files or shareable references for Cursor; clearly distinguish (1) release-integrity engineering blockers, (2) methodological questions requiring further research, and (3) scientific publication requirements. For the HUD inquiry: official recipient and complete proposed message for review before sending; nothing sent under Kevin's name without his approval.

<!-- END FILE: decisions/2026-10-22_spec_questions_resolved.md -->

---

<!-- BEGIN FILE: decisions/2026-10-22_final_remediation_priorities.md -->

# Kevin Mannion: final remediation priorities (message t41u)
Recorded: 2026-10-22T06:23:58Z. Base 273406208abe.

Proceed with the final implementation package.
- CH-19 and CH-21 are mandatory release-blocking corrections.
- CH-19: require negative tests proving that duplicate, unexpected, missing, or unauthenticated Census housing CSV components are rejected without contaminating caches or results.
- CH-21: replace the hard-coded PASS with a real protected-output validation check. Require negative tests showing rejection occurs before any writes.
- Accept fb58ddc as the verified Git historical baseline, but retain the original release ZIP comparison as BLOCKED until those artifacts are available. Do not claim original distribution-byte verification is complete.
- The 112 acceptance tests must be mapped to actual evidence. Report PASS, FAIL, or BLOCKED per test, not just a count.
- Keep the original scientific results and governance history unchanged.
- Finish the consolidated Cursor implementation specification and have the Audit Lead independently review it.
- No additional routine approval requests are necessary. Escalate only scientific conflicts or material integrity failures.

<!-- END FILE: decisions/2026-10-22_final_remediation_priorities.md -->

---

<!-- BEGIN FILE: decisions/2026-10-22_hud_contact_authorization.md -->

# Kevin Mannion: HUD contact authorized (message t35u)
Recorded: 2026-10-22T05:47:37Z. Base 273406208abe.

Kevin authorized contacting HUD for a narrowly scoped technical clarification of Westchester County's applicable FMR for 2024-10-01 to 2024-12-31: A = Westchester's separately published FY2024 FMR ($2,352, 2BR) or B = New York HUD Metro FY2024 FMR ($2,752, 2BR). The inquiry states that this concerns historical FMR applicability during the transition to FY2025 geography, including the New York Metro FY2025 reevaluation. It asks HUD to identify the controlling notice, effective-date rule, historical dataset or other authoritative documentation. Use the appropriate official HUD channel. Send only a professional research inquiry: no private data, no claimed HUD affiliation. Retain the exact question, date, recipient, response and source links in the provenance record. If direct contact is unavailable, prepare the inquiry and identify the submission channel; do not claim it was sent.

In parallel: finish the NY FY2024 sensitivity with 80 replicates; preserve 17.6839565% unchanged; record the original, Reading A, Reading B and NY FY2024 cases separately; correct the April 27/28 documentation without altering historical numerical results; do not choose an interpretation by preferred result. FMR methodology stays unapproved until the evidence is sufficient. One consolidated report when the sensitivity and authoritative-source investigation are complete. Escalate any HUD response that materially changes methodology.

Coordinator note: per standing rules, the outgoing message is shown to Kevin as a draft before sending (Kevin presses Send).

<!-- END FILE: decisions/2026-10-22_hud_contact_authorization.md -->

---

<!-- BEGIN FILE: CURSOR_IMPLEMENTATION_SPEC.md -->

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

<!-- END FILE: CURSOR_IMPLEMENTATION_SPEC.md -->

---

<!-- BEGIN FILE: ACCEPTANCE_TESTS.md -->

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

<!-- END FILE: ACCEPTANCE_TESTS.md -->

---

<!-- BEGIN FILE: 2026-10-22_fb58ddc_v1_verification.md -->

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

<!-- END FILE: 2026-10-22_fb58ddc_v1_verification.md -->

---

<!-- BEGIN FILE: D-05_DECISION.md -->

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

<!-- END FILE: D-05_DECISION.md -->

---

<!-- BEGIN FILE: CURSOR_PACKAGE_MANIFEST.md -->

# CURSOR PACKAGE MANIFEST: D-05 remediation (base 273406208abe)
> **AI methods review, not independent human peer review.** A list of the files Cursor needs, for Kevin and Cursor. It is not an approval.
> - Hashes and sizes computed **last**, at 2026-10-22T06:14:30Z, by `scratch/methods-reviewer/package/build_manifest.py` (VERIFIED: computed with Python hashlib over the exact bytes). Paths are relative to `/workspace/hesi-team/` unless absolute.
> - Base: `273406208abe439cbad960567f32822b870c43b5`. v1 snapshot: `fb58ddc045976d844c6da1fca99ed1f9f108bb85` (resolution (a), verified PASS).
> - **Read-only rule:** every file below is an input to Cursor and must not be edited. "READ-ONLY (mode)" = the filesystem mode has no write bit (decisions and sealed evidence). "treat as read-only" = writable on disk but owned by another role or frozen by the record; changes only additively by its owner.
> - The repository itself (frozen results, gates, original manifests, LOCK_REGISTER, history) is read-only for everyone except Kevin/Cursor implementing Part 1, and even then only as the spec allows.
> - Verify after transfer: `sha256sum -c` against the table, or re-run the build script.

## Read order for Cursor
1. `CURSOR_IMPLEMENTATION_SPEC.md`, FINAL-FOR-CURSOR section; 2. `ACCEPTANCE_TESTS.md` (§1 setup, then A2-A4); 3. `D-05_DECISION.md` §3; 4. decisions files; 5. Engineer candidate diffs (E); 6. evidence and findings as cited.


## A. Specification and tests (primary)
| Path | sha256 | Bytes | Read-only | Purpose |
|---|---|---|---|---|
| `proposals/2026-10-22_remediation/CURSOR_IMPLEMENTATION_SPEC.md` | `0e6a25618433408eba7acd1fef6b5766396ade58dff7f1419c34213573ffce36` | 53407 | treat as read-only | Implementation spec. Read the FINAL-FOR-CURSOR section (supersedes the DRAFT above it): Part 1 blockers CH-01..CH-21, Part 2 research, Part 3 publication |
| `proposals/2026-10-22_remediation/ACCEPTANCE_TESTS.md` | `d0e3c07e3d374e0f5eb2be7714877f49898741ca1a28dd67e55785c71ae24c98` | 68582 | treat as read-only | 112 acceptance tests (49 original + A2 37 + A3 9 + A4 17), traceability, no-gate-relaxed G-01..G-11 |

## B. Decision memos and records (reviewer)
| Path | sha256 | Bytes | Read-only | Purpose |
|---|---|---|---|---|
| `proposals/2026-10-22_remediation/D-05_DECISION.md` | `6fc07b65c1bb833f9bb9ec88a423b523aa08b57f807a84bc39dbe6e1bfc3fbee` | 51778 | treat as read-only | D-05 combined memo: §3(A) immutable original locks, (B) v2 locks, (C) definition changes; C4 FMR addenda |
| `proposals/2026-10-22_remediation/FMR_OUTCOMES.md` | `76e0379ed9e91996fee6752e5974f8e4fc628485297cdd0d65b7fcc85a31e782` | 26717 | treat as read-only | Neutral FMR record; §6 the four cases O/A/B/C-W2 with sealed-evidence numbers; no recommendation to replace 17.6839565% |
| `proposals/2026-10-22_remediation/TRACK_E_CORRECTIVE_DRAFT.md` | `2046f4633653d5dd525608878d4dbd8909c76aa9e2989ea48b2d6589ef7dc991` | 17893 | treat as read-only | Paste-ready additive corrective decision + erratum for Track E (apply with its dated D1 note) |
| `proposals/2026-10-22_remediation/FINAL_PLAN.md` | `cb9644c05ee078ed210cf47fec1d2d6023543100f0d190ac690fd82588dba97c` | 13251 | treat as read-only | Earlier F1-F5 verdicts and the three rulings (history/context) |
| `proposals/2026-10-22_remediation/REVIEW.md` | `8ced43573f476e264bdb05d0374c7d51e51d68765202985f46fe8466622b1db5` | 40332 | treat as read-only | Detailed methods review history (context) |

## C. Governance decisions (Coordinator-recorded; read-only)
| Path | sha256 | Bytes | Read-only | Purpose |
|---|---|---|---|---|
| `decisions/2026-10-22_formal_governance_decisions.md` | `090a630665aeba727dc3002c95d2607bff8da3849123e2079c976350016828f8` | 3358 | READ-ONLY (mode) | Recorded by the Coordinator as Kevin's decisions (D1-D3, conditions 1-9) |
| `decisions/2026-10-22_formal_governance_decisions.md.sha256` | `2494b357ff44de9724566987b5dcf27311f115a2bfdbcd6808abe7bd1fcdd8bd` | 108 | READ-ONLY (mode) | companion hash |
| `decisions/2026-10-22_five_governance_answers.md` | `6af3bc51ed4a482186839dc38ce540ace37bfdb6867f47c53d31fcc73783a7a0` | 3204 | READ-ONLY (mode) | Recorded by the Coordinator as Kevin's answers (D1-D5) |
| `decisions/2026-10-22_five_governance_answers.md.sha256` | `d7f39d6341e0dae84a447f969ce71296bc1271348c37c78baaa352778aa13505` | 104 | READ-ONLY (mode) | companion hash |
| `decisions/2026-10-22_hud_contact_authorization.md` | `53bc916d92955a0e481d389787a4152e85772887fc9e76541c78d0006a639836` | 1664 | READ-ONLY (mode) | Recorded by the Coordinator as Kevin's order (04-27/28 label fix; HUD-contact authorization) |
| `decisions/2026-10-22_hud_contact_authorization.md.sha256` | `9bcd755a43f929ed88cbc13b0d4996b34a02087a252f7411e8449d83bc546c0d` | 106 | READ-ONLY (mode) | companion hash |
| `decisions/2026-10-22_spec_questions_resolved.md` | `9e6f1b757e6c7424dc23f4b53466811e194a1e2b3e26707499bb360352f96800` | 1501 | READ-ONLY (mode) | Recorded by the Coordinator as Kevin's resolution ((a) v1=fb58ddc, (b) housing validation) |
| `decisions/2026-10-22_spec_questions_resolved.md.sha256` | `19bae408760156a03431ae710084837a7c9ff6f5f89c30b2647f26db4250f134` | 104 | READ-ONLY (mode) | companion hash |

## D. Sealed evidence (SHA256SUMS; each verified 0 failures with sha256sum -c)
| Path | sha256 | Bytes | Read-only | Purpose |
|---|---|---|---|---|
| `proposals/2026-10-22_remediation/evidence_e45eb87/SHA256SUMS` | `19f8d242893e4cc17046cbef4a4cda5717e198a67a3d6da5e68a36fad9cbe038` | 6389 | READ-ONLY (mode) | e45eb87 remediation evidence (Engineer) |
| `proposals/2026-10-22_remediation/evidence_final_tree/SHA256SUMS` | `73fd7804658b68647587fbfd99cc980cdf776a571af94ca524fc3d5c5652799d` | 4829 | READ-ONLY (mode) | e45eb87 final-tree national rerun 6/6, 80/80 (Engineer) |
| `proposals/2026-10-22_remediation/evidence_2734062_step1/SHA256SUMS` | `355d3d339b9e1f13a965ee771a16a1b348c63f1118a60be0d40fad3dddeb5153` | 5947 | READ-ONLY (mode) | 2734062 step 1 (Engineer) |
| `proposals/2026-10-22_remediation/evidence_2734062_step2/SHA256SUMS` | `5e3b8c4a158045468521538cf64dec9050125ab2fdb0ecb38381e2355a1a2776` | 6972 | READ-ONLY (mode) | 2734062 step 2 (Engineer) |
| `proposals/2026-10-22_remediation/evidence_2734062_step3/SHA256SUMS` | `04a5ac8e2e4cb4e7bbbb0fe60522696bd7b05f4e03bac0f211bb669aeeef31c3` | 11254 | READ-ONLY (mode) | 2734062 matched-year reproduction runs A/C/D (Engineer) |
| `proposals/2026-10-22_remediation/evidence_2734062_step4/SHA256SUMS` | `575eda0687cc5a7957e8c10964f870777e2f98699e37cfa4ce6fa6777e756132` | 7507 | READ-ONLY (mode) | FMR sensitivity readings A and B (Engineer) |
| `proposals/2026-10-22_remediation/evidence_2734062_step4_w2/SHA256SUMS` | `117a1ba6766877f214c04300523c86b158e12a17d4b66e533916ccb2900bd5d8` | 4106 | READ-ONLY (mode) | FMR sensitivity C-W2 (Engineer); satisfies 9a sensitivity part |
| `proposals/2026-10-22_remediation/evidence_2734062_step5/SHA256SUMS` | `deac0fd2fd96bc7f48f647e29e520990689dfe6ed2dd51716bc7424a315483c3` | 6814 | READ-ONLY (mode) | BLS hash and dependency checks (Engineer) |
| `proposals/2026-10-22_remediation/F1v2_F4_F2_evidence/SHA256SUMS` | `d3320b279c82bd9dc26ea5ee4a894d951174f81321d798e45907fba1d7b059ae` | 3733 | treat as read-only | F1_v2/F4/F2 evidence (Engineer) |
| `proposals/2026-10-22_remediation/F1v2_manifest_F3b_v2_evidence/SHA256SUMS` | `a97bacd95b5022f521c3c49f4e7f0996139d825db0d15f5ab926bd875caeb8bd` | 1083 | treat as read-only | manifest v2 / F3b_v2 evidence (Engineer) |
| `/workspace/hesi-data/fmr_effective_dates/SHA256SUMS` | `803d5c5b408314cbc0ea9b6ec8f061d5e3b08ecec7f9a1950dc3694c81fc3900` | 11759 | treat as read-only | Federal Register / HUD sources for FMR effective dates (Data Scout) |
| `/workspace/hesi-data/hud_inquiry/SHA256SUMS` | `2b95509b1c61ba4ca50a3a5348f6ccff529d99c1ea15cee1c1999f9ba552e48e` | 2181 | treat as read-only | HUD channel evidence (Data Scout) |

## E. Engineer candidate patch set (scratch; not verified as a whole by the reviewer)
| Path | sha256 | Bytes | Read-only | Purpose |
|---|---|---|---|---|
| `proposals/2026-10-22_remediation/integrity_v2/01_F1_v2_pums_ingestion_hardening.diff` | `e511816d0d50a7c85054144731ae76c8c734619c12d21dca016733ba12ab7418` | 32927 | treat as read-only | Engineer integrity_v2 candidate diff (base 2734062); input to Cursor, to be verified by the acceptance tests |
| `proposals/2026-10-22_remediation/integrity_v2/02_F1_v2_valid_input_test.diff` | `c522038f71d69de85a0f6d444b06e19073633de7f9b8eb22e8983f9d5d100366` | 3164 | treat as read-only | Engineer integrity_v2 candidate diff (base 2734062); input to Cursor, to be verified by the acceptance tests |
| `proposals/2026-10-22_remediation/integrity_v2/03_drop_test_lock_override.diff` | `317a6127cac81d8eee4413e303b565b26eb26d0f2ce18d40f25f9be893dc887d` | 13350 | treat as read-only | Engineer integrity_v2 candidate diff (base 2734062); input to Cursor, to be verified by the acceptance tests |
| `proposals/2026-10-22_remediation/integrity_v2/04_output_guard_F6_folded.diff` | `9ad7f005c50fcfb68eef24d7e8da94b2c72221210ff3e75f410bd073b60a9333` | 22084 | treat as read-only | Engineer integrity_v2 candidate diff (base 2734062); input to Cursor, to be verified by the acceptance tests |
| `proposals/2026-10-22_remediation/integrity_v2/05_matched_food_cache_hardening.diff` | `ea771e54113552ccd48bddf103227511447c65fa44fa4e980e0768914bce5e16` | 17382 | treat as read-only | Engineer integrity_v2 candidate diff (base 2734062); input to Cursor, to be verified by the acceptance tests |
| `proposals/2026-10-22_remediation/integrity_v2/06_F2_bls_hash_three_refs_errata.diff` | `ed045053a9d605501fbf7a13133df1679fb0cd30992bfecfa105e26443f40aca` | 7467 | treat as read-only | Engineer integrity_v2 candidate diff (base 2734062); input to Cursor, to be verified by the acceptance tests |
| `proposals/2026-10-22_remediation/integrity_v2/07_F4_requirements_dev_pytest.diff` | `9d6fb892d6b6f449e89c31e66bd1c56c3038618c0eeb384db8f61e04f36bc9e8` | 260 | treat as read-only | Engineer integrity_v2 candidate diff (base 2734062); input to Cursor, to be verified by the acceptance tests |
| `proposals/2026-10-22_remediation/integrity_v2/08_F5_status_wording_additive.diff` | `1e47c5dcbc7479a14e348c11c2d062c39f9cdc36aad27682cf4237d76a02ea6e` | 1709 | treat as read-only | Engineer integrity_v2 candidate diff (base 2734062); input to Cursor, to be verified by the acceptance tests |
| `proposals/2026-10-22_remediation/integrity_v2/09_v1_fb58ddc_manifest_restore_history.diff` | `584c8fa807ba62cdc0ebc151fc3f3985cb1c1a8c2b64256c0fc97eb9b968d0d3` | 6027 | treat as read-only | Engineer integrity_v2 candidate diff (base 2734062); input to Cursor, to be verified by the acceptance tests |
| `proposals/2026-10-22_remediation/integrity_v2/10_verify_package_manifest_v1_default_v2_explicit.diff` | `a67e0ca6ded73fb6823697153447cf5fc11d77c7383a89d5feff0564f009f701` | 17243 | treat as read-only | Engineer integrity_v2 candidate diff (base 2734062); input to Cursor, to be verified by the acceptance tests |
| `proposals/2026-10-22_remediation/integrity_v2/11_refresh_release_hashes_no_overwrite.diff` | `89b1ac8533a8829d86b4489f69a116ff017210c343d129b0353f293f8a0ad0ae` | 7780 | treat as read-only | Engineer integrity_v2 candidate diff (base 2734062); input to Cursor, to be verified by the acceptance tests |
| `proposals/2026-10-22_remediation/integrity_v2/12_core_RELEASE_FILE_HASHES_v2_PROPOSED.diff` | `a7d8310384b018dae8551027049d17d28ce8327b8fd860223d7ce2d9a5e0b75f` | 14512 | treat as read-only | Engineer integrity_v2 candidate diff (base 2734062); input to Cursor, to be verified by the acceptance tests |
| `proposals/2026-10-22_remediation/integrity_v2/13_pillar_LOCK_v2_verify_release_v2.diff` | `3ce49397b3643af588a173f1704853f21f4799fd4597d5a4b9d8a7e1ac8ea8e0` | 43614 | treat as read-only | Engineer integrity_v2 candidate diff (base 2734062); input to Cursor, to be verified by the acceptance tests |
| `proposals/2026-10-22_remediation/integrity_v2/ALL_integrity_v2_on2734062.diff` | `635f863512dd9a614cde85cb775a57c4c3232df6abed823b5d098aff8b5f4b49` | 175068 | treat as read-only | Engineer integrity_v2 candidate diff (base 2734062); input to Cursor, to be verified by the acceptance tests |

## F. Findings
| Path | sha256 | Bytes | Read-only | Purpose |
|---|---|---|---|---|
| `findings/methods-reviewer/2026-10-22_fb58ddc_v1_verification.md` | `9949497acda4db5a394d7f27100ab702d7377a2784ca35312b048eeb0d1c6c9c` | 15355 | treat as read-only | (a) verification: fb58ddc PASS with documented earlier changes; housing structure (b) |
| `findings/methods-reviewer/2026-10-22_baseline_review.md` | `999237b7ae7e29257827d370a8c4f35788e2430b758e6f8b42f3f9b506086448` | 33005 | treat as read-only | Baseline and delta review (MR-, D- findings) |
| `findings/data-scout/2026-10-22_matched2024_provenance.md` | `fb01f79ee1c8bdcb862b38778c7de1428f3972fcd578f03cdec64ee93d3497e3` | 15375 | treat as read-only | 12 reevaluation areas provenance (Data Scout) |
| `findings/data-scout/2026-10-22_fmr_effective_dates.md` | `61459eba822725088dcb5362387c456bdced965df1edfb7623b85c08989e6877` | 14791 | treat as read-only | FMR effective dates, W1/W2, Honolulu (Data Scout) |
| `findings/data-scout/2026-10-22_hud_inquiry_draft.md` | `32300cdb119c2731bf06b0a607e9292e7258608d98d2cd1462e20355c54d6f53` | 9624 | treat as read-only | HUD inquiry DRAFT, not sent (Data Scout); Part 2 |
| `findings/data-scout/2026-10-22_source_register.md` | `ced55100f7bf1ef611c9bfd9f56da31900d1359a6c715658a2aea4ee79c10e1a` | 16617 | treat as read-only | Source register (Data Scout) |
| `findings/reproducer/2026-10-22_F1v2_manifest_F3b_v2.md` | `4eeaece1b0876bcda516266e3b98830635f665b6282f4c2cea489dfa708849cd` | 15380 | treat as read-only | Engineer: manifest v2, F3b_v2 |
| `findings/reproducer/2026-10-22_2734062_step3_matched2024.md` | `0dcf8ac850edaf5673d23171ed4f21d35d12d28a553eef943923de9d41b8f605` | 11447 | treat as read-only | Engineer: matched-year reproduction |
| `findings/reproducer/2026-10-22_2734062_step4_fmr_sensitivity.md` | `79fc34b664ac7177fc001b31a12208c9c879e3671afe56549622da6dcd9f8301` | 8649 | treat as read-only | Engineer: readings A/B |
| `findings/reproducer/2026-10-22_2734062_step4_w2.md` | `4c43c636748cc93965ab4d0f0eeb037c080cf2f6587b5b52087f4369ce8b3b52` | 8314 | treat as read-only | Engineer: C-W2 |
| `findings/reproducer/2026-10-22_2734062_step5_bls_deps.md` | `ee9c32ea34abe0a75fade5ee6b51ab0e8f826c8dac0dd64e95ec25931e111a44` | 8337 | treat as read-only | Engineer: BLS and dependencies |
| `findings/reproducer/step6_STATUS.md` | `5220c1959bb5317b394728fddfd4351513993b5bd7dd5ce82dff61be0f6c3eba` | 1935 | treat as read-only | Engineer: status |

## G. Reviewer tools (scratch)
| Path | sha256 | Bytes | Read-only | Purpose |
|---|---|---|---|---|
| `scratch/methods-reviewer/acceptance/no_gate_relaxed.py` | `2244a4378d72f29cc521d0f3c0a87285542f2a2611246277f54ca7ff5b8cf1be` | 1700 | treat as read-only | G-01 reference script |
| `scratch/methods-reviewer/fb58_v1/v1check.py` | `b63fd3d78b03282b58d22f4d38ce85bd03e9d4117fab30b639098f024f7c0188` | 1645 | treat as read-only | P-24 reference implementation (manifest recomputation via git show) |
| `scratch/methods-reviewer/fb58_v1/v1check.out` | `1a056afabc83f6b8184781f23c3564001275dca46b45eb9394725a774ce039cb` | 2486 | treat as read-only | P-24 output at d658c08..2734062 |
| `scratch/methods-reviewer/hus_probe/hus_probe.log` | `3425633180c5aa9f071fe558158947ab7c8b9f892f93755bd64a0032332dea8a` | 1000 | treat as read-only | Housing verifier probe at 2734062 (N-60/N-61 baseline behaviour) |
| `CHARTER.md` | `7ed6076ad8219c84974266ecb1190f21ab22870899d58f8c276c78215acbbb00` | 6214 | treat as read-only | Team charter (rules for all agents) |

## Notes
- Not listed on purpose: the Census ZIPs (`csv_pus.zip` `afdc6d90…`, `csv_hus.zip` `8281008e…`; hashes in `core_r24/PUMS_ARCHIVE_LOCK.json`) and the operator-local tract files. Cursor obtains them from Census or Kevin; they are not redistributed here.
- Findings copies of the reviewer files under `findings/methods-reviewer/` are byte-identical copies of the proposal files and are not listed twice.
- This manifest cannot contain its own hash; it is reported with the deliverable and in `CURSOR_PACKAGE_MANIFEST.md.sha256`.

---

## Dated note 2026-10-22 (about 06:50 UTC): files updated after this manifest was built (additive; the table above is kept as built at 06:14:30Z)
> AI methods review, not independent human peer review. The rows above for the spec and the tests are superseded by these values (VERIFIED with `sha256sum`/`stat` at the time of this note):

| Path | sha256 | Bytes | Read-only | Purpose |
|---|---|---|---|---|
| `proposals/2026-10-22_remediation/CURSOR_IMPLEMENTATION_SPEC.md` | `71090b3e90f17d7016218352fb44c34d5b9d02877a5002cc315f59748f2544a9` | 56407 | treat as read-only | spec + 06:40Z RELEASE-BLOCKING/baseline note |
| `proposals/2026-10-22_remediation/ACCEPTANCE_TESTS.md` | `e920114e51bd8c3860f3ee6d3962b098efe8c7d8c337365f314611752439ecfd` | 82397 | treat as read-only | 127 tests incl. Addendum A5 |
| `findings/methods-reviewer/2026-10-22_fb58ddc_v1_verification.md` | `ba1d84dc129b8ab87d99b47c418052b303e8dee065ab273d706612451e2f2e11` | 16464 | treat as read-only | (a) verification + baseline-status note |
| `findings/methods-reviewer/CANDIDATE_REVIEW_TEMPLATE.md` | `c476d69ae9f5075d9685d8db643e4b7209e1c4f6a6e09988534a651f473d90dd` | 28987 | treat as read-only | per-test candidate review template (127 IDs + CH-01..21) |
| `decisions/2026-10-22_final_remediation_priorities.md` | `d8555f09e7990ae1edb8433480c8378e548878d02358d6f1deeb6019f27f01c0` | 1200 | READ-ONLY (mode) | Coordinator record of Kevin priorities (CH-19/CH-21 release-blocking) |
| `decisions/2026-10-22_final_remediation_priorities.md.sha256` | `5cfc277bd8e66e113448e5be7004658470774d82d27d9fcfe434cb0dbb249661` | 109 | READ-ONLY (mode) | companion hash |
| `decisions/DECISION_REGISTER.md` | `a41961d2dac1da6db81a8d3c17aff4e15787fa3abae706cef2111dff2b346e70` | 1262 | treat as read-only | Coordinator decision register (writable on disk; append-only by policy) |

This note changes the manifest file itself, so its new sha256 is in `CURSOR_PACKAGE_MANIFEST.md.sha256` (regenerated) and in the report.

<!-- END FILE: CURSOR_PACKAGE_MANIFEST.md -->
