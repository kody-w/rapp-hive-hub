---
id: reproduce-dispatch-defect
title: Reproduce severity alphabetization in the reference dispatcher
status: blocked
depends_on:
  - map-backlog-impact
---

# Reproduce severity alphabetization in the reference dispatcher

Room `engineering` (recovery-engineer). Blocked until [[map-backlog-impact]] is done.

Run the small authored product dispatcher through the analysis utility and create a minimal reproduction. Keep this baseline fixture separate from any candidate fix.

## Inputs

- `product/dispatch.py`: [[dispatch.py]]
- `tools/recovery.py`: [[recovery.py]]
- `tests/test_recovery.py`: [[test_recovery.py]]
- `quality/recovery-cases.csv`: [[recovery-cases.csv]]
- `deliverables/backlog-impact.csv`, from [[map-backlog-impact]]

## Outputs

- `deliverables/dispatch-reproduction.json`

## Acceptance

- Shows the legacy first four as ticket-009, ticket-002, ticket-006, and ticket-012, all low priority.
- Explains why string sorting places low before normal before urgent and shows the blocked row is excluded.
