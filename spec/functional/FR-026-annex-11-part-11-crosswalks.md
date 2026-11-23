---
id: FR-026
title: "Annex 11 Part 11 crosswalks"
type: FR
relationships:
  - target: "ix://agent-ix/spec-clauses-eu-law/US-001"
    type: "traces_to"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-024"
    type: "depends_on"
---
# FR-026: Annex 11 Part 11 crosswalks

## Description

The Annex 11 set SHALL crosswalk the clauses listed in the Annex 11 Part 11 Crosswalk Policy in `spec.md` to the clause set `us-fda/21-cfr-11@2026-11-12`. Each target SHALL resolve in its installed module. The set SHALL use only `partial` or `informative` relations.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-026-AC-1 | Each clause listed in the policy has the listed targets and relations, and no other clause has a Part 11 crosswalk. | Test |
| FR-026-AC-2 | Every crosswalk target resolves to an existing clause in the installed Part 11 module; an absent set or clause fails validation. | Test |
| FR-026-AC-3 | No Annex 11 crosswalk uses an `equivalent` relation and every rationale is non-empty original wording. | Test |
| FR-026-AC-4 | The commands `quire validate <spec-file-or-glob> --module <module-root>` and `quire publish-check --module <module-root>` each exit 0; a nonzero exit fails the check. | Test |

## Dependencies

Source clauses are defined in [FR-024](./FR-024-annex-11-clause-table-and-applicability.md). The Part 11 module is an installed test-time dependency; its contents are not copied into this module.
