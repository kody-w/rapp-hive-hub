---
id: motion-board
title: Plan the motion board
status: blocked
depends_on:
  - brief
  - transcript
  - brand-kit
---

# Plan the motion board

Room `motion-board` (board-planner). Blocked until [[brief]], [[transcript]], [[brand-kit]] are done.

In plan mode, write the timestamped motion board: the hook in the first three seconds, cuts in silence, one row per overlay with zone, effect, on-screen words, claim key and reference image, and where captions move.

## Inputs

- `deliverables/brief/BRIEF.md`, from [[brief]]
- `deliverables/transcript/words.json`, from [[transcript]]
- `deliverables/brand/design.md`, from [[brand-kit]]
- `board/motion-board-template.md`: [[motion-board-template]]
- `source/claims.json`: [[claims.json]]
- `guides/effects.md`: [[effects]]
- `refs/handshake-panel.svg`: [[handshake-panel.svg]]
- `refs/chat-window.svg`: [[chat-window.svg]]

## Outputs

- `deliverables/board/motion-board.md`

## Acceptance

- Beats cover the whole cut without two overlays in one zone at once.
- Every technical overlay cites a claim key.
- No beat is placed in the face zone or the platform-safe areas.
