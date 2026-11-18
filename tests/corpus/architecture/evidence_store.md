---
id: example-invalid-evidence_store
title: "EvidenceStore"
object: data_schema
type: data_schema
---
# example-invalid-evidence_store: EvidenceStore

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| record_id | String | 1..1 | identity |
| evidence_uri | String | 1..1 | minLength: 1 |
| sha256 | String | 1..1 | pattern: /^[a-f0-9]{64}$/ |

## Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "EvidenceStore",
  "type": "object",
  "required": ["record_id", "evidence_uri", "sha256"],
  "properties": {
    "record_id": { "type": "string", "minLength": 1 },
    "evidence_uri": { "type": "string", "minLength": 1 },
    "sha256": { "type": "string", "pattern": "^[a-f0-9]{64}$" }
  },
  "additionalProperties": false
}
```
