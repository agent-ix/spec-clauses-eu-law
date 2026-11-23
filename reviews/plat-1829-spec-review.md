---
id: SR-034
title: "Spec review — GDPR clause set re-audit"
type: SpecReview
analysis: base
scope: "agent-ix/spec-clauses-eu-law; PR #26 at b249533c14d97ef55d58a8a344f747e5056e6757; spec/spec.md GDPR table, bindings paragraph and output catalog; FR-010, FR-012, FR-013"
review_set: subset
date: 2026-11-23
relationships:
  - { target: "ix://agent-ix/spec-clauses-eu-law/FR-012", type: references }
---

## Summary

Ticket: PLAT-1829. Spec review of the GDPR output bindings. The pass covered integrity, EARS and scope boundary, with checks against the spec-clauses-us-health origin/main ephi-access-control precedent, against quoin origin/main FR-208, and against the pack's Annex 11 set. `quire validate` passes on all four changed spec files.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | art-32(1)(c) (restore availability and access after an incident) names no backup or restore output. The pack already declares the customer-supplied backup-restore-record for Annex 11 7.2. | spec/spec.md:106 |
| FND-002 | medium | FR-012-AC-2 specifies a quoin behaviour that the pack cannot affect: quoin rejects any accepted_risk disposition without an approvalRef at record time, whatever approvalRoles says. The AC also calls this undischarged, but it is a record-time rejection. | spec/functional/FR-012-human-dpia-risk-acceptance.md:30 |
| FND-003 | low | FR-012 and the spec.md bindings paragraph use status wording that will go stale: "today (quoin FR-208)", "once quoin FR-211 ships", "not tested here until it ships". | spec/functional/FR-012-human-dpia-risk-acceptance.md:19-30 |
| FND-004 | low | FR-010-AC-3 bundles two obligations (the art-32(4) mapping and the producer statements). It also says access-control is "not bound", while the change removes it from the GDPR catalog and the test asserts that removal. | spec/functional/FR-010-gdpr-clause-table.md:28 |

## Finding details

### FND-001 — spec.md#gdpr-clause-table-art-32-1-c

Art 32(1)(c) concerns the ability to restore availability and access in a timely manner. Its expected outputs are security-risk-records and verification-records, and neither of those evidences restoration. backup-restore-record already exists in this pack ("Customer-owned evidence that backups are taken and restoration is checked; no quoin, quire or engineering-assurance command produces it.", kind procedure).

Expected fix: In this PR, add backup-restore-record to art-32(1)(c) in the spec table and the JSON. Add the catalog entry to the GDPR set with the Annex 11 kind and description verbatim (the same-name rule), and extend FR-010-AC-3 or add an AC plus a test assertion. The clause keeps its record outputs, so it does not become customer-owned-only.

### FND-002 — FR-012-AC-2

Probe result: an art-35(1) accepted_risk disposition with approvalRef missing, "" or "   " is rejected by `quoin evidence record-discharge` with an identical error with and without approvalRoles.

Expected fix: Delete FR-012-AC-2. Reword the Description from "a fact or disposition discharges only with" to "a direct fact on an approval-role clause discharges only with". The pack's obligation is AC-1: declare the role.

### FND-003 — FR-012

These phrases describe the delivery state of another repository. quoin FR-208 already specifies the target: discharge requires an approvalRef that verifies under FR-211.

Expected fix: State the target once, for example: "Quoin discharges an approval-role clause only when its approvalRef verifies under quoin FR-208 and FR-211; the pack declares the role and does not check approvals." Keep the ACs to what is observable: missing or blank leaves the clause undischarged.

### FND-004 — FR-010-AC-3

Expected fix: Split the AC into (a) art-32(4) names processing-access-control, and the GDPR output catalog does not declare access-control; and (b) the privacy-by-default-settings and processing-access-control descriptions state that no toolchain producer exists.

## Verdict

Changes requested on FND-001 and FND-002. These parts are honest and correct:

- processing-access-control mirrors the US ephi-access-control precedent: customer-authored spec-objects-security records or customer-supplied evidence, and the clause set defines no producer. Narrowing it to security.role and security.permission fits Art 32(4)'s "acting under the authority / on instructions".
- privacy-by-default-settings is described as customer-supplied with no producer, and its corpus record carries `suppliedBy: customer`.
- art-30(4) gains written-procedure.
- FR-013 drops the ticket narration and names the real `quoin dossier generate --doc records-of-processing` producer.
- Both changed or new catalog names are EU-only (absent from spec-clauses-us-health origin/main), so FR-006-AC-3 shared descriptions are unchanged.
- No clause text was added or copied, no tool-assigned verdict appears, no ticket ids appear in public prose, and nothing is vendored.

Out of this PR, recommended as a follow-up ticket: the Annex 11 set binds repository access-control to 12.1 and 12.2. Those clauses restrict access to the regulated computerised system, which is the same dev-repo-versus-product mismatch. 7.1 and 12.3 keep a real tie wherever the toolchain's signed records are the GMP record store.

## Scope examined

- spec.md#gdpr-clause-table (examined)
- spec.md#gdpr-output-bindings-paragraph (examined)
- spec.md#eu-pack-output-catalog (examined)
- FR-010 (examined)
- FR-010-AC-3 (examined)
- FR-010-AC-4 (examined)
- FR-012 (examined)
- FR-012-AC-1 (examined)
- FR-012-AC-2 (examined)
- FR-012-AC-3 (examined)
- FR-013 (examined)
