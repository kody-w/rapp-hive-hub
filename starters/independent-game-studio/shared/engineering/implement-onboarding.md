---
id: implement-onboarding
title: Build the bounded onboarding revision
status: blocked
depends_on:
  - prepare-readable-art
  - specify-local-cues
---

# Build the bounded onboarding revision

Room `engineering` (game-engineer). Blocked until [[prepare-readable-art]], [[specify-local-cues]] are done.

Produce a revised engine/UI source pair from the working reference, incorporating the reviewed specification, symbol work, and optional cues. Preserve offline file opening and deterministic rules.

## Inputs

- `game/index.html`: [[index.html]]
- `game/game.js`: [[game.js]]
- `tests/game.test.js`: [[game.test.js]]
- `deliverables/onboarding-spec.md`, from [[revise-bridge-onboarding]]
- `deliverables/courier-atlas.svg`, from [[prepare-readable-art]]
- `deliverables/readability-notes.md`, from [[prepare-readable-art]]
- `deliverables/audio-map.json`, from [[specify-local-cues]]

## Outputs

- `deliverables/game.js`
- `deliverables/index.html`
- `deliverables/engineering-checks.json`

## Acceptance

- The supplied engine tests still pass, including solver coverage for all three boards.
- The revised HTML references only local files and supports keyboard restart, undo, wait, and level selection.
- Records tests actually run separately from any unrun browser/device checks.
