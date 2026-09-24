---
id: requirements-trace
title: Build field-to-requirement traceability
status: blocked
depends_on:
  - source-reconciliation
---

# Build field-to-requirement traceability

Room `discovery` (Process and requirements discovery). Blocked until [[source-reconciliation]] is done.

Map the supplied requirements to source fields, process facts, and the eight acceptance cases. Mark any new requirement as proposed and name the role that must resolve it.

## Inputs

- `deliverables/source-facts.csv`, from [[source-reconciliation]]
- `docs/requirements.csv`: [[requirements.csv]]
- `docs/acceptance-cases.md`: [[acceptance-cases]]
- `docs/handoff-contracts.md`: [[handoff-contracts]]

## Outputs

- `deliverables/requirements-trace.csv`

## Acceptance

- Every supplied requirement has at least one acceptance case.
- Data readiness and policy review are separate requirements.
- Unresolved policy questions are not silently converted into defaults.
