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

This specification defines the clause-only EU-law module and its sets for software-related requirements from Regulation (EU) 2017/745 (MDR), interpretive cybersecurity guidance from MDCG 2019-16 rev.1, and selected obligations in Regulation (EU) 2016/679 (GDPR). Clause summaries use original expression and link to official sources. The pack records evidence and produces an RMM; it does not determine legal compliance.

## Scope

### In Scope

- Repository `agent-ix/spec-clauses-eu-law`, Python package `spec_clauses_eu_law`, module `clause_sets`.
- MDR set `eu/mdr-2017-745@2026-07-19`, MDCG set `eu-mdcg/mdcg-2019-16@rev1`, and GDPR set `eu/gdpr-2016-679@2016-05-04`.
- Set identities, sources, rights metadata, clause identifiers, applicability, expected outputs, MDCG-to-MDR and GDPR-to-NIST/HIPAA crosswalks, shared output catalog, customer-owned obligations, and synthetic reference corpus rules.
- GDPR Articles 25, 30, 32 and 35; the modeled controller/processor and high-risk-processing values; human approval for DPIA residual-risk acceptance; and the security-analysis skill's coverage boundary for GDPR material.

### Out of Scope

- Clause JSON/content, package manifest, corpus, implementation tests, CI, publish gate, output bindings, and scaffold beyond this specification (PLAT-1425, PLAT-1623, PLAT-1624, PLAT-1626).
- GDPR Articles outside 25, 30, 32 and 35, including data-subject rights, international transfers, and breach notifications under Articles 33 and 34; AI Act sets; engine changes; legal advice or compliance determinations.
- Any source text or expression from harmonised or other paywalled standards.

## System Overview

The module manifest lists each set with module-relative paths, declares no object types, archetypes or edges, and installs as a clause-only module. The Quire engine owns generic clause-set schema validation, applicability evaluation, publication checks, and the generic crosswalk contract. Quoin owns disposition evaluation and RMM rendering. This pack owns the EU clause identifiers and original summaries, source-specific rights metadata, the EU output catalog, expected results for applicability and crosswalk tests, and the test-only comparison with the PLAT-1422 canonical output catalog.

Verification requires `quire validate` with clause-set and crosswalk support, `quire clauses evaluate`, `quire publish-check`, and `quoin evidence record-discharge` plus `quoin discharge --rmm`. Test preflight checks the executable and required subcommand/capability before running the relevant checks. A missing executable or capability is a failing verification result naming the unavailable tool or capability; it is never a skipped or passing check.

## Set Design

MDR identity is authority `eu`, ID `mdr-2017-745`, and version `2026-07-19`, the EUR-Lex consolidated-text date consulted. A later consolidation is a new version. Its official URL is `https://eur-lex.europa.eu/eli/reg/2017/745/2026-07-19/eng` (EUR-Lex ELI). Set rights are `structure: citation_only`, `text: original`, `clearance_ref: null`. Licence metadata shall say: `EUR-Lex legal documents may be reused for commercial or non-commercial purposes unless otherwise specified. Consolidated texts are CC BY 4.0; acknowledge the source and indicate changes.` Attribution metadata shall say `© European Union. Source: <official URL>. Changes made.` Source: EUR-Lex legal notice `https://eur-lex.europa.eu/content/legal-notice/legal-notice.html?locale=en`.

GDPR identity is authority `eu`, ID `gdpr-2016-679`, and version `2016-05-04`, the current consolidated-text date shown by EUR-Lex when this specification was authored. A later consolidation is a new version. Its official URL is `https://eur-lex.europa.eu/eli/reg/2016/679/2016-05-04/eng`. Rights are `structure: citation_only`, `text: original`, and `clearance_ref: null`. Licence metadata shall state that EUR-Lex legal documents may be reused for commercial or non-commercial purposes unless otherwise specified, and that EUR-Lex's consolidated text is under CC BY 4.0 with source attribution and indication of changes. Attribution shall identify the European Union, link the official EUR-Lex source and state that the module contains original summaries and changes. The legal notice is `https://eur-lex.europa.eu/content/legal-notice/legal-notice.html?locale=en`. The set contains only Articles 25, 30, 32 and 35; it does not claim coverage of other GDPR articles.

MDCG identity is authority `eu-mdcg`, ID `mdcg-2019-16`, version `rev1`, with source `https://health.ec.europa.eu/document/download/b23b362f-8a56-434c-922a-5b3ca4d0a7a1_en?filename=md_cybersecurity_en.pdf` and listing `https://health.ec.europa.eu/medical-devices-sector/new-regulations/guidance-mdcg-endorsed-documents-and-other-guidance_en`. The PDF identifies the document as endorsed by the Medical Device Coordination Group, states that it is not a European Commission document, and says its views are non-binding. Rights are `structure: citation_only`, `text: original`, and `clearance_ref: null`. Licence metadata SHALL state that no reuse licence is asserted for this source and that the module contains only citations and original summaries, not reproduced PDF text. Attribution SHALL identify the Medical Device Coordination Group (MDCG), *MDCG 2019-16 rev.1*, July 2020, and the official PDF URL; it SHALL identify the module's summaries as original Agent-IX text and SHALL NOT attribute the source to the European Commission or apply Decision 2011/833/EU to it. The guidance is non-binding; clauses are `recommended`. MDR clauses are `mandatory`.

Clause IDs are `<annex roman>-<section>` with subparagraphs in parentheses, e.g. `I-17.3`, `I-23.4(ab)`, `II-6.1(b)`. MDCG IDs are section identifiers without a prefix, e.g. `3.2`. IDs contain no slash. `mobile_platform` has values `yes` and `no`; only `I-17.3` uses it (`eq mobile_platform yes`). Other MDR clauses always bind. Device class is not a dimension because no in-scope clause depends on it.

GDPR clause IDs use the article and paragraph designators, retaining subparagraph letters in parentheses, e.g. `art-30(1)(a)`. `gdpr_role` has values `controller` and `processor`; `high_risk_processing` has values `yes` and `no`. Both are supplied by a person and are never inferred from product or data-flow content. Health data may inform a person's assessment, but it does not determine the high-risk value. Articles 25, 30(1) and 35 apply to controllers; Article 30(2) applies to processors; Article 30(3), 30(4), and 32 apply to both roles. Article 35 applies only when a person sets `high_risk_processing` to `yes` for a controller. Articles 25(3) and 32(3) are not clauses because they describe optional ways to demonstrate compliance. Article 30(5)'s small-organization exemption is not modeled; its exceptions require facts outside the selected dimensions, including whether special-category data are processed. These exclusions do not make another GDPR clause non-binding. Article 35(3) and (4) are triggers used to inform the person's high-risk classification, not separate clauses. Articles 35(5) and (6) assign duties to supervisory authorities, Article 35(8) is conditional on adherence to an approved code, and Article 35(10) is an exception tied to an existing legal basis and prior impact assessment; these are explicit coverage limits because their actors or triggers are outside the selected dimensions. No tool decides the high-risk classification or accepts a DPIA's residual risk.

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

## GDPR Clause Table

The table is normative for clause IDs, force, applicability, and expected outputs. All listed clauses are mandatory. `all[...]` denotes the engine's `all` expression and each `eq` is an equality condition. For Article 32, no applicability expression means the clause applies to both roles.

| Clause ID | Applicability | Expected outputs |
|---|---|---|
| `art-25(1)` | `eq gdpr_role controller` | `privacy-by-default-settings`, `data-flow-model`, `software-architecture`, `security-risk-records` |
| `art-25(2)` | `eq gdpr_role controller` | `privacy-by-default-settings`, `data-flow-model` |
| `art-30(1)(a)` | `eq gdpr_role controller` | `records-of-processing`, `data-flow-model` |
| `art-30(1)(b)` | `eq gdpr_role controller` | `records-of-processing`, `data-flow-model` |
| `art-30(1)(c)` | `eq gdpr_role controller` | `records-of-processing` |
| `art-30(1)(d)` | `eq gdpr_role controller` | `records-of-processing`, `data-flow-model` |
| `art-30(1)(e)` | `eq gdpr_role controller` | `records-of-processing`, `data-flow-model` |
| `art-30(1)(f)` | `eq gdpr_role controller` | `records-of-processing`, `data-flow-model` |
| `art-30(1)(g)` | `eq gdpr_role controller` | `records-of-processing`, `data-flow-model` |
| `art-30(2)(a)` | `eq gdpr_role processor` | `records-of-processing`, `data-flow-model` |
| `art-30(2)(b)` | `eq gdpr_role processor` | `records-of-processing`, `data-flow-model` |
| `art-30(2)(c)` | `eq gdpr_role processor` | `records-of-processing`, `data-flow-model` |
| `art-30(2)(d)` | `eq gdpr_role processor` | `records-of-processing`, `data-flow-model` |
| `art-30(3)` | always | `records-of-processing` |
| `art-30(4)` | always | `records-of-processing` |
| `art-32(1)(a)` | always | `security-risk-records`, `verification-records` |
| `art-32(1)(b)` | always | `security-risk-records`, `verification-records` |
| `art-32(1)(c)` | always | `security-risk-records`, `verification-records` |
| `art-32(1)(d)` | always | `security-risk-records`, `verification-records` |
| `art-32(2)` | always | `security-risk-records` |
| `art-32(4)` | always | `access-control`, `written-procedure`, `training-record` |
| `art-35(1)` | `all[eq gdpr_role controller, eq high_risk_processing yes]` | `dpia`, `data-flow-model`, `security-risk-records` |
| `art-35(2)` | `all[eq gdpr_role controller, eq high_risk_processing yes]` | `dpia`, `data-flow-model` |
| `art-35(7)(a)` | `all[eq gdpr_role controller, eq high_risk_processing yes]` | `dpia`, `data-flow-model` |
| `art-35(7)(b)` | `all[eq gdpr_role controller, eq high_risk_processing yes]` | `dpia`, `security-risk-records` |
| `art-35(7)(c)` | `all[eq gdpr_role controller, eq high_risk_processing yes]` | `dpia`, `data-flow-model`, `privacy-by-default-settings` |
| `art-35(7)(d)` | `all[eq gdpr_role controller, eq high_risk_processing yes]` | `dpia`, `security-risk-records` |
| `art-35(9)` | `all[eq gdpr_role controller, eq high_risk_processing yes]` | `dpia` |
| `art-35(11)` | `all[eq gdpr_role controller, eq high_risk_processing yes]` | `dpia`, `data-flow-model`, `security-risk-records` |

Articles 25(3) and 32(3) are not clauses because they describe optional ways to demonstrate compliance. Article 30(5) is not modeled as an exemption: processing special-category data is one of its explicit exceptions, so the medical-product context does not justify assuming the exemption. Article 35(3) and (4) are triggers rather than separate clauses; paragraphs (5) and (6) are supervisory-authority duties; paragraph (8) is conditional on a code-of-conduct circumstance not represented by the selected dimensions; paragraph (10) is an exception dependent on external legal-basis and prior-assessment facts. Those paragraphs are identified as coverage limits and are not evaluated by this set. Any residual-risk decision associated with a DPIA remains with a named person.

## Article 32 Crosswalk Policy

Crosswalks originate from `art-32(1)(a)` through `(d)` and `art-32(2)`. They may point to `nist/sp800-53@5.2.0` in `spec-objects-security` and `us-hhs/45-cfr-164-subpart-c@2026-11-12` in `spec-clauses-us-health`. The target modules are test-time dependencies and are never copied into this module. Each source clause has at least one target in each module. Relations are `partial` or `informative`; they never assert equivalence. Every target set and clause identifier must resolve in the installed target module. The rationale is an original explanation of scope, not a restatement of target text.

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
| signed-record | record | Signed commits and tags verified by the `signature-verify` capability. |
| audit-trail | record | Git history and signed-approval history produced by the `approval-trail` capability for the record. |
| signer-registry | record | Allowed-signers mapping from signing key to named person, read by the `approval-trail` capability. |
| signature-meaning | record | The `Signed-off-meaning:` trailer verified by the `approval-verify` capability. |
| fda-certification-record | record | Evidence that the electronic-signature certification was submitted to FDA. |
| approval-trail | record | Signed approval history for a record produced by the `approval-trail` capability. |
| access-control | record | Repository permission and branch-rule settings. |
| system-validation | record | Validation evidence for the toolchain's intended use. |
| training-record | procedure | Customer-owned training record. |
| data-flow-model | record | Architecture connections with their declared data flows and classifications. |
| records-of-processing | record | Controller or processor record of processing activities derived from the declared data-flow model. |
| dpia | document | Product-specific data protection impact assessment authored by people, with any residual-risk acceptance recorded by a named approver. |
| privacy-by-default-settings | record | Declared default processing settings and data-minimisation choices. |

A clause whose expected outputs are all procedures is customer-owned and requires a delegated disposition with rationale and customer approval reference, never a direct fact. `tests/corpus/` is synthetic; every synthetic ID and evidence reference uses `example.invalid`, and discharge facts are written to a temporary store.

## Requirements Architecture

FR-001 through FR-015 define module home, rights, MDR, MDCG and GDPR clauses and applicability, crosswalks, catalog, customer-owned obligations, skill mapping, and corpus. NFR-001 defines the licensing and standards boundary; NFR-002 defines the GDPR-specific source and original-expression boundary. StR-001 records the manufacturer's need for reviewable evidence; US-001 describes the human review outcome. FR-001 through FR-015 trace to US-001, and both NFRs constrain the applicable functional requirements.

Dependency graph (an edge A → B means A depends on B): FR-003 → FR-001, FR-002, FR-006; FR-004 → FR-003; FR-005 → FR-001, FR-002, FR-003, FR-006; FR-006 → FR-001; FR-007 → FR-006; FR-008 → FR-001, FR-003, FR-004, FR-005, FR-006, FR-007; FR-009 → FR-001, FR-002, FR-006; FR-010 → FR-009; FR-011 → FR-010; FR-012 → FR-010, FR-011; FR-013 → FR-010, FR-011; FR-014 → FR-010; FR-015 → FR-009, FR-010. NFR-001 constrains FR-001 through FR-015; NFR-002 constrains FR-009 through FR-015.

## Upstream Contracts

The module uses existing `clause-set-v1`, `clause_sets`, `quire clauses evaluate`, `quire publish-check`, `quoin evidence record-discharge`, and `quoin discharge --rmm`. No engine change is specified.

## References

- EUR-Lex current consolidated MDR text consulted: `https://eur-lex.europa.eu/eli/reg/2017/745/2026-07-19/eng`.
- EUR-Lex legal notice: `https://eur-lex.europa.eu/content/legal-notice/legal-notice.html?locale=en`.
- MDCG 2019-16 rev.1 official PDF: `https://health.ec.europa.eu/document/download/b23b362f-8a56-434c-922a-5b3ca4d0a7a1_en?filename=md_cybersecurity_en.pdf`.
- Commission MDCG listing: `https://health.ec.europa.eu/medical-devices-sector/new-regulations/guidance-mdcg-endorsed-documents-and-other-guidance_en`.
- EUR-Lex current consolidated GDPR text consulted: `https://eur-lex.europa.eu/eli/reg/2016/679/2016-05-04/eng`.
- EUR-Lex legal notice on reuse and attribution: `https://eur-lex.europa.eu/content/legal-notice/legal-notice.html?locale=en`.
