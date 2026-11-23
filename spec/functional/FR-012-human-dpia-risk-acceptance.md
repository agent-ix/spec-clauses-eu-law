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
35 clause. Quoin verifies the approval when evidence claims to discharge such a
clause: today (quoin FR-208) a fact or disposition discharges only with a
non-blank `approvalRef`, and once quoin FR-211 ships it requires an
engineering-assurance-verified approval by the named role. The pack carries the
role and does not check approvals itself. No tool SHALL score the DPIA or accept
its residual risk.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-012-AC-1 | Every Article 35 clause declares `approvalRoles` equal to `["privacy-officer"]`. An Article 35 direct fact citing a DPIA with a missing or blank `approvalRef` leaves the clause undischarged under quoin FR-208. That the approval identifies the named person who accepted residual risk is verified by quoin FR-211 and is not tested here until it ships. | Test |
| FR-012-AC-2 | An Article 35 `accepted_risk` disposition with a missing or blank `approvalRef` leaves the clause undischarged under quoin FR-208. That the approval identifies the named person is verified by quoin FR-211 and is not tested here until it ships. | Test |
| FR-012-AC-3 | The set and module contract contain no risk score, threshold, or automated risk-acceptability field for DPIA decisions. | Inspection |

## Dependencies

- The Article 35 clauses and their applicability are specified by [FR-010](./FR-010-gdpr-clause-table.md) and [FR-011](./FR-011-gdpr-role-and-risk-applicability.md).
- The `dpia` output is defined in [FR-006](./FR-006-pack-wide-output-catalog.md).
