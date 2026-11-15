---
id: FR-018
title: "AI Act Annex IV technical documentation"
type: FR
relationships:
  - target: "ix://agent-ix/spec-clauses-eu-law/US-001"
    type: "traces_to"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-016"
    type: "depends_on"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-006"
    type: "depends_on"
---
# FR-018: AI Act Annex IV technical documentation

## Description

The Annex IV set SHALL contain exactly every clause ID in the AI Act Annex IV Table in `spec.md`. Each clause SHALL be mandatory, use provider applicability, declare the table's outputs, and have an original, nonempty summary.

## Acceptance Criteria

| ID | Criteria | Verification |
|---|---|---|
| FR-018-AC-1 | Evaluation returns exactly the Annex IV table's IDs, including all lettered points and no missing, duplicate, or additional IDs. | Test |
| FR-018-AC-2 | Each clause's force, provider applicability, and expected outputs match its table row; every output is a catalog `record` or `document`. | Test |
| FR-018-AC-3 | An injected missing, extra, or altered clause ID or output fails and names the affected clause and field. | Test |
| FR-018-AC-4 | The clause summaries do not reproduce statutory text or name, quote, number, or paraphrase a paywalled or harmonised standard. | Analysis |

## Dependencies

Depends on [FR-016](./FR-016-ai-act-sets-declared.md) and [FR-006](./FR-006-pack-wide-output-catalog.md). The Annex IV table in `spec.md` is exhaustive and includes the selected MDR Annex II target or `none` for every point.
