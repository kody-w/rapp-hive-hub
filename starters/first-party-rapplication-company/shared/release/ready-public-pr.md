---
id: ready-public-pr
title: Hand a sanitized checked PR to its owner
status: blocked
depends_on:
  - request-separate-decision
---

# Hand a sanitized checked PR to its owner

Room `release` (Internal release and public promotion). Blocked until [[request-separate-decision]] is done.

After exact publication approval, revalidate the decision, outgoing bytes, PR copy, privacy/licenses, all local suites and current required CI. Use existing authorized access to prepare a non-draft PR. If submission is unavailable or unapproved, retain only the local proposal and report the blocker.

## Inputs

- `deliverables/decision-reference.json`, from [[request-separate-decision]]
- `deliverables/public-projection.json`, from [[prepare-projection]]
- `deliverables/pr-draft.md`, from [[prepare-projection]]
- `deliverables/privacy-report.json`, from [[review-projection]]
- `deliverables/license-review.json`, from [[review-projection]]
- `templates/promotion-request.json`: [[promotion-request.json]]
- `docs/promotion-checklist.md`: [[promotion-checklist]]

## Outputs

- `deliverables/ready-pr.json`

## Acceptance

- The actual PR's exact head, diff and text match owner-reviewed artifacts and current passing required checks.
- Changed bytes or text trigger fresh affected checks; pending/missing/skipped/failed required checks block.
- The handoff says ready for owner merge, not published or shipped.
