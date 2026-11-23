---
id: SR-020
title: "Scope-boundary analysis — Annex 11 tool versus person allocation"
type: SpecReview
analysis: scope-boundary
scope: "agent-ix/spec-clauses-eu-law; PR #21 diff: spec/spec.md Annex 11 sections, FR-023..FR-028, NFR-004"
review_set: subset
date: 2026-11-23
---

## Summary

Ticket: PLAT-1832. Reviewed `git diff origin/main...HEAD` at fa6a43513c94460e2c62277023523f824f4d84c1 of agent-ix/spec-clauses-eu-law PR #21. Method: spec-review/spec-scope-boundary-analysis.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | The stated limits that make each binding honest (signer-claimed signing time, deleted tags invisible, no reason-for-change field, attribution without authorisation) live only in spec.md. | spec/functional/FR-025-annex-11-output-bindings.md:17 |

## Finding details

### FND-001 — FR-025

The stated limits that make each binding honest (signer-claimed signing time, deleted tags invisible, no reason-for-change field, attribution without authorisation) live only in spec.md. The shipped clause JSON carries just the catalog description, so a pack user sees `signed-record` with no limit attached. The boundary is correct in the spec but is not carried into the delivered artifact.

Expected fix: Either carry each output's limit into its catalog description, or state in FR-025 that the bindings table is spec-only documentation.

## Scope examined

- spec.md#annex-11-set-design (examined)
- spec.md#annex-11-rights (examined)
- spec.md#annex-11-clause-table (examined)
- spec.md#annex-11-output-bindings (examined)
- spec.md#annex-11-part-11-crosswalk-policy (examined)
- spec.md#scope-out-annex-11 (examined)
- FR-023 (examined)
- FR-024 (examined)
- FR-025 (examined)
- FR-026 (examined)
- FR-027 (examined)
- FR-028 (examined)
- NFR-004 (examined)
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
- FR-027-AC-1 (examined)
- FR-027-AC-2 (examined)
- FR-027-AC-3 (examined)
- FR-027-AC-4 (examined)
- FR-027-AC-5 (examined)
- FR-028-AC-1 (examined)
- FR-028-AC-2 (examined)
- FR-028-AC-3 (examined)

## Verdict

Not mergeable until the high findings are fixed. All 13 Part 11 crosswalk targets resolve in us-fda-21-cfr-11-2026-11-12.json (spec-clauses-us-health origin/main c5a8ca8), and the partial/informative strengths are defensible. Every named quoin and engineering-assurance command exists. The version-in-force claim matches the Commission listing ("revision January 2011"). The rights wording is truthful: the PDF has no licence statement of its own. No tool assigns a score, class or criticality, and the clause table covers every numbered paragraph of the 2011 text. No AC pins counts, versions or hashes. No ticket or roadmap narration was added.


## New findings (disposition pass 2)

Reviewed `git diff ceb584e0..b936c7ba`.

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-002 | low | Two rows of the new Annex 11 Tool Limits table fall outside the selection rule that AC-6 and the Tool Limits paragraph state ('a producer command and a limit other than None'). 'signer-registry' has producer 'none' (spec/spec.md:248), and ' | spec/functional/FR-025-annex-11-output-bindings.md:28 |

### FND-002 — FR-025-AC-6

Two rows of the new Annex 11 Tool Limits table fall outside the selection rule that AC-6 and the Tool Limits paragraph state ('a producer command and a limit other than None'). 'signer-registry' has producer 'none' (spec/spec.md:248), and 'security-risk-records' now has limit 'None' (spec/spec.md:252). Yet the table gives each a 'Tool limit:' sentence (spec/spec.md:268 and the risk row). A test that derives clauses from the rule will not require the registry sentence on 12.3, 12.4 and 14(a), or the risk sentence on 12.2. A reader of the table expects both. The signer-registry limit is real, the same gap SR-020 FND-001 named.

Expected fix: Make the rule and the table agree. Either select every shared output whose bindings row states a limit other than None, whatever its producer (which keeps signer-registry), and give security-risk-records its limit back in the bindings row; or drop the two rows from the Tool Limits table.

## Dispositions

Round 1 at head ceb584e0c8c0568364f5b31d71739718800a4690; round 2 at head b936c7ba3920b9298fb3d7d52b4ece8678dc066f (rows appended after round 1).

| FND | outcome | reason |
|---|---|---|
| FND-001 | still-open | The fix adds the mechanism (limits in Annex-11-only descriptions, and 'Tool limit:' sentences for shared names) but covers only 7 clauses, and FR-025-AC-6 checks only the clauses in that table. Clauses that bind a shared output whose stated limit never reaches the shipped text: verification-records (no adequacy judgement) on 4.6, 4.7, 4.8, 5 and 6; signed-record (signer-claimed time) on 7.1 and 14(b); signer-registry on 12.4 and 14(a); anomaly-list on 4.2 and 13; risk-management-records on 1; security-risk-records on 12.2; soup-list on 3.3. The 12.4 sentence also names quoin actor labels, which are not among 12.4's outputs. Either add a limit sentence to every clause that binds a limited shared output and make AC-6 derive the clause list from the bindings table, or narrow FR-025's 'each binding's limit' to the listed clauses. |
| FND-001 | fixed | - |
