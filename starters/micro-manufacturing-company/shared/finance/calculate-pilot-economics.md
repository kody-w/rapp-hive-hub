---
id: calculate-pilot-economics
title: Reproduce a hypothetical 20-kit cost baseline
status: blocked
depends_on:
  - bound-material-assumptions
  - check-pack-envelope
---

# Reproduce a hypothetical 20-kit cost baseline

Room `finance` (cost-analyst). Blocked until [[bound-material-assumptions]], [[check-pack-envelope]] are done.

Compute material including yield loss, handling, packaging, overhead, and a bounded sensitivity range. Round after aggregation and keep projected contribution separate from realized profit.

## Inputs

- `data/cost-assumptions.csv`: [[cost-assumptions.csv]]
- `data/bom.csv`: [[bom.csv]]
- `case/brief.json`: [[brief.json]]
- `tools/plan.py`: [[plan.py]]
- `deliverables/material-assumption-range.csv`, from [[bound-material-assumptions]]
- `deliverables/packing-assessment.json`, from [[check-pack-envelope]]

## Outputs

- `deliverables/pilot-cost-scenarios.json`

## Acceptance

- Baseline modeled solid mass is 151.67184 g, displayed unit cost is USD 7.61, and the 20-kit aggregate is USD 152.13.
- Explains why multiplying a rounded unit display differs from rounding the unrounded batch total.
- Marks all economics hypothetical; creates no purchase, sale, or profit claim.
