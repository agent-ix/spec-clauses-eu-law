---
id: FR-004
title: "MDR applicability"
type: FR
relationships:
  - target: "ix://agent-ix/spec-clauses-eu-law/US-001"
    type: "traces_to"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-003"
    type: "depends_on"
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

Depends on FR-003's normative MDR clause table. Quire evaluates the declared applicability expressions; the EU pack owns the expected outcomes in its context tests. If the `quire clauses evaluate` capability is unavailable, the verification gate fails with the missing executable or capability and does not skip the criterion.
