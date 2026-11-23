---
id: SR-20261104139950
title: "Spec review of PLAT-1831 spec-clauses-eu-law PR #28 (catalog producers)"
type: SpecReview
analysis: base
scope: "agent-ix/spec-clauses-eu-law; spec/functional/FR-006-pack-wide-output-catalog.md, spec/spec.md (EU Output Producers) (PR #28 head 2114094)"
review_set: subset
---

## Summary

Ticket: PLAT-1831. This review covers the new FR-006 paragraph, FR-006-AC-4 to AC-6 and the "EU Output Producers" section. They were checked against quoin FR-211, quire-rs FR-073 and the PLAT-1853 decision (option (a): customer-supplied artifacts get a retained kind that packs list in `producers`). `quire validate` passes on both files.

## Verdict

**Changes requested.** The producers table is real contract, not ceremony: it extends the canonical EU catalog that every set must equal, and it pins no count. The issues match the US review. A closed SHALL NOT contradicts PLAT-1853 and cannot be tested, and the statement repeats the table in "today" wording. AC-4 is compound. AC-5 and AC-6 repeat obligations that are already stated. One existing paragraph now sits under the wrong heading.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | The FR-006 statement "A tool-generated document or report and a customer-supplied output SHALL NOT carry `producers`" contradicts the PLAT-1853 decision to give customer artifacts a retained kind that packs list. The "Every other output omits... Omission means" classification also leaves out outputs that are neither kind (system-validation, audit-trail, signed-record), and no test can check it. Delete both, and keep the table as the contract. | spec/functional/FR-006-pack-wide-output-catalog.md:17; spec/spec.md:466 |
| FND-002 | low | FR-006-AC-4 is compound: it covers kind validity and conformance to the table. The statement also repeats the table ("today that is `verification-records`") in time-bound wording. Split the AC, and drop the "today" clause in favour of the table reference. | spec/functional/FR-006-pack-wide-output-catalog.md:17,26 |
| FND-003 | low | FR-006-AC-5 is subsumed once FR-006-AC-3 compares the whole catalog definition, which is what its test already does. FR-006-AC-6 is quire-rs FR-073's contract, already covered by the existing publish-check criteria. Widen AC-3 to the whole definition (kind, description, producers) and delete AC-5 and AC-6. | spec/functional/FR-006-pack-wide-output-catalog.md:25,27-28 |
| FND-004 | low | The new "### EU Output Producers" heading sits between the catalog table and the existing `tests/corpus/` paragraph, so that paragraph now falls under the producers subsection. Move the paragraph above the new heading. | spec/spec.md:458-468 |
