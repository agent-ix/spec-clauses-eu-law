---
id: FR-002
title: "Truthful and publishable rights metadata"
type: FR
relationships:
  - target: "ix://agent-ix/spec-clauses-eu-law/US-001"
    type: "traces_to"
---
# FR-002: Truthful and publishable rights metadata

## Description

Each set SHALL declare `structure: citation_only`, `text: original`, `clearance_ref: null`, nonblank `licence`, and nonblank `attribution`, using the wording and legal-notice URLs recorded in `spec.md`.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-002-AC-1 | A metadata test checks all declared sets' required rights fields and source-specific licence and attribution values; an injected mismatch names the affected set and field. | Test |
| FR-002-AC-2 | `quire publish-check --module <pkg>` exits 0; a fixture with `text: licensed` exits 2 and identifies its set key. | Test |
| FR-002-AC-3 | The source URL in each set equals its official source URL in `spec.md`; a changed URL fails and identifies the set. | Test |

## Dependencies

The source rights and attribution statements in `spec.md` are reviewed against their primary source notices. The metadata test is pack-owned. `quire publish-check` supplies the generic clause-set rights check; it does not establish whether an external source notice is accurate. If `quire` or its rights capability is unavailable, the verification gate fails with the missing executable or capability and does not skip the criterion.
