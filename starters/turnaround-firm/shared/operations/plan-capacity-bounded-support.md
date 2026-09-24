---
id: plan-capacity-bounded-support
title: Plan the 420-minute support slice
status: blocked
depends_on:
  - agree-priority-rule
---

# Plan the 420-minute support slice

Room `operations` (recovery-operations-lead). Blocked until [[agree-priority-rule]] is done.

Run the candidate triage simulation under the approved-for-review policy and map the chosen work to the five-day sprint skeleton. Keep blocked and capacity-deferred tickets visible.

## Inputs

- `data/support-backlog.csv`: [[support-backlog.csv]]
- `ops/recovery-sprint.csv`: [[recovery-sprint.csv]]
- `tools/recovery.py`: [[recovery.py]]
- `deliverables/triage-policy.json`, from [[agree-priority-rule]]

## Outputs

- `deliverables/support-sprint-plan.json`

## Acceptance

- Selects ticket-001, ticket-010, ticket-007, ticket-011, ticket-005, and ticket-008 for exactly 420 estimated minutes.
- Retains one blocked and five capacity-deferred tickets; it reports no actual completion or resolution.
- Keeps the separate 360-minute engineering budget distinct from support capacity.
