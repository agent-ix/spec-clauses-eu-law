---
id: FR-008
title: "Reference corpus"
type: FR
relationships:
  - target: "ix://agent-ix/spec-clauses-eu-law/US-001"
    type: "traces_to"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-001"
    type: "depends_on"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-003"
    type: "depends_on"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-004"
    type: "depends_on"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-005"
    type: "depends_on"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-006"
    type: "depends_on"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-007"
    type: "depends_on"
---
# FR-008: Reference corpus

## Description

Pack discharge tests SHALL use a minimal synthetic project at `tests/corpus/`. Artifact-local identifiers with fixed archetype grammars SHALL follow those grammars, including `FR-NNN`, `NFR-NNN`, and `TM-NNN` identifiers. Free-form artifact-local identifiers SHALL use the synthetic namespace marker `example-invalid-` and remain unique within the corpus. URI-valued identifiers and references SHALL use the exact authority `example.invalid`. Test facts SHALL use a temporary evidence store. The corpus SHALL contain no secret material.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-008-AC-1 | Corpus validates; fixed-grammar artifact-local identifiers follow their Quire archetype schema; free-form artifact-local identifiers use the `example-invalid-` prefix and are unique within the corpus; every URI-valued identifier or reference uses the exact authority `example.invalid`. | Test |
| FR-008-AC-2 | Discharge tests write facts to a temporary store and remove it after execution. | Test |
| FR-008-AC-3 | The test preflight detects `quire` and `quoin` with the required clause-set validation and discharge/RMM capabilities; if either is missing, the gate fails with the executable or capability named and no criterion is reported as passed. | Test |
| FR-008-AC-4 | No secret material is committed under `tests/corpus/`. | Inspection |

## Dependencies

The pack owns its synthetic corpus and cleanup checks. Quire supplies module/clauses validation and Quoin supplies record-discharge and RMM rendering. Before running the corpus, the test preflight verifies the required commands are available; missing tools are an explicit failure, never a skipped pass. Discharge facts are stored only in a temporary store and cleaned up on success or failure.
