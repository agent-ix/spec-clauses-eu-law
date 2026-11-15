---
id: SR-011
title: "Integrity analysis — AI Act specification"
type: SpecReview
analysis: integrity
scope: "agent-ix/spec-clauses-eu-law; AI Act specification tables and FR-016–FR-022, NFR-003"
review_set: subset
---

## Summary

Requirement IDs and trace links are consistent, all new FRs have testable or inspectable acceptance criteria, and NFR-003 constrains the new AI Act requirements. The cross-file dependency summary has one mismatch with an FR's declared dependency edge.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | The dependency summary omits FR-020's declared dependency on FR-018 | spec/spec.md:278; FR-020 |

## Finding details

### FND-001 — Dependency summary omits a declared edge

`FR-020` frontmatter declares `depends_on` edges to both `FR-017` and `FR-018`, while the Requirements Architecture graph lists `FR-020 → FR-017` only. Keep the authoritative graph and frontmatter synchronized, or remove the unnecessary edge with a rationale.

## Dispositions

| FND | outcome | reason |
|---|---|---|
| FND-001 | fixed | The Requirements Architecture graph now includes FR-020 → FR-018, matching FR-020 frontmatter. |
