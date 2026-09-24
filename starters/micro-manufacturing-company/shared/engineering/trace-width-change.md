---
id: trace-width-change
title: Trace the 196 mm width request through dependencies
status: blocked
depends_on:
  - define-inspection-gates
  - calculate-pilot-economics
---

# Trace the 196 mm width request through dependencies

Room `engineering` (design-engineer). Blocked until [[define-inspection-gates]], [[calculate-pilot-economics]] are done.

Run the width scenario and map impacts to geometry, BOM mass, fit nominal, quality limits, economics, and packing. Do not silently overwrite the baseline or reuse its synthetic inspection rows as proof for the changed design.

## Inputs

- `ops/change-request.json`: [[change-request.json]]
- `tools/plan.py`: [[plan.py]]
- `ops/pack-spec.json`: [[pack-spec.json]]
- `deliverables/nominal-interface.json`, from [[verify-parametric-fit]]
- `deliverables/inspection-plan.csv`, from [[define-inspection-gates]]
- `deliverables/pilot-cost-scenarios.json`, from [[calculate-pilot-economics]]

## Outputs

- `deliverables/width-change-impact.json`

## Acceptance

- Shows that 196 mm plus two 2 mm pads exceeds the 192 mm packing interior.
- Names the tasks that must be reopened if the design or packaging changes.
- Reports changed mass/cost and the absence of physical validation.
