---
id: transcript
title: Publish the word-timed transcript
status: blocked
depends_on:
  - source-take
---

# Publish the word-timed transcript

Room `transcription` (transcriber). Blocked until [[source-take]] is done.

Transcribe the take with tools/transcribe.mjs, fix terms, reconcile against the script with --known, and publish words.json and transcript.txt on the source timeline.

## Inputs

- `deliverables/source/take.json`, from [[source-take]]
- `source/script.md`: [[script]]
- `source/reference-words.json`: [[reference-words.json]]
- `tools/transcribe.mjs`: [[transcribe.mjs]]

## Outputs

- `deliverables/transcript/words.json`
- `deliverables/transcript/transcript.txt`

## Acceptance

- Word times are monotonic and inside the take.
- Script agreement is reported; terms such as Sec-WebSocket-Key are spelled as in the script.
- Records the engine, model and settings.
