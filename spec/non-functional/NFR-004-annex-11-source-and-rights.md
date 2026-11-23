---
id: NFR-004
title: "Annex 11 source and rights"
type: NFR
quality_attribute: compliance
relationships:
  - target: "ix://agent-ix/spec-clauses-eu-law/US-001"
    type: "traces_to"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-023"
    type: "constrains"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-024"
    type: "constrains"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-025"
    type: "constrains"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-026"
    type: "constrains"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-027"
    type: "constrains"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-028"
    type: "constrains"
---
# NFR-004: Annex 11 source and rights

## Statement

The module SHALL cite the official European Commission Annex 11 document, state the reuse basis truthfully, and use original clause summaries that reproduce no Annex 11 sentence. It SHALL NOT name, number, quote, or paraphrase-copy a paywalled standard or certification scheme.

## Scope

Applies to Annex 11 source metadata, clause summaries, applicability descriptions, output bindings, crosswalk rationales and test fixtures.

## Rationale

The Commission reuse policy (Decision 2011/833/EU) and the Commission legal notice license Commission content under CC BY 4.0 with attribution, but the Annex 11 document carries no licence statement of its own. The module therefore records citations and original summaries only and states exactly what the reuse basis is.

## Measurement and Evaluation

| Metric | Target | Threshold | Method |
|--------|--------|-----------|--------|
| Annex 11 source and rights fields | Every field matches the contract in `spec.md` | 100% of required fields match | Test and inspection |
| Published expression | Summaries and rationales use original wording and avoid protected standards or schemes | No prohibited reference or copied passage | Analysis and inspection |

These are binary compliance checks, not performance targets.

## Verification

Check the source and rights fields, scan package content for prohibited references, and have a reviewer analyze that summaries and rationales use original expression.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| NFR-004-AC-1 | The set's source URL, identity, licence, attribution and indication of changes match `spec.md`, and the licence text says the Annex 11 document has no licence statement of its own. | Test |
| NFR-004-AC-2 | Published Annex 11 summaries and crosswalk rationales contain no copied Annex passage and no name or designator of a paywalled standard or certification scheme. | Analysis |

## Dependencies

Constrains the Annex 11 set. The source-specific values are defined in `spec.md`.
