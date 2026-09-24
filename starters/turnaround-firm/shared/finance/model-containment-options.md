---
id: model-containment-options
title: Model containment without claiming savings
status: blocked
depends_on:
  - verify-recovery-handoff
  - set-cash-guardrails
---

# Model containment without claiming savings

Room `finance` (turnaround-finance-lead). Blocked until [[verify-recovery-handoff]], [[set-cash-guardrails]] are done.

Compare the repeated-September scenario to the supplied lower contractor/hosting assumption. Explain the approval and operational evidence needed, using regression results as a constraint rather than treating them as achieved financial value.

## Inputs

- `data/scenarios.csv`: [[scenarios.csv]]
- `tools/recovery.py`: [[recovery.py]]
- `ops/approval-gates.json`: [[approval-gates.json]]
- `deliverables/cash-guardrails.json`, from [[set-cash-guardrails]]
- `deliverables/recovery-regression-results.csv`, from [[verify-recovery-handoff]]

## Outputs

- `deliverables/containment-scenarios.json`

## Acceptance

- Shows USD 9000 versus USD 7300 modeled monthly burn, a USD 1700 difference, and the associated cash-floor sensitivity.
- Marks contractor and hosting changes unapproved and includes no actual cancellation, transfer, purchase, sale, trade, or profit claim.
