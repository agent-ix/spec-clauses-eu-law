---
id: FR-014
title: "Article 32 crosswalks"
type: FR
relationships:
  - target: "ix://agent-ix/spec-clauses-eu-law/US-001"
    type: "traces_to"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-010"
    type: "depends_on"
---
# FR-014: Article 32 crosswalks

## Description

The GDPR set SHALL crosswalk each Article 32(1)(a) through (d) and Article 32(2)
clause to both the selected NIST and HIPAA clause sets. Each target SHALL resolve
in its installed module, and a relation SHALL express partial or informative
coverage rather than equivalence.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-014-AC-1 | Each Article 32(1)(a) through (d) and Article 32(2) clause has at least one target in `nist/sp800-53@5.2.0` and at least one target in `us-hhs/45-cfr-164-subpart-c@2026-11-12`. | Test |
| FR-014-AC-2 | Every crosswalk target resolves to an existing clause in the installed target module; an absent set or clause fails validation. | Test |
| FR-014-AC-3 | No Article 32 crosswalk uses an `equivalent` relation. | Test |

## Dependencies

The source clauses and permitted relationship scope are defined in [FR-010](./FR-010-gdpr-clause-table.md) and `spec.md`. The referenced sets are installed test-time dependencies; their contents are not copied into this module.
