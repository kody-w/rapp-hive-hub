# Changelog

## Target shape (experimental branch; `main` keeps the previous design)

- The hub is now a tree of markdown cards, one fact per file, plus `tools/build.py`, a
  byte-identical copy of the generic Hive Hub's standard-library builder. It checks every card
  and starter template and generates `views/`: the api/v2 JSON, a static site that needs no
  JavaScript, and `chants.txt`.
- Cards: the protocols `hive-md` (experimental), `rapp-hive/1` (in force) and `rapp-hive/2`
  (frozen), the synthetic Contoso model Hive (experimental, no live shared copy), the RAPP Hive
  (planned, no pins yet), and one organization card (specified) and one starter card
  (experimental) for each of the twelve starters.
- The twelve organization seeds became `starters/<slug>/` Hive templates: `HIVE.md` with 2
  approvals, a `fields:` hint and a `hive:` placeholder, one note per task under `shared/<team>/`
  with `[[id]]` links between dependencies, the charter, the first case and the starter files as
  notes. Each README.md says where the starter fits and what does not map cleanly.
- Joining and starting happen only in the person's own Brainstem, with the card's pins or the
  template. The hub writes nothing into a Hive, keeps no subscription state and runs nothing.
- Removed the generated api v1 and site, the public inputs and receipts, the seed packages and
  ZIPs, join cards, boot Eggs with the SeedRunner organ, the inherited Python core, CLI,
  subscriptions, bootstrap and adapters, the build scripts, the skills, the old docs and tests,
  and the inactive workflow templates. The earlier additive fit on this branch is superseded.
- Kept the frozen `hive-hub-chant/1` vocabulary; a chant now comes from a card's SHA-256.

## Unreleased

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
