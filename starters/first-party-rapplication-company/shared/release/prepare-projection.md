---
id: prepare-projection
title: Prepare a separately reviewed public distribution
status: blocked
depends_on:
  - final-review
---

# Prepare a separately reviewed public distribution

Room `release` (Internal release and public promotion). Blocked until [[final-review]] is done.

Select only the authorized public payload, matching the final subject's intended projection inventory. Prepare truthful PR copy and a reversible publication proposal, not a public write. Never use a private organization or Hive root as the input distribution.

## Inputs

- `deliverables/final-candidate.json`, from [[revise-candidate]]
- `deliverables/final-review.json`, from [[final-review]]
- `docs/promotion-checklist.md`: [[promotion-checklist]]
- `templates/promotion-request.json`: [[promotion-request.json]]

## Outputs

- `deliverables/public-projection.json`
- `deliverables/pr-draft.md`

## Acceptance

- Outgoing filenames and byte hashes match the frozen public-projection inventory.
- The proposal excludes private records, identities, native stores and conversations.
- No submission, merge or publication is claimed.
