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

## Dispositions

Disposition pass 1, head cba6ffb91b6170f5a192ead07d3670e38239e157, fix commits 96e9d2f and cba6ffb.

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | FR-021 is retitled "AI Act to MDR crosswalks", and its statement now covers the provider set's article crosswalks. That statement's Annex I wording is wrong for art-9 (see FND-003). |
| FND-002 | fixed | The art-20 and art-73 output rule moved to FR-017-AC-6. The IV-9 half of FR-021-AC-4 is dropped, and IV-9 → none stays covered by the FR-021-AC-1 table-equality test: restoring the old IV-9 crosswalk fails it. |

## New findings (disposition pass 1)

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-003 | high | The new FR-021 sentence "The provider set's article crosswalks (`art-9`, `art-15`) SHALL target resolving MDR Annex I clauses" is false for the data: `art-9` → `II-5` targets Annex II. No test checks which annex is targeted, so this passes unnoticed. Fix: "SHALL target resolving MDR Annex I or Annex II clauses", or drop the annex qualifier. | spec/functional/FR-021-ai-act-mdr-crosswalks.md:17, spec_clauses_eu_law/clauses/eu-ai-act-2024-1689-2026-07-27.json (art-9 → II-5) |

Coverage for this pass: `quire validate` with spec-artifacts-iso passes on spec.md, FR-017 and FR-021 (exit 0). Full `spec/**/*.md` validation exits 0; its only warnings are EARS warnings on FR-024, FR-027 and FR-028, which came from PR #21, not this PR. The rebase merge of spec.md is clean. The catalog keeps the six customer-supplied AI rows next to the Annex 11 supplier rows, and the inventory lists art-20, art-73, MDCG 5.2 and the Annex 11 rows with no duplicates.
