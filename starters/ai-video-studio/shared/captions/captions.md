---
id: captions
title: Build the spatial captions
status: blocked
depends_on:
  - board-approval
---

# Build the spatial captions

Room `captions` (caption-editor). Blocked until [[board-approval]] is done.

Run tools/caption-phraser.mjs on the transcript with the issued kit and the board's cuts, place phrases in the caption zone, move them where the board says an overlay owns that zone, and verify the trace.

## Inputs

- `deliverables/transcript/words.json`, from [[transcript]]
- `deliverables/brand/tokens.json`, from [[brand-kit]]
- `deliverables/board/motion-board.md`, from [[motion-board]]
- `deliverables/approvals/motion-board.md`, from [[board-approval]]
- `tools/caption-phraser.mjs`: [[caption-phraser.mjs]]

## Outputs

- `deliverables/captions/captions.json`

## Acceptance

- caption-phraser.mjs --verify passes.
- No caption overlaps the face zone, the platform-safe areas or an active overlay.
