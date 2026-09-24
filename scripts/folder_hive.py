#!/usr/bin/env python3
"""Turn each RAPP Work starter into an inert folder-Hive template and an organism map.

    python3 -B scripts/folder_hive.py                    summarize every starter's template
    python3 -B scripts/folder_hive.py --check            rebuild twice; refuse drift or a rule break
    python3 -B scripts/folder_hive.py --slug S --out DIR write one template tree into a new folder

A template follows the Hive folder convention (HIVE-MD, experimental): `HIVE.md`, `.gitattributes`
and `shared/<room>/` markdown files. It is data, not a Hive: `hive:` stays empty until a founder's
Brainstem creates the Hive with the Hive agent. Nothing here runs, signs, or creates keys.
Standard library only; the output depends only on the starter's blueprint and files.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# The rules below restate the subset of the Hive folder convention a template must obey. Source:
# kody-w/rapp-model-hive, branch experimental/hive-md, agents/hive_agent.py. The tests compare
# every restated rule with that exact file when a pinned copy is present.
CONVENTION = {
    "repository": "https://github.com/kody-w/rapp-model-hive",
    "branch": "experimental/hive-md",
    "commit": "2bd7c95152ede719b6418b80e2bdc2cd457bf711",
    "convention": "HIVE-MD.md",
    "convention_sha256": "f3186e0d88cc36e18582171fff4ed9a68feddc4ae316f66fb8acc2982892fd96",
    "agent": "agents/hive_agent.py",
    "agent_sha256": "e9a2d7243da31fd2388f140bb8138c3d8d2db428ad09075530eb049a0355e8dd",
}
ATTRS = b"* text eol=lf\n"
TOPS = ("members", "requests", "shared", "former")
INSTRUCTION_NAMES = {
    "agents.md", "claude.md", "claude.local.md", "gemini.md", "skill.md", "copilot-instructions.md"}
RESERVED = {"con", "prn", "aux", "nul", *(f"com{i}" for i in range(1, 10)),
            *(f"lpt{i}" for i in range(1, 10))}
SEGMENT = re.compile(r"[A-Za-z0-9][A-Za-z0-9 ._-]{0,63}")
PERSON = re.compile(r"[a-z0-9][a-z0-9-]{0,31}")
FORMER = re.compile(r"[a-z0-9][a-z0-9-]{0,31}(-([2-9]|[1-9][0-9]))?")
BAD_TEXT = re.compile(
    "[\x00-\x08\x0b-\x1f\x7f-\x9f\ud800-\udfff\xad\u034f\u061c\u115f\u1160\u17b4\u17b5\u180b-\u180f"
    "\u200b-\u200f\u2028-\u202e\u2060-\u206f\u3164\ufe00-\ufe0f\ufeff\uffa0\ufff0-\ufffb"
    "\ufdd0-\ufdef\ue000-\uf8ff\U00013430-\U0001343f\U0001bca0-\U0001bca3\U0001d173-\U0001d17a"
    "\U000e0000-\U000e0fff\U000f0000-\U0010ffff"
    + "".join(chr(plane << 16 | 0xFFFE) + chr(plane << 16 | 0xFFFF) for plane in range(15)) + "]")
EMOJI = ("\u00a9\u00ae\u203c\u2049\u2122\u2139\u2194-\u21aa\u231a-\u23ff\u24c2\u25aa-\u25fe"
         "\u2600-\u27bf\u2934\u2935\u2b05-\u2b55\u3030\u303d\u3297\u3299\U0001f000-\U0001faff")
EMOJI_OK = re.compile(f"(?<=[{EMOJI}])[\ufe0e\ufe0f]|(?<=[0-9#*])\ufe0f(?=\u20e3)"
                      f"|(?:(?<=[{EMOJI}])|(?<=[{EMOJI}]\ufe0f))\u200d(?=[{EMOJI}])")
DATAVIEWJS = re.compile(r"^[ \t>*+\-0-9.)]*(`{3,}|~{3,})[ \t]*dataviewjs|`+[ \t]*\$=", re.M | re.I)
LINK = re.compile(r"\[\[([^\]|#\n]+)")
MAX_FILE, MAX_PATH, MAX_MEMBER_PATH = 1 << 20, 120, 116

ROOM_ROOT = "folder-hive"
CASEWORK = "casework"
APPROVALS = 2
FIELDS = "id=id; title=title; status=status; owner=owner,assignee; depends on=depends_on"
ECOSYSTEM_URL = (
    "https://github.com/kody-w/rapp-work/blob/experimental/rapp-work-constitution/ECOSYSTEM.md"
)
CONSTITUTION_URL = (
    "https://github.com/kody-w/rapp-work/blob/experimental/rapp-work-constitution/CONSTITUTION.md"
)
CONVENTION_URL = "https://github.com/kody-w/rapp-model-hive/blob/experimental/hive-md/HIVE-MD.md"


def name_refusal(path: str) -> str | None:
    """Why the convention refuses this file name in a Hive tree (HIVE-MD `name_rules`)."""
    parts = path.split("/")
    if path in ("HIVE.md", ".gitattributes"):
        return None
    if (parts[0] not in TOPS or len(parts) < 3 or not path.endswith(".md") or len(path) > MAX_PATH
            or parts[0] == "members" and len(path) > MAX_MEMBER_PATH):
        return "files sit in a folder under members/, requests/, shared/ or former/, end in .md"
    for part in parts:
        if (not SEGMENT.fullmatch(part) or part[-1] in " ."
                or part.split(".")[0].rstrip(" ").lower() in RESERVED
                or part.lower() in INSTRUCTION_NAMES):
            return "names use portable characters and are never an AI instruction file name"
    if ((parts[0] in ("members", "requests") and not PERSON.fullmatch(parts[1]))
            or (parts[0] == "former" and not FORMER.fullmatch(parts[1]))
            or (parts[0] == "requests"
                and (len(parts) != 3 or not PERSON.fullmatch(parts[2][:-3])))
            or (parts[0] == "members" and parts[2] == "keys"
                and (len(parts) != 4 or not PERSON.fullmatch(parts[3][:-3])))):
        return "person and device names are lowercase letters, digits and dashes"
    return None


def text_refusal(path: str, data: bytes) -> str | None:
    """Why the convention refuses these bytes at `path` (HIVE-MD `text_rules` and file size)."""
    why = name_refusal(path)
    if why:
        return why
    if path == ".gitattributes":
        return None if data == ATTRS else ".gitattributes must be exactly `* text eol=lf`"
    if len(data) > MAX_FILE:
        return "files are at most 1 MB"
    text = data.decode("utf-8", "replace")
    if "\ufffd" in text or BAD_TEXT.search(EMOJI_OK.sub("", text)):
        return "only UTF-8 text, without control, bidi, invisible or private-use characters"
    if DATAVIEWJS.search(text):
        return "no dataviewjs blocks or `$=` inline code"
    return None


def tree_refusal(paths: list[str]) -> str | None:
    """Case-only collisions, which the convention refuses anywhere in a tree."""
    seen: dict[str, str] = {}
    for parts in (path.split("/") for path in paths):
        for name in ("/".join(parts[:index]) for index in range(1, len(parts) + 1)):
            first = seen.setdefault(name.casefold(), name)
            if first != name:
                return f"`{name}` and `{first}` differ only by case"
    return None


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


PLAIN_SCALAR = re.compile(r"[A-Za-z0-9(][^\n\t]*")
YAML_SPECIAL = re.compile(
    r"(?i:true|false|yes|no|on|off|null|~|y|n)|[-+]?(?:\d[\d_]*|\.\d+|\d[\d_]*\.\d*)(?:e[-+]?\d+)?"
    r"|0x[0-9a-f]+|0o[0-7]+|[-+]?\.(?:inf|nan)|\d{4}-\d\d-\d\d.*"
)


def scalar(value: str) -> str:
    """One YAML scalar: plain when that is unambiguous, otherwise a JSON (YAML) quoted string."""
    if (PLAIN_SCALAR.fullmatch(value) and not YAML_SPECIAL.fullmatch(value)
            and ": " not in value and " #" not in value and not value.endswith((":", " "))):
        return value
    return json.dumps(value, ensure_ascii=False)


def frontmatter(pairs: list[tuple[str, str | int | list[str]]]) -> str:
    lines = ["---"]
    for key, value in pairs:
        if isinstance(value, list):
            lines.append(f"{key}: []" if not value else f"{key}:")
            lines.extend(f"  - {scalar(item)}" for item in value)
        elif isinstance(value, int):
            lines.append(f"{key}: {value}")
        else:
            lines.append(f"{key}:" if value == "" else f"{key}: {scalar(value)}")
    return "\n".join([*lines, "---", ""]) + "\n"


def fenced(text: str) -> str:
    """Non-markdown text as one fence longer than any backtick run in it (as the Hive agent does)."""
    fence = "`" * max(3, 1 + max(map(len, re.findall("`+", text)), default=0))
    body = text[:-1] if text.endswith("\n") else text
    return f"{fence}\n{body}\n{fence}\n"


def _note(path: str) -> str:
    return path.rsplit("/", 1)[-1].removesuffix(".md")


def _claim(path: str, notes: dict[str, str], paths: set[str]) -> str:
    """The first free name, using the convention's rule for a taken name: -2, -3, ...

    Note names must be unique across the tree, because note apps and the Hive agent resolve a
    [[link]] by name alone."""
    stem, number, candidate = path.removesuffix(".md"), 1, path
    while _note(candidate).casefold() in notes or candidate.casefold() in paths:
        number += 1
        candidate = f"{stem}-{number}.md"
    notes[_note(candidate).casefold()] = candidate
    paths.add(candidate.casefold())
    return candidate


def _holder(name: str, notes: dict[str, str]) -> str:
    return f"`{notes[name.casefold()]}`"


def _team_index(blueprint: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {team["slug"]: team for team in blueprint["teams"]}


def build_template(
    blueprint: dict[str, Any], source_files: dict[str, bytes]
) -> tuple[dict[str, bytes], list[str]]:
    """The template tree (paths relative to the template root) and plain mapping notes."""
    slug, case = blueprint["slug"], blueprint["case"]
    teams = _team_index(blueprint)
    tasks = {task["id"]: task for task in blueprint["tasks"]}
    notes_taken: dict[str, str] = {}
    paths_taken: set[str] = {"hive.md", ".gitattributes"}
    notes: list[str] = []
    task_paths = {
        task_id: _claim(f"shared/{task['team']}/{task_id}.md", notes_taken, paths_taken)
        for task_id, task in tasks.items()
    }
    for wanted, label in ((f"shared/{CASEWORK}/{case['id']}.md", "The case intake"),
                          (f"shared/{CASEWORK}/{slug}.md", "The charter")):
        if _note(wanted).casefold() in notes_taken or wanted.casefold() in paths_taken:
            notes.append(f"{label} shares its note name with {_holder(_note(wanted), notes_taken)}, "
                         "so it takes the next free name (the convention's rule for a taken name).")
    case_path = _claim(f"shared/{CASEWORK}/{case['id']}.md", notes_taken, paths_taken)
    charter_path = _claim(f"shared/{CASEWORK}/{slug}.md", notes_taken, paths_taken)
    artifact_paths: dict[str, str] = {}
    for relative in blueprint["files"]:
        wanted = f"shared/{CASEWORK}/artifacts/{relative}"
        wanted += "" if relative.endswith(".md") else ".md"
        holder = (_holder(_note(wanted), notes_taken)
                  if _note(wanted).casefold() in notes_taken else None)
        claimed = _claim(wanted, notes_taken, paths_taken)
        artifact_paths[relative] = claimed
        if claimed != wanted:
            notes.append(
                f"The starter file `{relative}` has the same note name as {holder}, and note apps "
                "and the Hive agent resolve [[links]] by name alone, so its note is "
                f"`{claimed.rsplit('/', 1)[-1]}` (the convention's rule for a taken name).")

    def artifact_link(relative: str) -> str:
        return f"`{relative}`: [[{_note(artifact_paths[relative])}]]"

    producers = {output: task["id"] for task in blueprint["tasks"] for output in task["outputs"]}

    def input_line(item: str) -> str:
        if item in artifact_paths:
            return f"- {artifact_link(item)}"
        return f"- `{item}`, from [[{_note(task_paths[producers[item]])}]]"

    files: dict[str, str] = {}
    rooms = [team["slug"] for team in blueprint["teams"]]
    for task in blueprint["tasks"]:
        team = teams[task["team"]]
        links = [f"[[{_note(task_paths[item])}]]" for item in task["depends_on"]]
        status = "ready" if not task["depends_on"] else "blocked"
        after = ("Ready to claim: it depends on nothing." if not links
                 else "Blocked until " + ", ".join(links) + " " + ("is" if len(links) == 1 else "are")
                 + " done.")
        body = [
            f"# {task['title']}",
            "",
            f"Room `{team['slug']}` ({team['role']}). {after}",
            "",
            task["instructions"],
            "",
            "## Inputs",
            "",
            *map(input_line, task["inputs"]),
            "",
            "## Outputs",
            "",
            *(f"- `{output}`" for output in task["outputs"]),
            "",
            "## Acceptance",
            "",
            *(f"- {item}" for item in task["acceptance"]),
            "",
        ]
        files[task_paths[task["id"]]] = frontmatter(
            [("id", task["id"]), ("title", task["title"]), ("status", status),
             ("depends_on", list(task["depends_on"]))]
        ) + "\n".join(body)
    by_room = [
        f"- [[{_note(task_paths[task['id']])}]] {task['title']} (`{task['team']}`, "
        + ("ready" if not task["depends_on"] else "blocked") + ")"
        for room in rooms for task in blueprint["tasks"] if task["team"] == room
    ]
    files[case_path] = frontmatter([("id", case["id"]), ("title", case["title"])]) + "\n".join([
        f"# {case['title']}",
        "",
        case["brief"],
        "",
        "## Inputs",
        "",
        *(f"- {artifact_link(item)}" for item in case["inputs"]),
        "",
        "## Success criteria",
        "",
        *(f"- {item}" for item in case["success_criteria"]),
        "",
        "## Tasks",
        "",
        *by_room,
        "",
        "No reference artifact counts as completed work without review.",
        "",
    ])
    related = ", ".join(f"`{item}`" for item in blueprint["related_seeds"])
    files[charter_path] = frontmatter([("title", blueprint["name"])]) + "\n".join([
        f"# {blueprint['name']}",
        "",
        blueprint["tagline"],
        "",
        blueprint["mission"],
        "",
        "## Rooms",
        "",
        *(f"- `shared/{team['slug']}/`: {team['role']}. {team['purpose']}"
          for team in blueprint["teams"]),
        f"- `shared/{CASEWORK}/`: the shared delivery case. Its intake is "
        f"[[{_note(case_path)}]]; shared inputs sit in `artifacts/`; accepted deliverables land "
        "here too.",
        "",
        *([f"Related starters, for discovery only (never shared membership): {related}.", ""]
          if related else []),
        "All names, estimates and observations are synthetic public starter data.",
        "",
    ])
    rendered = {path: text.encode("utf-8") for path, text in files.items()}
    for relative, path in artifact_paths.items():
        data = source_files[relative]
        head = frontmatter([
            ("seed_file", f"templates/casework/work/starter/{relative}"),
            ("seed_sha256", sha(data)),
        ])
        text = data.decode("utf-8")
        rendered[path] = (head + (text if relative.endswith(".md") else fenced(text))).encode()
    fenced_count = sum(1 for relative in artifact_paths if not relative.endswith(".md"))
    room_list = ", ".join(f"`shared/{room}/`" for room in rooms)
    hive_body = "\n".join([
        f"# {blueprint['name']}",
        "",
        f"A folder-Hive template made from the RAPP Hive Hub starter `{slug}`. It is not a Hive "
        "yet: `hive:` stays empty on purpose. A founder's Brainstem creates the Hive with the Hive "
        f"agent, which gives it a fresh id, starts it at {APPROVALS} approvals, keeps the "
        "`fields:` hint above, and signs the founder's key file into `members/`. Nothing in this "
        "folder runs.",
        "",
        f"- Charter: [[{_note(charter_path)}]]",
        f"- First case: [[{_note(case_path)}]]",
        f"- Rooms: {room_list} and `shared/{CASEWORK}/`",
        "",
        "`members/`, `requests/` and `former/` appear as people join and leave. This template "
        "holds no keys, members or real ids.",
        "",
    ])
    rendered["HIVE.md"] = (
        frontmatter([("hive", ""), ("version", 1), ("approvals", APPROVALS),
                     ("fields", FIELDS)]) + hive_body
    ).encode("utf-8")
    rendered[".gitattributes"] = ATTRS
    kept: dict[str, bytes] = {}
    for path in sorted(rendered):
        why = text_refusal(path, rendered[path])
        if why is None:
            kept[path] = rendered[path]
            continue
        source = next((rel for rel, claimed in artifact_paths.items() if claimed == path), path)
        notes.append(f"`{source}` is left out of the template: {why}.")
    why = tree_refusal(sorted(kept))
    if why:
        raise ValueError(f"{slug}: template tree refused: {why}")
    partner_briefs = [relative for relative in blueprint["files"]
                      if Path(relative).stem in blueprint["related_seeds"]]
    if partner_briefs:
        notes.append(
            "Partner briefs for other starters (" + ", ".join(f"`{item}`" for item in partner_briefs)
            + ") are data in this Hive. Working with another organization's Hive needs signed "
            "agreements under rapp-federation/1 (candidate), and dial records do not describe "
            "folder Hives yet (G12), so that part of the case stays outside the folder Hive.")
    notes.extend([
        f"{fenced_count} of {len(artifact_paths)} starter files are not markdown, so they sit in "
        "`shared/casework/artifacts/` as fenced markdown notes named `<file>.md`; `seed_file` and "
        "`seed_sha256` name the exact package file. In a Hive they are data: run or edit the "
        "originals from the ZIP or a workspace.",
        "Task outputs are logical `deliverables/` paths. A folder Hive holds only markdown, so a "
        "team adds each finished output as a note (or keeps it in a workspace); the template "
        "creates none.",
        "The demonstration world id has no folder-Hive counterpart: a folder Hive has its own "
        "random `hive:` id and no world. The seed's unassigned tasks have no `owner` until a "
        "member claims one.",
    ])
    return kept, notes


LAYERS = (
    (0, "RAPP/1", "in force"),
    (1, "Estate", "in force"),
    (2, "Organization", "specified"),
    (3, "Hive", "in force: rapp-hive/1 Private Hive · experimental: folder Hive"),
    (4, "Your device", "in force: workspaces · experimental: Hive copies, references"),
    (5, "Brainstem", "in force"),
    (6, "You", "—"),
)


def organism_map(
    blueprint: dict[str, Any], template: dict[str, bytes], notes: list[str],
    dependencies: dict[str, Any],
) -> dict[str, Any]:
    teams = len(blueprint["teams"])
    rapp1 = dependencies["protocol"]["commit"][:7]
    sdk = dependencies["sdk"]["commit"][:7]
    touches = [
        f"Its plans mint RAPP/1 RAPPIDs with the pinned reference (kody-w/rapp-1 at {rapp1}). The "
        "package itself holds no RAPPID, key or signature.",
        "Nothing: no registry entry, owner key or signature is included, and initialize.json "
        "says signed_estate_activation: false.",
        f"An Organization plan: one owner you choose, one world ({blueprint['world_id']}), "
        f"{teams} teams and one case. Canonical rapp-work/1 is specified; no estate has activated "
        "it yet (G16), and it cannot bind a folder Hive yet (G10). The SDK Organization that "
        "initialize.json plans is a pointer-only routing object (G11 proposes calling it a "
        "workspace index), not an activated organization.",
        "Today the one Hive an organization can hold is a rapp-hive/1 Private Hive; this package "
        "declares none, and its owner would create one under rapp-hive/1. Experimental option: "
        f"the folder-Hive template in {ROOM_ROOT}/, which a founder's Brainstem creates with the "
        "Hive agent.",
        f"Each member's scoped Workspaces from templates/ ({teams} teams plus casework), planned "
        f"with the pinned RAPP Work SDK (kody-w/rapp-work at {sdk}). The unzipped package is a "
        "reference: read as data, brought into a Hive only by signed copy.",
        "The boot Egg hatches a Brainstem with the SeedRunner organ (experimental), which runs "
        "the same SDK flow; the Hive agent, one file in a Brainstem, creates a folder Hive from "
        "the template.",
        "You choose the owner label and destination, and confirm every exact plan in a later "
        "turn.",
    ]
    rooms = [team["slug"] for team in blueprint["teams"]] + [CASEWORK]
    return {
        "schema": "hive-hub-organism-map/1",
        "status": "starter-package-not-activated",
        "layers": [
            {"layer": number, "name": name, "health": health, "touches": touches[number]}
            for number, name, health in LAYERS
        ],
        "across": [{
            "part": "Hive Mind",
            "health": "candidate",
            "touches": "Hive Hub finds and joins across Hives. This starter's Dial Record and join "
            "cards describe the package, not a live Hive; dial records do not describe folder "
            "Hives yet (G12). Transport carries; signatures decide.",
        }],
        "frozen": [{"id": "rapp-hive/2", "health": "frozen",
                    "note": "a research record; this starter does not use it"}],
        "folderHive": {
            "root": ROOM_ROOT,
            "health": "experimental",
            "hive": None,
            "approvals": APPROVALS,
            "fields": FIELDS,
            "rooms": rooms,
            "files": len(template),
            "tasks": len(blueprint["tasks"]),
            "artifacts": sum(1 for path in template if "/artifacts/" in path),
            "convention": CONVENTION,
            "notes": notes,
        },
        "sources": {
            "ecosystem": ECOSYSTEM_URL,
            "constitution": CONSTITUTION_URL,
            "convention": CONVENTION_URL,
        },
    }


def organism_markdown(blueprint: dict[str, Any], organism: dict[str, Any]) -> bytes:
    hive = organism["folderHive"]
    rooms = hive["rooms"]
    lines = [
        f"# Where this fits: {blueprint['name']}",
        "",
        "This package is a RAPP Work starter: synthetic public files that you read as data. It is "
        "not an activated organization, a Hive, a membership or a running service, and it grants "
        "no authority.",
        "",
        "## The stack, bottom to top",
        "",
        "| # | Layer | Health | What this starter touches |",
        "| --- | --- | --- | --- |",
        *(f"| {item['layer']} | {item['name']} | {item['health']} | {item['touches']} |"
          for item in organism["layers"]),
        "",
        *(f"Across: {item['part']} ({item['health']}). {item['touches']}"
          for item in organism["across"]),
        "",
        "`rapp-hive/2` is frozen as a research record; nothing here uses it.",
        "",
        "## Pull it down as a reference",
        "",
        "Download the ZIP, check its SHA-256 against the seed page, and unzip it into a new "
        "folder. That folder, like the seed folder in the repository, is a reference in its own "
        "shape: read-only, never run, and read as data. Nothing moves into a Hive until a member "
        "brings a piece of it in by one signed commit, stamped with `brought_from` and "
        "`brought_sha256`. The hive-network skill verifies the package first and never runs it.",
        "",
        f"## Create the folder Hive ({hive['health']})",
        "",
        f"`{hive['root']}/` is an inert template in the Hive folder convention. It holds "
        f"`HIVE.md`, `.gitattributes` and {len(rooms)} rooms under `shared/`: one note per task "
        "(with `id`, `title`, `status` and `depends_on`, linked by `[[id]]`), the charter and "
        "case intake, and the starter files as notes in `shared/casework/artifacts/`.",
        "",
        "1. Ask your Brainstem to create a Hive with the Hive agent: `create` with this starter's "
        f"name as its title, `approvals` {hive['approvals']}, and the `fields` hint from "
        f"`{hive['root']}/HIVE.md`. The Hive agent writes `HIVE.md` with a fresh `hive:` id, the "
        "`.gitattributes` file and your signed key file.",
        "2. Pin the unzipped folder as a reference (`reference`), then bring each room by signed "
        f"copy: `bring` from `{hive['root']}/shared/<room>` to `shared/<room>`. Each proposal "
        "shows who will see the files; nothing applies until you confirm it in a later turn.",
        "3. Invite people. Each person's Brainstem files one signed request; members admit them "
        "with the Hive's approvals.",
        "",
        "An organization cannot bind a folder Hive yet (G10), so this Hive stays beside the "
        "Organization plan, not inside it.",
        "",
        "## How the starter maps",
        "",
        *(f"- {note}" for note in hive["notes"]),
        "",
        f"Maps: [ECOSYSTEM.md]({organism['sources']['ecosystem']}) and "
        f"[CONSTITUTION.md]({organism['sources']['constitution']}) (kody-w/rapp-work, experimental), "
        f"and the [Hive folder convention]({organism['sources']['convention']}) "
        "(kody-w/rapp-model-hive, experimental). Specifications decide; this page only points at "
        "them.",
        "",
    ]
    return "\n".join(lines).encode("utf-8")


def package_additions(
    blueprint: dict[str, Any], source_files: dict[str, bytes], dependencies: dict[str, Any]
) -> tuple[dict[str, bytes], dict[str, Any]]:
    """New package files (the organism page and the template tree) and the organism map."""
    template, notes = build_template(blueprint, source_files)
    organism = organism_map(blueprint, template, notes, dependencies)
    files = {f"{ROOM_ROOT}/{path}": data for path, data in template.items()}
    files["ORGANISM.md"] = organism_markdown(blueprint, organism)
    return files, organism


def _load(slug: str) -> tuple[dict[str, Any], dict[str, bytes], dict[str, Any]]:
    from scripts.file_integrity import read_regular_bytes
    from scripts.organization_seeds import load_blueprint

    blueprint, source_files = load_blueprint(slug)
    dependencies = json.loads(read_regular_bytes(ROOT / "seed-src" / "SDK_PIN.json"))
    return blueprint, source_files, dependencies


def main() -> None:
    from scripts.organization_seeds import SEED_SLUGS

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--slug", choices=SEED_SLUGS)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    if args.out is not None:
        if args.slug is None:
            parser.error("--out needs --slug")
        target = args.out.resolve()
        if target.exists():
            parser.error("--out must name a new folder")
        template, _ = build_template(*_load(args.slug)[:2])
        for path, data in template.items():
            destination = target / path
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
        print(json.dumps({"slug": args.slug, "files": len(template), "out": str(target)}))
        return
    summary = []
    for slug in [args.slug] if args.slug else SEED_SLUGS:
        blueprint, source_files, dependencies = _load(slug)
        first, organism = package_additions(blueprint, source_files, dependencies)
        if args.check:
            again, _ = package_additions(blueprint, source_files, dependencies)
            if first != again:
                raise SystemExit(f"{slug}: the template is not deterministic")
        summary.append({"slug": slug, "files": len(first),
                        "sha256": sha(json.dumps({p: sha(d) for p, d in sorted(first.items())},
                                                 sort_keys=True).encode()),
                        "notes": len(organism["folderHive"]["notes"])})
    print(json.dumps({"templates": summary, "mode": "checked" if args.check else "built",
                      "runs": "nothing"}, sort_keys=True))


if __name__ == "__main__":
    main()
