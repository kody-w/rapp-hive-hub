---
id: record-owner-merge
title: Observe the owner's merge and verify the publication
status: blocked
depends_on:
  - ready-public-pr
---

# Observe the owner's merge and verify the publication

Room `release` (Internal release and public promotion). Blocked until [[ready-public-pr]] is done.

Wait for the owner's separate merge decision and action; do not merge or infer consent. After an actual merge, verify the checked head and published artifact against the approved projection and record a sanitized reference plus withdrawal procedure.

## Inputs

- `deliverables/ready-pr.json`, from [[ready-public-pr]]
- `deliverables/public-projection.json`, from [[prepare-projection]]
- `templates/promotion-request.json`: [[promotion-request.json]]
- `docs/promotion-checklist.md`: [[promotion-checklist]]

## Outputs

- `deliverables/owner-merge-reference.json`

## Acceptance

- Completion requires an observed owner-merged PR and verification of the resulting artifact.
- Release does not perform automated merge or claim a still-open PR as shipped.
- Missing authority, head drift or publication mismatch is retained as a blocker.
