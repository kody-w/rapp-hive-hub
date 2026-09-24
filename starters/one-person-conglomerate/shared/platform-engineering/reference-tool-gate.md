---
id: reference-tool-gate
title: Prepare the CSV reference-tool handoff
status: blocked
depends_on:
  - portfolio-decision
---

# Prepare the CSV reference-tool handoff

Room `platform-engineering` (Shared engineering). Blocked until [[portfolio-decision]] is done.

Repeat the CSV checks, document the sample's expected nonzero exit, and assemble a release-readiness checklist for the one real small reference tool. Publication is a later, separately approved operation.

## Inputs

- `deliverables/portfolio-decision.json`, from [[portfolio-decision]]
- `deliverables/ledgerleaf-probe.md`, from [[ledgerleaf-intake]]
- `reference/csv_guard.py`: [[csv_guard.py]]
- `reference/test_csv_guard.py`: [[test_csv_guard.py]]
- `data/csv-intake.csv`: [[csv-intake.csv]]
- `docs/review-rubric.md`: [[review-rubric]]

## Outputs

- `deliverables/csv-tool-handoff.md`

## Acceptance

- The tool reads only the explicitly selected UTF-8 file and writes JSON to stdout.
- All authored tests pass; the intentionally duplicated sample key yields a duplicate-key finding.
- Distribution, signing, billing, and real-file ingestion are not represented as completed.
