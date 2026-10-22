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
