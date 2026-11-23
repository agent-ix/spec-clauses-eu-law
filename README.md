# EU Law Compliance Pack

A Quoin module of clause sets for software that is a medical device, supports
one, or handles health or pharma data in the EU. It tells you which clauses
apply to your product, which of your records and tool outputs back each one,
and which clauses are still open. It never decides whether you comply. People
do that.

## What is in the pack

| Clause set | Source |
| --- | --- |
| MDR software-related requirements | Regulation (EU) 2017/745, Annexes I and II |
| MDCG 2019-16 | Cybersecurity guidance for medical devices, rev. 1 |
| GDPR | Regulation (EU) 2016/679: Articles 25, 30, 32 and 35 |
| AI Act high-risk obligations | Regulation (EU) 2024/1689: Articles 9 to 20, 26, 43, 47, 72 and 73 |
| AI Act Annex IV | Technical documentation elements of Regulation (EU) 2024/1689 |
| EU GMP Annex 11 | EudraLex Volume 4, Annex 11, computerised systems |

Every summary is written in our own words. Each set carries rights metadata
(source, licence, attribution) and the pack follows it: EUR-Lex and European
Commission material is cited and summarised with attribution, and no set
reproduces paywalled standard text. Read each clause as a pointer to the
source, not a replacement for it. See [CONTENT_RIGHTS.md](CONTENT_RIGHTS.md).

Some clauses also crosswalk to other packs: MDR clauses, US 21 CFR Part 11, the
HIPAA security rule and NIST SP 800-53. A crosswalk says how far two clauses
overlap. It never says one satisfies the other. The pack works without the
crosswalk target packs; install them (the US health-law pack, and the security
object module for NIST) if you want the crosswalks to resolve.

## Install

From a git checkout, which works today:

```sh
quoin module ensure-defaults
quoin module install github:agent-ix/spec-clauses-eu-law//spec_clauses_eu_law
```

From npm, once the package is published:

```sh
quoin module install package:@agent-ix/spec-clauses-eu-law
```

`quoin module list` shows the pack as installed. The default modules provide
the record types behind commands such as `quoin risk-summary`.

## Use it

1. Declare your context (for example `gdpr_role=controller`). Quire turns it
   into a binding report that lists which clauses apply and which do not.
2. Produce your evidence: author records, tag tests, run the tool commands in
   the table below.
3. Record what you attest per clause with `quoin evidence record-discharge`:
   either direct evidence references, or a disposition (for example delegated
   to a named owner) with an approval reference.
4. Run `quoin discharge --rmm --pack spec_clauses_eu_law` to get one
   requirements mapping matrix per clause set.
5. For GDPR Article 30, `quoin dossier generate --doc records-of-processing`
   builds the record of processing activities from your declared data flows
   and lists the gaps it finds.

### Example

A GDPR controller with high-risk processing, recording two facts. The
facts file holds one direct fact for `art-32(1)(a)` and one accepted-risk
disposition for `art-35(1)` that names the privacy officer as approver.

```sh
M=~/.ix/filament/modules/spec_clauses_eu_law
quire clauses evaluate --module $M --authority eu --set gdpr-2016-679 \
  --version 2016-05-04 --context gdpr_role=controller \
  --context high_risk_processing=yes \
  --context article_30_records_applicability=applies --json > binding.json

quoin evidence record-discharge --repo . --binding binding.json --facts facts.json

quoin discharge --rmm --pack spec_clauses_eu_law --repo . \
  --as-of 2026-11-23T00:00:00Z \
  --context gdpr_role=controller --context high_risk_processing=yes \
  --context article_30_records_applicability=applies \
  --context mobile_platform=no --context ai_high_risk=no \
  --context gmp_regulated_use=no
```

The matrix lists every set. The GDPR rows, trimmed:

```text
| art-30(1)(a) | Applicable | Not compliant - undischarged: no discharge fact | - |
| art-32(1)(a) | Applicable | Compliant | evidence://acme/tests/encryption-tests.md |
| art-35(1)    | Applicable | Tailored  | accepted_risk (approval person://acme.example/people/privacy-officer) |
| art-35(11)   | Applicable | Not compliant - undischarged: no discharge fact | - |
```

Clauses with no recorded fact stay open. "Compliant" here means the evidence
you recorded was accepted for that clause, not that the law is satisfied.

## What each clause needs

"Tool produces" lists commands that write a report or record. "You supply"
lists what your team authors or provides: records in the shipped record types,
tagged tests, documents and procedures. Rows that say "-" under "Tool
produces" have no command behind them. Customer-owned clauses need your own
procedures, whatever the tool reports. Clause groups that share the same
columns are merged into one row. Annex IV points also each have their own
applicability setting, so you declare which points apply to your system. In
the example, "Tailored" means the clause carries a disposition instead of
direct evidence.

### MDR (Regulation 2017/745)

| Clauses | Tool produces | You supply | Limits |
|---|---|---|---|
| I-1 to I-8 | `quoin risk-summary` | hazard and failure-mode records | - |
| I-14.2(d) | - | threat, risk and control records; IT requirements statement | - |
| I-17.1 | `quoin matrix`, `quoin evidence record` | requirements records; architecture records; tests tagged to requirements | - |
| I-17.2 | `quoin matrix`, `quoin evidence record` | requirements records; architecture records; threat, risk and control records; tests tagged to requirements | - |
| I-17.3 | `quoin matrix`, `quoin evidence record` | requirements records; architecture records; tests tagged to requirements | Applies when mobile_platform=yes |
| I-17.4 | - | threat, risk and control records; IT requirements statement | - |
| I-18.8 | `quoin matrix`, `quoin evidence record` | threat, risk and control records; tests tagged to requirements | - |
| I-23.4(ab) | - | IT requirements statement | - |
| II-1.1 | - | requirements records; architecture records | - |
| II-4 | `quoin matrix`, `quoin evidence record` | requirements records; architecture records; tests tagged to requirements | - |
| II-5 | `quoin risk-summary`, `quoin matrix`, `quoin evidence record` | hazard and failure-mode records; requirements records; tests tagged to requirements; threat, risk and control records | - |
| II-6.1(b) | `quoin matrix`, `quoin evidence record` | architecture records; tests tagged to requirements | - |

### MDCG 2019-16 cybersecurity guidance

| Clauses | Tool produces | You supply | Limits |
|---|---|---|---|
| 2.1 | `quoin risk-summary` | hazard and failure-mode records; threat, risk and control records | - |
| 2.2 | - | threat, risk and control records | - |
| 2.3 | - | threat, risk and control records; IT requirements statement | - |
| 2.4 | - | threat, risk and control records | - |
| 2.5 to 2.6 | - | threat, risk and control records; IT requirements statement | - |
| 3.1 to 3.2 | - | threat, risk and control records | - |
| 3.3 | - | threat, risk and control records; architecture records | - |
| 3.4 | - | threat, risk and control records; requirements records | - |
| 3.5 | `quoin matrix`, `quoin evidence record` | threat, risk and control records; tests tagged to requirements | - |
| 3.6 | - | IT requirements statement | - |
| 3.7 | `quoin matrix`, `quoin evidence record` | tests tagged to requirements | - |
| 3.8 | `quoin anomaly report`, `quoin release snapshot`, `quoin soup report` | threat, risk and control records | - |
| 4.1 to 4.3 | - | IT requirements statement | - |
| 5.1 | `quoin soup report` | threat, risk and control records; written procedure | - |
| 5.2 | - | written procedure | - |

### GDPR

| Clauses | Tool produces | You supply | Limits |
|---|---|---|---|
| art-25(1) | - | declared data flows; architecture records; threat, risk and control records; default settings record | Applies when gdpr_role=controller |
| art-25(2) | - | declared data flows; default settings record | Applies when gdpr_role=controller |
| art-30(1)(a) to art-30(1)(b) | `quoin dossier generate --doc records-of-processing` | declared data flows | Applies when gdpr_role=controller and article_30_records_applicability=applies |
| art-30(1)(c) | `quoin dossier generate --doc records-of-processing` | - | Applies when gdpr_role=controller and article_30_records_applicability=applies |
| art-30(1)(d) to art-30(1)(g) | `quoin dossier generate --doc records-of-processing` | declared data flows | Applies when gdpr_role=controller and article_30_records_applicability=applies |
| art-30(2)(a) to art-30(2)(d) | `quoin dossier generate --doc records-of-processing` | declared data flows | Applies when gdpr_role=processor and article_30_records_applicability=applies |
| art-30(3) | `quoin dossier generate --doc records-of-processing` | - | Applies when article_30_records_applicability=applies |
| art-30(4) | `quoin dossier generate --doc records-of-processing` | written procedure | Applies when article_30_records_applicability=applies |
| art-32(1)(a) to art-32(1)(b) | `quoin matrix`, `quoin evidence record` | threat, risk and control records; tests tagged to requirements | - |
| art-32(1)(c) | `quoin matrix`, `quoin evidence record` | threat, risk and control records; tests tagged to requirements; backup and restore evidence | - |
| art-32(1)(d) | `quoin matrix`, `quoin evidence record` | threat, risk and control records; tests tagged to requirements | - |
| art-32(2) | - | threat, risk and control records | - |
| art-32(4) | - | access records for personal-data processing; written procedure; training record | - |
| art-35(1) | - | declared data flows; threat, risk and control records; DPIA (people write it) | Applies when gdpr_role=controller and high_risk_processing=yes; Needs approval by the privacy officer |
| art-35(2) to art-35(7)(a) | - | declared data flows; DPIA (people write it) | Applies when gdpr_role=controller and high_risk_processing=yes; Needs approval by the privacy officer |
| art-35(7)(b) | - | threat, risk and control records; DPIA (people write it) | Applies when gdpr_role=controller and high_risk_processing=yes; Needs approval by the privacy officer |
| art-35(7)(c) | - | declared data flows; DPIA (people write it); default settings record | Applies when gdpr_role=controller and high_risk_processing=yes; Needs approval by the privacy officer |
| art-35(7)(d) | - | threat, risk and control records; DPIA (people write it) | Applies when gdpr_role=controller and high_risk_processing=yes; Needs approval by the privacy officer |
| art-35(9) | - | DPIA (people write it) | Applies when gdpr_role=controller and high_risk_processing=yes; Needs approval by the privacy officer |
| art-35(11) | - | declared data flows; threat, risk and control records; DPIA (people write it) | Applies when gdpr_role=controller and high_risk_processing=yes; Needs approval by the privacy officer |

### AI Act high-risk obligations

Unless a row says otherwise, clauses apply when ai_high_risk=yes and ai_role=provider.

| Clauses | Tool produces | You supply | Limits |
|---|---|---|---|
| art-9 | `quoin risk-summary` | hazard and failure-mode records | - |
| art-10 | `quoin matrix`, `quoin evidence record` | tests tagged to requirements; data lineage record | - |
| art-11 | `quoin matrix`, `quoin evidence record` | architecture records; tests tagged to requirements; AI system description | - |
| art-12 | - | event logging design | - |
| art-13 | - | AI system description; written procedure | - |
| art-14 | - | human oversight design | - |
| art-15 | `quoin matrix`, `quoin evidence record` | tests tagged to requirements; threat, risk and control records | - |
| art-16 | `quoin release snapshot` | AI system description; written procedure | - |
| art-17 | `engineering-assurance approval-trail` | written procedure | - |
| art-18 | - | AI system description; event logging design | - |
| art-19 | - | event logging design | - |
| art-20 | - | written procedure | - |
| art-26 | - | human oversight design; written procedure; event logging design | Applies when ai_role=deployer |
| art-43 | `quoin matrix`, `quoin evidence record` | tests tagged to requirements; declaration of conformity | - |
| art-47 | - | declaration of conformity | - |
| art-72 | - | post-market monitoring plan; event logging design | - |
| art-73 | - | written procedure | - |

### AI Act Annex IV

Unless a row says otherwise, clauses apply when ai_high_risk=yes and ai_role=provider.

| Clauses | Tool produces | You supply | Limits |
|---|---|---|---|
| IV-1(a) | - | AI system description | - |
| IV-1(b) | - | architecture records | - |
| IV-1(c) to IV-1(d) | - | AI system description | - |
| IV-1(e) to IV-1(f) | - | architecture records | - |
| IV-1(g) | - | AI system description | - |
| IV-1(h) | - | AI system description; written procedure | - |
| IV-2(a) | `quoin matrix`, `quoin evidence record` | architecture records; tests tagged to requirements | - |
| IV-2(b) | - | architecture records; AI system description | - |
| IV-2(c) | - | architecture records | - |
| IV-2(d) | - | data lineage record | - |
| IV-2(e) | - | human oversight design | - |
| IV-2(f) | `quoin release snapshot`, `quoin matrix`, `quoin evidence record` | tests tagged to requirements | - |
| IV-2(g) | `quoin matrix`, `quoin evidence record` | tests tagged to requirements | - |
| IV-2(h) | `quoin matrix`, `quoin evidence record` | threat, risk and control records; tests tagged to requirements | - |
| IV-3 | - | threat, risk and control records; AI system description; human oversight design | - |
| IV-4 | `quoin matrix`, `quoin evidence record` | tests tagged to requirements | - |
| IV-5 | `quoin risk-summary` | hazard and failure-mode records | - |
| IV-6 | `quoin release snapshot` | - | - |
| IV-7 | `quoin matrix`, `quoin evidence record` | tests tagged to requirements; AI system description | - |
| IV-8 | - | declaration of conformity | - |
| IV-9 | - | post-market monitoring plan | - |

### EU GMP Annex 11

Unless a row says otherwise, clauses apply when gmp_regulated_use=yes.

| Clauses | Tool produces | You supply | Limits |
|---|---|---|---|
| 1 | `quoin risk-summary` | hazard and failure-mode records; written procedure | Accepting a risk is a person's decision; The customer owns and supplies this record; Needs approval by the system owner |
| 2 | - | written procedure; training record | The customer owns and supplies this record |
| 3.1 | - | supplier agreement | Applies when third_party_supplier=yes |
| 3.2 | - | supplier assessment | Applies when third_party_supplier=yes; Needs approval by the system owner |
| 3.3 | `quoin soup report` | supplier assessment | Assessing the supplier stays with the customer; Applies when third_party_supplier=yes |
| 3.4 | - | supplier assessment | Applies when third_party_supplier=yes |
| 4.1 | `quoin matrix`, `quoin evidence record` | tests tagged to requirements; validation evidence | No command produces validation evidence; the customer supplies it; The matrix and evidence report what ran and do not judge whether it is adequate; Needs approval by the system owner |
| 4.2 | `quoin change-assurance write-record`, `quoin anomaly report` | - | An anomaly's content is a person's assessment |
| 4.3 | - | architecture records; declared data flows; system inventory | Needs approval by the system owner |
| 4.4 | - | requirements records | Needs approval by the system owner |
| 4.5 | - | supplier assessment; written procedure | The customer owns and supplies this record; Applies when third_party_supplier=yes |
| 4.6 | `quoin matrix`, `quoin evidence record` | tests tagged to requirements; validation evidence | The matrix and evidence report what ran and do not judge whether it is adequate; No command produces validation evidence; the customer supplies it; Applies when custom_or_customised=yes |
| 4.7 | `quoin matrix`, `quoin evidence record` | tests tagged to requirements; validation evidence | The matrix and evidence report what ran and do not judge whether it is adequate; No command produces validation evidence; the customer supplies it |
| 4.8 | `quoin matrix`, `quoin evidence record` | tests tagged to requirements; validation evidence | The matrix and evidence report what ran and do not judge whether it is adequate; No command produces validation evidence; the customer supplies it; Applies when data_migration=yes |
| 5 | `quoin matrix`, `quoin evidence record` | declared data flows; tests tagged to requirements | The matrix and evidence report what ran and do not judge whether it is adequate; Applies when data_exchange=yes |
| 6 | `quoin matrix`, `quoin evidence record` | tests tagged to requirements; written procedure | The customer owns and supplies this record; The matrix and evidence report what ran and do not judge whether it is adequate; Applies when manual_critical_entry=yes; Needs approval by the system owner |
| 7.1 | `engineering-assurance signature-verify` | repository permission settings; written procedure | No command reads repository permissions; the customer supplies them; The signing time is the signer's own claim, neither attested nor checked; The customer owns and supplies this record |
| 7.2 | - | backup and restore evidence; written procedure | The customer owns and supplies this record |
| 8.1 | `quoin matrix`, `quoin evidence audit` | - | - |
| 8.2 | `quoin matrix`, `quoin evidence audit`, `engineering-assurance approval-trail` | - | Deleted tags are invisible, and no reason-for-change field exists for every change; Applies when batch_release_records=yes |
| 9 | `engineering-assurance approval-trail` | written procedure | Deleted tags are invisible, and no reason-for-change field exists for every change; The customer owns and supplies this record; Needs approval by the system owner |
| 10 | `quoin change-assurance write-record` | baseline document; written procedure | The customer owns and supplies this record |
| 11 | - | periodic evaluation | - |
| 12.1 | - | system access records; written procedure | The customer owns and supplies this record |
| 12.2 | - | threat, risk and control records; system access records | Accepting a risk is a person's decision; Needs approval by the system owner |
| 12.3 | `engineering-assurance approval-trail` | allowed-signers file; repository permission settings | No command reads repository permissions; the customer supplies them; The allowed-signers registry has no audit trail beyond git; Deleted tags are invisible, and no reason-for-change field exists for every change |
| 12.4 | `engineering-assurance approval-trail` | allowed-signers file | Deleted tags are invisible, and no reason-for-change field exists for every change; The allowed-signers registry has no audit trail beyond git |
| 13 | `quoin anomaly report` | written procedure | An anomaly's content is a person's assessment; The customer owns and supplies this record; Needs approval by the system owner |
| 14(a) | `engineering-assurance approval-verify`, `engineering-assurance approval-trail` | allowed-signers file; written procedure | The signing time is the signer's own claim, neither attested nor checked; The allowed-signers registry has no audit trail beyond git; The customer owns and supplies this record; Applies when electronic_signature_use=yes |
| 14(b) to 14(c) | `engineering-assurance signature-verify`, `engineering-assurance approval-trail` | - | The signing time is the signer's own claim, neither attested nor checked; Deleted tags are invisible, and no reason-for-change field exists for every change; Applies when electronic_signature_use=yes |
| 15 | - | batch certification record; written procedure | The customer owns and supplies this record; Applies when batch_certification_in_system=yes |
| 16 | - | continuity plan | Applies when critical_process_support=yes; Needs approval by the system owner |
| 17 | - | archive check; written procedure | The customer owns and supplies this record; Applies when data_archived=yes |

## What the tool does not do

- It does not assign an AI Act risk class. You declare `ai_high_risk` and
  `ai_role` as context.
- It does not score risks or decide whether a risk is acceptable. Those are
  people's decisions.
- It never decides compliance. Reports show what evidence is recorded for each
  clause, nothing more.
- People approve. The GDPR Article 35 clauses name the privacy officer as the
  approval role for the DPIA, and the Annex 11 clauses for risk, validation,
  inventory and requirements, audit trail, incident management, supplier
  competence, continuity and similar name the system owner. Quoin checks that
  an approval reference is present on the fact. Customer-owned clauses need
  the customer's own procedures.

## Known limits

- Approval references are checked for presence, not for a verified signature.
- Records you supply yourself (documents, procedures, declarations) are not a
  record kind quoin can check, so clauses that depend only on them stay
  undischarged in quoin. Record a disposition with an owner and approval
  reference to show who is responsible.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). The design of every set is in
[spec/spec.md](spec/spec.md). The installable module name is
`spec_clauses_eu_law`.
