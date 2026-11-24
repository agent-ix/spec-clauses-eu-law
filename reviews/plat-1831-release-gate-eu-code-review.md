---
id: SR-20261116045021
title: "Code review of PLAT-1831 spec-clauses-eu-law PR #29 (release content-rights gate)"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-clauses-eu-law; README.md, tests/test_publish_gate.py, .github/workflows/ci.yml, .github/workflows/release-npm.yml"
review_set: subset
date: 2026-11-24
---

## Summary

Ticket: PLAT-1831. I reviewed `git diff origin/main...HEAD` at a41e0308 (spec-clauses-eu-law PR #29) in a scratch clone. The PR rewords two README lines, adds an end-to-end test that builds the real wheel and npm archive and runs `scripts/publish_gate.py`, and moves the engineering-assurance checkout `ref:` in both workflows from v0.10.1 to 19d33f67 (the merge of EA #302).

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | No findings (placeholder) | - |

## Verdict

**APPROVE.** No defects.

Verified independently:

- EA 19d33f67 built from source with locked-build.sh (`cargo build --locked --features full --bin engineering-assurance`). EA v0.10.1 built the same way for contrast.
- The new test passes on the PR head with the 19d33f67 binary first on PATH, `npm ci` from npmjs (quoin 0.36.10, quire 0.52.1) and a throwaway HOME. Run time 1.9 s.
- The test fails with EA v0.10.1: the wheel is withheld for `unapproved-external-url` at eu-eu-gmp-annex-11-2011-01.json lines 11, 12 and 17.
- The test fails on main's README with the pinned EA: the npm archive is withheld for `package/README.md:62: tilde-workstation-location` and `package/README.md:355: legal-review-material`.
- The workflow's exact gate command (`python scripts/publish_gate.py --module spec_clauses_eu_law --wheel-dir dist --npm-dir dist --engineering-assurance .deps/engineering-assurance/target/debug/engineering-assurance`) exits 0 on the head after the workflow's build steps. The same command exits 1 with the v0.10.1 binary.
- Both workflow diffs change only the `ref:` line. The SHA is load-bearing: v0.10.1 does not approve the Annex 11 source URLs and no EA tag contains #302.
- The test leaves nothing in the repo: `git status --porcelain --ignored` after the run shows only the pre-existing .venv, node_modules and caches. The wheel and tarball go to tmp_path. npm prepack staging is undone by postpack. The test sets `npm_config_userconfig` to /dev/null, so a dead ~/.npmrc token does not break it. CI's pytest step already has poetry, npm and the EA binary on PATH, so the test runs there.
- README meaning: the install snippet still tells the reader to put the binary on PATH, now in prose. The disclaimer reads "It gives no legal opinion and does not certify anything", which still states that the pack gives no legal opinion.

## Scope examined

- README.md lines 55-66 (examined)
- README.md line 356 (examined)
- tests/test_publish_gate.py test_release_gate_accepts_freshly_built_wheel_and_npm_archive (examined)
- .github/workflows/ci.yml engineering-assurance checkout (examined)
- .github/workflows/release-npm.yml engineering-assurance checkout and gate step (examined)
- scripts/publish_gate.py (context_only)
- scripts/stage-npm.mjs (context_only)
