---
id: agree-priority-rule
title: Agree the narrow recovery triage rule
status: blocked
depends_on:
  - reproduce-dispatch-defect
  - set-cash-guardrails
---

# Agree the narrow recovery triage rule

Room `product-recovery` (recovery-product-lead). Blocked until [[reproduce-dispatch-defect]], [[set-cash-guardrails]] are done.

Define severity ranking, oldest-first ties, blocked exclusions, deterministic identifiers, and capacity handling. Reconcile the policy with cash and customer-risk constraints before changing code.

## Inputs

- `deliverables/backlog-impact.csv`, from [[map-backlog-impact]]
- `deliverables/dispatch-reproduction.json`, from [[reproduce-dispatch-defect]]
- `deliverables/cash-guardrails.json`, from [[set-cash-guardrails]]
- `case/recovery.json`: [[recovery.json]]

## Outputs

- `deliverables/triage-policy.json`

## Acceptance

- Orders eligible urgent before normal before low; same-severity work is oldest first with deterministic ties.
- Defines the non-preemptive fit rule and records that a larger deferred ticket is not silently completed or discarded.
