---
id: SR-002
title: "Gap analysis — EU-law clause module scaffold PR #2"
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/spec-clauses-eu-law@35521ff; complete spec, computed matrix, tests and changed package/CI code"
review_set: subset
relationships:
  - { target: "ix://agent-ix/spec-clauses-eu-law/spec", type: references }
---

## Summary

The PR's scaffold-specific acceptance checks pass, but the repository-wide matrix still has 23 of 28 criteria without valid test evidence: 20 are untagged, two have no test symbol, and the FR-001-AC-1 binding is contradicted by the empty-manifest test. The remaining unbound criteria cover later clause-set work and the licensing boundary.

## Verdict

**FAIL** — the computed matrix has 20 untagged criteria and two criteria whose verification method has no test symbol.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | The computed matrix has no executable test binder for 22 of 28 criteria: 20 are untagged and NFR-001-AC-3 and NFR-001-M-3 have method-without-symbol status. In addition, FR-001-AC-1 is tagged but its tests do not verify the exact two M1 keys; the empty-manifest test asserts the opposite. | spec/functional/FR-001-pack-module-and-home.md:19; spec/functional/FR-002-truthful-and-publishable-rights-metadata.md:19-21; spec/functional/FR-003-mdr-software-clause-set.md:25-27; spec/functional/FR-004-mdr-applicability.md:21-23; spec/functional/FR-005-mdcg-companion-and-crosswalks.md:29; spec/functional/FR-006-pack-wide-output-catalog.md:23; spec/functional/FR-007-customer-owned-obligations.md:21-22; spec/functional/FR-008-reference-corpus.md:31-33; spec/non-functional/NFR-001-published-content-respects-reuse-and-standards-boundaries.md:56-60 |

## Coverage

- `quoin matrix --repo . --json` (Quoin 0.34.0; Quire CLI 0.45.0, engine 0.60.0): 28 criteria; 6 tagged; 20 untagged; 2 method-without-symbol. No run evidence is bound.
- The two FR-001-AC-1 binders are `test_manifest_is_clause_only_and_starts_without_sets` and `test_quire_validates_the_module_and_spec_bundle`; neither verifies the exact two-key manifest. The first asserts the opposite.
- `quire coverage --scope . --json` reports 11 unmatched test trace IDs, including `FR-001-AC-3` and `FR-001-AC-6` (ticket acceptance labels, not current spec criterion IDs), plus local `TC-*` identifiers. It reports 19 pre-existing verification rows without test binders.
- Direct scaffold verification: locked-build pytest 9/9; locked-build `make lint` passed. Package/install, output-catalog mismatch, crosswalk missing-target, wheel/npm-content and tracked-generated-directory checks passed.
- Untagged clause-content criteria are outside this scaffold ticket's implementation scope and are expected to land in downstream pack tickets; they remain repository-level assurance gaps in the computed full-spec matrix.
- Plan completion: not assessed.
- Semantic review: skipped.

## Fix dispositions — review follow-up

- Removed invalid FR-001-AC-1 bindings from the empty-manifest and generic validation tests; no placeholder trace tags were added. The FR-001-AC-2 path-install test now checks both manifest and installed catalog contributions.
- Removed unmatched ticket-only FR-001-AC-3/AC-6 tags and non-criterion TC trace tags identified in the review. Remaining trace tags bind only actual criteria asserted by those tests.
- PLAT-1758 tracks extraction of shared clause-pack test helpers. No supported API currently exists; this scaffold retains local helpers pending that follow-up.
- The dependency crosswalk tests now exercise lookup through installed dependency modules, including failure for a missing target clause.
- Fix-round matrix and focused-check evidence will be appended after verification.

### Fix-round verification

- `locked-build.sh <worktree>/target poetry run pytest tests/test_clause_sets.py -q`: 9 passed; `locked-build.sh <worktree>/target make lint` passed Ruff and Black; `git diff --check` passed.
- Recomputed `quoin matrix --repo . --json`: 28 criteria; 3 tagged, 23 untagged, 2 method-without-symbol. FR-001-AC-1 is now untagged, matching the empty scaffold's actual contents. Existing downstream content criteria remain untagged.
- The three remaining test-backed scaffold criterion tags show `unmarked-trace-id` while remaining `tagged`. This behavior also occurs on clean spec-objects-security main for its one-line trace-marker tests, so it is not introduced by this PR.
