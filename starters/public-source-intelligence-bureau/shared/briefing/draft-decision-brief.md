---
id: draft-decision-brief
title: Draft a source-cited bounded decision brief
status: blocked
depends_on:
  - adjudicate-source-conflicts
---

# Draft a source-cited bounded decision brief

Room `briefing` (briefing-editor). Blocked until [[adjudicate-source-conflicts]] is done.

Use the briefing structure to answer the specific pilot question. Separate authored facts, document claims, inferences, and unknowns; offer conditional paths rather than unsupported certainty.

## Inputs

- `briefing/decision-template.md`: [[decision-template]]
- `case/question.json`: [[question.json]]
- `deliverables/annotated-timeline.csv`, from [[build-event-timeline]]
- `deliverables/benchmark-audit.json`, from [[verify-benchmark-arithmetic]]
- `deliverables/hypothesis-matrix.csv`, from [[compare-launch-hypotheses]]
- `deliverables/conflict-ledger.csv`, from [[adjudicate-source-conflicts]]

## Outputs

- `deliverables/pilot-decision-brief.md`

## Acceptance

- Every material statement has a file/row citation or is explicitly labeled inference/unknown.
- Does not endorse an unattended 72-hour pilot on the present corpus; any supervised alternative states its limitations and owner gate.
