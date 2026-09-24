---
id: allocation-proposal
title: Prepare a reasoned founder allocation
status: blocked
depends_on:
  - allocation-analysis
  - uncertainty-audit
---

# Prepare a reasoned founder allocation

Room `portfolio-finance` (Shared finance). Blocked until [[allocation-analysis]], [[uncertainty-audit]] are done.

Produce a complete ten-row proposed worksheet with selected flags and a rationale column. Accept or override the mathematical recommendation explicitly; if estimates change, retain the original values alongside proposed values.

## Inputs

- `deliverables/allocation-analysis.json`, from [[allocation-analysis]]
- `deliverables/uncertainty-register.csv`, from [[uncertainty-audit]]
- `data/allocation-worksheet.csv`: [[allocation-worksheet.csv]]
- `docs/decision-template.json`: [[decision-template.json]]

## Outputs

- `deliverables/allocation-proposal.csv`

## Acceptance

- The proposal contains all ten stable experiment IDs.
- At most one experiment per unit and three active units are selected.
- Any override includes a reason and preserves the protected reserves.
