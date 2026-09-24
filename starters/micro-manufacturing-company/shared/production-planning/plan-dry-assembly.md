---
id: plan-dry-assembly
title: Plan fit checks and a reversible pilot sequence
status: blocked
depends_on:
  - verify-parametric-fit
---

# Plan fit checks and a reversible pilot sequence

Room `production-planning` (production-planner). Blocked until [[verify-parametric-fit]] is done.

Adapt the supplied dry-fit sequence for twenty hypothetical kits, including segregation of mismatched tray/insert pairs. Do not add toolpaths, machine settings, or hazardous machinery instructions.

## Inputs

- `ops/assembly.md`: [[assembly]]
- `case/brief.json`: [[brief.json]]
- `deliverables/desk-use-requirements.md`, from [[freeze-desk-use]]
- `deliverables/nominal-interface.json`, from [[verify-parametric-fit]]

## Outputs

- `deliverables/pilot-sequence.csv`

## Acceptance

- Includes pair identification, dry insertion, removal, desk stability, and hold/review steps.
- Clearly states that fabrication, material/process selection, and physical trial execution have not occurred and require separate approval.
