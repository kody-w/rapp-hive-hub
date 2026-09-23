#!/usr/bin/env python3
"""improver: offline bookkeeping for the Autonomous Software Improvement Lab.

The AI host (the orchestrator) spawns the strategists and the integrator. This
kit prepares their inputs and records their outputs: it validates the config,
records baselines, plans strategies, renders briefs, creates git worktrees,
audits protected paths, drafts tallies, records generations and reports status.
Python 3.10+ standard library only. Offline, deterministic, no AI calls.

Safety contract:
- every mutating subcommand prints its plan and changes nothing without --apply;
- files are written only inside the configured state directory; in the project
  repository the kit only adds, moves and renames local worktrees and branches;
- it never pushes, fetches, pulls, merges, rebases, stashes, deletes branches or
  runs a shell; verify commands run as argument lists with a timeout.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shlex
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from fractions import Fraction
from pathlib import Path
from typing import Any

KIT_VERSION = "1.0.0"
PACKAGE_DIR = Path(__file__).resolve().parent.parent
CONFIG_SCHEMA = "improver-config/1"
POOL_SCHEMA = "improver-strategy-pool/1"
SURFACES = ("any", "api", "cli", "data", "library", "service", "ui")
RESERVED = frozenset(
    {
        "archive", "baseline", "homes", "integrator", "markers", "prompts",
        "receipts", "reports", "requests", "review", "scratch", "worktrees",
    }
)
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
KEY = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*:[a-z0-9]+(?:-[a-z0-9]+)*$")
KEY_IN_TEXT = re.compile(r"(?<![\w/.-])[a-z][a-z0-9]*(?:-[a-z0-9]+)*:[a-z0-9]+(?:-[a-z0-9]+)*")
SHA_IN_TEXT = re.compile(r"\b[0-9a-f]{7,40}\b")
PLACEHOLDER = re.compile(r"\{([A-Z][A-Z0-9_]*)\}")
ENV_NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
BRANCH = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/-]*$")
GIT_ALLOWED = frozenset(
    {"branch", "log", "merge-base", "rev-parse", "show-ref", "status", "worktree"}
)
SKIP_DIRS = frozenset({".git", ".venv", "__pycache__", "node_modules"})
WALK_CAP = 50_000
HOME_VARS = ("HOME", "USERPROFILE")
HOME_SUBDIRS = {
    "XDG_CONFIG_HOME": ".config",
    "XDG_DATA_HOME": ".local/share",
    "XDG_CACHE_HOME": ".cache",
    "XDG_STATE_HOME": ".local/state",
    "APPDATA": "AppData/Roaming",
    "LOCALAPPDATA": "AppData/Local",
}
TEMP_VARS = ("TMPDIR", "TEMP", "TMP")
COMMON_KEYS = {
    "GEN", "N", "PROJECT_NAME", "PROJECT_CONTEXT", "SURFACES", "FOCUS", "HISTORY",
    "BASE_COMMIT", "INTEGRATION_BRANCH", "BASELINE", "VERIFY_COMMANDS", "HARNESS",
    "PROTECTED_PATHS", "LIVE_PORTS",
}
TEMPLATE_KEYS = {
    "strategist-brief.md": COMMON_KEYS | {
        "IDX", "STRATEGY_NAME", "STRATEGY_SLUG", "LENS", "FINDS", "RISK_NOTES",
        "WORKTREE", "BRANCH", "SCRATCH", "REPORT", "REPORT_TEMPLATE",
    },
    "report.md": {"GEN", "STRATEGY_NAME", "STRATEGY_SLUG", "BRANCH"},
    "integrator-brief.md": COMMON_KEYS | {
        "INTEGRATOR_BRANCH", "INTEGRATOR_WORKTREE", "SCRATCH", "REPORT", "DECISION",
        "CONSENSUS_FEATURES", "SOURCE_COMMITS", "RECONCILIATION", "EXCLUDED_MINORITY",
    },
    "review.md": {
        "PROJECT_NAME", "UPDATED_AT", "STATUS", "NEXT_ACTION", "INTEGRATION_BRANCH",
        "INTEGRATION_HEAD", "BASE_BRANCH", "START_COMMIT", "LATEST_BASELINE", "GENERATIONS",
        "HISTORY", "OWNER_REQUESTS", "RECURRING", "KEPT_BRANCHES", "RECEIPTS", "SWITCH_BACK",
        "STOP_HOW",
    },
}


class KitError(Exception):
    """A refusal with a message the operator can act on."""


def require(condition: object, message: str) -> None:
    if not condition:
        raise KitError(message)


def now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise KitError(f"missing file: {path}") from None
    except json.JSONDecodeError as exc:
        raise KitError(f"not valid JSON: {path}: {exc}") from None


def dump_json(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def within(child: Path, parent: Path) -> bool:
    return child == parent or parent in child.parents


def overlaps(first: Path, second: Path) -> bool:
    return within(first, second) or within(second, first)


def majority(count: int) -> int:
    """At least ceil((N+1)/2) strategists, e.g. 5 of 8."""
    return (count + 2) // 2


def bullet(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def closed(value: Any, required: set[str], optional: set[str], where: str) -> dict[str, Any]:
    require(isinstance(value, dict), f"{where}: expected an object")
    missing = sorted(required - value.keys())
    unknown = sorted(value.keys() - required - optional)
    require(not missing, f"{where}: missing {', '.join(missing)}")
    require(not unknown, f"{where}: unknown field(s) {', '.join(unknown)}")
    return value


def text(value: Any, where: str, maximum: int = 2000, empty: bool = False) -> str:
    require(
        isinstance(value, str) and (empty or value.strip()) and len(value) <= maximum,
        f"{where}: expected {'' if empty else 'non-empty '}text of at most {maximum} characters",
    )
    return str(value)


def integer(value: Any, where: str, low: int, high: int) -> int:
    require(
        isinstance(value, int) and not isinstance(value, bool) and low <= value <= high,
        f"{where}: expected an integer from {low} to {high}",
    )
    return int(value)


def labels(value: Any, where: str, maximum: int = 64) -> list[str]:
    require(isinstance(value, list) and len(value) <= maximum, f"{where}: expected a list")
    items = [text(item, where, 64) for item in value]
    require(all(SLUG.match(item) for item in items), f"{where}: use lowercase-hyphenated words")
    require(len(items) == len(set(items)), f"{where}: duplicate values")
    return items


def argv_list(value: Any, where: str) -> list[str]:
    require(
        isinstance(value, list) and 1 <= len(value) <= 64,
        f"{where}: expected an argument list such as [\"npm\", \"test\"] (no shell)",
    )
    return [text(item, where, 4000) for item in value]


def branch_name(value: Any, where: str) -> str:
    name = text(value, where, 200)
    require(
        BRANCH.match(name) and ".." not in name and "//" not in name
        and not name.endswith(("/", ".", ".lock")),
        f"{where}: not a valid local branch name: {name!r}",
    )
    return name


def resolve_path(base: Path, value: str) -> Path:
    path = Path(os.path.expanduser(value))
    return (path if path.is_absolute() else base / path).resolve()


def verify_command(value: Any, index: int) -> dict[str, Any]:
    where = f"verify[{index}]"
    optional = {"cwd", "timeout_seconds", "hermetic_home", "env"}
    entry = closed(value, {"name", "run"}, optional, where)
    cwd = text(entry.get("cwd", "."), f"{where}.cwd", 400)
    parts = Path(cwd).parts
    require(not Path(cwd).is_absolute() and ".." not in parts,
            f"{where}.cwd: stay inside the project")
    hermetic = entry.get("hermetic_home", True)
    require(isinstance(hermetic, bool), f"{where}.hermetic_home: expected true or false")
    env = entry.get("env", {})
    require(
        isinstance(env, dict)
        and all(ENV_NAME.match(k) and isinstance(v, str) for k, v in env.items()),
        f"{where}.env: expected an object of environment names to text values",
    )
    name = text(entry["name"], f"{where}.name", 64)
    require(SLUG.match(name), f"{where}.name: use lowercase-hyphenated words")
    return {
        "name": name,
        "run": argv_list(entry["run"], f"{where}.run"),
        "cwd": cwd,
        "timeout_seconds": integer(entry.get("timeout_seconds", 1800), where, 1, 86_400),
        "hermetic_home": hermetic,
        "env": dict(env),
    }


class Config:
    """The validated configuration, with absolute paths resolved from the config file."""

    TOP_REQUIRED = {"schema", "project", "state_dir", "strategists", "seed", "verify",
                    "protected_paths"}
    TOP_OPTIONAL = {"focus", "harness", "live_ports", "clear_env_prefixes", "stale_minutes",
                    "nice", "strategy_pool", "templates_dir"}

    def __init__(self, path: Path) -> None:
        raw = read_json(path)
        self.file = path.resolve()
        self.digest = sha256_bytes(json.dumps(raw, sort_keys=True).encode("utf-8"))
        base = self.file.parent
        top = closed(raw, self.TOP_REQUIRED, self.TOP_OPTIONAL, "config")
        require(top["schema"] == CONFIG_SCHEMA, f"config.schema must be {CONFIG_SCHEMA!r}")
        project = closed(
            top["project"],
            {"name", "path", "context", "surfaces", "base_branch", "integration_branch"},
            {"branch_prefix"},
            "config.project",
        )
        self.name = text(project["name"], "project.name", 120)
        self.context = text(project["context"], "project.context", 8000)
        self.project = resolve_path(base, text(project["path"], "project.path", 1000))
        self.surfaces = labels(project["surfaces"], "project.surfaces", 6)
        require(
            self.surfaces and set(self.surfaces) <= set(SURFACES) - {"any"},
            f"project.surfaces: choose from {', '.join(s for s in SURFACES if s != 'any')}",
        )
        self.base_branch = branch_name(project["base_branch"], "project.base_branch")
        self.integration_branch = branch_name(
            project["integration_branch"], "project.integration_branch"
        )
        self.prefix = branch_name(project.get("branch_prefix", "improve"), "project.branch_prefix")
        require(
            self.integration_branch != self.base_branch,
            "project.integration_branch must differ from project.base_branch",
        )
        self.state = resolve_path(base, text(top["state_dir"], "state_dir", 1000))
        self.n = integer(top["strategists"], "strategists", 1, 16)
        self.seed = text(top["seed"], "seed", 200)
        require(isinstance(top["verify"], list) and 1 <= len(top["verify"]) <= 32,
                "verify: expected 1-32 named commands")
        self.verify = [verify_command(item, i) for i, item in enumerate(top["verify"])]
        names = [item["name"] for item in self.verify]
        require(len(names) == len(set(names)), "verify: command names must be unique")
        require(isinstance(top["protected_paths"], list) and len(top["protected_paths"]) <= 64,
                "protected_paths: expected a list")
        self.protected = [
            resolve_path(base, text(item, "protected_paths", 1000))
            for item in top["protected_paths"]
        ]
        focus = closed(top.get("focus", {}), set(), {"text", "prefer_tags"}, "config.focus")
        self.focus_text = text(focus.get("text", ""), "focus.text", 4000, empty=True).strip()
        self.prefer_tags = labels(focus.get("prefer_tags", []), "focus.prefer_tags")
        self.harness: dict[str, Any] | None = None
        if top.get("harness") is not None:
            harness = closed(top["harness"], {"run", "description"}, set(), "config.harness")
            self.harness = {
                "run": argv_list(harness["run"], "harness.run"),
                "description": text(harness["description"], "harness.description", 8000),
            }
        ports = top.get("live_ports", [])
        require(isinstance(ports, list) and len(ports) <= 64, "live_ports: expected a list")
        self.live_ports = [integer(port, "live_ports", 1, 65_535) for port in ports]
        prefixes = top.get("clear_env_prefixes", [])
        require(
            isinstance(prefixes, list)
            and all(isinstance(p, str) and ENV_NAME.match(p) for p in prefixes),
            "clear_env_prefixes: expected environment-name prefixes such as MYAPP_",
        )
        self.clear_env = list(prefixes)
        self.stale_minutes = integer(top.get("stale_minutes", 30), "stale_minutes", 1, 1440)
        self.nice = integer(top.get("nice", 10), "nice", 0, 19)
        pool = top.get("strategy_pool")
        self.pool_path = (
            resolve_path(base, text(pool, "strategy_pool", 1000))
            if pool else PACKAGE_DIR / "data" / "strategy-pool.json"
        )
        templates = top.get("templates_dir")
        self.templates = (
            resolve_path(base, text(templates, "templates_dir", 1000))
            if templates else PACKAGE_DIR / "templates"
        )
        require(
            not overlaps(self.state, self.project),
            "state_dir must be outside project.path, and must not contain it",
        )
        for protected in self.protected:
            require(not overlaps(protected, self.state),
                    f"protected path {protected} overlaps state_dir")
            require(not overlaps(protected, self.project),
                    f"protected path {protected} overlaps project.path")

    def rel(self, path: Path) -> str:
        """A state-relative spelling for messages."""
        try:
            return path.resolve().relative_to(self.state).as_posix()
        except ValueError:
            return str(path)


def load_pool(cfg: Config) -> list[dict[str, Any]]:
    raw = closed(read_json(cfg.pool_path), {"schema", "strategies"}, {"notes"}, "strategy pool")
    require(raw["schema"] == POOL_SCHEMA, f"strategy pool schema must be {POOL_SCHEMA!r}")
    require(isinstance(raw["strategies"], list) and raw["strategies"],
            "strategy pool: expected a non-empty strategies list")
    seen: set[str] = set()
    pool = []
    for index, item in enumerate(raw["strategies"]):
        where = f"strategy pool [{index}]"
        entry = closed(item, {"slug", "name", "lens", "finds", "needs", "risks"},
                       {"tags", "retired"}, where)
        slug = text(entry["slug"], f"{where}.slug", 48)
        require(SLUG.match(slug), f"{where}.slug: use lowercase-hyphenated words")
        require(slug not in RESERVED,
                f"{where}.slug {slug!r} collides with a reserved state directory name")
        require(slug not in seen, f"{where}.slug {slug!r} is duplicated")
        seen.add(slug)
        needs = labels(entry["needs"], f"{where}.needs", 7)
        require(needs and set(needs) <= set(SURFACES),
                f"{where}.needs: choose from {', '.join(SURFACES)}")
        for field in ("name", "lens", "finds", "risks"):
            text(entry[field], f"{where}.{field}", 4000)
        retired = entry.get("retired", False)
        require(isinstance(retired, bool), f"{where}.retired: expected true or false")
        pool.append({**entry, "tags": labels(entry.get("tags", []), f"{where}.tags"),
                     "retired": retired})
    return pool


def load_templates(cfg: Config) -> dict[str, str]:
    templates = {}
    for name, allowed in TEMPLATE_KEYS.items():
        path = cfg.templates / name
        require(path.is_file(), f"missing template {path}")
        content = path.read_text(encoding="utf-8")
        unknown = sorted(set(PLACEHOLDER.findall(content)) - allowed)
        require(not unknown, f"template {name} uses unknown placeholder(s) {', '.join(unknown)}")
        templates[name] = content
    return templates


def fill(template: str, values: dict[str, str], name: str) -> str:
    """Replace every {PLACEHOLDER} in one pass; values are never rescanned."""
    missing = sorted(set(PLACEHOLDER.findall(template)) - values.keys())
    require(not missing, f"{name}: no value for placeholder(s) {', '.join(missing)}")
    return PLACEHOLDER.sub(lambda match: values[match.group(1)], template)


def guard(cfg: Config, path: Path) -> Path:
    resolved = path.resolve()
    require(within(resolved, cfg.state),
            f"refusing to write outside the state directory: {resolved}")
    return resolved


def make_dir(cfg: Config, path: Path) -> None:
    guard(cfg, path).mkdir(parents=True, exist_ok=True)


def write_text(cfg: Config, path: Path, content: str) -> None:
    """Atomic write inside the state directory: temporary file, then replace."""
    target = guard(cfg, path)
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_name(f".{target.name}.{os.getpid()}.tmp")
    with open(temporary, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(content)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, target)


def git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    """Run an allowlisted, local-only git command."""
    require(args and args[0] in GIT_ALLOWED, f"git {' '.join(args[:1])} is not allowed")
    require(not (args[0] == "branch" and {"-d", "-D", "--delete", "-f", "--force"} & set(args)),
            "the kit never deletes or force-moves branches")
    require(not (args[0] == "worktree" and args[1:2] not in (("add",), ("move",), ("list",))),
            "the kit only adds, moves and lists worktrees")
    env = dict(os.environ, GIT_TERMINAL_PROMPT="0", GIT_OPTIONAL_LOCKS="0")
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), *args],
            capture_output=True, text=True, env=env, timeout=300, check=False,
        )
    except FileNotFoundError:
        raise KitError("git is not installed or not on PATH") from None
    except subprocess.TimeoutExpired:
        raise KitError(f"git {args[0]} timed out") from None
    if check and result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        raise KitError(f"git {' '.join(args)} failed: {detail}")
    return result


def commit_of(repo: Path, ref: str) -> str | None:
    result = git(repo, "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}", check=False)
    value = result.stdout.strip()
    return value if result.returncode == 0 and value else None


def is_ancestor(repo: Path, older: str, newer: str) -> bool:
    return git(repo, "merge-base", "--is-ancestor", older, newer, check=False).returncode == 0


def common_dir(path: Path) -> Path:
    value = Path(git(path, "rev-parse", "--git-common-dir").stdout.strip())
    return (value if value.is_absolute() else path / value).resolve()


def show_plan(title: str, steps: list[str], apply: bool) -> None:
    print(title)
    for number, step in enumerate(steps, 1):
        print(f"  {number}. {step}")
    if not steps:
        print("  (nothing to do)")
    elif not apply:
        print("PLAN ONLY: nothing was changed. Re-run with --apply to perform these steps.")


def gen_dir(cfg: Config, gen: int) -> Path:
    return cfg.state / f"g{gen}"


def generations(cfg: Config) -> list[int]:
    """Regular generation directories; interrupted archives never count."""
    if not cfg.state.is_dir():
        return []
    found = []
    for child in cfg.state.iterdir():
        match = re.fullmatch(r"g([1-9][0-9]*)", child.name)
        if match and child.is_dir():
            found.append(int(match.group(1)))
    return sorted(found)


def ensure_initialized(cfg: Config) -> dict[str, Any]:
    marker = cfg.state / "improver-state.json"
    require(marker.is_file(), f"not initialized: run init --apply (expected {marker})")
    return read_json(marker)


def refuse_if_stopped(cfg: Config, what: str) -> None:
    """While STOP exists, nothing that sets up new agent work is applied."""
    stop = cfg.state / "STOP"
    if stop.exists():
        reason = stop.read_text(encoding="utf-8", errors="replace").strip()
        raise KitError(f"STOP is requested ({reason}): {what} would start new work. Record or "
                       "finish what is in flight; run resume --apply to continue")


def load_plan(cfg: Config, gen: int) -> dict[str, Any]:
    ensure_initialized(cfg)
    path = gen_dir(cfg, gen) / "plan.json"
    require(path.is_file(), f"generation {gen} is not planned: run plan {gen} --apply")
    return read_json(path)


def integration_head(cfg: Config) -> str:
    head = commit_of(cfg.project, f"refs/heads/{cfg.integration_branch}")
    require(head, f"integration branch {cfg.integration_branch!r} is missing: run init --apply")
    return str(head)


def history_text(cfg: Config) -> str:
    path = cfg.state / "history.md"
    if path.is_file() and path.read_text(encoding="utf-8").strip():
        return path.read_text(encoding="utf-8").strip()
    return "Nothing has been integrated yet: this is the first generation."


def load_baseline(cfg: Config, label: str = "latest") -> dict[str, Any] | None:
    path = cfg.state / "baseline" / f"{label}.json"
    return read_json(path) if path.is_file() else None


def baseline_block(record: dict[str, Any]) -> str:
    passed = sum(1 for item in record["results"] if item["passed"])
    lines = [
        f"Recorded at {record['head'][:12]} on {record['recorded_at']}: "
        f"{passed} of {len(record['results'])} verify commands pass."
    ]
    for item in record["results"]:
        state = "PASS" if item["passed"] else "FAIL"
        detail = "timed out" if item["timed_out"] else f"exit {item['exit_code']}"
        line = f"- {item['name']}: {state} ({detail}, {item['seconds']} s)"
        if not item["passed"]:
            line += " - already failing at the base: do not make it worse, and say so."
        lines.append(line)
    return "\n".join(lines)


def verify_block(cfg: Config) -> str:
    return bullet([
        f"{item['name']}: `{shlex.join(item['run'])}` (in `{item['cwd']}`, timeout "
        f"{item['timeout_seconds']} s, "
        f"{'throwaway home' if item['hermetic_home'] else 'real home'})"
        for item in cfg.verify
    ])


def harness_block(cfg: Config) -> str:
    if cfg.harness is None:
        return (
            "No isolated harness is configured. Do not start this project's user interface, "
            "servers or background services; work through its tests and command-line entry "
            "points only."
        )
    return (
        f"Run the user interface or live services ONLY through the isolated harness: "
        f"`{shlex.join(cfg.harness['run'])}`\n{cfg.harness['description']}"
    )


def focus_block(focus: dict[str, Any]) -> str:
    if focus.get("text"):
        return (
            f"This generation carries the owner's focus: {focus['text']}\n"
            "Attack this focus through your lens; the other strategists attack it through theirs."
        )
    return "No focus is set for this generation: follow your lens to the most valuable problem."


def common_values(cfg: Config, plan: dict[str, Any], baseline: dict[str, Any]) -> dict[str, str]:
    return {
        "GEN": str(plan["generation"]),
        "N": str(plan["strategist_count"]),
        "PROJECT_NAME": cfg.name,
        "PROJECT_CONTEXT": cfg.context,
        "SURFACES": ", ".join(cfg.surfaces),
        "FOCUS": focus_block(plan["focus"]),
        "HISTORY": history_text(cfg),
        "BASE_COMMIT": plan["base"],
        "INTEGRATION_BRANCH": plan["integration_branch"],
        "BASELINE": baseline_block(baseline),
        "VERIFY_COMMANDS": verify_block(cfg),
        "HARNESS": harness_block(cfg),
        "PROTECTED_PATHS": bullet([str(p) for p in cfg.protected])
        or "- none declared: ask the orchestrator before touching anything outside your worktree",
        "LIVE_PORTS": ", ".join(str(port) for port in cfg.live_ports) or "none declared",
    }


def cmd_init(cfg: Config, args: argparse.Namespace) -> int:
    pool = load_pool(cfg)
    load_templates(cfg)
    require(cfg.project.is_dir(), f"project.path does not exist: {cfg.project}")
    top = Path(git(cfg.project, "rev-parse", "--show-toplevel").stdout.strip()).resolve()
    require(top == cfg.project, f"project.path must be the top of a git work tree, not {top}")
    base = commit_of(cfg.project, f"refs/heads/{cfg.base_branch}")
    require(base, f"base branch {cfg.base_branch!r} does not exist in {cfg.project}")
    head = commit_of(cfg.project, f"refs/heads/{cfg.integration_branch}")
    eligible = eligible_strategies(pool, cfg, set())
    print(f"Project: {cfg.name} ({cfg.project})")
    print(f"Base branch: {cfg.base_branch} at {str(base)[:12]}; integration branch: "
          f"{cfg.integration_branch} ({'at ' + head[:12] if head else 'to be created'})")
    print(f"Strategy pool: {len(pool)} lenses, {len(eligible)} fit surfaces "
          f"{', '.join(cfg.surfaces)}; {cfg.n} per generation, so about "
          f"{len(eligible) // cfg.n} generations before strategy-library must add lenses.")
    print(f"Verify commands: {', '.join(item['name'] for item in cfg.verify)}")
    print(f"Protected paths: {', '.join(str(p) for p in cfg.protected) or 'none declared'}")
    steps = []
    if not cfg.state.exists():
        steps.append(f"create the state directory {cfg.state}")
    if head is None:
        steps.append(f"create local branch {cfg.integration_branch} at {cfg.base_branch} "
                     f"({str(base)[:12]})")
    steps.append("write improver-state.json (kit version, config digest, starting commit)")
    show_plan("init", steps, args.apply)
    if not args.apply:
        return 0
    cfg.state.mkdir(parents=True, exist_ok=True)
    if head is None:
        git(cfg.project, "branch", cfg.integration_branch, str(base))
    marker = cfg.state / "improver-state.json"
    previous = read_json(marker) if marker.is_file() else {}
    write_text(cfg, marker, dump_json({
        "schema": "improver-state/1",
        "kit_version": KIT_VERSION,
        "config": str(cfg.file),
        "config_sha256": cfg.digest,
        "project": str(cfg.project),
        "start_commit": previous.get("start_commit", head or base),
        "initialized_at": previous.get("initialized_at", now_iso()),
    }))
    print(f"APPLIED: state directory ready at {cfg.state}")
    return 0


def files_under(root: Path, cap: int = 200) -> list[str]:
    found: list[str] = []
    for dirpath, _dirnames, filenames in os.walk(root):
        for name in filenames:
            found.append(Path(dirpath, name).relative_to(root).as_posix())
            if len(found) >= cap:
                return sorted(found)
    return sorted(found)


def run_verify(cfg: Config, command: dict[str, Any], at: Path, label: str,
               keep_homes: bool) -> dict[str, Any]:
    cwd = (at / command["cwd"]).resolve()
    require(within(cwd, at), f"verify {command['name']}: cwd escapes the checkout")
    env = {key: value for key, value in os.environ.items()
           if not any(key.startswith(prefix) for prefix in cfg.clear_env)}
    env.update(command["env"])
    throwaway: Path | None = None
    if command["hermetic_home"]:
        make_dir(cfg, cfg.state / "homes")
        throwaway = Path(tempfile.mkdtemp(prefix=f"{label}-{command['name']}-",
                                          dir=cfg.state / "homes"))
        home, temp = throwaway / "home", throwaway / "tmp"
        home.mkdir()
        temp.mkdir()
        for name in HOME_VARS:
            env[name] = str(home)
        for name, relative in HOME_SUBDIRS.items():
            env[name] = str(home / relative)
        for name in TEMP_VARS:
            env[name] = str(temp)
        env["IMPROVER_THROWAWAY_HOME"] = str(home)
    executable = shutil.which(command["run"][0], path=env.get("PATH")) or command["run"][0]
    options: dict[str, Any] = {}
    if os.name == "posix":
        options["start_new_session"] = True
        if cfg.nice:
            options["preexec_fn"] = lambda: os.nice(cfg.nice)
    started = time.monotonic()
    timed_out = False
    exit_code: int | None = None
    try:
        process = subprocess.Popen([executable, *command["run"][1:]], cwd=cwd, env=env,
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT, **options)
        try:
            output, _ = process.communicate(timeout=command["timeout_seconds"])
        except subprocess.TimeoutExpired:
            timed_out = True
            if os.name == "posix":
                os.killpg(process.pid, signal.SIGKILL)
            else:
                process.kill()
            output, _ = process.communicate()
        exit_code = None if timed_out else process.returncode
    except OSError as exc:
        output = f"could not start {command['run'][0]!r}: {exc}\n".encode()
    seconds = round(time.monotonic() - started, 1)
    log_text = output.decode("utf-8", errors="replace")
    log_path = cfg.state / "baseline" / "logs" / label / f"{command['name']}.log"
    write_text(cfg, log_path, log_text)
    home_writes: list[str] = []
    if throwaway is not None:
        home_writes = files_under(throwaway / "home")
        if not keep_homes:
            shutil.rmtree(guard(cfg, throwaway), ignore_errors=True)
    return {
        "name": command["name"],
        "run": command["run"],
        "cwd": command["cwd"],
        "exit_code": exit_code,
        "timed_out": timed_out,
        "passed": exit_code == 0,
        "seconds": seconds,
        "tail": log_text.splitlines()[-15:],
        "log": cfg.rel(log_path),
        "hermetic_home": command["hermetic_home"],
        "home_writes": home_writes,
    }


def cmd_baseline(cfg: Config, args: argparse.Namespace) -> int:
    ensure_initialized(cfg)
    label = args.label
    require(SLUG.match(label), "--label: use lowercase-hyphenated words, e.g. g2-verify")
    at = Path(args.at).resolve() if args.at else cfg.project
    require(at.is_dir(), f"--at: not a directory: {at}")
    require(common_dir(at) == common_dir(cfg.project),
            f"--at must be the project or one of its worktrees: {at}")
    head = commit_of(at, "HEAD")
    require(head, f"no commit checked out at {at}")
    selected = cfg.verify
    if args.only:
        unknown = sorted(set(args.only) - {item["name"] for item in cfg.verify})
        require(not unknown, f"--only: unknown verify command(s) {', '.join(unknown)}")
        selected = [item for item in cfg.verify if item["name"] in args.only]
    result_path = cfg.state / "baseline" / f"{label}.json"
    steps = [
        f"run {item['name']}: {shlex.join(item['run'])} in {item['cwd']} (timeout "
        f"{item['timeout_seconds']} s, {'throwaway' if item['hermetic_home'] else 'REAL'} home, "
        f"cleared env prefixes: {', '.join(cfg.clear_env) or 'none'}, nice {cfg.nice})"
        for item in selected
    ]
    steps.append(f"record results in {cfg.rel(result_path)} and logs in baseline/logs/{label}/")
    show_plan(f"baseline '{label}' at {at} (HEAD {str(head)[:12]})", steps, args.apply)
    if not args.apply:
        return 0
    results = [run_verify(cfg, item, at, label, args.keep_homes) for item in selected]
    passed = all(item["passed"] for item in results)
    write_text(cfg, result_path, dump_json({
        "schema": "improver-baseline/1",
        "label": label,
        "at": str(at),
        "head": head,
        "recorded_at": now_iso(),
        "passed": passed,
        "results": results,
    }))
    for item in results:
        writes = item["home_writes"]
        note = f" - wrote into the throwaway home: {', '.join(writes[:5])}" if writes else ""
        print(f"  {'PASS' if item['passed'] else 'FAIL'} {item['name']} "
              f"({item['seconds']} s){note}")
    count = sum(1 for item in results if item["passed"])
    print(f"APPLIED: baseline '{label}' recorded at {str(head)[:12]}: "
          f"{count}/{len(results)} passed")
    return 0 if passed else 3


def eligible_strategies(pool: list[dict[str, Any]], cfg: Config,
                        used: set[str]) -> list[dict[str, Any]]:
    surfaces = set(cfg.surfaces)
    return [
        item for item in pool
        if not item["retired"] and item["slug"] not in used
        and ("any" in item["needs"] or surfaces & set(item["needs"]))
    ]


def used_strategies(cfg: Config, except_gen: int) -> dict[str, int]:
    """Every slug planned by any other generation, including interrupted archives."""
    used: dict[str, int] = {}
    if not cfg.state.is_dir():
        return used
    for child in sorted(cfg.state.iterdir()):
        match = re.fullmatch(r"g([1-9][0-9]*)(?:-interrupted-[0-9]+)?", child.name)
        plan_path = child / "plan.json"
        if not match or int(match.group(1)) == except_gen or not plan_path.is_file():
            continue
        for item in read_json(plan_path)["strategists"]:
            used.setdefault(item["slug"], int(match.group(1)))
    return used


def choose(pool: list[dict[str, Any]], cfg: Config, gen: int,
           used: set[str]) -> list[dict[str, Any]]:
    """Seeded, reproducible choice: rank by SHA-256(seed, generation, slug)."""
    eligible = eligible_strategies(pool, cfg, used)
    prefer = set(cfg.prefer_tags)

    def rank(item: dict[str, Any]) -> str:
        return sha256_bytes(f"{cfg.seed}\n{gen}\n{item['slug']}".encode())

    preferred = sorted((i for i in eligible if prefer & set(i["tags"])), key=rank)
    others = sorted((i for i in eligible if not prefer & set(i["tags"])), key=rank)
    picks = (preferred + others)[: cfg.n]
    require(
        len(picks) == cfg.n,
        f"only {len(picks)} unused strategies fit surfaces {', '.join(cfg.surfaces)}; "
        f"strategies are never reused, so strategy-library must add lenses to "
        f"{cfg.pool_path.name} before generation {gen}",
    )
    return picks


def cmd_plan(cfg: Config, args: argparse.Namespace) -> int:
    ensure_initialized(cfg)
    gen = args.gen
    if args.apply:
        refuse_if_stopped(cfg, f"plan {gen}")
    folder = gen_dir(cfg, gen)
    plan_path = folder / "plan.json"
    if plan_path.is_file() and not args.replace:
        plan = read_json(plan_path)
        for item in plan["strategists"]:
            print(f"  {item['index']}. {item['name']} ({item['slug']}) -> {item['branch']}")
        print(f"Generation {gen} is already planned from {plan['base'][:12]}; nothing changed. "
              "Use --replace to plan it again before its worktrees exist.")
        return 0
    require(not (folder / "worktrees.json").exists(),
            f"generation {gen} already has worktrees; if it was interrupted, run resume --apply, "
            "which archives it, then plan it again")
    base = integration_head(cfg)
    pool = load_pool(cfg)
    used = used_strategies(cfg, gen)
    strategists = []
    for index, item in enumerate(choose(pool, cfg, gen, set(used)), 1):
        slug = item["slug"]
        strategists.append({
            "index": index, "slug": slug, "name": item["name"], "lens": item["lens"],
            "finds": item["finds"], "needs": item["needs"], "risks": item["risks"],
            "tags": item["tags"],
            "branch": f"{cfg.prefix}/g{gen}-{slug}",
            "worktree": str(cfg.state / "worktrees" / f"g{gen}" / slug),
            "scratch": str(folder / "scratch" / slug),
            "report": str(folder / "reports" / f"{slug}.md"),
            "brief": str(folder / "prompts" / f"{slug}.md"),
        })
    plan = {
        "schema": "improver-plan/1",
        "generation": gen,
        "seed": cfg.seed,
        "base": base,
        "integration_branch": cfg.integration_branch,
        "strategist_count": cfg.n,
        "majority": majority(cfg.n),
        "focus": {"text": cfg.focus_text, "prefer_tags": cfg.prefer_tags},
        "surfaces": cfg.surfaces,
        "pool_sha256": sha256_bytes(cfg.pool_path.read_bytes()),
        "excluded_as_used": sorted(used),
        "strategists": strategists,
        "planned_at": now_iso(),
    }
    for item in strategists:
        print(f"  {item['index']}. {item['name']} ({item['slug']}) -> {item['branch']}")
    print(f"{len(used)} earlier strategies excluded; majority threshold "
          f"{majority(cfg.n)} of {cfg.n}.")
    show_plan(f"plan generation {gen} from {cfg.integration_branch} at {base[:12]} "
              f"(seed {cfg.seed!r})", [f"write {cfg.rel(plan_path)}"], args.apply)
    if args.apply:
        write_text(cfg, plan_path, dump_json(plan))
        print(f"APPLIED: generation {gen} planned")
    return 0


def cmd_render(cfg: Config, args: argparse.Namespace) -> int:
    plan = load_plan(cfg, args.gen)
    templates = load_templates(cfg)
    baseline = load_baseline(cfg)
    require(baseline, "no baseline recorded: run baseline --apply first; every change must "
                      "hold the baseline, so the briefs quote it")
    assert baseline is not None
    if baseline["head"] != plan["base"]:
        print(f"WARNING: the latest baseline was recorded at {baseline['head'][:12]} but "
              f"generation {args.gen} starts from {plan['base'][:12]}: record a fresh baseline "
              "so the briefs quote the right bar.")
    if not baseline["passed"]:
        print("WARNING: the baseline has failing commands; the briefs say which ones.")
    common = common_values(cfg, plan, baseline)
    outputs = []
    for item in plan["strategists"]:
        report = fill(templates["report.md"], {
            "GEN": str(plan["generation"]), "STRATEGY_NAME": item["name"],
            "STRATEGY_SLUG": item["slug"], "BRANCH": item["branch"],
        }, "report.md")
        values = {
            **common,
            "IDX": str(item["index"]), "STRATEGY_NAME": item["name"],
            "STRATEGY_SLUG": item["slug"], "LENS": item["lens"], "FINDS": item["finds"],
            "RISK_NOTES": item["risks"], "WORKTREE": item["worktree"],
            "BRANCH": item["branch"], "SCRATCH": item["scratch"], "REPORT": item["report"],
            "REPORT_TEMPLATE": report,
        }
        brief = fill(templates["strategist-brief.md"], values, "strategist-brief.md")
        outputs.append((Path(item["brief"]), brief))
    reports = gen_dir(cfg, args.gen) / "reports"
    steps = [f"write {cfg.rel(path)} ({len(body)} characters)" for path, body in outputs]
    steps.append(f"create {cfg.rel(reports)}/ for the {len(outputs)} reports")
    show_plan(f"render generation {args.gen} briefs", steps, args.apply)
    if args.apply:
        for path, body in outputs:
            write_text(cfg, path, body)
        make_dir(cfg, reports)
        print(f"APPLIED: {len(outputs)} briefs rendered")
    return 0


def cmd_worktrees(cfg: Config, args: argparse.Namespace) -> int:
    plan = load_plan(cfg, args.gen)
    gen = args.gen
    if args.apply:
        refuse_if_stopped(cfg, f"worktrees {gen}")
    folder = gen_dir(cfg, gen)
    head = integration_head(cfg)
    entries = []
    if args.integrator:
        tally_path = folder / "tally.json"
        require(tally_path.is_file(), f"run tally {gen} --apply first: the integrator builds "
                                      "what the tally decided")
        at_tally = read_json(tally_path)["integration_head"]
        require(at_tally == head, f"the integration branch moved to {head[:12]} after the tally "
                                  f"(at {at_tally[:12]}); re-run tally {gen} --apply so the "
                                  "integrator brief names the right base")
        entries.append({
            "slug": "integrator", "branch": f"{cfg.prefix}/g{gen}-integration",
            "worktree": str(cfg.state / "worktrees" / f"g{gen}" / "integrator"),
            "scratch": str(folder / "scratch" / "integrator"), "base": head,
        })
    else:
        require(head == plan["base"],
                f"the integration branch moved from {plan['base'][:12]} to {head[:12]} since "
                f"generation {gen} was planned: run plan {gen} --replace --apply and render again")
        for item in plan["strategists"]:
            require(SLUG.match(item["slug"]) and item["slug"] not in RESERVED,
                    f"refusing strategy slug {item['slug']!r}: it collides with a reserved "
                    "state directory name")
            entries.append({key: item[key] for key in ("slug", "branch", "worktree", "scratch")}
                           | {"base": plan["base"]})
    steps = []
    for entry in entries:
        path = guard(cfg, Path(entry["worktree"]))
        require(not path.exists(), f"refusing to reuse an existing path: {path}")
        require(commit_of(cfg.project, f"refs/heads/{entry['branch']}") is None,
                f"refusing: branch {entry['branch']} already exists")
        steps.append(f"git worktree add -b {entry['branch']} {path} {entry['base'][:12]}")
        steps.append(f"create scratch directory {cfg.rel(Path(entry['scratch']))}")
    record_path = folder / ("integrator.json" if args.integrator else "worktrees.json")
    steps.append(f"record {cfg.rel(record_path)}")
    show_plan(f"worktrees for generation {gen}{' (integrator)' if args.integrator else ''}",
              steps, args.apply)
    if not args.apply:
        return 0
    for entry in entries:
        make_dir(cfg, Path(entry["worktree"]).parent)
        git(cfg.project, "worktree", "add", "-b", entry["branch"], entry["worktree"],
            entry["base"])
        make_dir(cfg, Path(entry["scratch"]))
    record: dict[str, Any] = {"created_at": now_iso(), "entries": entries}
    if args.integrator:
        record["report"] = str(folder / "INTEGRATION.md")
        record["brief"] = str(folder / "integrator-brief.md")
    write_text(cfg, record_path, dump_json(record))
    print(f"APPLIED: {len(entries)} worktree(s) created")
    return 0


def snapshot(paths: list[Path]) -> dict[str, Any]:
    """Size and modification time of every entry under each protected path (read-only)."""
    result: dict[str, Any] = {}
    for root in paths:
        entry: dict[str, Any] = {"exists": root.exists() or root.is_symlink(),
                                 "entries": {}, "truncated": False}
        if root.is_symlink() or root.is_file():
            info = root.lstat()
            entry["entries"]["."] = [info.st_size, info.st_mtime_ns]
        elif root.is_dir():
            for dirpath, dirnames, filenames in os.walk(root):
                names = filenames + [d for d in dirnames if os.path.islink(Path(dirpath, d))]
                for name in names:
                    full = Path(dirpath, name)
                    try:
                        info = full.lstat()
                    except OSError:
                        continue
                    entry["entries"][full.relative_to(root).as_posix()] = [
                        info.st_size, info.st_mtime_ns]
                    if len(entry["entries"]) >= WALK_CAP:
                        entry["truncated"] = True
                        break
                if entry["truncated"]:
                    break
        result[str(root)] = entry
    return result


def audit_findings(marker: dict[str, Any], current: dict[str, Any]) -> list[str]:
    findings: list[str] = []
    since = marker["marked_ns"]
    for root, before in sorted(marker["paths"].items()):
        after = current.get(root, {"exists": False, "entries": {}, "truncated": False})
        if before["exists"] != after["exists"]:
            findings.append(f"{'created' if after['exists'] else 'deleted'} {root}")
        old, new = before["entries"], after["entries"]
        partial = before["truncated"] or after["truncated"]
        for name in sorted(new.keys() - old.keys()):
            if not partial or new[name][1] > since:
                findings.append(f"created {root}/{name}")
        if not partial:
            findings.extend(f"deleted {root}/{name}" for name in sorted(old.keys() - new.keys()))
        findings.extend(f"modified {root}/{name}" for name in sorted(old.keys() & new.keys())
                        if old[name] != new[name])
    return findings


def run_audit(cfg: Config, label: str) -> dict[str, Any]:
    marker_path = cfg.state / "markers" / f"{label}.json"
    require(marker_path.is_file(), f"no audit marker {label!r}: run audit {label} --mark --apply "
                                   "before any strategist or implementer starts")
    marker = read_json(marker_path)
    watched = [Path(path) for path in marker["paths"]]
    findings = audit_findings(marker, snapshot(watched))
    unwatched = sorted(str(p) for p in cfg.protected if str(p) not in marker["paths"])
    return {"marker": label, "marked_at": marker["marked_at"], "checked_at": now_iso(),
            "clean": not findings, "findings": findings[:500], "finding_count": len(findings),
            "not_covered_by_marker": unwatched}


def cmd_audit(cfg: Config, args: argparse.Namespace) -> int:
    ensure_initialized(cfg)
    label = args.marker
    require(SLUG.match(label), "marker: use lowercase-hyphenated words, e.g. g3")
    marker_path = cfg.state / "markers" / f"{label}.json"
    if args.mark:
        steps = [f"snapshot {len(cfg.protected)} protected path(s) into {cfg.rel(marker_path)}"]
        if marker_path.is_file():
            steps.insert(0, f"replace the marker recorded {read_json(marker_path)['marked_at']}")
        show_plan(f"audit marker '{label}'", steps, args.apply)
        if args.apply:
            marked_ns = time.time_ns()
            write_text(cfg, marker_path, dump_json({
                "schema": "improver-audit-marker/1", "marker": label, "marked_at": now_iso(),
                "marked_ns": marked_ns, "paths": snapshot(cfg.protected),
            }))
            print(f"APPLIED: marker '{label}' recorded")
        return 0
    result = run_audit(cfg, label)
    if args.json:
        print(dump_json(result), end="")
    else:
        print(f"audit '{label}' since {result['marked_at']}: "
              f"{'CLEAN' if result['clean'] else 'PROTECTED PATHS CHANGED'}")
        for finding in result["findings"][:50]:
            print(f"  - {finding}")
        for path in result["not_covered_by_marker"]:
            print(f"  note: {path} was added to protected_paths after the marker")
    if args.apply:
        write_text(cfg, cfg.state / "markers" / f"{label}.result.json", dump_json(result))
    return 0 if result["clean"] else 3


REPORT_SECTIONS = ("verdict", "evidence", "why this target", "solution", "verification",
                   "commits", "risks", "top 3 features", "candidate ledger")


def split_sections(body: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for line in body.splitlines():
        match = re.match(r"^##(?!#)\s*(.+?)\s*#*\s*$", line)
        if match:
            heading = match.group(1).lower().replace("top three", "top 3")
            current = next((name for name in REPORT_SECTIONS if heading.startswith(name)),
                           heading)
            sections.setdefault(current, [])
        elif current is not None:
            sections[current].append(line)
    return {name: "\n".join(lines).strip() for name, lines in sections.items()}


def find_key(line: str) -> str | None:
    for candidate in re.findall(r"`([^`]+)`", line):
        if KEY.match(candidate.strip().lower()):
            return candidate.strip().lower()
    match = KEY_IN_TEXT.search(line.lower())
    return match.group(0) if match else None


def score(cell: str) -> int | None:
    match = re.fullmatch(r"\s*\**([1-5])\**(?:\s*/\s*5)?\s*", cell)
    return int(match.group(1)) if match else None


def parse_report(body: str) -> dict[str, Any]:
    """Read the fixed report format: Verdict, Commits, Top 3 features, Candidate ledger."""
    sections = split_sections(body)
    problems = []
    absent = [name for name in ("verdict", "commits", "top 3 features", "candidate ledger")
              if name not in sections]
    if absent:
        problems.append(f"missing section(s): {', '.join(absent)}")
    verdict = next((line.strip() for line in sections.get("verdict", "").splitlines()
                    if line.strip()), "")
    top3: list[list[str]] = []
    for line in sections.get("top 3 features", "").splitlines():
        item = re.match(r"^\s*(?:\d+[.)]|[-*])\s+(.*)$", line)
        if not item:
            continue
        key = find_key(item.group(1))
        if key is None:
            problems.append(f"top-3 line has no area:problem key: {line.strip()[:80]}")
            continue
        if key in [existing for existing, _ in top3]:
            continue
        spec = item.group(1).replace(f"`{key}`", "", 1)
        spec = re.sub(re.escape(key), "", spec, count=1, flags=re.IGNORECASE)
        top3.append([key, spec.strip(" \t-:|*").strip()])
        if len(top3) == 3:
            break
    ledger = []
    for line in sections.get("candidate ledger", "").splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", cell) for cell in cells if cell):
            continue
        if cells[0].strip("` *").lower() == "key":
            continue
        if len(cells) < 6:
            problems.append(f"ledger row has {len(cells)} cells, needs 6: {stripped[:80]}")
            continue
        key = cells[0].strip("` *").lower()
        if not KEY.match(key):
            problems.append(f"ledger key is not kebab-case area:problem: {cells[0][:60]}")
            continue
        flag = cells[5].strip("` *").lower()
        if flag.startswith("partial"):
            implemented = "partial"
        elif flag.startswith(("yes", "done", "implemented")) or flag == "y":
            implemented = "yes"
        else:
            implemented = "no"
        impact, confidence = score(cells[3]), score(cells[4])
        if impact is None or confidence is None:
            problems.append(f"{key}: impact and confidence must be integers from 1 to 5")
        ledger.append({"key": key, "problem": cells[1], "solution": cells[2],
                       "impact": impact, "confidence": confidence,
                       "implemented": implemented})
    commits: list[str] = []
    for sha in SHA_IN_TEXT.findall(sections.get("commits", "")):
        if any(ch.isdigit() for ch in sha) and sha not in commits:
            commits.append(sha)
    return {"verdict": verdict, "top3": top3, "ledger": ledger, "commits": commits,
            "problems": problems}


def load_aliases(path: Path) -> dict[str, str]:
    if not path.is_file():
        return {}
    raw = read_json(path)
    require(isinstance(raw, dict), f"{path.name}: expected an object of key -> canonical key")
    for key, target in raw.items():
        require(isinstance(target, str) and KEY.match(key) and KEY.match(target),
                f"{path.name}: {key!r} -> {target!r}: both must be area:problem keys")
        require(raw.get(target, target) == target,
                f"{path.name}: {target!r} is itself an alias; point aliases at the final key")
    return dict(raw)


def build_tally(plan: dict[str, Any], reports: dict[str, dict[str, Any]],
                aliases: dict[str, str], missing: list[str], head: str) -> dict[str, Any]:
    order = [item["slug"] for item in plan["strategists"]]
    count = plan["strategist_count"]
    threshold = majority(count)
    clusters: dict[str, dict[str, Any]] = {}

    def cluster(key: str) -> dict[str, Any]:
        name = aliases.get(key, key)
        return clusters.setdefault(name, {
            "key": name, "supporters": set(), "top3": set(), "scores": [],
            "implemented": {}, "keys": set(), "solutions": [], "problems": [], "specs": []})

    for slug in order:
        report = reports.get(slug)
        if report is None:
            continue
        for key, spec in report["top3"]:
            entry = cluster(key)
            entry["supporters"].add(slug)
            entry["top3"].add(slug)
            entry["keys"].add(key)
            if spec:
                entry["specs"].append([slug, spec])
        for row in report["ledger"]:
            entry = cluster(row["key"])
            entry["supporters"].add(slug)
            entry["keys"].add(row["key"])
            if row["impact"] and row["confidence"]:
                entry["scores"].append(row["impact"] * row["confidence"])
            if row["implemented"] != "no":
                entry["implemented"][slug] = row["implemented"]
            entry["solutions"].append([slug, row["solution"]])
            entry["problems"].append([slug, row["problem"]])

    def mean(entry: dict[str, Any]) -> Fraction:
        scores = entry["scores"]
        return Fraction(sum(scores), len(scores)) if scores else Fraction(0)

    ranked = sorted(clusters.values(), key=lambda e: (
        -len(e["supporters"]), -mean(e), -len(e["top3"]), e["key"]))
    serial = [{
        "rank": rank,
        "key": entry["key"],
        "support": len(entry["supporters"]),
        "supporters": [slug for slug in order if slug in entry["supporters"]],
        "top3_mentions": len(entry["top3"]),
        "mean_impact_confidence": f"{float(mean(entry)):.1f}",
        "implemented_by": {s: entry["implemented"][s] for s in order if s in entry["implemented"]},
        "merged_keys": sorted(entry["keys"]),
        "majority": len(entry["supporters"]) >= threshold,
        "solutions": entry["solutions"],
        "problems": entry["problems"],
        "specs": entry["specs"],
    } for rank, entry in enumerate(ranked, 1)]
    top = serial[:3]
    decision = "none" if not top else ("majority" if top[0]["majority"] else "majority-like")
    return {
        "schema": "improver-tally/1",
        "generation": plan["generation"],
        "base": plan["base"],
        "integration_head": head,
        "strategist_count": count,
        "majority": threshold,
        "reports": len(reports),
        "missing": missing,
        "decision": decision,
        "top3": [entry["key"] for entry in top],
        "clusters": serial,
        "strategists": {slug: {"verdict": reports[slug]["verdict"],
                               "problems": reports[slug]["problems"]}
                        for slug in order if slug in reports},
        "tallied_at": now_iso(),
    }


def recurring(cfg: Config, gen: int, current: dict[str, Any]) -> list[dict[str, Any]]:
    """Findings not selected, carried across generations (earlier tallies plus this one)."""
    tallies = [read_json(gen_dir(cfg, g) / "tally.json") for g in generations(cfg)
               if g < gen and (gen_dir(cfg, g) / "tally.json").is_file()]
    table: dict[str, dict[str, Any]] = {}
    for data in [*tallies, current]:
        selected = set(data["top3"])
        for entry in data["clusters"]:
            row = table.setdefault(entry["key"], {
                "key": entry["key"], "generations": [], "support_total": 0,
                "selected_in": [], "latest_solution": ""})
            if entry["key"] in selected:
                row["selected_in"].append(data["generation"])
                continue
            row["generations"].append(data["generation"])
            row["support_total"] += entry["support"]
            if entry["solutions"]:
                row["latest_solution"] = entry["solutions"][0][1]
    rows = [row for row in table.values() if row["generations"]]
    return sorted(rows, key=lambda r: (-len(r["generations"]), -r["support_total"], r["key"]))


def branch_evidence(cfg: Config, plan: dict[str, Any],
                    reports: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """What git says, independent of what the reports claim."""
    evidence = {}
    for item in plan["strategists"]:
        head = commit_of(cfg.project, f"refs/heads/{item['branch']}")
        worktree = Path(item["worktree"])
        clean = None
        if worktree.is_dir():
            status = git(worktree, "status", "--porcelain", check=False)
            clean = status.returncode == 0 and not status.stdout.strip()
        new_commits = 0
        if head:
            log = git(cfg.project, "log", "--format=%H", f"{plan['base']}..{head}", check=False)
            new_commits = len(log.stdout.split()) if log.returncode == 0 else 0
        claimed = [{
            "sha": sha,
            "on_branch": bool(head) and is_ancestor(cfg.project, sha, str(head))
            and not is_ancestor(cfg.project, sha, plan["base"]),
        } for sha in reports.get(item["slug"], {}).get("commits", [])]
        evidence[item["slug"]] = {"branch": item["branch"], "head": head,
                                  "new_commits": new_commits, "worktree_clean": clean,
                                  "claimed_commits": claimed}
    return evidence


def cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def decision_text(result: dict[str, Any]) -> str:
    count, threshold = result["strategist_count"], result["majority"]
    top = [c for c in result["clusters"] if c["key"] in result["top3"]]
    if not top:
        return "No report contained a usable Top 3 or Candidate ledger: nothing to integrate."
    if result["decision"] == "majority":
        lines = [f"Majority: `{top[0]['key']}` reached {top[0]['support']} of {count} "
                 f"strategists (threshold {threshold})."]
    else:
        lines = [f"No cluster reached a majority ({threshold} of {count}). The broadest cluster, "
                 f"`{top[0]['key']}` with {top[0]['support']} of {count}, is taken as "
                 "MAJORITY-LIKE: confirm it is one coherent solution before integrating."]
    lines.append("Top 3 consensus features (continuous mode): " + "; ".join(
        f"`{c['key']}` {c['support']}/{count} "
        f"({'majority' if c['majority'] else 'majority-like'})" for c in top))
    return "\n".join(lines)


def render_tally(plan: dict[str, Any], result: dict[str, Any],
                 rows: list[dict[str, Any]]) -> str:
    count, threshold = result["strategist_count"], result["majority"]
    names = {item["slug"]: item["name"] for item in plan["strategists"]}
    evidence = result["evidence"]
    out = [
        f"# Generation {result['generation']}: tally (draft)", "",
        f"Base `{result['base'][:12]}` - {result['reports']} of {count} reports - majority "
        f"means at least {threshold} of {count} distinct strategists.", "",
        "> Drafted by the kit from each report's Top 3 and Candidate ledger, clustered by "
        "ledger key. Consensus is decided by what each solution REQUIRES, not by its wording: "
        "read the proposed solutions below, map keys that need the same change onto one key in "
        "`aliases.json` next to this file, and run the tally again. Finalize this file before "
        "integrating; `record` snapshots it as a read-only receipt.", "",
    ]
    if result["missing"]:
        out += [f"**Incomplete:** no report from {', '.join(result['missing'])}. Tallied with "
                "--allow-missing; interrupted work is never counted.", ""]
    out += ["## Strategists", "",
            "| # | Strategy | Verdict | Branch | New commits | Claimed commits verified | Clean |",
            "|---|---|---|---|---|---|---|"]
    for item in plan["strategists"]:
        slug = item["slug"]
        found = evidence[slug]
        claimed = found["claimed_commits"]
        verified = sum(1 for c in claimed if c["on_branch"])
        summary = result["strategists"].get(slug, {}).get("verdict") or "(no report)"
        clean = {True: "yes", False: "NO", None: "n/a"}[found["worktree_clean"]]
        out.append(f"| {item['index']} | {cell(item['name'])} (`{slug}`) | {cell(summary)} | "
                   f"`{found['branch']}` | {found['new_commits']} | {verified} of "
                   f"{len(claimed)} | {clean} |")
    out += ["", "## Clusters", "",
            "Ranked by distinct supporting strategists, then mean impact x confidence, then "
            "Top 3 mentions.", "",
            "| Rank | Key | Support | Strategists | In Top 3 of | Mean I x C | Implemented by |"
            " Status |", "|---|---|---|---|---|---|---|---|"]
    for c in result["clusters"]:
        status = "majority" if c["majority"] else "minority"
        if c["key"] in result["top3"]:
            status += ", TOP 3"
        implementers = ", ".join(f"{s} ({v})" for s, v in c["implemented_by"].items()) or "-"
        merged = f" (merged: {', '.join(c['merged_keys'])})" if len(c["merged_keys"]) > 1 else ""
        out.append(f"| {c['rank']} | `{c['key']}`{merged} | {c['support']}/{count} | "
                   f"{', '.join(c['supporters'])} | {c['top3_mentions']} | "
                   f"{c['mean_impact_confidence']} | {implementers} | {status} |")
    out += ["", "## Decision", "", decision_text(result), ""]
    for number, c in enumerate([c for c in result["clusters"] if c["key"] in result["top3"]], 1):
        out.append(f"{number}. `{c['key']}` - {c['support']} of {count}")
        for slug, solution in c["solutions"]:
            out.append(f"   - {names.get(slug, slug)} proposes: {cell(solution)}")
        for slug, spec in c["specs"]:
            out.append(f"   - {names.get(slug, slug)} (Top 3): {cell(spec)}")
    areas: dict[str, list[str]] = {}
    for c in result["clusters"]:
        areas.setdefault(c["key"].split(":", 1)[0], []).append(f"`{c['key']}` ({c['support']})")
    shared = [f"- area `{area}`: {', '.join(keys)}" for area, keys in sorted(areas.items())
              if len(keys) > 1]
    out += ["", "## Same-area keys to review", "",
            "Do any of these require the same solution? If so, merge them in aliases.json.", "",
            *(shared or ["- none"]), "", "## Minority findings kept for later", ""]
    minority = [c for c in result["clusters"] if c["key"] not in result["top3"]]
    out += ["| Key | Support | Strategists | Proposed solution |", "|---|---|---|---|"]
    out += [f"| `{c['key']}` | {c['support']}/{count} | {', '.join(c['supporters'])} | "
            f"{cell(c['solutions'][0][1] if c['solutions'] else '-')} |" for c in minority]
    out += ["", "## Recurring problems across generations", ""]
    repeated = [r for r in rows if len(r["generations"]) > 1]
    if repeated:
        out += ["| Key | Generations | Total support | Latest proposed solution |",
                "|---|---|---|---|"]
        out += [f"| `{r['key']}` | {', '.join(f'g{g}' for g in r['generations'])} | "
                f"{r['support_total']} | {cell(r['latest_solution'] or '-')} |" for r in repeated]
    else:
        out.append("No unselected finding has recurred across generations yet.")
    kept = []
    for item in plan["strategists"]:
        found = evidence[item["slug"]]
        used = [c["key"] for c in result["clusters"]
                if c["key"] in result["top3"] and item["slug"] in c["implemented_by"]]
        if found["new_commits"]:
            role = f"source for {', '.join(used)}" if used else "minority work"
            kept.append(f"- `{found['branch']}` ({cell(item['name'])}): {role}; kept, never "
                        "deleted by the kit")
    out += ["", "## Branches kept for the owner", "", *(kept or ["- none with new commits"])]
    problems = [f"- {slug}: {p}" for slug, data in result["strategists"].items()
                for p in data["problems"]]
    out += ["", "## Report format problems", "", *(problems or ["- none"]), ""]
    return "\n".join(out)


def integrator_values(cfg: Config, plan: dict[str, Any], result: dict[str, Any],
                      baseline: dict[str, Any]) -> dict[str, str]:
    gen, count = plan["generation"], result["strategist_count"]
    folder = gen_dir(cfg, gen)
    names = {item["slug"]: item["name"] for item in plan["strategists"]}
    evidence = result["evidence"]
    top = [c for c in result["clusters"] if c["key"] in result["top3"]]
    features: list[str] = []
    sources: list[str] = []
    for number, c in enumerate(top, 1):
        status = "majority" if c["majority"] else "majority-like: below the majority threshold"
        spec = c["specs"][0][1] if c["specs"] else ""
        features.append(f"{number}. `{c['key']}` - {c['support']} of {count} strategists "
                        f"({status}). {spec}".rstrip())
        features += [f"   - {names.get(s, s)}: {sol}" for s, sol in c["solutions"]]
        if not c["implemented_by"]:
            sources.append(f"- `{c['key']}`: nobody implemented it; build it from the proposals.")
        for slug, how in c["implemented_by"].items():
            found = evidence[slug]
            good = [x["sha"][:12] for x in found["claimed_commits"] if x["on_branch"]]
            bad = [x["sha"][:12] for x in found["claimed_commits"] if not x["on_branch"]]
            line = (f"- `{c['key']}` ({how}) by {names.get(slug, slug)}: branch "
                    f"`{found['branch']}` at `{(found['head'] or 'missing')[:12]}`, commits "
                    f"{', '.join(good) or 'none verified on the branch'}")
            if bad:
                line += f"; claimed but NOT on the branch, do not trust: {', '.join(bad)}"
            sources.append(line)
    notes = ["ORCHESTRATOR: before launching the integrator, replace this list with exactly how "
             "the pieces fit together where they meet (shared files, conflicting designs, "
             "ordering)."]
    for c in top:
        if len(c["implemented_by"]) > 1:
            who = ", ".join(names.get(s, s) for s in c["implemented_by"])
            notes.append(f"- `{c['key']}` has {len(c['implemented_by'])} implementations "
                         f"({who}): keep one coherent design and the strongest tests of each.")
    for slug in names:
        features_by = [c["key"] for c in top if slug in c["implemented_by"]]
        if len(features_by) > 1:
            notes.append(f"- {names[slug]} implemented {', '.join(features_by)} together: "
                         "its commits may already combine them.")
    excluded = [f"- `{c['key']}` ({c['support']} of {count}) by {names.get(s, s)} on "
                f"`{evidence[s]['branch']}`: excluded this generation, kept for the owner."
                for c in result["clusters"] if c["key"] not in result["top3"]
                for s in c["implemented_by"]]
    return {
        **common_values(cfg, plan, baseline),
        "BASE_COMMIT": result["integration_head"],
        "INTEGRATOR_BRANCH": f"{cfg.prefix}/g{gen}-integration",
        "INTEGRATOR_WORKTREE": str(cfg.state / "worktrees" / f"g{gen}" / "integrator"),
        "SCRATCH": str(folder / "scratch" / "integrator"),
        "REPORT": str(folder / "INTEGRATION.md"),
        "DECISION": decision_text(result),
        "CONSENSUS_FEATURES": "\n".join(features) or "No consensus features: nothing to build.",
        "SOURCE_COMMITS": "\n".join(sources) or "- none",
        "RECONCILIATION": "\n".join(notes),
        "EXCLUDED_MINORITY": "\n".join(excluded) or "- no other implemented work this generation",
    }


def cmd_tally(cfg: Config, args: argparse.Namespace) -> int:
    plan = load_plan(cfg, args.gen)
    folder = gen_dir(cfg, args.gen)
    reports: dict[str, dict[str, Any]] = {}
    missing = []
    for item in plan["strategists"]:
        path = Path(item["report"])
        if path.is_file():
            reports[item["slug"]] = parse_report(path.read_text(encoding="utf-8", errors="replace"))
        else:
            missing.append(item["slug"])
    require(not missing or args.allow_missing,
            f"{len(missing)} of {len(plan['strategists'])} reports are missing "
            f"({', '.join(missing)}): wait for them, or if status shows them dead, re-run the "
            "whole generation (resume --apply). --allow-missing tallies anyway and says so.")
    baseline = load_baseline(cfg)
    require(baseline, "no baseline recorded: run baseline --apply first")
    assert baseline is not None
    result = build_tally(plan, reports, load_aliases(folder / "aliases.json"), missing,
                         integration_head(cfg))
    result["evidence"] = branch_evidence(cfg, plan, reports)
    rows = recurring(cfg, args.gen, result)
    result["recurring"] = rows[:50]
    templates = load_templates(cfg)
    brief = fill(templates["integrator-brief.md"],
                 integrator_values(cfg, plan, result, baseline), "integrator-brief.md")
    tally_md = render_tally(plan, result, rows)
    print(decision_text(result))
    steps = [f"write {cfg.rel(folder / 'TALLY.md')} (a draft the orchestrator finalizes)",
             f"write {cfg.rel(folder / 'tally.json')}",
             f"write {cfg.rel(folder / 'integrator-brief.md')} (edit its reconciliation first)"]
    show_plan(f"tally generation {args.gen}", steps, args.apply)
    if args.apply:
        write_text(cfg, folder / "TALLY.md", tally_md)
        write_text(cfg, folder / "tally.json", dump_json(result))
        write_text(cfg, folder / "integrator-brief.md", brief)
        print(f"APPLIED: generation {args.gen} tallied")
    return 0


def last_activity(paths: list[Path]) -> float | None:
    """Newest modification time under the given paths (bounded, skips .git and caches)."""
    newest: float | None = None
    seen = 0
    for root in paths:
        if not root.exists():
            continue
        candidates = [root.stat().st_mtime]
        if root.is_dir():
            for dirpath, dirnames, filenames in os.walk(root):
                dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
                for name in filenames:
                    try:
                        candidates.append(os.lstat(Path(dirpath, name)).st_mtime)
                    except OSError:
                        continue
                    seen += 1
                if seen > WALK_CAP:
                    break
        top = max(candidates)
        newest = top if newest is None else max(newest, top)
    return newest


def gen_status(cfg: Config, gen: int) -> dict[str, Any]:
    folder = gen_dir(cfg, gen)
    plan = read_json(folder / "plan.json") if (folder / "plan.json").is_file() else None
    status: dict[str, Any] = {"generation": gen, "planned": plan is not None}
    if plan is None:
        return status
    now = time.time()
    limit = cfg.stale_minutes * 60
    people = []
    for item in plan["strategists"]:
        worktree, report = Path(item["worktree"]), Path(item["report"])
        if report.is_file():
            state = "reported"
        elif not worktree.is_dir():
            state = "not-started"
        else:
            active = last_activity([worktree, Path(item["scratch"])])
            state = "dead" if active is None or now - active > limit else "working"
        people.append({"slug": item["slug"], "state": state,
                       "brief": Path(item["brief"]).is_file()})
    integrator: dict[str, Any] = {"state": "not-started"}
    record = folder / "integrator.json"
    if record.is_file():
        entry = read_json(record)["entries"][0]
        if (folder / "INTEGRATION.md").is_file():
            integrator = {"state": "reported"}
        else:
            active = last_activity([Path(entry["worktree"]), Path(entry["scratch"])])
            dead = active is None or now - active > limit
            integrator = {"state": "dead" if dead else "working"}
    status.update({
        "strategists": len(people),
        "briefs": sum(1 for p in people if p["brief"]),
        "worktrees": (folder / "worktrees.json").is_file(),
        "reports": sum(1 for p in people if p["state"] == "reported"),
        "dead": [p["slug"] for p in people if p["state"] == "dead"],
        "working": [p["slug"] for p in people if p["state"] == "working"],
        "marker": (cfg.state / "markers" / f"g{gen}.json").is_file(),
        "tally": (folder / "tally.json").is_file(),
        "integrator": integrator["state"],
        "recorded": (folder / "record.json").is_file(),
    })
    return status


def next_action(cfg: Config, statuses: list[dict[str, Any]], stopped: bool) -> str:
    if stopped:
        return "Stopped by the owner: start nothing new. Run resume --apply when told to continue."
    if load_baseline(cfg) is None:
        return "Record the baseline: baseline --apply"
    if not statuses:
        return "Plan generation 1: plan 1 --apply"
    s = statuses[-1]
    gen = s["generation"]
    if not s["planned"]:
        return f"plan {gen} --apply"
    if s["briefs"] < s["strategists"]:
        return f"render {gen} --apply"
    if not s["worktrees"]:
        return f"worktrees {gen} --apply"
    if not s["marker"]:
        return f"audit g{gen} --mark --apply, then launch all {s['strategists']} strategists"
    if s["reports"] < s["strategists"]:
        if s["dead"]:
            return (f"Interrupted: {', '.join(s['dead'])} left no report and no recent writes. "
                    f"resume --apply archives generation {gen}; then plan, render and create "
                    "worktrees again from the current head. Never count interrupted work.")
        return (f"Wait for reports ({s['reports']}/{s['strategists']}); launch any strategist "
                "that has not started.")
    if not s["tally"]:
        return f"tally {gen} --apply, then finalize TALLY.md"
    if s["integrator"] == "not-started":
        return f"worktrees {gen} --integrator --apply, then launch the integrator"
    if s["integrator"] == "working":
        return "Wait for the integrator's INTEGRATION.md."
    if s["integrator"] == "dead":
        return (f"The integrator left no report and no recent writes: resume --apply moves its "
                f"worktree aside; then worktrees {gen} --integrator --apply and relaunch it.")
    if not s["recorded"]:
        return (f"Verify independently: baseline --at <integrator worktree> --label g{gen}-verify "
                f"--apply and audit g{gen}; only then fast-forward {cfg.integration_branch}, "
                f"then record {gen} --commit <sha> --summary '...' --apply")
    return f"Plan the next generation: plan {gen + 1} --apply"


def cmd_status(cfg: Config, args: argparse.Namespace) -> int:
    ensure_initialized(cfg)
    stop_path = cfg.state / "STOP"
    stopped = stop_path.exists()
    statuses = [gen_status(cfg, gen) for gen in generations(cfg)]
    head = commit_of(cfg.project, f"refs/heads/{cfg.integration_branch}")
    baseline = load_baseline(cfg)
    report = {
        "project": cfg.name,
        "integration_branch": cfg.integration_branch,
        "integration_head": head,
        "stop_requested": stopped,
        "stop_reason": stop_path.read_text(encoding="utf-8").strip() if stopped else None,
        "baseline": None if baseline is None else {
            "head": baseline["head"], "passed": baseline["passed"],
            "recorded_at": baseline["recorded_at"]},
        "generations": statuses,
        "interrupted_archives": sorted(p.name for p in cfg.state.glob("g*-interrupted-*")),
        "next": next_action(cfg, statuses, stopped),
    }
    if args.json:
        print(dump_json(report), end="")
        return 0
    print(f"{cfg.name}: {cfg.integration_branch} at {(head or 'missing')[:12]}")
    print(f"STOP: {'REQUESTED - ' + str(report['stop_reason']) if stopped else 'not requested'}")
    if baseline:
        print(f"Baseline: {'all passing' if baseline['passed'] else 'FAILING'} at "
              f"{baseline['head'][:12]} ({baseline['recorded_at']})")
    for s in statuses:
        if not s["planned"]:
            print(f"  g{s['generation']}: not planned")
            continue
        print(f"  g{s['generation']}: briefs {s['briefs']}/{s['strategists']} - worktrees "
              f"{'yes' if s['worktrees'] else 'no'} - reports {s['reports']}/{s['strategists']}"
              f" - tally {'yes' if s['tally'] else 'no'} - integrator {s['integrator']} - "
              f"recorded {'yes' if s['recorded'] else 'no'}")
        if s["dead"]:
            print(f"      dead (no report, no writes for {cfg.stale_minutes}+ min): "
                  f"{', '.join(s['dead'])}")
        if s["working"]:
            print(f"      working: {', '.join(s['working'])}")
    for name in report["interrupted_archives"]:
        print(f"  {name}: archived interrupted attempt (never counted)")
    print(f"Next: {report['next']}")
    return 0


def snapshot_receipts(cfg: Config, folder: Path, sources: list[Path]) -> list[dict[str, Any]]:
    """Copy each source into folder/receipts once, read-only; never overwrite."""
    target_dir = folder / "receipts"
    make_dir(cfg, target_dir)
    entries = []
    for source in sources:
        data = source.read_bytes()
        target, number = target_dir / source.name, 2
        while target.exists() and target.read_bytes() != data:
            target = target_dir / f"{source.stem}-{number}{source.suffix}"
            number += 1
        if not target.exists():
            guard(cfg, target).write_bytes(data)
            target.chmod(0o444)
        entries.append({"file": cfg.rel(target), "sha256": sha256_bytes(data),
                        "bytes": len(data), "source": str(source)})
    index = target_dir / "receipts.json"
    write_text(cfg, index, dump_json({"schema": "improver-receipts/1", "receipts": entries}))
    index.chmod(0o444)
    return entries


def verified_commit(cfg: Config, commit: str, label: str,
                    marker: str) -> tuple[str, dict[str, Any], dict[str, Any]]:
    """The gate: verified at this exact commit, audit clean, already on the integration branch."""
    sha = commit_of(cfg.project, commit)
    require(sha, f"unknown commit {commit!r}")
    assert sha is not None
    require(is_ancestor(cfg.project, sha, integration_head(cfg)),
            f"{sha[:12]} is not on {cfg.integration_branch}: fast-forward only after independent "
            "verification and a clean audit, then record")
    verification = load_baseline(cfg, label)
    require(verification, f"no verification '{label}': run baseline --at <checkout of "
                          f"{sha[:12]}> --label {label} --apply")
    assert verification is not None
    require(verification["head"] == sha, f"verification '{label}' ran at "
                                         f"{verification['head'][:12]}, not at {sha[:12]}")
    require(verification["passed"], f"verification '{label}' has failures; a load-sensitive "
                                    "failure counts only if a single rerun reproduces it")
    audit = run_audit(cfg, marker)
    require(audit["clean"], f"protected paths changed since marker '{marker}': "
                            + "; ".join(audit["findings"][:5]))
    return sha, verification, audit


def append_history(cfg: Config, entry: str) -> None:
    path = cfg.state / "history.md"
    current = path.read_text(encoding="utf-8") if path.is_file() else ""
    write_text(cfg, path, (current.rstrip() + "\n\n" if current.strip() else "") + entry + "\n")


def cmd_record(cfg: Config, args: argparse.Namespace) -> int:
    plan = load_plan(cfg, args.gen)
    gen = args.gen
    folder = gen_dir(cfg, gen)
    require((folder / "tally.json").is_file(), f"run tally {gen} --apply first")
    require(not (folder / "record.json").exists(),
            f"generation {gen} is already recorded; receipts are immutable")
    label = args.verify_label or f"g{gen}-verify"
    sha, verification, audit = verified_commit(cfg, args.commit, label, f"g{gen}")
    tally = read_json(folder / "tally.json")
    sources = [folder / "TALLY.md", folder / "tally.json",
               cfg.state / "baseline" / f"{label}.json"]
    if (folder / "INTEGRATION.md").is_file():
        sources.append(folder / "INTEGRATION.md")
    for extra in args.receipt:
        path = Path(extra).resolve()
        require(path.is_file(), f"--receipt: not a file: {path}")
        sources.append(path)
    counts = {c["key"]: c["support"] for c in tally["clusters"]}
    passed = sum(1 for item in verification["results"] if item["passed"])
    entry = "\n".join([
        f"## Generation {gen}: {sha[:12]} ({now_iso()[:10]})", "",
        f"- From `{plan['base'][:12]}` to `{sha[:12]}` on `{cfg.integration_branch}`.",
        "- Strategies (never reuse): " + ", ".join(
            f"{item['name']} ({item['slug']})" for item in plan["strategists"]) + ".",
        f"- Decision: {tally['decision']}; top 3: " + ", ".join(
            f"`{key}` {counts[key]}/{tally['strategist_count']}" for key in tally["top3"]) + ".",
        f"- Integrated: {args.summary.strip()}",
        f"- Verified: {label} {passed}/{len(verification['results'])} commands at "
        f"`{sha[:12]}`; protected-path audit clean since marker g{gen}.",
    ])
    steps = ["append this generation to history.md (the next briefs quote it)",
             f"snapshot {len(sources)} receipt(s) read-only into {cfg.rel(folder / 'receipts')}/",
             f"write {cfg.rel(folder / 'record.json')}",
             "re-render the living review (review/REVIEW.md, never a receipt)"]
    print(entry)
    show_plan(f"record generation {gen}", steps, args.apply)
    if args.apply:
        append_history(cfg, entry)
        receipts = snapshot_receipts(cfg, folder, sources)
        write_text(cfg, folder / "record.json", dump_json({
            "schema": "improver-record/1", "generation": gen, "commit": sha,
            "summary": args.summary.strip(), "verification": label, "audit": audit,
            "receipts": receipts, "recorded_at": now_iso()}))
        write_review(cfg)
        print(f"APPLIED: generation {gen} recorded at {sha[:12]}")
    return 0


def cmd_request(cfg: Config, args: argparse.Namespace) -> int:
    ensure_initialized(cfg)
    name = args.name
    require(SLUG.match(name), "request name: use lowercase-hyphenated words")
    folder = cfg.state / "requests" / name
    require(not (folder / "request.json").exists(), f"owner request {name!r} is already recorded")
    marker = args.marker or f"request-{name}"
    sha, verification, audit = verified_commit(cfg, args.commit, args.verify_label, marker)
    passed = sum(1 for item in verification["results"] if item["passed"])
    entry = "\n".join([
        f"## Owner request '{name}': {sha[:12]} ({now_iso()[:10]})", "",
        "- Delivered outside the vote by a dedicated implementer and merged onto "
        f"`{cfg.integration_branch}`; build on it, do not redo it.",
        f"- Changed: {args.summary.strip()}",
        f"- Verified: {args.verify_label} {passed}/{len(verification['results'])} commands at "
        f"`{sha[:12]}`; protected-path audit clean since marker {marker}.",
    ])
    source = cfg.state / "baseline" / f"{args.verify_label}.json"
    print(entry)
    show_plan(f"record owner request '{name}'",
              ["append the request to history.md", f"snapshot the verification into "
               f"{cfg.rel(folder / 'receipts')}/", f"write {cfg.rel(folder / 'request.json')}",
               "re-render the living review"], args.apply)
    if args.apply:
        append_history(cfg, entry)
        receipts = snapshot_receipts(cfg, folder, [source])
        write_text(cfg, folder / "request.json", dump_json({
            "schema": "improver-request/1", "name": name, "commit": sha,
            "summary": args.summary.strip(), "verification": args.verify_label,
            "audit": audit, "receipts": receipts, "recorded_at": now_iso()}))
        write_review(cfg)
        print(f"APPLIED: owner request '{name}' recorded")
    return 0


def review_text(cfg: Config) -> str:
    state = ensure_initialized(cfg)
    stop_path = cfg.state / "STOP"
    stopped = stop_path.exists()
    statuses = [gen_status(cfg, gen) for gen in generations(cfg)]
    head = commit_of(cfg.project, f"refs/heads/{cfg.integration_branch}") or "missing"
    rows = ["| Generation | Strategies | Decision (top 3) | Integrated | Verification |",
            "|---|---|---|---|---|"]
    kept: list[str] = []
    receipts: list[str] = []
    latest_recurring: list[dict[str, Any]] = []
    for gen in generations(cfg):
        folder = gen_dir(cfg, gen)
        if not (folder / "plan.json").is_file():
            continue
        plan = read_json(folder / "plan.json")
        tally = read_json(folder / "tally.json") if (folder / "tally.json").is_file() else None
        record = read_json(folder / "record.json") if (folder / "record.json").is_file() else None
        decision = "-"
        if tally:
            support = {c["key"]: c["support"] for c in tally["clusters"]}
            decision = f"{tally['decision']}: " + ", ".join(
                f"`{k}` {support[k]}/{tally['strategist_count']}" for k in tally["top3"])
            latest_recurring = tally.get("recurring", [])
            for item in plan["strategists"]:
                found = tally["evidence"][item["slug"]]
                if found["new_commits"] and not any(
                        item["slug"] in c["implemented_by"] for c in tally["clusters"]
                        if c["key"] in tally["top3"]):
                    kept.append(f"- g{gen} `{found['branch']}` ({item['name']}): minority work, "
                                "verified by its strategist, kept for you")
        names = ", ".join(item["slug"] for item in plan["strategists"])
        integrated = f"`{record['commit'][:12]}` {cell(record['summary'])}" if record else "-"
        verified = f"{record['verification']}, audit clean" if record else "-"
        rows.append(f"| g{gen} | {names} | {cell(decision)} | {integrated} | {verified} |")
        if record:
            receipts += [f"- g{gen}: `{r['file']}` sha256 `{r['sha256'][:16]}`"
                         for r in record["receipts"]]
    requests = []
    for path in sorted((cfg.state / "requests").glob("*/request.json")):
        data = read_json(path)
        requests.append(f"- {data['name']}: `{data['commit'][:12]}` {data['summary']}")
        receipts += [f"- request {data['name']}: `{r['file']}` sha256 `{r['sha256'][:16]}`"
                     for r in data["receipts"]]
    recurring_rows = [r for r in latest_recurring if len(r["generations"]) > 1]
    recurring_text = "\n".join(
        f"- `{r['key']}`: seen in {', '.join(f'g{g}' for g in r['generations'])} "
        f"(total support {r['support_total']}): {r['latest_solution']}" for r in recurring_rows
    ) or "No unselected finding has recurred across generations yet."
    baseline = load_baseline(cfg)
    config_hint = f"python3 improver.py --config {cfg.file}"
    values = {
        "PROJECT_NAME": cfg.name,
        "UPDATED_AT": now_iso(),
        "STATUS": ("STOPPED: " + stop_path.read_text(encoding="utf-8").strip()) if stopped
        else "running (local only; nothing is pushed or published)",
        "NEXT_ACTION": next_action(cfg, statuses, stopped),
        "INTEGRATION_BRANCH": cfg.integration_branch,
        "INTEGRATION_HEAD": head[:12],
        "BASE_BRANCH": cfg.base_branch,
        "START_COMMIT": str(state.get("start_commit", ""))[:12],
        "LATEST_BASELINE": baseline_block(baseline) if baseline else "No baseline recorded yet.",
        "GENERATIONS": "\n".join(rows),
        "HISTORY": history_text(cfg),
        "OWNER_REQUESTS": "\n".join(requests) or "None yet.",
        "RECURRING": recurring_text,
        "KEPT_BRANCHES": "\n".join(kept) or "None yet.",
        "RECEIPTS": "\n".join(receipts) or "None yet.",
        "SWITCH_BACK": "\n".join([
            f"- Everything integrated is on `{cfg.integration_branch}`; your "
            f"`{cfg.base_branch}` branch is untouched.",
            f"- Try it: commit your own work, then `git switch {cfg.integration_branch}`.",
            f"- Go back: `git switch {cfg.base_branch}`.",
            f"- Compare: `git log --oneline {cfg.base_branch}..{cfg.integration_branch}`.",
        ]),
        "STOP_HOW": f"`{config_hint} stop --reason \"...\" --apply`, or create the file "
                    f"`{cfg.state / 'STOP'}`. Continue with `{config_hint} resume --apply`.",
    }
    return fill(load_templates(cfg)["review.md"], values, "review.md")


def write_review(cfg: Config) -> Path:
    path = cfg.state / "review" / "REVIEW.md"
    write_text(cfg, path, review_text(cfg))
    return path


def cmd_review(cfg: Config, args: argparse.Namespace) -> int:
    path = cfg.state / "review" / "REVIEW.md"
    body = review_text(cfg)
    show_plan("review", [f"write the living review {cfg.rel(path)} ({len(body)} characters)"],
              args.apply)
    if args.apply:
        write_review(cfg)
        print(f"APPLIED: {path}")
    return 0


def cmd_stop(cfg: Config, args: argparse.Namespace) -> int:
    ensure_initialized(cfg)
    path = cfg.state / "STOP"
    if path.exists():
        print(f"STOP is already requested: {path.read_text(encoding='utf-8').strip()}")
        return 0
    reason = (args.reason or "the owner asked to stop").strip()
    show_plan("stop", [f"create {cfg.rel(path)} ({reason})", "re-render the living review"],
              args.apply)
    if args.apply:
        write_text(cfg, path, f"{now_iso()} {reason}\n")
        write_review(cfg)
        print("APPLIED: the orchestrator starts nothing new until resume --apply")
    return 0


def next_suffix(cfg: Config, pattern: str) -> int:
    number = 1
    while list(cfg.state.glob(pattern.format(n=number))) or list(
            (cfg.state / "worktrees").glob(pattern.format(n=number))):
        number += 1
    return number


def cmd_resume(cfg: Config, args: argparse.Namespace) -> int:
    ensure_initialized(cfg)
    steps: list[str] = []
    moves: list[tuple[str, Path, Path]] = []
    renames: list[tuple[str, str]] = []
    stop = cfg.state / "STOP"
    if stop.exists():
        steps.append(f"remove {cfg.rel(stop)}")
    gens = generations(cfg)
    status = gen_status(cfg, gens[-1]) if gens else {"planned": False}
    if status["planned"]:
        gen = status["generation"]
        folder = gen_dir(cfg, gen)
        plan = read_json(folder / "plan.json")
        if status["reports"] < status["strategists"] and status["dead"]:
            k = next_suffix(cfg, f"g{gen}-interrupted-{{n}}")
            for item in plan["strategists"]:
                old = Path(item["worktree"])
                if old.is_dir():
                    archived = cfg.state / "worktrees" / f"g{gen}-interrupted-{k}" / item["slug"]
                    moves.append(("worktree", old, archived))
                if commit_of(cfg.project, f"refs/heads/{item['branch']}"):
                    renames.append((item["branch"], f"{item['branch']}-interrupted-{k}"))
            moves.append(("folder", folder, cfg.state / f"g{gen}-interrupted-{k}"))
            steps.append(f"generation {gen} was interrupted ({', '.join(status['dead'])} left no "
                         "report and no recent writes): archive it, never count it")
        elif status.get("integrator") == "dead":
            k = next_suffix(cfg, f"g{gen}-integrator-interrupted-{{n}}")
            entry = read_json(folder / "integrator.json")["entries"][0]
            moves.append(("worktree", Path(entry["worktree"]),
                          cfg.state / "worktrees" / f"g{gen}-integrator-interrupted-{k}"))
            renames.append((entry["branch"], f"{entry['branch']}-interrupted-{k}"))
            moves.append(("folder", folder / "integrator.json",
                          folder / f"integrator-interrupted-{k}.json"))
            steps.append(f"the generation {gen} integrator left no report and no recent writes")
    for kind, old, new in moves:
        verb = "git worktree move" if kind == "worktree" else "move"
        steps.append(f"{verb} {old} -> {new}")
    steps += [f"git branch -m {old} {new}" for old, new in renames]
    if moves:
        steps.append("then plan/render/worktrees again from the current integration head "
                     "(same strategies, fresh branches)")
    if steps:
        steps.append("re-render the living review")
    show_plan("resume", steps, args.apply)
    if not args.apply or not steps:
        return 0
    if stop.exists():
        guard(cfg, stop).unlink()
    for kind, old, new in moves:
        make_dir(cfg, new.parent)
        guard(cfg, new)
        if kind == "worktree":
            git(cfg.project, "worktree", "move", str(old), str(new))
        else:
            guard(cfg, old).rename(new)
    for old_branch, new_branch in renames:
        git(cfg.project, "branch", "-m", old_branch, new_branch)
    write_review(cfg)
    print("APPLIED: resumed")
    return 0


def positive(value: str) -> int:
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("generation numbers start at 1")
    return number


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="improver",
        description="Offline bookkeeping for the Autonomous Software Improvement Lab. "
                    "Mutating commands print a plan and change nothing without --apply.")
    parser.add_argument("--config", default=os.environ.get("IMPROVER_CONFIG",
                                                           "improver.config.json"))
    parser.add_argument("--version", action="version", version=f"improver {KIT_VERSION}")
    sub = parser.add_subparsers(dest="command", required=True)

    def command(name: str, summary: str, apply: bool = True) -> argparse.ArgumentParser:
        item = sub.add_parser(name, help=summary, description=summary)
        if apply:
            item.add_argument("--apply", action="store_true",
                              help="perform the plan (default: print it only)")
        return item

    command("init", "validate the config and create the state directory")
    item = command("baseline", "run the named verify commands and record the results")
    item.add_argument("--label", default="latest")
    item.add_argument("--at", help="another checkout of the project, e.g. the integrator worktree")
    item.add_argument("--only", nargs="+", metavar="NAME")
    item.add_argument("--keep-homes", action="store_true")
    item = command("plan", "pick N never-used strategies, seeded and reproducible")
    item.add_argument("gen", type=positive)
    item.add_argument("--replace", action="store_true")
    item = command("render", "fill the strategist briefs from the templates")
    item.add_argument("gen", type=positive)
    item = command("worktrees", "create one git worktree and branch per strategist")
    item.add_argument("gen", type=positive)
    item.add_argument("--integrator", action="store_true")
    item = command("audit", "mark or check protected paths (check is read-only)")
    item.add_argument("marker", help="marker label, e.g. g1 or request-dark-mode")
    item.add_argument("--mark", action="store_true")
    item.add_argument("--json", action="store_true")
    item = command("tally", "parse the reports and draft TALLY.md and the integrator brief")
    item.add_argument("gen", type=positive)
    item.add_argument("--allow-missing", action="store_true")
    item = command("record", "record a verified, fast-forwarded generation")
    item.add_argument("gen", type=positive)
    item.add_argument("--commit", required=True)
    item.add_argument("--summary", required=True)
    item.add_argument("--verify-label")
    item.add_argument("--receipt", action="append", default=[])
    item = command("request", "record a verified owner request delivered outside the vote")
    item.add_argument("name")
    item.add_argument("--commit", required=True)
    item.add_argument("--summary", required=True)
    item.add_argument("--verify-label", required=True)
    item.add_argument("--marker")
    item = command("status", "show per-generation state and the next action", apply=False)
    item.add_argument("--json", action="store_true")
    command("review", "re-render the living review document")
    item = command("stop", "ask the orchestrator to stop (creates the STOP file)")
    item.add_argument("--reason")
    command("resume", "clear STOP and archive an interrupted generation")
    return parser


COMMANDS = {
    "init": cmd_init, "baseline": cmd_baseline, "plan": cmd_plan, "render": cmd_render,
    "worktrees": cmd_worktrees, "audit": cmd_audit, "tally": cmd_tally, "record": cmd_record,
    "request": cmd_request, "status": cmd_status, "review": cmd_review, "stop": cmd_stop,
    "resume": cmd_resume,
}


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return COMMANDS[args.command](Config(Path(args.config)), args)
    except KitError as exc:
        print(f"improver: refused: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
