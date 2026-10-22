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
