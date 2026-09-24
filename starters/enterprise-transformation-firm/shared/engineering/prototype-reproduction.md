---
id: prototype-reproduction
title: Reproduce the offline quote batch
status: blocked
depends_on:
  - calculation-boundary
---

# Reproduce the offline quote batch

Room `engineering` (Prototype engineering). Blocked until [[calculation-boundary]] is done.

Run only the authored utility and tests on the supplied data. Capture the full result and command metadata as a proposed engineering handoff, without altering source fixtures.

## Inputs

- `deliverables/calculation-contract.md`, from [[calculation-boundary]]
- `reference/quote_flow.py`: [[quote_flow.py]]
- `reference/test_quote_flow.py`: [[test_quote_flow.py]]
- `data/accounts.csv`: [[accounts.csv]]
- `data/quotes.csv`: [[quotes.csv]]
- `data/quote-lines.csv`: [[quote-lines.csv]]
- `data/policy.json`: [[policy.json]]
- `reference/expected-results.json`: [[expected-results.json]]

## Outputs

- `deliverables/prototype-run.json`

## Acceptance

- Exactly eight results are captured in quote-ID order.
- The authored tests pass and source inputs remain unchanged.
- The run records three readiness categories and never claims a real invoice.
