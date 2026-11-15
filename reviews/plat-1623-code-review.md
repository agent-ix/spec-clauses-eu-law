---
id: SR-001
title: "Code review — EU-law clause module scaffold PR #2"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-clauses-eu-law@35521ff; tests/conftest.py, tests/test_clause_sets.py, package and CI configuration (PR #2)"
review_set: subset
relationships:
  - { target: "ix://agent-ix/spec-clauses-eu-law/spec", type: references }
---

## Summary

Reviewed PR #2 at 35521ff, including the Python test helpers, npm staging script, Python/npm packaging and CI changes. The ticket's scaffold checks pass, but duplicated helpers, a false FR-001-AC-1 binding and incomplete installed-dependency crosswalk resolution remain.

## Verdict

**FAIL** — a high-severity duplication finding and a false test-to-criterion binding remain.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | The new test helpers duplicate existing clause-pack helpers in spec-objects-security, creating a second implementation that can drift. | tests/conftest.py:30-126; tests/test_clause_sets.py:297-344 |
| FND-002 | high | The empty-manifest test claims FR-001-AC-1, which requires exactly two M1 keys; the test asserts an empty list and therefore makes the matrix report false coverage. | tests/test_clause_sets.py:73-85; spec/functional/FR-001-pack-module-and-home.md:19 |
| FND-003 | medium | Crosswalk resolution only searches the supplied clause-set list; it cannot load a target set from an installed dependency module as the ticket design requires. | tests/conftest.py:163-181 |

## Review Coverage

- The review compared `engine_tool`, set staging, evaluation and record/render helpers against `spec-objects-security/tests/conftest.py` and `tests/test_clause_sets.py`; equivalent behavior is already defined there.
- The ticket acceptance tests ran through `~/dev/worktrees/locked-build.sh`: 9 passed. `make lint` through the same wrapper passed Ruff and Black.
- The PR adds no Rust files, mock-heavy tests, database tests, coverage pragmas or tracked generated directories. `git ls-files` found no `target/`, `dist/` or `node_modules/`.
- Packaging checks inspect the wheel and npm tarball and confirm each contains the manifest and a declared synthetic set. Path install reports `pack: false`; licensed-set fixture install reports `pack: true`. Catalog mismatch and missing crosswalk target diagnostics include both set identifiers.
- Ticket AC6 is checked by the packaging test; its `FR-001-AC-6` tag is not a criterion in this repository's current FR-001. The ticket acceptance itself is exercised, but that tag is unmatched.
- Crosswalk helper limitation: it indexes only the clause sets passed by the caller. It does not load a target from an installed dependency module, as the PLAT-1623 design notes require.
- Test classes and `mocker` are not used; this follows the repository's function-based pytest style, and no mocks or database interactions were added.

## Fix dispositions — review follow-up

- **FND-001 — disposition: follow-up tracked.** No supported shared helper API exists: spec-objects-security defines comparable functions only in its private pytest suite, which is not included in its published module. PLAT-1758 tracks extraction of reusable helpers. This scaffold retains its small local helpers until that API exists.
- **FND-002 — fixed.** Removed the contradictory FR-001-AC-1 traces. The path-install test now verifies the manifest and installed catalog contain no object or artifact contributions, and is tagged to FR-001-AC-2.
- **FND-003 — fixed.** Crosswalk resolution now searches manifest-declared clause sets in installed Quoin modules when a target is not in the supplied set list. Tests cover a present dependency target and a missing clause in an installed dependency set.

Focused checks and resulting head are recorded below after the fix-round run.

### Fix-round verification

- `locked-build.sh <worktree>/target poetry run pytest tests/test_clause_sets.py -q`: 9 passed.
- `locked-build.sh <worktree>/target make lint`: Ruff and Black passed.
- `git diff --check`: passed.
- `quoin matrix --repo . --json`: 28 criteria; 3 tagged, 23 untagged, 2 method-without-symbol. FR-001-AC-1 is untagged after removing the false binding. The three remaining intended criterion tags are recognized as `tagged` but report `unmarked-trace-id`; the same finding reproduces on clean spec-objects-security main with its declared `trace` marker and one-line `@pytest.mark.trace(...)` tests. This is recorded as a clean-main matrix behavior, not a PR-specific finding.
