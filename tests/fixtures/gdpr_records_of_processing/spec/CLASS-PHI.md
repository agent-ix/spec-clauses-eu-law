---
id: CLASS-PHI
title: Synthetic health data
type: data_classification
object: data_classification
regulated_categories:
  - health
---
# CLASS-PHI: Synthetic health data

## Handling

Synthetic test data is encrypted at rest and in transit.

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| classification_id | UUID | 1..1 | identity |
| level | String | 1..1 | minLength: 1 |
