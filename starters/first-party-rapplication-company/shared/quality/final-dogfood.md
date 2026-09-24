---
id: final-dogfood
title: Qualify the final candidate through real chat
status: blocked
depends_on:
  - final-internal-release
---

# Qualify the final candidate through real chat

Room `quality` (Independent quality and verification). Blocked until [[final-internal-release]] is done.

Repeat actual chat qualification for every changed candidate and the final suite. Compare earlier failures without erasing them. Unchanged evidence can be referenced only with exact current bindings; unobserved work stays blocked.

## Inputs

- `deliverables/final-internal-release.json`, from [[final-internal-release]]
- `deliverables/final-candidate.json`, from [[revise-candidate]]
- `deliverables/dogfood-scorecard.json`, from [[dogfood-chat]]
- `docs/chat-acceptance.md`: [[chat-acceptance]]
- `templates/dogfood-scorecard.json`: [[dogfood-scorecard.json]]

## Outputs

- `deliverables/final-dogfood.json`

## Acceptance

- All mandatory final journeys have actual pass evidence or shipment remains blocked.
- Identity separation from builders and CEO is validated by the trusted host.
- Reference fixtures are never represented as live qualification.
