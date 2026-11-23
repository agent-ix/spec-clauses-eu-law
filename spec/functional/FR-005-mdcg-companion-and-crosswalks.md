---
id: FR-005
title: "MDCG companion and crosswalks"
type: FR
relationships:
  - target: "ix://agent-ix/spec-clauses-eu-law/US-001"
    type: "traces_to"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-001"
    type: "depends_on"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-002"
    type: "depends_on"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-003"
    type: "depends_on"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-006"
    type: "depends_on"
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
| FR-005-AC-4 | Security-goal section `2.1` expects `security-risk-records`. Post-market and vigilance sections `5.1` and `5.2` expect the customer-supplied `written-procedure`, and no section outside `3.8` expects `release-record` or `anomaly-list`. | Test |

## Dependencies

Depends on FR-001, FR-002, FR-003, and FR-006. Quire validates each crosswalk's local structure and allowed relation; the EU pack contract test verifies every cross-set target against the loaded MDR set and names a missing target. If the `quire` crosswalk capability is unavailable, the verification gate fails with the missing executable or capability and does not skip the criterion.
