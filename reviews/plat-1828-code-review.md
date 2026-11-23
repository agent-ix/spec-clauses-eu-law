---
id: SR-026
title: "Code review — AI Act and Annex IV output and crosswalk audit"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-clauses-eu-law; spec/spec.md, spec_clauses_eu_law/clauses/eu-ai-act-2024-1689-2026-07-27.json, spec_clauses_eu_law/clauses/eu-ai-act-2024-1689-annex-iv-2026-07-27.json, tests/test_clause_sets.py"
review_set: subset
---

## Summary

Ticket: PLAT-1828. PR agent-ix/spec-clauses-eu-law#23 at head 082a7ee32e8b5e7f6c785035a14e8400da182867, diff `origin/main...HEAD`. Reviewed the six customer-supplied catalog descriptions, the art-73 output change and its customer-owned inventory row, the art-15 and Annex IV crosswalk rationale rewrites, the removed IV-9 crosswalk, and the two new tests.

## Verdict

**CHANGES REQUESTED (one medium).** Every producer claim is real. On quoin origin/main and the installed quoin 0.36.8, `quoin release snapshot`, `quoin risk-summary`, `quoin matrix`, `quoin evidence record` and `quoin anomaly report` exist. engineering-assurance origin/main has the `approval-trail` capability (`src/approval_trail_host.rs`). The spec-objects modules named in the catalog are installed. No quoin, quire or engineering-assurance origin/main source produces data lineage, an oversight design, a logging design, a post-market plan, a model description or a declaration of conformity. The quoin dossier kinds are srs, architecture, risk-management, risk-management-plan, threat-model, trace-matrix, verification-report, release-record, soup, anomalies, rmm and records-of-processing. So the six customer-supplied labels are honest. The tool still assigns no AI Act class, score or acceptability. The art-9 and art-14 person-named approval rule (FR-020) is untouched.

Moving art-73 to written-procedure only is correct. `quoin anomaly report` lists unresolved software anomalies. It is not a record of serious incidents or of reporting them to authorities. The clause is now all-procedure, and the customer-owned inventory row it needs is added. `tests/test_pack_discharge.py` passes with it.

The crosswalk rewrites match this repo's own MDR summaries and are in original wording: I-17.2 is lifecycle controls with information-security risk management and V&V; I-17.4 is the stated hardware, network and security prerequisites; I-18.8 is protection against unauthorised access; II-4 is the requirements-compliance record; II-1.1 is the device and software-component description. IV-9 → `none` is right because Annex II has no post-market content.

The remaining defect is art-20 (FND-001). One low wording point (FND-002) is optional.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | art-20 still expects `release-record`. A release snapshot cannot show that a release was a corrective action for a non-conformity. It also cannot show a withdrawal, disablement or recall, or that the provider told deployers and authorities, which are what the clause summary requires. It is the same case as the `anomaly-list` this PR removes from art-73. Fix: art-20 expects `written-procedure` only, add `ai-act-2024-1689 / art-20` to the Customer-Owned Obligations inventory, and extend FR-017-AC-5 and its test with `outputs["art-20"] == {"written-procedure"}`. | spec/spec.md:144, spec_clauses_eu_law/clauses/eu-ai-act-2024-1689-2026-07-27.json:455-458, spec/spec.md:287-290 |
| FND-002 | low | The new art-15→I-17.4 rationale links the stated operating prerequisites only to "operating conditions". It leaves out that I-17.4's prerequisites include the IT-security measures needed to run the software, which is the clause's most direct overlap with Article 15 cybersecurity. Suggested: "The minimum hardware, network and IT-security prerequisites the manufacturer states bound the conditions the AI system operates in, without covering the accuracy, robustness or cybersecurity evaluation itself." | spec_clauses_eu_law/clauses/eu-ai-act-2024-1689-2026-07-27.json:660 |

## Coverage

- Focused tests on the branch, with `spec_clauses_us_health` installed from a temporary copy of spec-clauses-us-health origin/main: `pytest tests/test_clause_sets.py -k "customer_supplied or art_15 or customer_owned or share_one_output_catalog or crosswalk or ai_act"` gave 21 passed, and `tests/test_pack_discharge.py` gave 15 passed. The FR-006-AC-3 parity test passes, and none of the six re-described names exist in the US catalog.
- Fail-on-old-data: the branch tests were run in a temporary copy with origin/main `spec.md` and both AI Act JSON files. `test_ai_act_outputs_without_a_producer_are_marked_customer_supplied` and `test_ai_act_art_15_crosswalks_describe_the_mdr_clauses_they_target` both fail. Neither pins a count or a version.
- Hard rules: the diff has no standard text or designators and no ticket narration in prose, JSON or test docstrings. Nothing is vendored: the US catalog is read from the installed module.
- Concurrent PR #21 also edits spec.md. That is a rebase concern, not a finding.
