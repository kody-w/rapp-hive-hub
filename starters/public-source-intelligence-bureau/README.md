# The Public-Source Intelligence Bureau: starter

Make a business-technology judgment that can be traced back to every included row.

Investigate a fictional offline-kiosk launch using original synthetic public-style notices, release
notes, lab notes, and benchmark rows. Separate claims from verification, compare competing
hypotheses, expose contradictions and uncertainty, and prepare a decision-gated next investigation.

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
2. **Organization** (specified): the org card `public-source-intelligence-bureau` plans one
   accountable owner, one world (planned id `demo-public-source-intelligence-bureau`), one policy,
   one release scope and exactly one Hive. No estate has activated canonical `rapp-work/1` yet
   (G16), and it cannot bind a folder Hive yet (G10).
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
- with `npx degit kody-w/rapp-hive-hub/starters/public-source-intelligence-bureau#experimental/organism-fit public-source-intelligence-bureau`;
- or as a ZIP of the repository.

## Create the Hive

1. Ask your Brainstem to create a Hive with its Hive agent: `create` with the title "The
   Public-Source Intelligence Bureau", `approvals` 2 and the `fields` hint from `HIVE.md`. The Hive
   agent writes a fresh `hive:` id and signs your key file into `members/`.
2. Pin this starter's `shared/` folder as a reference, then `bring` each room, with path `<room>`
   and to `shared/<room>`. Pin `shared/`, not this folder: the Hive agent will not bring from a
   folder whose `HIVE.md` names a Hive, and this template's `HIVE.md` holds a placeholder id. Every
   file arrives in one signed commit, stamped with `brought_from` and `brought_sha256`.
3. Invite people. Each person's Brainstem files one signed request, and members admit it with the
   Hive's approvals.

Nothing applies until you confirm the exact proposal in a later turn.

## Rooms

- `shared/collection/`: collection-editor. Maintain a bounded local corpus and exact file/row
  citations, with no live collection or private data. 3 tasks.
- `shared/analysis/`: technology-analyst. Reconstruct chronology and distinguish announcement scope
  from demonstrated technical behavior. 1 task.
- `shared/competing-hypotheses/`: hypothesis-reviewer. Test alternative explanations and challenge
  confidence without counting correlated sources as independent votes. 2 tasks.
- `shared/verification/`: evidence-verifier. Reproduce benchmark arithmetic, audit references, and
  classify unresolved conflicts and measurement gaps. 2 tasks.
- `shared/briefing/`: briefing-editor. Deliver a bounded recommendation, uncertainties, and explicit
  owner decision gates. 2 tasks.
- `shared/casework/`: the charter (`public-source-intelligence-bureau.md`), the first case
  (`juniper-offline-pilot.md`: Can fictional Juniper Queue support an unattended offline pilot on 15
  October?) and 14 starter files in `artifacts/`.

## What maps cleanly, and what does not

- 12 of 14 starter files are not markdown, so they sit in `shared/casework/artifacts/` as fenced
  notes named `<file>.md`, and each note's `file` and `sha256` name the file and its exact bytes
  once copied out. In a Hive they are data: to run a reference tool, copy its fenced text into a
  workspace file of that name, check the SHA-256, and review it first.
- Task outputs are logical `deliverables/` paths. A folder Hive holds only markdown, so a team adds
  each finished output as a note; the template creates none.
- The organization's planned world id (`demo-public-source-intelligence-bureau`) has no folder-Hive
  counterpart: a folder Hive has its own `hive:` id and no world. No task has an `owner` until a
  member claims it.
