---
id: SR-027
title: "Gap analysis — AI Act and Annex IV output and crosswalk audit"
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/spec-clauses-eu-law; spec/functional/FR-017-ai-act-high-risk-obligations.md, spec/functional/FR-021-ai-act-mdr-crosswalks.md, spec/functional/FR-006-pack-wide-output-catalog.md, spec/functional/FR-007-customer-owned-obligations.md, spec_clauses_eu_law/clauses/, tests/test_clause_sets.py"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-017"
    type: reviews
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-021"
    type: reviews
---

## Summary

Ticket: PLAT-1828. PR agent-ix/spec-clauses-eu-law#23 at head 082a7ee32e8b5e7f6c785035a14e8400da182867. This gap analysis covers the touched FRs: FR-017 (AC-1 to AC-5), FR-021 (AC-1 to AC-4), FR-006-AC-3 for catalog parity, and the customer-owned inventory. It checked AC-to-test tags, AC-to-data agreement, and stubs and inflated coverage in the new tests.

## Verdict

**CHANGES REQUESTED (one medium).** Every AC of FR-017 and FR-021 has a tagged test (`@pytest.mark.trace`). FR-017-AC-5 and FR-021-AC-4 are new and each tagged once, and both tests fail on origin/main data. The data agrees with the spec tables for art-73, IV-9 and the catalog descriptions. The gap is that FR-017-AC-5's second clause, "every other output the AI Act sets use names its producing command or artifact archetype", is neither true of the data nor asserted. `written-procedure` ("Customer-owned written procedure.") names no producer. The test only checks that the other outputs are not labelled customer-supplied.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | FR-017-AC-5 claims every non-customer-supplied output names its producing command or archetype. `written-procedure` does not, and the test asserts only the absence of "customer-supplied", so an output with no producer and no label would pass. Fix: carve out the customer-owned `written-procedure` procedure in the AC. In the test, assert that each remaining description names a backticked command or archetype, or that the output kind is `procedure`. | spec/functional/FR-017-ai-act-high-risk-obligations.md:27, tests/test_clause_sets.py:1316-1319 |

## Coverage

- Tags: FR-017-AC-1..5 and FR-021-AC-1..4 are each present in `tests/test_clause_sets.py`.
- Focused run on the branch, with the US module installed from a temporary copy of us-health origin/main: 21 passed in `test_clause_sets.py` and 15 passed in `test_pack_discharge.py`.
- On old data (origin/main spec.md and AI Act JSON in a temporary copy), both new tests fail.
- No stubs. The `CUSTOMER_SUPPLIED_AI_OUTPUTS` constant restates the AC's own list. It is the assertion's subject, not a count pin.

## Dispositions

Disposition pass 1, head cba6ffb91b6170f5a192ead07d3670e38239e157, fix commits 96e9d2f and cba6ffb.

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | FR-017-AC-5 now exempts the customer-owned `written-procedure`. The test skips only `kind == "procedure"` outputs and asserts that each remaining non-customer-supplied description names a backticked command or archetype. The art-73 half moved to the new FR-017-AC-6, with its own test. Focused run: 26 passed in `test_clause_sets.py` and 14 in `test_pack_discharge.py`, with a throwaway HOME and us-health origin/main installed. All three PLAT-1828 tests fail on origin/main data. |
