---
id: SR-025
title: "Gap analysis — Annex 11 acceptance criteria versus tests"
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/spec-clauses-eu-law; PR #21 git diff origin/main...HEAD at 645527d4: tests/test_annex11.py, tests/annex11_spec.py, tests/test_clause_sets.py, spec_clauses_eu_law/manifest.yaml, spec_clauses_eu_law/clauses/eu-eu-gmp-annex-11-2011-01.json, spec FR-001, FR-023..FR-028, NFR-004"
review_set: subset
date: 2026-11-23
---

## Summary

Ticket: PLAT-1832. Reviewed `git diff origin/main...HEAD` at 645527d4e838b4b46c25192ec45b043a1680dba4 of agent-ix/spec-clauses-eu-law PR #21. Method: gap-analysis.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | Coverage inflation. The matrix shows FR-027-AC-2 as covered (tests/test_annex11.py:564), but the covering assertion is a test helper. | spec/functional/FR-027-annex-11-corpus-discharge.md:34 |
| FND-002 | medium | Partially covered: only the missing-approvalRef branch has a test. | spec/functional/FR-028-annex-11-human-decisions.md:24 |

## Finding details

### FND-001 — FR-027-AC-2

Coverage inflation. The matrix shows FR-027-AC-2 as covered (tests/test_annex11.py:564), but the covering assertion is a test helper. The shipped pack is data only and quoin origin/main accepts the direct fact (measured: clause `2` renders `compliant`). The AC is unmet by the product.

Expected fix: Same as SR-024 FND-001: assert through quoin, or record the AC as blocked on quoin FR-211.

### FND-002 — FR-028-AC-2

Partially covered: only the missing-approvalRef branch has a test. The blank and unresolved branches have none, and the AC names the wrong state ('unresolved' instead of 'undischarged').

Expected fix: See SR-024 FND-003.

## Scope examined

- FR-001-AC-1 (examined)
- FR-023-AC-1 (examined)
- FR-023-AC-2 (examined)
- FR-023-AC-3 (examined)
- FR-023-AC-4 (examined)
- FR-024-AC-1 (examined)
- FR-024-AC-2 (examined)
- FR-024-AC-3 (examined)
- FR-024-AC-4 (examined)
- FR-024-AC-5 (examined)
- FR-025-AC-1 (examined)
- FR-025-AC-2 (examined)
- FR-025-AC-3 (examined)
- FR-025-AC-4 (examined)
- FR-025-AC-5 (examined)
- FR-025-AC-6 (examined)
- FR-026-AC-1 (examined)
- FR-026-AC-2 (examined)
- FR-026-AC-3 (examined)
- FR-026-AC-4 (examined)
- FR-027-AC-1 (examined)
- FR-027-AC-2 (examined)
- FR-027-AC-3 (examined)
- FR-027-AC-4 (examined)
- FR-027-AC-5 (examined)
- FR-028-AC-1 (examined)
- FR-028-AC-2 (examined)
- FR-028-AC-3 (examined)
- NFR-004-AC-1 (examined)
- NFR-004-AC-2 (examined)

## Verdict

Every FR-001, FR-023..FR-028 and NFR-004 criterion except FR-025-AC-5 (Inspection; inspected, clean) is tagged by at least one test in tests/test_annex11.py or tests/test_clause_sets.py, and all of them pass. The gaps are FR-027-AC-2, where the coverage is a test helper and not the product, and FR-028-AC-2, which is only partly covered. Reverse gap: the shipped JSON carries `approvalRoles: [system-owner]`, plus `title` and `subjects` on every clause, and no requirement defines those values (SR-024 FND-002). No stub was found.

## New findings (disposition pass 1)

Reviewed `git diff 645527d4..355a76a9`. Tests: test_annex11.py, test_clause_sets.py, test_pack_discharge.py, 84 passed with spec-clauses-us-health origin/main installed from a temp copy and removed afterwards.

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-003 | medium | `_assert_customer_owned_facts` is still the only customer-owned check behind an FR-007 trace. test_records_facts_and_renders_both_clause_sets is tagged FR-007-AC-2, which now reads 'renders as tailored through quoin discharge --rmm'. That t | tests/test_pack_discharge.py:818-825,908 |

### FND-003 — FR-007-AC-2

`_assert_customer_owned_facts` is still the only customer-owned check behind an FR-007 trace. test_records_facts_and_renders_both_clause_sets is tagged FR-007-AC-2, which now reads 'renders as tailored through quoin discharge --rmm'. That test calls the helper on its own fixture facts (line 908) and never asserts a tailored row (no 'tailored' anywhere in tests/test_pack_discharge.py). The Annex 11 corpus test does assert `tailored` for all ten customer-owned clauses through quoin, but it is tagged FR-027-AC-2, not FR-007-AC-2.

Expected fix: Tag the Annex 11 corpus test with FR-007-AC-2 (it proves the AC through quoin) and drop the FR-007-AC-2 tag from test_records_facts_and_renders_both_clause_sets. Either delete the helper call or keep it only as a fixture sanity check that no trace claims.

## Dispositions

Round 1 at head 355a76a9b4f3b9757913b38bf714ee1aebcbc4b6; round 2 at head 1f35d5e7b3adee40b9d1ef3d9c3344e0c3584041.

| FND | outcome | reason |
|---|---|---|
| FND-001 | deferred | deferred: PLAT-1805. Lead decision (Round 2 lead): rejecting a direct fact on a customer-owned clause is quoin's job under quoin FR-211, which PLAT-1805 is implementing. FR-007-AC-3 and FR-027-AC-6 now state that requirement and are untested until FR-211 ships. The helper-based test test_all_procedure_clauses_accept_only_a_delegated_disposition was removed, and FR-027-AC-2 is narrowed to 'delegated disposition renders tailored', which the corpus test asserts through quoin. |
| FND-002 | fixed | - |
| FND-003 | fixed | - |
