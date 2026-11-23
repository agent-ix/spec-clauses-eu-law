---
id: SR-028
title: "Spec review — AI Act and Annex IV output and crosswalk audit"
type: SpecReview
analysis: base
scope: "agent-ix/spec-clauses-eu-law; spec/spec.md, spec/functional/FR-017-ai-act-high-risk-obligations.md, spec/functional/FR-021-ai-act-mdr-crosswalks.md"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-017"
    type: reviews
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-021"
    type: reviews
---

## Summary

Ticket: PLAT-1828. PR agent-ix/spec-clauses-eu-law#23 at head 082a7ee32e8b5e7f6c785035a14e8400da182867. This spec review covers the spec edits: the AI Act obligations table row for art-73, the Annex IV table rows IV-1(f), IV-2(h) and IV-9, the six EU catalog descriptions, the customer-owned inventory row, FR-017-AC-5 and FR-021-AC-4. `quire validate` with spec-artifacts-iso passes on the three edited files.

## Verdict

**CHANGES REQUESTED (one medium).** The table and catalog edits are consistent with each other and with the JSON. FR-021-AC-4 constrains the provider set's art-15 crosswalks to MDR Annex I clauses. FR-021's title and SHALL statement cover only Annex IV → MDR Annex II crosswalks, and spec.md has no table for article-level crosswalks. So the AC requires something its FR does not state. Both new ACs also bundle two unrelated checks.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | FR-021-AC-4 exceeds its FR. The FR statement and title cover Annex IV points mapped to MDR Annex II, while the art-15 crosswalks are article-level and target Annex I (I-17.2, I-17.4, I-18.8). Fix: extend FR-021's statement and title to cover the provider set's article crosswalks to MDR Annex I, with the same relation and rationale rules. | spec/functional/FR-021-ai-act-mdr-crosswalks.md:13-17, spec/functional/FR-021-ai-act-mdr-crosswalks.md:26 |
| FND-002 | low | Compound ACs. FR-017-AC-5 joins the catalog-description rule with the art-73 output rule. FR-021-AC-4 joins the art-15 rationales with IV-9 → none, which the Annex IV table under AC-1 already covers. Split them, or drop the IV-9 half of AC-4. | spec/functional/FR-017-ai-act-high-risk-obligations.md:27, spec/functional/FR-021-ai-act-mdr-crosswalks.md:26 |

## Coverage

- `quire validate --scope . --module ~/.ix/filament/modules/spec-artifacts-iso` on spec/spec.md, FR-017 and FR-021: exit 0.
- Checked the IV-9 `none` row against the section 155 prose ("`none` records that no direct Annex II counterpart is asserted"): consistent.
- Checked the art-73 inventory row against the FR-007 "exhaustive" rule and the data: consistent.
- No paywalled standard text and no ticket narration in the spec edits.
