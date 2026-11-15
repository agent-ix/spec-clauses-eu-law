---
id: FR-012
title: "Human acceptance of DPIA residual risk"
type: FR
relationships:
  - target: "ix://agent-ix/spec-clauses-eu-law/US-001"
    type: "traces_to"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-010"
    type: "depends_on"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-011"
    type: "depends_on"
---
# FR-012: Human acceptance of DPIA residual risk

## Description

The module SHALL require a named person's approval reference when evidence
claims to discharge an Article 35 clause by presenting a DPIA whose residual
risk was accepted. No tool SHALL score the DPIA or accept its residual risk.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-012-AC-1 | An Article 35 direct fact citing a DPIA is accepted only when it includes an approval reference identifying the named person who accepted residual risk. | Test |
| FR-012-AC-2 | An Article 35 `accepted_risk` disposition is accepted only when it includes an approval reference identifying the named person; without it the clause remains open. | Test |
| FR-012-AC-3 | The set and module contract contain no risk score, threshold, or automated risk-acceptability field for DPIA decisions. | Inspection |

## Dependencies

- The Article 35 clauses and their applicability are specified by [FR-010](./FR-010-gdpr-clause-table.md) and [FR-011](./FR-011-gdpr-role-and-risk-applicability.md).
- The `dpia` output is defined in [FR-006](./FR-006-pack-wide-output-catalog.md).
