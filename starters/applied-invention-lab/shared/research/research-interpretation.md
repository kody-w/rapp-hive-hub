---
id: research-interpretation
title: Interpret gains, regressions, and model gaps
status: blocked
depends_on:
  - variant-experiment
  - packing-prototype
---

# Interpret gains, regressions, and model gaps

Room `research` (Problem framing and interpretation). Blocked until [[variant-experiment]], [[packing-prototype]] are done.

Compare baseline, all trial results, and the operator prototype. Explain why one-dimensional intuition can fail under two constraints and distinguish computational evidence from physical or market evidence.

## Inputs

- `deliverables/variant-comparison.json`, from [[variant-experiment]]
- `deliverables/baseline-results.json`, from [[baseline-computation]]
- `deliverables/packing-instructions.html`, from [[packing-prototype]]
- `deliverables/assumption-ledger.csv`, from [[research-assumptions]]
- `docs/experiment-design.md`: [[experiment-design]]

## Outputs

- `deliverables/research-interpretation.md`

## Acceptance

- The mixed-classroom regression and the bulky-gaps lower-bound gap are discussed.
- The conclusion uses the complete trial set and does not generalize four synthetic scenarios to real libraries.
- At least two decisions remain conditional on later physical or operator observations.
