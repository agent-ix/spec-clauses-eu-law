---
id: FR-007
title: "Customer-owned obligations"
type: FR
relationships:
  - target: "ix://agent-ix/spec-clauses-eu-law/US-001"
    type: "traces_to"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-006"
    type: "depends_on"
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

Depends on FR-006 because procedure output kinds define which clauses are customer-owned. The pack owns the classification test; Quoin owns disposition evaluation and rendering of tailoring fields in the RMM. If `quoin evidence record-discharge` or `quoin discharge --rmm` is unavailable, integration verification fails with the missing executable or capability and does not skip the criterion.
