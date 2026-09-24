---
id: calculation-boundary
title: Specify the replaceable calculation contract
status: blocked
depends_on:
  - requirements-trace
---

# Specify the replaceable calculation contract

Room `architecture` (Solution architecture). Blocked until [[requirements-trace]] is done.

Describe the pure input/output contract, validation limits, rounding points, and state precedence around the authored utility. Keep enterprise adapters, identity, persistence, and approval outside the reference.

## Inputs

- `deliverables/requirements-trace.csv`, from [[requirements-trace]]
- `data/policy.json`: [[policy.json]]
- `reference/quote_flow.py`: [[quote_flow.py]]
- `docs/handoff-contracts.md`: [[handoff-contracts]]

## Outputs

- `deliverables/calculation-contract.md`

## Acceptance

- The contract specifies cent precision and ROUND_HALF_UP per line and shipping tax.
- needs-data outranks needs-review and no state means invoice-sent.
- Unknown accounts and malformed numeric values are rejected without network side effects.
