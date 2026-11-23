---
id: SR-021
title: "Code review — MDR and MDCG 2019-16 output and crosswalk audit"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-clauses-eu-law; spec/spec.md, spec_clauses_eu_law/clauses/eu-mdr-2017-745-2026-07-19.json, spec_clauses_eu_law/clauses/eu-mdcg-mdcg-2019-16-rev1.json, tests/test_clause_sets.py, tests/test_pack_discharge.py"
review_set: subset
---

## Summary

Ticket: PLAT-1827. PR agent-ix/spec-clauses-eu-law#22 at head d8b6d5e852e25849049cc2a97590dadd778090c4, diff `origin/main...HEAD` (base 4c159e2). Reviewed the MDR output remapping (I-17.2, I-17.4, I-18.8, II-5), the MDCG output and crosswalk retargeting (2.1, 2.3, 2.6, 3.1-3.8, 4.3, 5.1, 5.2), the catalog subset changes, and the two new tests.

## Verdict

**CHANGES REQUESTED.** The MDR readings are correct. I-17.4 is the manufacturer's statement of minimum hardware, network and IT-security prerequisites. I-18.8 is design protection against unauthorised access. I-17.2 names verification and validation, and II-5 is the risk-management record in the technical file. Every named output has a real producer on origin/main: spec-objects-security threat, risk and control records; `quoin soup report`, which includes OSV advisories; `quoin anomaly`; and the engineering-assurance `release-decision`. `it-requirements-statement` has no producer, and the PR now says so. Both new tests fail on the old mapping and pin no counts or versions.

There is one blocking regression. MDCG 5.2 now expects only `written-procedure`, which makes it the first all-procedure (customer-owned) clause in any EU set. The discharge test's delegated fact has no `owner`, so `quoin evidence record-discharge` rejects it. CI on the head fails on exactly this, and the same test passes on origin/main.

The two crosswalk-test failures seen locally are not caused by this PR (see Coverage).

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | MDCG 5.2 becomes all-procedure, so the discharge test builds a delegated disposition fact without the `owner` field quoin requires. `test_records_facts_and_renders_both_clause_sets` now fails (CI run 45219985479 and locally) and passes on origin/main. | tests/test_pack_discharge.py:381-392, spec_clauses_eu_law/clauses/eu-mdcg-mdcg-2019-16-rev1.json:367-381 |
| FND-002 | medium | The 5.2→I-3 rationale says the toolchain gathers no vulnerability intelligence. That contradicts the 5.1→I-17.2 row, which relies on advisories from `quoin soup report`. It also puts a toolchain-capability claim in a normative crosswalk rationale, which the spec defines as a mapping-scope statement. | spec/spec.md:243, spec_clauses_eu_law/clauses/eu-mdcg-mdcg-2019-16-rev1.json:851, tests/test_clause_sets.py:1113 |
| FND-003 | medium | Section 3.8 reassesses security risk and ships updates. Its I-18.8 row expects only `anomaly-list`, and 3.8's outputs omit `security-risk-records`, the one output that records protection against unauthorised access. | spec/spec.md:235, spec_clauses_eu_law/clauses/eu-mdcg-mdcg-2019-16-rev1.json:280-297 |
| FND-004 | low | The 2.1→I-1 output became `security-risk-records`, but its rationale still describes generic risk-management context and not the security goals that section 2.1 covers. | spec/spec.md:208, spec_clauses_eu_law/clauses/eu-mdcg-mdcg-2019-16-rev1.json:396 |

## Coverage

- Focused tests on the branch: `pytest tests/test_clause_sets.py -k "security_prerequisite or security_sections or catalog or mdr_clause or mdcg_clause"`: 9 passed. Both new tests were run against origin/main data (branch test file on a base checkout), and both fail with the old I-17.4 and MDCG outputs.
- `test_records_facts_and_renders_both_clause_sets`: fails on the branch with `disposition discharge fact is missing owner` (local quoin 0.36.8, and CI with node_modules quoin 0.36.6). It passes on origin/main 4c159e2. quoin v0.36.6 `discharge/parse.rs` requires `owner` on every disposition fact. On origin/main, no EU set has an all-procedure clause; on the branch, MDCG `5.2` is the only one.
- Pre-existing, not caused by this PR: `test_mdcg_crosswalks_match_spec_and_resolve_to_mdr` and `test_ai_act_crosswalks_match_the_annex_table_and_resolve_to_mdr` fail identically on origin/main 4c159e2. `assert_crosswalk_targets_resolve` walks every loaded set, including the GDPR→HIPAA crosswalks. On this machine, `quoin module list` (global quoin 0.36.8) has no `spec_clauses_us_health` module. `_installed_clause_set` returns None, so the target clause list is empty, and the first us-hhs crosswalk (`art-32(1)(a)`→`164.312(a)(2)(iv)`) is reported as a missing clause. That id exists in `us-hhs/45-cfr-164-subpart-c@2026-11-12` at both spec-clauses-us-health origin/main and the CI-pinned ca78ac0. CI installs that module and both tests pass there. PLAT-1824 is unrelated.
- Hard rules: the diff contains no standard text, designators, scores, classes or ticket narration. Nothing is vendored.
- MDCG section topics were judged from the module's own original section summaries. The official PDF could not be fetched (HTTP 429).

## New findings (disposition pass 1)

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-005 | high | The new missing-set message in `assert_crosswalk_targets_resolve` drops the target clause id. FR-014-AC-2 requires both the missing set key and the clause id, so `test_gdpr_article32_missing_nist_set_names_source_and_target` now fails locally and in CI run 45234136495. | tests/conftest.py:200-205 |
| FND-006 | high | Every EU set now uses the US origin/main output descriptions, but CI still checks out spec-clauses-us-health at ca78ac0. Its `verification-records` text differs, so `test_all_declared_sets_share_one_output_catalog` fails in CI run 45234136495. It passes against US origin/main 926c22d. | .github/workflows/ci.yml:24-28, spec_clauses_eu_law/clauses/eu-ai-act-2024-1689-annex-iv-2026-07-27.json:208-210 |

## New findings (disposition pass 2)

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-007 | high | CI now checks out spec-clauses-us-health main, where #35 (merged after round 1) changed the `soup-list` description to name `quoin soup report`. The EU catalog and the MDCG set still carry the old text, so `test_all_declared_sets_share_one_output_catalog` fails in CI run 45241952623. No other shared name drifts. | spec/spec.md:255, spec_clauses_eu_law/clauses/eu-mdcg-mdcg-2019-16-rev1.json:48-50 |

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | The delegated fact now carries `owner`. `test_records_facts_and_renders_both_clause_sets` passes locally (quoin 0.36.8) and is not among the CI failures at 479718c. FR-007 now names the owner field. |
| FND-002 | fixed | The 5.2→I-3 rationale now states mapping scope only, and the test docstring no longer makes the toolchain claim. |
| FND-003 | fixed | The 3.8→I-18.8 row and 3.8 expectedOutputs include security-risk-records, and the FR-005-AC-4 test asserts it. |
| FND-004 | fixed | The 2.1→I-1 rationale now refers to the security goals. |
| FND-005 | fixed | The missing-set message now ends with `{target_key}#{target['clause']}`. `test_gdpr_article32_missing_nist_set_names_source_and_target` passes locally and is not among the CI failures at 566079f. |
| FND-006 | fixed | The CI us-health checkout now uses `ref: main` and the pinned commit is gone. The parity test no longer fails on `verification-records`; its remaining CI failure is the new FND-007. |
