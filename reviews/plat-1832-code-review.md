---
id: SR-024
title: "Code review — Annex 11 clause set, tests and corpus discharge"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-clauses-eu-law; PR #21 git diff origin/main...HEAD at 645527d4: tests/test_annex11.py, tests/annex11_spec.py, tests/test_clause_sets.py, spec_clauses_eu_law/manifest.yaml, spec_clauses_eu_law/clauses/eu-eu-gmp-annex-11-2011-01.json, spec FR-001, FR-023..FR-028, NFR-004"
review_set: subset
date: 2026-11-23
---

## Summary

Ticket: PLAT-1832. Reviewed `git diff origin/main...HEAD` at 645527d4e838b4b46c25192ec45b043a1680dba4 of agent-ix/spec-clauses-eu-law PR #21. Method: code-review.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | The rejection half of FR-027-AC-2 is asserted only against the test-local helper `_assert_customer_owned_facts` (tests/test_pack_discharge.py:176-194), not against the pack or quoin. | tests/test_annex11.py:564-576 |
| FND-002 | medium | FR-028 says the ten clauses discharge 'only with a person-named approvalRef'. | spec/functional/FR-028-annex-11-human-decisions.md:17,23 |
| FND-003 | medium | The test tagged FR-028-AC-2 covers only a missing approvalRef. | tests/test_annex11.py:611-640 |
| FND-004 | low | `_assert_tool_limits` checks `sentence in clause['text']`. The AC requires the clause to end its text with the sentence, and spec.md requires each distinct sentence exactly once. | tests/test_annex11.py:89-97 |
| FND-005 | low | The corpus test is tagged FR-027-AC-5. It checks the `example.invalid` authority of evidence refs (via `_assert_fact_refs_resolve`), but not the `example-invalid-` identifier prefix or that discharge facts are removed with the temporary store. | tests/test_annex11.py:539 |
| FND-006 | low | `expected_metadata()` hard-codes `SET_KEY` and `OFFICIAL_URL` instead of reading them from spec.md, so the 'matches spec.md' check for the identity and source URL compares the JSON with test constants. | tests/annex11_spec.py:9-14,104-125 |

## Finding details

### FND-001 — FR-027-AC-2

The rejection half of FR-027-AC-2 is asserted only against the test-local helper `_assert_customer_owned_facts` (tests/test_pack_discharge.py:176-194), not against the pack or quoin. Measured: recording a direct fact on customer-owned clause `2` through `quoin evidence record-discharge`, then `quoin discharge --rmm --pack` (quoin 0.36.8), gives `compliance: compliant`. quoin origin/main 42fd3658 has no customer-owned check; FR-211's `customer-owned` reason is spec-only. The test passes while the product does the opposite of the AC.

Expected fix: Run the rejection case through quoin, as the corpus test does. Until quoin FR-211 lands, say in FR-027 that quoin owns the rejection and mark the AC blocked on it rather than claiming it with a helper. The same pattern sits under FR-007-AC-2 on main.

### FND-002 — FR-028-AC-1

FR-028 says the ten clauses discharge 'only with a person-named approvalRef'. quoin origin/main (FR-208, quoin-quire clauses.rs:156,216) only checks that approvalRef is non-blank. Measured: a direct fact on clause `9` with `approvalRef: "x"` renders `compliant`. Quoin FR-211 (spec-only on origin/main) will instead require a signed annotated tag that engineering-assurance `approval-verify` accepts, with a `meaning` equal to one of the clause's `approvalRoles`. The shipped role `system-owner` is not named anywhere in the spec. Moving from 'delegated disposition only' to 'direct fact with approvalRef on an approval-class clause' is the right model and matches FR-208/FR-211. But 'person-named' is a property nothing checks, and the fixture `person://example.invalid/people/system-owner` will stop discharging once FR-211 ships.

Expected fix: State the contract as quoin's: an approval-class clause declares approvalRoles [`system-owner`] (name the role in spec.md and say why it is that role), and quoin decides discharge per FR-208 today and FR-211 once it lands. Drop 'person-named' unless something enforces it.

### FND-003 — FR-028-AC-2

The test tagged FR-028-AC-2 covers only a missing approvalRef. Neither the blank case nor the unresolved case is exercised. The AC also says the clause is left 'unresolved', but the engine and the test give `compliance: undischarged` with applicability `applicable`. 'Unresolved' is the applicability state, so the AC names the wrong state.

Expected fix: Change 'unresolved' to 'undischarged' in FR-028-AC-2. Add the blank-string case. For 'unresolved approvalRef', either define it (an FR-211 verification failure) or drop it until FR-211 lands.

### FND-004 — FR-025-AC-6

`_assert_tool_limits` checks `sentence in clause['text']`. The AC requires the clause to end its text with the sentence, and spec.md requires each distinct sentence exactly once. A sentence placed mid-text or duplicated passes.

Expected fix: Assert that the text after the summary is exactly the set of required 'Tool limit:' sentences, each once.

### FND-005 — FR-027-AC-5

The corpus test is tagged FR-027-AC-5. It checks the `example.invalid` authority of evidence refs (via `_assert_fact_refs_resolve`), but not the `example-invalid-` identifier prefix or that discharge facts are removed with the temporary store.

Expected fix: Assert both, or drop the FR-027-AC-5 tag and say it is covered by FR-008's corpus tests.

### FND-006 — FR-023-AC-3

`expected_metadata()` hard-codes `SET_KEY` and `OFFICIAL_URL` instead of reading them from spec.md, so the 'matches spec.md' check for the identity and source URL compares the JSON with test constants. A spec edit to the URL would not fail the test.

Expected fix: Parse the identity and official URL from the Annex 11 Set Design section, as the licence and attribution already are.

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
- tests/annex11_spec.py (examined)
- tests/test_annex11.py (examined)
- spec_clauses_eu_law/clauses/eu-eu-gmp-annex-11-2011-01.json (examined)

## Verdict

Not mergeable: one high and two medium findings. Sound: `pytest tests/test_annex11.py tests/test_clause_sets.py tests/test_pack_discharge.py` gives 81 passed, with spec-clauses-us-health origin/main 64f95e4 installed as a module and removed afterwards. The catalog-parity tests now pass, so SR-016 FND-006 is resolved. The JSON has the 34 clauses of the spec table. The spec-table readers cannot pass vacuously: an empty clause, bindings, tool-limit or crosswalk table fails a set-equality or `>=` assertion elsewhere. Clause text and crosswalk rationales are original. Compared with the official 2011 PDF, the longest shared word run is 7 words, a noun list ('patient safety, data integrity and product quality'), and no sentence is copied. No tool assigns a score, class or criticality, and the RMM test checks that no score, percentage or overall key appears. Every producer command answers --help. FR-025-AC-5 (Inspection) has no test: by inspection, no Annex 11 clause text, binding or limit claims a tool verdict.
