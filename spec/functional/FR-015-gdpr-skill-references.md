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
Articles 25, 30, 32, and 35. It SHALL preserve existing untyped context for
Chapters II, III, and V until future sets cover them, while clearly stating that
this context is not evaluated clause coverage.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-015-AC-1 | PLAT-1628 replaces the Article 25, 30, 32, and 35 sections in `skills/spec-security-analysis/references/gdpr/ChIV-ControllerProcessor.md` with links to `eu/gdpr-2016-679@2016-05-04`, without duplicating the clause summaries. | Inspection |
| FR-015-AC-2 | PLAT-1628 updates `skills/spec-security-analysis/references/gdpr/index.md`, `skills/spec-security-analysis/SKILL.md`, and `skills/spec-security-analysis/references/standards-index.md` to identify the set and its coverage boundary. | Inspection |
| FR-015-AC-3 | PLAT-1628 retains `skills/spec-security-analysis/references/gdpr/ChII-Principles.md`, `ChIII-DataSubjectRights.md`, and `ChV-DataTransfers.md` as clearly labeled untyped context until future clause sets cover those chapters; this content is not reported as evaluated. | Inspection |
| FR-015-AC-4 | PLAT-1628 modifies only the four files named in AC-1 and AC-2, preserves the three context files named in AC-3, and does not modify or delete other Quoin files. | Inspection |

## Dependencies

The GDPR set identity and coverage boundary are defined in [FR-009](./FR-009-gdpr-set-declared.md) and [FR-010](./FR-010-gdpr-clause-table.md). PLAT-1628 modifies `skills/spec-security-analysis/references/gdpr/index.md`, `skills/spec-security-analysis/references/gdpr/ChIV-ControllerProcessor.md`, `skills/spec-security-analysis/SKILL.md`, and `skills/spec-security-analysis/references/standards-index.md`; it preserves `skills/spec-security-analysis/references/gdpr/ChII-Principles.md`, `ChIII-DataSubjectRights.md`, and `ChV-DataTransfers.md` as labeled untyped context. No other GDPR reference files are changed or deleted.
