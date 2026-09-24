---
id: replication-run
title: Replicate the computation independently
status: blocked
depends_on:
  - variant-experiment
---

# Replicate the computation independently

Room `replication` (Independent reproducibility). Blocked until [[variant-experiment]] is done.

Follow the replication protocol in a fresh interpreter using the same explicit source files. Recompute hashes, baseline assignments, and seeded trials; report exact agreement or discrepancies, including runtime details.

## Inputs

- `deliverables/variant-comparison.json`, from [[variant-experiment]]
- `deliverables/baseline-results.json`, from [[baseline-computation]]
- `docs/replication-protocol.md`: [[replication-protocol]]
- `reference/tote_pack.py`: [[tote_pack.py]]
- `reference/run_experiment.py`: [[run_experiment.py]]
- `reference/test_tote_pack.py`: [[test_tote_pack.py]]
- `reference/expected-baseline.json`: [[expected-baseline.json]]
- `data/items.csv`: [[items.csv]]
- `data/capacity.json`: [[capacity.json]]
- `data/experiment-plan.json`: [[experiment-plan.json]]

## Outputs

- `deliverables/replication-report.json`

## Acceptance

- Input hashes and every per-trial count agree or a discrepancy is explicitly reported.
- All assignment constraints are checked again rather than trusting the first report.
- Not-observed physical outcomes remain outside the replication claim.
