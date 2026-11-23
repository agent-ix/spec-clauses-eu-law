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

This specification defines the clause-only EU-law module and its sets for software-related requirements from Regulation (EU) 2017/745 (MDR), interpretive cybersecurity guidance from MDCG 2019-16 rev.1, selected obligations in Regulation (EU) 2016/679 (GDPR), selected high-risk AI obligations and technical-documentation elements in Regulation (EU) 2024/1689 (AI Act), and the EU GMP guideline Annex 11 on computerised systems (EudraLex Volume 4). Clause summaries use original expression and link to official sources. The pack records evidence and produces an RMM; it does not determine legal compliance.

## Scope

### In Scope

- Repository `agent-ix/spec-clauses-eu-law`, Python package `spec_clauses_eu_law`, module `clause_sets`.
- MDR set `eu/mdr-2017-745@2026-07-19`, MDCG set `eu-mdcg/mdcg-2019-16@rev1`, GDPR set `eu/gdpr-2016-679@2016-05-04`, and AI Act sets `eu/ai-act-2024-1689@2026-07-27` and `eu/ai-act-2024-1689-annex-iv@2026-07-27`.
- Annex 11 set `eu/eu-gmp-annex-11@2011-01`: every numbered paragraph of the January 2011 Annex 11, person-supplied scope dimensions, Part 11 crosswalks to `us-fda/21-cfr-11@2026-11-12`, and output bindings stating which tool command produces each expected output or that the customer supplies it.
- Set identities, sources, rights metadata, clause identifiers, applicability, expected outputs, MDCG-to-MDR and GDPR-to-NIST/HIPAA crosswalks, shared output catalog, customer-owned obligations, and synthetic reference corpus rules.
- GDPR Articles 25, 30, 32 and 35; the person-supplied controller/processor, high-risk-processing, and Article 30(5) applicability values; human approval for DPIA residual-risk acceptance; and the security-analysis skill's coverage boundary for GDPR material.
- AI Act high-risk provider obligations in Articles 9–20, 43, 47, 72 and 73; deployer obligations in Article 26; Annex IV technical-documentation elements; person-supplied high-risk, operator-role and per-point applicability values; and crosswalks to MDR Annex II.

### Out of Scope

- Clause JSON/content, package manifest, corpus, implementation tests, CI, publish gate, output bindings, and scaffold beyond this specification (PLAT-1425, PLAT-1623, PLAT-1624, PLAT-1626).
- GDPR Articles outside 25, 30, 32 and 35, including data-subject rights, international transfers, and breach notifications under Articles 33 and 34; AI Act provisions outside the selected high-risk provider/deployer duties and Annex IV, including prohibited practices, general-purpose AI models and fundamental-rights impact assessments; engine changes; legal advice or compliance determinations.
- The 2025 consultation drafts of a revised Annex 11, a revised Chapter 4 and a new Annex 22; none is in force, and none is specified here. The Chapter 4 in force is not part of this set.
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
| I-14.2(d) | always | it-requirements-statement, security-risk-records |
| I-17.1 | always | software-requirements, software-architecture, verification-records |
| I-17.2 | always | software-requirements, software-architecture, security-risk-records, verification-records |
| I-17.3 | eq mobile_platform yes | software-requirements, software-architecture, verification-records |
| I-17.4 | always | it-requirements-statement, security-risk-records |
| I-18.8 | always | security-risk-records, verification-records |
| I-23.4(ab) | always | it-requirements-statement |
| II-1.1 | always | software-requirements, software-architecture |
| II-4 | always | software-requirements, software-architecture, verification-records |
| II-5 | always | risk-management-records, software-requirements, verification-records, security-risk-records |
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
| `art-30(4)` | `eq article_30_records_applicability applies` | `records-of-processing`, `written-procedure` |
| `art-32(1)(a)` | always | `security-risk-records`, `verification-records` |
| `art-32(1)(b)` | always | `security-risk-records`, `verification-records` |
| `art-32(1)(c)` | always | `security-risk-records`, `verification-records`, `backup-restore-record` |
| `art-32(1)(d)` | always | `security-risk-records`, `verification-records` |
| `art-32(2)` | always | `security-risk-records` |
| `art-32(4)` | always | `processing-access-control`, `written-procedure`, `training-record` |
| `art-35(1)` | `all[eq gdpr_role controller, eq high_risk_processing yes]` | `dpia`, `data-flow-model`, `security-risk-records` |
| `art-35(2)` | `all[eq gdpr_role controller, eq high_risk_processing yes]` | `dpia`, `data-flow-model` |
| `art-35(7)(a)` | `all[eq gdpr_role controller, eq high_risk_processing yes]` | `dpia`, `data-flow-model` |
| `art-35(7)(b)` | `all[eq gdpr_role controller, eq high_risk_processing yes]` | `dpia`, `security-risk-records` |
| `art-35(7)(c)` | `all[eq gdpr_role controller, eq high_risk_processing yes]` | `dpia`, `data-flow-model`, `privacy-by-default-settings` |
| `art-35(7)(d)` | `all[eq gdpr_role controller, eq high_risk_processing yes]` | `dpia`, `security-risk-records` |
| `art-35(9)` | `all[eq gdpr_role controller, eq high_risk_processing yes]` | `dpia` |
| `art-35(11)` | `all[eq gdpr_role controller, eq high_risk_processing yes]` | `dpia`, `data-flow-model`, `security-risk-records` |

Articles 25(3) and 32(3) are not clauses because they describe optional ways to demonstrate compliance. Article 30(5)'s exemption decision is represented by the person-supplied `article_30_records_applicability` value; a medical-product context or assumed health-data use is not enough to resolve it. Article 30(3) and (4) explicitly inherit this value because they concern records required under paragraphs 1 and 2. Article 35(3) and (4) are triggers rather than separate clauses; paragraphs (5) and (6) are supervisory-authority duties; paragraph (8) is conditional on a code-of-conduct circumstance not represented by the selected dimensions; paragraph (10) is an exception dependent on external legal-basis and prior-assessment facts. Those Article 35 paragraphs are identified as coverage limits and are not evaluated by this set. Any residual-risk decision associated with a DPIA remains with a named person.

GDPR output bindings state what produces each output. `records-of-processing` is produced by `quoin dossier generate --doc records-of-processing` from the declared data-flow model, with explicit GAP lines where the model lacks a field; making the record available to a supervisory authority on request (Article 30(4)) is the controller's or processor's own procedure, so `art-30(4)` also names `written-procedure`. `privacy-by-default-settings` and `processing-access-control` have no toolchain producer: the customer supplies them, and the pack never marks them as produced. `processing-access-control` describes the product's processing system (who may process personal data, on whose instructions); the repository permission and branch-rule settings in `access-control` describe the development repository, so the GDPR set does not contain `access-control` and no GDPR clause names it. `art-32(1)(c)` also names `backup-restore-record`, the customer-owned evidence that backups are taken and restoration is checked, because the tool's records and test results do not show that restoration works. `dpia` is authored by people. For the Article 35 clauses, quoin decides discharge: a direct fact on an approval-role clause needs a non-blank `approvalRef` (quoin FR-208) that engineering-assurance verifies as an approval by the named role (quoin FR-211). The pack carries `approvalRoles` and does not check approvals itself.

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
| `art-20` | Corrective action and authority notification | `all[eq ai_high_risk yes, eq ai_role provider]` | mandatory | `written-procedure` |
| `art-26` | Deployer use, oversight, monitoring and incident duties | `all[eq ai_high_risk yes, eq ai_role deployer]` | mandatory | `human-oversight-design`, `written-procedure`, `event-logging-design` |
| `art-43` | Conformity-assessment route | `all[eq ai_high_risk yes, eq ai_role provider]` | mandatory | `conformity-declaration`, `verification-records` |
| `art-47` | EU declaration of conformity | `all[eq ai_high_risk yes, eq ai_role provider]` | mandatory | `conformity-declaration` |
| `art-72` | Post-market monitoring system and plan | `all[eq ai_high_risk yes, eq ai_role provider]` | mandatory | `post-market-monitoring-plan`, `event-logging-design` |
| `art-73` | Serious-incident reporting | `all[eq ai_high_risk yes, eq ai_role provider]` | mandatory | `written-procedure` |

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
| `IV-1(f)` | Product component illustrations, external features, markings and layout | Only where the AI system is a component of a product | `all[eq ai_high_risk yes, eq ai_role provider, eq ai_annex_iv_1_f_applicable yes]` | `software-architecture` | `II-1.1` | partial | MDR device description identifies the device and its software components, while this point covers the AI component's visible placement in a product. |
| `IV-1(g)` | Basic description of the deployer-facing interface | As applicable to the relevant system | `all[eq ai_high_risk yes, eq ai_role provider, eq ai_annex_iv_1_g_applicable yes]` | `model-description` | `none` | `none` | The selected MDR software clauses do not directly cover the AI deployer interface description. |
| `IV-1(h)` | Instructions for use and applicable interface description | Interface description where applicable; as applicable to the relevant system | `all[eq ai_high_risk yes, eq ai_role provider, eq ai_annex_iv_1_h_applicable yes]` | `model-description`, `written-procedure` | `none` | `none` | The selected MDR software clauses do not directly cover these AI-specific deployer instructions. |
| `IV-2(a)` | Development methods and steps | Third-party or pre-trained tools where relevant; as applicable to the relevant system | `all[eq ai_high_risk yes, eq ai_role provider, eq ai_annex_iv_2_a_applicable yes]` | `software-architecture`, `verification-records` | `none` | `none` | The selected MDR software clauses do not directly cover the AI development-process record. |
| `IV-2(b)` | Design specifications, logic, assumptions and classification choices | As applicable to the relevant system | `all[eq ai_high_risk yes, eq ai_role provider, eq ai_annex_iv_2_b_applicable yes]` | `model-description`, `software-architecture` | `II-1.1` | informative | MDR device description provides context for the AI design record without covering its internal logic or classification choices. |
| `IV-2(c)` | Architecture, component integration and computational resources | As applicable to the relevant system | `all[eq ai_high_risk yes, eq ai_role provider, eq ai_annex_iv_2_c_applicable yes]` | `software-architecture` | `II-1.1` | partial | The MDR device description informs system architecture while the AI point adds model and computational-resource detail. |
| `IV-2(d)` | Data requirements, provenance, selection and preparation | Only where relevant to the system | `all[eq ai_high_risk yes, eq ai_role provider, eq ai_annex_iv_2_d_applicable yes]` | `data-lineage` | `none` | `none` | No selected MDR Annex II software clause directly specifies AI training-data governance documentation. |
| `IV-2(e)` | Human-oversight assessment and output-interpretation measures | Measures needed for the system | `all[eq ai_high_risk yes, eq ai_role provider, eq ai_annex_iv_2_e_applicable yes]` | `human-oversight-design` | `none` | `none` | The selected MDR software clauses do not directly impose the AI Act human-oversight documentation element. |
| `IV-2(f)` | Predetermined system changes and continuous-conformity measures | Only where predetermined changes apply | `all[eq ai_high_risk yes, eq ai_role provider, eq ai_annex_iv_2_f_applicable yes]` | `release-record`, `verification-records` | `none` | `none` | The selected MDR software clauses do not directly cover this AI-specific change-control description. |
| `IV-2(g)` | Validation and test procedures, data, metrics, logs and reports | As applicable to the relevant system | `all[eq ai_high_risk yes, eq ai_role provider, eq ai_annex_iv_2_g_applicable yes]` | `verification-records` | `II-6.1(b)` | partial | MDR software validation evidence overlaps, but does not cover the full AI validation and reporting detail. |
| `IV-2(h)` | Cybersecurity measures | As applicable to the relevant system | `all[eq ai_high_risk yes, eq ai_role provider, eq ai_annex_iv_2_h_applicable yes]` | `security-risk-records`, `verification-records` | `II-4` | partial | The MDR requirements-compliance record shows how the applicable security-related requirements are addressed, while this point describes the AI system's own cybersecurity measures. |
| `IV-3` | Capabilities, limitations, risks, oversight and input specifications | Specifications and measures applicable to the relevant system | `all[eq ai_high_risk yes, eq ai_role provider, eq ai_annex_iv_3_applicable yes]` | `model-description`, `human-oversight-design`, `security-risk-records` | `II-1.1` | partial | Device description provides context, but does not cover all AI performance, oversight and input details. |
| `IV-4` | Suitability of performance metrics for the system | As applicable to the relevant system | `all[eq ai_high_risk yes, eq ai_role provider, eq ai_annex_iv_4_applicable yes]` | `verification-records` | `II-6.1(b)` | partial | MDR software validation metrics overlap, but the AI point adds metric suitability for the AI system. |
| `IV-5` | Risk-management system | As applicable to the relevant system | `all[eq ai_high_risk yes, eq ai_role provider, eq ai_annex_iv_5_applicable yes]` | `risk-management-records` | `II-5` | partial | MDR benefit-risk and risk-management evidence overlaps with the AI risk system without establishing equivalence. |
| `IV-6` | Relevant lifecycle changes | Changes made by the provider through the system lifecycle | `all[eq ai_high_risk yes, eq ai_role provider, eq ai_annex_iv_6_applicable yes]` | `release-record` | `none` | `none` | The selected MDR software clauses do not directly cover the complete AI lifecycle-change description. |
| `IV-7` | Applied standards or other solutions used to meet requirements | Applicable solutions; no particular standard is identified by this set | `all[eq ai_high_risk yes, eq ai_role provider, eq ai_annex_iv_7_applicable yes]` | `model-description`, `verification-records` | `II-4` | informative | The MDR requirements-compliance record may contextualize solutions, but no particular standards are named or treated as equivalent. |
| `IV-8` | EU declaration of conformity | Where the relevant declaration exists | `all[eq ai_high_risk yes, eq ai_role provider, eq ai_annex_iv_8_applicable yes]` | `conformity-declaration` | `none` | `none` | The declaration is a separate AI Act deliverable and has no direct selected MDR Annex II clause. |
| `IV-9` | Post-market performance evaluation system and monitoring plan | As applicable to the relevant system | `all[eq ai_high_risk yes, eq ai_role provider, eq ai_annex_iv_9_applicable yes]` | `post-market-monitoring-plan` | `none` | `none` | The selected MDR software clauses contain no post-market monitoring counterpart in Annex II. |

The `ai_annex_iv_<point>_applicable` dimensions are person-supplied yes/no values. Each point can therefore resolve independently to binding, not_binding, or unresolved without inferring system features. For `IV-7`, the set records the documentation category without naming, numbering, quoting, or paraphrasing any harmonised standard, standardisation-request deliverable, or other paywalled standard. `IV-8` has no direct Annex II counterpart because the MDR declaration is defined separately from its Annex II technical-documentation contents.

## Annex 11 Set Design

The Annex 11 set uses authority `eu`, ID `eu-gmp-annex-11`, and version `2011-01`. The source is EudraLex Volume 4, Annex 11 "Computerised Systems", the January 2011 revision published by the European Commission, which the Commission's Volume 4 page lists as the current Annex 11. The official document URL is `https://health.ec.europa.eu/document/download/8d305550-dd22-4dad-8463-2ddb4a1345f1_en?filename=annex11_01-2011_en.pdf` and the listing page is `https://health.ec.europa.eu/medicinal-products/eudralex/eudralex-volume-4_en`. The version string is the year and month of the revision in force. A draft revision of Annex 11 was published for stakeholder consultation in July 2025 with comments due 7 October 2025; it is a draft, not in force, and this set does not specify it. If the Commission adopts a revised Annex 11, the adopted text is a new set version named by its own revision date, and the `2011-01` set stays unchanged for systems still assessed against the 2011 text.

Rights are `structure: citation_only`, `text: original`, and `clearance_ref: null`. Licence metadata says exactly: `European Commission documents may be reused under the Commission reuse policy (Decision 2011/833/EU); the Commission legal notice (https://commission.europa.eu/legal-notice_en) licenses Commission content under CC BY 4.0 with attribution. The Annex 11 document carries no licence statement of its own. This set reproduces no Annex 11 text.` Attribution says `© European Union. Source: <{official document URL}>. Original summaries; changes made.` The set reproduces no Annex 11 sentence, so it does not depend on the reuse licence for any copied text.

Annex 11 is part of the EU GMP guidelines, which interpret the binding GMP requirements; its wording is "should". All clauses are therefore `recommended`. The module does not say whether a system complies with the underlying GMP law.

Clause IDs are the Annex 11 paragraph numbers: `1`, `2`, `3.1`, `4.3`, `12.4`, and `14(a)`. The Principle statement is not a clause. IDs contain no slash. The person supplies every applicability dimension; the tool never infers one from the product, the data, or a risk score. Dimensions each have values `yes` and `no`: `gmp_regulated_use` (the system is used in GMP-regulated activity), `third_party_supplier`, `custom_or_customised`, `data_exchange` (data exchanged electronically with other systems), `data_migration`, `manual_critical_entry`, `batch_release_records`, `electronic_signature_use`, `batch_certification_in_system`, `critical_process_support`, and `data_archived`. Every clause requires `eq gmp_regulated_use yes`; a clause with a second dimension requires `all[eq gmp_regulated_use yes, eq <dimension> yes]`. A `no` value makes the clause not binding; a missing value leaves it unresolved. The risk-scaled paragraphs carry `approvalRoles: [system-owner]`. Annex 11 paragraph 2 names the system owner, with the process owner, as the person responsible for the system, so these decisions are the system owner's. Quoin decides discharge: a fact on an approval-role clause needs a non-blank `approvalRef` (quoin FR-208) that engineering-assurance verifies as a signed tag whose meaning equals an approval role (quoin FR-211). Whether a system, process, entry or datum is critical, and how the risk-scaled paragraphs (1, 3.2, 4.1, 4.3, 4.4, 6, 9, 12.2, 13, 16) are scaled, are human decisions the pack records but never makes.

## Annex 11 Clause Table

The table is normative for clause IDs, force, applicability and expected outputs. All clauses are `recommended`. `all[...]` denotes the engine's `all` expression, and `D` means the clause also requires `eq <dimension> yes`.

| Clause ID | Subject (original summary) | Applicability | Expected outputs |
|---|---|---|---|
| `1` | Risk management across the system lifecycle, covering patient safety, data integrity and product quality | gmp_regulated_use | `risk-management-records`, `written-procedure` |
| `2` | Close cooperation and suitable training and access for all people involved | gmp_regulated_use | `written-procedure`, `training-record` |
| `3.1` | Formal agreement with a third party that provides or supports the system | D third_party_supplier | `supplier-agreement` |
| `3.2` | Supplier competence and reliability weigh heavily in selection | D third_party_supplier | `supplier-assessment` |
| `3.3` | Documentation and quality information of off-the-shelf products is assessed | D third_party_supplier | `soup-list`, `supplier-assessment` |
| `3.4` | Inspectors can obtain the supplier's quality-system and audit information when they ask | D third_party_supplier | `supplier-assessment` |
| `4.1` | Validation documentation covers the lifecycle and is justified by risk | gmp_regulated_use | `system-validation`, `verification-records` |
| `4.2` | Validation documentation includes change-control and deviation records | gmp_regulated_use | `change-assurance-record`, `anomaly-list` |
| `4.3` | Current inventory of GMP systems; critical systems also have a system description | gmp_regulated_use | `system-inventory`, `software-architecture`, `data-flow-model` |
| `4.4` | Traceable user requirements based on GMP impact and risk | gmp_regulated_use | `software-requirements` |
| `4.5` | The system is developed under a quality management system and the supplier is assessed | D third_party_supplier | `supplier-assessment`, `written-procedure` |
| `4.6` | Custom or customised systems have formal assessment of quality and performance measures at each lifecycle stage | D custom_or_customised | `verification-records`, `system-validation` |
| `4.7` | Evidence of suitable test methods, scenarios, limits, error handling, and adequate test tools and environments | gmp_regulated_use | `verification-records`, `system-validation` |
| `4.8` | Data migrated to another format or system is checked for unchanged value and meaning | D data_migration | `verification-records`, `system-validation` |
| `5` | Electronic data exchange has built-in checks for correct and secure entry and processing | D data_exchange | `data-flow-model`, `verification-records` |
| `6` | Manually entered critical data has an additional accuracy check, with risk considered | D manual_critical_entry | `written-procedure`, `verification-records` |
| `7.1` | Data is protected physically and electronically, remains accessible, readable and accurate through retention | gmp_regulated_use | `access-control`, `signed-record`, `written-procedure` |
| `7.2` | Regular backups, with integrity, accuracy and restorability checked in validation and periodically | gmp_regulated_use | `backup-restore-record`, `written-procedure` |
| `8.1` | Clear printed copies of stored electronic data can be obtained | gmp_regulated_use | `record-export` |
| `8.2` | Batch-release supporting records can be printed showing whether data changed since first entry | D batch_release_records | `record-export`, `audit-trail` |
| `9` | Risk-based audit trail of GMP-relevant changes and deletions, with reasons, readable and regularly reviewed | gmp_regulated_use | `audit-trail`, `approval-trail`, `written-procedure` |
| `10` | Changes and configuration changes only under a defined, controlled procedure | gmp_regulated_use | `change-assurance-record`, `baseline-record`, `written-procedure` |
| `11` | Periodic evaluation confirms the system stays validated and GMP-compliant | gmp_regulated_use | `periodic-evaluation-record` |
| `12.1` | Physical or logical controls limit access to authorised people | gmp_regulated_use | `system-access-control`, `written-procedure` |
| `12.2` | How strong the security controls are depends on how critical the system is | gmp_regulated_use | `security-risk-records`, `system-access-control` |
| `12.3` | Creating, changing and cancelling access authorisations is recorded | gmp_regulated_use | `access-control`, `signer-registry`, `audit-trail` |
| `12.4` | Systems record who entered, changed, confirmed or deleted data, with date and time | gmp_regulated_use | `audit-trail`, `approval-trail`, `signer-registry` |
| `13` | Incidents are reported and assessed; critical incidents get root cause and corrective and preventive action | gmp_regulated_use | `anomaly-list`, `written-procedure` |
| `14(a)` | Within the company an electronic signature has the same standing as a handwritten one | D electronic_signature_use | `signature-meaning`, `signer-registry`, `written-procedure` |
| `14(b)` | A signature stays bound to the record it signs and cannot be detached | D electronic_signature_use | `signed-record`, `approval-trail` |
| `14(c)` | A signature shows when it was applied | D electronic_signature_use | `signed-record`, `approval-trail` |
| `15` | A system used for batch certification lets only Qualified Persons certify and records who did | D batch_certification_in_system | `batch-certification-record`, `written-procedure` |
| `16` | Continuity arrangements for systems supporting critical processes, documented and tested | D critical_process_support | `business-continuity-plan` |
| `17` | Archived data is periodically confirmed to be reachable, legible and intact, and retrieval is retested when equipment or programs change | D data_archived | `archive-verification-record`, `written-procedure` |

A clause whose expected outputs are all procedures is customer-owned: `2`, `3.1`, `3.2`, `3.4`, `4.5`, `7.2`, `11`, `15`, `16` and `17`.

## Annex 11 Clause Titles and Subjects

Each clause carries the title and subject tags below. They label the clause for readers and selection; no applicability expression reads them.

| Clause ID | Title | Subjects |
|---|---|---|
| `1` | Risk management | `risk` |
| `2` | Personnel | `personnel` |
| `3.1` | Supplier agreement | `suppliers` |
| `3.2` | Supplier competence | `suppliers` |
| `3.3` | Off-the-shelf product assessment | `suppliers` |
| `3.4` | Supplier information for inspectors | `suppliers` |
| `4.1` | Validation documentation | `validation` |
| `4.2` | Validation change and deviation records | `validation` |
| `4.3` | System inventory and description | `validation` |
| `4.4` | User requirements | `validation` |
| `4.5` | Development quality system | `validation` |
| `4.6` | Custom system assessment | `validation` |
| `4.7` | Testing evidence | `validation` |
| `4.8` | Data migration checks | `validation` |
| `5` | Data exchange checks | `data-exchange` |
| `6` | Accuracy checks | `data-accuracy` |
| `7.1` | Data protection and retention | `data-storage` |
| `7.2` | Backup and restore | `data-storage` |
| `8.1` | Printed copies | `printouts` |
| `8.2` | Release printouts and data changes | `printouts` |
| `9` | Audit trail | `audit-trail` |
| `10` | Change and configuration management | `change-control` |
| `11` | Periodic evaluation | `periodic-evaluation` |
| `12.1` | Access restriction | `security` |
| `12.2` | Security control extent | `security` |
| `12.3` | Access authorisation records | `security` |
| `12.4` | Operator identity records | `security` |
| `13` | Incident management | `incidents` |
| `14(a)` | Signature standing | `electronic-signature` |
| `14(b)` | Signature linking | `electronic-signature` |
| `14(c)` | Signature time | `electronic-signature` |
| `15` | Batch certification | `batch-certification` |
| `16` | Business continuity | `continuity` |
| `17` | Archiving | `archiving` |

## Annex 11 Output Bindings

Expected outputs that already exist in the US Health-Law Output Catalog (`audit-trail`, `approval-trail`, `signed-record`, `signature-meaning`, `signer-registry`, `access-control`, `system-validation`, `written-procedure`, `training-record`, `verification-records`, `risk-management-records`, `software-requirements`, `software-architecture`, `soup-list`, `security-risk-records`, `anomaly-list`) keep that catalog's kind and description exactly; their tool limits travel in the Annex 11 clause text (see Annex 11 Tool Limits). A binding below states the command that produces the output today; "customer-supplied" means no quoin, quire or engineering-assurance command produces it, and the person supplies it. The pack never marks a customer-supplied output as produced.

| Output | Producer command | Source and authoring | Limit stated |
|---|---|---|---|
| `audit-trail`, `approval-trail` | `engineering-assurance approval-trail` | Git history | Deleted tags are invisible; no reason-for-change field exists for every change, so paragraph 9 reasons stay a customer procedure |
| `signed-record`, `signature-meaning` | `engineering-assurance signature-verify`, `engineering-assurance approval-verify` | Signed commits and tags | The signing time is the signer's own claim, neither attested nor checked |
| `signer-registry` | none | Allowed-signers file the customer authors; read by `approval-trail` and `signature-verify` | It has no audit trail beyond git |
| `change-assurance-record` | `quoin change-assurance write-record` | Explicit inputs from the producer | Records attribution only; it does not establish authorisation |
| `baseline-record` | `quire validate` | Engineering-assurance `Baseline` artifact authored by a person and read by `release-verify` | A person decides its contents |
| `verification-records` | `quoin matrix`, `quoin evidence record` | Suite run results | Reports what ran; does not judge adequacy |
| `software-requirements`, `software-architecture`, `data-flow-model` | `quire validate` | Spec artifacts authored by people | None |
| `security-risk-records` | `quire validate` | Security artifacts authored by people | Risk acceptance is a person's decision |
| `risk-management-records` | `quoin risk-summary` | Safety artifacts authored by people | Risk acceptance is a person's decision |
| `soup-list` | `quoin soup report` | SBOM components | Supplier assessment stays with the customer |
| `anomaly-list` | `quoin anomaly check`, `quoin anomaly report` | Anomaly documents authored by people | Anomaly content is a person's assessment |
| `record-export` | `quoin matrix`, `engineering-assurance approval-trail`, `quoin evidence audit` | Retained records | No printout shows a record's change history since first entry |
| `system-validation` | none | Customer-supplied | No command produces validation evidence |
| `access-control` | none | Customer-supplied | No command reads repository permissions |
| `system-access-control` | none | Customer-supplied | No command reads or checks who may access the computerised system |
| `written-procedure`, `training-record` | none | Customer-supplied | The customer owns and supplies the record |
| `supplier-agreement`, `supplier-assessment`, `system-inventory`, `backup-restore-record`, `periodic-evaluation-record`, `business-continuity-plan`, `archive-verification-record`, `batch-certification-record` | none | Customer-supplied | No backup or restore check, periodic evaluation, or archive re-verification after a signer or system change exists |

## Annex 11 Tool Limits

Descriptions of names shared with the US Health-Law Output Catalog are canonical and cannot carry Annex 11 limits. For each shared output that has a limit other than `None` in the Annex 11 Output Bindings table, whether or not a command produces it, the limit travels in the `text` of every Annex 11 clause whose expected outputs include that output, as a closing sentence beginning "Tool limit:". A clause binding several such outputs ends with each distinct sentence once. Names used only by Annex 11 carry their limit in their own catalog description.

| Output | Tool limit sentence |
|---|---|
| `audit-trail`, `approval-trail` | Tool limit: deleted tags are invisible, and no reason-for-change field exists for every change. |
| `signed-record`, `signature-meaning` | Tool limit: the signing time is the signer's own claim, neither attested nor checked. |
| `signer-registry` | Tool limit: the allowed-signers registry has no audit trail beyond git. |
| `verification-records` | Tool limit: the matrix and evidence report what ran and do not judge whether it is adequate. |
| `risk-management-records`, `security-risk-records` | Tool limit: accepting a risk is a person's decision. |
| `soup-list` | Tool limit: assessing the supplier stays with the customer. |
| `anomaly-list` | Tool limit: an anomaly's content is a person's assessment. |
| `system-validation` | Tool limit: no command produces validation evidence; the customer supplies it. |
| `access-control` | Tool limit: no command reads repository permissions; the customer supplies them. |
| `written-procedure`, `training-record` | Tool limit: the customer owns and supplies this record. |

## Annex 11 Part 11 Crosswalk Policy

Selected Annex 11 clauses crosswalk to `us-fda/21-cfr-11@2026-11-12` in `spec-clauses-us-health`. The target module is a test-time dependency and is never copied into this module. Relations are `partial` or `informative`; they never assert equivalence and never discharge the source clause. Every target resolves in the installed target module. Rationales use original wording that states the limited overlap.

| Source clause | Part 11 targets | Relation |
|---|---|---|
| `2` | `11.10(i)` | `partial` |
| `4.1` | `11.10(a)` | `partial` |
| `4.7` | `11.10(a)` | `partial` |
| `5` | `11.10(h)` | `informative` |
| `7.1` | `11.10(c)` | `partial` |
| `8.1` | `11.10(b)` | `partial` |
| `8.2` | `11.10(b)` | `informative` |
| `9` | `11.10(e)` | `partial` |
| `10` | `11.10(k)` | `partial` |
| `12.1` | `11.10(d)` | `partial` |
| `12.1` | `11.10(g)` | `partial` |
| `12.3` | `11.10(d)` | `informative` |
| `12.4` | `11.10(e)` | `partial` |
| `14(a)` | `11.10(j)` | `partial` |
| `14(a)` | `11.100(c)` | `informative` |
| `14(b)` | `11.70` | `partial` |
| `14(c)` | `11.50(a)` | `partial` |
| `17` | `11.10(c)` | `informative` |

## Security-Analysis Skill Disposition

For PLAT-1628, retain `skills/spec-security-analysis/references/gdpr/ChII-Principles.md`, `ChIII-DataSubjectRights.md`, and `ChV-DataTransfers.md` as clearly labeled untyped context until future clause sets cover those chapters. Do not delete their summaries or treat them as evaluated clauses. Modify `skills/spec-security-analysis/references/gdpr/ChIV-ControllerProcessor.md` to replace the covered Article 25, 30, 32, and 35 summaries with links to `eu/gdpr-2016-679@2016-05-04`. Modify `skills/spec-security-analysis/references/gdpr/index.md`, `skills/spec-security-analysis/SKILL.md`, and `skills/spec-security-analysis/references/standards-index.md` to link the set and state the uncovered-topic boundary. These are the complete affected Quoin files; no other GDPR reference files are to be deleted or modified for this set.

## Article 32 Crosswalk Policy

Crosswalks cover every Article 32 clause present in the GDPR Clause Table: `art-32(1)(a)`, `art-32(1)(b)`, `art-32(1)(c)`, `art-32(1)(d)`, `art-32(2)`, and `art-32(4)`. `art-32(3)` is not a clause in this set and has no crosswalk. Each listed source clause has at least one target in both `nist/sp800-53@5.2.0` in `spec-objects-security` and `us-hhs/45-cfr-164-subpart-c@2026-11-12` in `spec-clauses-us-health`. These target modules are test-time dependencies and are never copied into this module. Relations are `partial` or `informative`; they never assert equivalence or automatically discharge the source obligation. Every target set and clause identifier must resolve in the installed target module. Rationales use original wording to explain the limited scope of each mapping, not restate target text.

For `art-32(4)`, the planned mappings are:

| Source clause | Target set | Target clause | Relation | Original rationale |
|---|---|---|---|---|
| `art-32(4)` | `nist/sp800-53@5.2.0` | `AC-6` | `partial` | Least-privilege access restrictions can limit a person's or process's access, but they do not establish that processing follows the controller's or processor's instructions. |
| `art-32(4)` | `us-hhs/45-cfr-164-subpart-c@2026-11-12` | `164.308(a)(4)(i)` | `partial` | Access-authorization policies address the authorization boundary for access, but they do not establish instruction-bound processing or cover personal data beyond the HIPAA scope. |

The mappings are informative evidence of related control scope only. Neither target establishes the full Article 32(4) obligation, and neither mapping discharges it automatically.

## MDCG Companion Table

The pack includes only the substantive software and cybersecurity sections 2.1–2.6, 3.1–3.8, 4.1–4.3, and 5.1–5.2 from the official table of contents. Section 1 (introduction and abbreviations), section 6 (other Union legislation and guidance), and Annexes I–IV are outside this set; the annex material that identifies standards is excluded. Subsections 2.6.1–2.6.3 are included within section 2.6, not separate clause IDs. Every included section is recommended, not mandatory. The source table of contents contains no section 5.3. Crosswalk relations use `partial` when the MDCG section gives cybersecurity/software detail that addresses only part of the cited MDR clause, and `informative` when it supplies context without asserting equivalent coverage. Targets resolve against the loaded MDR set. The rationale is an original statement of mapping scope and does not restate guidance text.

| MDCG ID | MDR target | Relation | Rationale | Expected outputs |
|---|---|---|---|---|
| 2.1 | I-1 | informative | The security goals set the context in which device risks are considered; they do not replace the MDR risk-management requirement. | security-risk-records |
| 2.1 | I-3 | partial | Connects cybersecurity risk consideration to the broader risk process while covering only the cybersecurity aspect. | risk-management-records, security-risk-records |
| 2.2 | I-17.2 | partial | Describes cybersecurity as part of software risk management, covering only that aspect of the MDR software lifecycle clause. | security-risk-records |
| 2.3 | I-17.2 | partial | Frames cybersecurity risk management across the software lifecycle, a subset of the clause's lifecycle activities. | security-risk-records |
| 2.3 | I-17.4 | partial | The described use and operating environment informs the operating prerequisites the manufacturer states, without fixing the hardware and network values. | it-requirements-statement, security-risk-records |
| 2.4 | I-17.2 | partial | Describes a risk-management approach for cybersecurity threats, not the entire software lifecycle process. | security-risk-records |
| 2.5 | I-17.2 | partial | Connects threat identification and risk analysis to software lifecycle risk records. | security-risk-records |
| 2.5 | I-14.2(d) | informative | Network and IT-security considerations can inform the device's stated environmental and infrastructure requirements. | it-requirements-statement |
| 2.6 | I-17.2 | partial | The section's security risk-control discussion covers a subset of software lifecycle risk management. | security-risk-records |
| 2.6 | I-17.4 | partial | Stakeholder security responsibilities inform which security measures the manufacturer states as operating prerequisites, not the hardware and network prerequisites. | it-requirements-statement, security-risk-records |
| 3.1 | I-17.2 | partial | Security-by-design guidance concerns software lifecycle activities, limited to the cybersecurity dimension. | security-risk-records |
| 3.1 | I-18.8 | partial | Security-by-design informs protection against access that could stop the device operating as intended, one aspect of the lifecycle guidance. | security-risk-records |
| 3.2 | I-17.2 | partial | Secure design guidance concerns software lifecycle activity only for cybersecurity risks. | security-risk-records |
| 3.2 | I-18.8 | partial | Design recommendations inform protection against unauthorised access, without establishing that the protection works. | security-risk-records |
| 3.3 | I-17.1 | partial | Architecture guidance concerns software architecture within the broader software lifecycle. | software-architecture |
| 3.3 | I-17.2 | partial | Architecture guidance addresses cybersecurity-related software lifecycle risks. | security-risk-records |
| 3.3 | I-18.8 | partial | Security capabilities in the architecture are how the design provides protection against unauthorised access. | software-architecture, security-risk-records |
| 3.4 | I-17.1 | partial | Software requirements guidance addresses only the requirements portion of lifecycle processes. | software-requirements |
| 3.4 | I-17.2 | partial | Security requirements contribute to, but do not exhaust, software risk management. | security-risk-records |
| 3.5 | I-17.2 | partial | Implementation guidance addresses cybersecurity risk controls within lifecycle risk management. | security-risk-records |
| 3.5 | I-17.3 | partial | The guidance can inform mobile-platform verification when applicable, without making that MDR clause universally applicable. | verification-records |
| 3.6 | I-14.2(d) | partial | Minimum IT requirements inform only the device's infrastructure requirement. | it-requirements-statement |
| 3.6 | I-17.4 | partial | Minimum operating-environment requirements are the content of the operating prerequisites the manufacturer specifies. | it-requirements-statement |
| 3.6 | I-23.4(ab) | informative | Environment and security information may inform instructions but does not cover the whole instructions requirement. | it-requirements-statement |
| 3.7 | I-17.2 | partial | Verification and validation guidance addresses the verification part of the software lifecycle clause for cybersecurity. | verification-records |
| 3.7 | I-18.8 | partial | Security test evidence shows whether protection against unauthorised access behaves as designed, without covering the design of that protection. | verification-records |
| 3.8 | I-17.2 | partial | Maintenance guidance covers the post-release part of the software lifecycle, including updates and component advisories. | release-record, soup-list |
| 3.8 | I-18.8 | partial | Fixing vulnerabilities restores protection against unauthorised access, without covering the design of that protection. | security-risk-records, anomaly-list |
| 4.1 | I-14.2(d) | partial | Security requirements for the operating environment inform only the IT-infrastructure portion of this requirement. | it-requirements-statement |
| 4.1 | I-23.4(ab) | informative | User information can inform the security-related content considered for instructions, without asserting full equivalence. | it-requirements-statement |
| 4.2 | I-23.4(ab) | partial | Security information for users contributes to, but does not exhaust, the information required by this clause. | it-requirements-statement |
| 4.3 | I-17.4 | partial | Information for healthcare providers informs the operating prerequisites the manufacturer states, not the hardware and network values. | it-requirements-statement |
| 4.3 | I-23.4(ab) | informative | User-facing security considerations may inform instructions but do not establish clause equivalence. | it-requirements-statement |
| 5.1 | I-3 | partial | Cybersecurity surveillance supplies part of the post-market information that updates the risk process; the manufacturer's own surveillance procedure is customer-supplied. | security-risk-records, written-procedure |
| 5.1 | I-17.2 | partial | Advisories reported against third-party components inform lifecycle maintenance of the software, covering only that input. | soup-list |
| 5.2 | I-3 | partial | Incident and vulnerability handling feeds the risk process; investigating and reporting incidents is the manufacturer's own procedure, which is customer-supplied. | written-procedure |

## EU Pack Output Catalog

The same artifact has the same name, kind and description in every EU-law set. Each set declares only its used subset. For names shared with the US pack, the canonical definition is the PLAT-1422 US Health-Law Output Catalog in its `spec/spec.md`; the EU contract test loads that file as a test-only dependency and compares every shared name and both fields. It does not keep a copied fixture or hand-maintained list of shared names.

| Name | Kind | Description |
|---|---|---|
| risk-management-records | record | `spec-objects-safety` `hazard` and `failure_mode` artifacts; `quoin risk-summary`. |
| software-requirements | record | Requirements authored with the `spec-artifacts-iso` StR, FR, and NFR archetypes. |
| software-architecture | record | `spec-objects-architecture` `part`, `port`, `connection`, and `allocation` artifacts; ADR artifacts from `spec-artifacts-process`. |
| verification-records | record | `quire matrix` / `quoin matrix` results and `quoin evidence record`. |
| soup-list | record | Software of unknown provenance (SOUP) report produced by `quoin soup report`. |
| security-risk-records | record | `spec-objects-security` threat, risk, and control records. |
| anomaly-list | record | Unresolved anomalies reported by `quoin anomaly report`. |
| release-record | record | Release evidence snapshot produced by `quoin release snapshot`. |
| it-requirements-statement | document | Customer-supplied statement of minimum hardware, network and IT-security requirements for instructions for use; no toolchain producer. |
| written-procedure | procedure | Customer-owned written procedure. |
| signed-record | record | Signed commits and tags verified by the `signature-verify` capability. |
| audit-trail | record | Git history and signed-approval history produced by the `approval-trail` capability for the record. |
| signer-registry | record | Allowed-signers mapping from signing key to named person, read by the `approval-trail` capability. |
| signature-meaning | record | The `Signed-off-meaning:` trailer verified by the `approval-verify` capability. |
| fda-certification-record | record | Evidence that the electronic-signature certification was submitted to FDA. |
| approval-trail | record | Signed approval history for a record produced by the `approval-trail` capability. |
| access-control | record | Repository permission and branch-rule settings. |
| processing-access-control | record | `spec-objects-security` `security.role` and `security.permission` records the customer authors for the personal-data processing system, or customer-supplied evidence of who may process personal data and on whose instructions; the clause set defines no producer. |
| system-access-control | record | `spec-objects-security` `security.role` and `security.permission` records the customer authors for the computerised system, or customer-supplied evidence of who may access it; no quoin, quire or engineering-assurance command produces it. |
| system-validation | record | Validation evidence for the toolchain's intended use. |
| training-record | procedure | Customer-owned training record. |
| data-flow-model | record | Architecture connections with their declared data flows and classifications. |
| records-of-processing | record | Controller or processor record of processing activities derived from the declared data-flow model. |
| dpia | document | Product-specific data protection impact assessment authored by people, with any residual-risk acceptance recorded by a named approver. |
| privacy-by-default-settings | record | Customer-supplied record of declared default processing settings and data-minimisation choices; no toolchain producer. |
| data-lineage | record | Customer-supplied record of provenance, selection, preparation and transformations for data used by the AI system; no toolchain producer. |
| model-description | document | Customer-supplied original description of AI system purpose, version, behavior, limits and use; no toolchain producer. |
| event-logging-design | record | Customer-supplied record of declared events, retention and access controls for AI system logs; no toolchain producer. |
| human-oversight-design | record | Customer-supplied record of human oversight roles, measures, competence and output-interpretation controls; no toolchain producer. |
| post-market-monitoring-plan | document | Customer-supplied provider plan and evidence for post-market performance monitoring; no toolchain producer. |
| conformity-declaration | document | Customer-supplied EU declaration of conformity and its controlled reference; no toolchain producer. |
| supplier-agreement | procedure | Customer-owned formal agreement with a third party that provides or supports a computerised system; no quoin, quire or engineering-assurance command produces it. |
| supplier-assessment | procedure | Customer-owned assessment of a supplier's competence, quality system and audit information; no quoin, quire or engineering-assurance command produces it. |
| system-inventory | procedure | Customer-owned inventory of GMP-relevant computerised systems and their functionality; no quoin, quire or engineering-assurance command produces it. |
| backup-restore-record | procedure | Customer-owned evidence that backups are taken and restoration is checked; no quoin, quire or engineering-assurance command produces it. |
| periodic-evaluation-record | procedure | Customer-owned periodic evaluation of a system's validated and compliant state; no quoin, quire or engineering-assurance command produces it. |
| business-continuity-plan | procedure | Customer-owned documented and tested continuity arrangements for a critical process; no quoin, quire or engineering-assurance command produces it. |
| archive-verification-record | procedure | Customer-owned check of archived data for accessibility, readability and integrity; no quoin, quire or engineering-assurance command produces it. |
| batch-certification-record | procedure | Customer-owned record of who certified batch release and their authority; no quoin, quire or engineering-assurance command produces it. |
| change-assurance-record | record | Change-assurance record written by `quoin change-assurance write-record`, addressed by record id and revision; attribution only, it does not establish authorisation. |
| baseline-record | record | Engineering-assurance Baseline document naming configuration items by repository path at one git commit; a person decides its contents. |
| record-export | record | Human-readable rendering of retained records from `quoin matrix`, `engineering-assurance approval-trail` and `quoin evidence audit`; it does not show a record's change history since first entry. |

`tests/corpus/` is synthetic; every synthetic ID and evidence reference uses `example.invalid`, and discharge facts are written to a temporary store.

## Customer-Owned Obligations

A clause whose expected outputs are all procedures is customer-owned and requires a delegated disposition with an owner, rationale and customer approval reference, never a direct fact. The inventory is exhaustive:

| Clause set | Clause ID | Expected outputs |
|---|---|---|
| ai-act-2024-1689 | art-20 | written-procedure |
| ai-act-2024-1689 | art-73 | written-procedure |
| mdcg-2019-16 | 5.2 | written-procedure |
| eu-gmp-annex-11 | 2 | written-procedure, training-record |
| eu-gmp-annex-11 | 3.1 | supplier-agreement |
| eu-gmp-annex-11 | 3.2 | supplier-assessment |
| eu-gmp-annex-11 | 3.4 | supplier-assessment |
| eu-gmp-annex-11 | 4.5 | supplier-assessment, written-procedure |
| eu-gmp-annex-11 | 7.2 | backup-restore-record, written-procedure |
| eu-gmp-annex-11 | 11 | periodic-evaluation-record |
| eu-gmp-annex-11 | 15 | batch-certification-record, written-procedure |
| eu-gmp-annex-11 | 16 | business-continuity-plan |
| eu-gmp-annex-11 | 17 | archive-verification-record, written-procedure |

## Requirements Architecture

FR-001 through FR-015 define module home, rights, MDR, MDCG and GDPR clauses and applicability, crosswalks, catalog, customer-owned obligations, skill mapping, and corpus. FR-016 through FR-022 define the AI Act sets, provider/deployer obligations, Annex IV table, human decision evidence, MDR crosswalks and application date. NFR-001 defines the general licensing and standards boundary; NFR-002 defines the GDPR-specific source and original-expression boundary; NFR-003 defines the AI Act source and standards boundary. FR-023 through FR-028 define the Annex 11 set, its clause table and applicability, output bindings, Part 11 crosswalks, corpus discharge and human decisions; NFR-004 defines the Annex 11 source and rights boundary. StR-001 records the manufacturer's need for reviewable evidence; US-001 describes the human review outcome. All functional requirements trace to US-001.

Dependency graph (an edge A → B means A depends on B): FR-003 → FR-001, FR-002, FR-006; FR-004 → FR-003; FR-005 → FR-001, FR-002, FR-003, FR-006; FR-006 → FR-001; FR-007 → FR-006; FR-008 → FR-001, FR-003, FR-004, FR-005, FR-006, FR-007; FR-009 → FR-001, FR-002, FR-006; FR-010 → FR-009; FR-011 → FR-010; FR-012 → FR-010, FR-011; FR-013 → FR-010, FR-011; FR-014 → FR-010; FR-015 → FR-009, FR-010; FR-016 → FR-001, FR-002; FR-017 → FR-016, FR-006; FR-018 → FR-016, FR-006; FR-019 → FR-017, FR-018; FR-020 → FR-017, FR-018; FR-021 → FR-018, FR-003; FR-022 → FR-016. NFR-001 constrains FR-001 through FR-022; NFR-002 constrains FR-009 through FR-015; NFR-003 constrains FR-016 through FR-022. FR-023 → FR-001, FR-002; FR-024 → FR-023, FR-006; FR-025 → FR-024, FR-006; FR-026 → FR-024; FR-027 → FR-024, FR-025, FR-007, FR-008; FR-028 → FR-024, FR-027. NFR-004 constrains FR-023 through FR-028.

## Upstream Contracts

The module uses existing `clause-set-v1`, `clause_sets`, `quire clauses evaluate`, `quire publish-check`, `quoin evidence record-discharge`, and `quoin discharge --rmm`. No engine change is specified.

## References

- EUR-Lex current consolidated MDR text consulted: `https://eur-lex.europa.eu/eli/reg/2017/745/2026-07-19/eng`.
- EUR-Lex legal notice: `https://eur-lex.europa.eu/content/legal-notice/legal-notice.html?locale=en`.
- MDCG 2019-16 rev.1 official PDF: `https://health.ec.europa.eu/document/download/b23b362f-8a56-434c-922a-5b3ca4d0a7a1_en?filename=md_cybersecurity_en.pdf`.
- Commission MDCG listing: `https://health.ec.europa.eu/medical-devices-sector/new-regulations/guidance-mdcg-endorsed-documents-and-other-guidance_en`.
- EUR-Lex current consolidated GDPR text consulted: `https://eur-lex.europa.eu/eli/reg/2016/679/2016-05-04/eng`.
- EUR-Lex legal notice on reuse and attribution: `https://eur-lex.europa.eu/content/legal-notice/legal-notice.html?locale=en`.
- EudraLex Volume 4 Annex 11 (January 2011) official document: `https://health.ec.europa.eu/document/download/8d305550-dd22-4dad-8463-2ddb4a1345f1_en?filename=annex11_01-2011_en.pdf`; Volume 4 listing: `https://health.ec.europa.eu/medicinal-products/eudralex/eudralex-volume-4_en`.
- European Commission legal notice (reuse, CC BY 4.0): `https://commission.europa.eu/legal-notice_en`.
- EUR-Lex consolidated AI Act text consulted: `https://eur-lex.europa.eu/eli/reg/2024/1689/2026-07-27/eng`.
- EUR-Lex legal notice on reuse and attribution: `https://eur-lex.europa.eu/content/legal-notice/legal-notice.html?locale=en`.
