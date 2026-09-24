# The One-Person Conglomerate: starter

Five small businesses, one explicitly limited founder.

Allocate a synthetic founder's attention across five distinct business units using bounded learning
experiments, shared operating functions, and evidence rather than invented revenue.

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
2. **Organization** (specified): the org card `one-person-conglomerate` plans one accountable owner,
   one world (planned id `demo-one-person-conglomerate`), one policy, one release scope and exactly
   one Hive. No estate has activated canonical `rapp-work/1` yet (G16), and it cannot bind a folder
   Hive yet (G10).
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
- with `npx degit kody-w/rapp-hive-hub/starters/one-person-conglomerate#experimental/organism-fit one-person-conglomerate`;
- or as a ZIP of the repository.

## Create the Hive

1. Ask your Brainstem to create a Hive with its Hive agent: `create` with the title "The One-Person
   Conglomerate", `approvals` 2 and the `fields` hint from `HIVE.md`. The Hive agent writes a fresh
   `hive:` id and signs your key file into `members/`.
2. Pin this starter's `shared/` folder as a reference, then `bring` each room, with path `<room>`
   and to `shared/<room>`. Pin `shared/`, not this folder: the Hive agent will not bring from a
   folder whose `HIVE.md` names a Hive, and this template's `HIVE.md` holds a placeholder id. Every
   file arrives in one signed commit, stamped with `brought_from` and `brought_sha256`.
3. Invite people. Each person's Brainstem files one signed request, and members admit it with the
   Hive's approvals.

Nothing applies until you confirm the exact proposal in a later turn.

## Rooms

- `shared/executive-office/`: Portfolio owner. Own capacity limits, decisions, and stop conditions
  without confusing a recommendation with authority. 2 tasks.
- `shared/portfolio-research/`: Shared research. Separate assumptions, public desk research, and
  later consented field evidence. 1 task.
- `shared/portfolio-finance/`: Shared finance. Maintain the founder-hour and hypothetical cash
  worksheet; no profit forecasts masquerade as facts. 2 tasks.
- `shared/platform-engineering/`: Shared engineering. Maintain the offline allocation analysis and
  reusable CSV preflight reference tool. 2 tasks.
- `shared/portfolio-go-to-market/`: Shared go-to-market. Draft differentiated offers and
  approval-gated learning invitations for each unit. 1 task.
- `shared/ledgerleaf-tools/`: Business unit: file utilities. Explore small offline CSV quality tools
  for people preparing imports. 1 task.
- `shared/fieldnote-guides/`: Business unit: practical guides. Develop original, non-safety-critical
  workspace organization guides. 1 task.
- `shared/quietbench-templates/`: Business unit: accessible templates. Prototype accessible meeting
  and purchasing-request templates. 1 task.
- `shared/routepaper-planners/`: Business unit: printable planners. Explore printable errand
  grouping sheets without collecting real location histories. 1 task.
- `shared/tinylesson-studio/`: Business unit: short lessons. Create original offline lessons on
  basic file organization and data hygiene. 1 task.
- `shared/casework/`: the charter (`one-person-conglomerate.md`), the first case
  (`first-portfolio-cycle.md`: Choose no more than three learning experiments for a 40-hour week)
  and 14 starter files in `artifacts/`.

## What maps cleanly, and what does not

- 10 of 14 starter files are not markdown, so they sit in `shared/casework/artifacts/` as fenced
  notes named `<file>.md`, and each note's `file` and `sha256` name the file and its exact bytes
  once copied out. In a Hive they are data: to run a reference tool, copy its fenced text into a
  workspace file of that name, check the SHA-256, and review it first.
- Task outputs are logical `deliverables/` paths. A folder Hive holds only markdown, so a team adds
  each finished output as a note; the template creates none.
- The organization's planned world id (`demo-one-person-conglomerate`) has no folder-Hive
  counterpart: a folder Hive has its own `hive:` id and no world. No task has an `owner` until a
  member claims it.
