# The Autonomous Software Improvement Lab

A generic starter for continuous, consensus-driven, autonomous improvement of
any software, with the AI host you already use. Each round (a generation):
**eight independent strategies look at your software, the loop builds what
they converge on, verifies it independently, and repeats until you say stop.
Everything stays local by default:** local commits on a separate integration
branch, nothing pushed or published.

What is in this starter:

| Path | What it is |
|---|---|
| `docs/playbook.md` | The method, step by step, with every rule learned from running it |
| `docs/safety.md` | Hard safety rules, protected paths, hermetic tests, the harness firewall pattern |
| `docs/consensus.md` | How a tally is decided, with a worked, clearly illustrative example |
| `templates/` | Strategist brief, integrator brief, report format and living review, with `{PLACEHOLDERS}` the kit fills |
| `data/strategy-pool.json` | 49 generic strategy lenses for any software |
| `data/improver.config.example.json`, `data/improver.config.schema.json` | Kit configuration and its schema |
| `reference/improver.py` | The kit: offline, deterministic, Python 3.10+ standard library, no AI calls |
| `reference/test_improver.py` | The kit's tests, with illustrative sample reports as fixtures |
| `target/` | Practice Shelf, a small, deliberately flawed practice target, and its answer key |

The kit prepares and records; your AI host (for example a command-line agent
in an autonomous mode) spawns the agents. Every kit command that changes
anything prints its plan and changes nothing without `--apply`.

## 1. Initialize this seed with the trusted RAPP Work SDK

This package is inert starter data. Downloading it, browsing it or joining it
through the RAPP Hive Hub never runs anything and grants no authority.

1. Verify the package: the ZIP byte count and SHA-256, the file inventory in
   `seed.json`, and the Dial Record, protocol, learning bundle, conformance
   contract and adapter shown on its hub page.
2. Use only the exact, locally trusted RAPP Work SDK and RAPP/1 revisions
   pinned in `seed.json` and `initialize.json`. If they are not available, stop:
   that is a blocker, not something to work around.
3. Choose your own owner label and a new local destination. Plan the native
   Organization and each team and casework Workspace listed in
   `initialize.json`; review each complete plan and approve its exact digest
   before applying it.
4. Review the declared template files, then copy them into each new
   workspace's `work/` directory without replacing anything. Register the
   same-world workspace pointers with `Organization.plan_register` and
   `apply_register`, approving each complete plan first.
5. Open the casework task board and claim the ready tasks. These starter files
   end up in the casework workspace under `work/starter/`.

Running the kit, or anything in `target/`, is a separate decision you make
later, on your own machine.

## 2. Practice on Practice Shelf first

Run one whole generation on something harmless before pointing the kit at
real software. Work from the directory that contains `starter/` (in the
casework workspace, that is `work/`):

```sh
mkdir -p practice/practice-shelf
cp starter/target/shelf.py starter/target/test_shelf.py starter/target/README.md practice/practice-shelf/
cd practice/practice-shelf && git init -b main && git add . && git commit -m "Practice Shelf as shipped" && cd ..
cp ../starter/data/improver.config.example.json improver.config.json
K="python3 ../starter/reference/improver.py --config improver.config.json"
$K init            # read the plan
$K init --apply
```

Keep `target/ANSWER-KEY.md` out of the practice repository, and read it only
after the tally is drafted. The case's first tasks make the practice tests
hermetic (as shipped, they write into your real home directory; the target's
README explains) and record the baseline. Then follow `docs/playbook.md`:

```sh
$K baseline --apply                 # the bar every change must hold
$K plan 1 --apply                   # eight never-used lenses, seeded
$K render 1 --apply                 # one brief per strategist
$K worktrees 1 --apply              # one worktree and branch each
$K audit g1 --mark --apply          # snapshot protected paths first
# launch 8 background strategists, each with the full text of its brief
$K status                           # who reported, who is working, who died
$K tally 1 --apply                  # draft TALLY.md and the integrator brief
$K worktrees 1 --integrator --apply # then launch the integrator
$K baseline --at <integrator worktree> --label g1-verify --apply
$K audit g1                         # must be CLEAN before anything moves
git -C practice-shelf fetch . improve/g1-integration:improve/integration
$K record 1 --commit <sha> --summary "..." --apply
```

To see a tally before running any AI, write the illustrative sample reports
into a planned generation, then tally them. They are labeled as fixtures:

```sh
python3 ../starter/reference/test_improver.py write-samples --config improver.config.json --gen 1
```

Delete those sample reports before a real run.

## 3. Then point it at your own software

1. Agree the intake with yourself or your team: what matters, an optional
   focus, which paths hold live data and configuration, which live software
   and ports must never be touched.
2. Write your own `improver.config.json`: project path, base branch,
   integration branch, the number of strategists, every verify command by
   name (lint or typecheck, unit, contract, end-to-end, build), an isolated
   harness command if your software has a user interface or live services,
   protected paths, live ports, environment prefixes to clear, and a state
   directory outside the project. The schema documents every field.
3. Make your tests hermetic and build the harness (`docs/safety.md`).
4. Run `init`, `baseline`, and your first generation as in the playbook.

## 4. Leave it running, and stop it

Give your AI host the playbook and this instruction: run generations
continuously, check `status` before every step, and stop starting new work as
soon as STOP is requested. The living review, `review/REVIEW.md` in the state
directory, is your entry point: status, next action, every generation's
decision, verification and receipts, owner requests, recurring problems,
kept branches, and how to try the integration branch or switch back.

- Stop: tell the host, or `$K stop --reason "..." --apply`, or create the file
  `STOP` in the state directory. While STOP exists, the kit refuses to plan a
  generation or create worktrees.
- Continue: `$K resume --apply`. If the host restarted and killed its agents,
  resume archives the interrupted generation so it is re-run from the current
  head and never counted.
- Ask for something directly: a dedicated implementer delivers it outside the
  vote, verified the same way (playbook, section 4).

Nothing is pushed, published or released unless you explicitly ask for it.

## License

The files in this starter are original. `LICENSE.txt` applies to them.
