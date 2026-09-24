---
id: set-cash-guardrails
title: Set runway and authority guardrails
status: blocked
depends_on:
  - reconcile-synthetic-cash
---

# Set runway and authority guardrails

Room `finance` (turnaround-finance-lead). Blocked until [[reconcile-synthetic-cash]] is done.

Reserve the prior-period catch-up obligations and compute the repeated-September runway to zero and to the owner's cash floor. Specify review triggers and prohibit automatic spending or cost actions.

## Inputs

- `case/recovery.json`: [[recovery.json]]
- `data/payables.csv`: [[payables.csv]]
- `ops/approval-gates.json`: [[approval-gates.json]]
- `deliverables/cash-reconciliation.json`, from [[reconcile-synthetic-cash]]

## Outputs

- `deliverables/cash-guardrails.json`

## Acceptance

- Reserves USD 5500 and reports USD 26900 available before the USD 12000 floor.
- Reports approximately 89.7 days to zero after reserves and 49.7 days to the floor using 30-day modeled months.
- Does not treat these mechanical scenarios as a forecast guarantee, solvency opinion, trade, or authorized financial action.
