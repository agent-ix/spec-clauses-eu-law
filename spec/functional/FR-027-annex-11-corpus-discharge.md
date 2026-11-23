---
id: FR-027
title: "Annex 11 corpus discharge"
type: FR
relationships:
  - target: "ix://agent-ix/spec-clauses-eu-law/US-001"
    type: "traces_to"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-024"
    type: "depends_on"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-025"
    type: "depends_on"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-007"
    type: "depends_on"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-008"
    type: "depends_on"
---
# FR-027: Annex 11 corpus discharge

## Description

Pack discharge tests SHALL evaluate the Annex 11 set against the synthetic corpus in `tests/corpus/`.

The tests SHALL write facts to a temporary store.

Clauses whose outputs are all procedures (`2`, `3.1`, `3.2`, `3.4`, `4.5`, `7.2`, `11`, `15`, `16`, `17`) SHALL accept only a delegated disposition with a rationale and a customer approval reference.

The pack SHALL NOT render an aggregate score, percentage or overall determination.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-027-AC-1 | Evaluation with every dimension set to `yes` and `quoin discharge --rmm` over the corpus partitions every Annex 11 clause into direct evidence, disposition or open work with none lost. | Test |
| FR-027-AC-2 | A direct fact on each all-procedure clause is rejected; a delegated disposition with rationale and customer approval reference succeeds. | Test |
| FR-027-AC-3 | A clause with a `no` dimension value appears as not binding, and a clause with an unset value appears as unresolved; neither is counted as discharged. | Test |
| FR-027-AC-4 | The rendered RMM contains no aggregate score, percentage or overall compliance determination; its per-clause status column reflects only that clause's recorded discharge state. | Test |
| FR-027-AC-5 | Corpus identifiers use the `example.invalid` authority and `example-invalid-` prefix, and discharge facts are removed with the temporary store. | Test |

## Dependencies

Corpus rules are defined in [FR-008](./FR-008-reference-corpus.md); customer-owned handling in [FR-007](./FR-007-customer-owned-obligations.md). If `quire` or `quoin` lacks the needed capability the gate fails naming it.
