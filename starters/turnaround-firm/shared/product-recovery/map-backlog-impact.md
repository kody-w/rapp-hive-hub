---
id: map-backlog-impact
title: Map the authored backlog to recovery risk
status: ready
depends_on: []
---

# Map the authored backlog to recovery risk

Room `product-recovery` (recovery-product-lead). Ready to claim: it depends on nothing.

Review ticket severity, age, affected-account counts, and dependencies. Do not sum overlapping affected-account counts into unique customers or assert that a support fix recovers revenue.

## Inputs

- `data/support-backlog.csv`: [[support-backlog.csv]]
- `case/recovery.json`: [[recovery.json]]
- `quality/recovery-cases.csv`: [[recovery-cases.csv]]

## Outputs

- `deliverables/backlog-impact.csv`

## Acceptance

- Covers twelve open tickets, four urgent rows, and the one blocked urgent ticket.
- Connects the dispatch behavior to delayed urgent work without inventing churn attribution or actual customer harm.
