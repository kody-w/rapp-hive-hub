---
id: rehearse-content-acceptance
title: Rerun content acceptance after rework
status: blocked
depends_on:
  - assemble-reference-rework
---

# Rerun content acceptance after rework

Room `acceptance-quality` (acceptance-reviewer). Blocked until [[assemble-reference-rework]] is done.

Apply the same eighteen criteria to the proposed reference set and record derived dependency acceptance. Keep content validity separate from actual delivery, performance testing, and owner approval.

## Inputs

- `data/acceptance-matrix.csv`: [[acceptance-matrix.csv]]
- `tools/acceptance.py`: [[acceptance.py]]
- `tests/test_acceptance.py`: [[test_acceptance.py]]
- `deliverables/proposed-reference-submissions.json`, from [[assemble-reference-rework]]
- `deliverables/rejection-rehearsal.json`, from [[rehearse-explicit-rejection]]

## Outputs

- `deliverables/content-acceptance-rehearsal.json`

## Acceptance

- All three corrected local fixtures and derived integration report satisfy content checks without changing the matrix.
- The report still says delivery_authorized false, real_partner_submissions false, and no external effects.
- Lists live usability, independent application verification, owner exchange approval, and commercial acceptance as unperformed.
