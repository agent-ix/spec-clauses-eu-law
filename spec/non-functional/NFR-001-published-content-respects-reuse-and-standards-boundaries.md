---
id: NFR-001
title: "Published content respects reuse and standards boundaries"
type: NFR
quality_attribute: compliance
---
# NFR-001: Published content respects reuse and standards boundaries

## Statement

The pack SHALL publish only original summaries based on identified public EU sources, with truthful attribution and reuse metadata. It SHALL NOT name, number, quote or paraphrase a harmonised or other paywalled standard.

## Scope

Applies to specification, source, tests, examples, package resources and generated distribution files.

## Rationale

EUR-Lex and Commission sources have stated reuse terms, while referenced standards may have separate rights.

## Measurement and Evaluation

| Metric | Target | Threshold | Method |
|---|---|---|---|
| Rights metadata | Both sets record exact licence, attribution and source URL | Any missing or inconsistent field fails review | Inspection |
| Standard designator scan | No paywalled-standard designator or text in package | Scan passes on package and identifies file/line for injected fixture | Test |
| Original expression | No source text or paraphrase of paywalled standards | Any identified occurrence blocks publication | Analysis |

## Verification

Review source notices and rights fields; scan package files for known designators and verify the scan detects an injected fixture. Human analysis checks that authored summaries do not reproduce protected expression.
