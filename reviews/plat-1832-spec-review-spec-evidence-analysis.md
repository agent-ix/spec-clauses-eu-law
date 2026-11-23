---
id: SR-019
title: "Evidence analysis — Annex 11 acceptance criteria"
type: SpecReview
analysis: evidence
scope: "agent-ix/spec-clauses-eu-law; PR #21 diff: spec/spec.md Annex 11 sections, FR-023..FR-028, NFR-004"
review_set: subset
date: 2026-11-23
---

## Summary

Ticket: PLAT-1832. Reviewed `git diff origin/main...HEAD` at fa6a43513c94460e2c62277023523f824f4d84c1 of agent-ix/spec-clauses-eu-law PR #21. Method: spec-review/spec-evidence-analysis.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | "cannot discharge a clause among `1`, ..., `12.2` or `16`'s risk scaling" does not say whether the whole clause or only a risk-scaling decision within it is meant. | spec/functional/FR-028-annex-11-human-decisions.md:21 |
| FND-002 | medium | "marked customer-supplied with kind `procedure` where the catalog says so" is circular, because the AC checks the catalog against itself. | spec/functional/FR-025-annex-11-output-bindings.md:25 |

## Finding details

### FND-001 — FR-028-AC-1

"cannot discharge a clause among `1`, ..., `12.2` or `16`'s risk scaling" does not say whether the whole clause or only a risk-scaling decision within it is meant. If it is the whole clause, then 4.1, 4.4, 9 and 12.2, whose outputs are tool-produced records, can never land in FR-027-AC-1's direct-evidence partition. quoin's direct fact can carry an approvalRef but has no rationale field. A coder cannot write a test that fails on a wrong mapping without picking a reading.

Expected fix: Say which fact kind is required (for example: a disposition with rationale and approvalRef, or a direct fact whose approvalRef names the person who made the risk decision), and for which clauses.

### FND-002 — FR-025-AC-3

"marked customer-supplied with kind `procedure` where the catalog says so" is circular, because the AC checks the catalog against itself. It also lists "Validation", whose output `system-validation` has kind `record`, and omits `access-control`, `written-procedure` and `training-record`, which the bindings table also marks customer-supplied. A wrong kind or a producer wrongly added to one of those rows passes this AC.

Expected fix: List the exact output names that must be customer-supplied (all 12 in the two customer-supplied rows). Assert that no producer command is named for them, and state the expected kind of each separately.

## Scope examined

- FR-023-AC-1 (examined)
- FR-023-AC-2 (examined)
- FR-023-AC-3 (examined)
- FR-023-AC-4 (examined)
- FR-024-AC-1 (examined)
- FR-024-AC-2 (examined)
- FR-024-AC-3 (examined)
- FR-024-AC-4 (examined)
- FR-024-AC-5 (examined)
- FR-025-AC-1 (examined)
- FR-025-AC-2 (examined)
- FR-025-AC-3 (examined)
- FR-025-AC-4 (examined)
- FR-025-AC-5 (examined)
- FR-026-AC-1 (examined)
- FR-026-AC-2 (examined)
- FR-026-AC-3 (examined)
- FR-026-AC-4 (examined)
- FR-027-AC-1 (examined)
- FR-027-AC-2 (examined)
- FR-027-AC-3 (examined)
- FR-027-AC-4 (examined)
- FR-027-AC-5 (examined)
- FR-028-AC-1 (examined)
- FR-028-AC-2 (examined)
- FR-028-AC-3 (examined)
- NFR-004-AC-1 (examined)
- NFR-004-AC-2 (examined)

## Verdict

Not mergeable until the high findings are fixed. All 13 Part 11 crosswalk targets resolve in us-fda-21-cfr-11-2026-11-12.json (spec-clauses-us-health origin/main c5a8ca8), and the partial/informative strengths are defensible. Every named quoin and engineering-assurance command exists. The version-in-force claim matches the Commission listing ("revision January 2011"). The rights wording is truthful: the PDF has no licence statement of its own. No tool assigns a score, class or criticality, and the clause table covers every numbered paragraph of the 2011 text. No AC pins counts, versions or hashes. No ticket or roadmap narration was added.

## Dispositions

Round 1, head ceb584e0c8c0568364f5b31d71739718800a4690.

| FND | outcome | reason |
|---|---|---|
| FND-001 | fixed | - |
| FND-002 | fixed | - |
