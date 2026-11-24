---
id: SR-20261116045022
title: "Gap analysis of PLAT-1831 spec-clauses-eu-law PR #29 (release content-rights gate)"
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/spec-clauses-eu-law; tests/test_publish_gate.py; NFR-001-AC-2, NFR-004-AC-1"
review_set: subset
date: 2026-11-24
---

## Summary

Ticket: PLAT-1831. Planless gap analysis scoped to PR #29 at a41e0308, using `quoin matrix` (quoin 0.36.10) at the head. The PR changes no production code; it adds one test and rewords README lines. Plan completion: not assessed.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | The new test runs the content-rights scan over the real built wheel and npm archive, which is the "a scan of package files passes" half of NFR-001-AC-2, but it carries no trace tag. Its three sibling tests in the same file carry `@pytest.mark.trace("NFR-001-AC-2")`. | tests/test_publish_gate.py:204 |

## Finding details

### FND-001 — NFR-001-AC-2

NFR-001-AC-2: "The publishable package contains no name or designator of a harmonised or other paywalled standard; a scan of package files passes and identifies the file and line for an injected fixture." The existing tagged tests cover the injected-fixture half on synthetic trees. The new test is the only one that scans the real publishable packages, yet quoin matrix does not see it.

Expected fix: add `@pytest.mark.trace("NFR-001-AC-2")` to test_release_gate_accepts_freshly_built_wheel_and_npm_archive.

## Verdict

One low finding; mergeable. NFR-001-AC-2 is already reported as tagged by the sibling tests, so this is a traceability gap, not missing coverage. NFR-004-AC-1 (Annex 11 source URL and rights) is examined: the new test now proves the Annex 11 source URLs pass the release scan, which previously failed with `unapproved-external-url` under EA v0.10.1.

## Scope examined

- NFR-001-AC-2 (examined)
- NFR-004-AC-1 (examined)
- NFR-004-AC-2 (context_only)
