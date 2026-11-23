---
id: SR-018
title: "EARS analysis — Annex 11 requirement statements"
type: SpecReview
analysis: ears-conformance
scope: "agent-ix/spec-clauses-eu-law; PR #21 diff: spec/spec.md Annex 11 sections, FR-023..FR-028, NFR-004"
review_set: subset
date: 2026-11-23
---

## Summary

Ticket: PLAT-1832. Reviewed `git diff origin/main...HEAD` at fa6a43513c94460e2c62277023523f824f4d84c1 of agent-ix/spec-clauses-eu-law PR #21. Method: spec-review/spec-ears-analysis.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | `quire validate 'spec/**/*.md'` (quire 0.52.0) exits 0 with four warnings, all on this PR's files: ears:non-singular on FR-025:17, FR-026:15, FR-027:21 and quality:agentless-passive on FR-025:17 ("shall be declared" names no agent). | spec/functional/FR-025-annex-11-output-bindings.md:17 |

## Finding details

### FND-001 — FR-025

`quire validate 'spec/**/*.md'` (quire 0.52.0) exits 0 with four warnings, all on this PR's files: ears:non-singular on FR-025:17, FR-026:15, FR-027:21 and quality:agentless-passive on FR-025:17 ("shall be declared" names no agent). FR-023, FR-024 and FR-028 also carry several SHALLs per statement. This matches the repo's existing FR style, so it is low.

Expected fix: Name the agent in FR-025 ("The pack SHALL declare ..."); optionally split the multi-SHALL statements.

## Scope examined

- FR-023 (examined)
- FR-024 (examined)
- FR-025 (examined)
- FR-026 (examined)
- FR-027 (examined)
- FR-028 (examined)
- NFR-004 (examined)

## Verdict

Not mergeable until the high findings are fixed. All 13 Part 11 crosswalk targets resolve in us-fda-21-cfr-11-2026-11-12.json (spec-clauses-us-health origin/main c5a8ca8), and the partial/informative strengths are defensible. Every named quoin and engineering-assurance command exists. The version-in-force claim matches the Commission listing ("revision January 2011"). The rights wording is truthful: the PDF has no licence statement of its own. No tool assigns a score, class or criticality, and the clause table covers every numbered paragraph of the 2011 text. No AC pins counts, versions or hashes. No ticket or roadmap narration was added.

## Dispositions

Round 1, head ceb584e0c8c0568364f5b31d71739718800a4690.

| FND | outcome | reason |
|---|---|---|
| FND-001 | fixed | - |
