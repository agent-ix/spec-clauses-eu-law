---
id: US-001
title: "Review device software and cybersecurity evidence"
type: US
relationships:
  - target: "ix://agent-ix/spec-clauses-eu-law/StR-001"
    type: "traces_to"
---
# US-001: Review device software and cybersecurity evidence

## Story

**As a** medical-device manufacturer reviewing a software-containing device
**I want** to map each in-scope source requirement to its applicability and
supporting documentation
**So that** I can assess the technical file and unresolved work without an
automated compliance decision.

## Context

The manufacturer supplies the product facts and the supporting records. The
pack provides a structured view of public MDR provisions and the selected
MDCG guidance sections. It does not determine whether a device or manufacturer
is legally compliant.

## Acceptance Examples (Illustrative)

### US-001-EX-1: Review a supported requirement

- **Given** an applicable requirement with its supporting record
- **When** the manufacturer reviews the mapping
- **Then** the source, applicability, and expected evidence are visible together

### US-001-EX-2: Review an unresolved requirement

- **Given** a requirement whose applicability or evidence has not been supplied
- **When** the manufacturer reviews the mapping
- **Then** the unresolved information remains visible for a person to decide

## Traceability (Informative)

This story traces to StR-001. FR-001 through FR-008 define the module, rights,
sets, applicability, outputs, customer-owned actions, and corpus that support
the story. NFR-001 constrains the rights and content boundary.
