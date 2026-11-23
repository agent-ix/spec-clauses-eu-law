---
id: SR-20261104139943
title: "Code review of PLAT-1831 spec-clauses-eu-law PR #27 (adopter README)"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-clauses-eu-law; README.md"
review_set: subset
---

## Summary

Ticket: PLAT-1831. I reviewed `git diff origin/main...HEAD` at 21083644 (spec-clauses-eu-law PR #27) in a scratch clone. The PR rewrites only README.md, for adopters. It covers the pack contents, install, a five-step workflow, a GDPR example, one table per clause set ("Tool produces", "You supply", "Limits"), what the tool does not do, and known limits.

## Verdict

**REQUEST CHANGES.** I found four medium defects and six low ones. All of them are prose fixes in README.md.

What holds up:

- Table accuracy. I checked 41 rows against the clause JSON on main: expected outputs, applicability and approval roles. The rows checked were all 12 MDR rows; MDCG 2.1, 2.3, 3.3, 3.8 and 5.1; GDPR art-25(1), art-30(1)(c), art-30(2)(a)-(d), art-32(1)(c), art-32(4), art-35(1) and art-35(7)(c); AI Act art-10, 16, 17, 26 and 43; Annex IV IV-1(b), IV-2(f), IV-3 and IV-6; and Annex 11 rows 1, 3.3, 4.1, 4.2, 4.3, 7.1, 8.1, 8.2, 10, 12.3, 14(a) and 14(b)-(c). The You-supply columns and applicability match. The exceptions are FND-005, FND-007 and FND-008.
- Commands. Every named command exists with the stated behaviour in quoin 0.36.10, quire 0.52.1 and engineering-assurance 0.10.1. The quoin commands are `risk-summary`, `matrix`, `evidence record`, `evidence audit`, `evidence record-discharge`, `discharge --rmm --pack`, `release snapshot`, `soup report`, `anomaly report`, `change-assurance write-record` and `dossier generate --doc records-of-processing`. The last one writes DOS-ROP and lists its gaps. The engineering-assurance commands are `approval-trail`, `approval-verify` and `signature-verify`.
- Install and example. I used `npm ci` from npmjs only and a throwaway HOME at an absolute scratch path. `ensure-defaults` and the git install both exit 0, and the module lands at `~/.ix/filament/modules/spec_clauses_eu_law`, as the example's `M=` says. I wrote a facts.json to the README's description. The evaluate, record-discharge and discharge steps all exit 0. The four GDPR rows match in substance: art-30(1)(a) and art-35(11) undischarged, art-32(1)(a) Compliant, and art-35(1) Tailored accepted_risk.
- Known limits, confirmed by experiment. A direct fact on art-35(9) with `approvalRef: "anything"` renders Compliant, so approval references are checked only for presence. Without an approvalRef, the clause prints `Not compliant - undischarged: required approval reference is missing`.
- Hard rules. There is no paywalled text, and no tool-assigned class, score or acceptability. The README says plainly that the tool never decides compliance. There is no roadmap or delivery order. There are no SHAs and no toolchain pins. `--version 2016-05-04` is the clause-set version argument. The npm form is marked "once the package is published", and npmjs returns E404 for the package.
- Customer-authored records. security-risk-records, software-architecture, software-requirements, data-flow-model and baseline-record are authored by the customer, so listing them under "You supply" is right. They are not unchecked, though. See FND-001.

## Verification

- Scratch clone at 21083644, then `npm ci --registry https://registry.npmjs.org/ --@agent-ix:registry=https://registry.npmjs.org/ --userconfig /dev/null`. `quoin --version` reports 0.36.10. `quire --version` reports 0.52.1 (engine 0.62.2).
- Throwaway HOME: `quoin module ensure-defaults`, then `quoin module install github:agent-ix/spec-clauses-eu-law//spec_clauses_eu_law`, then the README example with a reconstructed facts.json.
- Probes:
  - `--as-of 2028-01-01T00:00:00Z` prints `Not compliant - attestation not current: discharge fact is expired`.
  - Dropping `gdpr_role` prints `Undetermined: context does not declare gdpr_role`.
  - A disposition without `attestation` is rejected with `attestation must be an object`.
  - A `temporary_exception` without `decisionExpiresAt` is rejected with `disposition discharge fact is missing decisionExpiresAt`.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | Line 104 says rows with "-" under "Tool produces" "have no command behind them". That contradicts the spec's Annex 11 Output Bindings (spec/spec.md:293-296). software-requirements, software-architecture, data-flow-model and security-risk-records are authored in shipped record types and checked by `quire validate`. baseline-record is checked by `quire validate` against the engineering-assurance Baseline schema and read by `engineering-assurance release-verify`. data-flow-model is the input to `quoin dossier generate --doc records-of-processing`. Keeping these records under "You supply" is right, and so is leaving `quire validate` out of "Tool produces". Fix: reword 102-106 to say these records are yours and are schema-checked by `quire validate` (data flows are also read by `dossier generate`, and a Baseline by `release-verify`), and that "-" means no command writes a report for the clause. Schema checking does not judge content. | README.md:102-106 |
| FND-002 | medium | The clause states are not explained to match what the RMM prints. "Compliant" (97-98) also needs an attestation current at `--as-of`; an expired one prints `Not compliant - attestation not current`. On approval-role clauses, a missing approvalRef prints `Not compliant - undischarged: required approval reference is missing`. `Undetermined` (a context dimension not declared) and `Not applicable` are not explained. Nor is the literal "Not compliant", which means nothing current is recorded, not a finding of non-compliance. Fix: add a short state legend, worded the same as the US pack's legend. | README.md:97-98, 108-110 |
| FND-003 | medium | The example cannot be reproduced, and step 3 understates the fact fields. facts.json is described but never shown. A disposition needs `decision`, `owner`, `rationale`, `approvalRef` and an `attestation` object; record-discharge rejects it without the attestation (`attestation must be an object`). `temporary_exception` also needs `decisionExpiresAt`. Fix: add the facts.json heredoc, one direct fact and one accepted_risk disposition each with an attestation, as the US README does. Name the required disposition fields in step 3. | README.md:56-58, 67-70 |
| FND-004 | medium | The Annex 11 Limits column omits the limits that live only in the EU catalog descriptions. Rows 8.1 and 8.2 leave out record-export's limit: it "does not show a record's change history since first entry". Paragraph 8.2 asks for printouts showing whether data changed since first entry, so the 8.2 row overclaims. Rows 4.2 and 10 leave out change-assurance-record's limit: "attribution only, it does not establish authorisation". Fix: add these limits to rows 8.1, 8.2, 4.2 and 10. | README.md:239, 250-251, 253 |
| FND-005 | low | "I-1 to I-8" implies I-6 and I-7. The MDR set has I-1 to I-5 and I-8, and the matrix prints those six. Fix: "I-1 to I-5, I-8". | README.md:116 |
| FND-006 | low | The trimmed output drops the header, the separator and two Tailoring columns, and it unescapes the ids. The real rows read `art-30\(1\)\(a\)`. The art-35(1) row also moves the tailoring text into the Evidence column; in the real output, Evidence is `-` and the text sits under Tailoring Description, followed by a Rationale column. Fix: show the real header and columns, or say what was trimmed. | README.md:90-95 |
| FND-007 | low | The context notes do not name the clauses they affect. The art-26 row's "Applies when ai_role=deployer", read after the preface "unless a row says otherwise ... ai_high_risk=yes and ai_role=provider", suggests art-26 drops the high-risk condition; it requires ai_high_risk=yes and ai_role=deployer. The Annex IV preface leaves out each point's own `ai_annex_iv_<point>_applicable` dimension; without it the point prints Undetermined. Fix: say "ai_high_risk=yes and ai_role=deployer" in the art-26 row, and name the per-point dimension in the Annex IV preface. | README.md:176, 192, 200 |
| FND-008 | low | The producer attribution is off in two Annex 11 rows. Row 14(a) lists `engineering-assurance approval-trail`, but none of its outputs is produced by approval-trail: signer-registry's producer is "none" (spec/spec.md:291), and approval-trail only reads it. Row 8.1 lists matrix and evidence audit but leaves out `engineering-assurance approval-trail`, which the record-export catalog entry also names. Fix: 14(a) Tool produces `approval-verify` only; add approval-trail to 8.1. | README.md:250, 260 |
| FND-009 | low | Install does not say where the engineering-assurance CLI comes from. Eight table rows name `engineering-assurance` commands, but the npm toolchain ships only `quoin` and `quire`, and the default `engineering-assurance` module provides schemas, not the binary. Separately, lines 29-30 tell adopters to install "the security object module for NIST", but `quoin module ensure-defaults` already installs spec-objects-security. Fix: add one line on getting the engineering-assurance CLI. Drop the NIST install advice, or say it comes with the defaults. | README.md:29-30, 32-48 |
| FND-010 | low | The README is inconsistent with the US pack README (spec-clauses-us-health#40). The headings differ: "What each clause needs" here, "What each clause set needs" there, and "Contributing" here, "Development" there. The install order is reversed. This README marks empty cells "-" where the US one says "Nothing", and the two define "Tool produces" differently. The shared limits are missing: "Evidence checks are shallow" (the example's nonexistent `evidence://acme/...` ref is accepted as Compliant, which I verified) and "not legal advice and does not certify anything". Fix: align the headings, the install order and the Tool-produces definition, and copy the shared limit wording. | README.md:32-45, 100-106, 266-293 |

## New findings (disposition pass 1)

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-011 | low | The engineering-assurance install offers only `cargo install --git ... --locked --features full --bin engineering-assurance`. That command is valid: the `engineering-assurance` bin requires `full`. But a prebuilt binary also exists. The v0.10.1 GitHub release (Latest) carries one asset, `engineering-assurance` (26,350,832 bytes, application/octet-stream), and spec-clauses-us-health's ci.yml downloads it with curl on `ubuntu-latest`. An adopter on Linux x86-64 does not need a Rust toolchain. Fix: offer the download first, using the unpinned `https://github.com/agent-ix/engineering-assurance/releases/latest/download/engineering-assurance` URL so that no version pin sits in prose. Say it is a Linux x86-64 binary, and keep Cargo as the route for other platforms. | README.md:54-61 |

## Dispositions

Round 1 checks `git diff 21083644..7b7462b7`. I re-ran the new README example verbatim (lines 92-121) in a scratch clone with a throwaway HOME: `npm ci` from npmjs only (quoin 0.36.10, quire 0.52.1), then `ensure-defaults` and the git install. All steps exit 0. The four rows printed under `eu/gdpr-2016-679@2016-05-04` match README lines 132-135 byte for byte. I also probed the new state legend. An expired `temporary_exception` prints `Not compliant - temporary exception expired`, and a missing context prints `Unresolved` / `Undetermined: ...`. Both match lines 328-333.

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | Lines 145-151 now say these records are yours and are schema-checked by `quire validate`, which does not judge content. Data flows are read by `quoin dossier generate` and a Baseline by `engineering-assurance release-verify`. "Nothing" means that no command writes a report. |
| FND-002 | fixed | Lines 318-337 give a full state legend. Every state in it matches what quoin 0.36.10 prints, including attestation not current, temporary exception expired, approval reference missing, Undetermined/Unresolved and Not applicable. |
| FND-003 | fixed | Lines 70-77 name the required fact fields. Lines 99-112 show facts.json, and the example reproduces exactly. |
| FND-004 | fixed | Rows 4.2, 8.1, 8.2 and 10 (lines 285, 296, 297, 299) now carry the record-export and change-assurance limits. |
| FND-005 | fixed | Line 162 now reads "I-1 to I-5, I-8". |
| FND-006 | fixed | Lines 124-136 show the real header and all six columns verbatim, with escaping, and say what was trimmed. |
| FND-007 | fixed | Line 238 now reads "ai_high_risk=yes and ai_role=deployer". Line 246 names the per-point `ai_annex_iv_*_applicable` dimension and says a missing one shows as Undetermined. |
| FND-008 | fixed | Row 14(a) (line 306) now lists only `approval-verify`. Row 8.1 (line 296) adds `engineering-assurance approval-trail`. |
| FND-009 | fixed | Lines 54-61 now say where the engineering-assurance CLI comes from, and line 34 says NIST comes with the default modules. The new low FND-011 asks for the release-binary route in addition. |
| FND-010 | fixed | Headings, install order, "Nothing", the Tool-produces definition, "Evidence checks are shallow", "not legal advice" and "Development" now match the US README. |
