---
id: verify-recovery-handoff
title: Verify candidate queue behavior and rollback boundaries
status: blocked
depends_on:
  - repair-dispatch-candidate
  - plan-capacity-bounded-support
---

# Verify candidate queue behavior and rollback boundaries

Room `operations` (recovery-operations-lead). Blocked until [[repair-dispatch-candidate]], [[plan-capacity-bounded-support]] are done.

Execute the candidate's tests and replay the acceptance table against both the preserved baseline and candidate. Review capacity accounting and explain how an owner could hold the candidate without changing the reference.

## Inputs

- `quality/recovery-cases.csv`: [[recovery-cases.csv]]
- `ops/approval-gates.json`: [[approval-gates.json]]
- `deliverables/dispatch-candidate.py`, from [[repair-dispatch-candidate]]
- `deliverables/dispatch-candidate-tests.py`, from [[repair-dispatch-candidate]]
- `deliverables/support-sprint-plan.json`, from [[plan-capacity-bounded-support]]

## Outputs

- `deliverables/recovery-regression-results.csv`

## Acceptance

- Separates the intentionally failing legacy behavior from candidate pass/fail evidence.
- Records blocked-ticket, zero-capacity, duplicate-ID, deterministic-tie, and unknown-severity cases.
- Explicitly says production deployment and support execution have not occurred.
