---
id: SR-005
title: "Code review — PLAT-1629 Article 32 crosswalks"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-clauses-eu-law; PR #10 at 249493c5959afdd5b83ef2c10e39377be35b3762; Article 32 data and crosswalk tests"
review_set: subset
relationships:
  - { target: "ix://agent-ix/spec-clauses-eu-law/FR-014", type: references }
---

## Summary

The crosswalk data matches FR-014's five-clause scope, all exact NIST and HIPAA targets resolve in the installed modules, the rights metadata publishes cleanly, the no-copy check matches the ticket's filename rule, and the wheel/npm archive scans pass with Engineering Assurance 0.10.1. CI is green. The ticket AC wording conflicts with the source specification about Article 32(4), and its literal `quire validate --module <pkg>` command is not valid Quire 0.45.0 syntax.

## Verdict

**CONDITIONAL** — reconcile the ticket's Article 32 scope with FR-014 and make the validation AC executable and verifiable.

## Findings

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-001 | medium | PLAT-1629 AC-1 says “Every Art 32 clause,” which includes `art-32(4)` in the normative GDPR clause table. FR-014 and the Crosswalk Policy require targets only for 32(1)(a)–(d) and 32(2); the data and test follow that narrower scope. No target mapping for 32(4) is specified. The ticket and source spec need an explicit scope decision. | PLAT-1629 AC-1; spec/spec.md:100-105,121-123; spec/functional/FR-014-article-32-crosswalks.md:15-25; tests/test_clause_sets.py:837-841 |
| FND-002 | medium | PLAT-1629 AC-4's literal `quire validate --module <pkg>` invocation exits 2 because Quire 0.45.0 requires a positional Markdown document or glob; the module path alone does not validate clause-set JSON. CI exercises `publish-check`, but no test validates the AC's stated command or an equivalent clearly specified validation invocation. | PLAT-1629 AC-4; tests/test_clause_sets.py:949-960 |

## Review Coverage

- The 15 crosswalk rows map `art-32(1)(a)` through `(d)` and `(2)` to NIST `sp800-53@5.2.0` and HIPAA `45-cfr-164-subpart-c@2026-11-12`. The tests assert the exact pair sets, require non-empty rationales, prohibit `equivalent`, and run the resolver.
- Actual installed NIST module: `spec-objects-security` v0.13.0; HIPAA module: the pinned `spec-clauses-us-health` commit `ca78ac063186e5ff8d8e074382a3527b6b84d0b8`. Every referenced target clause ID resolved.
- `git ls-files` contains no `nist-sp800-53*` or `us-hhs-*` set file.
- `quire publish-check --module spec_clauses_eu_law` passed. A wheel and npm tarball were built; `scripts/publish_gate.py` accepted both with the CI-pinned Engineering Assurance v0.10.1 checker. The installed 0.8.2 checker rejected the new public URL hosts, so it was not used as the verdict source.
- Focused crosswalk and no-copy tests: 2 passed. PR CI: 35 tests passed, lint passed, and aggregate checks passed at head `249493c5959afdd5b83ef2c10e39377be35b3762`.
- The workflow checks out the US module at immutable commit `ca78ac063186e5ff8d8e074382a3527b6b84d0b8` and installs NIST at v0.13.0.
- `quire validate --module spec_clauses_eu_law` exits 2 with the usage error that `<DOC_OR_GLOB>` is required. The repo's valid specification invocation supplies `spec/**/*.md`; this is distinct from validating the JSON clause-set module.
- No Quoin gap-analysis was run because the diff changes JSON clause data, tests, and CI configuration but no production code or spec artifacts. No spec-review method was run because the PR does not change `spec/**` or `plan/**`.

## Findings data

```yaml
findings:
  - fnd: FND-001
    severity: medium
    confidence: high
    method: code-review
    check: spec-code-faithfulness
    artifact_id: PLAT-1629-AC-1
    related_ids: [FR-014-AC-1]
    path: spec/spec.md
    lines: "100-105, 121-123"
    excerpt: "| `art-32(4)` | always | `access-control`, `written-procedure`, `training-record` |\nCrosswalks originate from `art-32(1)(a)` through `(d)` and `art-32(2)`."
    finding: "The ticket's all-Article-32 AC includes art-32(4), while FR-014 and the spec crosswalk policy scope targets to 32(1)(a)-(d) and 32(2). The implementation follows FR-014 and omits art-32(4), for which no targets are specified."
  - fnd: FND-002
    severity: medium
    confidence: high
    method: code-review
    check: acceptance-criteria-verification
    artifact_id: PLAT-1629-AC-4
    related_ids: [FR-014-AC-2]
    path: tests/test_clause_sets.py
    lines: "949-960"
    excerpt: "result = run(engine_tool(\"quire\"), \"publish-check\", \"--module\", str(PACKAGE_ROOT))"
    finding: "The literal `quire validate --module <pkg>` AC invocation exits 2 because Quire 0.45.0 requires a positional Markdown document or glob. The current CI covers publish-check but has no assertion for a clearly specified equivalent validation command."
```

## New findings (disposition pass 1)

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-003 | medium | The Article 32 crosswalk test only builds `actual` for the six expected source IDs. It never asserts that every crosswalk source is one of those IDs, so an extra Article 32(3) row or other out-of-scope source can pass when its target resolves, despite FR-014-AC-1 explicitly prohibiting Article 32(3) crosswalks. | tests/test_clause_sets.py:839-871; spec/functional/FR-014-article-32-crosswalks.md:24 |

## Dispositions

| FND | outcome | reason |
|---|---|---|
| FND-001 | fixed | The Article 32(4) NIST and HIPAA targets and their bounded partial rationales are now specified and implemented; the exact-pair test checks both targets. |
| FND-002 | fixed | FR-014-AC-4 now specifies valid doc/glob validation and publish-check commands, and the test suite invokes both. |

| FND-003 | fixed | The exact source-set check now runs against the actual GDPR crosswalks, and a regression test injects `art-32(3)` and requires a named failure. |
