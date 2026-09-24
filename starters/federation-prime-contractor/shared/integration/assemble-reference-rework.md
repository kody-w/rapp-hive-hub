---
id: assemble-reference-rework
title: Assemble the corrected local reference set
status: blocked
depends_on:
  - bound-reference-rework
---

# Assemble the corrected local reference set

Room `integration` (integration-lead). Blocked until [[bound-reference-rework]] is done.

Use the included corrected fixture as a worked example, verify it against the bounded rework plan, and produce a proposed inert submission set. No actual partner artifact is fetched or exchanged.

## Inputs

- `fixtures/rework-submissions.json`: [[rework-submissions.json]]
- `interfaces/pilot.json`: [[pilot.json]]
- `data/deliverables.csv`: [[deliverables.csv]]
- `data/dependencies.csv`: [[dependencies.csv]]
- `deliverables/reference-rework-plan.json`, from [[bound-reference-rework]]

## Outputs

- `deliverables/proposed-reference-submissions.json`

## Acceptance

- Contains exactly the three declared reference artifacts with SYNTHETIC classification, candidate slugs, public-reference-fixture visibility, and no exchange approval.
- Carries no unknown payload fields, private content, executable partner code, remote locator, or workspace registration.
