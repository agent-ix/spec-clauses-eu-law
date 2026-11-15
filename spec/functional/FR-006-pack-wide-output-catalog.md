---
id: FR-006
title: "Pack-wide output catalog"
type: FR
---
# FR-006: Pack-wide output catalog

## Description

The pack SHALL maintain one catalog in `spec.md`. Each set declares only its used subset with identical kind and description. EU definitions match shared US definitions for reused names.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-006-AC-1 | Catalog contains exactly the names and definitions in `spec.md`; set subsets match them. | Test |
| FR-006-AC-2 | A mismatch fixture differing in kind or description fails and names the output. | Test |
| FR-006-AC-3 | `written-procedure`, `signed-record` and `audit-trail` preserve the shared definitions. | Test |

## Dependencies

Uses the clause-set, evaluation, publication and discharge contracts already implemented by quire and quoin.
