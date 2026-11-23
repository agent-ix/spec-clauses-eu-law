---
id: FR-010
title: "GDPR clause table"
type: FR
relationships:
  - target: "ix://agent-ix/spec-clauses-eu-law/US-001"
    type: "traces_to"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-009"
    type: "depends_on"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-006"
    type: "depends_on"
---
# FR-010: GDPR clause table

## Description

The GDPR set SHALL contain exactly the clause identifiers, forces,
applicability expressions, and expected outputs in the GDPR Clause Table in
`spec.md`. Each clause SHALL have an original, non-empty summary and at least
one expected output declared in the EU Pack Output Catalog.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-010-AC-1 | Evaluation returns exactly the clause IDs in the GDPR Clause Table, with no missing or additional IDs. | Test |
| FR-010-AC-2 | Every evaluated clause has the force specified in the table, non-empty original text, and at least one expected output that resolves in the catalog. | Test |
| FR-010-AC-3 | `art-32(4)` names `processing-access-control` and not `access-control`. The GDPR set's catalog does not contain `access-control`, and no GDPR clause names it. | Test |
| FR-010-AC-4 | `art-30(4)` names `written-procedure` beside `records-of-processing`, because making the record available on request is the person's procedure. | Test |
| FR-010-AC-5 | The descriptions of `privacy-by-default-settings` and `processing-access-control` state that the output is customer-supplied and has no toolchain producer. | Test |
| FR-010-AC-6 | `art-32(1)(c)` names `backup-restore-record` beside `security-risk-records` and `verification-records`, with the kind and description the EU catalog gives it. | Test |

## Dependencies

- The GDPR set identity is defined by [FR-009](./FR-009-gdpr-set-declared.md).
- Expected outputs are defined by [FR-006](./FR-006-pack-wide-output-catalog.md).
