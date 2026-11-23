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
