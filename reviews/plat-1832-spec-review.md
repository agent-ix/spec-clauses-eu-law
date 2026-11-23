---
id: SR-016
title: "Spec review — Annex 11 clause set (producer claims, rights, sources)"
type: SpecReview
analysis: base
scope: "agent-ix/spec-clauses-eu-law; PR #21 diff: spec/spec.md Annex 11 sections, FR-023..FR-028, NFR-004"
review_set: subset
date: 2026-11-23
---

## Summary

Ticket: PLAT-1832. Reviewed `git diff origin/main...HEAD` at fa6a43513c94460e2c62277023523f824f4d84c1 of agent-ix/spec-clauses-eu-law PR #21. Method: spec-review.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | Annex 11 binds `verification-records` (clauses 4.1, 4.6, 4.7, 4.8, 5, 6), a name in the US Part 11 catalog (us-fda-21-cfr-11-2026-11-12.json and us-health spec.md: "`quire matrix` / `quoin matrix` results and `quoin evidence record`."), but the EU catalog row  | spec/functional/FR-025-annex-11-output-bindings.md:24 |
| FND-002 | medium | The bindings table names producers that are not quoin or engineering-assurance commands: `quire validate` (baseline-record, software-requirements), "git history", "Allowed-signers file", "Authored spec artifacts", "Authored safety and security records". | spec/functional/FR-025-annex-11-output-bindings.md:26 |
| FND-003 | low | The catalog description of `record-export` names `quoin matrix` and `approval-trail --format table`, while the bindings row at spec/spec.md:256 also names `quoin evidence audit`. | spec/spec.md:387 |
| FND-004 | medium | "... Annex 22, and Chapter 4; none is in force" is false for Chapter 4: EudraLex Volume 4 Chapter 4 (Documentation) is in force. | spec/spec.md:36 |
| FND-005 | low | Several summaries track the official wording closely (checked against the January 2011 PDF): 17 "checked for accessibility, readability and integrity" (source: "should be checked for accessibility, readability and integrity"), 14(b) "permanently linked to thei | spec/spec.md:208,227,232,233,236 |

## Finding details

### FND-001 — FR-025-AC-2

Annex 11 binds `verification-records` (clauses 4.1, 4.6, 4.7, 4.8, 5, 6), a name in the US Part 11 catalog (us-fda-21-cfr-11-2026-11-12.json and us-health spec.md: "`quire matrix` / `quoin matrix` results and `quoin evidence record`."), but the EU catalog row at spec/spec.md:351 reads "Test matrix and retained evidence." FR-025-AC-2 therefore fails on the spec as written, and the shared-name list in Annex 11 Output Bindings (spec/spec.md:242) omits `verification-records`. Other names Annex 11 uses (risk-management-records, software-requirements, software-architecture, anomaly-list) also differ from the US Health-Law catalog that FR-006 makes canonical.

Expected fix: Align the EU catalog descriptions of verification-records (and the other shared names Annex 11 uses) with the US catalog, and add verification-records to the shared-name list at spec/spec.md:242.

### FND-002 — FR-025-AC-4

The bindings table names producers that are not quoin or engineering-assurance commands: `quire validate` (baseline-record, software-requirements), "git history", "Allowed-signers file", "Authored spec artifacts", "Authored safety and security records". A test written to this AC either fails on real rows or needs an undeclared exemption list. All named quoin/EA commands do exist (verified: quoin 0.36.8 and quoin origin/main 70aa08ad; engineering-assurance 0.10.1 and origin/main b44cfe9e2), so the defect is the AC, not the bindings.

Expected fix: Split the table into a producer-command column (quoin, quire or engineering-assurance subcommand, checked against that CLI's command list) and a free-text source column for non-command inputs; scope the AC to the command column and include quire.

### FND-003 — spec.md#catalog-record-export

The catalog description of `record-export` names `quoin matrix` and `approval-trail --format table`, while the bindings row at spec/spec.md:256 also names `quoin evidence audit`. Same output, two producer lists.

Expected fix: Make the catalog description and the bindings row name the same producers.

### FND-004 — spec.md#scope-out-annex-11

"... Annex 22, and Chapter 4; none is in force" is false for Chapter 4: EudraLex Volume 4 Chapter 4 (Documentation) is in force. Only the 2025 draft revision of Chapter 4 (and the new draft Annex 22) is not.

Expected fix: Say "the 2025 consultation drafts of a revised Annex 11, a revised Chapter 4 and a new Annex 22; none is in force".

### FND-005 — spec.md#annex-11-clause-table

Several summaries track the official wording closely (checked against the January 2011 PDF): 17 "checked for accessibility, readability and integrity" (source: "should be checked for accessibility, readability and integrity"), 14(b) "permanently linked to their record", 14(c) "include the time and date applied", 12.2 "Extent of security controls follows system criticality", 3.4 "... available to inspectors on request". No full sentence is copied and reuse is CC BY 4.0, so the risk is low. But NFR-004 and FR-024 promise original summaries, and the clause JSON will copy these rows.

Expected fix: Reword those five summaries in the pack's own phrasing before they reach the clause JSON.

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

## New findings (disposition pass 1)

Reviewed `git diff fa6a4351..ceb584e0`.

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-006 | high | Merged alone, this spec-only PR turns the repo red. The fix for FND-001 rewrote the EU catalog descriptions of risk-management-records, software-requirements, software-architecture, verification-records, anomaly-list and release-record in s | spec/functional/FR-025-annex-11-output-bindings.md:24 |
| FND-007 | low | FR-025 and its AC-2, plus the shared-name paragraph in Annex 11 Output Bindings, call the comparison source the 'US Part 11 catalog'. Of the listed names, release-record, risk-management-records, software-requirements, software-architecture | spec/functional/FR-025-annex-11-output-bindings.md:17 |

### FND-006 — FR-025-AC-2

Merged alone, this spec-only PR turns the repo red. The fix for FND-001 rewrote the EU catalog descriptions of risk-management-records, software-requirements, software-architecture, verification-records, anomaly-list and release-record in spec/spec.md. The shipped MDR, MDCG, GDPR, AI Act and Annex IV clause JSON still carry the old descriptions, and tests/test_clause_sets.py parses the spec.md catalog and compares it to them. Measured at ceb584e0: 5 tests fail that pass on origin/main 'test_mdr_declares_the_spec_catalog_subset_used_by_its_clauses', 'test_mdcg_declares_the_spec_catalog_subset_used_by_its_clauses', 'test_gdpr_clause_ids_fields_and_catalog_match_the_spec', 'test_ai_act_clause_ids_applicability_and_outputs_match_the_spec' and 'test_ai_act_annex_rows_match_the_normative_table'.

Expected fix: Update the outputCatalog descriptions in the five shipped clause JSON files in this PR, or land it together with the implementation PR.

### FND-007 — FR-025

FR-025 and its AC-2, plus the shared-name paragraph in Annex 11 Output Bindings, call the comparison source the 'US Part 11 catalog'. Of the listed names, release-record, risk-management-records, software-requirements, software-architecture, soup-list, security-risk-records and anomaly-list are not in us-fda-21-cfr-11-2026-11-12.json outputCatalog. They are in the US Health-Law Output Catalog in us-health spec/spec.md, which FR-006 names as canonical.

Expected fix: Say 'US Health-Law Output Catalog (the FR-006 comparison source)' instead of 'US Part 11 catalog'.

## Dispositions

Round 1 at head ceb584e0c8c0568364f5b31d71739718800a4690; round 2 at head b936c7ba3920b9298fb3d7d52b4ece8678dc066f (rows appended after round 1).

| FND | outcome | reason |
|---|---|---|
| FND-001 | fixed | - |
| FND-002 | fixed | - |
| FND-003 | fixed | - |
| FND-004 | fixed | - |
| FND-005 | fixed | - |
| FND-006 | deferred | Coordinator decision: PR #21 will be rebased on #22 and gain the Annex 11 JSON, tests and corpus before it merges. The five test_clause_sets.py catalog-parity failures are a merge-order condition, not a spec-content defect. Re-check that the suite is green on the rebased head before merging. |
| FND-007 | still-open | FR-025 and FR-025-AC-2 now say 'US Health-Law Output Catalog', but spec/spec.md:242 (the Annex 11 Output Bindings paragraph) still says 'Expected outputs that already exist in the US Part 11 catalog (...) keep that catalog's kind and description exactly', and its list includes names that are not in the Part 11 set. Change that one phrase to 'US Health-Law Output Catalog'. |
