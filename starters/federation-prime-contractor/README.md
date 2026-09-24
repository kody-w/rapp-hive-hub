# The Federation Prime Contractor: starter

Coordinate candidate partner work through explicit artifacts, acceptance, and owner gates.

Run a prime's own program, partner-discovery, integration, quality, and change-control teams around
a synthetic offline maker-hall intake engagement. Split proposed work among three discoverable
organization seeds, integrate only local public-reference fixtures, and rehearse rejection and
rework without activating a federation or claiming partner authority.

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
2. **Organization** (specified): the org card `federation-prime-contractor` plans one accountable
   owner, one world (planned id `demo-federation-prime-contractor`), one policy, one release scope
   and exactly one Hive. No estate has activated canonical `rapp-work/1` yet (G16), and it cannot
   bind a folder Hive yet (G10).
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
- with `npx degit kody-w/rapp-hive-hub/starters/federation-prime-contractor#experimental/organism-fit federation-prime-contractor`;
- or as a ZIP of the repository.

## Create the Hive

1. Ask your Brainstem to create a Hive with its Hive agent: `create` with the title "The Federation
   Prime Contractor", `approvals` 2 and the `fields` hint from `HIVE.md`. The Hive agent writes a
   fresh `hive:` id and signs your key file into `members/`.
2. Pin this starter's `shared/` folder as a reference, then `bring` each room, with path `<room>`
   and to `shared/<room>`. Pin `shared/`, not this folder: the Hive agent will not bring from a
   folder whose `HIVE.md` names a Hive, and this template's `HIVE.md` holds a placeholder id. Every
   file arrives in one signed commit, stamped with `brought_from` and `brought_sha256`.
3. Invite people. Each person's Brainstem files one signed request, and members admit it with the
   Hive's approvals.

Nothing applies until you confirm the exact proposal in a later turn.

## Rooms

- `shared/program-office/`: prime-program-lead. Own the fictional engagement scope, deliverable
  sequence, and conditional owner handoff. 2 tasks.
- `shared/partner-sourcing/`: partner-brief-editor. Prepare bounded discovery-only briefs for three
  candidate organizations without outreach, contracts, or workspace registration. 3 tasks.
- `shared/integration/`: integration-lead. Maintain the public data interface and assemble only
  inert local synthetic fixtures for review. 2 tasks.
- `shared/acceptance-quality/`: acceptance-reviewer. Run the offline content checks, reject
  incompatible submissions, and distinguish fixture passes from real acceptance. 2 tasks.
- `shared/change-control/`: change-controller. Track rework, scope impacts, public-artifact
  boundaries, and the missing owner approvals. 2 tasks.
- `shared/casework/`: the charter (`federation-prime-contractor.md`), the first case
  (`pocket-queue-prime-pilot.md`: Pocket Queue: a 60-attendee maker-hall intake rehearsal) and 16
  starter files in `artifacts/`.

## What maps cleanly, and what does not

- Partner briefs for other starters (`briefs/applied-invention-lab.json`,
  `briefs/enterprise-transformation-firm.json`, `briefs/product-launch-company.json`) are data in
  this Hive. Working with another organization's Hive needs signed agreements under
  rapp-federation/1 (candidate), and dial records do not describe folder Hives yet (G12), so that
  part of the case stays outside the folder Hive.
- 15 of 16 starter files are not markdown, so they sit in `shared/casework/artifacts/` as fenced
  notes named `<file>.md`, and each note's `file` and `sha256` name the file and its exact bytes
  once copied out. In a Hive they are data: to run a reference tool, copy its fenced text into a
  workspace file of that name, check the SHA-256, and review it first.
- Task outputs are logical `deliverables/` paths. A folder Hive holds only markdown, so a team adds
  each finished output as a note; the template creates none.
- The organization's planned world id (`demo-federation-prime-contractor`) has no folder-Hive
  counterpart: a folder Hive has its own `hive:` id and no world. No task has an `owner` until a
  member claims it.
