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

## Package content-rights verification follow-up

- Scanner: the published Engineering Assurance v0.10.1 GitHub release binary, SHA-256 `97f09047917f6d9520a1dbd0b403eb2b4b7ea958ec63ac2729113f5a7e7e1d5d`.
- The wheel and npm tarball were built from this branch through `~/dev/worktrees/locked-build.sh`, unpacked without file edits into temporary Git-selected trees, and scanned with `engineering-assurance content-rights-tree`.
- Wheel: `spec_clauses_eu_law-0.1.0-py3-none-any.whl`, SHA-256 `83f8b001b8ca175e4f4fc038a0200eacdb6b4ffb7d70d4c69c8d75439dfa7e8e`.
- npm: `agent-ix-spec-clauses-eu-law-0.0.0-managed.tgz`, SHA-256 `94cb930c071e453aa52aea5bdf781cf62da7e9e2596f1e563d1ddfc8b6f079c5`.
- The GDPR ELI and legal-notice URLs produce no finding in either artifact. No suppression was added. The remaining findings are on unchanged MDR/MDCG attribution lines and npm package repository metadata.

Exact scanner output for the wheel:

```json
{"protocol":"engineering-assurance.content-rights-tree-result/v1","outcome":"withheld","inspected_entries":10,"findings":[{"path":"spec_clauses_eu_law/clauses/eu-mdcg-mdcg-2019-16-rev1.json","line":12,"category":"unapproved-external-url"},{"path":"spec_clauses_eu_law/clauses/eu-mdr-2017-745-2026-07-19.json","line":12,"category":"unapproved-external-url"}]}
```

Exact scanner output for npm:

```json
{"protocol":"engineering-assurance.content-rights-tree-result/v1","outcome":"withheld","inspected_entries":8,"findings":[{"path":"package/clauses/eu-mdcg-mdcg-2019-16-rev1.json","line":12,"category":"unapproved-external-url"},{"path":"package/clauses/eu-mdr-2017-745-2026-07-19.json","line":12,"category":"unapproved-external-url"},{"path":"package/package.json","line":15,"category":"unapproved-external-url"}]}
```
