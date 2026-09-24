---
id: ordering-repair
title: Prepare the deterministic event-order patch
status: blocked
depends_on:
  - deduplication-repair
---

# Prepare the deterministic event-order patch

Room `engineering` (Reference-project engineering). Blocked until [[deduplication-repair]] is done.

Build on the deduplication patch and normalize event order by at_minute then event_id before reduction. Add a same-minute tie case and retain deterministic item ordering. Do not claim the patch was merged or released.

## Inputs

- `deliverables/deduplication.patch`, from [[deduplication-repair]]
- `deliverables/reproduced-issues.json`, from [[issue-reproduction]]
- `reference/line_ledger.py`: [[line_ledger.py]]
- `data/events-out-of-order.jsonl`: [[events-out-of-order.jsonl]]
- `data/expected-contract.json`: [[expected-contract.json]]
- `docs/contract.md`: [[contract]]

## Outputs

- `deliverables/ordering.patch`

## Acceptance

- The out-of-order fixture ends item-a closed with last_minute 20.
- Equal-minute events resolve by event_id rather than input order.
- The patch preserves original inputs and the deduplication fix.
