---
id: FR-015
title: "GDPR references in security-analysis skill"
type: FR
relationships:
  - target: "ix://agent-ix/spec-clauses-eu-law/US-001"
    type: "traces_to"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-009"
    type: "depends_on"
---
# FR-015: GDPR references in security-analysis skill

## Description

The security-analysis skill SHALL identify the GDPR clause set as the source for
Articles 25, 30, 32, and 35. It SHALL state that other GDPR topics are not
represented by this set and require separate assessment; it SHALL NOT present
those topics as evaluated clause coverage.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-015-AC-1 | After the skill update in PLAT-1628, its GDPR references for Articles 25, 30, 32, and 35 identify `eu/gdpr-2016-679@2016-05-04` and do not duplicate article summaries as a second source of clause data. | Inspection |
| FR-015-AC-2 | The skill states that Articles outside 25, 30, 32, and 35 are not covered by this set and are not reported as evaluated. | Inspection |
| FR-015-AC-3 | Existing contextual material for GDPR chapters not covered by this set is retained or linked as untyped context, clearly marked as outside clause-set evaluation. | Inspection |

## Dependencies

The GDPR set identity and coverage boundary are defined in [FR-009](./FR-009-gdpr-set-declared.md) and [FR-010](./FR-010-gdpr-clause-table.md). The skill changes are implemented in PLAT-1628.
