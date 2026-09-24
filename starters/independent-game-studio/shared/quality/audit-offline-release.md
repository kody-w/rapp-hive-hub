---
id: audit-offline-release
title: Audit file-only release and accessibility
status: blocked
depends_on:
  - verify-game-regressions
---

# Audit file-only release and accessibility

Room `quality` (qa-lead). Blocked until [[verify-game-regressions]] is done.

Inspect the candidate for network references, storage, external assets, focus behavior, optional sound, and non-color state cues. Use the checklist to separate automated evidence from browser and assistive-technology limits.

## Inputs

- `ops/release-checklist.md`: [[release-checklist]]
- `deliverables/index.html`, from [[implement-onboarding]]
- `deliverables/game.js`, from [[implement-onboarding]]
- `deliverables/courier-atlas.svg`, from [[prepare-readable-art]]
- `deliverables/regression-results.csv`, from [[verify-game-regressions]]

## Outputs

- `deliverables/offline-accessibility-review.md`

## Acceptance

- Reports no network-capable gameplay code or remote assets.
- Explicitly records whether keyboard-only, sound-disabled, narrow-screen, and screen-reader checks were performed.
