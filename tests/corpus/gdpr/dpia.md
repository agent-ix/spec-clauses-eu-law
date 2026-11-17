---
id: example-invalid-DPIA-001
title: "Synthetic device-support processing impact assessment"
type: example
---
# Synthetic device-support processing impact assessment

## Processing and purpose

The synthetic service routes device-support requests to a human review team.
Requests may contain health data when needed to explain a device issue.

## Necessity and proportionality

The service collects request details needed for review, restricts access to
assigned reviewers, and removes records after the declared retention period.

## Risks and safeguards

Risks include disclosure of health data to an unintended recipient and use
beyond the support purpose. The synthetic controls use encryption at rest,
role-based access, and purpose-limited defaults.

## Residual risk decision

Named approver: person://example.invalid/people/privacy-officer

Approval reference: person://example.invalid/people/privacy-officer
