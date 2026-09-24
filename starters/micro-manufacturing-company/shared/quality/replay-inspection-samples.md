---
id: replay-inspection-samples
title: Classify the synthetic gauge exercise
status: blocked
depends_on:
  - define-inspection-gates
---

# Classify the synthetic gauge exercise

Room `quality` (quality-engineer). Blocked until [[define-inspection-gates]] is done.

Use the planner and included authored sample rows to reproduce conformance decisions. Explain each rejection and the treatment of unmeasured characteristics.

## Inputs

- `quality/inspection-samples.csv`: [[inspection-samples.csv]]
- `quality/dimensions.csv`: [[dimensions.csv]]
- `tools/plan.py`: [[plan.py]]
- `deliverables/inspection-plan.csv`, from [[define-inspection-gates]]

## Outputs

- `deliverables/synthetic-inspection-results.csv`

## Acceptance

- Rows 01, 02, and 05 pass the specified synthetic checks; row 03 fails width and row 04 fails fit clearance.
- Does not label any real batch accepted or assume that a scenario width change is covered by these baseline samples.
