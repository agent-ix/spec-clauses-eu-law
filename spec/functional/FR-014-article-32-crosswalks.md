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

The GDPR set SHALL crosswalk each Article 32 clause present in the selected set:
Article 32(1)(a) through (d), Article 32(2), and Article 32(4), to both the
selected NIST and HIPAA clause sets. Article 32(3) is not a clause in the
selected set. Each target SHALL resolve in its installed module. The GDPR set SHALL use only partial or informative relations, with no equivalent relation.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-014-AC-1 | Each Article 32(1)(a) through (d), Article 32(2), and Article 32(4) clause has at least one target in `nist/sp800-53@5.2.0` and at least one target in `us-hhs/45-cfr-164-subpart-c@2026-11-12`; Article 32(3) has no clause or crosswalk. | Test |
| FR-014-AC-2 | Every crosswalk target resolves to an existing clause in the installed target module; an absent set or clause fails validation. | Test |
| FR-014-AC-3 | No Article 32 crosswalk uses an `equivalent` relation. | Test |
| FR-014-AC-4 | Validation invokes `quire validate <spec-file-or-glob> --module <module-root-containing-manifest.yaml>` and `quire publish-check --module <module-root>` using module-root paths, and fails when either command exits nonzero. | Test |

## Dependencies

The source clauses and permitted relationship scope are defined in [FR-010](./FR-010-gdpr-clause-table.md) and `spec.md`. The referenced sets are installed test-time dependencies; their contents are not copied into this module. The target clause IDs and original, scoped rationales are specified in the Article 32 Crosswalk Policy in `spec.md`.
