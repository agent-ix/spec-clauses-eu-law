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

The original FR-011-AC-5 wording did not describe the role-specific Article 30
outcomes when records applicability is missing. The spec-only clarification in
PR #8 now states the outcomes produced by the unchanged clause table and
evaluator.

## Verdict

**RESOLVED BY SPEC CLARIFICATION** — merged FR-011-AC-5 now explicitly states
the known-role and missing-value outcomes; the table and evaluator semantics
remain unchanged.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | Before clarification, AC-5 did not distinguish results of role-specific predicates when `article_30_records_applicability` was missing. The merged AC requires Article 30(1) unresolved for controller/not binding for processor, Article 30(2) not binding for controller/unresolved for processor, and Article 30(3)-(4) unresolved for either role. | spec/spec.md:51,87-99; spec/functional/FR-011-gdpr-role-and-risk-applicability.md:30 |

## Evidence

- Command: `quire clauses evaluate --module spec_clauses_eu_law --authority eu --set gdpr-2016-679 --version 2016-05-04 --context gdpr_role=controller --json` (Quire CLI 0.45.0, engine 0.60.0).
- Result: `art-30(1)(a)` through `(g)` and `art-30(3)`/`(4)` are `unresolved` with `missing_dimension: article_30_records_applicability`; `art-30(2)(a)` through `(d)` are `not_binding` with no reason.
- The same distinction follows from the table: Article 30(2) is `all[eq gdpr_role processor, eq article_30_records_applicability applies]`; known controller context makes the first term false.

## Disposition

Resolved by spec-only PR #8, merge `9e3a569`. The clarified AC matches the
role-specific outcomes shown in the reproduction above. PLAT-1628 now tests
both known-role cases with missing records applicability, as well as missing
role and missing records applicability. No Article 30 clause or evaluator
semantics changed.

## Package content-rights verification follow-up

- Scanner: the published Engineering Assurance v0.10.1 GitHub release binary, SHA-256 `97f09047917f6d9520a1dbd0b403eb2b4b7ea958ec63ac2729113f5a7e7e1d5d`.
- The actual wheel and npm tarball were built from this rebased branch through `locked-build.sh`; the workflow's `scripts/publish_gate.py` ran through the same wrapper using the published scanner.
- Wheel: `spec_clauses_eu_law-0.1.0-py3-none-any.whl`, SHA-256 `ebc993cf6a487a41201bea032bb97d92a901ad64f6f7fb9cc14501e63319ac51`.
- npm: `agent-ix-spec-clauses-eu-law-0.0.0-managed.tgz`, SHA-256 `75d71ad1cd243a08fce35e8dbd623086436be31bc94696fb75d687afdc8cc0c5`.
- The locked-build publish gate passed with exit 0. Direct artifact-scan results from the same `scan_archive` procedure were:

```json
{"archive":"agent-ix-spec-clauses-eu-law-0.0.0-managed.tgz","outcome":"accepted","findings":[]}
{"archive":"spec_clauses_eu_law-0.1.0-py3-none-any.whl","outcome":"accepted","findings":[]}
```

No source URL or package metadata findings remain in either artifact. No suppressions or archive edits were applied; the prior MDR/MDCG and npm metadata findings disappeared after PR #5's packaging changes merged.
