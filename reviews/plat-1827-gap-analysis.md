---
id: SR-022
title: "Gap analysis — MDR and MDCG 2019-16 output and crosswalk audit"
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/spec-clauses-eu-law; spec/functional/FR-003-mdr-software-clause-set.md, spec/functional/FR-005-mdcg-companion-and-crosswalks.md, spec/functional/FR-006-pack-wide-output-catalog.md, spec/functional/FR-007-customer-owned-obligations.md, spec_clauses_eu_law/clauses/, tests/"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-003"
    type: reviews
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-005"
    type: reviews
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-006"
    type: reviews
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-007"
    type: reviews
---

## Summary

Ticket: PLAT-1827. `quoin matrix --repo . --json` was run on head d8b6d5e. FR-003-AC-1..4, FR-005-AC-1..4 and FR-006-AC-1..3 are tagged. The new FR-003-AC-4 test (tests/test_clause_sets.py:1084) and FR-005-AC-4 test (:1110) are bound correctly and assert behaviour. The diff has no stubs and no untraced production content. FR-007 is in scope because this PR creates the first customer-owned EU clause. No plan was supplied, so plan completion was not assessed.

## Verdict

**CONDITIONAL.** One gap: FR-007-AC-1 has no test and no inventory, and the PR now gives it a real subject (MDCG 5.2). The discharge regression this exposes is recorded as SR-021 FND-001 and is not duplicated here.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | FR-007-AC-1 is untagged and the spec has no customer-owned inventory. MDCG 5.2 becomes all-procedure in this PR, but no test checks that every all-procedure clause is listed. | spec/functional/FR-007-customer-owned-obligations.md:21, spec/spec.md:281 |

## Coverage

- Bindings verified: test_mdr_security_prerequisite_clauses_map_to_security_and_it_outputs → FR-003-AC-4 (correct). test_mdcg_security_sections_map_to_security_and_customer_outputs → FR-005-AC-4 (correct).
- Pre-existing, outside this diff: FR-006-AC-3 (`test_all_declared_sets_share_one_output_catalog`, tests/test_clause_sets.py:793) passes vacuously when `spec_clauses_us_health` is not installed, because `_installed_clause_sets` returns []. FR-006's Dependencies section requires the gate to fail instead. Against spec-clauses-us-health origin/main, six shared names drift: anomaly-list, release-record, risk-management-records, software-architecture, software-requirements and verification-records. The CI checkout of the older ca78ac0 hides this. This PR's catalog edits (it-requirements-statement, which is not in the US catalog, and soup-list and written-procedure, which match US exactly) add no drift.
