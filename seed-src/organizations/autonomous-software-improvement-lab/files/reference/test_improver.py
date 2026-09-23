"""Tests for improver.py: every subcommand, in temporary directories.

Run from this directory:  python3 -B -m unittest -v test_improver
Worktree, tally, record and resume tests use a real temporary git repository.

The SAMPLE reports below are illustrative fixtures for exercising the tally.
They are not results of any real strategist. To see a tally without running
any AI, write them into a planned generation:

    python3 -B test_improver.py write-samples --config improver.config.json --gen 1
"""

from __future__ import annotations

import io
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import time
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import improver  # noqa: E402

SAMPLE_NOTE = "SAMPLE FIXTURE, not a real strategist result."
K_STORE = "storage:non-atomic-save"
K_LOST = "storage:lost-update"
K_ERR = "errors:catch-all-hides-cause"
K_REMOVE = "cli:remove-silent-noop"
K_DUP = "import:duplicate-default-contradiction"
K_SLOW = "import:quadratic-save"
K_HOME = "tests:write-real-home"
K_JSON = "cli:json-output"
ROWS = {
    K_STORE: ("save truncates the file in place and writers race",
              "temp file, fsync, atomic replace, lock and re-read"),
    K_LOST: ("two writers load, change and save; the second one wins",
             "serialize writers with a lock file and re-read under it"),
    K_ERR: ("every failure prints the same message without its cause",
            "print the cause and the next step; exit non-zero"),
    K_REMOVE: ("remove with an unknown id says removed and exits 0",
               "fail clearly with a non-zero exit for unknown ids"),
    K_DUP: ("add refuses duplicates but import accepts them",
            "one duplicate policy shared by add and import"),
    K_SLOW: ("import rewrites the whole file after every row", "validate every row, save once"),
    K_HOME: ("command-line tests write into the real home", "a preload giving a throwaway home"),
    K_JSON: ("list output is not machine-readable", "add --json to list and export"),
}


def rows(*specs: tuple[str, int, int, str]) -> list[tuple[str, str, str, int, int, str]]:
    return [(key, *ROWS[key], impact, confidence, done) for key, impact, confidence, done in specs]


SAMPLES = [
    {"verdict": "Saves are not atomic.", "top3": [K_STORE, K_SLOW, K_ERR],
     "ledger": rows((K_STORE, 5, 5, "yes"), (K_SLOW, 3, 4, "no"), (K_ERR, 4, 4, "no"),
                    (K_HOME, 3, 5, "no")),
     "commits": "- 1a2b3c4 Make saves atomic (sample sha, not a real commit)"},
    {"verdict": "remove reports success for unknown ids.", "top3": [K_REMOVE, K_ERR, K_STORE],
     "ledger": rows((K_REMOVE, 4, 5, "yes"), (K_ERR, 4, 4, "no"), (K_STORE, 5, 4, "no"))},
    {"verdict": "Concurrent adds lose links.", "top3": [K_STORE, K_DUP, K_JSON],
     "ledger": rows((K_STORE, 5, 4, "yes"), (K_DUP, 3, 4, "no"), (K_JSON, 2, 3, "no"))},
    {"verdict": "Errors hide their cause.", "top3": [K_ERR, K_REMOVE, K_HOME],
     "ledger": rows((K_ERR, 4, 5, "yes"), (K_REMOVE, 4, 4, "no"), (K_HOME, 3, 4, "no"))},
    {"verdict": "Two writers lose data.", "top3": [K_LOST, K_ERR, K_REMOVE],
     "ledger": rows((K_LOST, 5, 5, "yes"), (K_ERR, 3, 3, "no"), (K_REMOVE, 3, 4, "no"))},
    {"verdict": "Large imports are slow.", "top3": [K_SLOW, K_STORE, K_JSON],
     "ledger": rows((K_SLOW, 3, 5, "yes"), (K_STORE, 4, 4, "no"), (K_JSON, 2, 3, "no"))},
    {"verdict": "Automation cannot read the output.", "top3": [K_JSON, K_REMOVE, K_ERR],
     "ledger": rows((K_JSON, 3, 4, "yes"), (K_REMOVE, 4, 4, "no"), (K_ERR, 4, 3, "no"))},
    {"verdict": "Tests touch the real home.", "top3": [K_HOME, K_STORE, K_DUP],
     "ledger": rows((K_HOME, 4, 5, "yes"), (K_STORE, 4, 4, "no"), (K_DUP, 3, 3, "no"))},
]


def sample_report(gen: int, slug: str, sample: dict) -> str:
    lines = [f"# G{gen} - sample - {slug}", "", "## Verdict", f"{SAMPLE_NOTE} {sample['verdict']}",
             "", "## Evidence", "Illustrative only.", "", "## Why this target",
             "Illustrative only.", "", "## Solution", "Illustrative only.", "",
             "## Verification", "Illustrative only.", "", "## Commits",
             sample.get("commits", "No commits (sample fixture)."), "", "## Risks", "None.", "",
             "## Top 3 features"]
    lines += [f"{i}. `{key}` - {ROWS[key][1]} - illustrative"
              for i, key in enumerate(sample["top3"], 1)]
    lines += ["", "## Candidate ledger", "",
              "| key | problem | proposed solution | impact 1-5 | confidence 1-5 | implemented |",
              "|---|---|---|---|---|---|"]
    lines += [f"| {k} | {p} | {s} | {i} | {c} | {d} |" for k, p, s, i, c, d in sample["ledger"]]
    return "\n".join(lines) + "\n"


def write_samples(plan: dict, only: range | None = None) -> list[Path]:
    written = []
    for index, item in enumerate(plan["strategists"]):
        if only is not None and index not in only:
            continue
        path = Path(item["report"])
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(sample_report(plan["generation"], item["slug"],
                                      SAMPLES[index % len(SAMPLES)]), encoding="utf-8")
        written.append(path)
    return written


def run_git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), "-c", "user.name=Kit Test",
         "-c", "user.email=kit-test@example.invalid", "-c", "commit.gpgsign=false", *args],
        check=True, capture_output=True, text=True)
    return result.stdout.strip()


class Workspace:
    """A temporary layout: a git project, a protected directory, a config, a state dir."""

    def __init__(self, root: Path, **overrides: object) -> None:
        self.root = root
        self.project = root / "project"
        self.project.mkdir()
        (self.project / "app.py").write_text("print('app')\n", encoding="utf-8")
        run_git(self.project, "init", "-q")
        run_git(self.project, "symbolic-ref", "HEAD", "refs/heads/main")
        run_git(self.project, "add", "app.py")
        run_git(self.project, "commit", "-q", "-m", "initial")
        self.protected = root / "live-data"
        self.protected.mkdir()
        (self.protected / "settings.json").write_text("{}\n", encoding="utf-8")
        self.state = root / "state"
        self.config_data: dict = {
            "schema": "improver-config/1",
            "project": {"name": "Test Project", "path": "project",
                        "context": "A tiny project used by the kit's tests.",
                        "surfaces": ["cli", "library"], "base_branch": "main",
                        "integration_branch": "improve/integration"},
            "state_dir": "state",
            "strategists": 8,
            "seed": "test-seed",
            "verify": [{"name": "unit", "run": [sys.executable, "-c", "print('ok')"],
                        "timeout_seconds": 120}],
            "protected_paths": ["live-data"],
            "clear_env_prefixes": ["KITTEST_"],
            "stale_minutes": 30,
            "nice": 0,
        }
        self.config_data.update(overrides)
        self.config = root / "improver.config.json"
        self.save()

    def save(self) -> None:
        self.config.write_text(json.dumps(self.config_data, indent=2), encoding="utf-8")

    def kit(self, *args: str) -> tuple[int, str, str]:
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = improver.main(["--config", str(self.config), *args])
        return code, out.getvalue(), err.getvalue()

    def ok(self, *args: str) -> str:
        code, out, err = self.kit(*args)
        if code != 0:
            raise AssertionError(f"{args} exited {code}\n{out}\n{err}")
        return out

    def cfg(self) -> improver.Config:
        return improver.Config(self.config)

    def plan(self, gen: int) -> dict:
        return json.loads((self.state / f"g{gen}" / "plan.json").read_text(encoding="utf-8"))

    def ready(self, gen: int = 1) -> dict:
        """init, baseline, plan, render, worktrees and marker for one generation."""
        if not (self.state / "improver-state.json").exists():
            self.ok("init", "--apply")
            self.ok("baseline", "--apply")
        self.ok("plan", str(gen), "--apply")
        self.ok("render", str(gen), "--apply")
        self.ok("worktrees", str(gen), "--apply")
        self.ok("audit", f"g{gen}", "--mark", "--apply")
        return self.plan(gen)


@unittest.skipUnless(shutil.which("git"), "git is required")
class KitTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="improver-test-")
        self.root = Path(self.temporary.name).resolve()
        self.ws = Workspace(self.root)

    def tearDown(self) -> None:
        for path in self.root.rglob("*"):
            if path.is_file() and not path.is_symlink():
                path.chmod(stat.S_IWRITE | stat.S_IREAD)
        self.temporary.cleanup()


class ConfigAndInitTests(KitTestCase):
    def test_valid_config_resolves_paths(self) -> None:
        cfg = self.ws.cfg()
        self.assertEqual(cfg.project, self.ws.project)
        self.assertEqual(cfg.state, self.ws.state)
        self.assertEqual(cfg.n, 8)
        self.assertEqual(improver.majority(8), 5)
        self.assertEqual([improver.majority(n) for n in (1, 2, 3, 7)], [1, 2, 2, 4])

    def test_invalid_configs_are_refused(self) -> None:
        mutations = {
            "state inside project": lambda c: c.update(state_dir="project/state"),
            "protected overlaps state": lambda c: c.update(protected_paths=["state/x"]),
            "unknown key": lambda c: c.update(extra=True),
            "bad strategist count": lambda c: c.update(strategists=0),
            "bad surface": lambda c: c["project"].update(surfaces=["desktop"]),
            "shell string": lambda c: c["verify"][0].update(run="make test"),
            "duplicate names": lambda c: c["verify"].append(dict(c["verify"][0])),
            "cwd escapes": lambda c: c["verify"][0].update(cwd="../elsewhere"),
            "same branches": lambda c: c["project"].update(integration_branch="main"),
        }
        original = json.loads(json.dumps(self.ws.config_data))
        for name, mutate in mutations.items():
            with self.subTest(name=name):
                self.ws.config_data = json.loads(json.dumps(original))
                mutate(self.ws.config_data)
                self.ws.save()
                with self.assertRaises(improver.KitError):
                    self.ws.cfg()

    def test_init_is_plan_first_then_applies_idempotently(self) -> None:
        out = self.ws.ok("init")
        self.assertIn("PLAN ONLY", out)
        self.assertFalse(self.ws.state.exists())
        self.assertIsNone(improver.commit_of(self.ws.project, "refs/heads/improve/integration"))
        self.ws.ok("init", "--apply")
        self.assertTrue((self.ws.state / "improver-state.json").is_file())
        main = improver.commit_of(self.ws.project, "refs/heads/main")
        integration = improver.commit_of(self.ws.project, "refs/heads/improve/integration")
        self.assertEqual(integration, main)
        self.ws.ok("init", "--apply")

    def test_commands_refuse_before_init(self) -> None:
        code, _, err = self.ws.kit("plan", "1", "--apply")
        self.assertEqual(code, 1)
        self.assertIn("not initialized", err)

    def test_git_guard_refuses_dangerous_commands(self) -> None:
        for args in (("push",), ("fetch",), ("stash",), ("branch", "-D", "main"),
                     ("worktree", "remove", "x"), ("reset", "--hard")):
            with self.subTest(args=args), self.assertRaises(improver.KitError):
                improver.git(self.ws.project, *args)


class BaselineTests(KitTestCase):
    def test_baseline_is_hermetic_and_records_failures(self) -> None:
        probe = ("import os, pathlib; "
                 "pathlib.Path(os.environ['HOME'], 'written-by-test.txt').write_text('x'); "
                 "print('secret visible:', 'KITTEST_TOKEN' in os.environ)")
        self.ws.config_data["verify"] = [
            {"name": "writes-home", "run": [sys.executable, "-B", "-c", probe]},
            {"name": "fails", "run": [sys.executable, "-B", "-c", "raise SystemExit(4)"]},
        ]
        self.ws.save()
        self.ws.ok("init", "--apply")
        self.assertIn("PLAN ONLY", self.ws.ok("baseline"))
        self.assertFalse((self.ws.state / "baseline" / "latest.json").exists())
        real_home = Path.home()
        os.environ["KITTEST_TOKEN"] = "must-not-leak"
        try:
            code, out, _ = self.ws.kit("baseline", "--apply")
        finally:
            del os.environ["KITTEST_TOKEN"]
        self.assertEqual(code, 3)
        record = json.loads((self.ws.state / "baseline" / "latest.json").read_text())
        first, second = record["results"]
        self.assertTrue(first["passed"])
        self.assertIn("written-by-test.txt", first["home_writes"])
        self.assertIn("secret visible: False", "\n".join(first["tail"]))
        self.assertFalse((real_home / "written-by-test.txt").exists())
        self.assertEqual((second["passed"], second["exit_code"]), (False, 4))
        self.assertFalse(record["passed"])
        self.assertFalse(list((self.ws.state / "homes").iterdir()))
        self.assertIn("FAIL fails", out)

    def test_baseline_timeout_and_at_other_checkout(self) -> None:
        self.ws.config_data["verify"] = [
            {"name": "slow", "run": [sys.executable, "-c", "import time; time.sleep(30)"],
             "timeout_seconds": 1}]
        self.ws.save()
        self.ws.ok("init", "--apply")
        code, _, _ = self.ws.kit("baseline", "--label", "timeout-check", "--apply")
        self.assertEqual(code, 3)
        result = json.loads((self.ws.state / "baseline" / "timeout-check.json").read_text())
        self.assertTrue(result["results"][0]["timed_out"])
        code, _, err = self.ws.kit("baseline", "--at", str(self.root), "--apply")
        self.assertEqual(code, 1)
        self.assertIn("refused", err)


class PlanRenderWorktreeTests(KitTestCase):
    def test_plan_is_seeded_reproducible_and_never_reuses(self) -> None:
        self.ws.ok("init", "--apply")
        first = self.ws.ok("plan", "1")
        self.assertEqual(first, self.ws.ok("plan", "1"))
        self.ws.ok("plan", "1", "--apply")
        one = {s["slug"] for s in self.ws.plan(1)["strategists"]}
        self.assertEqual(len(one), 8)
        self.ws.ok("plan", "2", "--apply")
        two = {s["slug"] for s in self.ws.plan(2)["strategists"]}
        self.assertEqual(len(two), 8)
        self.assertFalse(one & two, "a strategy was reused")
        self.assertIn("already planned", self.ws.ok("plan", "1"))
        pool = improver.load_pool(self.ws.cfg())
        needs = {item["slug"]: item["needs"] for item in pool}
        for slug in one | two:
            self.assertTrue("any" in needs[slug] or {"cli", "library"} & set(needs[slug]))

    def test_focus_tags_are_preferred_and_exhaustion_is_refused(self) -> None:
        self.ws.config_data["focus"] = {"text": "Make it drivable by an agent.",
                                        "prefer_tags": ["automation"]}
        self.ws.save()
        self.ws.ok("init", "--apply")
        self.ws.ok("plan", "1", "--apply")
        tags = {item["slug"]: item["tags"] for item in improver.load_pool(self.ws.cfg())}
        picked = [s["slug"] for s in self.ws.plan(1)["strategists"]]
        self.assertTrue(all("automation" in tags[slug] for slug in picked))
        self.ws.config_data["strategists"] = 16
        self.ws.save()
        for gen in range(2, 5):
            code, _, err = self.ws.kit("plan", str(gen), "--apply")
            if code:
                break
        self.assertEqual(code, 1)
        self.assertIn("never reused", err)

    def test_render_fills_every_placeholder(self) -> None:
        self.ws.ok("init", "--apply")
        self.ws.ok("plan", "1", "--apply")
        code, _, err = self.ws.kit("render", "1", "--apply")
        self.assertEqual(code, 1)
        self.assertIn("no baseline", err)
        self.ws.ok("baseline", "--apply")
        self.assertIn("PLAN ONLY", self.ws.ok("render", "1"))
        self.ws.ok("render", "1", "--apply")
        for item in self.ws.plan(1)["strategists"]:
            brief = Path(item["brief"]).read_text(encoding="utf-8")
            self.assertIsNone(improver.PLACEHOLDER.search(brief), item["slug"])
            for expected in (item["lens"], item["worktree"], item["branch"], item["report"],
                             "## Candidate ledger", "first generation", "1 of 1 verify"):
                self.assertIn(expected, brief)

    def test_worktrees_refuse_reserved_slugs_and_existing_paths(self) -> None:
        plan = self.ws.ready()
        base = plan["base"]
        for item in plan["strategists"]:
            self.assertTrue(Path(item["worktree"]).is_dir())
            self.assertEqual(improver.commit_of(Path(item["worktree"]), "HEAD"), base)
            self.assertTrue(Path(item["scratch"]).is_dir())
        code, _, err = self.ws.kit("worktrees", "1", "--apply")
        self.assertEqual(code, 1)
        self.assertIn("existing path", err)
        path = self.ws.state / "g2" / "plan.json"
        self.ws.ok("plan", "2", "--apply")
        data = json.loads(path.read_text())
        data["strategists"][0]["slug"] = "prompts"
        path.write_text(json.dumps(data))
        code, _, err = self.ws.kit("worktrees", "2", "--apply")
        self.assertEqual(code, 1)
        self.assertIn("reserved", err)

    def test_pool_refuses_reserved_slug(self) -> None:
        pool = json.loads((improver.PACKAGE_DIR / "data" / "strategy-pool.json").read_text())
        pool["strategies"][0]["slug"] = "reports"
        custom = self.root / "pool.json"
        custom.write_text(json.dumps(pool), encoding="utf-8")
        self.ws.config_data["strategy_pool"] = str(custom)
        self.ws.save()
        with self.assertRaises(improver.KitError):
            improver.load_pool(self.ws.cfg())


class AuditTests(KitTestCase):
    def test_audit_detects_created_modified_and_deleted(self) -> None:
        self.ws.ok("init", "--apply")
        self.assertIn("PLAN ONLY", self.ws.ok("audit", "g1", "--mark"))
        code, _, err = self.ws.kit("audit", "g1")
        self.assertEqual(code, 1)
        self.assertIn("no audit marker", err)
        self.ws.ok("audit", "g1", "--mark", "--apply")
        self.assertIn("CLEAN", self.ws.ok("audit", "g1"))
        (self.ws.protected / "new.txt").write_text("x", encoding="utf-8")
        settings = self.ws.protected / "settings.json"
        settings.write_text('{"changed": true}\n', encoding="utf-8")
        future = time.time() + 5
        os.utime(settings, (future, future))
        code, out, _ = self.ws.kit("audit", "g1", "--json")
        self.assertEqual(code, 3)
        findings = json.loads(out)["findings"]
        self.assertTrue(any(f.startswith("created") and f.endswith("new.txt") for f in findings))
        self.assertTrue(any(f.startswith("modified") for f in findings))
        (self.ws.protected / "new.txt").unlink()
        settings.unlink()
        code, out, _ = self.ws.kit("audit", "g1", "--json")
        self.assertTrue(any(f.startswith("deleted") for f in json.loads(out)["findings"]))


class TallyTests(KitTestCase):
    def tally(self, gen: int = 1) -> dict:
        return json.loads((self.ws.state / f"g{gen}" / "tally.json").read_text(encoding="utf-8"))

    def test_parse_report_accepts_variants_and_flags_problems(self) -> None:
        body = "\n".join([
            "## Verdict", "Something.", "## Commits", "- abc1234 fix; 2026 is not a sha",
            "## Top three features",
            "1. **`data:atomic-save`** - write safely", "2. errors:show-cause - say why",
            "3. no key on this line",
            "## Candidate ledger", "| key | problem | solution | impact | confidence | done |",
            "| --- | --- | --- | --- | --- | --- |",
            "| `data:atomic-save` | loses data | atomic | 4/5 | 5 | Yes |",
            "| Bad Key | x | y | 3 | 3 | no |", "| data:short | too few |"])
        parsed = improver.parse_report(body)
        self.assertEqual([k for k, _ in parsed["top3"]], ["data:atomic-save", "errors:show-cause"])
        self.assertEqual(parsed["ledger"][0]["impact"], 4)
        self.assertEqual(parsed["ledger"][0]["implemented"], "yes")
        self.assertEqual(parsed["commits"], ["abc1234"])
        self.assertEqual(len(parsed["problems"]), 3)

    def test_tally_majority_top3_evidence_and_aliases(self) -> None:
        plan = self.ws.ready()
        code, _, err = self.ws.kit("tally", "1", "--apply")
        self.assertEqual(code, 1)
        self.assertIn("missing", err)
        write_samples(plan)
        self.assertIn("PLAN ONLY", self.ws.ok("tally", "1"))
        self.ws.ok("tally", "1", "--apply")
        result = self.tally()
        self.assertEqual(result["decision"], "majority")
        self.assertEqual(result["top3"], [K_STORE, K_ERR, K_REMOVE])
        clusters = {c["key"]: c for c in result["clusters"]}
        self.assertEqual((clusters[K_STORE]["support"], clusters[K_STORE]["majority"]), (5, True))
        self.assertEqual(clusters[K_STORE]["mean_impact_confidence"], "19.4")
        self.assertEqual((clusters[K_REMOVE]["support"], clusters[K_REMOVE]["majority"]),
                         (4, False))
        first = plan["strategists"][0]["slug"]
        self.assertEqual(result["evidence"][first]["claimed_commits"],
                         [{"sha": "1a2b3c4", "on_branch": False}])
        tally_md = (self.ws.state / "g1" / "TALLY.md").read_text(encoding="utf-8")
        self.assertIn("Majority:", tally_md)
        self.assertIn("majority-like", tally_md)
        self.assertIn(SAMPLE_NOTE, tally_md)
        brief = (self.ws.state / "g1" / "integrator-brief.md").read_text(encoding="utf-8")
        self.assertIsNone(improver.PLACEHOLDER.search(brief))
        self.assertIn("NOT on the branch", brief)
        self.assertIn(K_JSON, brief.split("## Explicitly excluded")[1])
        aliases = self.ws.state / "g1" / "aliases.json"
        aliases.write_text(json.dumps({K_LOST: K_STORE}), encoding="utf-8")
        self.ws.ok("tally", "1", "--apply")
        merged = {c["key"]: c for c in self.tally()["clusters"]}
        self.assertEqual(merged[K_STORE]["support"], 6)
        self.assertNotIn(K_LOST, merged)
        aliases.write_text(json.dumps({K_LOST: K_STORE, K_STORE: K_ERR}), encoding="utf-8")
        self.assertEqual(self.ws.kit("tally", "1")[0], 1)

    def test_tally_says_majority_like_when_nothing_reaches_majority(self) -> None:
        plan = self.ws.ready()
        write_samples(plan, only=range(3, 8))
        self.ws.ok("tally", "1", "--allow-missing", "--apply")
        result = self.tally()
        self.assertEqual(result["decision"], "majority-like")
        self.assertEqual(len(result["missing"]), 3)
        text = (self.ws.state / "g1" / "TALLY.md").read_text(encoding="utf-8")
        self.assertIn("No cluster reached a majority", text)
        self.assertIn("MAJORITY-LIKE", text)
        self.assertIn("Incomplete", text)

    def test_recurring_minority_is_carried_across_generations(self) -> None:
        write_samples(self.ws.ready(1))
        self.ws.ok("tally", "1", "--apply")
        run_git(self.ws.project, "branch", "-f", "improve/integration", "main")
        write_samples(self.ws.ready(2))
        self.ws.ok("tally", "2", "--apply")
        recurring = {r["key"]: r for r in self.tally(2)["recurring"]}
        self.assertEqual(recurring[K_HOME]["generations"], [1, 2])
        self.assertEqual(recurring[K_HOME]["support_total"], 6)
        text = (self.ws.state / "g2" / "TALLY.md").read_text(encoding="utf-8")
        self.assertIn("g1, g2", text)


class StatusStopResumeTests(KitTestCase):
    def status(self) -> dict:
        return json.loads(self.ws.ok("status", "--json"))

    def age(self, *roots: Path) -> None:
        old = time.time() - 3 * 3600
        for root in roots:
            for path in [root, *root.rglob("*")]:
                if path.name != ".git" or path.is_file():
                    os.utime(path, (old, old), follow_symlinks=False)

    def test_status_reports_next_actions(self) -> None:
        self.ws.ok("init", "--apply")
        self.assertIn("baseline", self.status()["next"])
        self.ws.ok("baseline", "--apply")
        self.assertIn("plan 1", self.status()["next"])
        plan = self.ws.ready()
        report = self.status()
        self.assertEqual(report["generations"][0]["working"], [s["slug"] for s in
                                                               plan["strategists"]])
        self.assertIn("Wait for reports", report["next"])
        write_samples(plan)
        self.assertIn("tally 1", self.status()["next"])

    def test_dead_strategists_are_detected_and_resume_archives_the_generation(self) -> None:
        plan = self.ws.ready()
        write_samples(plan, only=range(0, 2))
        for item in plan["strategists"][2:]:
            self.age(Path(item["worktree"]), Path(item["scratch"]))
        report = self.status()
        self.assertEqual(len(report["generations"][0]["dead"]), 6)
        self.assertIn("Interrupted", report["next"])
        self.assertIn("PLAN ONLY", self.ws.ok("resume"))
        self.ws.ok("resume", "--apply")
        self.assertFalse((self.ws.state / "g1").exists())
        archive = self.ws.state / "g1-interrupted-1"
        self.assertTrue((archive / "plan.json").is_file())
        first = plan["strategists"][0]
        self.assertTrue((archive / "reports" / f"{first['slug']}.md").is_file())
        self.assertIsNotNone(improver.commit_of(self.ws.project,
                                                f"refs/heads/{first['branch']}-interrupted-1"))
        self.assertTrue((self.ws.state / "worktrees" / "g1-interrupted-1" / first["slug"]).is_dir())
        self.ws.ok("plan", "1", "--apply")
        again = [s["slug"] for s in self.ws.plan(1)["strategists"]]
        self.assertEqual(again, [s["slug"] for s in plan["strategists"]])
        self.ws.ok("render", "1", "--apply")
        self.ws.ok("worktrees", "1", "--apply")
        self.assertEqual(self.status()["interrupted_archives"], ["g1-interrupted-1"])

    def test_stop_and_resume(self) -> None:
        self.ws.ok("init", "--apply")
        self.ws.ok("baseline", "--apply")
        self.ws.ok("plan", "1", "--apply")
        self.ws.ok("render", "1", "--apply")
        self.assertIn("PLAN ONLY", self.ws.ok("stop", "--reason", "owner is away"))
        self.assertFalse((self.ws.state / "STOP").exists())
        self.ws.ok("stop", "--reason", "owner is away", "--apply")
        report = self.status()
        self.assertTrue(report["stop_requested"])
        self.assertIn("Stopped", report["next"])
        self.assertIn("STOPPED", (self.ws.state / "review" / "REVIEW.md").read_text())
        for command in (("worktrees", "1", "--apply"), ("plan", "2", "--apply")):
            code, _, err = self.ws.kit(*command)
            self.assertEqual(code, 1, command)
            self.assertIn("STOP is requested (", err)
            self.assertIn("owner is away", err)
        self.assertFalse((self.ws.state / "g1" / "worktrees.json").exists())
        self.assertFalse((self.ws.state / "g2").exists())
        self.assertIn("PLAN ONLY", self.ws.ok("worktrees", "1"))
        self.ws.ok("resume", "--apply")
        self.assertFalse(self.status()["stop_requested"])
        self.ws.ok("worktrees", "1", "--apply")
        self.assertTrue((self.ws.state / "g1" / "worktrees.json").is_file())


class RecordTests(KitTestCase):
    def commit_in(self, worktree: Path, name: str) -> str:
        (worktree / name).write_text(f"{name}\n", encoding="utf-8")
        run_git(worktree, "add", name)
        run_git(worktree, "commit", "-q", "-m", f"add {name}")
        return run_git(worktree, "rev-parse", "HEAD")

    def test_record_requires_verification_audit_and_fast_forward(self) -> None:
        plan = self.ws.ready()
        write_samples(plan)
        self.ws.ok("tally", "1", "--apply")
        self.ws.ok("worktrees", "1", "--integrator", "--apply")
        integrator = self.ws.state / "worktrees" / "g1" / "integrator"
        sha = self.commit_in(integrator, "integrated.txt")
        code, _, err = self.ws.kit("record", "1", "--commit", sha, "--summary", "x", "--apply")
        self.assertEqual(code, 1)
        self.assertIn("not on improve/integration", err)
        run_git(self.ws.project, "fetch", "-q", ".",
                "improve/g1-integration:improve/integration")
        code, _, err = self.ws.kit("record", "1", "--commit", sha, "--summary", "x", "--apply")
        self.assertIn("no verification", err)
        self.ws.ok("baseline", "--at", str(integrator), "--label", "g1-verify", "--apply")
        (self.ws.protected / "leak.txt").write_text("x", encoding="utf-8")
        code, _, err = self.ws.kit("record", "1", "--commit", sha, "--summary", "x", "--apply")
        self.assertIn("protected paths changed", err)
        (self.ws.protected / "leak.txt").unlink()
        self.ws.ok("record", "1", "--commit", sha, "--summary", "Safe saves and honest errors.",
                   "--apply")
        history = (self.ws.state / "history.md").read_text(encoding="utf-8")
        self.assertIn("Safe saves and honest errors.", history)
        receipts = self.ws.state / "g1" / "receipts"
        tally_receipt = receipts / "TALLY.md"
        self.assertFalse(tally_receipt.stat().st_mode & stat.S_IWUSR)
        self.assertTrue((receipts / "receipts.json").is_file())
        review = (self.ws.state / "review" / "REVIEW.md").read_text(encoding="utf-8")
        self.assertIn("never a receipt", review)
        self.assertIn(sha[:12], review)
        self.assertIsNone(improver.PLACEHOLDER.search(review))
        code, _, err = self.ws.kit("record", "1", "--commit", sha, "--summary", "x", "--apply")
        self.assertIn("already recorded", err)
        self.ws.ok("render", "1")
        self.ws.ok("plan", "2", "--apply")
        self.ws.ok("baseline", "--apply")
        self.ws.ok("render", "2", "--apply")
        brief = Path(self.ws.plan(2)["strategists"][0]["brief"]).read_text(encoding="utf-8")
        self.assertIn("Safe saves and honest errors.", brief)
        self.assertIn("worktrees 2", json.loads(self.ws.ok("status", "--json"))["next"])

    def test_owner_request_is_recorded_outside_the_vote(self) -> None:
        self.ws.ok("init", "--apply")
        self.ws.ok("audit", "request-dark-mode", "--mark", "--apply")
        worktree = self.ws.state / "worktrees" / "request-dark-mode"
        run_git(self.ws.project, "worktree", "add", "-q", "-b", "improve/request-dark-mode",
                str(worktree), "improve/integration")
        sha = self.commit_in(worktree, "dark-mode.txt")
        self.ws.ok("baseline", "--at", str(worktree), "--label", "request-dark-mode-verify",
                   "--apply")
        run_git(self.ws.project, "fetch", "-q", ".",
                "improve/request-dark-mode:improve/integration")
        self.ws.ok("request", "dark-mode", "--commit", sha, "--summary", "Dark mode.",
                   "--verify-label", "request-dark-mode-verify", "--apply")
        history = (self.ws.state / "history.md").read_text(encoding="utf-8")
        self.assertIn("Owner request 'dark-mode'", history)
        self.assertIn("Dark mode.", (self.ws.state / "review" / "REVIEW.md").read_text())


def _write_samples_command(argv: list[str]) -> int:
    import argparse

    parser = argparse.ArgumentParser(prog="test_improver.py write-samples")
    parser.add_argument("--config", default="improver.config.json")
    parser.add_argument("--gen", type=int, required=True)
    args = parser.parse_args(argv)
    plan = improver.load_plan(improver.Config(Path(args.config)), args.gen)
    for path in write_samples(plan):
        print(f"wrote sample report {path}")
    print("These are illustrative fixtures, not strategist results. Remove them before a real run.")
    return 0


if __name__ == "__main__":
    if sys.argv[1:2] == ["write-samples"]:
        raise SystemExit(_write_samples_command(sys.argv[2:]))
    unittest.main()
