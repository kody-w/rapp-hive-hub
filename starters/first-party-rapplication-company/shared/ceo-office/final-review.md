---
id: final-review
title: Review final evidence and preserve every finding
status: blocked
depends_on:
  - final-dogfood
---

# Review final evidence and preserve every finding

Room `ceo-office` (Founder-CEO office). Blocked until [[final-dogfood]] is done.

Review the final subject, dogfood and iteration evidence. Carry every prior finding forward with an evidenced disposition. Recommend ship only with mandatory criteria met; otherwise request successor tasks and retain the blocked gate.

## Inputs

- `deliverables/final-dogfood.json`, from [[final-dogfood]]
- `deliverables/final-candidate.json`, from [[revise-candidate]]
- `deliverables/iteration-evidence.json`, from [[revise-candidate]]
- `deliverables/review.json`, from [[review-craftsmanship]]
- `deliverables/punch-list.json`, from [[review-craftsmanship]]
- `docs/craftsmanship-rubric.md`: [[craftsmanship-rubric]]
- `templates/punch-list.json`: [[punch-list.json]]

## Outputs

- `deliverables/final-review.json`
- `deliverables/final-punch-list.json`

## Acceptance

- No open blocker/major finding is hidden, deleted, or relabeled to allow shipment.
- Current-subject evidence supports every resolution.
- A favorable recommendation still requires independent verification and a separate decision.
