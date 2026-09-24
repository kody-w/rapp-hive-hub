---
id: plan-next-collection
title: Turn uncertainty into a prospective investigation board
status: blocked
depends_on:
  - adjudicate-source-conflicts
---

# Turn uncertainty into a prospective investigation board

Room `collection` (collection-editor). Blocked until [[adjudicate-source-conflicts]] is done.

Prioritize the supplied inquiry rows using the conflict ledger. Define the next safe public artifact or synthetic test specification needed and who reviews it; no live collection occurs in this task.

## Inputs

- `ops/investigation-board.csv`: [[investigation-board.csv]]
- `case/question.json`: [[question.json]]
- `deliverables/conflict-ledger.csv`, from [[adjudicate-source-conflicts]]
- `deliverables/corpus-inventory.json`, from [[freeze-local-corpus]]

## Outputs

- `deliverables/prospective-investigation.csv`

## Acceptance

- Includes a 72-hour cold-restart test, acknowledged/recovered-ID reconciliation, exact release identification, and source-independence question.
- Every inquiry has an owner, stopping condition, and decision dependency; any actual collection or contact remains approval-gated.
