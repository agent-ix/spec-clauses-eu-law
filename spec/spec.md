---
type: master-requirements
name: spec-clauses-eu-law
org: agent-ix
component_type: clause-set-module
implementation_language: markdown
tags:
  - eu-law
  - clause-sets
  - mdr
  - medical-device-cybersecurity
security_critical: false
---
# Master Requirements Specification

## Purpose

This specification defines the clause-only EU-law module and its first two sets: software-related requirements from Regulation (EU) 2017/745 (MDR), and interpretive cybersecurity guidance from MDCG 2019-16 rev.1. Clause summaries will be original expression and linked to official sources. The pack records evidence and produces an RMM; it does not determine legal compliance.

## Scope

### In Scope

- Repository `agent-ix/spec-clauses-eu-law`, Python package `spec_clauses_eu_law`, module `clause_sets`.
- MDR set `eu/mdr-2017-745@2026-07-19` and MDCG set `eu-mdcg/mdcg-2019-16@rev1`.
- Set identities, sources, rights metadata, clause identifiers, applicability, expected outputs, MDCG-to-MDR crosswalks, shared output catalog, customer-owned obligations, and synthetic reference corpus rules.

### Out of Scope

- Clause JSON/content, package manifest, corpus, implementation tests, CI, publish gate, output bindings, and scaffold beyond this specification (PLAT-1425, PLAT-1623, PLAT-1624, PLAT-1626).
- GDPR and AI Act sets; engine changes; legal advice or compliance determinations.
- Any source text or expression from harmonised or other paywalled standards.

## System Overview

The module manifest lists each set with module-relative paths, declares no object types, archetypes or edges, and installs as a clause-only module. The sets use existing clause validation, evaluation, publication and discharge commands.

## Set Design

MDR identity is authority `eu`, ID `mdr-2017-745`, and version `2026-07-19`, the EUR-Lex consolidated-text date consulted. A later consolidation is a new version. Its official URL is `https://eur-lex.europa.eu/eli/reg/2017/745/2026-07-19/eng` (EUR-Lex ELI). Set rights are `structure: citation_only`, `text: original`, `clearance_ref: null`. Licence metadata shall say: `EUR-Lex legal documents may be reused for commercial or non-commercial purposes unless otherwise specified. Consolidated texts are CC BY 4.0; acknowledge the source and indicate changes.` Attribution metadata shall say `© European Union. Source: <official URL>. Changes made.` Source: EUR-Lex legal notice `https://eur-lex.europa.eu/content/legal-notice/legal-notice.html?locale=en`.

MDCG identity is authority `eu-mdcg`, ID `mdcg-2019-16`, version `rev1`, with source `https://health.ec.europa.eu/medical-devices-sector/new-regulations/guidance-mdcg-endorsed-documents-and-other-guidance_en` and official PDF linked there. Its rights are `citation_only`, `original`, null clearance; licence is `Commission document reuse policy under Decision 2011/833/EU, subject to source-specific notices and third-party rights`. Attribution is `© European Union. Source: <official PDF URL>. Changes made.` The guidance is non-binding; clauses are `recommended`. MDR clauses are `mandatory`.

Clause IDs are `<annex roman>-<section>` with subparagraphs in parentheses, e.g. `I-17.3`, `I-23.4(ab)`, `II-6.1(b)`. MDCG IDs are section identifiers without a prefix, e.g. `3.2`. IDs contain no slash. `mobile_platform` has values `yes` and `no`; only `I-17.3` uses it (`eq mobile_platform yes`). Other MDR clauses always bind. Device class is not a dimension because no in-scope clause depends on it.

## MDR Clause Table

The table is normative for IDs, applicability and outputs. All outputs resolve in the catalog below. All clauses are mandatory.

| Clause ID | Applicability | Expected outputs |
|---|---|---|
| I-1 | always | risk-management-records |
| I-2 | always | risk-management-records |
| I-3 | always | risk-management-records |
| I-4 | always | risk-management-records |
| I-5 | always | risk-management-records |
| I-8 | always | risk-management-records |
| I-14.2(d) | always | it-requirements-statement |
| I-17.1 | always | software-requirements, software-architecture, verification-records |
| I-17.2 | always | software-requirements, software-architecture, security-risk-records |
| I-17.3 | eq mobile_platform yes | software-requirements, software-architecture, verification-records |
| I-17.4 | always | soup-list, anomaly-list, risk-management-records |
| I-18.8 | always | release-record, verification-records, anomaly-list |
| I-23.4(ab) | always | it-requirements-statement |
| II-1.1 | always | software-requirements, software-architecture |
| II-4 | always | software-requirements, software-architecture, verification-records |
| II-5 | always | software-requirements, verification-records, security-risk-records |
| II-6.1(b) | always | software-architecture, verification-records |

## MDCG Companion Table

Each guidance section is recommended and has at least one informative or partial crosswalk to an MDR clause. Targets resolve against the loaded MDR set. Crosswalk rationale is authored by this pack; the table identifies the mapping boundary and does not restate guidance text.

| MDCG ID | MDR crosswalk targets | Expected outputs |
|---|---|---|
| 2.1 | I-1, I-3 | risk-management-records |
| 2.2 | I-17.2 | security-risk-records |
| 2.3 | I-17.2, I-17.4 | security-risk-records, anomaly-list |
| 2.4 | I-17.2 | security-risk-records |
| 2.5 | I-17.2, I-14.2(d) | security-risk-records, it-requirements-statement |
| 3.1 | I-17.2, I-17.4 | security-risk-records, anomaly-list |
| 3.2 | I-17.2, I-17.4 | security-risk-records, anomaly-list |
| 3.3 | I-17.1, I-17.2 | software-architecture, security-risk-records |
| 3.4 | I-17.1, I-17.2 | software-requirements, security-risk-records |
| 3.5 | I-17.2, I-17.3 | security-risk-records, verification-records |
| 3.6 | I-17.1, I-17.2 | software-architecture, security-risk-records |
| 3.7 | I-17.4, I-18.8 | anomaly-list, release-record |
| 3.8 | I-17.4, I-18.8 | anomaly-list, release-record |
| 4.1 | I-14.2(d), I-23.4(ab) | it-requirements-statement |
| 4.2 | I-23.4(ab) | it-requirements-statement |
| 5.1 | I-17.4, I-18.8 | anomaly-list, release-record |
| 5.2 | I-17.4, I-18.8 | anomaly-list, release-record |
| 5.3 | I-17.4, I-18.8 | anomaly-list, release-record |

## EU Pack Output Catalog

The same artifact has the same name, kind and description in every EU-law set and the US pack. Each set declares only its used subset; pack tests compare definitions.

| Name | Kind | Description |
|---|---|---|
| risk-management-records | record | Hazard, harm, risk-estimate and residual-risk records. |
| software-requirements | record | Functional and non-functional requirements (FR/NFR). |
| software-architecture | record | Parts and connections in the software architecture. |
| verification-records | record | Test matrix and retained verification evidence. |
| soup-list | record | Software of unknown provenance report. |
| security-risk-records | record | Threat, risk and control records. |
| anomaly-list | record | Unresolved anomaly report. |
| release-record | record | Engineering-assurance release decision. |
| it-requirements-statement | document | Minimum hardware, network and IT-security requirements for instructions for use. |
| written-procedure | procedure | Customer-owned written procedure. |
| signed-record | record | Signed commit or tag verified by the toolchain. |
| audit-trail | record | Git history of the record. |

A clause whose expected outputs are all procedures is customer-owned and requires a delegated disposition with rationale and customer approval reference, never a direct fact. `tests/corpus/` is synthetic; every synthetic ID and evidence reference uses `example.invalid`, and discharge facts are written to a temporary store.

## Requirements Architecture

FR-001 through FR-008 define module home, rights, MDR clauses and applicability, MDCG crosswalks, catalog, customer-owned obligations and corpus. NFR-001 defines the licensing and standards boundary.

## Upstream Contracts

The module uses existing `clause-set-v1`, `clause_sets`, `quire clauses evaluate`, `quire publish-check`, `quoin evidence record-discharge`, and `quoin discharge --rmm`. No engine change is specified.

## References

- EUR-Lex current consolidated MDR text consulted: `https://eur-lex.europa.eu/eli/reg/2017/745/2026-07-19/eng`.
- EUR-Lex legal notice: `https://eur-lex.europa.eu/content/legal-notice/legal-notice.html?locale=en`.
- Commission MDCG listing: `https://health.ec.europa.eu/medical-devices-sector/new-regulations/guidance-mdcg-endorsed-documents-and-other-guidance_en`.
- Commission Decision 2011/833/EU: `https://eur-lex.europa.eu/eli/dec/2011/833/oj/eng`.
