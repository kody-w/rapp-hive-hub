---
id: triage-feedback
title: Synthesize observations without copying conversations
status: blocked
depends_on:
  - dogfood-chat
---

# Synthesize observations without copying conversations

Room `support` (Support and product learning). Blocked until [[dogfood-chat]] is done.

Turn observed dogfood issues into minimal reproducible feedback. Preserve failures, separate hypotheses from observations, and request no additional private data without need and consent.

## Inputs

- `deliverables/dogfood-scorecard.json`, from [[dogfood-chat]]
- `deliverables/support-kit.md`, from [[prepare-support]]
- `templates/feedback.json`: [[feedback.json]]
- `docs/support-playbook.md`: [[support-playbook]]

## Outputs

- `deliverables/feedback.json`

## Acceptance

- Each finding has a candidate binding, reproduction, expected/observed behavior and evidence reference.
- No feedback or customer satisfaction is fabricated.
- Raw chats, identities and private locations stay outside public artifacts.
