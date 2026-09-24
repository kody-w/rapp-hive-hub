---
id: reconcile-synthetic-cash
title: Reconcile the three-month cash and subscription baseline
status: ready
depends_on: []
---

# Reconcile the three-month cash and subscription baseline

Room `finance` (turnaround-finance-lead). Ready to claim: it depends on nothing.

Run the authored analysis utility and tests, reconcile every synthetic transaction to monthly plan counts, and distinguish cash receipts from general revenue-recognition claims.

## Inputs

- `case/recovery.json`: [[recovery.json]]
- `data/cash-ledger.csv`: [[cash-ledger.csv]]
- `data/subscriptions.csv`: [[subscriptions.csv]]
- `data/payables.csv`: [[payables.csv]]
- `tools/recovery.py`: [[recovery.py]]
- `tests/test_recovery.py`: [[test_recovery.py]]

## Outputs

- `deliverables/cash-reconciliation.json`

## Acceptance

- Reproduces opening 52000, receipts 48500, payments 68100, and closing 32400 USD.
- Reports monthly net cash of -4000, -6600, and -9000 USD with the explicit fixture assumption that subscription billings were collected in-month.
- Keeps incremental unpaid prior-period obligations outside the cash-ledger payments.
