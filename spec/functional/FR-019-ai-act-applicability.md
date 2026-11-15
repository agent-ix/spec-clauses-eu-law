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

The clause sets SHALL use the person-supplied `ai_high_risk` and `ai_role` dimensions and Annex IV point-applicability values defined in `spec.md`. The tool SHALL NOT infer any of these values from product characteristics or other records.

## Acceptance Criteria

| ID | Criteria | Verification |
|---|---|---|
| FR-019-AC-1 | With `ai_high_risk=no`, every clause in both sets is `not_binding`. | Test |
| FR-019-AC-2 | With `ai_high_risk=yes`, `ai_role=provider`, and every Annex IV point-applicability value `yes`, all provider and Annex IV clauses bind and Article 26 is `not_binding`. | Test |
| FR-019-AC-3 | With `ai_high_risk=yes` and `ai_role=deployer`, Article 26 binds and every provider and Annex IV clause is `not_binding`, regardless of Annex IV point-applicability values. | Test |
| FR-019-AC-4 | With an empty context, every clause is `unresolved`; omitting any required common or per-point applicability dimension leaves only dependent clauses unresolved. | Test |
| FR-019-AC-5 | The only applicability dimensions are `ai_high_risk`, `ai_role`, and the 23 `ai_annex_iv_<point>_applicable` values enumerated in the Annex IV table; no classification or point-applicability value is derived from a product fact or system output. | Test |

## Dependencies

Applicability expressions are specified in the AI Act tables in `spec.md`. A person decides whether Article 6(1) classification applies and which operator role is relevant.
