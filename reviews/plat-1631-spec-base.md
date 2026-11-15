---
id: SR-009
title: "Base spec review — AI Act obligations and Annex IV"
type: SpecReview
analysis: base
scope: "agent-ix/spec-clauses-eu-law; spec/spec.md and spec/functional/FR-001, FR-006, FR-016–FR-022, spec/non-functional/NFR-003"
review_set: subset
---

## Summary

The specification uses the correct EUR-Lex consolidation and application date, supplies the complete 23-point Annex IV table, resolves each nonempty MDR target, and states original summaries and source-specific reuse terms. The current draft has two legal-scope errors: it makes all Annex IV elements unconditional and assigns Article 49 registration to Annex I systems. It also specifies an invalid Quire validation command. These issues must be corrected before implementation.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | Article 49 registration is incorrectly assigned to all Annex I provider systems | spec/spec.md:148; FR-017; FR-019 |
| FND-002 | high | Annex IV applicability qualifiers are lost and all 23 points are made unconditional | spec/spec.md:156; FR-018-AC-2 |
| FND-003 | medium | FR-016 requires a Quire command that exits 3 because it omits the required document/glob argument | FR-016-AC-4; FR-001-AC-1 |

## Review scope

Examined complete AI Act and Annex IV tables, the source/date and rights statement, applicability and human-decision FRs, all AI Act acceptance criteria, output catalog additions, NFR-003, the edited FR-001 and FR-006, and crosswalk target IDs. The 23 Annex IV IDs cover section 1(a)-(h), section 2(a)-(h), and points 3–9. MDR targets `II-1.1`, `II-6.1(b)`, `II-4`, and `II-5` all resolve in the selected MDR file. The EUR-Lex 2026-07-27 consolidated text reflects Regulation (EU) 2026/1744 and its Article 113(c)(ii) date of 2 August 2028. EUR-Lex legal-notice terms match the stated CC BY 4.0 attribution/change notice. New criteria remain untagged in the computed matrix because their implementation tests are downstream tickets; this is expected for this spec-only change and is recorded as a baseline, not a spec blocker.

## Findings details

### FND-001 — Article 49 registration is incorrectly assigned to Annex I providers

The set is specifically scoped to Article 6(1)/Annex I systems, but the normative table makes `art-49` mandatory for every provider. Article 49(1) is limited to systems listed in Annex III; Article 49(2) concerns a provider's conclusion that an Annex III system is not high-risk under Article 6(3). Neither is an obligation for this Annex I-only set. This creates a false required record and makes FR-019-AC-2 bind it for all provider contexts. Source: EUR-Lex Article 49, https://eur-lex.europa.eu/eli/reg/2024/1689/2026-07-27/eng.

### FND-002 — Annex IV elements are treated as unconditionally mandatory

The normative introduction says every Annex IV point is mandatory and FR-018-AC-2 requires that force/applicability match the table. The consolidated Annex IV introduction limits its elements to those “as applicable to the relevant AI system”; individual points also carry `where applicable` / `where relevant` conditions. The current tables have no per-point applicability or qualification, so the set marks some conditional documentation as always binding. Preserve those source conditions in the selected clauses and acceptance criteria. Source: EUR-Lex Annex IV, https://eur-lex.europa.eu/eli/reg/2024/1689/2026-07-27/eng.

### FND-003 — Invalid validation command

`FR-016-AC-4` requires `quire validate --module <pkg>` without the positional Markdown document/glob required by Quire 0.45.0. Running the specified form returned exit 3 with “the following required arguments were not provided: <DOC_OR_GLOB>”. The edited `FR-001-AC-1` retains the same invalid invocation. State a supported doc-validation invocation with its document/glob, alongside `publish-check`.

## Dispositions

| FND | outcome | reason |
|---|---|---|
| FND-001 | fixed | The high-risk obligations table and FR-017 now exclude Article 49; FR-017 explains its Annex III / Article 6(3) scope. |
| FND-002 | fixed | Annex IV points now use per-point person-supplied applicability flags and preserve the introductory and point-specific conditions. |
| FND-003 | fixed | FR-016-AC-4 and FR-001-AC-1 now specify Quire validation with the required Markdown glob. |
| FND-003 | fixed | Final AC wording includes both the ISO schema module and process module roots required to validate the spec bundle; the exact command succeeds at e85c59b. |
