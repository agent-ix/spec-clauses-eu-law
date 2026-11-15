---
id: SR-012
title: "Dependency analysis — AI Act specification"
type: SpecReview
analysis: dependency
scope: "agent-ix/spec-clauses-eu-law; FR-016–FR-022 dependency edges and Requirements Architecture graph"
review_set: subset
---

## Summary

The AI Act requirement dependency graph is acyclic and mostly orders enablement before features: set/catalog definitions precede clause tables, applicability, crosswalks, and date metadata. The inline graph omits one dependency declared by FR-020.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | The dependency summary omits FR-020's declared dependency on FR-018 | spec/spec.md:278; FR-020 |

## Dependency graph

The requirement frontmatter is acyclic. Relevant order: FR-016 → FR-017/FR-018 → FR-019/FR-020/FR-021, with FR-022 after FR-016. FR-020's header also declares FR-018, but the inline dependency summary omits that edge; see the finding.

## Dispositions

| FND | outcome | reason |
|---|---|---|
| FND-001 | fixed | The Requirements Architecture graph now includes FR-020 → FR-018, matching FR-020 frontmatter. |
