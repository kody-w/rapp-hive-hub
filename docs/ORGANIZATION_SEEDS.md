# Public RAPP Work organization seeds

These are complete starter packages, not prompts or activated companies.
Browse [the catalog](https://kody-w.github.io/hive-hub/hub/#organizations) or
read [its static API](https://kody-w.github.io/hive-hub/api/hive-hub/v1/organization-seeds.json).

Give any AI the complete
[global network skill](https://kody-w.github.io/hive-hub/hub/skills/hive-network/SKILL.md).
It covers discovery, local setup through the trusted native SDK, scoped work,
and owner-reviewed public contributions. A web-only AI can inspect; it cannot
claim to create local files or submit changes without those capabilities.

| Organization | Seed |
| --- | --- |
| The One-Person Conglomerate | [Open](https://kody-w.github.io/hive-hub/hub/seeds/one-person-conglomerate/) |
| The Enterprise Transformation Firm | [Open](https://kody-w.github.io/hive-hub/hub/seeds/enterprise-transformation-firm/) |
| The Product Launch Company | [Open](https://kody-w.github.io/hive-hub/hub/seeds/product-launch-company/) |
| The Open-Source Infrastructure Foundation | [Open](https://kody-w.github.io/hive-hub/hub/seeds/open-source-infrastructure-foundation/) |
| The Applied Invention Lab | [Open](https://kody-w.github.io/hive-hub/hub/seeds/applied-invention-lab/) |
| The Independent Game Studio | [Open](https://kody-w.github.io/hive-hub/hub/seeds/independent-game-studio/) |
| The Micro-Manufacturing Company | [Open](https://kody-w.github.io/hive-hub/hub/seeds/micro-manufacturing-company/) |
| The Public-Source Intelligence Bureau | [Open](https://kody-w.github.io/hive-hub/hub/seeds/public-source-intelligence-bureau/) |
| The Turnaround Firm | [Open](https://kody-w.github.io/hive-hub/hub/seeds/turnaround-firm/) |
| The Federation Prime Contractor | [Open](https://kody-w.github.io/hive-hub/hub/seeds/federation-prime-contractor/) |
| The AI Video Studio | [Open](https://kody-w.github.io/rapp-hive-hub/hub/seeds/ai-video-studio/) |
| The First-Party Rapplication Company | [Open](https://kody-w.github.io/rapp-hive-hub/hub/seeds/first-party-rapplication-company/) |

The First-Party Rapplication Company is an additional seed in the RAPP-focused
distribution. It contains seven team workspaces plus casework, an unconfigured
founder-CEO persona slot, a craftsmanship rubric, and a pipeline from idea to
internal use, critique, iteration, independent verification, and an owner-merged
public promotion PR. Its runnable checklist reference uses a fixed command
grammar; unit tests do not claim live chat qualification. The supplied forms
are unsigned templates, not approval receipts or activated authority.

## Where this fits

Read the RAPP/1 organism bottom to top: 0 RAPP/1 (in force) · 1 Estate, a signed
registry with protocol pins (in force) · 2 Organization, canonical `rapp-work/1`
with one accountable owner, one world, one policy, one release scope and exactly
one Hive (specified: no estate has activated it yet, G16; it cannot bind a folder
Hive yet, G10) · 3 Hive, a `rapp-hive/1` Private Hive (in force, the one Hive an
organization can hold today) or the Hive folder convention (experimental) · 4 your
device: Hive copies, references and private workspaces · 5 Brainstem, the one
surface you talk to (in force) · 6 you. This hub is RAPP Work starters plus
discovery and join across Hives, part of the Hive Mind (candidate) beside the
stack; transport carries, signatures decide. `rapp-hive/2` is frozen as a
research record. See [ECOSYSTEM.md](https://github.com/kody-w/rapp-work/blob/experimental/rapp-work-constitution/ECOSYSTEM.md),
[CONSTITUTION.md](https://github.com/kody-w/rapp-work/blob/experimental/rapp-work-constitution/CONSTITUTION.md)
and the [Hive folder convention](https://github.com/kody-w/rapp-model-hive/blob/experimental/hive-md/HIVE-MD.md).

Every starter is a package, not an activated organization. Each one touches the
same layers, and its `ORGANISM.md` and seed page say so in its own terms:

- **Organization (specified):** an Organization plan with one owner you choose,
  one demonstration world, its teams and one case. The SDK `Organization` that
  `initialize.json` plans is a pointer-only routing object (G11 proposes calling
  it a workspace index).
- **Hive:** today the one Hive an organization can hold is a `rapp-hive/1`
  Private Hive (in force), which the package does not declare and its owner
  would create separately; as an experimental option, the inert `folder-hive/`
  template.
- **Your device and Brainstem:** each member's scoped Workspaces from
  `templates/` (in force, through the pinned SDK), the boot Egg with its
  SeedRunner organ (experimental), and the Hive agent that creates a folder Hive.

### Folder-Hive templates (experimental)

`scripts/folder_hive.py` (standard library only) turns each starter's teams,
tasks, charter and starter files into a tree in the
[Hive folder convention](https://github.com/kody-w/rapp-model-hive/blob/experimental/hive-md/HIVE-MD.md):
`HIVE.md` (2 approvals, a `fields:` hint for this task shape, and an empty
`hive:` that the founder's Brainstem fills at create time), `.gitattributes`,
one room per team with one note per task (`id`, `title`, `status`,
`depends_on`, and `[[id]]` links), and `shared/casework/` with the charter, the
case intake and the starter files in `artifacts/`. It follows the convention's
file rules: markdown only, portable names, no instruction-file names, no hidden
file but the fixed `.gitattributes`, no absolute paths. The template is inert
data; nothing in it runs.

A founder's Brainstem creates the Hive with the Hive agent (`create` with the
starter's name, 2 approvals and the `fields:` hint), pins the unzipped package as
a reference, and brings each room by signed copy (`bring` from
`folder-hive/shared/<room>` to `shared/<room>`). Every brought file is stamped
with `brought_from` and `brought_sha256`, and nothing applies until the person
confirms the plan in a later turn. An organization cannot bind a folder Hive yet
(G10).

Every starter shares three caveats: its non-markdown starter files sit in the
template as fenced markdown notes (the `seed_file` and `seed_sha256` of each
note name the exact package file); task outputs are logical `deliverables/`
paths that a team adds as notes when the work is done; and the demonstration
world id has no folder-Hive counterpart. Beyond those:

| Starter | Rooms | Tasks | Non-markdown starter files | Also does not map cleanly |
| --- | --- | --- | --- | --- |
| The One-Person Conglomerate | 11 | 13 | 10 of 14 | nothing |
| The Enterprise Transformation Firm | 7 | 12 | 8 of 14 | nothing |
| The Product Launch Company | 7 | 12 | 7 of 15 | nothing |
| The Open-Source Infrastructure Foundation | 8 | 12 | 9 of 16 | `docs/community-intake.md` shares a note name with the task `community-intake`, so its note is `community-intake-2.md` |
| The Applied Invention Lab | 6 | 10 | 8 of 15 | nothing |
| The Independent Game Studio | 8 | 10 | 10 of 13 | nothing |
| The Micro-Manufacturing Company | 8 | 10 | 12 of 14 | nothing |
| The Public-Source Intelligence Bureau | 6 | 10 | 12 of 14 | nothing |
| The Turnaround Firm | 6 | 11 | 12 of 14 | nothing |
| The Federation Prime Contractor | 6 | 11 | 15 of 16 | its partner briefs are data; work with another organization's Hive needs `rapp-federation/1` agreements (candidate) and folder-Hive dial records (G12) |
| The AI Video Studio | 10 | 14 | 14 of 23 | nothing |
| The First-Party Rapplication Company | 8 | 21 | 12 of 21 | nothing |

### Pull a starter down as a reference

A downloaded ZIP, or a seed folder in this repository, is a reference in its own
shape: read-only, never run, read as data. The
[hive-network skill](https://kody-w.github.io/rapp-hive-hub/hub/skills/hive-network/SKILL.md)
verifies the package first. Nothing enters a Hive until a member brings a piece
of it in by one signed commit.

### Successor records

A Dial Record commits, through its declaration, to the exact seed JSON, which
embeds the ZIP and its inventory. Adding `ORGANISM.md` and `folder-hive/` left
every earlier package file's bytes unchanged but changed each package, so each
starter has a successor declaration, Dial Record, join card and chant. The
earlier records, cards, declarations, seed documents and ZIPs stay at their
content addresses, outside the active dialbook (`seed-src/SEED_PREDECESSORS.json`,
`public-src/historical/rapp-seeds-e579f9c/`), each successor declaration and seed
index entry names its predecessor, and receipt 0005 records the step. A ZIP,
join card or boot Egg someone already has keeps working.

## Package contents

- `seed.json`: package classification, exact dependency pins, and file inventory.
- `initialize.json`: native Organization/Workspace scaffold inputs, team ownership,
  template mappings, and same-world pointer registration requirements.
- `templates/teams/<team>/work/`: scoped team purpose, owned work, and acceptance.
- `templates/casework/work/`: synthetic intake, dependency-linked task board,
  success criteria, and original usable starter artifacts.
- `README.md`: initialization and operating instructions.
- `ORGANISM.md`: where the starter fits, layer by layer, and how it maps to a
  folder Hive.
- `folder-hive/`: the inert folder-Hive template (experimental).

All starter task ownership and prerequisites are explicit. A task with no
prerequisites is ready to claim; dependent tasks are blocked. No task is
silently assigned or marked completed. Reference programs, designs, and reports
are examples, not proof that a customer's engagement has been delivered.

## Initialize, do not impersonate

Give the verified seed to a capable AI host with the exact locally trusted
RAPP Work SDK. Choose your owner label and a new destination. The seed does not
contain an organization RAPPID or another person's private state.

Use the canonical SDK to plan the Organization and each member Workspace.
Approve each complete native plan and its exact digest before applying it.
Review the declared template-copy effects and native `Organization.plan_register`
plans separately. Register only same-world workspace pointers. Do not copy team
contents into the Organization or register external partners across worlds.

Joining through Hive Hub saves only a reversible local subscription and returns
an inert next step. It does not initialize the organization, install an SDK, run
downloaded code, grant access, or activate a federation. An unavailable SDK,
missing owner authorization, or an incapable host is a blocker, not success.

The prime contractor's partner references are candidate briefs. Actual external
communication, publication, spending, membership, or signing still requires
the appropriate owner authorization.

## Rebuild and verify

```bash
npm run sync:release
npm run verify
PYTHONPATH=src:. python3 -B -m unittest tests.test_organization_seeds tests.test_folder_hive
python3 -B scripts/folder_hive.py --check
python3 -B scripts/check_organization_seeds.py --exercise-native \
  --sdk-path /exact/qualified/rapp-work \
  --rapp1-path /exact/qualified/rapp-1
```

The template tests compare the restated folder rules with the convention's own
`agents/hive_agent.py` when a pinned copy (`kody-w/rapp-model-hive` at
`2bd7c95152ede719b6418b80e2bdc2cd457bf711`) sits under
`.hive-hub/deps/rapp-model-hive`; they read it as data and never import it.

The native conformance command requires the exact clean dependencies pinned by
`seed-src/SDK_PIN.json`. It initializes and verifies all organizations and member
workspaces in isolated temporary fixtures and removes those fixtures afterward.
That is structural and initialization evidence, not a signed business-protocol
receipt or activation of a user's organization.

Seed sources are bounded and individually allowlisted under `seed-src/`.
Builds never discover, read, copy, or republish private Hive state.
