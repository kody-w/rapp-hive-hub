---
id: bound-material-assumptions
title: Review the inert BOM and assumed cost inputs
status: blocked
depends_on:
  - verify-parametric-fit
---

# Review the inert BOM and assumed cost inputs

Room `sourcing` (sourcing-planner). Blocked until [[verify-parametric-fit]] is done.

Review part quantities, modeled density, feedstock price, and yield assumptions. Produce a low/base/high assumption table with no named supplier, quotation, purchased part, or purchase instruction.

## Inputs

- `data/bom.csv`: [[bom.csv]]
- `data/cost-assumptions.csv`: [[cost-assumptions.csv]]
- `design/parameters.json`: [[parameters.json]]
- `deliverables/nominal-interface.json`, from [[verify-parametric-fit]]

## Outputs

- `deliverables/material-assumption-range.csv`

## Acceptance

- Retains one tray and one insert and labels every cost SYNTHETIC.
- Shows sensitivity to density, assumed price, and yield rather than claiming a vendor commitment.
