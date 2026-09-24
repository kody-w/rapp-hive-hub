---
id: release-plan
title: Prepare a separately approved publication plan
status: blocked
depends_on:
  - release-notes-draft
---

# Prepare a separately approved publication plan

Room `release` (Acceptance and release operations). Blocked until [[release-notes-draft]] is done.

Prepare an inert release plan with candidate hashes, proposed version, exact artifacts, checks, publication destination to be selected by an owner, and withdrawal steps. Do not publish, tag, sign, or mint identities.

## Inputs

- `deliverables/release-notes-draft.md`, from [[release-notes-draft]]
- `deliverables/maintainer-review.md`, from [[maintainer-review]]
- `deliverables/candidate-acceptance.json`, from [[candidate-acceptance]]
- `docs/release-checklist.md`: [[release-checklist]]
- `LICENSE.txt`: [[LICENSE.txt]]

## Outputs

- `deliverables/publication-plan.json`

## Acceptance

- A failing or unreviewed candidate blocks publication.
- Every external operation remains a separate explicit approval boundary.
- Hashes identify public candidate files only and are not represented as signatures.
