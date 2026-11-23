---
id: SR-20261104139948
title: "Code review of PLAT-1831 spec-clauses-eu-law PR #28 (catalog producers)"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-clauses-eu-law; spec_clauses_eu_law/clauses/*.json, tests/conftest.py, tests/test_annex11.py, tests/test_clause_sets.py (PR #28 head 21140948ca77bb8eaedcdffb0929979e7eb63074)"
review_set: subset
---

## Summary

Ticket: PLAT-1831. Diff reviewed: `git diff origin/main...HEAD` at head 2114094. The PR adds `"producers": ["run"]` to `verification-records` in six EU sets. It adds a `producers` reader to the spec catalog parser, an `assert_shared_producers_identical` helper with a drift-fixture test, an FR-211 kind test and a quire acceptance test.

The tests ran against spec-clauses-us-health PR #42 (head fba28a1), installed as a path module in a throwaway HOME with quoin 0.36.10 and quire 0.52.1. `tests/test_clause_sets.py -k "producers or catalog"`: 8 passed. `tests/test_annex11.py tests/test_pack_discharge.py`: 40 passed. With the old EU set data restored, the parity test, the three subset tests and the FR-211 kind test fail. The drift test, the mismatch test and `test_quire_accepts_sets_that_carry_producers` still pass.

## Verdict

**Changes requested (low only).** The data matches US #42: `verification-records` has the same description and `producers: ["run"]` in both packs, and the shared `system-validation` has no `producers` in either. The mapping is correct; see the US review for the quoin evidence. Quoin 0.36.10 ignores `producers`, and the existing Annex 11 and pack `record-discharge` tests pass with `producers` present. The new helper is a duplicate: the existing `assert_output_catalog_consistent` compares whole catalog definitions, and it rejects both a `["scan"]` drift and a missing `producers` (checked directly).

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | `assert_shared_producers_identical` duplicates `assert_output_catalog_consistent`, which already compares whole definitions and fails on a `producers` drift or a missing `producers`. Both call sites run right after the existing check and add no detection, and the FR-006-AC-5 drift test exercises the duplicate. Delete the helper and point the drift fixture at `assert_output_catalog_consistent`. | tests/conftest.py:163-176; tests/test_clause_sets.py:828,831-856; tests/test_annex11.py:292 |
| FND-002 | low | `test_quire_accepts_sets_that_carry_producers` passes on data with no `producers` (verified on origin/main data). It repeats the existing `publish-check` and evaluate runs over PACKAGE_ROOT (test_clause_sets.py:746,1022,1693; test_annex11.py:74,162). Delete it with FR-006-AC-6. | tests/test_clause_sets.py:2589-2611 |
| FND-003 | low | `test_catalog_producers_name_only_fr_211_kinds_and_match_the_spec` re-checks quire FR-073-AC-9 shape rules and the per-set table equality that `_spec_output_catalog` already gives the subset tests. Keep only the FR-211 membership check of the spec table. | tests/test_clause_sets.py:2569-2586 |

## Dispositions

Round 1, checked against `git diff 21140948..26539266` (head 265392667df3a4a9655feea3401516b8340975e6), with us-health #42 at eb8b71d installed as a path module. `tests/test_clause_sets.py -k "producers or catalog"` plus `test_annex11.py::test_shared_outputs_equal_the_us_health_law_catalog` gives 8 passed. `test_annex11.py test_pack_discharge.py` gives 40 passed. The drift fixture raises for both `["scan"]` and an absent `producers`. A mutant of `assert_output_catalog_consistent` that compares only kind and description makes it fail, so the fixture is not vacuous.

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | `assert_shared_producers_identical` and its three call sites are removed. The drift fixture now calls `assert_output_catalog_consistent` and is traced to FR-006-AC-3. |
| FND-002 | fixed | `test_quire_accepts_sets_that_carry_producers` and FR-006-AC-6 are removed. |
| FND-003 | fixed | Reduced to `test_spec_producers_name_only_fr_211_kinds`, which checks spec-table kinds against the family set only. |
