---
id: deduplication-repair
title: Prepare the identical-event deduplication patch
status: blocked
depends_on:
  - issue-reproduction
  - input-boundary-review
---

# Prepare the identical-event deduplication patch

Room `engineering` (Reference-project engineering). Blocked until [[issue-reproduction]], [[input-boundary-review]] are done.

Create a reviewable patch that counts each identical event ID once while retaining rejection of conflicting payloads. Add or update regression tests; do not weaken expected-contract.json to make the defect disappear.

## Inputs

- `deliverables/reproduced-issues.json`, from [[issue-reproduction]]
- `deliverables/input-boundary-review.md`, from [[input-boundary-review]]
- `reference/line_ledger.py`: [[line_ledger.py]]
- `reference/test_baseline.py`: [[test_baseline.py]]
- `data/events-duplicate.jsonl`: [[events-duplicate.jsonl]]
- `data/expected-contract.json`: [[expected-contract.json]]
- `docs/contribution-guide.md`: [[contribution-guide]]

## Outputs

- `deliverables/deduplication.patch`

## Acceptance

- The duplicate fixture's event_count becomes 3 and item-a event_count becomes 2.
- Conflicting duplicate payloads remain rejected.
- Expected desired results are unchanged and the second defect remains visible until separately repaired.
