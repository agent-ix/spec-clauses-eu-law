---
id: SR-015
title: "Code review — EU clause pack release dry-run workflow"
type: SpecReview
analysis: code-review
scope: ".github/workflows/release-npm.yml"
review_set: subset
---

## Summary

Reviewed PLAT-1624 PR #19, which moves Quire/Quoin PATH setup before default-module installation in the EU release workflow. The correction addresses the failed dry-run startup while preserving publication checks and the dry-run upload guard.

## Verdict

**PASS** — the focused workflow change fixes the reproduced command lookup failure without changing either publication gate or allowing dry-run uploads.

## Coverage

- Confirmed the workflow's `npm ci` step installs Quoin/Quire before the PATH entry is applied to subsequent steps.
- Confirmed `quoin module ensure-defaults` now follows the PATH step.
- Compared the publish-check and Engineering Assurance packaged-content checks against `origin/main`; their commands and ordering before publication are unchanged.
- Confirmed the reusable publish job still has `if: ${{ inputs.dry_run == false }}`, so `dry_run: true` runs checks and skips publication.
- The original main-branch dry run failed at `quoin module ensure-defaults` with exit 127 (`quoin: command not found`), run 43786392325. PR hosted CI passed at head `7f52b4c9d7d8ec5ff72f281fbb34b2b32202dfae`. The AC6 dry-run on that branch passed in run 43787159810: all publication checks succeeded and the `publish` job was skipped.
- The change is workflow-only, so no production-code gap-analysis lane applies. `quoin gap-analysis` is not an installed CLI command; `quoin matrix --repo . --json` was available and showed no test/spec edits in this diff.

## Findings

| ID      | Severity | Summary                  | Refs |
| ------- | -------- | ------------------------ | ---- |
| FND-001 | low      | No findings (placeholder) | -    |
