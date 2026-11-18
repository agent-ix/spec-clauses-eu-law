---
id: example-invalid-RISK-002
title: "EvidenceIntegrityLoss"
type: risk
object: risk
likelihood: unlikely
impact: moderate
decision: undecided
---
# example-invalid-RISK-002: EvidenceIntegrityLoss

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| risk_id | UUID | 1..1 | identity |
| likelihood | String | 1..1 | minLength: 1 |
| impact | String | 1..1 | minLength: 1 |
