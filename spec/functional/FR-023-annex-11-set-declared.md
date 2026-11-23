---
id: FR-023
title: "Annex 11 set declared"
type: FR
relationships:
  - target: "ix://agent-ix/spec-clauses-eu-law/US-001"
    type: "traces_to"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-001"
    type: "depends_on"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-002"
    type: "depends_on"
---
# FR-023: Annex 11 set declared

## Description

The module SHALL declare the Annex 11 set with authority `eu`, ID `eu-gmp-annex-11`, version `2011-01`, and the source URL, rights structure, licence and attribution defined in `spec.md`.

The version SHALL name the revision of Annex 11 in force.

The pack SHALL NOT specify the 2025 consultation drafts. The pack SHALL publish an adopted revision as a new set version.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-023-AC-1 | The manifest contains exactly `eu/eu-gmp-annex-11@2011-01` for this set and references its declared clause file. | Test |
| FR-023-AC-2 | `quire publish-check` exits 0 for the module containing the Annex 11 set. | Test |
| FR-023-AC-3 | The set's source URL, identity, rights structure, text, clearance reference, licence, and attribution match `spec.md`; an incorrect or missing value is detected by field. | Test |
| FR-023-AC-4 | The set's metadata and clauses make no reference to the 2025 draft revision as a source of any clause. | Inspection |

## Dependencies

Module and rights contract: [FR-001](./FR-001-pack-module-and-home.md) and [FR-002](./FR-002-truthful-and-publishable-rights-metadata.md). The clause file uses the catalog in [FR-006](./FR-006-pack-wide-output-catalog.md).
