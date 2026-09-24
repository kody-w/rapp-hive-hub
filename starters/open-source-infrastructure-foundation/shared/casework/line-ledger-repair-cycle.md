---
id: line-ledger-repair-cycle
title: "Line Ledger: repair duplicate counting and out-of-order state reduction"
---

# Line Ledger: repair duplicate counting and out-of-order state reduction

Line Ledger is an original Python standard-library reference, not copied infrastructure or a real private project. Its SYNTHETIC JSONL fixtures model harmless open/close events for fictional work items. The implementation deliberately counts repeated identical event IDs twice and follows arrival order instead of event time. One clean contract case passes; two defect cases fail. The organization must reproduce, repair, review, and only then consider release.

## Inputs

- `docs/charter.md`: [[charter]]
- `docs/contract.md`: [[contract]]
- `docs/issue-register.csv`: [[issue-register.csv]]
- `data/events-clean.jsonl`: [[events-clean.jsonl]]
- `data/events-duplicate.jsonl`: [[events-duplicate.jsonl]]
- `data/events-out-of-order.jsonl`: [[events-out-of-order.jsonl]]
- `data/expected-contract.json`: [[expected-contract.json]]
- `reference/line_ledger.py`: [[line_ledger.py]]

## Success criteria

- The untouched reference characterizes one passing and two failing strict contract cases; failures are not hidden as completed fixes.
- Repair proposals address identical-ID deduplication and deterministic ordering by at_minute then event_id.
- Bounded input validation, conflict rejection, no-mutation behavior, and offline operation are preserved.
- A release candidate requires the strict contract checker to pass every case plus reviewed regression tests.
- Source ownership, remaining limitations, and external publication approvals are explicit.

## Tasks

- [[maintainer-scope]] Open the two-defect repair cycle (`maintainers`, ready)
- [[maintainer-review]] Review candidate scope and evidence (`maintainers`, blocked)
- [[issue-reproduction]] Reproduce the deliberate contract failures (`triage`, blocked)
- [[deduplication-repair]] Prepare the identical-event deduplication patch (`engineering`, blocked)
- [[ordering-repair]] Prepare the deterministic event-order patch (`engineering`, blocked)
- [[input-boundary-review]] Review the inert data boundary (`security`, blocked)
- [[contributor-quickstart]] Write a reproducible contributor quickstart (`docs`, blocked)
- [[release-notes-draft]] Draft evidence-linked release notes (`docs`, blocked)
- [[candidate-acceptance]] Evaluate a candidate against the strict contract (`release`, blocked)
- [[release-plan]] Prepare a separately approved publication plan (`release`, blocked)
- [[community-intake]] Prepare a contributor issue form (`community`, blocked)
- [[community-announcement]] Draft an honest contributor announcement (`community`, blocked)

No reference artifact counts as completed work without review.
