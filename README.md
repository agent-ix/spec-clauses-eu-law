# EU Law Compliance Pack

A clause-set module for [Quoin](https://github.com/agent-ix/quoin) and Quire
for teams building medical-device, health or pharma software for the EU. It
helps you record, clause by clause, the evidence you hold against EU law
obligations, and render the result as a requirements mapping matrix (RMM).

The pack records evidence. It does not decide whether you comply. See
[What the tool does not do](#what-the-tool-does-not-do).

## What is in the pack

Six clause sets. Every clause is a short summary in our own words with a
citation to the public source, following each set's rights metadata (source,
licence, attribution). No set reproduces paywalled standard text. Read each
clause as a pointer to the source, not a replacement for it. See
[CONTENT_RIGHTS.md](CONTENT_RIGHTS.md).

| Clause set | Source |
| --- | --- |
| `eu/mdr-2017-745` | MDR, Regulation (EU) 2017/745, Annexes I and II (software-related requirements) |
| `eu-mdcg/mdcg-2019-16` | MDCG 2019-16 rev. 1, cybersecurity guidance for medical devices |
| `eu/gdpr-2016-679` | GDPR, Regulation (EU) 2016/679: Articles 25, 30, 32 and 35 |
| `eu/ai-act-2024-1689` | AI Act, Regulation (EU) 2024/1689: Articles 9 to 20, 26, 43, 47, 72 and 73 |
| `eu/ai-act-2024-1689-annex-iv` | AI Act Annex IV, technical documentation elements |
| `eu/eu-gmp-annex-11` | EudraLex Volume 4, Annex 11, computerised systems |

Each clause carries an identifier, a force (mandatory or recommended), an
applicability rule over context you declare, and the named outputs that would
back it. Some clauses crosswalk to MDR clauses, US 21 CFR Part 11, the HIPAA
Security Rule and NIST SP 800-53. A crosswalk says how far two clauses
overlap. It never says one satisfies the other. The pack works without the
crosswalk target packs; install the US health-law pack if you want those
crosswalks to resolve (NIST comes with the default modules).

## Install

From npm, once the package is published:

```sh
quoin module install package:@agent-ix/spec-clauses-eu-law
```

From git, which works today:

```sh
quoin module ensure-defaults
quoin module install github:agent-ix/spec-clauses-eu-law//spec_clauses_eu_law
```

Check it with `quoin module list`. The default modules provide the record
types behind commands such as `quoin risk-summary`.

Several commands in the tables below are `engineering-assurance` commands.
That CLI is a native binary and is not part of the npm toolchain.
On Linux x86-64, download the latest release binary and put it on your `PATH`:

```sh
curl -fsSL -o engineering-assurance \
  https://github.com/agent-ix/engineering-assurance/releases/latest/download/engineering-assurance
chmod +x engineering-assurance
mv engineering-assurance ~/.local/bin/
```

On other platforms, build it with Cargo:

```sh
cargo install --git https://github.com/agent-ix/engineering-assurance \
  --locked --features full --bin engineering-assurance
```

## Use it

1. Declare your context, for example `gdpr_role=controller`. Applicability is
   computed from context you supply. The pack never guesses it, and a clause
   whose context is missing shows as undetermined.
2. Evaluate a clause set to get a binding report with
   `quire clauses evaluate --module <installed module path> --authority <a> --set <s> --version <v> --json --context key=value`.
3. Record your discharge facts with `quoin evidence record-discharge`. A fact is
   either direct (evidence references plus an attestation) or a disposition.
   A disposition has a `decision` (`delegated`, `accepted_risk` or
   `temporary_exception`), an `owner`, a `rationale` and an `approvalRef`.
   Every fact, direct or disposition, needs an `attestation` object
   (`attestedBy`, `authority`, `attestedAt`, `expiresAt`). A
   `temporary_exception` also needs `decisionExpiresAt`, no later than the
   attestation's `expiresAt`.
4. Render the matrix for every set with
   `quoin discharge --rmm --pack spec_clauses_eu_law`.
5. For GDPR Article 30, `quoin dossier generate --doc records-of-processing`
   builds the record of processing activities from your declared data flows
   and lists the gaps it finds.

### Example

This is a real run in an empty git repository with a throwaway home
directory. It is a GDPR controller with high-risk processing. It records one
direct fact for `art-32(1)(a)` and one accepted-risk disposition for
`art-35(1)`, and leaves the rest open.

```sh
M=$HOME/.ix/filament/modules/spec_clauses_eu_law   # installed module path

quire clauses evaluate --module $M --authority eu --set gdpr-2016-679 \
  --version 2016-05-04 --json \
  --context gdpr_role=controller --context high_risk_processing=yes \
  --context article_30_records_applicability=applies > binding.json

cat > facts.json <<'JSON'
[{"kind": "direct", "clauseId": "art-32(1)(a)",
  "evidenceRefs": ["evidence/encryption-tests.md"],
  "attestation": {"attestedBy": "qa@example.com", "authority": "quality-lead",
                  "attestedAt": "2026-11-23T00:00:00Z",
                  "expiresAt": "2027-11-23T00:00:00Z"}},
 {"kind": "disposition", "clauseId": "art-35(1)", "decision": "accepted_risk",
  "owner": "privacy-officer@example.com",
  "rationale": "The privacy officer reviewed the DPIA and accepted the residual risk.",
  "approvalRef": "evidence/dpia-approval.json",
  "attestation": {"attestedBy": "privacy-officer@example.com", "authority": "dpo",
                  "attestedAt": "2026-11-23T00:00:00Z",
                  "expiresAt": "2027-11-23T00:00:00Z"}}]
JSON

quoin evidence record-discharge --binding binding.json --facts facts.json

quoin discharge --rmm --pack spec_clauses_eu_law --repo . \
  --as-of 2026-11-23T00:00:00Z \
  --context gdpr_role=controller --context high_risk_processing=yes \
  --context article_30_records_applicability=applies \
  --context mobile_platform=no --context ai_high_risk=no \
  --context gmp_regulated_use=no
```

Trimmed output (the other sets' matrices and most GDPR rows are left out; the
rest is verbatim, including the Markdown escaping):

```text
# Requirements mapping matrix: eu/gdpr-2016-679@2016-05-04

| Req# | Applicability | Compliance | Evidence | Tailoring Description | Tailoring Rationale |
| --- | --- | --- | --- | --- | --- |
| art-30\(1\)\(a\) | Applicable | Not compliant - undischarged: no discharge fact | - | - | - |
| art-32\(1\)\(a\) | Applicable | Compliant | evidence/encryption-tests.md | - | - |
| art-35\(1\) | Applicable | Tailored | - | accepted\_risk \(approval evidence/dpia-approval.json\) | The privacy officer reviewed the DPIA and accepted the residual risk. |
| art-35\(11\) | Applicable | Not compliant - undischarged: no discharge fact | - | - | - |
```

## What each clause set needs

"Tool produces" lists outputs whose catalog entry names a Quoin, Quire or
engineering-assurance command or capability. "You supply" lists everything
else: records you author, documents, procedures and settings. The tool never
fills these in.

Records you author in the shipped record types (requirements, architecture,
security risk, hazard, data-flow and baseline records) are yours. They are
checked against their schema with `quire validate`, which does not judge their
content. Data flows are also read by `quoin dossier generate`, and a Baseline
document by `engineering-assurance release-verify`. "Nothing" under "Tool
produces" means no command writes a report for that clause. It does not mean
nothing checks your records.

Customer-owned clauses need your own procedures, whatever the tool reports.
Clause groups that share the same columns are merged into one row. In the
GDPR table, art-30 rows also depend on `article_30_records_applicability`.
Annex IV points each have their own applicability setting.

### MDR (Regulation 2017/745)

| Clauses | Tool produces | You supply | Limits |
|---|---|---|---|
| I-1 to I-5, I-8 | `quoin risk-summary` | hazard and failure-mode records | None |
| I-14.2(d) | Nothing | threat, risk and control records; IT requirements statement | None |
| I-17.1 | `quoin matrix`, `quoin evidence record` | requirements records; architecture records; tests tagged to requirements | None |
| I-17.2 | `quoin matrix`, `quoin evidence record` | requirements records; architecture records; threat, risk and control records; tests tagged to requirements | None |
| I-17.3 | `quoin matrix`, `quoin evidence record` | requirements records; architecture records; tests tagged to requirements | Applies when mobile_platform=yes |
| I-17.4 | Nothing | threat, risk and control records; IT requirements statement | None |
| I-18.8 | `quoin matrix`, `quoin evidence record` | threat, risk and control records; tests tagged to requirements | None |
| I-23.4(ab) | Nothing | IT requirements statement | None |
| II-1.1 | Nothing | requirements records; architecture records | None |
| II-4 | `quoin matrix`, `quoin evidence record` | requirements records; architecture records; tests tagged to requirements | None |
| II-5 | `quoin risk-summary`, `quoin matrix`, `quoin evidence record` | hazard and failure-mode records; requirements records; tests tagged to requirements; threat, risk and control records | None |
| II-6.1(b) | `quoin matrix`, `quoin evidence record` | architecture records; tests tagged to requirements | None |

### MDCG 2019-16 cybersecurity guidance

| Clauses | Tool produces | You supply | Limits |
|---|---|---|---|
| 2.1 | `quoin risk-summary` | hazard and failure-mode records; threat, risk and control records | None |
| 2.2 | Nothing | threat, risk and control records | None |
| 2.3 | Nothing | threat, risk and control records; IT requirements statement | None |
| 2.4 | Nothing | threat, risk and control records | None |
| 2.5 to 2.6 | Nothing | threat, risk and control records; IT requirements statement | None |
| 3.1 to 3.2 | Nothing | threat, risk and control records | None |
| 3.3 | Nothing | threat, risk and control records; architecture records | None |
| 3.4 | Nothing | threat, risk and control records; requirements records | None |
| 3.5 | `quoin matrix`, `quoin evidence record` | threat, risk and control records; tests tagged to requirements | None |
| 3.6 | Nothing | IT requirements statement | None |
| 3.7 | `quoin matrix`, `quoin evidence record` | tests tagged to requirements | None |
| 3.8 | `quoin anomaly report`, `quoin release snapshot`, `quoin soup report` | threat, risk and control records | None |
| 4.1 to 4.3 | Nothing | IT requirements statement | None |
| 5.1 | `quoin soup report` | threat, risk and control records; written procedure | None |
| 5.2 | Nothing | written procedure | None |

### GDPR

| Clauses | Tool produces | You supply | Limits |
|---|---|---|---|
| art-25(1) | Nothing | declared data flows; architecture records; threat, risk and control records; default settings record | Applies when gdpr_role=controller |
| art-25(2) | Nothing | declared data flows; default settings record | Applies when gdpr_role=controller |
| art-30(1)(a) to art-30(1)(b) | `quoin dossier generate --doc records-of-processing` | declared data flows | Applies when gdpr_role=controller and article_30_records_applicability=applies |
| art-30(1)(c) | `quoin dossier generate --doc records-of-processing` | Nothing | Applies when gdpr_role=controller and article_30_records_applicability=applies |
| art-30(1)(d) to art-30(1)(g) | `quoin dossier generate --doc records-of-processing` | declared data flows | Applies when gdpr_role=controller and article_30_records_applicability=applies |
| art-30(2)(a) to art-30(2)(d) | `quoin dossier generate --doc records-of-processing` | declared data flows | Applies when gdpr_role=processor and article_30_records_applicability=applies |
| art-30(3) | `quoin dossier generate --doc records-of-processing` | Nothing | Applies when article_30_records_applicability=applies |
| art-30(4) | `quoin dossier generate --doc records-of-processing` | written procedure | Applies when article_30_records_applicability=applies |
| art-32(1)(a) to art-32(1)(b) | `quoin matrix`, `quoin evidence record` | threat, risk and control records; tests tagged to requirements | None |
| art-32(1)(c) | `quoin matrix`, `quoin evidence record` | threat, risk and control records; tests tagged to requirements; backup and restore evidence | None |
| art-32(1)(d) | `quoin matrix`, `quoin evidence record` | threat, risk and control records; tests tagged to requirements | None |
| art-32(2) | Nothing | threat, risk and control records | None |
| art-32(4) | Nothing | access records for personal-data processing; written procedure; training record | None |
| art-35(1) | Nothing | declared data flows; threat, risk and control records; DPIA (people write it) | Applies when gdpr_role=controller and high_risk_processing=yes; Needs approval by the privacy officer |
| art-35(2) to art-35(7)(a) | Nothing | declared data flows; DPIA (people write it) | Applies when gdpr_role=controller and high_risk_processing=yes; Needs approval by the privacy officer |
| art-35(7)(b) | Nothing | threat, risk and control records; DPIA (people write it) | Applies when gdpr_role=controller and high_risk_processing=yes; Needs approval by the privacy officer |
| art-35(7)(c) | Nothing | declared data flows; DPIA (people write it); default settings record | Applies when gdpr_role=controller and high_risk_processing=yes; Needs approval by the privacy officer |
| art-35(7)(d) | Nothing | threat, risk and control records; DPIA (people write it) | Applies when gdpr_role=controller and high_risk_processing=yes; Needs approval by the privacy officer |
| art-35(9) | Nothing | DPIA (people write it) | Applies when gdpr_role=controller and high_risk_processing=yes; Needs approval by the privacy officer |
| art-35(11) | Nothing | declared data flows; threat, risk and control records; DPIA (people write it) | Applies when gdpr_role=controller and high_risk_processing=yes; Needs approval by the privacy officer |

### AI Act high-risk obligations

Unless a row says otherwise, clauses apply when ai_high_risk=yes and ai_role=provider.

| Clauses | Tool produces | You supply | Limits |
|---|---|---|---|
| art-9 | `quoin risk-summary` | hazard and failure-mode records | None |
| art-10 | `quoin matrix`, `quoin evidence record` | tests tagged to requirements; data lineage record | None |
| art-11 | `quoin matrix`, `quoin evidence record` | architecture records; tests tagged to requirements; AI system description | None |
| art-12 | Nothing | event logging design | None |
| art-13 | Nothing | AI system description; written procedure | None |
| art-14 | Nothing | human oversight design | None |
| art-15 | `quoin matrix`, `quoin evidence record` | tests tagged to requirements; threat, risk and control records | None |
| art-16 | `quoin release snapshot` | AI system description; written procedure | None |
| art-17 | `engineering-assurance approval-trail` | written procedure | None |
| art-18 | Nothing | AI system description; event logging design | None |
| art-19 | Nothing | event logging design | None |
| art-20 | Nothing | written procedure | None |
| art-26 | Nothing | human oversight design; written procedure; event logging design | Applies when ai_high_risk=yes and ai_role=deployer |
| art-43 | `quoin matrix`, `quoin evidence record` | tests tagged to requirements; declaration of conformity | None |
| art-47 | Nothing | declaration of conformity | None |
| art-72 | Nothing | post-market monitoring plan; event logging design | None |
| art-73 | Nothing | written procedure | None |

### AI Act Annex IV

Clauses apply when ai_high_risk=yes and ai_role=provider, and when you declare the point's own dimension: `ai_annex_iv_1_a_applicable` for IV-1(a), `ai_annex_iv_2_h_applicable` for IV-2(h), `ai_annex_iv_3_applicable` for IV-3, and so on. A point whose dimension is not declared shows as Undetermined.

| Clauses | Tool produces | You supply | Limits |
|---|---|---|---|
| IV-1(a) | Nothing | AI system description | None |
| IV-1(b) | Nothing | architecture records | None |
| IV-1(c) to IV-1(d) | Nothing | AI system description | None |
| IV-1(e) to IV-1(f) | Nothing | architecture records | None |
| IV-1(g) | Nothing | AI system description | None |
| IV-1(h) | Nothing | AI system description; written procedure | None |
| IV-2(a) | `quoin matrix`, `quoin evidence record` | architecture records; tests tagged to requirements | None |
| IV-2(b) | Nothing | architecture records; AI system description | None |
| IV-2(c) | Nothing | architecture records | None |
| IV-2(d) | Nothing | data lineage record | None |
| IV-2(e) | Nothing | human oversight design | None |
| IV-2(f) | `quoin release snapshot`, `quoin matrix`, `quoin evidence record` | tests tagged to requirements | None |
| IV-2(g) | `quoin matrix`, `quoin evidence record` | tests tagged to requirements | None |
| IV-2(h) | `quoin matrix`, `quoin evidence record` | threat, risk and control records; tests tagged to requirements | None |
| IV-3 | Nothing | threat, risk and control records; AI system description; human oversight design | None |
| IV-4 | `quoin matrix`, `quoin evidence record` | tests tagged to requirements | None |
| IV-5 | `quoin risk-summary` | hazard and failure-mode records | None |
| IV-6 | `quoin release snapshot` | Nothing | None |
| IV-7 | `quoin matrix`, `quoin evidence record` | tests tagged to requirements; AI system description | None |
| IV-8 | Nothing | declaration of conformity | None |
| IV-9 | Nothing | post-market monitoring plan | None |

### EU GMP Annex 11

Unless a row says otherwise, clauses apply when gmp_regulated_use=yes.

| Clauses | Tool produces | You supply | Limits |
|---|---|---|---|
| 1 | `quoin risk-summary` | hazard and failure-mode records; written procedure | Accepting a risk is a person's decision; The customer owns and supplies this record; Needs approval by the system owner |
| 2 | Nothing | written procedure; training record | The customer owns and supplies this record |
| 3.1 | Nothing | supplier agreement | Applies when third_party_supplier=yes |
| 3.2 | Nothing | supplier assessment | Applies when third_party_supplier=yes; Needs approval by the system owner |
| 3.3 | `quoin soup report` | supplier assessment | Assessing the supplier stays with the customer; Applies when third_party_supplier=yes |
| 3.4 | Nothing | supplier assessment | Applies when third_party_supplier=yes |
| 4.1 | `quoin matrix`, `quoin evidence record` | tests tagged to requirements; validation evidence | No command produces validation evidence; the customer supplies it; The matrix and evidence report what ran and do not judge whether it is adequate; Needs approval by the system owner |
| 4.2 | `quoin change-assurance write-record`, `quoin anomaly report` | Nothing | An anomaly's content is a person's assessment; a change-assurance record is attribution only and does not establish authorisation |
| 4.3 | Nothing | architecture records; declared data flows; system inventory | Needs approval by the system owner |
| 4.4 | Nothing | requirements records | Needs approval by the system owner |
| 4.5 | Nothing | supplier assessment; written procedure | The customer owns and supplies this record; Applies when third_party_supplier=yes |
| 4.6 | `quoin matrix`, `quoin evidence record` | tests tagged to requirements; validation evidence | The matrix and evidence report what ran and do not judge whether it is adequate; No command produces validation evidence; the customer supplies it; Applies when custom_or_customised=yes |
| 4.7 | `quoin matrix`, `quoin evidence record` | tests tagged to requirements; validation evidence | The matrix and evidence report what ran and do not judge whether it is adequate; No command produces validation evidence; the customer supplies it |
| 4.8 | `quoin matrix`, `quoin evidence record` | tests tagged to requirements; validation evidence | The matrix and evidence report what ran and do not judge whether it is adequate; No command produces validation evidence; the customer supplies it; Applies when data_migration=yes |
| 5 | `quoin matrix`, `quoin evidence record` | declared data flows; tests tagged to requirements | The matrix and evidence report what ran and do not judge whether it is adequate; Applies when data_exchange=yes |
| 6 | `quoin matrix`, `quoin evidence record` | tests tagged to requirements; written procedure | The customer owns and supplies this record; The matrix and evidence report what ran and do not judge whether it is adequate; Applies when manual_critical_entry=yes; Needs approval by the system owner |
| 7.1 | `engineering-assurance signature-verify` | repository permission settings; written procedure | No command reads repository permissions; the customer supplies them; The signing time is the signer's own claim, neither attested nor checked; The customer owns and supplies this record |
| 7.2 | Nothing | backup and restore evidence; written procedure | The customer owns and supplies this record |
| 8.1 | `quoin matrix`, `quoin evidence audit`, `engineering-assurance approval-trail` | Nothing | The export does not show a record's change history since first entry |
| 8.2 | `quoin matrix`, `quoin evidence audit`, `engineering-assurance approval-trail` | Nothing | The export does not show a record's change history since first entry; deleted tags are invisible, and no reason-for-change field exists for every change; Applies when batch_release_records=yes |
| 9 | `engineering-assurance approval-trail` | written procedure | Deleted tags are invisible, and no reason-for-change field exists for every change; The customer owns and supplies this record; Needs approval by the system owner |
| 10 | `quoin change-assurance write-record` | baseline document; written procedure | The customer owns and supplies this record; a change-assurance record is attribution only and does not establish authorisation |
| 11 | Nothing | periodic evaluation | None |
| 12.1 | Nothing | system access records; written procedure | The customer owns and supplies this record |
| 12.2 | Nothing | threat, risk and control records; system access records | Accepting a risk is a person's decision; Needs approval by the system owner |
| 12.3 | `engineering-assurance approval-trail` | allowed-signers file; repository permission settings | No command reads repository permissions; the customer supplies them; The allowed-signers registry has no audit trail beyond git; Deleted tags are invisible, and no reason-for-change field exists for every change |
| 12.4 | `engineering-assurance approval-trail` | allowed-signers file | Deleted tags are invisible, and no reason-for-change field exists for every change; The allowed-signers registry has no audit trail beyond git |
| 13 | `quoin anomaly report` | written procedure | An anomaly's content is a person's assessment; The customer owns and supplies this record; Needs approval by the system owner |
| 14(a) | `engineering-assurance approval-verify` | allowed-signers file; written procedure | The signing time is the signer's own claim, neither attested nor checked; The allowed-signers registry has no audit trail beyond git; The customer owns and supplies this record; Applies when electronic_signature_use=yes |
| 14(b) to 14(c) | `engineering-assurance signature-verify`, `engineering-assurance approval-trail` | Nothing | The signing time is the signer's own claim, neither attested nor checked; Deleted tags are invisible, and no reason-for-change field exists for every change; Applies when electronic_signature_use=yes |
| 15 | Nothing | batch certification record; written procedure | The customer owns and supplies this record; Applies when batch_certification_in_system=yes |
| 16 | Nothing | continuity plan | Applies when critical_process_support=yes; Needs approval by the system owner |
| 17 | Nothing | archive check; written procedure | The customer owns and supplies this record; Applies when data_archived=yes |


## What the tool does not do

- It never assigns an AI Act risk class, risk scores, documentation levels or
  acceptability. You declare `ai_high_risk` and `ai_role` as context. People
  accept risk and approve.
- It never decides compliance. A clause state is a report of the evidence you
  recorded, as of the `--as-of` time you give. The matrix prints these states:
  - **Compliant**: a direct fact is recorded and its attestation is current at
    `--as-of`.
  - **Tailored**: a disposition is recorded with an owner, rationale and
    approval reference, and its attestation is current.
  - **Not compliant - undischarged: no discharge fact**: nothing is recorded
    for the clause.
  - **Not compliant - undischarged: required approval reference is missing**:
    the clause names an approval role and the fact has no approval reference.
  - **Not compliant - attestation not current**: a fact exists but its
    attestation has expired at `--as-of` (the matrix says "discharge fact is
    expired"). A `temporary_exception` past its end date prints
    **Not compliant - temporary exception expired**.
  - **Undetermined**: a context value the clause depends on is not declared.
    The applicability column shows Unresolved.
  - **Not applicable**: the declared context excludes the clause.

  "Not compliant" only means nothing current is recorded for that clause. It
  is not a finding that you fail the regulation.
- People approve. The GDPR Article 35 clauses name the privacy officer as the
  approval role for the DPIA. Annex 11 clauses on risk, supplier competence,
  validation, system inventory, requirements, accuracy checks, audit trail,
  security controls, incident management and continuity name the system owner.
  Quoin checks that an approval reference is present on the fact.
- Customer-owned clauses, where every expected output is a procedure, need
  your own written procedures. The pack records that you own them, not that
  they exist or are adequate.
- It is not legal advice and does not certify anything.

## Known limits

- **Evidence checks are shallow.** `quoin discharge` shows a clause as
  compliant when a direct fact with evidence references and an attestation is
  recorded. A reference to a file that does not exist is accepted the same
  way. Check that your evidence is real and sufficient; the matrix does not do
  it for you.
- **Approval references are checked for presence, not signature.** Any
  non-blank reference satisfies a required approval role; it is not yet
  verified as a signature by the named person.
- **Customer-supplied records stay undischarged.** Quoin has no
  customer-artifact record kind yet, so clauses whose outputs are documents,
  procedures or records you supply remain undischarged in the matrix unless
  you record a disposition for them. A direct fact does not turn such an
  output into tool-produced evidence.

## Development

Specification: [`spec/spec.md`](spec/spec.md). Clause data:
`spec_clauses_eu_law/clauses/`. Content rules:
[`CONTENT_RIGHTS.md`](CONTENT_RIGHTS.md). See
[`CONTRIBUTING.md`](CONTRIBUTING.md). Licensed under the AGPL-3.0-or-later.
