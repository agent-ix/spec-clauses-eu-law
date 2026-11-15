---
id: FR-013
title: "Records of processing evidence"
type: FR
relationships:
  - target: "ix://agent-ix/spec-clauses-eu-law/US-001"
    type: "traces_to"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-010"
    type: "depends_on"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-011"
    type: "depends_on"
---
# FR-013: Records of processing evidence

## Description

The GDPR set SHALL identify `records-of-processing` as an expected output for
each Article 30 clause.

When a records-of-processing field has no source in the declared data-flow
model, the discharge result SHALL leave the corresponding Article 30 clause
open for assessment.

If a records-of-processing field has no source in the declared data-flow model,
then the discharge result SHALL NOT treat that field as evidence of compliance.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-013-AC-1 | Each Article 30(1)(a) through (g) and 30(2)(a) through (d) clause names `records-of-processing` as an expected output. | Test |
| FR-013-AC-2 | In the reference corpus, a records-of-processing field with no source in the data-flow model leaves the corresponding Article 30 clause open. | Test |

## Dependencies

- The clause IDs and applicability are specified by [FR-010](./FR-010-gdpr-clause-table.md) and [FR-011](./FR-011-gdpr-role-and-risk-applicability.md).
- `data-flow-model` and `records-of-processing` are defined in [FR-006](./FR-006-pack-wide-output-catalog.md). The records-of-processing generator and data-flow connection classification remain separate work in PLAT-1658 and PLAT-1440.
