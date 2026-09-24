---
id: dataset-audit
title: Audit the original synthetic dataset
status: blocked
depends_on:
  - research-assumptions
---

# Audit the original synthetic dataset

Room `replication` (Independent reproducibility). Blocked until [[research-assumptions]] is done.

Reconcile row counts, expanded item IDs, units, per-scenario totals, and capacity validity. Preserve source order because it is a deliberate baseline variable, not random observed history.

## Inputs

- `deliverables/assumption-ledger.csv`, from [[research-assumptions]]
- `docs/data-dictionary.md`: [[data-dictionary]]
- `data/items.csv`: [[items.csv]]
- `data/capacity.json`: [[capacity.json]]
- `reference/tote_pack.py`: [[tote_pack.py]]

## Outputs

- `deliverables/dataset-audit.json`

## Acceptance

- Eleven item-type rows expand to 29 instances in four scenarios.
- All expanded IDs are unique within a scenario and every item individually fits the scalar capacities.
- The order-trap, weight-trap, mixed-classroom, and bulky-gaps purposes are identified.
