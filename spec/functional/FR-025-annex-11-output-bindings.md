---
id: FR-025
title: "Annex 11 output bindings"
type: FR
relationships:
  - target: "ix://agent-ix/spec-clauses-eu-law/US-001"
    type: "traces_to"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-024"
    type: "depends_on"
  - target: "ix://agent-ix/spec-clauses-eu-law/FR-006"
    type: "depends_on"
---
# FR-025: Annex 11 output bindings

## Description

The pack SHALL declare every expected output used by the Annex 11 set in the EU Pack Output Catalog. The Annex 11 Output Bindings table in `spec.md` SHALL name, for each output, the quoin, quire or engineering-assurance command that produces it today in a producer-command column, or `none` when the output is customer-supplied; non-command inputs go in a separate source column. The pack SHALL NOT name a producer that does not exist. Outputs that also exist in the US Health-Law Output Catalog SHALL keep that catalog's kind and description. Each binding's limit SHALL reach the shipped pack: in the catalog description for names used only by Annex 11, and in the closing `Tool limit:` sentence of the clause text for shared names. No binding SHALL state or imply that a tool decides compliance, scores, classifies, or accepts a risk.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-025-AC-1 | Every expected output in the Annex 11 Clause Table resolves in the catalog and the set's subset equals the catalog definition. | Test |
| FR-025-AC-2 | Every name shared with the US Health-Law Output Catalog, including `verification-records`, `risk-management-records`, `software-requirements`, `software-architecture`, `anomaly-list` and `release-record`, has identical kind and description to the US Health-Law Output Catalog definition; a mismatch fixture fails and names the output and field. | Test |
| FR-025-AC-3 | These outputs are customer-supplied and name no producer command: `system-validation` (record), `access-control` (record), `system-access-control` (record), `written-procedure` (procedure), `training-record` (procedure), `supplier-agreement`, `supplier-assessment`, `system-inventory`, `backup-restore-record`, `periodic-evaluation-record`, `business-continuity-plan`, `archive-verification-record` and `batch-certification-record` (all procedure). | Inspection |
| FR-025-AC-4 | Each command in the producer-command column of the bindings table exists in the installed `quoin`, `quire` or `engineering-assurance` command list; an absent command fails and names the output. | Test |
| FR-025-AC-5 | No Annex 11 summary or binding text states or implies a compliance verdict, score, class or acceptance made by a tool. | Inspection |
| FR-025-AC-6 | The catalog description of each Annex 11-only name carries its limit from the bindings table. For every shared output whose bindings row has a limit other than `None`, whether or not a command produces it, every clause in the Annex 11 Clause Table whose expected outputs include that output ends its text with that output's sentence from Annex 11 Tool Limits; the clause list is derived from the bindings and clause tables, and a missing sentence fails and names the clause and output. | Test |
| FR-025-AC-7 | Clauses `12.1` and `12.2` name `system-access-control` and not `access-control`, because they restrict access to the computerised system and not to the repository; `7.1` and `12.3` keep `access-control`. | Test |

## Dependencies

Catalog contract: [FR-006](./FR-006-pack-wide-output-catalog.md). Clause table: [FR-024](./FR-024-annex-11-clause-table-and-applicability.md). Producers are measured against the installed tools; a producer that is missing is reported and the output stays customer-supplied.
