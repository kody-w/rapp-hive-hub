---
id: define-inspection-gates
title: Derive a dimensional inspection sheet
status: blocked
depends_on:
  - verify-parametric-fit
---

# Derive a dimensional inspection sheet

Room `quality` (quality-engineer). Blocked until [[verify-parametric-fit]] is done.

Check the nominal tolerances against the model and write a sampling/measurement sheet with explicit acceptance boundaries. A synthetic row is not a measurement of a real object.

## Inputs

- `quality/dimensions.csv`: [[dimensions.csv]]
- `design/parameters.json`: [[parameters.json]]
- `ops/assembly.md`: [[assembly]]
- `deliverables/nominal-interface.json`, from [[verify-parametric-fit]]

## Outputs

- `deliverables/inspection-plan.csv`

## Acceptance

- Covers tray width, depth, height, per-side insert clearance, and visible edge defects.
- Defines both lower and upper limits and identifies the instruments/methods as a future review need.
