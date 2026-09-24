---
id: repair-dispatch-candidate
title: Produce a minimal dispatcher candidate
status: blocked
depends_on:
  - agree-priority-rule
---

# Produce a minimal dispatcher candidate

Room `engineering` (recovery-engineer). Blocked until [[agree-priority-rule]] is done.

Implement the agreed severity ranking in a candidate module with narrow tests. Preserve the authored defective baseline as reproduction evidence; do not deploy or execute work against real accounts.

## Inputs

- `product/dispatch.py`: [[dispatch.py]]
- `tests/test_recovery.py`: [[test_recovery.py]]
- `quality/recovery-cases.csv`: [[recovery-cases.csv]]
- `deliverables/triage-policy.json`, from [[agree-priority-rule]]
- `deliverables/dispatch-reproduction.json`, from [[reproduce-dispatch-defect]]

## Outputs

- `deliverables/dispatch-candidate.py`
- `deliverables/dispatch-candidate-tests.py`

## Acceptance

- Rejects unknown severities and invalid limits, excludes blocked/non-open work, and handles ties deterministically.
- Returns ticket-001, ticket-010, ticket-007, and ticket-011 for the agreed four-item review batch.
- Makes no network, persistence, customer, or billing changes.
