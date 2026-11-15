---
id: FR-011
title: "GDPR role and high-risk applicability"
type: FR
relationships:
  - target: "ix://agent-ix/spec-clauses-eu-law/US-001"
    type: "traces_to"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-010"
    type: "depends_on"
---
# FR-011: GDPR role and high-risk applicability

## Description

The module SHALL evaluate GDPR clause applicability from the person-supplied
`gdpr_role` and `high_risk_processing` dimensions as defined in `spec.md`.

The module SHALL NOT infer either dimension from product or data-flow content.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-011-AC-1 | For `gdpr_role=controller` and `high_risk_processing=yes`, Articles 25, 30(1), 32, and 35 clauses are binding, and Article 30(2) clauses are not binding. | Test |
| FR-011-AC-2 | For `gdpr_role=processor`, Article 30(2) and Article 32 clauses are binding; Articles 25, 30(1), and 35 clauses are not binding. | Test |
| FR-011-AC-3 | For `gdpr_role=controller` and `high_risk_processing=no`, Article 35 clauses are not binding while Articles 25, 30(1), and 32 retain their specified applicability. | Test |
| FR-011-AC-4 | With no dimension values supplied, every role- or high-risk-dependent clause is unresolved; clauses without applicability expressions remain binding. | Test |

## Dependencies

The IDs, force, and expressions are specified by [FR-010](./FR-010-gdpr-clause-table.md).
