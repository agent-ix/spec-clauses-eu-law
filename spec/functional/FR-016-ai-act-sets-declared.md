---
id: FR-016
title: "AI Act sets declared"
type: FR
relationships:
  - target: "ix://agent-ix/spec-clauses-eu-law/US-001"
    type: "traces_to"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-001"
    type: "depends_on"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-002"
    type: "depends_on"
---
# FR-016: AI Act sets declared

## Description

The module SHALL declare exactly the AI Act set keys `eu/ai-act-2024-1689@2026-07-27` and `eu/ai-act-2024-1689-annex-iv@2026-07-27` with the source identities and rights metadata in `spec.md`.

## Acceptance Criteria

| ID | Criteria | Verification |
|---|---|---|
| FR-016-AC-1 | The manifest contains both specified keys exactly once and references the respective declared clause files. | Test |
| FR-016-AC-2 | Both sets use the exact EUR-Lex 2026-07-27 official source URL, authority, ID, version, `structure: citation_only`, `text: original`, and `clearance_ref: null` specified in `spec.md`; a changed or missing field fails with its field path. | Test |
| FR-016-AC-3 | Both sets' licence and attribution fields match the EUR-Lex reuse statement, exact source URL, change indication, and legal-notice URL specified in `spec.md`; an injected mismatch fails with its set and field path. | Test |
| FR-016-AC-4 | `quire validate "spec/**/*.md" --module <spec-artifacts-iso-module-root>` and `quire publish-check --module <pkg>` exit 0. | Test |

## Dependencies

Uses the existing clause-only module contract in [FR-001](./FR-001-pack-module-and-home.md) and the source-rights policy in [FR-002](./FR-002-truthful-and-publishable-rights-metadata.md). A later EUR-Lex consolidation is a new set version and requires a corresponding reviewed rights/source update.
