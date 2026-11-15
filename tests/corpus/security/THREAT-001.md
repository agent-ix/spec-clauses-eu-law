---
id: example.invalid/THREAT-001
title: "EvidenceReferenceSubstitution"
type: threat
object: threat
stride_category: Tampering
vector: "An attacker replaces a stored evidence reference with another record."
---
# THREAT-001: EvidenceReferenceSubstitution

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| threat_id | UUID | 1..1 | identity |
| stride_category | String | 1..1 | minLength: 1 |
| vector | String | 1..1 | minLength: 1 |
