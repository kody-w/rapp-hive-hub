---
id: build-event-timeline
title: Reconstruct promise, preview, and correction chronology
status: blocked
depends_on:
  - build-provenance-index
---

# Reconstruct promise, preview, and correction chronology

Room `analysis` (technology-analyst). Blocked until [[build-provenance-index]] is done.

Generate the local timeline and annotate changes in claim scope through the as-of date. Separate announcement date, proposed launch date, and measurement date.

## Inputs

- `tools/evidence.py`: [[evidence.py]]
- `case/question.json`: [[question.json]]
- `deliverables/evidence-index.json`, from [[build-provenance-index]]
- `deliverables/citation-audit.json`, from [[build-provenance-index]]

## Outputs

- `deliverables/annotated-timeline.csv`

## Acceptance

- Shows the 1 September promise, 8 September credential condition, 12 September workaround, 14 September undated fix, and 17 September missing long-run evidence.
- Does not infer an observed launch or a confirmed schedule from future-facing text.
