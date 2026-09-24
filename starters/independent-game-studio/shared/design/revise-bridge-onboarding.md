---
id: revise-bridge-onboarding
title: Specify bridge and carrying onboarding
status: blocked
depends_on:
  - read-synthetic-feedback
---

# Specify bridge and carrying onboarding

Room `design` (game-designer). Blocked until [[read-synthetic-feedback]] is done.

Write an exact first-minute interaction specification using the current four-beat bridge rule. Include blocked movement, standing on a closing bridge, depot reload, and undo.

## Inputs

- `design/rules.md`: [[rules]]
- `case/production.json`: [[production.json]]
- `deliverables/feedback-baseline.json`, from [[read-synthetic-feedback]]
- `deliverables/feedback-coding.md`, from [[read-synthetic-feedback]]

## Outputs

- `deliverables/onboarding-spec.md`

## Acceptance

- A player can determine whether the next bridge entry is legal from visible text.
- Each rule has an example action/state pair and does not change the three level layouts.
