# Playbook: continuous, consensus-driven improvement of any software

This is the method, written for two readers at once: the orchestrating AI that
runs the loop, and the human owner whose software it is. It is generic. It
works for a command-line tool, a library, a service or an application with a
user interface, in any language, with any AI host that can run background
sub-agents and shell commands.

The shape of one round, called a generation: eight strategists, each with a
different strategy, independently find and fix the most valuable problem they
can see. A tally finds what they converge on. One integrator builds the top
consensus features as a single coherent change. The orchestrator verifies it
independently and, only then, moves the integration branch forward. Then the
next generation starts from the improved version, until the owner says stop.
Everything stays local unless the owner explicitly asks for more.

In the commands below, `K` stands for the kit:

```sh
K="python3 /path/to/starter/reference/improver.py --config /path/to/improver.config.json"
```

Every kit command that changes anything prints its plan first and changes
nothing without `--apply`. Read the plan, then apply it.

## 1. Roles

| Role | Who | Responsibility |
|---|---|---|
| Owner | The person whose software it is | Sets scope, focus and protected paths; reviews; makes requests; says stop |
| Orchestrator | One AI host session left running | Runs the loop, launches agents, tallies, verifies, records |
| Strategists | N parallel sub-agents per generation (default 8) | Each applies one never-reused strategy lens, fixes one problem, reports |
| Integrator | One sub-agent per generation | Builds the consensus features as one coherent change |
| Verifier | The orchestrator itself | Re-runs every check and audits protected paths; trusts no claim |
| Implementers | Dedicated sub-agents | Deliver the owner's direct requests, outside the vote |
| Kit | `reference/improver.py` | Prepares briefs and worktrees, records results; never calls an AI |

## 2. Setup, once per project

1. **Intake with the owner.** Agree what the software is for and who uses it,
   what "better" means, an optional focus, which paths hold the owner's live
   data and configuration (protected paths), which live software and ports
   must never be touched, how to stop, and that everything stays local.
2. **Configure the kit.** Copy `data/improver.config.example.json`, check it
   against `data/improver.config.schema.json`, and fill in the project path,
   base branch, integration branch, verify commands, harness, protected
   paths, live ports and state directory. Name every suite the project has:
   typecheck or lint, unit, contract, integration or end-to-end, and build.
   Keep the state directory outside the project. Run `$K init`, read the plan,
   then `$K init --apply`. This creates the integration branch from the base
   branch; the owner's base branch is never changed.
3. **Make the tests hermetic** before anything else (rule R1). Prove it: mark
   an audit (`$K audit setup --mark --apply`), run the suite, and check the
   audit (`$K audit setup`) with the real data directory in the protected
   paths.
4. **Build or confirm the isolated harness** if the software has a user
   interface or live services (rule R2). Put its command in the config.
5. **Record the baseline.** `$K baseline --apply` runs every verify command on
   the integration head with a throwaway home and cleared app environment,
   and records the results. That is the bar every change must hold. If a
   command already fails, it is listed as failing at the base, and briefs say
   so; do not start a generation on a red baseline you have not understood.

## 3. One generation, step by step

**Step 0: baseline.** The latest baseline must be recorded at the current
integration head. `render` warns when it is not. Record a fresh one with
`$K baseline --apply` whenever the head moves.

**Step 1: choose N strategies.** `$K plan G --apply`. The kit picks N lenses
from `data/strategy-pool.json` that differ from each other and from every
lens used in any earlier generation (rule R10), fit the project's surfaces,
and prefer the owner's focus tags. The choice is seeded and reproducible:
the same config and pool always give the same plan. Each lens is a distinct
method of finding the most valuable problem, not a topic. When the owner sets
a focus, such as "make it drivable by an automated agent", every lens attacks
that focus from its own angle. When fewer than N unused lenses remain, the
strategy-library team adds new ones; the kit refuses to reuse.

**Step 2: briefs and worktrees.** `$K render G --apply` fills
`templates/strategist-brief.md` for each strategist with the mission and
focus, the lens, the product context, the history of what earlier generations
integrated (build on it, do not redo it), the baseline, the environment and
harness, the hard safety rules, the required phases and the fixed report
format. `$K worktrees G --apply` creates one git worktree and branch per
strategist from the integration head, never the shared checkout, plus a
scratch directory. It refuses reserved slugs and existing paths (rule R4).
Then mark the audit before anyone starts: `$K audit gG --mark --apply`.

**Step 3: launch.** Start all N strategists in parallel as background
sub-agents. Give each one the full text of its brief file and nothing else;
strategists must not read each other's worktrees, branches or reports
(rule R11). Each works through the required phases: DISCOVER with hard
evidence, DECIDE the single most impactful problem, IMPLEMENT a complete,
production-quality fix, VERIFY every suite, COMMIT locally with narrative
messages and a clean worktree, and REPORT in the fixed format of
`templates/report.md`: Verdict, Evidence, Why this target, Solution,
Verification, Commits, Risks, a ranked Top 3 features list, and a Candidate
ledger table (key | problem | proposed solution | impact 1-5 | confidence 1-5
| implemented). Keys are kebab-case `area:problem` strings so votes can be
counted. Wait for all N reports. `$K status` shows who has reported, who is
still writing, and who is dead (rule R5).

**Step 4: tally.** `$K tally G --apply` parses every report's Top 3 and
Candidate ledger and drafts `gG/TALLY.md`, `gG/tally.json` and
`gG/integrator-brief.md`. Then the orchestrator does the part only judgment
can do: cluster findings by what the solution REQUIRES, not by symptom
wording (rule R12). Where two keys need the same change, map one onto the
other in `gG/aliases.json` and re-run the tally. The rules, with a worked
example, are in `docs/consensus.md`: a majority is at least ceil((N+1)/2)
distinct strategists (5 of 8); continuous mode takes the top 3 clusters by
distinct support, then mean impact x confidence; when nothing reaches a
majority, the broadest coherent cluster is taken as majority-like and the
tally says so explicitly. Findings that were not selected go into the
recurring-problems table, carried across generations, so problems found
again and again surface later. Every minority branch is kept (rule R14).

**Step 5: integrate.** Review `gG/integrator-brief.md`: it carries the
consensus features, the exact source commits (checked against the strategist
branches by the kit), a reconciliation section you must complete (how the
pieces fit where they meet), the verification bar, and the minority work that
is explicitly excluded. Create the integrator's worktree with
`$K worktrees G --integrator --apply` and launch the integrator with the full
brief. It builds one coherent change on its own branch from the integration
head and reports to `gG/INTEGRATION.md`.

**Step 6: verify independently.** Never trust the integrator's claims
(rule R13). Re-run every suite at the integrator's final commit:
`$K baseline --at <integrator worktree> --label gG-verify --apply`. Run the
harness end-to-end suite if there is one. Audit the protected paths:
`$K audit gG` must say CLEAN. A load-sensitive failure is rerun once and
counts only if it reproduces (rule R6). Only then fast-forward the
integration branch, locally:

```sh
git -C <project> fetch . <prefix>/gG-integration:<integration-branch>
```

That form updates a local branch and refuses anything but a fast-forward. If
the integration branch is checked out somewhere, run
`git merge --ff-only <prefix>/gG-integration` in that checkout instead.

**Step 7: record.** `$K record G --commit <sha> --summary "..." --apply`. The
kit refuses unless the commit is on the integration branch, the `gG-verify`
baseline passed at exactly that commit, and the audit is clean. It appends the
generation to `history.md` (the next briefs quote it), snapshots the tally,
the verification and the integration report as read-only receipts in
`gG/receipts/` (rule R3), and re-renders the living review,
`review/REVIEW.md`, which is the owner's entry point. An append-only journal
kept by the host is optional.

**Step 8: next generation.** Check `$K status`. If STOP is requested, start
nothing new. Otherwise plan generation G+1 from the new head, with the history
extended, and continue.

## 4. Owner requests, outside the vote

When the owner asks for something directly in the middle of a run, a
dedicated implementer delivers it; it does not wait for a generation or a
vote.

1. Mark an audit first: `$K audit request-<name> --mark --apply`.
2. Create a worktree from the current integration head:
   `git -C <project> worktree add -b <prefix>/request-<name> <state>/worktrees/request-<name> <integration-branch>`.
3. Brief the implementer with the request in the owner's words, the product
   context, the history, the baseline, the verify commands and the same hard
   safety rules as a strategist.
4. Verify it exactly like an integration:
   `$K baseline --at <that worktree> --label request-<name>-verify --apply`,
   the harness if any, and `$K audit request-<name>`.
5. If a newer integration head exists by then, rebase or cherry-pick the work
   onto it and resolve conflicts deliberately. Never overwrite integrated
   work, and verify again at the new commit.
6. Fast-forward the integration branch as in step 6, then
   `$K request <name> --commit <sha> --summary "..." --verify-label request-<name>-verify --apply`.
   The request is noted in the history, so the next generation builds on it.
7. If the owner is testing a live build, update and restart that build only
   for the owner's own requests and with consent. Tell the owner what changed
   and exactly how to switch back (the review lists the commands).

## 5. Leaving it running, stopping, resuming

The orchestrator's loop, in plain words:

```text
loop:
  status                      # STOP requested? dead agents? what is next?
  if STOP: update the review and start nothing new; wait for resume
  if no fresh baseline at the head: baseline --apply
  plan G, render G, worktrees G, audit gG --mark
  launch N strategists in the background; wait for all N reports
  tally G; cluster by required solution; finalize TALLY.md
  worktrees G --integrator; complete the reconciliation; launch the integrator
  verify at the integrator's commit; audit gG; fast-forward only if both pass
  record G
  G = G + 1
```

- **Stop.** The owner says stop, or runs `$K stop --reason "..." --apply`, or
  creates the file `STOP` in the state directory. The orchestrator checks
  before every step, starts nothing new, never integrates unverified work, and
  leaves running agents' work on their branches. Nothing is lost. While STOP
  exists, the kit refuses `plan --apply` and `worktrees --apply`, so no new
  strategist or integrator can be set up by mistake; recording work that is
  already verified still works.
- **Resume.** `$K resume --apply` removes STOP. If the latest generation was
  interrupted, it also archives that generation (rule R5): the generation
  directory becomes `gG-interrupted-K`, worktrees are moved aside and branches
  renamed with the same suffix. Then plan, render and create worktrees for G
  again from the current head; the kit picks the same strategies.
- **Be a good neighbor.** Verify commands run at lower CPU priority (`nice`
  in the config) so the owner's software stays responsive. Bound every long
  command with a timeout. Stop only processes you started.
- **Budget.** A generation of eight strategists commonly takes a few hours of
  agent time. Give strategists a time budget in their brief; a finished,
  verified improvement beats a big unfinished one.

## 6. The rules

These rules come from running this loop for real. Each one exists because
something went wrong without it.

**R1. Tests never touch the owner's real home or data.** Run unit suites with
a throwaway HOME and the application's environment configuration cleared,
through a preload that every test script imports first, so the whole test
process is isolated, not each test. Timers, retries and held requests can
outlive a test's own environment restore; in one real run, such a leftover
wrote a record into a real user data directory minutes after its test had
finished. The kit adds a second layer: every verify command gets a throwaway
home (HOME, USERPROFILE, XDG and temp directories) and the configured
environment prefixes are cleared. `home_writes` in a baseline lists what a
command wrote there. Toolchain caches are harmless, because the throwaway home
is deleted afterwards; application data there means the tests would have
written into the real home.

**R2. Anything with a user interface or live services runs only through an
isolated harness.** The harness gives every run a throwaway profile, a
scriptable fake backend, and dead or fake ports for real services. It
installs a side-effect firewall before the software loads: no OS permission
prompts, no browser or file-manager windows, no installers, and child
processes only from an allowlist, with every refusal recorded. Machine-wide
slots bound how many instances run at once, and each run writes one
`result.json`. `docs/safety.md` describes the pattern.

**R3. A living document is never a receipt.** The review is edited after
every generation; if it were referenced as a receipt, later edits would break
the receipt's verification. Receipts are separate read-only snapshots
(`gG/receipts/`, with SHA-256 digests), made by `record`.

**R4. A strategy slug never collides with a reserved directory name.** Once, a
strategy named like one of the generation's own directories (such as
`prompts`) made one strategist's worktree receive every brief. The kit refuses
reserved slugs in the pool, in plans and in `worktrees`, and keeps worktrees
in their own tree.

**R5. A restart of the orchestrator's host session kills its background
sub-agents.** Detect it: no report and no recent writes in the worktree and
scratch directory for `stale_minutes`. `status` flags such agents as dead.
Re-run the whole generation from the current head (`resume --apply`, then
plan, render, worktrees). Never count interrupted work.

**R6. Load-sensitive flakes are rerun once.** A failure is a regression only
if it reproduces. Record both runs.

**R7. Worktrees share state.** Never use `git stash`: stashes are shared by
every worktree of a repository, so one agent's stash can land in another's
work. If agents share a task list, prefix every id with the agent's slug.

**R8. The owner's live software is off limits.** Never drive, restart or kill
it, except to deploy the owner's own requests with consent. Lower the loop's
CPU priority so it stays responsive.

**R9. Local-only by default.** No push, publish or release unless the owner
explicitly asks. The kit has no command that pushes, fetches from a remote,
or deletes branches.

**R10. Strategies are never reused.** All N differ from each other and from
every earlier generation, so each generation looks with fresh eyes.

**R11. Strategists work independently.** Convergence counts only when nobody
copied.

**R12. Consensus is about the required solution.** Cluster by what each
solution requires, not by how a symptom is worded; say "majority-like"
whenever a pick falls below the majority threshold.

**R13. Verify independently before moving the integration branch.** Re-run
every suite, audit the protected paths since the generation began, and only
then fast-forward. `record` enforces this order.

**R14. Keep every minority branch.** Minority work was verified by its
strategist; the owner may want it later. The kit never deletes a branch.

## 7. What the kit does, and what the host does

The kit prepares and records. It validates the config, records baselines,
plans strategies, renders briefs, creates worktrees, audits protected paths,
drafts tallies and integrator briefs, gates and records generations and owner
requests, renders the living review, and reports status. It is Python 3.10+
standard library only, offline and deterministic, and it never calls an AI.

The AI host does everything that needs judgment or agents: it launches the
strategists, the integrator and the implementers, clusters findings by
required solution, completes the reconciliation, runs the harness,
fast-forwards the integration branch after verification, and talks with the
owner.
