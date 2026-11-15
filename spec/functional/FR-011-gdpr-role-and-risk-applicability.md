---
id: FR-011
title: "GDPR role, risk, and records applicability"
type: FR
relationships:
  - target: "ix://agent-ix/spec-clauses-eu-law/US-001"
    type: "traces_to"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-010"
    type: "depends_on"
---
# FR-011: GDPR role, risk, and records applicability

## Description

The module SHALL evaluate GDPR clause applicability from the person-supplied
`gdpr_role`, `high_risk_processing`, and
`article_30_records_applicability` dimensions as defined in `spec.md`.

The module SHALL NOT infer these values from product type, data type, a risk
score, or another dimension.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-011-AC-1 | For `gdpr_role=controller`, `high_risk_processing=yes`, and `article_30_records_applicability=applies`, Articles 25, 30(1), 32, and 35 clauses are binding, and Article 30(2) clauses are not binding. | Test |
| FR-011-AC-2 | For `gdpr_role=processor` and `article_30_records_applicability=applies`, Article 30(2) and Article 32 clauses are binding; Articles 25, 30(1), and 35 clauses are not binding. | Test |
| FR-011-AC-3 | For `gdpr_role=controller`, `high_risk_processing=no`, and `article_30_records_applicability=applies`, Article 35 clauses are not binding while Articles 25, 30(1), and 32 retain their specified applicability. | Test |
| FR-011-AC-4 | If a role- or high-risk-dependent dimension is missing, each clause depending on it is unresolved; clauses without applicability expressions remain binding. | Test |
| FR-011-AC-5 | `article_30_records_applicability=exempt` makes Article 30(1) through (4) not binding. When it is `applies`, Articles 30(3) and (4) are binding for either role; 30(1) is binding for a controller and not binding for a processor; 30(2) is binding for a processor and not binding for a controller. When the value is missing, 30(1) is unresolved for a controller and not binding for a processor; 30(2) is unresolved for a processor and not binding for a controller; and 30(3) and (4) are unresolved for either role. If `gdpr_role` is also missing, Articles 30(1) through (4) are all unresolved. | Test |

## Dependencies

The IDs, force, and expressions are specified by [FR-010](./FR-010-gdpr-clause-table.md).
