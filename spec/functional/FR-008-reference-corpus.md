---
id: FR-008
title: "Reference corpus"
type: FR
---
# FR-008: Reference corpus

## Description

Pack discharge tests SHALL use a minimal synthetic project at `tests/corpus/`. Synthetic identifiers and evidence references use `example.invalid`, and test facts use a temporary evidence store.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-008-AC-1 | Corpus validates and every identifier/reference uses `example.invalid`; no secret material is present. | Test |
| FR-008-AC-2 | Discharge tests write facts to a temporary store and remove it after execution. | Test |

## Dependencies

Uses the clause-set, evaluation, publication and discharge contracts already implemented by quire and quoin.
