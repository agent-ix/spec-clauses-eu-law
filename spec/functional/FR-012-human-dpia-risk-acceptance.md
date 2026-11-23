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

The module SHALL declare the `privacy-officer` approval role on every Article
35 clause. Quoin verifies the approval when a direct fact claims to discharge
such a clause: the fact needs a non-blank `approvalRef` (quoin FR-208) that
engineering-assurance verifies as an approval by the named role (quoin FR-211).
The pack carries the role and does not check approvals itself. No tool SHALL score the DPIA or accept
its residual risk.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-012-AC-1 | Every Article 35 clause declares `approvalRoles` equal to `["privacy-officer"]`. An Article 35 direct fact citing a DPIA with a missing or blank `approvalRef` leaves the clause undischarged with the reason that the required approval reference is missing, and the same fact with an `approvalRef` discharges. Verification that the approval names the person who accepted residual risk belongs to quoin FR-211. | Test |
| FR-012-AC-2 | The set and module contract contain no risk score, threshold, or automated risk-acceptability field for DPIA decisions. | Inspection |

## Dependencies

- The Article 35 clauses and their applicability are specified by [FR-010](./FR-010-gdpr-clause-table.md) and [FR-011](./FR-011-gdpr-role-and-risk-applicability.md).
- The `dpia` output is defined in [FR-006](./FR-006-pack-wide-output-catalog.md).
