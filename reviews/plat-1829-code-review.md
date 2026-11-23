---
id: SR-032
title: "Code review — GDPR clause set re-audit"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-clauses-eu-law; PR #26 at b249533c14d97ef55d58a8a344f747e5056e6757; tests/test_pack_discharge.py, tests/test_clause_sets.py, tests/corpus/gdpr, spec_clauses_eu_law/clauses/eu-gdpr-2016-679-2016-05-04.json"
review_set: subset
date: 2026-11-23
relationships:
  - { target: "ix://agent-ix/spec-clauses-eu-law/FR-012", type: references }
---

## Summary

Ticket: PLAT-1829. Reviewed `git diff origin/main...HEAD` of PR #26 at b249533c14d97ef55d58a8a344f747e5056e6757. Method: code-review (Python lane). Tests run in a temporary clone with the repo's npm toolchain (quoin 0.36.10, quire 0.52.1, engineering-assurance 0.10.1) and a throwaway HOME.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | test_gdpr_dpia_fact_without_approval_ref_stays_open mostly cannot fail on the pack: with approvalRoles removed from every art-35 clause, 5 of its 6 cases still pass. Only [None-direct] fails. | tests/test_pack_discharge.py:733-824 |
| FND-002 | low | Two untagged GDPR tests check only the test helper _assert_named_person_approvals against hand-built dicts, not the pack or quoin. | tests/test_pack_discharge.py:656-697 |

## Finding details

### FND-001 — FR-012-AC-1

Measured by mutation in a temp clone. Setting `approvalRoles: []` on every art-35 clause leaves 5 of 6 parametrized cases passing. Probe results for each case:

- direct + None: with roles, recorded and `undischarged` ("required approval reference is missing"). Without roles, `compliant`. This is the only case that fails under the mutation.
- direct + "" or "   ": with roles, recorded and `undischarged`. Without roles, record-discharge rejects with "approvalRef must not be empty", and the `else` branch accepts that rejection. The case passes both ways.
- disposition + None, "" or "   ": record-discharge rejects in both configurations ("disposition discharge fact is missing approvalRef" / "must not be empty"). This is quoin behaviour that does not depend on the pack, so all three cases pass both ways.

The test also has no positive control. Nothing in it shows that the same fact with a valid approvalRef reaches `compliant`, so an `undischarged` result cannot be attributed to the missing approval rather than to any other gap.

Expected fix:
(1) Drop the `else` rejection branch. For direct facts, assert `recorded.returncode == 0`, then assert that the art-35(1) row is `undischarged` with reason "required approval reference is missing".
(2) Drop the disposition parametrization. Its behaviour belongs to quoin (see SR-034 FND-002).
(3) Add a positive control in the same harness: the same direct fact with `approvalRef` and `attestation.attestedBy` set to `person://example.invalid/people/privacy-officer` must report `compliant`. This was measured to report `compliant` today.

With these changes, the approvalRoles mutation fails every remaining case: None becomes compliant, and blank values are rejected at record time.

### FND-002 — tests/test_pack_discharge.py#test_gdpr_dpia_discharge_requires_named_person_approval

`test_gdpr_dpia_discharge_requires_named_person_approval` and `test_gdpr_dpia_direct_fact_passes_with_named_approval` lost their trace tags in this PR. They now exercise only a test-side helper against dicts the test builds itself. They check the test, not the module.

Expected fix: Delete both tests. Also drop the GDPR branch call to `_assert_named_person_approvals` in `test_records_facts_and_renders_both_clause_sets`, which only validates that test's own synthetic facts.

## Verdict

Changes requested (FND-001). The clause-set tests are sound:

- test_gdpr_processing_outputs_are_product_side_and_customer_supplied and test_gdpr_art30_supervisory_access_names_a_person_procedure both fail when the origin/main GDPR JSON is swapped back in.
- test_gdpr_article35_clauses_declare_the_privacy_officer_role is the real guard on approvalRoles; it passes on the old JSON because roles did not change.
- test_records_facts_and_renders_both_clause_sets passes with the new processing-access-control corpus record.
- ruff and black are clean on both test files.
- No count or version pins were added.
- Corpus records are marked `suppliedBy: customer` and are not presented as tool output.

## Scope examined

- tests/test_pack_discharge.py#test_gdpr_dpia_fact_without_approval_ref_stays_open (examined)
- tests/test_pack_discharge.py#_dpia_fact (examined)
- tests/test_pack_discharge.py#GDPR_EVIDENCE_REFS (examined)
- tests/test_pack_discharge.py#test_records_facts_and_renders_both_clause_sets (examined)
- tests/test_clause_sets.py#test_gdpr_processing_outputs_are_product_side_and_customer_supplied (examined)
- tests/test_clause_sets.py#test_gdpr_art30_supervisory_access_names_a_person_procedure (examined)
- tests/test_clause_sets.py#test_gdpr_article35_clauses_declare_the_privacy_officer_role (examined)
- tests/corpus/gdpr/processing-access-control.json (examined)
- tests/corpus/gdpr/privacy-by-default-settings.json (examined)
- spec_clauses_eu_law/clauses/eu-gdpr-2016-679-2016-05-04.json (examined)
