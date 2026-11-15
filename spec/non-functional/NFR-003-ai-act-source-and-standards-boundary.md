---
id: NFR-003
title: "AI Act source and standards boundary"
type: NFR
quality_attribute: compliance
relationships:
  - target: "ix://agent-ix/spec-clauses-eu-law/US-001"
    type: "traces_to"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-016"
    type: "constrains"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-017"
    type: "constrains"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-018"
    type: "constrains"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-019"
    type: "constrains"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-020"
    type: "constrains"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-021"
    type: "constrains"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-022"
    type: "constrains"
---
# NFR-003: AI Act source and standards boundary

## Statement

The pack SHALL publish only original AI Act summaries with the exact EUR-Lex source, attribution and reuse metadata for the consolidated version. The pack SHALL NOT name, number, quote or paraphrase any harmonised or other paywalled standard or standardisation-request deliverable.

## Scope

Applies to the AI Act set metadata, clause summaries, crosswalks, tests, documentation and published package resources.

## Rationale

The AI Act requires technical documentation to record information about standards and solutions, but this clause set names no particular standard. The legal-text reuse statement does not grant reuse rights to a separately published standard.

## Measurement and Evaluation

| Metric | Target | Threshold | Method |
|---|---|---|---|
| Source and rights metadata | Exact source and attribution in `spec.md` | All declared AI Act fields match | Test |
| Standard references | No protected standard identifiers or text | Zero findings in the publishable archive | Test and analysis |
| Original expression | AI Act summaries and crosswalk rationales use original wording | Reviewer finds no copied passage | Analysis |

## Verification

Package metadata tests compare the complete source and rights fields and detect an injected mismatch. The package scan checks the published wheel and npm archive. A reviewer checks authored summaries for copied legal wording and any named or paraphrased paywalled standard.

## Dependencies

Constrains [FR-016](../functional/FR-016-ai-act-sets-declared.md) through [FR-022](../functional/FR-022-ai-act-application-date.md). The exact source and legal-notice URLs are specified in `spec.md` and admitted at their exact archive paths by the engineering-assurance content-rights policy.
