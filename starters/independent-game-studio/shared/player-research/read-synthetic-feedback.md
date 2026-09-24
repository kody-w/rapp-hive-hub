---
id: read-synthetic-feedback
title: Reproduce the authored feedback baseline
status: blocked
depends_on:
  - lock-first-shift
---

# Reproduce the authored feedback baseline

Room `player-research` (player-researcher). Blocked until [[lock-first-shift]] is done.

Run the local feedback utility and inspect every record. Attach counts and a coding note distinguishing author-generated feedback from observed research.

## Inputs

- `data/playtests.csv`: [[playtests.csv]]
- `tools/feedback_report.py`: [[feedback_report.py]]
- `deliverables/first-shift-scope.md`, from [[lock-first-shift]]

## Outputs

- `deliverables/feedback-baseline.json`
- `deliverables/feedback-coding.md`

## Acceptance

- Reports eight records, five completions, five bridge stalls, and three undo discoveries.
- Explains that the sample cannot establish market demand or an actual usability improvement.
