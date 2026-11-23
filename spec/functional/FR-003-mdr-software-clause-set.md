---
id: FR-003
title: "MDR software clause set"
type: FR
relationships:
  - target: "ix://agent-ix/spec-clauses-eu-law/US-001"
    type: "traces_to"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-001"
    type: "depends_on"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-002"
    type: "depends_on"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-006"
    type: "depends_on"
---
# FR-003: MDR software clause set

## Description

The MDR set SHALL use the source, key, version, clause IDs, mandatory force, applicability and expected outputs in the normative MDR table in `spec.md`. Each clause SHALL contain original nonempty summary text. The table is exhaustive for this M1 set.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-003-AC-1 | IDs equal the MDR table exactly, including punctuation and no extra clauses. | Test |
| FR-003-AC-2 | Every clause is mandatory, has original nonempty text and at least one catalog output; set validation succeeds. | Test |
| FR-003-AC-3 | A clause referencing an output missing from its catalog fails validation and names the clause. | Test |
| FR-003-AC-4 | Clause `I-14.2(d)` expects `it-requirements-statement` and `security-risk-records`; `I-17.2` also expects `verification-records`; `II-5` also expects `risk-management-records`. Clause `I-17.4` expects `it-requirements-statement` and `security-risk-records`, and `I-18.8` expects `security-risk-records` and `verification-records`; neither expects `release-record`, `anomaly-list`, or `soup-list`. `it-requirements-statement` is described as customer-supplied with no toolchain producer. | Test |

## Dependencies

Depends on FR-001 for the module home, FR-002 for source rights, and FR-006 for expected-output definitions. Quire owns generic clause-set schema validation; the EU pack owns the exhaustive ID, original-summary, and catalog-reference assertions. If `quire validate` or its clause-set capability is unavailable, the criterion fails with the missing executable or capability and is not skipped.
