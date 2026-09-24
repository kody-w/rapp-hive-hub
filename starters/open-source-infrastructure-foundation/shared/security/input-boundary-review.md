---
id: input-boundary-review
title: Review the inert data boundary
status: blocked
depends_on:
  - maintainer-scope
---

# Review the inert data boundary

Room `security` (Defensive input-boundary review). Blocked until [[maintainer-scope]] is done.

Review the original reducer and documented input limits. Check that fixtures are data, not commands, and that any proposed fixes preserve rejection of conflicting IDs, invalid actions, oversized input, and invalid minute values. Produce defensive findings only; no hostile host tests.

## Inputs

- `deliverables/repair-scope.md`, from [[maintainer-scope]]
- `docs/security-boundary.md`: [[security-boundary]]
- `reference/line_ledger.py`: [[line_ledger.py]]
- `reference/test_baseline.py`: [[test_baseline.py]]
- `docs/contract.md`: [[contract]]

## Outputs

- `deliverables/input-boundary-review.md`

## Acceptance

- File reads are explicitly selected and bounded; no network, execution, write, or identity capability is introduced.
- The review distinguishes logic defects from claims of an exploitable vulnerability.
- Any remaining boundary concern has a concrete proposed regression case using inert in-memory data.
