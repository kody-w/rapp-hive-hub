---
id: source-reconciliation
title: Reconcile quote and account source facts
status: blocked
depends_on:
  - engagement-boundary
---

# Reconcile quote and account source facts

Room `discovery` (Process and requirements discovery). Blocked until [[engagement-boundary]] is done.

Reconcile keys and field meanings across accounts, headers, lines, and policy. Create a fact register distinguishing intentional bad-data fixtures, policy exceptions, and unknown real-world requirements.

## Inputs

- `deliverables/engagement-scope.md`, from [[engagement-boundary]]
- `docs/process-facts.md`: [[process-facts]]
- `data/accounts.csv`: [[accounts.csv]]
- `data/quotes.csv`: [[quotes.csv]]
- `data/quote-lines.csv`: [[quote-lines.csv]]
- `data/policy.json`: [[policy.json]]

## Outputs

- `deliverables/source-facts.csv`

## Acceptance

- All eight quotes and four accounts are covered without invented repairs.
- Missing PO and unknown tax on q-105 and negative quantity on q-107 are recorded.
- No synthetic policy is represented as tax or accounting advice.
