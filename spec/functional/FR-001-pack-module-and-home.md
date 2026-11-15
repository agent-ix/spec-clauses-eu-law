---
id: FR-001
title: "Pack module and home"
type: FR
relationships:
  - target: "ix://agent-ix/spec-clauses-eu-law/US-001"
    type: "traces_to"
---
# FR-001: Pack module and home

## Description

The repository SHALL use `spec/`, package `spec_clauses_eu_law`, and one `clause_sets` module. The module manifest SHALL list exactly the MDR set `eu/mdr-2017-745@2026-07-19`, MDCG set `eu-mdcg/mdcg-2019-16@rev1`, GDPR set `eu/gdpr-2016-679@2016-05-04`, AI Act high-risk set `eu/ai-act-2024-1689@2026-07-27`, and AI Act Annex IV set `eu/ai-act-2024-1689-annex-iv@2026-07-27`. The module SHALL declare no object types, archetypes or edges.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-001-AC-1 | Manifest lists exactly the MDR, MDCG, GDPR, AI Act high-risk, and AI Act Annex IV keys; `quire validate "spec/**/*.md" --module <spec-artifacts-iso-module-root> --module <spec-artifacts-process-module-root>` exits 0. | Test |
| FR-001-AC-2 | Module declares no object types, archetypes or edges; install reports `pack: false`. | Test |

## Dependencies

Uses the clause-set, evaluation, publication and discharge contracts already implemented by quire and quoin.
