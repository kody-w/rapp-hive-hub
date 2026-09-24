---
id: prepare-customer-drafts
title: Prepare honest customer-response drafts
status: blocked
depends_on:
  - plan-capacity-bounded-support
  - set-cash-guardrails
---

# Prepare honest customer-response drafts

Room `customer-success` (customer-recovery-lead). Blocked until [[plan-capacity-bounded-support]], [[set-cash-guardrails]] are done.

Adapt the supplied response policy into incident-class drafts and a review routing sheet. Refer only to synthetic ticket IDs and avoid promises of resolution time, refunds, recovered money, or completed fixes.

## Inputs

- `ops/customer-response.md`: [[customer-response]]
- `ops/approval-gates.json`: [[approval-gates.json]]
- `deliverables/backlog-impact.csv`, from [[map-backlog-impact]]
- `deliverables/support-sprint-plan.json`, from [[plan-capacity-bounded-support]]
- `deliverables/cash-guardrails.json`, from [[set-cash-guardrails]]

## Outputs

- `deliverables/customer-drafts.md`
- `deliverables/message-review-routing.csv`

## Acceptance

- Covers urgent export failure, blocked reproduction, and low-priority cosmetic feedback with different truthful next steps.
- Labels every draft unsent and requires owner review before any actual customer communication or refund commitment.
