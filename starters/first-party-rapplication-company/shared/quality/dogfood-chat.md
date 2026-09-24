---
id: dogfood-chat
title: Observe real internal chat journeys
status: blocked
depends_on:
  - internal-release
---

# Observe real internal chat journeys

Room `quality` (Independent quality and verification). Blocked until [[internal-release]] is done.

Using an authorized observer distinct from builders and CEO, run the candidate through its intended chat host. Cover normal, negative, duplicate and recovery journeys. Record evidence and timings with minimal synthetic content; stop if the host or authority is absent.

## Inputs

- `deliverables/internal-release.json`, from [[internal-release]]
- `deliverables/candidate-manifest.json`, from [[build-candidate]]
- `deliverables/chat-design.md`, from [[design-chat]]
- `docs/chat-acceptance.md`: [[chat-acceptance]]
- `templates/dogfood-scorecard.json`: [[dogfood-scorecard.json]]

## Outputs

- `deliverables/dogfood-scorecard.json`

## Acceptance

- Every observation binds candidate, internal artifact, runtime and qualification suite.
- Not-observed and failed journeys are not converted into passes.
- A unit run or mocked chat cannot satisfy the actual chat-use gate.
