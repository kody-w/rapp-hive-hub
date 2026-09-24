---
id: verify-parametric-fit
title: Verify the tray and lift-out insert model
status: blocked
depends_on:
  - freeze-desk-use
---

# Verify the tray and lift-out insert model

Room `engineering` (design-engineer). Blocked until [[freeze-desk-use]] is done.

Run the planner and tests, inspect the authored SCAD, and produce a dimensional interface report. The model estimates solid geometry only; do not imply process qualification.

## Inputs

- `design/parameters.json`: [[parameters.json]]
- `design/desk-caddy.scad`: [[desk-caddy.scad]]
- `tools/plan.py`: [[plan.py]]
- `tests/test_plan.py`: [[test_plan.py]]
- `deliverables/desk-use-requirements.md`, from [[freeze-desk-use]]

## Outputs

- `deliverables/nominal-interface.json`

## Acceptance

- Reports a 174 by 94 mm tray interior and 171 by 91 mm insert footprint.
- Reports nominal side clearance 1.5 mm, tray volume 101676 mm3, and insert volume 20640 mm3.
- Separates mathematical checks from any unrun CAD renderer or physical fit test.
