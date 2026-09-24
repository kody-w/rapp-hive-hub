---
id: qc
title: Run the quality gates
status: blocked
depends_on:
  - claims-carryover
---

# Run the quality gates

Room `quality` (reviewer). Blocked until [[claims-carryover]] is done.

Walk the review checklist: lint, check, duration, hook, caption trace and style, zones, claim carryover, loudness, and a contact sheet with one frame per beat compared against the approved board.

## Inputs

- `deliverables/cut/short.json`, from [[motion-graphics]]
- `deliverables/captions/captions.json`, from [[captions]]
- `deliverables/claims/carryover.json`, from [[claims-carryover]]
- `deliverables/approvals/motion-board.md`, from [[board-approval]]
- `quality/review-checklist.csv`: [[review-checklist.csv]]

## Outputs

- `deliverables/qc/report.json`
- `deliverables/qc/contact-sheet.png`

## Acceptance

- Every checklist row has a pass or a documented fail with evidence.
- The contact sheet shows one frame per board beat.
