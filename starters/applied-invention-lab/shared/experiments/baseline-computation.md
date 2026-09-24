---
id: baseline-computation
title: Run the packing baseline and invariant checks
status: blocked
depends_on:
  - dataset-audit
---

# Run the packing baseline and invariant checks

Room `experiments` (Computational experiments). Blocked until [[dataset-audit]] is done.

Run the authored tests and baseline CLI with optional small-model proof enabled. Record assignments, counts, lower bounds, and proof method for every scenario; do not omit unfavorable cases.

## Inputs

- `deliverables/dataset-audit.json`, from [[dataset-audit]]
- `reference/tote_pack.py`: [[tote_pack.py]]
- `reference/test_tote_pack.py`: [[test_tote_pack.py]]
- `reference/expected-baseline.json`: [[expected-baseline.json]]
- `data/items.csv`: [[items.csv]]
- `data/capacity.json`: [[capacity.json]]

## Outputs

- `deliverables/baseline-results.json`

## Acceptance

- All expected baseline counts match and all assignment invariants pass.
- mixed-classroom reports dominant 7 versus input-order 6 and volume-first 8 bins.
- Proof labels apply only to the abstract model and no physical experiment is claimed.
