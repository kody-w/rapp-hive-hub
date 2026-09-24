---
id: candidate-acceptance
title: Evaluate a candidate against the strict contract
status: blocked
depends_on:
  - ordering-repair
  - input-boundary-review
---

# Evaluate a candidate against the strict contract

Room `release` (Acceptance and release operations). Blocked until [[ordering-repair]], [[input-boundary-review]] are done.

Apply reviewed patches only to the consumer's explicitly selected candidate copy, then run strict acceptance and regression tests. Record actual evidence or a blocker; the seed reference itself remains the historical failing baseline.

## Inputs

- `deliverables/deduplication.patch`, from [[deduplication-repair]]
- `deliverables/ordering.patch`, from [[ordering-repair]]
- `deliverables/input-boundary-review.md`, from [[input-boundary-review]]
- `reference/check_acceptance.py`: [[check_acceptance.py]]
- `data/expected-contract.json`: [[expected-contract.json]]
- `reference/test_baseline.py`: [[test_baseline.py]]
- `docs/release-checklist.md`: [[release-checklist]]

## Outputs

- `deliverables/candidate-acceptance.json`

## Acceptance

- Strict checker exit 0 and every desired contract case are required for pass.
- Regression expectations are updated to fixed behavior without weakening contract targets.
- No missing candidate, failed test, or unperformed check is represented as release-ready.
