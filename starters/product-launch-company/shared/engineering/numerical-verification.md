---
id: numerical-verification
title: Reproduce the agenda acceptance cases
status: blocked
depends_on:
  - interaction-plan
---

# Reproduce the agenda acceptance cases

Room `engineering` (Offline product engineering). Blocked until [[interaction-plan]] is done.

Run the authored Node standard-library tests and JavaScript syntax checks. Compare every structured case against the core result and record commands and observed results rather than asserting a production launch.

## Inputs

- `deliverables/interaction-walkthrough.md`, from [[interaction-plan]]
- `demo/core.js`: [[core.js]]
- `demo/app.js`: [[app.js]]
- `reference/test_agenda.cjs`: [[test_agenda.cjs]]
- `data/acceptance-cases.json`: [[acceptance-cases.json]]
- `data/sample-agenda.json`: [[sample-agenda.json]]
- `docs/test-protocol.md`: [[test-protocol]]

## Outputs

- `deliverables/numerical-evidence.json`

## Acceptance

- All structured numerical cases pass, including blocked capacity and midnight bounds.
- The pure core does not mutate imported input.
- Automated results do not stand in for browser or assistive-technology observations.
