---
id: brand-kit
title: Issue the house kit
status: blocked
depends_on:
  - brief
---

# Issue the house kit

Room `brand` (brand-custodian). Blocked until [[brief]] is done.

Resolve the house kit for this production: download the OFL fonts with their licences, confirm zones for the chosen layout (talking head, or source card in place of the face zone), and issue design.md and tokens.json. Run tools/check-kit.mjs.

## Inputs

- `brand/house-kit.md`: [[house-kit]]
- `brand/tokens.json`: [[tokens.json]]
- `deliverables/brief/BRIEF.md`, from [[brief]]
- `tools/check-kit.mjs`: [[check-kit.mjs]]

## Outputs

- `deliverables/brand/design.md`
- `deliverables/brand/tokens.json`

## Acceptance

- check-kit.mjs passes on the issued kit.
- Every font is a licensed file with its licence text.
