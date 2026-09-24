---
id: compare-launch-hypotheses
title: Compare full-offline, supervised-only, and schedule-slip explanations
status: blocked
depends_on:
  - build-event-timeline
---

# Compare full-offline, supervised-only, and schedule-slip explanations

Room `competing-hypotheses` (hypothesis-reviewer). Blocked until [[build-event-timeline]] is done.

Review the supplied hypothesis definitions and claim coding. Build a qualitative evidence matrix with disconfirming observations and evidence that would change the assessment; do not convert row counts to probabilities.

## Inputs

- `analysis/hypotheses.json`: [[hypotheses.json]]
- `analysis/claims.csv`: [[claims.csv]]
- `deliverables/evidence-index.json`, from [[build-provenance-index]]
- `deliverables/annotated-timeline.csv`, from [[build-event-timeline]]

## Outputs

- `deliverables/hypothesis-matrix.csv`

## Acceptance

- Covers all three hypotheses with supporting, contradictory, and non-discriminating evidence.
- Explicitly treats the lack of a dated fix as uncertainty rather than proof of a delay.
