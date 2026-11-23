---
id: SR-033
title: "Gap analysis — GDPR clause set re-audit"
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/spec-clauses-eu-law; PR #26 at b249533c14d97ef55d58a8a344f747e5056e6757; FR-010, FR-012, FR-013 and the GDPR clause JSON"
review_set: subset
date: 2026-11-23
relationships:
  - { target: "ix://agent-ix/spec-clauses-eu-law/FR-012", type: references }
---

## Summary

Ticket: PLAT-1829. Planless gap analysis over the criteria this PR touches, using `quoin matrix --repo . --json` (quoin 0.36.10) at the PR head and on origin/main, followed by mutation checks of the tagged tests. Plan completion: not assessed.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | FR-012-AC-2 is tagged only to the disposition cases of test_gdpr_dpia_fact_without_approval_ref_stays_open, and those cases pass whether or not the pack declares approvalRoles. Nothing that depends on the pack backs the AC. | tests/test_pack_discharge.py:733-736 |
| FND-002 | low | FR-013-AC-1 and FR-013-AC-2 show static_status untagged in quoin matrix at head and on origin/main. AC-1 has no tagged test. AC-2's tag in the test_records_facts_and_renders_both_clause_sets marker is not picked up. | tests/test_pack_discharge.py:826-831 |

## Finding details

### FND-001 — FR-012-AC-2

Measured: quoin rejects an `accepted_risk` disposition that has no approvalRef or a blank one at record time, with the same error whether or not art-35 declares approvalRoles. The AC binding is therefore satisfied by quoin alone, and stripping the pack's roles does not fail it.

Expected fix: Delete FR-012-AC-2 and its test cases (see SR-034 FND-002), or rewrite the AC into something the pack controls. A binding to a quoin-invariant behaviour is not coverage of this module.

### FND-002 — FR-013-AC-2

On both head and origin/main, quoin matrix reports FR-013-AC-1 and FR-013-AC-2 as untagged with no binders. The PR edits FR-013's Dependencies text, so the FR is touched.

Expected fix: Tag (or write) a test asserting that each Article 30(1)(a)-(g) and 30(2)(a)-(d) clause names records-of-processing (AC-1). Find out why the multi-id marker at tests/test_pack_discharge.py:826-831 does not bind FR-013-AC-2 when FR-008-AC-2/3 in the same marker do bind; the docstring Trace line names only FR-008. Fix that so AC-2 shows as tagged.

## Verdict

Changes requested on FND-001. Bindings verified:

- FR-010-AC-3 → test_gdpr_processing_outputs_are_product_side_and_customer_supplied: correct. Fails on the origin/main JSON.
- FR-010-AC-4 → test_gdpr_art30_supervisory_access_names_a_person_procedure: correct. Fails on the origin/main JSON.
- FR-012-AC-1 → test_gdpr_article35_clauses_declare_the_privacy_officer_role: correct. This is a static guard on approvalRoles.
- FR-012-AC-1 → test_gdpr_dpia_fact_without_approval_ref_stays_open: only the [None-direct] case discriminates (SR-032 FND-001).
- FR-012-AC-3: Inspection; it has no test symbol, which is expected for that method.
- Removing the helper-only trace tags was correct.

## Scope examined

- FR-010-AC-3 (examined)
- FR-010-AC-4 (examined)
- FR-012-AC-1 (examined)
- FR-012-AC-2 (examined)
- FR-012-AC-3 (examined)
- FR-013-AC-1 (examined)
- FR-013-AC-2 (examined)
- FR-010-AC-1 (context_only)
- FR-010-AC-2 (context_only)
