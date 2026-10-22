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
