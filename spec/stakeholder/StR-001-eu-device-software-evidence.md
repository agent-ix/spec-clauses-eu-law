---
id: StR-001
title: "Device manufacturers need reviewable software and cybersecurity evidence"
type: StR
relationships:
  - target: "ix://agent-ix/spec-clauses-eu-law/US-001"
    type: "satisfied_by"
---
# StR-001: Device manufacturers need reviewable software and cybersecurity evidence

## Stakeholder Need

Medical-device manufacturers need a review that identifies the software-
related and cybersecurity evidence expected for a device and the records that
support each expectation, so reviewers can assess the device documentation
and unresolved work.

## Rationale

Manufacturers prepare and maintain technical documentation across design,
verification, use, and post-market activities. They need a reviewable way to
connect public regulatory sources and non-binding guidance to their own
requirements, architecture, risk, verification, and instructions-for-use
records. This need does not ask a tool or a pack to decide legal compliance.

## Validation Criteria

| ID | Criteria | Validation |
|----|----------|------------|
| StR-001-VC-1 | A manufacturer reviewer can identify the source clause, its applicability, and the evidence or customer-owned action expected for each in-scope item. | Demonstration |
| StR-001-VC-2 | Missing applicability or evidence is visible for review and is not presented as an automatic compliance decision. | Demonstration |

## Stakeholders

The primary stakeholder is a medical-device manufacturer responsible for
software-related technical documentation. Reviewers and operators who prepare,
assess, or use the device documentation are affected parties.

## Context and Assumptions

The manufacturer determines product facts and applicability. Public legislation
and the cited MDCG guidance provide source references; the manufacturer remains
responsible for interpreting obligations and making decisions.

## Dependencies

The need is answered by US-001. The functional requirements in this
specification refine the source, applicability, evidence, and documentation
information needed for that review.

## Traceability

This stakeholder need is satisfied by [US-001](../usecase/US-001-review-device-software-evidence.md).
