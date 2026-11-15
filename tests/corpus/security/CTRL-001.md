---
id: example.invalid/CTRL-001
title: "EvidenceDigestCheck"
type: control
object: control
---
# CTRL-001: EvidenceDigestCheck

## Effectiveness

`not_assessed`

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| control_id | UUID | 1..1 | identity |
| effectiveness | String | 1..1 | minLength: 1 |
| owner | String | 1..1 | minLength: 1 |

## Invariants

### EvidenceDigestCheckHasAnOwner

```ocl
context EvidenceDigestCheck
inv EvidenceDigestCheckHasAnOwner:
  self.owner->notEmpty()
```
