---
id: FR-021
title: "AI Act to MDR crosswalks"
type: FR
relationships:
  - target: "ix://agent-ix/spec-clauses-eu-law/US-001"
    type: "traces_to"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-018"
    type: "depends_on"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-003"
    type: "depends_on"
---
# FR-021: AI Act to MDR crosswalks

## Description

Every Annex IV point SHALL have at least one crosswalk to a resolving MDR Annex II clause, or an explicit `none` entry in the table where no direct counterpart is asserted. The provider set's article crosswalks (`art-9`, `art-15`) SHALL target resolving MDR Annex I clauses. Each crosswalk SHALL state a relation and original rationale. The relation `equivalent` SHALL NOT be used.

## Acceptance Criteria

| ID | Criteria | Verification |
|---|---|---|
| FR-021-AC-1 | Every Annex IV table row has one or more resolving MDR Annex II targets or the explicit `none` value; no row has an omitted target. | Test |
| FR-021-AC-2 | Every declared target resolves in the loaded MDR set, has relation `partial` or `informative`, and includes a nonempty rationale. | Test |
| FR-021-AC-3 | An injected unknown target, `equivalent` relation, or empty rationale fails and names its source clause and field. | Test |
| FR-021-AC-4 | The `art-15` crosswalks to `I-17.2`, `I-17.4` and `I-18.8` describe those MDR clauses by what they cover: `I-17.2` software lifecycle controls including information-security risk management and verification, `I-17.4` the hardware, network and IT-security prerequisites the manufacturer states, and `I-18.8` protection against unauthorised access. | Test |

## Dependencies

Depends on the Annex IV table in [FR-018](./FR-018-ai-act-annex-iv.md) and the MDR set in [FR-003](./FR-003-mdr-software-clause-set.md). Both clause sets are loaded as test dependencies; target content is not copied.
