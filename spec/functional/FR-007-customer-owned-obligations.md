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

When a clause has only outputs of kind `procedure`, the pack SHALL accept a delegated disposition with an `owner`, nonempty rationale and customer `approvalRef`. Quoin SHALL reject a direct fact on such a clause under its FR-211 `customer-owned` reason.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-007-AC-1 | Every all-procedure clause in every EU set appears in the customer-owned inventory in `spec.md`, and the inventory lists no other clause. | Test |
| FR-007-AC-2 | A delegated disposition with owner, rationale and customer approval reference renders as tailored through `quoin discharge --rmm`. | Test |
| FR-007-AC-3 | A direct fact on an all-procedure clause is rejected by quoin under its FR-211 `customer-owned` reason. | Test |

## Dependencies

Depends on FR-006 because procedure output kinds define which clauses are customer-owned. The pack owns the classification test; quoin owns the direct-fact rejection, so FR-007-AC-3 is verified through quoin once FR-211 ships; Quoin owns disposition evaluation and rendering of tailoring fields in the RMM. If `quoin evidence record-discharge` or `quoin discharge --rmm` is unavailable, integration verification fails with the missing executable or capability and does not skip the criterion.
