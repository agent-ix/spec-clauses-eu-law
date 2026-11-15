---
id: FR-003
title: "MDR software clause set"
type: FR
---
# FR-003: MDR software clause set

## Description

The MDR set SHALL use the source, key, version, clause IDs, mandatory force, applicability and expected outputs in the normative MDR table in `spec.md`. Each clause SHALL contain original nonempty summary text. The table is exhaustive for this M1 set.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-003-AC-1 | IDs equal the MDR table exactly, including punctuation and no extra clauses. | Test |
| FR-003-AC-2 | Every clause is mandatory, has original nonempty text and at least one catalog output; set validation succeeds. | Test |
| FR-003-AC-3 | A clause referencing an output missing from its catalog fails validation and names the clause. | Test |

## Dependencies

Uses the clause-set, evaluation, publication and discharge contracts already implemented by quire and quoin.
