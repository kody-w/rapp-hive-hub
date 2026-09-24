---
id: board-approval
title: Present the motion board and record the decision
status: blocked
depends_on:
  - motion-board
---

# Present the motion board and record the decision

Room `showrunner` (showrunner). Blocked until [[motion-board]] is done.

Check the board against the brief, present it to the owner, and record the owner's decision with the board sha256, or return it with specific, testable changes. Building starts only after an approval record exists.

## Inputs

- `deliverables/board/motion-board.md`, from [[motion-board]]
- `deliverables/brief/BRIEF.md`, from [[brief]]

## Outputs

- `deliverables/approvals/motion-board.md`

## Acceptance

- Records the decision, the reviewer and the board sha256.
