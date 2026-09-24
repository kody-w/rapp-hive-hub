---
id: claims-carryover
title: Certify claim carryover
status: blocked
depends_on:
  - motion-graphics
---

# Certify claim carryover

Room `explainers` (explainer-producer). Blocked until [[motion-graphics]] is done.

Map every on-screen technical statement in the cut to a verified claim key and anchor. Anything unmapped is a new claim: return it instead of certifying.

## Inputs

- `source/claims.json`: [[claims.json]]
- `deliverables/board/motion-board.md`, from [[motion-board]]
- `deliverables/cut/short.json`, from [[motion-graphics]]

## Outputs

- `deliverables/claims/carryover.json`

## Acceptance

- Zero unmapped on-screen statements.
