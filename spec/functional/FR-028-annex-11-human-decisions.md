---
id: FR-028
title: "Annex 11 human decisions"
type: FR
relationships:
  - target: "ix://agent-ix/spec-clauses-eu-law/US-001"
    type: "traces_to"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-024"
    type: "depends_on"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-027"
    type: "depends_on"
---
# FR-028: Annex 11 human decisions

## Description

The pack SHALL leave every risk-based and criticality decision in Annex 11 to a named person: the risk scaling of paragraphs 1, 3.2, 4.1, 4.4, 6, 9 and 16, and the criticality judgments in 4.3, 12.2 and 13. These ten clauses SHALL carry an approval role, and a fact or disposition on any of them SHALL discharge it only with a person-named `approvalRef`. The tool SHALL NOT create, infer, score or accept any such decision.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-028-AC-1 | Clauses `1`, `3.2`, `4.1`, `4.3`, `4.4`, `6`, `9`, `12.2`, `13` and `16` each declare a non-empty `approvalRoles`, and no other Annex 11 clause does. A fact on one of them without a person-named `approvalRef` is rejected or leaves the clause undischarged; with a named `approvalRef` it discharges. Every other clause follows the direct-evidence and disposition partition in FR-027-AC-1. | Test |
| FR-028-AC-2 | A missing, blank or unresolved `approvalRef` leaves the clause unresolved and emits no accepted-decision RMM field. | Test |
| FR-028-AC-3 | The evaluator generates no approval reference, approver identity, criticality value, risk level or acceptance. | Test |

## Dependencies

Selected decision clauses come from [FR-024](./FR-024-annex-11-clause-table-and-applicability.md); Quoin owns generic disposition validation and RMM rendering.
