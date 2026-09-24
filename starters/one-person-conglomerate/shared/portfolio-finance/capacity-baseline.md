---
id: capacity-baseline
title: Reconcile the allocation worksheet
status: blocked
depends_on:
  - portfolio-intake
---

# Reconcile the allocation worksheet

Room `portfolio-finance` (Shared finance). Blocked until [[portfolio-intake]] is done.

Check the ten candidate rows, money precision, selected flags, ordinal scores, and reserves. Produce a baseline reconciliation with totals and units before optimization.

## Inputs

- `deliverables/portfolio-intake.csv`, from [[portfolio-intake]]
- `data/allocation-worksheet.csv`: [[allocation-worksheet.csv]]
- `data/capacity.json`: [[capacity.json]]
- `docs/review-rubric.md`: [[review-rubric]]

## Outputs

- `deliverables/capacity-baseline.json`

## Acceptance

- The reference selection is lf-schema, fn-outline, and rp-sheet.
- It totals 19 hours and USD 90, leaving 13 discretionary hours and USD 410.
- Scores are not converted into revenue estimates.
