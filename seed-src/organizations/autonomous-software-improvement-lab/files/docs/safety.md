# Safety

The loop runs unattended on the owner's machine, next to the owner's live
software and data. These rules are hard limits for every agent in it: the
orchestrator, the strategists, the integrator and the implementers. Briefs
repeat them; the kit enforces the parts a program can enforce.

## Hard rules

1. **Write only where you were told to.** A strategist or integrator changes
   files only in its own worktree and scratch directory; the kit writes only in
   the state directory. Reading elsewhere is fine.
2. **Protected paths are never written.** They hold the owner's live data,
   profiles and configuration. They are listed in the config, snapshotted
   before a generation starts (`audit gG --mark`), and checked before anything
   is integrated (`audit gG`). `record` refuses when the audit is not clean.
3. **The owner's live software is off limits.** Never connect to it, drive it,
   restart it or kill it, and never touch its ports (`live_ports`). The only
   exception is deploying the owner's own request, with consent.
4. **Git stays local and non-destructive.** Commit on your own branch. Never
   push, pull, fetch from a remote, change remotes or git config, rewrite or
   delete branches or worktrees you do not own, or run gc or prune. Never use
   `git stash`; stashes are shared by every worktree of a repository.
5. **Tests are hermetic.** No test may write into the real home directory or
   real data, or depend on the developer's machine (see below).
6. **No side effects outside the machine or the task.** No installers, OS
   permission prompts, browser or file-manager windows, notifications,
   messages, network calls with side effects, publishing, releases, signing,
   spending or credential access.
7. **Be a good neighbor on a shared machine.** Bound every long command with a
   timeout, run at lower CPU priority, clean up every process you start, and
   stop only processes you started.
8. **Privacy.** When reading logs or data, never copy personal content into
   commits, tests, fixtures or reports. Describe patterns instead.
9. **Shared lists are prefixed.** If agents share a task list, every id starts
   with the agent's strategy slug.
10. **Honesty.** Report only what you actually ran and observed. A check that
    fails once under load is rerun once and counts only if it reproduces.

## Protected paths

List everything the owner would be upset to see changed: the live
application's data and profile directories, its configuration, caches it
trusts, the checkout the live build runs from, and any home-directory files
the software reads. Keep them outside the project and the state directory; the
kit refuses overlaps so its own writes can never trip the audit. The audit
compares sizes and modification times of every entry (created, modified,
deleted) against the marker; for very large trees it falls back to "newer
than the marker" and says so.

## Hermetic tests

The loop runs test suites dozens of times a day in many worktrees at once. A
single test that writes into the real home directory will eventually damage
real data. Make the whole test process hermetic, not each test:

- a preload module that every test entry point imports first sets HOME (and
  USERPROFILE on Windows) to a fresh temporary directory, points the
  application's data and configuration directories inside it, and removes the
  application's own environment variables;
- the throwaway home lives for the whole process, because background timers,
  retries and held requests can outlive a single test's cleanup;
- test scripts in the project's manifest load the preload, so nobody can
  forget it.

A minimal Python preload, for a project whose environment variables start
with `MYAPP_`:

```python
# hermetic_home.py: import this before the application in every test module.
import atexit
import os
import shutil
import tempfile

_home = tempfile.mkdtemp(prefix="tests-home-")
for _name in ("HOME", "USERPROFILE"):
    os.environ[_name] = _home
for _name in [n for n in os.environ if n.startswith("MYAPP_")]:
    del os.environ[_name]
atexit.register(shutil.rmtree, _home, ignore_errors=True)
```

The same idea works in any runtime that can load code before the tests
(a test-runner setup file, a `--require` or `--import` flag, a fixture that
runs once per session). The kit adds defense in depth: each verify command
runs with its own throwaway home and temp directory, with the configured
environment prefixes cleared, and the baseline lists anything written there.

## The isolated harness and its side-effect firewall

Software with a user interface or live services must never be run against
the owner's real profile, backend or devices. Build one harness command that
is the only allowed way to run it, and give it these parts:

| Part | What it does |
|---|---|
| Throwaway profile | Fresh data, configuration, cache and log directories per run, deleted afterwards |
| Fake backend | A scriptable local stand-in for every real service: configure its replies, inspect the calls it received |
| Dead or fake ports | Real services the software would reach point at closed ports or fakes, never at the owner's live instances |
| Side-effect firewall | Installed before the software loads: OS permission prompts answer "not granted", window-opening and shell-open calls are recorded instead of performed, installers are refused, and child processes start only from an explicit allowlist |
| Refusal log | Every refused action is recorded with what was attempted, so strategists can see it and never work around it |
| Machine-wide slots | A lock directory bounds how many instances run at once across all worktrees; later callers wait |
| One result per run | Each run writes a `result.json`: label, slot held, profile location, fake-backend calls, firewall refusals, checks passed and failed, artifacts such as screenshots and logs |

Modes that have proven useful: `smoke` (start, check status, capture a
screenshot and logs, stop), `e2e` (smoke plus an end-to-end test file), and
`serve` (keep an isolated instance up for a bounded time so an agent can drive
it through its automation surface). The harness is application-specific; the
pattern is not.

## Local-only by default

Nothing leaves the machine unless the owner explicitly asks: no push, pull
request, publish, release, upload or message. The kit contains no command
that pushes or talks to a remote. Integration happens on a local branch that
the owner can try, compare and discard with ordinary git commands, which the
review lists.

## What the kit enforces, and what the host must

The kit enforces: plan-first changes (`--apply`), writes only inside the state
directory, an allowlist of local git commands, no branch deletion, reserved
slug refusal, fresh worktrees from the integration head, throwaway homes and
cleared environment prefixes for verify commands, lower CPU priority and
timeouts, protected-path audits, STOP (no `plan` or `worktrees` is applied
while it exists), and the record gate (verified at the exact commit, audit
clean, already fast-forwarded).

The AI host must enforce everything else: that agents stay in their
worktrees, that the harness is used, that the live software and its ports are
left alone, and that nothing is pushed or published. Put these rules in every
brief; the templates already do.
