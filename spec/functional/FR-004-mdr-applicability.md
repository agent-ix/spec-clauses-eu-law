---
id: FR-004
title: "MDR applicability"
type: FR
---
# FR-004: MDR applicability

## Description

The set SHALL declare only `mobile_platform` for M1 applicability. Clause `I-17.3` uses `mobile_platform=yes`; every other listed MDR clause has no applicability expression. Device class is not a classification dimension in M1.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-004-AC-1 | With `mobile_platform=no`, only `I-17.3` is `not_binding`; with `yes`, all clauses bind. | Test |
| FR-004-AC-2 | With no context, `I-17.3` is unresolved and every other clause binds. | Test |
| FR-004-AC-3 | No other dimension or applicability condition is declared. | Test |

## Dependencies

Uses the clause-set, evaluation, publication and discharge contracts already implemented by quire and quoin.
