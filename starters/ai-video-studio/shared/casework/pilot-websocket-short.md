---
id: pilot-websocket-short
title: "Pilot: the WebSocket handshake in 40 seconds"
---

# Pilot: the WebSocket handshake in 40 seconds

Produce the studio's first vertical short (1080x1920, 30 to 45 seconds) from the provided two-voice script about how a WebSocket connection starts. Record it as a talking head or synthesize it for a faceless layout. Open on the question hook, show the HTTP Upgrade request as a live-typing window and the 101 answer as an animated UI panel, caption every spoken word in short unpunctuated phrases, keep every on-screen technical statement traceable to RFC 6455 through the claim ledger, and hand over a release-ready package. Nothing is uploaded or published.

## Inputs

- `case/pilot.json`: [[pilot.json]]
- `source/script.md`: [[script]]
- `source/claims.json`: [[claims.json]]
- `source/corpus.json`: [[corpus.json]]
- `source/reference-words.json`: [[reference-words.json]]
- `brand/house-kit.md`: [[house-kit]]
- `brand/tokens.json`: [[tokens.json]]
- `board/motion-board-template.md`: [[motion-board-template]]
- `refs/handshake-panel.svg`: [[handshake-panel.svg]]
- `refs/chat-window.svg`: [[chat-window.svg]]

## Success criteria

- A 1080x1920 H.264 MP4 of 30 to 45 seconds renders from a clean checkout with a pinned HyperFrames CLI, and lint and check report zero errors.
- The hook is on screen by 0.5 seconds, holds at least 2.5 seconds, and matches the approved motion board.
- Every caption word traces to the take's words.json in order; phrases have one to four words and no punctuation, and none enters the face zone or the platform-safe areas.
- Every on-screen technical statement maps to a verified claim whose anchor matches the pinned RFC 6455 bytes; nothing new is asserted.
- The motion board was approved before the build started, and PROVENANCE.json records the script, claim ledger, corpus, board and approval hashes, the project commit and the CLI version.
- No upload, publication or other external effect occurs.

## Tasks

- [[brief]] Write the production brief (`showrunner`, ready)
- [[board-approval]] Present the motion board and record the decision (`showrunner`, blocked)
- [[final-approval]] Present the final cut and record the decision (`showrunner`, blocked)
- [[brand-kit]] Issue the house kit (`brand`, blocked)
- [[kit-retro]] Fold the lessons back into the kit (`brand`, blocked)
- [[transcript]] Publish the word-timed transcript (`transcription`, blocked)
- [[motion-board]] Plan the motion board (`motion-board`, blocked)
- [[motion-graphics]] Build the overlays and assemble the cut (`motion-graphics`, blocked)
- [[captions]] Build the spatial captions (`captions`, blocked)
- [[script-lock]] Lock the script against the claim ledger (`explainers`, ready)
- [[source-take]] Record or synthesize the take (`explainers`, blocked)
- [[claims-carryover]] Certify claim carryover (`explainers`, blocked)
- [[qc]] Run the quality gates (`quality`, blocked)
- [[release-package]] Render and package the deliverables (`release`, blocked)

No reference artifact counts as completed work without review.
