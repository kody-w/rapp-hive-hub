---
id: rehearse-explicit-rejection
title: Rehearse incompatible-deliverable rejection
status: blocked
depends_on:
  - verify-local-interface
---

# Rehearse incompatible-deliverable rejection

Room `acceptance-quality` (acceptance-reviewer). Blocked until [[verify-local-interface]] is done.

Run the baseline fixture through the content matrix. Record exact failed criteria, source locations, downstream blockage, and the fact that these are authored examples rather than real submissions.

## Inputs

- `fixtures/submissions.json`: [[submissions.json]]
- `data/acceptance-matrix.csv`: [[acceptance-matrix.csv]]
- `data/dependencies.csv`: [[dependencies.csv]]
- `tools/acceptance.py`: [[acceptance.py]]
- `deliverables/interface-validation.json`, from [[verify-local-interface]]

## Outputs

- `deliverables/rejection-rehearsal.json`

## Acceptance

- Prototype content passes, operating-model retention 1440 fails the 1–120 bound, pilot-kit interface version 0 fails version 1, and integration-report is blocked.
- Captures the expected nonzero baseline CLI exit code and does not call a failed baseline a tool malfunction.
- Reports delivery_authorized false and no cross-world effects.
