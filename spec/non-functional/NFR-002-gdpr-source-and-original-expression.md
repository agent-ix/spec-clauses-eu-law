---
id: NFR-002
title: "GDPR source and original expression"
type: NFR
quality_attribute: compliance
relationships:
  - target: "ix://agent-ix/spec-clauses-eu-law/US-001"
    type: "traces_to"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-009"
    type: "constrains"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-010"
    type: "constrains"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-011"
    type: "constrains"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-012"
    type: "constrains"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-013"
    type: "constrains"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-014"
    type: "constrains"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-015"
    type: "constrains"
---
# NFR-002: GDPR source and original expression

## Statement

The module SHALL cite the official EUR-Lex GDPR source and use original clause
summaries with truthful source attribution. It SHALL NOT name, number, quote, or
paraphrase-copy a paywalled standard or certification scheme.

## Scope

Applies to GDPR source metadata, clause summaries, applicability descriptions,
crosswalk rationales, test fixtures, and the security-analysis skill references
that describe coverage of this set.

## Rationale

EUR-Lex permits reuse of legal documents unless otherwise specified and licenses
its consolidated texts under CC BY 4.0. The module can provide concise original
summaries and citations while clearly recording attribution and changes.

## Measurement and Evaluation

| Metric | Target | Threshold | Method |
|--------|--------|-----------|--------|
| GDPR source and rights fields | Every GDPR record matches the source and rights contract in `spec.md` | 100% of required fields match | Test and inspection |
| Published expression | Summaries and rationales use original wording and avoid protected standards or schemes | No prohibited reference or copied passage | Analysis and inspection |

These are binary compliance checks, not performance targets.

## Verification

Check the source notice and rights fields, scan package content for prohibited
references, and have a reviewer analyze that the summaries and rationales use
original expression.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| NFR-002-AC-1 | The GDPR set's source URL, source identity, licence, attribution, and indication of changes match the values in `spec.md`. | Test |
| NFR-002-AC-2 | Published GDPR summaries and crosswalk rationales contain no copied EUR-Lex passage and no name or designator of a paywalled standard or certification scheme. | Analysis |

## Dependencies

Constrains the GDPR set and its dependent skill references. The source-specific values are defined in `spec.md`.
