---
id: FR-022
title: "AI Act application date recorded"
type: FR
relationships:
  - target: "ix://agent-ix/spec-clauses-eu-law/US-001"
    type: "traces_to"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-016"
    type: "depends_on"
---
# FR-022: AI Act application date recorded

## Description

The AI Act set SHALL record the application date for its Annex I high-risk-system scope from Article 113 of the consolidated source version in its set metadata or clause rationale.

## Acceptance Criteria

| ID | Criteria | Verification |
|---|---|---|
| FR-022-AC-1 | The version `2026-07-27` records 2 August 2028 as the application date for the selected Article 6(1) Annex I scope and cites Article 113. | Test |
| FR-022-AC-2 | A missing, incorrect, or uncited date fails the test; the date is not represented as a clause applicability dimension and is never used to evaluate a clause. | Test |

## Dependencies

The date is source metadata from Article 113 of the EUR-Lex consolidated text in [FR-016](./FR-016-ai-act-sets-declared.md). A later consolidation requires a new version and reviewed metadata.
