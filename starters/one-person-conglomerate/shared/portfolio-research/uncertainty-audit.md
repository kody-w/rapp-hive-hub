---
id: uncertainty-audit
title: Turn assumed demand into falsifiable questions
status: blocked
depends_on:
  - portfolio-intake
---

# Turn assumed demand into falsifiable questions

Room `portfolio-research` (Shared research). Blocked until [[portfolio-intake]] is done.

Reconcile every evidence-register row with the intake. For each unit choose one question that a low-cost experiment could disconfirm. Distinguish offline artifact inspection from later consented customer research.

## Inputs

- `deliverables/portfolio-intake.csv`, from [[portfolio-intake]]
- `data/evidence-register.csv`: [[evidence-register.csv]]
- `docs/review-rubric.md`: [[review-rubric]]

## Outputs

- `deliverables/uncertainty-register.csv`

## Acceptance

- All ten assumption rows are accounted for.
- Every unit has a disconfirming observation and a stop condition.
- No synthetic observation is promoted to external validation.
