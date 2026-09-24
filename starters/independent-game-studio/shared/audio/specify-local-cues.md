---
id: specify-local-cues
title: Map optional synthesized cues
status: blocked
depends_on:
  - revise-bridge-onboarding
---

# Map optional synthesized cues

Room `audio` (sound-designer). Blocked until [[revise-bridge-onboarding]] is done.

Review the existing Web Audio cue sheet against the onboarding specification. Specify short tones, volume bounds, and a no-audio fallback rather than importing audio.

## Inputs

- `audio/cue-sheet.csv`: [[cue-sheet.csv]]
- `game/game.js`: [[game.js]]
- `deliverables/onboarding-spec.md`, from [[revise-bridge-onboarding]]

## Outputs

- `deliverables/audio-map.json`

## Acceptance

- Includes blocked, loaded, delivered, and won events with durations no greater than 180 ms.
- Requires a user opt-in and keeps every critical cue available in text.
