---
id: example.invalid/RISK-001
title: "EvidenceReviewDelay"
type: risk
object: risk
likelihood: possible
impact: minor
---
# RISK-001: EvidenceReviewDelay

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| risk_id | UUID | 1..1 | identity |
| likelihood | String | 1..1 | minLength: 1 |
| impact | String | 1..1 | minLength: 1 |
