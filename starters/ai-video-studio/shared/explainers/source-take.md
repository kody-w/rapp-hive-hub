---
id: source-take
title: Record or synthesize the take
status: blocked
depends_on:
  - script-lock
  - brief
---

# Record or synthesize the take

Room `explainers` (explainer-producer). Blocked until [[script-lock]], [[brief]] are done.

Record the locked script to camera (vertical, 30 fps, clean close-mic audio, written consent from everyone on camera), or synthesize the two voices with a voice licensed for publication. Record media path, sha256, duration and capture notes.

## Inputs

- `deliverables/script/script-lock.json`, from [[script-lock]]
- `deliverables/brief/BRIEF.md`, from [[brief]]
- `source/script.md`: [[script]]

## Outputs

- `deliverables/source/take.json`

## Acceptance

- The take speaks the locked script; deviations are listed.
- Records sha256, duration, layout option, and consent or voice licence.
