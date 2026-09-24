---
id: review-projection
title: Verify nested privacy and redistribution rights
status: blocked
depends_on:
  - prepare-projection
---

# Verify nested privacy and redistribution rights

Room `quality` (Independent quality and verification). Blocked until [[prepare-projection]] is done.

Scan every outgoing filename and byte, decoded form, nested archive and draft PR text with bounded fail-closed tooling. Supply private denylist values only at runtime. Review all source/dependency/asset licenses and required notices.

## Inputs

- `deliverables/public-projection.json`, from [[prepare-projection]]
- `deliverables/pr-draft.md`, from [[prepare-projection]]
- `deliverables/final-candidate.json`, from [[revise-candidate]]
- `docs/promotion-checklist.md`: [[promotion-checklist]]

## Outputs

- `deliverables/privacy-report.json`
- `deliverables/license-review.json`

## Acceptance

- Zero findings cover complete contents and archive members; unreadable or unscanned inputs block.
- Reports bind exact projection and PR text without including private denylist values.
- Licenses and notices are complete with no unresolved redistribution conflict.
