---
id: release-package
title: Render and package the deliverables
status: blocked
depends_on:
  - final-approval
---

# Render and package the deliverables

Room `release` (release-manager). Blocked until [[final-approval]] is done.

Render the approved commit from a clean checkout, export the SRT and a cover frame, draft the post copy, and write PROVENANCE.json. Prepare only: do not upload or publish.

## Inputs

- `deliverables/cut/short.json`, from [[motion-graphics]]
- `deliverables/approvals/final-cut.md`, from [[final-approval]]
- `deliverables/captions/captions.json`, from [[captions]]
- `ops/release-checklist.md`: [[release-checklist]]

## Outputs

- `deliverables/release/short-1080x1920.mp4`
- `deliverables/release/captions.srt`
- `deliverables/release/cover.png`
- `deliverables/release/post.md`
- `deliverables/release/PROVENANCE.json`

## Acceptance

- The MP4 is 1080x1920 H.264 between 30 and 45 seconds.
- PROVENANCE.json records every hash the case requires.
- Nothing was uploaded or published.
