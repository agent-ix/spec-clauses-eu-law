---
id: FR-001
title: "Pack module and home"
type: FR
---
# FR-001: Pack module and home

## Description

The repository SHALL use `spec/`, package `spec_clauses_eu_law`, and one `clause_sets` module. The M1 manifest SHALL list exactly `eu/mdr-2017-745@2026-07-19` and `eu-mdcg/mdcg-2019-16@rev1`, and declare no object types, archetypes or edges.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-001-AC-1 | Manifest lists exactly the two M1 keys and validates with `quire validate --module <pkg>`. | Test |
| FR-001-AC-2 | Module declares no object types, archetypes or edges; install reports `pack: false`. | Test |

## Dependencies

Uses the clause-set, evaluation, publication and discharge contracts already implemented by quire and quoin.
