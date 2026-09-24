---
id: contributor-quickstart
title: Write a reproducible contributor quickstart
status: blocked
depends_on:
  - issue-reproduction
---

# Write a reproducible contributor quickstart

Room `docs` (Contributor and operator documentation). Blocked until [[issue-reproduction]] is done.

Use observed reproduction evidence to explain the project, safe fixture commands, two failure modes, and the difference between characterization and strict acceptance. Keep the documentation useful before fixes exist.

## Inputs

- `deliverables/reproduced-issues.json`, from [[issue-reproduction]]
- `docs/contribution-guide.md`: [[contribution-guide]]
- `docs/contract.md`: [[contract]]
- `README.md`: [[README]]

## Outputs

- `deliverables/contributor-quickstart.md`

## Acceptance

- A contributor can reproduce both defects without installing packages or starting a server.
- Expected nonzero strict-check exit is explicit.
- Documentation does not describe pending repairs as completed.
