---
id: review-five-day-recovery
title: Issue the bounded recovery decision
status: blocked
depends_on:
  - prepare-customer-drafts
  - model-containment-options
---

# Issue the bounded recovery decision

Room `product-recovery` (recovery-product-lead). Blocked until [[prepare-customer-drafts]], [[model-containment-options]] are done.

Join cash diagnosis, candidate quality, the capacity plan, response drafts, and containment scenarios into a hold/rework/candidate recommendation. Document what new evidence is needed after any separately approved sprint.

## Inputs

- `deliverables/cash-reconciliation.json`, from [[reconcile-synthetic-cash]]
- `deliverables/recovery-regression-results.csv`, from [[verify-recovery-handoff]]
- `deliverables/support-sprint-plan.json`, from [[plan-capacity-bounded-support]]
- `deliverables/customer-drafts.md`, from [[prepare-customer-drafts]]
- `deliverables/message-review-routing.csv`, from [[prepare-customer-drafts]]
- `deliverables/containment-scenarios.json`, from [[model-containment-options]]
- `ops/approval-gates.json`: [[approval-gates.json]]

## Outputs

- `deliverables/recovery-decision.md`

## Acceptance

- Names unresolved risks, baseline/candidate differences, and a measurement plan for real future work.
- Claims no realized profit, completed customer recovery, live deployment, or external authority.
