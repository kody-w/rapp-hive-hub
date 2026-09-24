---
id: issue-reproduction
title: Reproduce the deliberate contract failures
status: blocked
depends_on:
  - maintainer-scope
---

# Reproduce the deliberate contract failures

Room `triage` (Reproduction and issue triage). Blocked until [[maintainer-scope]] is done.

Run the authored baseline tests, the characterization mode, and the strict checker on the supplied inert fixtures. Record expected and actual counts and item states. A zero characterization exit is not a release pass.

## Inputs

- `deliverables/repair-scope.md`, from [[maintainer-scope]]
- `reference/line_ledger.py`: [[line_ledger.py]]
- `reference/test_baseline.py`: [[test_baseline.py]]
- `reference/check_acceptance.py`: [[check_acceptance.py]]
- `data/events-clean.jsonl`: [[events-clean.jsonl]]
- `data/events-duplicate.jsonl`: [[events-duplicate.jsonl]]
- `data/events-out-of-order.jsonl`: [[events-out-of-order.jsonl]]
- `data/expected-contract.json`: [[expected-contract.json]]
- `docs/issue-register.csv`: [[issue-register.csv]]

## Outputs

- `deliverables/reproduced-issues.json`

## Acceptance

- Strict checking passes the clean case and fails exactly the duplicate and out-of-order cases.
- Characterization mode is labeled known-failure reproduction, not success of the desired behavior.
- The report includes exact commands and no host-affecting fixture execution.
