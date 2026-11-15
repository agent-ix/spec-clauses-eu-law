---
id: FR-020
title: "AI Act human decisions"
type: FR
relationships:
  - target: "ix://agent-ix/spec-clauses-eu-law/US-001"
    type: "traces_to"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-017"
    type: "depends_on"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-018"
    type: "depends_on"
---
# FR-020: AI Act human decisions

## Description

The pack SHALL require a person-named `approvalRef` for discharge decisions that assert completion of Article 9 residual-risk decisions or Article 14 human-oversight decisions. The tool SHALL NOT create or infer either decision.

## Acceptance Criteria

| ID | Criteria | Verification |
|---|---|---|
| FR-020-AC-1 | A fact alone cannot discharge an Article 9 residual-risk or Article 14 human-oversight decision; an accepted human decision includes a nonempty rationale and `approvalRef` resolving to a named person. | Test |
| FR-020-AC-2 | A missing, blank, or unresolved `approvalRef` leaves the affected clause unresolved and emits no accepted-decision RMM field. | Test |
| FR-020-AC-3 | The evaluator does not generate an approval reference, approver identity, acceptance, or legal conclusion. | Test |

## Dependencies

The pack owns the selected decision obligations; Quoin owns generic disposition validation and RMM rendering. This requirement defines which records require human authorization, not a legal determination.
