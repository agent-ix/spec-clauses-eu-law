---
id: SR-004
title: "Article 30 missing-applicability outcome"
type: SpecReview
analysis: correctness
scope: "PLAT-1628 GDPR Article 30 clause applicability"
review_set: subset
relationships:
  - { target: "ix://agent-ix/spec-clauses-eu-law/FR-011", type: references }
---

## Summary

The GDPR table's role-specific Article 30 expressions and FR-011-AC-5 disagree
about the result when records applicability is missing but the role is known.
The table leaves processor-only Article 30(2) clauses `not_binding` for a known
controller, while FR-011-AC-5 says a missing applicability value leaves all
Article 30(1)-(4) clauses unresolved.

## Verdict

**NEEDS SPEC OWNER DISPOSITION** — implementation follows the table as written;
the AC-5 wording does not currently describe that result for either known role.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | With `gdpr_role=controller` and no `article_30_records_applicability`, the seven Article 30(1) clauses and Article 30(3)-(4) are unresolved, but Article 30(2)(a)-(d) are not_binding because their role predicate is false. FR-011-AC-5 says the missing value leaves all Article 30(1)-(4) unresolved. | spec/spec.md:51,87-99; spec/functional/FR-011-gdpr-role-and-risk-applicability.md:30 |

## Evidence

- Command: `quire clauses evaluate --module spec_clauses_eu_law --authority eu --set gdpr-2016-679 --version 2016-05-04 --context gdpr_role=controller --json` (Quire CLI 0.45.0, engine 0.60.0).
- Result: `art-30(1)(a)` through `(g)` and `art-30(3)`/`(4)` are `unresolved` with `missing_dimension: article_30_records_applicability`; `art-30(2)(a)` through `(d)` are `not_binding` with no reason.
- The same distinction follows from the table: Article 30(2) is `all[eq gdpr_role processor, eq article_30_records_applicability applies]`; known controller context makes the first term false.

## Disposition

No table or engine semantics changed. The spec owner should clarify whether AC-5
means that only clauses role-applicable under the table remain unresolved, or
that all Article 30(1)-(4) clauses must remain unresolved until the records
applicability value is supplied. PLAT-1628 tests the declared table and keeps
the unresolved result for empty context.
