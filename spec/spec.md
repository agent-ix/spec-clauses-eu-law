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

The module manifest lists each set with module-relative paths, declares no object types, archetypes or edges, and installs as a clause-only module. The Quire engine owns generic clause-set schema validation, applicability evaluation, publication checks, and the generic crosswalk contract. Quoin owns disposition evaluation and RMM rendering. This pack owns the EU clause identifiers and original summaries, source-specific rights metadata, the EU output catalog, expected results for applicability and crosswalk tests, and the test-only comparison with the PLAT-1422 canonical output catalog.

Verification requires `quire validate` with clause-set and crosswalk support, `quire clauses evaluate`, `quire publish-check`, and `quoin evidence record-discharge` plus `quoin discharge --rmm`. Test preflight checks the executable and required subcommand/capability before running the relevant checks. A missing executable or capability is a failing verification result naming the unavailable tool or capability; it is never a skipped or passing check.

## Set Design

MDR identity is authority `eu`, ID `mdr-2017-745`, and version `2026-07-19`, the EUR-Lex consolidated-text date consulted. A later consolidation is a new version. Its official URL is `https://eur-lex.europa.eu/eli/reg/2017/745/2026-07-19/eng` (EUR-Lex ELI). Set rights are `structure: citation_only`, `text: original`, `clearance_ref: null`. Licence metadata shall say: `EUR-Lex legal documents may be reused for commercial or non-commercial purposes unless otherwise specified. Consolidated texts are CC BY 4.0; acknowledge the source and indicate changes.` Attribution metadata shall say `© European Union. Source: <official URL>. Changes made.` Source: EUR-Lex legal notice `https://eur-lex.europa.eu/content/legal-notice/legal-notice.html?locale=en`.

MDCG identity is authority `eu-mdcg`, ID `mdcg-2019-16`, version `rev1`, with source `https://health.ec.europa.eu/document/download/b23b362f-8a56-434c-922a-5b3ca4d0a7a1_en?filename=md_cybersecurity_en.pdf` and listing `https://health.ec.europa.eu/medical-devices-sector/new-regulations/guidance-mdcg-endorsed-documents-and-other-guidance_en`. The PDF identifies the document as endorsed by the Medical Device Coordination Group, states that it is not a European Commission document, and says its views are non-binding. Rights are `structure: citation_only`, `text: original`, and `clearance_ref: null`. Licence metadata SHALL state that no reuse licence is asserted for this source and that the module contains only citations and original summaries, not reproduced PDF text. Attribution SHALL identify the Medical Device Coordination Group (MDCG), *MDCG 2019-16 rev.1*, July 2020, and the official PDF URL; it SHALL identify the module's summaries as original Agent-IX text and SHALL NOT attribute the source to the European Commission or apply Decision 2011/833/EU to it. The guidance is non-binding; clauses are `recommended`. MDR clauses are `mandatory`.

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

The pack includes only the substantive software and cybersecurity sections 2.1–2.6, 3.1–3.8, 4.1–4.3, and 5.1–5.2 from the official table of contents. Section 1 (introduction and abbreviations), section 6 (other Union legislation and guidance), and Annexes I–IV are outside this set; the annex material that identifies standards is excluded. Subsections 2.6.1–2.6.3 are included within section 2.6, not separate clause IDs. Every included section is recommended, not mandatory. The source table of contents contains no section 5.3. Crosswalk relations use `partial` when the MDCG section gives cybersecurity/software detail that addresses only part of the cited MDR clause, and `informative` when it supplies context without asserting equivalent coverage. Targets resolve against the loaded MDR set. The rationale is an original statement of mapping scope and does not restate guidance text.

| MDCG ID | MDR target | Relation | Rationale | Expected outputs |
|---|---|---|---|---|
| 2.1 | I-1 | informative | Introduces the guidance context for risk management; it does not replace the MDR risk-management requirement. | risk-management-records |
| 2.1 | I-3 | partial | Connects cybersecurity risk consideration to the broader risk process while covering only the cybersecurity aspect. | risk-management-records |
| 2.2 | I-17.2 | partial | Describes cybersecurity as part of software risk management, covering only that aspect of the MDR software lifecycle clause. | security-risk-records |
| 2.3 | I-17.2 | partial | Frames cybersecurity risk management across the software lifecycle, a subset of the clause's lifecycle activities. | security-risk-records |
| 2.3 | I-17.4 | partial | Relates cybersecurity risk control to software security, without covering all software verification and validation. | security-risk-records, anomaly-list |
| 2.4 | I-17.2 | partial | Describes a risk-management approach for cybersecurity threats, not the entire software lifecycle process. | security-risk-records |
| 2.5 | I-17.2 | partial | Connects threat identification and risk analysis to software lifecycle risk records. | security-risk-records |
| 2.5 | I-14.2(d) | informative | Network and IT-security considerations can inform the device's stated environmental and infrastructure requirements. | it-requirements-statement |
| 2.6 | I-17.2 | partial | The section's security risk-control discussion covers a subset of software lifecycle risk management. | security-risk-records |
| 2.6 | I-17.4 | partial | Security-control discussion informs software security measures but does not cover the full verification and validation obligation. | security-risk-records, verification-records |
| 3.1 | I-17.2 | partial | Security-by-design guidance concerns software lifecycle activities, limited to the cybersecurity dimension. | security-risk-records |
| 3.1 | I-17.4 | partial | Security-by-design informs software security measures, not every verification and validation activity. | security-risk-records, anomaly-list |
| 3.2 | I-17.2 | partial | Secure design guidance concerns software lifecycle activity only for cybersecurity risks. | security-risk-records |
| 3.2 | I-17.4 | partial | Design recommendations inform security measures but do not establish the full verification outcome. | security-risk-records, anomaly-list |
| 3.3 | I-17.1 | partial | Architecture guidance concerns software architecture within the broader software lifecycle. | software-architecture |
| 3.3 | I-17.2 | partial | Architecture guidance addresses cybersecurity-related software lifecycle risks. | security-risk-records |
| 3.4 | I-17.1 | partial | Software requirements guidance addresses only the requirements portion of lifecycle processes. | software-requirements |
| 3.4 | I-17.2 | partial | Security requirements contribute to, but do not exhaust, software risk management. | security-risk-records |
| 3.5 | I-17.2 | partial | Implementation guidance addresses cybersecurity risk controls within lifecycle risk management. | security-risk-records |
| 3.5 | I-17.3 | partial | The guidance can inform mobile-platform verification when applicable, without making that MDR clause universally applicable. | verification-records |
| 3.6 | I-14.2(d) | partial | Minimum IT requirements inform only the device's infrastructure requirement. | it-requirements-statement |
| 3.6 | I-23.4(ab) | informative | Environment and security information may inform instructions but does not cover the whole instructions requirement. | it-requirements-statement |
| 3.7 | I-17.4 | partial | Verification and validation guidance addresses a portion of the software lifecycle process. | verification-records |
| 3.7 | I-18.8 | partial | Verification and validation evidence can contribute to the release process without covering its full scope. | verification-records, release-record |
| 3.8 | I-17.4 | partial | Lifecycle guidance informs continuing software security activities but not all verification and validation duties. | anomaly-list |
| 3.8 | I-18.8 | partial | Vulnerability resolution may affect release evidence, without covering all release-process duties. | release-record |
| 4.1 | I-14.2(d) | partial | Security requirements for the operating environment inform only the IT-infrastructure portion of this requirement. | it-requirements-statement |
| 4.1 | I-23.4(ab) | informative | User information can inform the security-related content considered for instructions, without asserting full equivalence. | it-requirements-statement |
| 4.2 | I-23.4(ab) | partial | Security information for users contributes to, but does not exhaust, the information required by this clause. | it-requirements-statement |
| 4.3 | I-17.4 | partial | Operational security guidance informs software security measures, not all verification and validation activities. | verification-records |
| 4.3 | I-23.4(ab) | informative | User-facing security considerations may inform instructions but do not establish clause equivalence. | it-requirements-statement |
| 5.1 | I-17.4 | partial | Lifecycle maintenance guidance informs software security evidence but does not exhaust the clause. | anomaly-list |
| 5.1 | I-18.8 | partial | Maintenance and update records can support release evidence within the broader release obligation. | release-record |
| 5.2 | I-17.4 | partial | Incident and vulnerability response informs software maintenance evidence, not the whole lifecycle obligation. | anomaly-list |
| 5.2 | I-18.8 | partial | Response and release handling are related, but the guidance addresses only part of the MDR release process. | release-record |

## EU Pack Output Catalog

The same artifact has the same name, kind and description in every EU-law set. Each set declares only its used subset. For names shared with the US pack, the canonical definition is the PLAT-1422 US Health-Law Output Catalog in its `spec/spec.md`; the EU contract test loads that file as a test-only dependency and compares every shared name and both fields. It does not keep a copied fixture or hand-maintained list of shared names.

| Name | Kind | Description |
|---|---|---|
| risk-management-records | record | `spec-objects-safety` hazard, harm, risk-estimate, and residual-risk records. |
| software-requirements | record | Functional and non-functional requirements (FR/NFR). |
| software-architecture | record | `spec-objects-architecture` parts and connections. |
| verification-records | record | Test matrix and retained evidence. |
| soup-list | record | Software of unknown provenance (SOUP) report. |
| security-risk-records | record | `spec-objects-security` threat, risk, and control records. |
| anomaly-list | record | Unresolved-anomaly report. |
| release-record | record | Engineering-assurance release decision. |
| it-requirements-statement | document | Minimum hardware, network and IT-security requirements for instructions for use. |
| written-procedure | procedure | Customer-owned written procedure. |
| signed-record | record | Signed commit or tag verified by `git verify-commit` or `git verify-tag`. |
| audit-trail | record | Git history of the record. |
| signer-registry | record | Allowed-signers mapping from signing key to named person. |
| signature-meaning | record | The `Signed-off-meaning:` trailer. |
| fda-certification-record | record | Evidence that the electronic-signature certification was submitted to FDA. |
| approval-trail | record | Engineering-assurance approval-trail output. |
| access-control | record | Repository permission and branch-rule settings. |
| system-validation | record | Validation evidence for the toolchain's intended use. |
| training-record | procedure | Customer-owned training record. |

A clause whose expected outputs are all procedures is customer-owned and requires a delegated disposition with rationale and customer approval reference, never a direct fact. `tests/corpus/` is synthetic; every synthetic ID and evidence reference uses `example.invalid`, and discharge facts are written to a temporary store.

## Requirements Architecture

FR-001 through FR-008 define module home, rights, MDR clauses and applicability, MDCG crosswalks, catalog, customer-owned obligations and corpus. NFR-001 defines the licensing and standards boundary. StR-001 records the manufacturer's need for reviewable evidence; US-001 describes the human review outcome. FR-001 through FR-008 trace to US-001, and NFR-001 constrains every FR.

Dependency graph (an edge A → B means A depends on B): FR-003 → FR-001, FR-002, FR-006; FR-004 → FR-003; FR-005 → FR-001, FR-002, FR-003, FR-006; FR-006 → FR-001; FR-007 → FR-006; FR-008 → FR-001, FR-003, FR-004, FR-005, FR-006, FR-007. NFR-001 constrains FR-001 through FR-008.

## Upstream Contracts

The module uses existing `clause-set-v1`, `clause_sets`, `quire clauses evaluate`, `quire publish-check`, `quoin evidence record-discharge`, and `quoin discharge --rmm`. No engine change is specified.

## References

- EUR-Lex current consolidated MDR text consulted: `https://eur-lex.europa.eu/eli/reg/2017/745/2026-07-19/eng`.
- EUR-Lex legal notice: `https://eur-lex.europa.eu/content/legal-notice/legal-notice.html?locale=en`.
- MDCG 2019-16 rev.1 official PDF: `https://health.ec.europa.eu/document/download/b23b362f-8a56-434c-922a-5b3ca4d0a7a1_en?filename=md_cybersecurity_en.pdf`.
- Commission MDCG listing: `https://health.ec.europa.eu/medical-devices-sector/new-regulations/guidance-mdcg-endorsed-documents-and-other-guidance_en`.
