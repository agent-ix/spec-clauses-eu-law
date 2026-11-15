---
id: example-invalid-SOUP-001
title: "ExampleDigestLibrary"
type: soup_record
object: soup_record
purl: "pkg:cargo/example-digest-library@1.0.0"
---
# example-invalid-SOUP-001: ExampleDigestLibrary

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| component_id | UUID | 1..1 | identity |
| purl | String | 1..1 | minLength: 1 |
| supplier | String | 0..1 | |
