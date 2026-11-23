---
id: FR-006
title: "Pack-wide output catalog"
type: FR
relationships:
  - target: "ix://agent-ix/spec-clauses-eu-law/US-001"
    type: "traces_to"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-001"
    type: "depends_on"
---
# FR-006: Pack-wide output catalog

## Description

The pack SHALL maintain one EU catalog in `spec.md`. Each EU set declares only its used subset with identical kind and description. For every catalog name also present in the US Health-Law Output Catalog in PLAT-1422's `spec/spec.md`, the EU definition SHALL match the canonical US `kind`, `description` and `producers` exactly. That US catalog is the comparison source; the pack contract test reads it as a test dependency and SHALL NOT copy its table into a fixture or test constant.

Each EU set SHALL list `producers` in its catalog entry for the outputs the "EU Output Producers" table in `spec.md` names, with the retained kinds that table gives. Quoin resolves an `evidenceRefs` entry against this list (quoin FR-211).

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-006-AC-1 | Catalog contains exactly the names and definitions in `spec.md`; set subsets match them. | Test |
| FR-006-AC-2 | A mismatch fixture differing in kind or description fails and names the output. | Test |
| FR-006-AC-3 | For every output name shared with the PLAT-1422 US catalog, the EU `kind`, `description` and `producers` equal the canonical definition; a mismatch fixture fails and names the output. | Test |
| FR-006-AC-4 | Every kind in the EU Output Producers table is one of `run`, `scan`, `mock-inspection`, `analysis-report`, `scenario`. | Test |
| FR-006-AC-5 | Each set's catalog entry for an output in the "EU Output Producers" table carries the `producers` that table lists. | Test |

## Dependencies

The EU pack owns its catalog and its per-set subsets. The US pack's PLAT-1422 catalog is the canonical comparison source for reused names and is loaded as a test-only dependency; no cross-repository engine behavior is assumed. If the canonical source cannot be loaded, the parity gate fails and reports the unavailable source instead of passing with a partial comparison.
