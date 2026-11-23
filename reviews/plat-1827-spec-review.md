---
id: SR-023
title: "Spec review — MDR and MDCG 2019-16 output and crosswalk audit"
type: SpecReview
analysis: base
scope: "agent-ix/spec-clauses-eu-law; spec/spec.md, spec/functional/FR-003-mdr-software-clause-set.md, spec/functional/FR-005-mdcg-companion-and-crosswalks.md"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-003"
    type: reviews
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-005"
    type: reviews
---

## Summary

Ticket: PLAT-1827. Reviewed the MDR Clause Table edits, the MDCG Companion Table edits, the catalog description change, and new criteria FR-003-AC-4 and FR-005-AC-4. Sub-analyses: none of the quoin spec-review sub-analyses applies. No FR statement changed, so EARS analysis has nothing to check. No structural, object or relationship edges changed. The new ACs were checked for testability and for agreement with the tables.

## Verdict

**CONDITIONAL.** The I-17.4, I-18.8, I-17.2 and II-5 rows now read the MDR correctly. The customer-supplied wording of `it-requirements-statement` is honest. Both new ACs can fail. Three gaps remain. The audit left I-14.2(d) mapped only to a document with no producer. FR-003-AC-4 does not state the I-17.2 and II-5 changes that its test asserts. FR-005-AC-4 does not name the crosswalk retargets that its test asserts.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | I-14.2(d) is a design duty to reduce risk from adverse software and IT-environment interaction, but it expects only `it-requirements-statement`, now declared customer-supplied with no producer. The risk-control evidence (security or risk records) is missing from the audited MDR table. | spec/spec.md:69, spec_clauses_eu_law/clauses/eu-mdr-2017-745-2026-07-19.json:118 |
| FND-002 | low | FR-003-AC-4 covers only I-17.4 and I-18.8. The PR also changes I-17.2 (adds verification-records) and II-5 (adds risk-management-records), and the AC-4 test asserts both, so the test does more than its AC states. | spec/functional/FR-003-mdr-software-clause-set.md:28, tests/test_clause_sets.py:1098-1099 |
| FND-003 | low | FR-005-AC-4 states only output expectations. The test also asserts crosswalk pairs (3.7→I-17.2, 3.6→I-17.4, not 3.7→I-17.4) that no AC names. | spec/functional/FR-005-mdcg-companion-and-crosswalks.md:30, tests/test_clause_sets.py:1125-1131 |

## Coverage

- Examined: MDR rows I-14.2(d), I-17.2, I-17.4, I-18.8, II-5. MDCG rows 2.1, 2.3, 2.6, 3.1, 3.2, 3.3, 3.6, 3.7, 3.8, 4.3, 5.1, 5.2. Catalog row it-requirements-statement. FR-003-AC-4, FR-005-AC-4.
- The spec prose has no standard text, designators, scores, classes or ticket narration.
