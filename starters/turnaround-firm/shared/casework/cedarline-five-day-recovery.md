---
id: cedarline-five-day-recovery
title: "Cedarline Desk: cash containment and a broken support dispatch queue"
---

# Cedarline Desk: cash containment and a broken support dispatch queue

SYNTHETIC case at 2026-09-30: Cedarline Desk has declining subscription receipts, increasing refunds, USD 32400 closing cash, and twelve authored open tickets. Its actual small reference dispatcher alphabetizes severity, sending low-priority tickets ahead of urgent ones. A five-day planning sprint has 360 engineering minutes and 420 support-remediation minutes. No production account, money, trade, customer message, or realized recovery is involved.

## Inputs

- `case/recovery.json`: [[recovery.json]]
- `data/cash-ledger.csv`: [[cash-ledger.csv]]
- `data/subscriptions.csv`: [[subscriptions.csv]]
- `data/payables.csv`: [[payables.csv]]
- `data/support-backlog.csv`: [[support-backlog.csv]]
- `product/dispatch.py`: [[dispatch.py]]

## Success criteria

- Fifteen synthetic cash rows reconcile USD 52000 opening cash plus USD 48500 receipts less USD 68100 payments to USD 32400 closing cash.
- USD 5500 incremental prior-period payables are reserved separately; runway to the USD 12000 floor is about 49.7 days under the repeated-September scenario.
- The alphabetical dispatch defect is reproducible and a candidate policy prioritizes eligible urgent tickets without dispatching a blocked ticket.
- The support simulation selects six tickets totaling exactly 420 estimated minutes and retains all other tickets as blocked or deferred.
- Any proposed USD 1700 monthly containment difference remains an approval-dependent scenario, not achieved savings, profit, sales, or executed financial activity.

## Tasks

- [[reconcile-synthetic-cash]] Reconcile the three-month cash and subscription baseline (`finance`, ready)
- [[set-cash-guardrails]] Set runway and authority guardrails (`finance`, blocked)
- [[model-containment-options]] Model containment without claiming savings (`finance`, blocked)
- [[map-backlog-impact]] Map the authored backlog to recovery risk (`product-recovery`, ready)
- [[agree-priority-rule]] Agree the narrow recovery triage rule (`product-recovery`, blocked)
- [[review-five-day-recovery]] Issue the bounded recovery decision (`product-recovery`, blocked)
- [[reproduce-dispatch-defect]] Reproduce severity alphabetization in the reference dispatcher (`engineering`, blocked)
- [[repair-dispatch-candidate]] Produce a minimal dispatcher candidate (`engineering`, blocked)
- [[plan-capacity-bounded-support]] Plan the 420-minute support slice (`operations`, blocked)
- [[verify-recovery-handoff]] Verify candidate queue behavior and rollback boundaries (`operations`, blocked)
- [[prepare-customer-drafts]] Prepare honest customer-response drafts (`customer-success`, blocked)

No reference artifact counts as completed work without review.
