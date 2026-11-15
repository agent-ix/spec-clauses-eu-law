---
id: FR-005
title: "MDCG companion and crosswalks"
type: FR
---
# FR-005: MDCG companion and crosswalks

## Description

The MDCG set SHALL use the key, source and section IDs in `spec.md`, with recommended force. Every guidance clause SHALL have at least one crosswalk to a listed MDR clause, relation `informative` or `partial`, and an original rationale.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-005-AC-1 | MDCG IDs equal the table exactly and every crosswalk target resolves to a loaded MDR clause. | Test |
| FR-005-AC-2 | A fixture with a missing target fails the pack test and names the crosswalk. | Test |
| FR-005-AC-3 | All guidance clauses are recommended and use only informative or partial relations. | Test |

## Dependencies

Uses the clause-set, evaluation, publication and discharge contracts already implemented by quire and quoin.
