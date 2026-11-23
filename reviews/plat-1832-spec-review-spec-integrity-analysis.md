---
id: SR-017
title: "Integrity analysis — Annex 11 clause set"
type: SpecReview
analysis: integrity
scope: "agent-ix/spec-clauses-eu-law; PR #21 diff: spec/spec.md Annex 11 sections, FR-023..FR-028, NFR-004"
review_set: subset
date: 2026-11-23
---

## Summary

Ticket: PLAT-1832. Reviewed `git diff origin/main...HEAD` at fa6a43513c94460e2c62277023523f824f4d84c1 of agent-ix/spec-clauses-eu-law PR #21. Method: spec-review/spec-integrity-analysis.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | FR-001 (statement and FR-001-AC-1, unchanged by this PR) requires the manifest to list *exactly* the MDR, MDCG, GDPR, AI Act high-risk and AI Act Annex IV sets. | spec/functional/FR-023-annex-11-set-declared.md:23 |
| FND-002 | medium | The risk-scaled paragraph list (FR-028:15, FR-028-AC-1, spec/spec.md:195: 1, 4.1, 4.4, 9, 11, 16) does not match the source. | spec/functional/FR-028-annex-11-human-decisions.md:21 |
| FND-003 | medium | quoin's RMM (`quoin discharge --rmm`, quoin origin/main rust/crates/quoin-assurance/src/discharge/rmm.rs:78,194,282) renders a `Compliance` column whose value is `Compliant` for every clause with a direct fact. | spec/functional/FR-027-annex-11-corpus-discharge.md:30 |
| FND-004 | low | Row 14(a) pairs two targets with two relations by position (`11.10(j)`, `11.100(c)` \| `partial`, `informative`). | spec/spec.md:278 |

## Finding details

### FND-001 — FR-023-AC-1

FR-001 (statement and FR-001-AC-1, unchanged by this PR) requires the manifest to list *exactly* the MDR, MDCG, GDPR, AI Act high-risk and AI Act Annex IV sets. Adding `eu/eu-gmp-annex-11@2011-01` per FR-023-AC-1 makes FR-001-AC-1 fail. The two requirements contradict each other.

Expected fix: Update FR-001's statement and FR-001-AC-1 to include the Annex 11 set (and add the FR-001 edge to FR-023, or the reverse).

### FND-002 — FR-028-AC-1

The risk-scaled paragraph list (FR-028:15, FR-028-AC-1, spec/spec.md:195: 1, 4.1, 4.4, 9, 11, 16) does not match the source. Checked against the January 2011 text: paragraph 11 (periodic evaluation) has no risk-based wording; paragraph 6 (critical data shall be covered by risk management) and paragraph 3.2 (need for a supplier audit based on a risk assessment) are risk-based and are missing. The criticality judgements in 4.3 (critical systems) and 13 (critical incidents) are also absent from the AC list, though the FR-028 statement covers them in prose.

Expected fix: Make the list 1, 3.2, 4.1, 4.4, 6, 9, 16 (plus 12.2 for criticality), drop 11, and add 4.3 and 13 to the AC if criticality decisions are meant to need an approvalRef.

### FND-003 — FR-027-AC-4

quoin's RMM (`quoin discharge --rmm`, quoin origin/main rust/crates/quoin-assurance/src/discharge/rmm.rs:78,194,282) renders a `Compliance` column whose value is `Compliant` for every clause with a direct fact. Read literally, the AC (and the FR-027 statement "SHALL NOT show a ... compliance verdict") fails on every real RMM. Read as "no aggregate verdict", it says nothing the engine does not already guarantee.

Expected fix: State what is forbidden precisely: no aggregate score, percentage or overall compliance determination; the per-clause Compliance column reflects only the recorded discharge state.

### FND-004 — spec.md#annex-11-part-11-crosswalk-policy

Row 14(a) pairs two targets with two relations by position (`11.10(j)`, `11.100(c)` | `partial`, `informative`). Every other row has one relation. A reader or a test parser has to guess the pairing.

Expected fix: Give 14(a) two rows, one per target.

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
- FR-001-AC-1 (context_only)

## Verdict

Not mergeable until the high findings are fixed. All 13 Part 11 crosswalk targets resolve in us-fda-21-cfr-11-2026-11-12.json (spec-clauses-us-health origin/main c5a8ca8), and the partial/informative strengths are defensible. Every named quoin and engineering-assurance command exists. The version-in-force claim matches the Commission listing ("revision January 2011"). The rights wording is truthful: the PDF has no licence statement of its own. No tool assigns a score, class or criticality, and the clause table covers every numbered paragraph of the 2011 text. No AC pins counts, versions or hashes. No ticket or roadmap narration was added.

## New findings (disposition pass 1)

Reviewed `git diff fa6a4351..ceb584e0`.

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-005 | low | The new clause 'its per-clause status column shows only the customer's attested disposition' is not what quoin renders. The RMM Compliance column also shows computed states that nobody attested: Undischarged, Undetermined and Not applicable | spec/functional/FR-027-annex-11-corpus-discharge.md:36 |

### FND-005 — FR-027-AC-4

The new clause 'its per-clause status column shows only the customer's attested disposition' is not what quoin renders. The RMM Compliance column also shows computed states that nobody attested: Undischarged, Undetermined and Not applicable (quoin rmm.rs:193-213). A test written to this wording fails on any open or unresolved clause.

Expected fix: Say that the per-clause column reflects only the recorded discharge state of that clause, and nothing aggregated across clauses.

## Dispositions

Round 1 at head ceb584e0c8c0568364f5b31d71739718800a4690; round 2 at head b936c7ba3920b9298fb3d7d52b4ece8678dc066f (rows appended after round 1).

| FND | outcome | reason |
|---|---|---|
| FND-001 | fixed | - |
| FND-002 | fixed | - |
| FND-003 | fixed | - |
| FND-004 | fixed | - |
| FND-005 | fixed | - |
