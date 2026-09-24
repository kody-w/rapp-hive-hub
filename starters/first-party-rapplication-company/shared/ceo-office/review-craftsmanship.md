---
id: review-craftsmanship
title: Critique the visible and hidden details
status: blocked
depends_on:
  - triage-feedback
---

# Critique the visible and hidden details

Room `ceo-office` (Founder-CEO office). Blocked until [[triage-feedback]] is done.

Review actual evidence with the craftsmanship rubric. Produce a recommendation and a preserved punch list with concrete loci, severity, ownership, expected behavior and evidence. Name one focus; a ship recommendation has no approval force.

## Inputs

- `deliverables/feedback.json`, from [[triage-feedback]]
- `deliverables/dogfood-scorecard.json`, from [[dogfood-chat]]
- `deliverables/candidate-manifest.json`, from [[build-candidate]]
- `docs/craftsmanship-rubric.md`: [[craftsmanship-rubric]]
- `templates/punch-list.json`: [[punch-list.json]]
- `templates/ceo-charter.md`: [[ceo-charter]]

## Outputs

- `deliverables/review.json`
- `deliverables/punch-list.json`

## Acceptance

- Unobserved dimensions remain not-observed; criticism targets the work, not people.
- The review inspects recovery, test quality, claims, licenses and simplicity as well as chat copy.
- The recommendation is ship/iterate/stop, never a self-issued release approval.
