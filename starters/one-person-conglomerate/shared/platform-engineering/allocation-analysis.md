---
id: allocation-analysis
title: Run and explain the bounded portfolio search
status: blocked
depends_on:
  - capacity-baseline
  - ledgerleaf-intake
  - fieldnote-intake
  - quietbench-intake
  - routepaper-intake
  - tinylesson-intake
---

# Run and explain the bounded portfolio search

Room `platform-engineering` (Shared engineering). Blocked until [[capacity-baseline]], [[ledgerleaf-intake]], [[fieldnote-intake]], [[quietbench-intake]], [[routepaper-intake]], [[tinylesson-intake]] are done.

Run the authored allocation tests and analyze the provided worksheet. Compare the reference selection with the computed recommendation and explain deterministic tie-breaking and the one-experiment-per-unit constraint.

## Inputs

- `deliverables/capacity-baseline.json`, from [[capacity-baseline]]
- `deliverables/ledgerleaf-probe.md`, from [[ledgerleaf-intake]]
- `deliverables/fieldnote-probe.md`, from [[fieldnote-intake]]
- `deliverables/quietbench-probe.md`, from [[quietbench-intake]]
- `deliverables/routepaper-probe.md`, from [[routepaper-intake]]
- `deliverables/tinylesson-probe.md`, from [[tinylesson-intake]]
- `data/allocation-worksheet.csv`: [[allocation-worksheet.csv]]
- `data/capacity.json`: [[capacity.json]]
- `reference/allocation.py`: [[allocation.py]]
- `reference/test_allocation.py`: [[test_allocation.py]]

## Outputs

- `deliverables/allocation-analysis.json`

## Acceptance

- A successful test summary and exact input paths are recorded.
- The recommendation respects all three capacity limits.
- The analysis reports unspent cash and unused hours rather than treating utilization as the objective.
