---
id: ledgerleaf-intake
title: Scope the CSV preflight business-unit probe
status: blocked
depends_on:
  - uncertainty-audit
---

# Scope the CSV preflight business-unit probe

Room `ledgerleaf-tools` (Business unit: file utilities). Blocked until [[uncertainty-audit]] is done.

Inspect the original csv_guard reference and fixture. Propose a narrow local-import quality use case, an explainable finding format, and exclusions. Run only the authored offline checks; treat them as tool evidence, not market evidence.

## Inputs

- `deliverables/uncertainty-register.csv`, from [[uncertainty-audit]]
- `docs/business-briefs.md`: [[business-briefs]]
- `reference/csv_guard.py`: [[csv_guard.py]]
- `reference/test_csv_guard.py`: [[test_csv_guard.py]]
- `data/csv-intake.csv`: [[csv-intake.csv]]

## Outputs

- `deliverables/ledgerleaf-probe.md`

## Acceptance

- The duplicate invoice key in the sample is identified.
- The brief states that preflight does not certify accounting, execute formulas, or send files.
- A usable tool boundary and an unvalidated offer are separately described.
