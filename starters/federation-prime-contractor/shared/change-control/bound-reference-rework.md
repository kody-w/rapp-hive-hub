---
id: bound-reference-rework
title: Bound the rejection-to-rework cycle
status: blocked
depends_on:
  - rehearse-explicit-rejection
---

# Bound the rejection-to-rework cycle

Room `change-control` (change-controller). Blocked until [[rehearse-explicit-rejection]] is done.

Review the rejection report and original change/risk rows. Specify minimal corrections, affected dependents, and renewed review gates; do not silently weaken the acceptance matrix.

## Inputs

- `ops/change-requests.csv`: [[change-requests.csv]]
- `ops/risk-register.csv`: [[risk-register.csv]]
- `interfaces/pilot.json`: [[pilot.json]]
- `deliverables/rejection-rehearsal.json`, from [[rehearse-explicit-rejection]]

## Outputs

- `deliverables/reference-rework-plan.json`

## Acceptance

- Proposes retention 120 and interface version 1, retaining both original failures as evidence.
- Identifies downstream pilot-kit/integration checks that must rerun.
- Does not approve the separate request to increase attendance to 90 or alter owner authority.
