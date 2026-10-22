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
