# RAPP Hive Hub

**`main` keeps the previous design; this branch is the target shape.** On `main`, RAPP Hive Hub
is a static site and api v1 built by Node and Python scripts, with downloadable organization seed
ZIPs, join cards and QR codes, boot Eggs with a SeedRunner organ, and the inherited Python core,
CLI and adapters. Here it is a tree of markdown cards, twelve starter templates and one
standard-library builder, and nothing else.

A hub is a tree of markdown cards, one fact per file, plus a builder that generates every view.
Reorganizing the hub means moving card files. Nothing in a hub runs, and joining happens in your
own Brainstem. This is the RAPP instance of the generic hub (`kody-w/hive-hub`): the same shape,
with `tools/build.py` a byte-identical copy of its builder. Everything RAPP-specific lives in
`HUB.md`, `cards/` and `starters/`.

```text
HUB.md                      what this hub is, who curates it, how to submit a card, where it fits
cards/protocols/<id>.md     one card per Hive protocol
cards/hives/<slug>.md       one card per Hive
cards/orgs/<slug>.md        one card per organization
cards/starters/<slug>.md    one card per starter
starters/<slug>/            a Hive template tree (HIVE.md, .gitattributes, shared/) plus README.md
tools/build.py              standard library only; builds views/; --check compares
views/                      GENERATED: api/v2/, site/ and chants.txt
llms.txt                    a short entry for AI apps
tests/                      the builder's tests and this hub's own
```

## The cards

| Card | Status |
| --- | --- |
| [`hive-md`](cards/protocols/hive-md.md): the Hive folder convention | experimental |
| [`rapp-hive/1`](cards/protocols/rapp-hive/1.md): RAPP Private Hive | in force |
| [`rapp-hive/2`](cards/protocols/rapp-hive/2.md): frozen research record | frozen |
| [`contoso-model-hive`](cards/hives/contoso-model-hive.md): a synthetic model Hive with no live shared copy | experimental |
| [`rapp-hive`](cards/hives/rapp-hive.md): the RAPP Hive, with no pins yet | planned |
| Twelve [organization cards](cards/orgs/): each a RAPP Work organization plan | specified |
| Twelve [starter cards](cards/starters/): each names its template under `starters/` | experimental |

The protocol cards and the Contoso card are the same files as in the generic hub, and so are
`tools/build.py`, `tests/test_build.py`, `.gitattributes` and the CI workflow.

## The starters

Each starter is a Hive template for the Hive folder convention. `HIVE.md` holds 2 approvals, a
`fields:` hint for the task shape and a `hive:` placeholder that the founder's Brainstem fills at
create time. Each team is a room under `shared/<team>/` with one note per task (`id`, `title`,
`status`, `depends_on`, and `[[id]]` links between dependencies); `shared/casework/` holds the
charter, the first case and the starter files as notes in `artifacts/`. The README.md beside each
template says where the starter fits, how to pull it down, how to create the Hive, and what does
not map cleanly. It is documentation, never part of the Hive.

Three caveats apply to every starter: non-markdown starter files are fenced notes (their `file`
and `sha256` name the exact file once copied out), task outputs are logical paths that a team adds
as notes, and the planned world id has no folder-Hive counterpart.

| Starter | Rooms | Also does not map cleanly |
| --- | --- | --- |
| [The AI Video Studio](starters/ai-video-studio/README.md) | 10 | three tools lose a Node shebang line |
| [The Applied Invention Lab](starters/applied-invention-lab/README.md) | 6 | nothing |
| [The Enterprise Transformation Firm](starters/enterprise-transformation-firm/README.md) | 7 | nothing |
| [The Federation Prime Contractor](starters/federation-prime-contractor/README.md) | 6 | partner briefs need `rapp-federation/1` agreements (candidate) |
| [The First-Party Rapplication Company](starters/first-party-rapplication-company/README.md) | 8 | nothing |
| [The Independent Game Studio](starters/independent-game-studio/README.md) | 8 | nothing |
| [The Micro-Manufacturing Company](starters/micro-manufacturing-company/README.md) | 8 | nothing |
| [The One-Person Conglomerate](starters/one-person-conglomerate/README.md) | 11 | nothing |
| [The Open-Source Infrastructure Foundation](starters/open-source-infrastructure-foundation/README.md) | 8 | one note is renamed `community-intake-2.md` to keep note names unique |
| [The Product Launch Company](starters/product-launch-company/README.md) | 7 | nothing |
| [The Public-Source Intelligence Bureau](starters/public-source-intelligence-bureau/README.md) | 6 | nothing |
| [The Turnaround Firm](starters/turnaround-firm/README.md) | 6 | nothing |

## Build and check

```bash
python tools/build.py            # check every card and template, and write views/
python tools/build.py --check    # rebuild in memory and compare with views/ byte for byte
python -m unittest discover -s tests
```

Never edit `views/` by hand. CI (`.github/workflows/ci.yml`, the same workflow as the generic hub)
runs the check and the tests on Linux, macOS and Windows with Python 3.12 and on Linux with Python
3.11; publishing a workflow file needs the `workflow` scope. With a pinned copy of the convention's
agent (`kody-w/rapp-model-hive` at `2bd7c95`, as `HIVE_MD_AGENT` or under
`.hive-hub/deps/rapp-model-hive/`), the tests also run that agent's own file rules over every
template file.

## Card fields

Each card is `---`, one `key: value` line per field, `---`, a blank line and a short body. The
builder refuses unknown fields, missing pins, commit ids that are not full, bad key fingerprints,
duplicate slugs, credentials in URLs and absolute paths.

| Card | Fields |
| --- | --- |
| `card: protocol` | `id`, `name`, `status`, `spec` (a URL at a full commit id) and `spec_sha256`; optional `checker` and `checker_sha256`, `agent` and `agent_sha256` |
| `card: hive` | `name`, `protocol`, `status`, `hive`, `root`, `founder`, `channel`; optional `public_copy`, `address` and `org`. A `planned` Hive may omit all three pins |
| `card: organization` | `name`, `status`, `hive` (a hive slug or `template`); optional `starter` |
| `card: starter` | `name`, `status`, `template` (`starters/<folder>/`), `org` |

Statuses are `in force`, `specified`, `experimental`, `candidate`, `planned` and `frozen`;
protocols do not use `planned`. A card's sha256 is the SHA-256 of its file, and its chant is seven
words from the first seven bytes of that digest, over the frozen `hive-hub-chant/1` vocabulary. A
chant is a locator, never authority; collisions are listed in `views/chants.txt`.

## Join

1. Dial a chant from `views/chants.txt`, or open a card.
2. Check the card's sha256 against `views/api/v2/index.json`.
3. Give the card to your Brainstem. Its Hive agent joins with the card's `address`, `hive`,
   `root` and `founder`: it clones the Hive, verifies the root and the founder fingerprint, writes
   one SSH-signed request file, and sends it the way the card's `channel` says.

To start from a starter instead, pull `starters/<slug>/` down read-only (the Hive agent's
`reference`, `npx degit` or a ZIP) and let your Brainstem's Hive agent create a new Hive from it,
as its README says. The hub never writes into a Hive, keeps no subscription state and runs
nothing.

## Removed on this branch

The generated api v1 and site (`api/`, `hub/`, `index.html`, `.well-known/`, `.nojekyll`), their
public inputs and receipts (`public-src/`, `public-manifest.json`, `public-withdrawals.json`),
the organization seed packages and ZIPs with their initialization plans and pins (`seed-src/`),
join cards and QR codes, boot Eggs with the SeedRunner organ and hatcher, the inherited Python
core, CLI, subscriptions, bootstrap and adapters (`src/`, `adapters/`, `pyproject.toml`,
`MANIFEST.in`), the Node and Python build scripts (`scripts/`, `package.json`), the locked Agent
Skill and the hive-network skill (`skills/`), the generic example, the old docs and tests, the
release inventories, and the inactive workflow templates. The earlier additive fit on this branch
(organism maps, templates inside seed packages and successor records) is superseded too. The
twelve starters live on as `starters/`, and the frozen chant vocabulary lives on in
`tools/build.py`.
