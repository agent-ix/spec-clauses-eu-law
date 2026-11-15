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
  - artificial-intelligence
security_critical: false
---
# Master Requirements Specification

## Purpose

This specification defines the clause-only EU-law module and its sets for software-related requirements from Regulation (EU) 2017/745 (MDR), interpretive cybersecurity guidance from MDCG 2019-16 rev.1, selected obligations in Regulation (EU) 2016/679 (GDPR), and selected high-risk AI obligations and technical-documentation elements in Regulation (EU) 2024/1689 (AI Act). Clause summaries use original expression and link to official sources. The pack records evidence and produces an RMM; it does not determine legal compliance.

## Scope

### In Scope

- Repository `agent-ix/spec-clauses-eu-law`, Python package `spec_clauses_eu_law`, module `clause_sets`.
- MDR set `eu/mdr-2017-745@2026-07-19`, MDCG set `eu-mdcg/mdcg-2019-16@rev1`, GDPR set `eu/gdpr-2016-679@2016-05-04`, and AI Act sets `eu/ai-act-2024-1689@2026-07-27` and `eu/ai-act-2024-1689-annex-iv@2026-07-27`.
- Set identities, sources, rights metadata, clause identifiers, applicability, expected outputs, MDCG-to-MDR and GDPR-to-NIST/HIPAA crosswalks, shared output catalog, customer-owned obligations, and synthetic reference corpus rules.
- GDPR Articles 25, 30, 32 and 35; the person-supplied controller/processor, high-risk-processing, and Article 30(5) applicability values; human approval for DPIA residual-risk acceptance; and the security-analysis skill's coverage boundary for GDPR material.
- AI Act high-risk provider obligations in Articles 9–20, 43, 47, 72 and 73; deployer obligations in Article 26; Annex IV technical-documentation elements; person-supplied high-risk, operator-role and per-point applicability values; and crosswalks to MDR Annex II.

### Out of Scope

- Clause JSON/content, package manifest, corpus, implementation tests, CI, publish gate, output bindings, and scaffold beyond this specification (PLAT-1425, PLAT-1623, PLAT-1624, PLAT-1626).
- GDPR Articles outside 25, 30, 32 and 35, including data-subject rights, international transfers, and breach notifications under Articles 33 and 34; AI Act provisions outside the selected high-risk provider/deployer duties and Annex IV, including prohibited practices, general-purpose AI models and fundamental-rights impact assessments; engine changes; legal advice or compliance determinations.
- Any source text or expression from harmonised or other paywalled standards.

## System Overview

The module manifest lists each set with module-relative paths, declares no object types, archetypes or edges, and installs as a clause-only module. The Quire engine owns generic clause-set schema validation, applicability evaluation, publication checks, and the generic crosswalk contract. Quoin owns disposition evaluation and RMM rendering. This pack owns the EU clause identifiers and original summaries, source-specific rights metadata, the EU output catalog, expected results for applicability and crosswalk tests, and the test-only comparison with the PLAT-1422 canonical output catalog.

Verification requires `quire validate` with clause-set and crosswalk support, `quire clauses evaluate`, `quire publish-check`, and `quoin evidence record-discharge` plus `quoin discharge --rmm`. Test preflight checks the executable and required subcommand/capability before running the relevant checks. A missing executable or capability is a failing verification result naming the unavailable tool or capability; it is never a skipped or passing check.

## Set Design

MDR identity is authority `eu`, ID `mdr-2017-745`, and version `2026-07-19`, the EUR-Lex consolidated-text date consulted. A later consolidation is a new version. Its official URL is `https://eur-lex.europa.eu/eli/reg/2017/745/2026-07-19/eng` (EUR-Lex ELI). Set rights are `structure: citation_only`, `text: original`, `clearance_ref: null`. Licence metadata shall say: `EUR-Lex legal documents may be reused for commercial or non-commercial purposes unless otherwise specified. Consolidated texts are CC BY 4.0; acknowledge the source and indicate changes.` Attribution metadata shall say `© European Union. Source: <{official URL}>. Changes made.` Source: EUR-Lex legal notice `https://eur-lex.europa.eu/content/legal-notice/legal-notice.html?locale=en`.

GDPR identity is authority `eu`, ID `gdpr-2016-679`, and version `2016-05-04`, the current consolidated-text date shown by EUR-Lex when this specification was authored. A later consolidation is a new version. Its official URL is `https://eur-lex.europa.eu/eli/reg/2016/679/2016-05-04/eng`. Rights are `structure: citation_only`, `text: original`, and `clearance_ref: null`. Licence metadata shall state that EUR-Lex legal documents may be reused for commercial or non-commercial purposes unless otherwise specified, and that EUR-Lex's consolidated text is under CC BY 4.0 with source attribution and indication of changes. Attribution shall identify the European Union, link the official EUR-Lex source and state that the module contains original summaries and changes. The legal notice is `https://eur-lex.europa.eu/content/legal-notice/legal-notice.html?locale=en`. The set contains only Articles 25, 30, 32 and 35; it does not claim coverage of other GDPR articles.

MDCG identity is authority `eu-mdcg`, ID `mdcg-2019-16`, version `rev1`, with source `https://health.ec.europa.eu/document/download/b23b362f-8a56-434c-922a-5b3ca4d0a7a1_en?filename=md_cybersecurity_en.pdf` and listing `https://health.ec.europa.eu/medical-devices-sector/new-regulations/guidance-mdcg-endorsed-documents-and-other-guidance_en`. The PDF identifies the document as endorsed by the Medical Device Coordination Group, states that it is not a European Commission document, and says its views are non-binding. Rights are `structure: citation_only`, `text: original`, and `clearance_ref: null`. Licence metadata SHALL state that no reuse licence is asserted for this source and that the module contains only citations and original summaries, not reproduced PDF text. Attribution SHALL say `Medical Device Coordination Group (MDCG), *MDCG 2019-16 rev.1*, July 2020. Source: <{source URL}>. Listing: <{listing URL}>. The source is not a European Commission publication; summaries are original Agent-IX text.` The guidance is non-binding; clauses are `recommended`. MDR clauses are `mandatory`.

Clause IDs are `<annex roman>-<section>` with subparagraphs in parentheses, e.g. `I-17.3`, `I-23.4(ab)`, `II-6.1(b)`. MDCG IDs are section identifiers without a prefix, e.g. `3.2`. IDs contain no slash. `mobile_platform` has values `yes` and `no`; only `I-17.3` uses it (`eq mobile_platform yes`). Other MDR clauses always bind. Device class is not a dimension because no in-scope clause depends on it.

GDPR clause IDs use the article and paragraph designators, retaining subparagraph letters in parentheses, e.g. `art-30(1)(a)`. `gdpr_role` has values `controller` and `processor`; `high_risk_processing` has values `yes` and `no`; and `article_30_records_applicability` has values `applies` and `exempt`. A responsible person supplies all three values. The module never infers them from product type, data type, risk score, or role. Health data may inform a person's assessment but does not determine `high_risk_processing`. For Article 30(5), the person sets `exempt` only after determining the organization employs fewer than 250 people and none of the statutory exceptions applies: processing is not occasional, is likely to result in risk to data-subject rights and freedoms, or includes special-category or criminal-conviction data. In every other case the person sets `applies`. If `article_30_records_applicability` is missing, Article 30(1) remains unresolved for a controller and not binding for a processor; 30(2) remains unresolved for a processor and not binding for a controller; and 30(3) and (4) remain unresolved for either role. If `gdpr_role` is also missing, Article 30(1) through (4) remain unresolved. If applicability is `exempt`, Article 30(1) through (4) are not binding. If it is `applies`, Article 30(1) applies to controllers, 30(2) applies to processors, and 30(3) and (4) apply to the records required under either role. The input is a classification of statutory applicability, not an accepted-risk disposition.

Articles 25 and 35 apply to controllers; Article 32 applies to both roles. Article 35 applies only when a person sets `high_risk_processing` to `yes` for a controller. Articles 25(3) and 32(3) are not clauses because they describe optional ways to demonstrate compliance. Article 35(3) and (4) are triggers used to inform the person's high-risk classification, not separate clauses. Articles 35(5) and (6) assign duties to supervisory authorities, Article 35(8) is conditional on adherence to an approved code, and Article 35(10) is an exception tied to an existing legal basis and prior impact assessment; these are explicit coverage limits because their actors or triggers are outside the selected dimensions. No tool decides the high-risk classification or accepts a DPIA's residual risk.

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
| `art-30(1)(a)` | `all[eq gdpr_role controller, eq article_30_records_applicability applies]` | `records-of-processing`, `data-flow-model` |
| `art-30(1)(b)` | `all[eq gdpr_role controller, eq article_30_records_applicability applies]` | `records-of-processing`, `data-flow-model` |
| `art-30(1)(c)` | `all[eq gdpr_role controller, eq article_30_records_applicability applies]` | `records-of-processing` |
| `art-30(1)(d)` | `all[eq gdpr_role controller, eq article_30_records_applicability applies]` | `records-of-processing`, `data-flow-model` |
| `art-30(1)(e)` | `all[eq gdpr_role controller, eq article_30_records_applicability applies]` | `records-of-processing`, `data-flow-model` |
| `art-30(1)(f)` | `all[eq gdpr_role controller, eq article_30_records_applicability applies]` | `records-of-processing`, `data-flow-model` |
| `art-30(1)(g)` | `all[eq gdpr_role controller, eq article_30_records_applicability applies]` | `records-of-processing`, `data-flow-model` |
| `art-30(2)(a)` | `all[eq gdpr_role processor, eq article_30_records_applicability applies]` | `records-of-processing`, `data-flow-model` |
| `art-30(2)(b)` | `all[eq gdpr_role processor, eq article_30_records_applicability applies]` | `records-of-processing`, `data-flow-model` |
| `art-30(2)(c)` | `all[eq gdpr_role processor, eq article_30_records_applicability applies]` | `records-of-processing`, `data-flow-model` |
| `art-30(2)(d)` | `all[eq gdpr_role processor, eq article_30_records_applicability applies]` | `records-of-processing`, `data-flow-model` |
| `art-30(3)` | `eq article_30_records_applicability applies` | `records-of-processing` |
| `art-30(4)` | `eq article_30_records_applicability applies` | `records-of-processing` |
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

Articles 25(3) and 32(3) are not clauses because they describe optional ways to demonstrate compliance. Article 30(5)'s exemption decision is represented by the person-supplied `article_30_records_applicability` value; a medical-product context or assumed health-data use is not enough to resolve it. Article 30(3) and (4) explicitly inherit this value because they concern records required under paragraphs 1 and 2. Article 35(3) and (4) are triggers rather than separate clauses; paragraphs (5) and (6) are supervisory-authority duties; paragraph (8) is conditional on a code-of-conduct circumstance not represented by the selected dimensions; paragraph (10) is an exception dependent on external legal-basis and prior-assessment facts. Those Article 35 paragraphs are identified as coverage limits and are not evaluated by this set. Any residual-risk decision associated with a DPIA remains with a named person.

## AI Act Set Design

The AI Act sets use authority `eu`, IDs `ai-act-2024-1689` and `ai-act-2024-1689-annex-iv`, and version `2026-07-27`, the EUR-Lex consolidated-text date consulted. Their official source is `https://eur-lex.europa.eu/eli/reg/2024/1689/2026-07-27/eng`; a later consolidated text is a new set version. Rights are `structure: citation_only`, `text: original`, and `clearance_ref: null`. Licence metadata states that EUR-Lex legal documents may be reused for commercial or non-commercial purposes unless otherwise specified and that the consolidated text is under CC BY 4.0 with source attribution and indication of changes. Attribution identifies the European Union, cites the exact official source, states that changes were made, and references `https://eur-lex.europa.eu/content/legal-notice/legal-notice.html?locale=en`. No Commission reuse terms for standards are inferred from this law-text licence.

AI Act clause IDs use `art-<article>` and Annex IV IDs use `IV-<section>(<letter>)` for lettered points or `IV-<section>` for unlettered points. The person supplies `ai_high_risk` (`yes` or `no`) and `ai_role` (`provider` or `deployer`); the tool never infers classification or role from the product. Provider clauses use `all[eq ai_high_risk yes, eq ai_role provider]`; Article 26 clauses use `all[eq ai_high_risk yes, eq ai_role deployer]`. Missing required values leave dependent clauses unresolved. A known role-incompatible clause is not binding. Each Annex IV point also has its own person-supplied applicability dimension `ai_annex_iv_<point>_applicable` (`yes` or `no`); its clause expression requires `yes` as well as high-risk provider context. A `no` value makes that point not binding, and a missing value leaves it unresolved. The person records whether the documentation item applies to the particular system from the conditions in the Annex IV table; the tool does not infer relevance or applicability. The Article 6(1) high-risk classification is made by a person outside this module; these dimensions record that decision rather than decide it.

For the consolidated text dated 2026-07-27, Article 113 applies Chapter III Sections 1–3 to Article 6(1) high-risk AI systems related to Annex I products from 2 August 2028. The AI Act set records that date for its Annex I scope. It is reference metadata, not an evaluated applicability dimension; a later amendment or consolidation requires a new set version.

## AI Act High-Risk Obligations Table

This table is normative for IDs, force, applicability, and expected outputs. The provider set includes only the listed provider-facing obligations. Article 26 contains the selected deployer obligations. Other actors, provisions and unlisted articles are outside this set. Each clause summary uses original wording and does not reproduce source text.

| Clause ID | Coverage | Applicability | Force | Expected outputs |
|---|---|---|---|---|
| `art-9` | Risk-management process and review | `all[eq ai_high_risk yes, eq ai_role provider]` | mandatory | `risk-management-records` |
| `art-10` | Training, validation and testing data governance | `all[eq ai_high_risk yes, eq ai_role provider]` | mandatory | `data-lineage`, `verification-records` |
| `art-11` | Technical documentation prepared and maintained | `all[eq ai_high_risk yes, eq ai_role provider]` | mandatory | `model-description`, `software-architecture`, `verification-records` |
| `art-12` | Automatic event logging and traceability | `all[eq ai_high_risk yes, eq ai_role provider]` | mandatory | `event-logging-design` |
| `art-13` | Information and instructions enabling deployer use | `all[eq ai_high_risk yes, eq ai_role provider]` | mandatory | `model-description`, `written-procedure` |
| `art-14` | Human-oversight design and measures | `all[eq ai_high_risk yes, eq ai_role provider]` | mandatory | `human-oversight-design` |
| `art-15` | Accuracy, robustness and cybersecurity | `all[eq ai_high_risk yes, eq ai_role provider]` | mandatory | `verification-records`, `security-risk-records` |
| `art-16` | Provider duties for conformity, documentation, corrective action and cooperation | `all[eq ai_high_risk yes, eq ai_role provider]` | mandatory | `model-description`, `release-record`, `written-procedure` |
| `art-17` | Quality-management system | `all[eq ai_high_risk yes, eq ai_role provider]` | mandatory | `written-procedure`, `audit-trail` |
| `art-18` | Retention of documentation and logs | `all[eq ai_high_risk yes, eq ai_role provider]` | mandatory | `model-description`, `event-logging-design` |
| `art-19` | Automatically generated logs under provider control | `all[eq ai_high_risk yes, eq ai_role provider]` | mandatory | `event-logging-design` |
| `art-20` | Corrective action and authority notification | `all[eq ai_high_risk yes, eq ai_role provider]` | mandatory | `written-procedure`, `release-record` |
| `art-26` | Deployer use, oversight, monitoring and incident duties | `all[eq ai_high_risk yes, eq ai_role deployer]` | mandatory | `human-oversight-design`, `written-procedure`, `event-logging-design` |
| `art-43` | Conformity-assessment route | `all[eq ai_high_risk yes, eq ai_role provider]` | mandatory | `conformity-declaration`, `verification-records` |
| `art-47` | EU declaration of conformity | `all[eq ai_high_risk yes, eq ai_role provider]` | mandatory | `conformity-declaration` |
| `art-72` | Post-market monitoring system and plan | `all[eq ai_high_risk yes, eq ai_role provider]` | mandatory | `post-market-monitoring-plan`, `event-logging-design` |
| `art-73` | Serious-incident reporting | `all[eq ai_high_risk yes, eq ai_role provider]` | mandatory | `written-procedure`, `anomaly-list` |

With `ai_high_risk=no`, every listed clause is `not_binding`; with `yes` and provider, provider clauses bind and Article 26 is `not_binding`; with `yes` and deployer, Article 26 binds and provider clauses are `not_binding`. A missing required dimension leaves dependent clauses unresolved. The set does not make a legal classification or conformity decision.

## AI Act Annex IV Table

This table is normative for every Annex IV point included. Each point has mandatory force when the person records it as applicable. Its applicability expression requires both provider/high-risk context and its own person-supplied point-applicability value. The Annex IV introduction limits the information to what applies to the relevant system; the condition column preserves that rule and each point's specific `where applicable` or `where relevant` qualifier. Each point declares at least one output from the catalog. A point's crosswalk target is an MDR Annex II clause; `none` records that no direct Annex II counterpart is asserted. Crosswalk rationales are original statements of scope, and relations are `partial` or `informative`, never `equivalent`.

| Clause ID | Documentation element | Applicability condition | Applicability expression | Expected outputs | MDR Annex II target | Relation | Rationale |
|---|---|---|---|---|---|---|---|
| `IV-1(a)` | Intended purpose, provider identity and version lineage | As applicable to the relevant system | `all[eq ai_high_risk yes, eq ai_role provider, eq ai_annex_iv_1_a_applicable yes]` | `model-description` | `II-1.1` | partial | MDR device description includes intended purpose and identity, but not the complete AI system/version lineage. |
| `IV-1(b)` | Interactions with hardware, software and other systems | Where such interactions are applicable; as applicable to the relevant system | `all[eq ai_high_risk yes, eq ai_role provider, eq ai_annex_iv_1_b_applicable yes]` | `software-architecture` | `II-1.1` | partial | MDR device description can identify the device context and related components, while this point documents AI-system interactions. |
| `IV-1(c)` | Relevant software or firmware versions and update requirements | Relevant versions and update requirements for the system | `all[eq ai_high_risk yes, eq ai_role provider, eq ai_annex_iv_1_c_applicable yes]` | `model-description` | `II-1.1` | partial | MDR device description covers device/software identification but not all AI software version-update information. |
| `IV-1(d)` | Forms in which the system is placed on the market or put into service | Forms used for the relevant system | `all[eq ai_high_risk yes, eq ai_role provider, eq ai_annex_iv_1_d_applicable yes]` | `model-description` | `none` | `none` | The selected MDR software clauses contain no direct counterpart for all AI distribution forms. |
| `IV-1(e)` | Hardware on which the system is intended to run | Hardware relevant to the system | `all[eq ai_high_risk yes, eq ai_role provider, eq ai_annex_iv_1_e_applicable yes]` | `software-architecture` | `II-1.1` | partial | The MDR device description can capture hardware context but does not enumerate all AI deployment hardware. |
| `IV-1(f)` | Product component illustrations, external features, markings and layout | Only where the AI system is a component of a product | `all[eq ai_high_risk yes, eq ai_role provider, eq ai_annex_iv_1_f_applicable yes]` | `software-architecture` | `II-1.1` | partial | MDR device description includes device illustrations, while this point identifies the AI component and its product placement. |
| `IV-1(g)` | Basic description of the deployer-facing interface | As applicable to the relevant system | `all[eq ai_high_risk yes, eq ai_role provider, eq ai_annex_iv_1_g_applicable yes]` | `model-description` | `none` | `none` | The selected MDR software clauses do not directly cover the AI deployer interface description. |
| `IV-1(h)` | Instructions for use and applicable interface description | Interface description where applicable; as applicable to the relevant system | `all[eq ai_high_risk yes, eq ai_role provider, eq ai_annex_iv_1_h_applicable yes]` | `model-description`, `written-procedure` | `none` | `none` | The selected MDR software clauses do not directly cover these AI-specific deployer instructions. |
| `IV-2(a)` | Development methods and steps | Third-party or pre-trained tools where relevant; as applicable to the relevant system | `all[eq ai_high_risk yes, eq ai_role provider, eq ai_annex_iv_2_a_applicable yes]` | `software-architecture`, `verification-records` | `none` | `none` | The selected MDR software clauses do not directly cover the AI development-process record. |
| `IV-2(b)` | Design specifications, logic, assumptions and classification choices | As applicable to the relevant system | `all[eq ai_high_risk yes, eq ai_role provider, eq ai_annex_iv_2_b_applicable yes]` | `model-description`, `software-architecture` | `II-1.1` | informative | MDR device description provides context for the AI design record without covering its internal logic or classification choices. |
| `IV-2(c)` | Architecture, component integration and computational resources | As applicable to the relevant system | `all[eq ai_high_risk yes, eq ai_role provider, eq ai_annex_iv_2_c_applicable yes]` | `software-architecture` | `II-1.1` | partial | The MDR device description informs system architecture while the AI point adds model and computational-resource detail. |
| `IV-2(d)` | Data requirements, provenance, selection and preparation | Only where relevant to the system | `all[eq ai_high_risk yes, eq ai_role provider, eq ai_annex_iv_2_d_applicable yes]` | `data-lineage` | `none` | `none` | No selected MDR Annex II software clause directly specifies AI training-data governance documentation. |
| `IV-2(e)` | Human-oversight assessment and output-interpretation measures | Measures needed for the system | `all[eq ai_high_risk yes, eq ai_role provider, eq ai_annex_iv_2_e_applicable yes]` | `human-oversight-design` | `none` | `none` | The selected MDR software clauses do not directly impose the AI Act human-oversight documentation element. |
| `IV-2(f)` | Predetermined system changes and continuous-conformity measures | Only where predetermined changes apply | `all[eq ai_high_risk yes, eq ai_role provider, eq ai_annex_iv_2_f_applicable yes]` | `release-record`, `verification-records` | `none` | `none` | The selected MDR software clauses do not directly cover this AI-specific change-control description. |
| `IV-2(g)` | Validation and test procedures, data, metrics, logs and reports | As applicable to the relevant system | `all[eq ai_high_risk yes, eq ai_role provider, eq ai_annex_iv_2_g_applicable yes]` | `verification-records` | `II-6.1(b)` | partial | MDR software validation evidence overlaps, but does not cover the full AI validation and reporting detail. |
| `IV-2(h)` | Cybersecurity measures | As applicable to the relevant system | `all[eq ai_high_risk yes, eq ai_role provider, eq ai_annex_iv_2_h_applicable yes]` | `security-risk-records`, `verification-records` | `II-4` | partial | MDR general safety and performance requirements include security concerns; this AI point adds system-specific measures. |
| `IV-3` | Capabilities, limitations, risks, oversight and input specifications | Specifications and measures applicable to the relevant system | `all[eq ai_high_risk yes, eq ai_role provider, eq ai_annex_iv_3_applicable yes]` | `model-description`, `human-oversight-design`, `security-risk-records` | `II-1.1` | partial | Device description provides context, but does not cover all AI performance, oversight and input details. |
| `IV-4` | Suitability of performance metrics for the system | As applicable to the relevant system | `all[eq ai_high_risk yes, eq ai_role provider, eq ai_annex_iv_4_applicable yes]` | `verification-records` | `II-6.1(b)` | partial | MDR software validation metrics overlap, but the AI point adds metric suitability for the AI system. |
| `IV-5` | Risk-management system | As applicable to the relevant system | `all[eq ai_high_risk yes, eq ai_role provider, eq ai_annex_iv_5_applicable yes]` | `risk-management-records` | `II-5` | partial | MDR benefit-risk and risk-management evidence overlaps with the AI risk system without establishing equivalence. |
| `IV-6` | Relevant lifecycle changes | Changes made by the provider through the system lifecycle | `all[eq ai_high_risk yes, eq ai_role provider, eq ai_annex_iv_6_applicable yes]` | `release-record` | `none` | `none` | The selected MDR software clauses do not directly cover the complete AI lifecycle-change description. |
| `IV-7` | Applied standards or other solutions used to meet requirements | Applicable solutions; no particular standard is identified by this set | `all[eq ai_high_risk yes, eq ai_role provider, eq ai_annex_iv_7_applicable yes]` | `model-description`, `verification-records` | `II-4` | informative | The MDR requirements-compliance record may contextualize solutions, but no particular standards are named or treated as equivalent. |
| `IV-8` | EU declaration of conformity | Where the relevant declaration exists | `all[eq ai_high_risk yes, eq ai_role provider, eq ai_annex_iv_8_applicable yes]` | `conformity-declaration` | `none` | `none` | The declaration is a separate AI Act deliverable and has no direct selected MDR Annex II clause. |
| `IV-9` | Post-market performance evaluation system and monitoring plan | As applicable to the relevant system | `all[eq ai_high_risk yes, eq ai_role provider, eq ai_annex_iv_9_applicable yes]` | `post-market-monitoring-plan` | `II-4` | informative | MDR general requirements provide product-safety context, not an equivalent AI post-market performance plan. |

The `ai_annex_iv_<point>_applicable` dimensions are person-supplied yes/no values. Each point can therefore resolve independently to binding, not_binding, or unresolved without inferring system features. For `IV-7`, the set records the documentation category without naming, numbering, quoting, or paraphrasing any harmonised standard, standardisation-request deliverable, or other paywalled standard. `IV-8` has no direct Annex II counterpart because the MDR declaration is defined separately from its Annex II technical-documentation contents.

## Security-Analysis Skill Disposition

For PLAT-1628, retain `skills/spec-security-analysis/references/gdpr/ChII-Principles.md`, `ChIII-DataSubjectRights.md`, and `ChV-DataTransfers.md` as clearly labeled untyped context until future clause sets cover those chapters. Do not delete their summaries or treat them as evaluated clauses. Modify `skills/spec-security-analysis/references/gdpr/ChIV-ControllerProcessor.md` to replace the covered Article 25, 30, 32, and 35 summaries with links to `eu/gdpr-2016-679@2016-05-04`. Modify `skills/spec-security-analysis/references/gdpr/index.md`, `skills/spec-security-analysis/SKILL.md`, and `skills/spec-security-analysis/references/standards-index.md` to link the set and state the uncovered-topic boundary. These are the complete affected Quoin files; no other GDPR reference files are to be deleted or modified for this set.

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
| data-lineage | record | Provenance, selection, preparation and transformations for data used by the AI system. |
| model-description | document | Original description of AI system purpose, version, behavior, limits and use. |
| event-logging-design | record | Declared events, retention and access controls for AI system logs. |
| human-oversight-design | record | Human oversight roles, measures, competence and output-interpretation controls. |
| post-market-monitoring-plan | document | Provider plan and evidence for post-market performance monitoring. |
| conformity-declaration | document | EU declaration of conformity and its controlled reference. |

A clause whose expected outputs are all procedures is customer-owned and requires a delegated disposition with rationale and customer approval reference, never a direct fact. `tests/corpus/` is synthetic; every synthetic ID and evidence reference uses `example.invalid`, and discharge facts are written to a temporary store.

## Requirements Architecture

FR-001 through FR-015 define module home, rights, MDR, MDCG and GDPR clauses and applicability, crosswalks, catalog, customer-owned obligations, skill mapping, and corpus. FR-016 through FR-022 define the AI Act sets, provider/deployer obligations, Annex IV table, human decision evidence, MDR crosswalks and application date. NFR-001 defines the general licensing and standards boundary; NFR-002 defines the GDPR-specific source and original-expression boundary; NFR-003 defines the AI Act source and standards boundary. StR-001 records the manufacturer's need for reviewable evidence; US-001 describes the human review outcome. All functional requirements trace to US-001.

Dependency graph (an edge A → B means A depends on B): FR-003 → FR-001, FR-002, FR-006; FR-004 → FR-003; FR-005 → FR-001, FR-002, FR-003, FR-006; FR-006 → FR-001; FR-007 → FR-006; FR-008 → FR-001, FR-003, FR-004, FR-005, FR-006, FR-007; FR-009 → FR-001, FR-002, FR-006; FR-010 → FR-009; FR-011 → FR-010; FR-012 → FR-010, FR-011; FR-013 → FR-010, FR-011; FR-014 → FR-010; FR-015 → FR-009, FR-010; FR-016 → FR-001, FR-002; FR-017 → FR-016, FR-006; FR-018 → FR-016, FR-006; FR-019 → FR-017, FR-018; FR-020 → FR-017, FR-018; FR-021 → FR-018, FR-003; FR-022 → FR-016. NFR-001 constrains FR-001 through FR-022; NFR-002 constrains FR-009 through FR-015; NFR-003 constrains FR-016 through FR-022.

## Upstream Contracts

The module uses existing `clause-set-v1`, `clause_sets`, `quire clauses evaluate`, `quire publish-check`, `quoin evidence record-discharge`, and `quoin discharge --rmm`. No engine change is specified.

## References

- EUR-Lex current consolidated MDR text consulted: `https://eur-lex.europa.eu/eli/reg/2017/745/2026-07-19/eng`.
- EUR-Lex legal notice: `https://eur-lex.europa.eu/content/legal-notice/legal-notice.html?locale=en`.
- MDCG 2019-16 rev.1 official PDF: `https://health.ec.europa.eu/document/download/b23b362f-8a56-434c-922a-5b3ca4d0a7a1_en?filename=md_cybersecurity_en.pdf`.
- Commission MDCG listing: `https://health.ec.europa.eu/medical-devices-sector/new-regulations/guidance-mdcg-endorsed-documents-and-other-guidance_en`.
- EUR-Lex current consolidated GDPR text consulted: `https://eur-lex.europa.eu/eli/reg/2016/679/2016-05-04/eng`.
- EUR-Lex legal notice on reuse and attribution: `https://eur-lex.europa.eu/content/legal-notice/legal-notice.html?locale=en`.
- EUR-Lex consolidated AI Act text consulted: `https://eur-lex.europa.eu/eli/reg/2024/1689/2026-07-27/eng`.
- EUR-Lex legal notice on reuse and attribution: `https://eur-lex.europa.eu/content/legal-notice/legal-notice.html?locale=en`.
