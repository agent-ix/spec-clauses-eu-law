---
id: SR-014
title: "Gap analysis — AI Act high-risk clause set"
type: SpecReview
analysis: gap-analysis
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

The high-risk clause data is backed by normative requirements and has focused tests. The computed matrix exposes premature test tags for requirements that cover both AI Act sets; the Annex IV set is still outside this PR.

## Verdict

**CONDITIONAL** — the repository matrix still has existing gaps, and this diff marks several cross-set criteria covered by tests that exercise only the high-risk set.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | Cross-set identity, rights and applicability criteria are marked tagged even though their new tests evaluate only the high-risk set; Annex IV remains unimplemented here. | tests/test_clause_sets.py:1093-1105, 1149-1184 |

## Coverage

- `quoin matrix --repo . --json` and `quire matrix --scope . --format json --strict` were run. The strict command exits 1 with 35 untagged criteria and 11 `method-without-symbol` criteria. The same repository at `origin/main` has 41 untagged criteria and 11 `method-without-symbol` criteria.
- In the changed AI Act scope, FR-017-AC-1 through AC-3 and FR-022-AC-1 through AC-2 are tagged. FR-016-AC-1 and AC-4 and FR-019-AC-2 and AC-5 remain untagged for the Annex IV implementation. FR-016-AC-2 and AC-3 and FR-019-AC-1, AC-3 and AC-4 are tagged by high-risk-only tests, although each criterion covers both sets. FR-017-AC-1 is tagged by a test that reads clause JSON but does not evaluate the set.
- The diff adds no production-code modules, stubs, or behavior without a requirement. New clause data is sourced from the declared normative table and rights requirements. No plan was supplied. Plan completion: not assessed.
- Focused command: `locked-build.sh <worktree>/target poetry run pytest tests/test_clause_sets.py -k ai_act`; 3 passed, exit 0.
