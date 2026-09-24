---
id: release-notes-draft
title: Draft evidence-linked release notes
status: blocked
depends_on:
  - maintainer-review
---

# Draft evidence-linked release notes

Room `docs` (Contributor and operator documentation). Blocked until [[maintainer-review]] is done.

Draft notes that explain desired fixed behavior, compatibility, remaining limits, and actual candidate evidence. If the maintainer recommendation is blocked, say so and retain draft status.

## Inputs

- `deliverables/maintainer-review.md`, from [[maintainer-review]]
- `deliverables/candidate-acceptance.json`, from [[candidate-acceptance]]
- `deliverables/contributor-quickstart.md`, from [[contributor-quickstart]]
- `docs/release-checklist.md`: [[release-checklist]]

## Outputs

- `deliverables/release-notes-draft.md`

## Acceptance

- Notes distinguish the failing source baseline from any tested candidate.
- No tag, package upload, signature, download count, or released version is invented.
- Event ordering, duplicate semantics, and remaining limitations are described accurately.
