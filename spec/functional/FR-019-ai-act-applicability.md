---
id: FR-019
title: "AI Act applicability"
type: FR
relationships:
  - target: "ix://agent-ix/spec-clauses-eu-law/US-001"
    type: "traces_to"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-017"
    type: "depends_on"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-018"
    type: "depends_on"
---
# FR-019: AI Act applicability

## Description

The clause sets SHALL use only the person-supplied `ai_high_risk` and `ai_role` dimensions defined in `spec.md`. The tool SHALL NOT infer either value from product characteristics or other records.

## Acceptance Criteria

| ID | Criteria | Verification |
|---|---|---|
| FR-019-AC-1 | With `ai_high_risk=no`, every clause in both sets is `not_binding`. | Test |
| FR-019-AC-2 | With `ai_high_risk=yes` and `ai_role=provider`, all Article 26 clauses are `not_binding` and all provider clauses and Annex IV clauses are binding. | Test |
| FR-019-AC-3 | With `ai_high_risk=yes` and `ai_role=deployer`, Article 26 clauses bind and every provider and Annex IV clause is `not_binding`. | Test |
| FR-019-AC-4 | With an empty context, every clause is `unresolved`; when one dimension is omitted, only clauses depending on that dimension are unresolved. | Test |
| FR-019-AC-5 | No set declares another applicability dimension, and no classification value is derived from a product fact or system output. | Test |

## Dependencies

Applicability expressions are specified in the AI Act tables in `spec.md`. A person decides whether Article 6(1) classification applies and which operator role is relevant.
