---
title: The AI Video Studio
---

# The AI Video Studio

Talking-head shorts and claim-checked explainers, planned on a motion board and built as code.

Run a nine-team video studio behind one AI front door. Every edit follows the same loop: a word-timed transcript, a timestamped motion board approved before anything is built, HyperFrames compositions for motion graphics and captions, hard quality gates, and a release package with provenance. Technical statements come from a pinned source and a claim ledger, and a derived cut never asserts more than its source. Publication stays with the owner.

## Rooms

- `shared/showrunner/`: showrunner. Owns the brief, routes work across the teams, presents the motion board and the final cut to the owner and records the decisions, and keeps the production board current. The owner's own AI is the front door; this office is a stage behind it, not a separate bot.
- `shared/brand/`: brand-custodian. Owns the reusable brand kit (type, colour, zones, caption style, motion language) that every production loads by name, and folds lessons from each release back into it.
- `shared/transcription/`: transcriber. Produces the word-timed transcript for every take (ElevenLabs Scribe or local Whisper), fixes names and terms, reconciles against the script, and publishes words.json as the timing truth.
- `shared/motion-board/`: board-planner. Plans each edit in plan mode: a timestamped motion board with the hook, cuts, every overlay beat with zone, effect, words and claim key, and the caption moves. Nothing is built until it is approved.
- `shared/motion-graphics/`: motion-designer. Builds the approved board as seek-safe HyperFrames compositions: hook cards, animated UI panels, live-typing windows, layer scans and punch-ins, on brand and clear of the face.
- `shared/captions/`: caption-editor. Turns the transcript into short unpunctuated caption phrases, places them in free space away from the face and the overlays, and keeps every caption word traceable to the transcript.
- `shared/explainers/`: explainer-producer. Owns scripts, sources and truth: locks each script against a pinned corpus and claim ledger, records or synthesizes the take, and certifies that every cut asserts nothing new.
- `shared/quality/`: reviewer. Gates every cut: lint and check clean, caption trace and style, face-safe placement, hook timing, duration and loudness, claim carryover, and a contact-sheet review against the approved board.
- `shared/release/`: release-manager. Renders the approved cut and packages the vertical MP4, caption file, cover frame, post copy and provenance. Prepares publication; never performs it.
- `shared/casework/`: the shared delivery case. Its intake is [[pilot-websocket-short]]; shared inputs sit in `artifacts/`; accepted deliverables land here too.

Related starters, for discovery only (never shared membership): `product-launch-company`.

All names, estimates and observations are synthetic public starter data.
