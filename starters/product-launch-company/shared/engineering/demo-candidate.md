---
id: demo-candidate
title: Prepare an evidence-linked demo candidate
status: blocked
depends_on:
  - accessibility-walkthrough
  - support-readiness
---

# Prepare an evidence-linked demo candidate

Room `engineering` (Offline product engineering). Blocked until [[accessibility-walkthrough]], [[support-readiness]] are done.

Review numerical tests, support issues, and accessibility observations. Produce a candidate manifest listing exact local source paths, content hashes, unresolved defects, and release blockers; do not hide not-observed manual gates.

## Inputs

- `deliverables/numerical-evidence.json`, from [[numerical-verification]]
- `deliverables/accessibility-observations.csv`, from [[accessibility-walkthrough]]
- `deliverables/support-kit.md`, from [[support-readiness]]
- `demo/index.html`: [[index.html]]
- `demo/styles.css`: [[styles.css]]
- `demo/core.js`: [[core.js]]
- `demo/app.js`: [[app.js]]
- `docs/launch-checklist.md`: [[launch-checklist]]

## Outputs

- `deliverables/demo-candidate.json`

## Acceptance

- All four demo files are identified with locally computed public-source hashes.
- No unresolved or unobserved gate is represented as passed.
- The candidate includes no credentials, remote dependencies, or invented signatures.
