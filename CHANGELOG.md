# Changelog

## Unreleased

- Mapped every organization starter onto the RAPP/1 organism. Each package now
  carries `ORGANISM.md`, which says layer by layer what the starter touches (an
  Organization plan, specified; a `rapp-hive/1` Private Hive today, or a folder
  Hive as an experimental option; members' Workspaces and Brainstems), with the
  honest status words in force, specified, experimental, candidate and frozen.
- Added `scripts/folder_hive.py`, a deterministic standard-library generator that
  turns each starter's teams, tasks, charter and files into an inert folder-Hive
  template (`folder-hive/`: `HIVE.md` with 2 approvals, a `fields:` hint and an
  empty `hive:`, one note per task linked by `[[id]]`, and the starter files as
  notes in `shared/casework/artifacts/`). It follows the Hive folder convention's
  file rules, pinned to `kody-w/rapp-model-hive@2bd7c95`, and notes where a
  starter's data does not map cleanly instead of inventing structure.
- Packages only gained files; every earlier file keeps its bytes and `seed.json`
  lists the new inventory. Because a Dial Record commits to its exact package,
  each starter has a successor declaration, record, join card and chant. The
  predecessors' records, cards, declarations, seed documents, ZIPs and the
  distribution receipt stay byte-exact at their content addresses, outside the
  active dialbook (`scripts/seed_predecessors.py`, `seed-src/SEED_PREDECESSORS.json`),
  and receipt 0005 records the step. Historical receipts now keep the URL of the
  site that published them.
- Added a consistent "Where this fits" section to the README, `llms.txt`, docs,
  the hive-network skill (1.1.0), `seed-src/README.md`, the examples and the site,
  which also shows each starter's template tree and its earlier package.
- Allowed public links to `kody-w/rapp-model-hive` for the Hive folder convention.
- Added the generic First-Party Rapplication Company organization seed:
  seven scoped teams and separate casework, a configurable founder-CEO charter,
  craftsmanship and promotion templates, and a synthetic checklist case.
- Included an inert stage/gate specification, an acceptance-linked task DAG,
  and a tested offline command reference. Independent verification, a separate
  decision receipt, nested privacy and license review, and owner-only PR merge
  remain explicit gates; no running company or authenticated authority is claimed.
- Regenerated the public-only catalog, exact package inventory, deterministic
  ZIP, join cards, QR codes, and release inventory for twelve starters.
- Gave the shared keyboard-focus outline at least 3:1 contrast across light
  and dark surfaces, with automated contrast coverage. Seed footers now label
  the fixed build epoch without implying fresh verification, and the checklist
  reference explains its exact identifier grammar with a valid example.
- Every catalog organization seed now ships a Brainstem boot: a deterministic
  RAPP/1 organism Egg (`rapp-seed-boot/1`) with the exact seed record, a soul,
  and the generic SeedRunner organ, published beside the seed with a plan-first
  hatcher (`hub/boot/hatch_seed.py`) and a boot section on each seed page.
- Added `scripts/seed_boot.py` (`pin`, `build [--check]`, `prove`) and
  conformance tests binding every boot Egg to its published seed.

## 0.1.1 - 2026-09-18

- Added protocol-neutral `hive-hub-chant/1` with deterministic seven-word
  locators derived from a complete `dial:sha256:` Dial Record ID.
- Corrected the public sample chant while preserving the original 0.1.0 source
  URLs, release object, schemas, and device-local dialbook compatibility.
- Added a versioned `hive-hub-dialbook/2` profile that separates aliases from
  chants and cryptographically binds locator and declaration references.

## 0.1.0 - 2026-09-18

- Introduced the typed, standard-library-only `hive_hub` package and
  `hive-hub` CLI.
- Added closed canonical contracts and packaged JSON Schemas.
- Added separated local/public/private dialbooks and collision-safe dialing.
- Added inert protocol learning, adapter registration, join cards,
  plan/apply/revert subscriptions, and one-card bootstrap.
- Added mandatory ACL semantics and optional scope/epoch-bound `acl+qr`.
- Added bounded no-follow storage, duplicate-key refusal, atomic no-replace
  writes, clean JSON errors, and zero-network tests.
- Integrated six exact-fingerprint stdlib adapters through a lazy, optional
  core bridge and plan-first CLI registration.
- Added the locked universal Agent Skill with exact core camera-AI card support
  and repository-neutral verified join-contract detection.
- Added the public-only deterministic static API, Pages join surface, release
  metadata, published core schemas, dual QR cards, and append-only receipts.
- Added deterministic source inventory, privacy scanning, packaging checks, and
  Python/Node CI matrices.
- Hardened Windows link verification with no-follow Win32 handle metadata so
  ordinary files report one link and hardlinks fail closed.
