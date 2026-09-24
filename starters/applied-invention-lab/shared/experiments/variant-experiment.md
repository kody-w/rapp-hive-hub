---
id: variant-experiment
title: Run the predeclared seeded comparison
status: blocked
depends_on:
  - baseline-computation
---

# Run the predeclared seeded comparison

Room `experiments` (Computational experiments). Blocked until [[baseline-computation]] is done.

Execute the original experiment runner using the supplied seed, 20 permutations per scenario, and all three declared algorithms. Retain every trial and the dataset/configuration/plan hashes.

## Inputs

- `deliverables/baseline-results.json`, from [[baseline-computation]]
- `docs/experiment-design.md`: [[experiment-design]]
- `data/experiment-plan.json`: [[experiment-plan.json]]
- `data/items.csv`: [[items.csv]]
- `data/capacity.json`: [[capacity.json]]
- `reference/run_experiment.py`: [[run_experiment.py]]
- `reference/tote_pack.py`: [[tote_pack.py]]

## Outputs

- `deliverables/variant-comparison.json`

## Acceptance

- The result contains 4 scenarios × 3 algorithms × 20 trial counts.
- The same permutation is used for each algorithm within a trial.
- No measured sample is discarded to claim a universally superior heuristic.
