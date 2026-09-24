---
id: verify-game-regressions
title: Execute rule and input acceptance cases
status: blocked
depends_on:
  - implement-onboarding
---

# Execute rule and input acceptance cases

Room `quality` (qa-lead). Blocked until [[implement-onboarding]] is done.

Use the regression table on the reference and revised build. Record state traces for bridge closure, illegal movement, delivery, winning, reset, and undo; do not mark manual browser checks passed without observation.

## Inputs

- `quality/acceptance.csv`: [[acceptance.csv]]
- `tests/game.test.js`: [[game.test.js]]
- `deliverables/game.js`, from [[implement-onboarding]]
- `deliverables/index.html`, from [[implement-onboarding]]
- `deliverables/engineering-checks.json`, from [[implement-onboarding]]

## Outputs

- `deliverables/regression-results.csv`

## Acceptance

- Every acceptance row has an actual result or explicit not-run status and reproduction steps.
- No wall collision consumes a beat and each board can reach its win state.
