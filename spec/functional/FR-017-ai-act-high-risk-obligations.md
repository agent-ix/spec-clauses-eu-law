---
id: FR-017
title: "AI Act high-risk obligations"
type: FR
relationships:
  - target: "ix://agent-ix/spec-clauses-eu-law/US-001"
    type: "traces_to"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-016"
    type: "depends_on"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-006"
    type: "depends_on"
---
# FR-017: AI Act high-risk obligations

## Description

The provider set SHALL contain exactly the Article 9–20, 43, 47, 72 and 73 obligations in the AI Act High-Risk Obligations Table in `spec.md`. The deployer set SHALL contain exactly the Article 26 obligation in that table. Every clause SHALL be mandatory when its applicability expression binds, use the table's applicability and outputs, and have an original, nonempty summary.

## Acceptance Criteria

| ID | Criteria | Verification |
|---|---|---|
| FR-017-AC-1 | Evaluating the provider and deployer sets returns exactly the IDs in the AI Act High-Risk Obligations Table, with no missing, duplicate, or additional IDs. | Test |
| FR-017-AC-2 | Each clause's force, applicability expression, and expected outputs equal its table row; every output resolves in the catalog and every summary is nonempty. | Test |
| FR-017-AC-3 | A changed applicability expression, force, or unresolved output fails and names the clause and field. | Test |
| FR-017-AC-4 | No clause includes an obligation assigned only to an importer, distributor, notified body, market-surveillance authority, or other out-of-scope actor. | Inspection |
| FR-017-AC-5 | The catalog entries `data-lineage`, `model-description`, `event-logging-design`, `human-oversight-design`, `post-market-monitoring-plan` and `conformity-declaration` are described as customer-supplied with no toolchain producer; every other output the AI Act sets use names its producing command or artifact archetype. Clause `art-73` expects only `written-procedure` and is customer-owned. | Test |

## Dependencies

Depends on [FR-016](./FR-016-ai-act-sets-declared.md) for the set identities and [FR-006](./FR-006-pack-wide-output-catalog.md) for output definitions. Article 49 is excluded: paragraphs (1) and (3) concern applicable Annex III systems, while paragraph (2) concerns systems determined not high-risk under Article 6(3); neither creates a provider registration duty for this Annex I scope. The complete clause IDs, force, applicability and output mapping are the table in `spec.md`.
