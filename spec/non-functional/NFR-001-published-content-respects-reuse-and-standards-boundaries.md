---
id: NFR-001
title: "Published content respects reuse and standards boundaries"
type: NFR
quality_attribute: compliance
relationships:
  - target: "ix://agent-ix/spec-clauses-eu-law/US-001"
    type: "traces_to"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-001"
    type: "constrains"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-002"
    type: "constrains"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-003"
    type: "constrains"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-004"
    type: "constrains"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-005"
    type: "constrains"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-006"
    type: "constrains"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-007"
    type: "constrains"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-008"
    type: "constrains"
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
# NFR-001: Published content respects reuse and standards boundaries

## Statement

The pack SHALL publish only original summaries based on identified public EU sources, with truthful attribution and reuse metadata. It SHALL NOT name, number, quote or paraphrase a harmonised or other paywalled standard.

## Scope

Applies to specification, source, tests, examples, package resources and generated distribution files.

## Rationale

EUR-Lex states reuse terms for its legal texts. The cited MDCG PDF says it is not a European Commission document and gives no reuse licence in the document. The module therefore includes only citations and original summaries for MDCG, without asserting Commission reuse terms.

## Measurement and Evaluation

| Metric | Target | Threshold | Method |
|---|---|---|---|
| Rights metadata | Every declared set record meets NFR-001-AC-1 | Not quantitative; binary acceptance is defined by AC-1 | Test and inspection |
| Standard designator scan | The package meets NFR-001-AC-2 | Not quantitative; binary acceptance is defined by AC-2 | Test |
| Original expression | Authored summaries meet NFR-001-AC-3 | Not quantitative; binary acceptance is defined by AC-3 | Analysis |

These measures are binary compliance checks, not performance targets. The
threshold column records the associated pass/fail criterion; no time, rate, or
resource threshold applies.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| NFR-001-AC-1 | Each set's `structure`, `text`, `clearance_ref`, `licence`, `attribution`, and source URL match the source-specific values in `spec.md`; an injected incorrect or missing value is detected and names the set and field. | Test |
| NFR-001-AC-2 | The publishable package contains no name or designator of a harmonised or other paywalled standard; a scan of package files passes and identifies the file and line for an injected fixture. | Test |
| NFR-001-AC-3 | A reviewer finds no copied source passage or paraphrase of a paywalled standard in any published summary. | Analysis |

## Verification

Review source notices and rights fields; scan package files for known designators and verify the scan detects an injected fixture. Human analysis checks that authored summaries do not reproduce protected expression.

## Dependencies

Constrains FR-001 through FR-015. The source-specific rights boundaries are
defined in `spec.md`; each FR specifies the tests and review methods that
enforce them.
