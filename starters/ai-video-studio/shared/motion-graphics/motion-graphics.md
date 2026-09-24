---
id: motion-graphics
title: Build the overlays and assemble the cut
status: blocked
depends_on:
  - captions
---

# Build the overlays and assemble the cut

Room `motion-graphics` (motion-designer). Blocked until [[captions]] is done.

Create the HyperFrames project, cut the take, build each board beat from the starter overlays and the effect catalogue, wire the captions, and keep lint and check clean.

## Inputs

- `deliverables/board/motion-board.md`, from [[motion-board]]
- `deliverables/approvals/motion-board.md`, from [[board-approval]]
- `deliverables/brand/tokens.json`, from [[brand-kit]]
- `deliverables/captions/captions.json`, from [[captions]]
- `deliverables/source/take.json`, from [[source-take]]
- `project/hook-card.html`: [[hook-card.html]]
- `project/typing-window.html`: [[typing-window.html]]
- `project/ui-panel.html`: [[ui-panel.html]]

## Outputs

- `deliverables/cut/short.json`

## Acceptance

- short.json lists every overlay with its board beat and zone.
- lint and check report zero errors.
- The hook overlay is on screen by 0.5 seconds.
