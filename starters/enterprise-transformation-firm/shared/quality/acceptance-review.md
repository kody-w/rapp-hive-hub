---
id: acceptance-review
title: Check arithmetic and exception acceptance
status: blocked
depends_on:
  - prototype-reproduction
---

# Check arithmetic and exception acceptance

Room `quality` (Acceptance and quality). Blocked until [[prototype-reproduction]] is done.

Compare the reproduced batch to the expected-results reference and requirements trace. Record each case's expected amount, actual amount, state, and review or data reason.

## Inputs

- `deliverables/prototype-run.json`, from [[prototype-reproduction]]
- `deliverables/requirements-trace.csv`, from [[requirements-trace]]
- `reference/expected-results.json`: [[expected-results.json]]
- `docs/acceptance-cases.md`: [[acceptance-cases]]
- `reference/test_quote_flow.py`: [[test_quote_flow.py]]

## Outputs

- `deliverables/acceptance-matrix.csv`

## Acceptance

- q-101 totals USD 268.21 and q-106 totals USD 10.16.
- q-102, q-103, q-104, and q-108 remain review-gated.
- q-105 and q-107 have null totals and needs-data, not zero-dollar approval.
