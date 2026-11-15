---
id: SR-013
title: "Code review — AI Act high-risk clause set"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-clauses-eu-law; spec/functional/FR-016-ai-act-sets-declared.md, spec/functional/FR-017-ai-act-high-risk-obligations.md, spec/functional/FR-019-ai-act-applicability.md, spec/functional/FR-022-ai-act-application-date.md, spec/spec.md, spec_clauses_eu_law/clauses/eu-ai-act-2024-1689-2026-07-27.json, spec_clauses_eu_law/manifest.yaml, tests/test_clause_sets.py"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-016"
    type: reviews
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-017"
    type: reviews
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-019"
    type: reviews
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-022"
    type: reviews
---

## Summary

Reviewed the new AI Act high-risk clause set, manifest entry, and tests against FR-016, FR-017, FR-019 and FR-022. The clause data and Article 113 date match the stated source scope, but three test bindings either overstate cross-set coverage or bind a criterion to a test that does not evaluate clauses.

## Verdict

**CONDITIONAL** — the focused AI Act tests pass, but the cross-set trace claims must be corrected before this PR is mergeable.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | The identity and rights test checks only the high-risk set but marks both-set FR-016 criteria as covered. | tests/test_clause_sets.py:1093-1105 |
| FND-002 | medium | The applicability test checks only the high-risk set but marks criteria covering both sets and Annex IV point dimensions as covered. | tests/test_clause_sets.py:1149-1184 |
| FND-003 | medium | FR-017-AC-1 is tagged on a raw clause-data comparison; the requirement says the evaluated provider and deployer sets return exactly the table IDs. | tests/test_clause_sets.py:1118-1128 |

## Review coverage

- FR-016-AC-1 through AC-4: checked manifest contents, source identity, rights and validation coverage.
- FR-017-AC-1 through AC-4: checked exact table alignment, outputs, applicability, out-of-scope exclusions and the inspection method.
- FR-019-AC-1 through AC-5: checked role and risk evaluation, both-set scope, and the separate Annex IV dimensions.
- FR-022-AC-1 and AC-2: checked the date value, Article 113 reference, scope and absence from applicability dimensions.
- Verified against the official consolidated EUR-Lex text at the declared source URL. Article 113 gives 2 August 2028 for Article 6(1) Annex I high-risk systems and Chapter III Sections 1–3.
- Focused command: `locked-build.sh <worktree>/target poetry run pytest tests/test_clause_sets.py -k ai_act`; 3 passed, exit 0. Matrix commands and comparison are recorded in the gap-analysis artifact.
