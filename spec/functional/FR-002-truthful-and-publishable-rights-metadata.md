---
id: FR-002
title: "Truthful and publishable rights metadata"
type: FR
---
# FR-002: Truthful and publishable rights metadata

## Description

Each set SHALL declare `structure: citation_only`, `text: original`, `clearance_ref: null`, nonblank `licence`, and nonblank `attribution`, using the wording and legal-notice URLs recorded in `spec.md`.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-002-AC-1 | Both sets have the stated rights fields and source-specific licence and attribution wording. | Inspection |
| FR-002-AC-2 | `quire publish-check --module <pkg>` exits 0; a fixture with `text: licensed` exits 2 and identifies its set key. | Test |

## Dependencies

Uses the clause-set, evaluation, publication and discharge contracts already implemented by quire and quoin.
