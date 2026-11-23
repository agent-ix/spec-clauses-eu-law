---
id: FR-024
title: "Annex 11 clause table and applicability"
type: FR
relationships:
  - target: "ix://agent-ix/spec-clauses-eu-law/US-001"
    type: "traces_to"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-023"
    type: "depends_on"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-006"
    type: "depends_on"
---
# FR-024: Annex 11 clause table and applicability

## Description

The Annex 11 set SHALL contain exactly the clause identifiers, `recommended` force, applicability expressions and expected outputs in the Annex 11 Clause Table in `spec.md`. Each clause SHALL have an original, non-empty summary that reproduces no Annex 11 sentence and at least one expected output that resolves in the catalog. Every dimension is supplied by a person; a missing value leaves its clauses unresolved and a `no` value makes them not binding. The pack SHALL NOT infer a dimension from the product, the data or any score.

Each clause SHALL carry the title and subjects in the Annex 11 Clause Titles and Subjects table in `spec.md`, and the clause text SHALL be its Clause Table summary followed by the Annex 11 Tool Limits sentences its outputs require.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-024-AC-1 | Evaluation returns exactly the clause IDs in the Annex 11 Clause Table, with no missing or additional IDs. | Test |
| FR-024-AC-2 | Every evaluated clause has force `recommended`, non-empty original text, and at least one expected output that resolves in the catalog. | Test |
| FR-024-AC-3 | With `gmp_regulated_use` unset, every clause is unresolved; with it `no`, every clause is not binding; with it `yes`, clauses without a second dimension bind. | Test |
| FR-024-AC-4 | For each clause with a second dimension, `yes` binds it, `no` makes it not binding, and an unset value leaves it unresolved. | Test |
| FR-024-AC-5 | The set declares no dimension for system criticality or risk class and no clause expression reads one; criticality remains a person's judgment. | Test |
| FR-024-AC-6 | Each clause's title and subjects equal the Clause Titles and Subjects table, and each clause's text equals its summary followed by exactly the tool-limit sentences its expected outputs require, each once. | Test |

## Dependencies

The set identity is defined by [FR-023](./FR-023-annex-11-set-declared.md). Expected outputs are defined by [FR-006](./FR-006-pack-wide-output-catalog.md).
