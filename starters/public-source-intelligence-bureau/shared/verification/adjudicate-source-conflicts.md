---
id: adjudicate-source-conflicts
title: Classify contradictions and metric mismatches
status: blocked
depends_on:
  - verify-benchmark-arithmetic
  - compare-launch-hypotheses
---

# Classify contradictions and metric mismatches

Room `verification` (evidence-verifier). Blocked until [[verify-benchmark-arithmetic]], [[compare-launch-hypotheses]] are done.

Review each conflict pair against the exact included rows, the hypotheses, and benchmark audit. Distinguish direct scope conflicts from schedule ambiguity and measurement mismatches.

## Inputs

- `analysis/contradictions.csv`: [[contradictions.csv]]
- `deliverables/benchmark-audit.json`, from [[verify-benchmark-arithmetic]]
- `deliverables/hypothesis-matrix.csv`, from [[compare-launch-hypotheses]]
- `deliverables/evidence-index.json`, from [[build-provenance-index]]

## Outputs

- `deliverables/conflict-ledger.csv`

## Acceptance

- Covers all three supplied conflict cases with citations, unresolved questions, and a falsifiable resolution request.
- Does not call unlike acknowledgment and durability metrics a demonstrated direct contradiction.
