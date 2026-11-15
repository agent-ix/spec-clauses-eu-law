---
id: FR-009
title: "GDPR set declared"
type: FR
relationships:
  - target: "ix://agent-ix/spec-clauses-eu-law/US-001"
    type: "traces_to"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-001"
    type: "depends_on"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-002"
    type: "depends_on"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-006"
    type: "depends_on"
---
# FR-009: GDPR set declared

## Description

The module SHALL declare the GDPR set with authority `eu`, ID `gdpr-2016-679`,
version `2016-05-04`, and source URL defined in `spec.md`. A later EUR-Lex
consolidated text SHALL use a new set version.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-009-AC-1 | The manifest contains exactly `eu/gdpr-2016-679@2016-05-04` for this set and references its declared clause file. | Test |
| FR-009-AC-2 | `quire publish-check` exits 0 for the module containing the GDPR set. | Test |
| FR-009-AC-3 | The set's source URL, identity, rights structure, text, clearance reference, licence, and attribution match the values specified in `spec.md`; an incorrect or missing value is detected by field. | Test |

## Dependencies

- The module and rights contract is defined by [FR-001](./FR-001-pack-module-and-home.md) and [FR-002](./FR-002-truthful-and-publishable-rights-metadata.md).
- The clause file uses the catalog in [FR-006](./FR-006-pack-wide-output-catalog.md).
