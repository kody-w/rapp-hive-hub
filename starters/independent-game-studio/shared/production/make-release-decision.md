---
id: make-release-decision
title: Record a conditional release decision
status: blocked
depends_on:
  - audit-offline-release
  - plan-observed-playtest
---

# Record a conditional release decision

Room `production` (producer). Blocked until [[audit-offline-release]], [[plan-observed-playtest]] are done.

Review the implementation, QA evidence, offline/accessibility review, and prospective test plan. Choose hold or a bounded candidate recommendation; do not publish or claim real player outcomes.

## Inputs

- `deliverables/first-shift-scope.md`, from [[lock-first-shift]]
- `deliverables/regression-results.csv`, from [[verify-game-regressions]]
- `deliverables/offline-accessibility-review.md`, from [[audit-offline-release]]
- `deliverables/prospective-playtest.csv`, from [[plan-observed-playtest]]
- `ops/release-checklist.md`: [[release-checklist]]

## Outputs

- `deliverables/release-decision.md`

## Acceptance

- Lists unresolved risks and every failed or unrun case.
- Any publication recommendation remains conditional on explicit owner approval and does not mislabel the seed as a shipped commercial game.
