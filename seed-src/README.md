# Public RAPP Work organization seeds

These sources build portable organization starters, not prompts and not activated
Hives. Each package contains scoped team work, a synthetic intake case, a task
dependency graph, original datasets, and usable starter artifacts.

## Where this fits

Read the RAPP/1 organism bottom to top: 0 RAPP/1 (in force) · 1 Estate (in force)
· 2 Organization, canonical `rapp-work/1` (specified: no estate has activated it
yet, G16; it cannot bind a folder Hive yet, G10) · 3 Hive, a `rapp-hive/1`
Private Hive (in force, the one Hive an organization can hold today) or the Hive
folder convention (experimental) · 4 your device · 5 Brainstem (in force) · 6
you. A starter touches the Organization layer as a plan, the Hive layer as an
optional folder-Hive template, and each member's device as native Workspaces.
This hub adds RAPP Work starters plus discovery and join across Hives; transport
carries, signatures decide. `rapp-hive/2` is frozen as a research record. Maps:
[ECOSYSTEM.md](https://github.com/kody-w/rapp-work/blob/experimental/rapp-work-constitution/ECOSYSTEM.md),
[CONSTITUTION.md](https://github.com/kody-w/rapp-work/blob/experimental/rapp-work-constitution/CONSTITUTION.md),
[Hive folder convention](https://github.com/kody-w/rapp-model-hive/blob/experimental/hive-md/HIVE-MD.md).

A seed folder here, like a downloaded ZIP, is a reference in its own shape:
read it as data, and bring pieces into a Hive only by signed copy.

The package format is `hive-hub-organization-seed/1`. It is an inert packaging
format, not an additional RAPP Work operation or authority-bearing payload.
Organization and Workspace creation uses the exact pinned `rapp-work-sdk/1`
implementation. The consumer chooses its owner and destination, reviews the
native plans, and approves their complete digests before any setup. Each
organization routes through workspace pointers; it does not absorb team content.

## Source layout

Each explicitly listed organization has:

```text
organizations/<slug>/blueprint.json
organizations/<slug>/files/<declared-relative-path>
```

The builder opens only files individually named by `blueprint.files`. Files are
original, synthetic, public seed material. Never read or copy private catalogs,
private Hives, customer workspaces, credentials, provider stores, or local paths.

A blueprint has exactly these keys:

- `schema`: `hive-hub-organization-blueprint/1`
- `slug`, `name`, `tagline`, `mission`: stable identity labels and useful description
- `world_id`: a lowercase, hyphenated demonstration world, at most 64 characters
- `teams`: 5-12 objects with `slug`, `name`, `role`, and `purpose`
- `case`: an object with `id`, `title`, `brief`, `inputs`, and `success_criteria`
- `tasks`: 6-50 objects with `id`, `team`, `title`, `instructions`, `inputs`,
  `outputs`, `depends_on`, and `acceptance`
- `files`: 6-24 distinct, explicitly listed relative UTF-8 file paths
- `related_seeds`: zero or more other catalog slugs, as discovery-only references

IDs and team slugs are lowercase and hyphenated. Each team owns at least one
task. Dependencies form a DAG. Inputs name a declared seed file or an output of
a prerequisite task. Outputs are unique paths under `deliverables/`. Acceptance
criteria are concrete and reviewable. Initial tasks are pending; reference
artifacts are examples, never fabricated evidence of completed work.

Include original structured sample data, at least one usable starter artifact
(for example a small offline app, calculation program, or parametric design),
and enough operating material to start the case. No TODO-only files, fake
customers, fake market validation, or invented completed business results.
Scripts in packages remain inert: neither browsing nor joining runs them.

## Generated organism files

`scripts/organization_seeds.py` adds two generated parts to every package
without changing the bytes of any other package file: `ORGANISM.md`, which says
where the starter fits layer by layer, and `folder-hive/`, an inert template in
the Hive folder convention produced by `scripts/folder_hive.py` from the
blueprint and its files. Authors never edit them. If a starter's data does not
map cleanly to a folder Hive, the generator says so in the starter's notes
instead of inventing structure.

A changed package gets a successor record. `SEED_PREDECESSORS.json` pins each
starter's earlier record, cards, declaration, seed document and ZIP, which
`scripts/seed_predecessors.py` keeps byte for byte under `public-src/historical/`.

Cross-organization references are candidate partner briefs, not cross-world
workspace registration or federation activation. External effects, private
membership, signing, spending, and publication require separate owner authority.
