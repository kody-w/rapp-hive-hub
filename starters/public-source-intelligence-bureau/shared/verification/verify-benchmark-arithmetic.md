---
id: verify-benchmark-arithmetic
title: Audit acknowledgments, restart conditions, and recovered IDs
status: blocked
depends_on:
  - build-provenance-index
---

# Audit acknowledgments, restart conditions, and recovered IDs

Room `verification` (evidence-verifier). Blocked until [[build-provenance-index]] is done.

Recompute each run from the included rows and reconcile the lab-style statements. Keep different durations and restart conditions separate; blank recovery measurements mean unknown, not zero.

## Inputs

- `sources/benchmark-runs.csv`: [[benchmark-runs.csv]]
- `sources/lab-notes.csv`: [[lab-notes.csv]]
- `sources/support-notices.csv`: [[support-notices.csv]]
- `tools/evidence.py`: [[evidence.py]]
- `deliverables/evidence-index.json`, from [[build-provenance-index]]

## Outputs

- `deliverables/benchmark-audit.json`

## Acceptance

- Reports 987/1000 for the no-restart run; 0/400 for each 36-hour blocked restart; 398/400 acknowledgments and 390 recovered IDs for the six-hour run.
- Identifies eight acknowledged-but-unreconciled IDs in the six-hour run and no measured 72-hour pass.
- Does not pool unlike scenarios into a reliability estimate.
