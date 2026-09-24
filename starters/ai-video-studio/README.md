# The AI Video Studio: starter

Talking-head shorts and claim-checked explainers, planned on a motion board and built as code.

Run a nine-team video studio behind one AI front door. Every edit follows the same loop: a
word-timed transcript, a timestamped motion board approved before anything is built, HyperFrames
compositions for motion graphics and captions, hard quality gates, and a release package with
provenance. Technical statements come from a pinned source and a claim ledger, and a derived cut
never asserts more than its source. Publication stays with the owner.

This folder is a Hive template for the Hive folder convention (`hive-md`, experimental). It is a
starter, not an activated organization, a Hive or a running service, and nothing in it runs. All
names, estimates and observations are synthetic. This README describes the starter; it is never
brought into a Hive.

## Where it fits

Read the RAPP/1 organism bottom to top:

0. **RAPP/1** (in force): bytes and identity beneath estates, organizations and Private Hives. A
   folder Hive signs with SSH keys instead, and its members are names bound to keys, not RAPPIDs
   (G8). This folder holds no key, id or signature.
1. **Estate** (in force): not touched. No registry entry, owner key or signature is included.
2. **Organization** (specified): the org card `ai-video-studio` plans one accountable owner, one
   world (planned id `ai-video-studio`), one policy, one release scope and exactly one Hive. No
   estate has activated canonical `rapp-work/1` yet (G16), and it cannot bind a folder Hive yet
   (G10).
3. **Hive**: this template becomes a `hive-md` Hive (experimental). Today the one Hive an
   organization can hold is a `rapp-hive/1` Private Hive (in force), which this starter does not
   declare.
4. **Your device**: your copy of the new Hive, with one key per device, and this folder as a
   read-only reference.
5. **Brainstem** (in force): its Hive agent (experimental) creates the Hive and brings the rooms in.
6. **You**: you confirm every proposal in a later turn.

Across the stack, the hub is part of the Hive Mind (candidate): it lists and verifies cards and
decides nothing. Transport carries; signatures decide.

## Pull it down

Read-only, in any of three ways:

- as a reference: pin this starter's `shared/` folder with your Hive agent's `reference`;
- with `npx degit kody-w/rapp-hive-hub/starters/ai-video-studio#experimental/organism-fit ai-video-studio`;
- or as a ZIP of the repository.

## Create the Hive

1. Ask your Brainstem to create a Hive with its Hive agent: `create` with the title "The AI Video
   Studio", `approvals` 2 and the `fields` hint from `HIVE.md`. The Hive agent writes a fresh
   `hive:` id and signs your key file into `members/`.
2. Pin this starter's `shared/` folder as a reference, then `bring` each room, with path `<room>`
   and to `shared/<room>`. Pin `shared/`, not this folder: the Hive agent will not bring from a
   folder whose `HIVE.md` names a Hive, and this template's `HIVE.md` holds a placeholder id. Every
   file arrives in one signed commit, stamped with `brought_from` and `brought_sha256`.
3. Invite people. Each person's Brainstem files one signed request, and members admit it with the
   Hive's approvals.

Nothing applies until you confirm the exact proposal in a later turn.

## Rooms

- `shared/showrunner/`: showrunner. Owns the brief, routes work across the teams, presents the
  motion board and the final cut to the owner and records the decisions, and keeps the production
  board current. The owner's own AI is the front door; this office is a stage behind it, not a
  separate bot. 3 tasks.
- `shared/brand/`: brand-custodian. Owns the reusable brand kit (type, colour, zones, caption style,
  motion language) that every production loads by name, and folds lessons from each release back
  into it. 2 tasks.
- `shared/transcription/`: transcriber. Produces the word-timed transcript for every take
  (ElevenLabs Scribe or local Whisper), fixes names and terms, reconciles against the script, and
  publishes words.json as the timing truth. 1 task.
- `shared/motion-board/`: board-planner. Plans each edit in plan mode: a timestamped motion board
  with the hook, cuts, every overlay beat with zone, effect, words and claim key, and the caption
  moves. Nothing is built until it is approved. 1 task.
- `shared/motion-graphics/`: motion-designer. Builds the approved board as seek-safe HyperFrames
  compositions: hook cards, animated UI panels, live-typing windows, layer scans and punch-ins, on
  brand and clear of the face. 1 task.
- `shared/captions/`: caption-editor. Turns the transcript into short unpunctuated caption phrases,
  places them in free space away from the face and the overlays, and keeps every caption word
  traceable to the transcript. 1 task.
- `shared/explainers/`: explainer-producer. Owns scripts, sources and truth: locks each script
  against a pinned corpus and claim ledger, records or synthesizes the take, and certifies that
  every cut asserts nothing new. 3 tasks.
- `shared/quality/`: reviewer. Gates every cut: lint and check clean, caption trace and style,
  face-safe placement, hook timing, duration and loudness, claim carryover, and a contact-sheet
  review against the approved board. 1 task.
- `shared/release/`: release-manager. Renders the approved cut and packages the vertical MP4,
  caption file, cover frame, post copy and provenance. Prepares publication; never performs it. 1
  task.
- `shared/casework/`: the charter (`ai-video-studio.md`), the first case
  (`pilot-websocket-short.md`: Pilot: the WebSocket handshake in 40 seconds) and 23 starter files in
  `artifacts/`.

## What maps cleanly, and what does not

- 14 of 23 starter files are not markdown, so they sit in `shared/casework/artifacts/` as fenced
  notes named `<file>.md`, and each note's `file` and `sha256` name the file and its exact bytes
  once copied out. In a Hive they are data: to run a reference tool, copy its fenced text into a
  workspace file of that name, check the SHA-256, and review it first.
- Task outputs are logical `deliverables/` paths. A folder Hive holds only markdown, so a team adds
  each finished output as a note; the template creates none.
- The organization's planned world id (`ai-video-studio`) has no folder-Hive counterpart: a folder
  Hive has its own `hive:` id and no world. No task has an `owner` until a member claims it.
- The `tools/caption-phraser.mjs`, `tools/transcribe.mjs`, `tools/check-kit.mjs` notes drop the
  first line, a Node shebang, because it names an absolute path and a Hive template holds none; run
  them with `node <file>`. Each `sha256` is of the file without that line.
