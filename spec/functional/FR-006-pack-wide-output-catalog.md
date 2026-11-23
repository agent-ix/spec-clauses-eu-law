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

The pack SHALL maintain one EU catalog in `spec.md`. Each EU set declares only its used subset with identical kind and description. For every catalog name also present in the US Health-Law Output Catalog in PLAT-1422's `spec/spec.md`, the EU definition SHALL match the canonical US `kind` and `description` exactly. That US catalog is the comparison source; the pack contract test reads it as a test dependency and SHALL NOT copy its table into a fixture or test constant.

An EU catalog entry whose evidence is a retained quoin evidence-store record SHALL carry `producers`, a non-empty list of distinct retained kinds as defined by quoin FR-211, as the "EU Output Producers" table in `spec.md` states; today that is `verification-records`. A tool-generated document or report and a customer-supplied output SHALL NOT carry `producers`. A shared name SHALL carry `producers` identical to the US catalog's.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-006-AC-1 | Catalog contains exactly the names and definitions in `spec.md`; set subsets match them. | Test |
| FR-006-AC-2 | A mismatch fixture differing in kind or description fails and names the output. | Test |
| FR-006-AC-3 | For every output name shared with the PLAT-1422 US catalog, the EU `kind` and `description` equal the canonical definition; a mismatch fixture fails and names the output and field. | Test |
| FR-006-AC-4 | Every catalog entry with `producers` lists only distinct, unpadded kinds from the quoin FR-211 set, and exactly the outputs in the "EU Output Producers" table carry it with the listed kinds. | Test |
| FR-006-AC-5 | For every output name shared with the US catalog, `producers` is identical, absent on both or equal on both; a drift fixture fails and names the output. | Test |
| FR-006-AC-6 | The installed `quire` validates and evaluates every set that carries `producers`. | Test |

## Dependencies

The EU pack owns its catalog and its per-set subsets. The US pack's PLAT-1422 catalog is the canonical comparison source for reused names and is loaded as a test-only dependency; no cross-repository engine behavior is assumed. If the canonical source cannot be loaded, the parity gate fails and reports the unavailable source instead of passing with a partial comparison.
