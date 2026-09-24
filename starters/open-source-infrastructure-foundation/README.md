# The Open-Source Infrastructure Foundation: starter

A tiny original project with real, reproducible repair work.

Coordinate maintainers, triage, engineering, security, documentation, release, and community around
a deliberately imperfect offline event reducer, preserving honest failures and evidence-based
release gates.

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
2. **Organization** (specified): the org card `open-source-infrastructure-foundation` plans one
   accountable owner, one world (planned id `demo-open-source-infrastructure-foundation`), one
   policy, one release scope and exactly one Hive. No estate has activated canonical `rapp-work/1`
   yet (G16), and it cannot bind a folder Hive yet (G10).
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
- with `npx degit kody-w/rapp-hive-hub/starters/open-source-infrastructure-foundation#experimental/organism-fit open-source-infrastructure-foundation`;
- or as a ZIP of the repository.

## Create the Hive

1. Ask your Brainstem to create a Hive with its Hive agent: `create` with the title "The Open-Source
   Infrastructure Foundation", `approvals` 2 and the `fields` hint from `HIVE.md`. The Hive agent
   writes a fresh `hive:` id and signs your key file into `members/`.
2. Pin this starter's `shared/` folder as a reference, then `bring` each room, with path `<room>`
   and to `shared/<room>`. Pin `shared/`, not this folder: the Hive agent will not bring from a
   folder whose `HIVE.md` names a Hive, and this template's `HIVE.md` holds a placeholder id. Every
   file arrives in one signed commit, stamped with `brought_from` and `brought_sha256`.
3. Invite people. Each person's Brainstem files one signed request, and members admit it with the
   Hive's approvals.

Nothing applies until you confirm the exact proposal in a later turn.

## Rooms

- `shared/maintainers/`: Project stewardship. Own the reference contract, narrow scope, review
  decisions, and release authority boundaries. 2 tasks.
- `shared/triage/`: Reproduction and issue triage. Reproduce the two deliberate logic defects and
  turn each into precise repair work. 1 task.
- `shared/engineering/`: Reference-project engineering. Prepare narrowly scoped deduplication and
  deterministic ordering fixes without rewriting the project. 2 tasks.
- `shared/security/`: Defensive input-boundary review. Review bounded inert data handling and
  prevent file, network, command, or identity capabilities from being added. 1 task.
- `shared/docs/`: Contributor and operator documentation. Keep quickstart, behavior, repair
  guidance, and release notes aligned with observed code. 2 tasks.
- `shared/release/`: Acceptance and release operations. Enforce strict contract checks and plan any
  later separately approved publication. 2 tasks.
- `shared/community/`: Contributor experience. Prepare respectful synthetic issue intake and honest
  announcement drafts without outreach. 2 tasks.
- `shared/casework/`: the charter (`open-source-infrastructure-foundation.md`), the first case
  (`line-ledger-repair-cycle.md`: Line Ledger: repair duplicate counting and out-of-order state
  reduction) and 16 starter files in `artifacts/`.

## What maps cleanly, and what does not

- The starter file `docs/community-intake.md` has the same note name as
  `shared/community/community-intake.md`, and note apps and the Hive agent resolve [[links]] by name
  alone, so its note is `community-intake-2.md` (the Hive agent's rule for a taken name).
- 9 of 16 starter files are not markdown, so they sit in `shared/casework/artifacts/` as fenced
  notes named `<file>.md`, and each note's `file` and `sha256` name the file and its exact bytes
  once copied out. In a Hive they are data: to run a reference tool, copy its fenced text into a
  workspace file of that name, check the SHA-256, and review it first.
- Task outputs are logical `deliverables/` paths. A folder Hive holds only markdown, so a team adds
  each finished output as a note; the template creates none.
- The organization's planned world id (`demo-open-source-infrastructure-foundation`) has no
  folder-Hive counterpart: a folder Hive has its own `hive:` id and no world. No task has an `owner`
  until a member claims it.
