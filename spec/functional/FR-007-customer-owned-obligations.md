---
id: FR-007
title: "Customer-owned obligations"
type: FR
---
# FR-007: Customer-owned obligations

## Description

When a clause has only outputs of kind `procedure`, the pack SHALL require delegated disposition with nonempty rationale and customer `approvalRef`; direct disposition is rejected.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-007-AC-1 | Every all-procedure clause appears in the customer-owned inventory. | Test |
| FR-007-AC-2 | Delegated disposition with rationale and customer approval reference succeeds; a direct fact is rejected. | Test |

## Dependencies

Uses the clause-set, evaluation, publication and discharge contracts already implemented by quire and quoin.
