"""Folder-Hive templates and seed successors: deterministic, inert, inside the file rules, and
additive, with every predecessor still resolvable byte for byte.

The restated folder rules live in scripts/folder_hive.py. When a pinned copy of the convention's
agent is present (kody-w/rapp-model-hive at the commit named there, under
.hive-hub/deps/rapp-model-hive or HIVE_MD_AGENT), the tests read it read-only and compare every
restated rule with it.
"""

from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import unicodedata
import unittest
from pathlib import Path
from typing import Any

from scripts import folder_hive
from scripts.organization_seeds import ROOT, SEED_SLUGS, build_seed, load_blueprint

PINNED_AGENT = Path(
    os.environ.get("HIVE_MD_AGENT", ROOT / ".hive-hub/deps/rapp-model-hive/agents/hive_agent.py")
)
INSTRUCTION_FILES = {
    "agents.md", "claude.md", "claude.local.md", "gemini.md", "skill.md", "copilot-instructions.md"}
HEALTH_WORDS = {"in force", "specified", "experimental", "candidate", "frozen", "—"}
FIELDS = "id=id; title=title; status=status; owner=owner,assignee; depends on=depends_on"
PREDECESSORS = ROOT / "seed-src" / "SEED_PREDECESSORS.json"
# Home and drive-letter paths, spelled in parts so the pattern is not itself a path.
LOCAL_PATH = re.compile("|".join(re.escape("/" + name + "/") for name in ("Users", "home"))
                        + r"|\b[A-Za-z]:\\")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def front(text: str) -> tuple[dict[str, Any], str]:
    """The convention's lenient frontmatter reading: `key: value`, or `key:` then `  - item`."""
    if not text.startswith("---\n"):
        return {}, text
    end = text.index("\n---\n", 3)
    meta: dict[str, Any] = {}
    key = ""
    for line in text[4:end].split("\n"):
        if line.startswith("  - ") and isinstance(meta.get(key), list):
            meta[key].append(line[4:])
            continue
        key, _, value = line.partition(":")
        meta[key] = value.strip() or []
    return meta, text[end + 5:]


def templates() -> dict[str, dict[str, bytes]]:
    result = {}
    for slug in SEED_SLUGS:
        blueprint, source_files = load_blueprint(slug)
        result[slug], _ = folder_hive.build_template(blueprint, source_files)
    return result


def published(slug: str) -> dict[str, Any]:
    return json.loads((ROOT / "public-src/organization-seeds" / f"{slug}.json").read_bytes())


class FolderHiveTemplateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.templates = templates()

    def test_generator_is_deterministic(self) -> None:
        self.assertEqual(templates(), self.templates)
        dependencies = json.loads((ROOT / "seed-src/SDK_PIN.json").read_bytes())
        for slug in SEED_SLUGS:
            with self.subTest(slug=slug):
                blueprint, source_files = load_blueprint(slug)
                first = folder_hive.package_additions(blueprint, source_files, dependencies)
                self.assertEqual(first, folder_hive.package_additions(blueprint, source_files, dependencies))
                seed = published(slug)
                shipped = {entry["path"]: entry["content"].encode() for entry in seed["files"]}
                self.assertEqual({path: shipped[path] for path in first[0]}, first[0])
                self.assertEqual(seed["organism"], first[1])

    def test_every_template_file_obeys_the_folder_rules(self) -> None:
        for slug, files in self.templates.items():
            with self.subTest(slug=slug):
                self.assertIsNone(folder_hive.tree_refusal(sorted(files)))
                self.assertEqual(files[".gitattributes"], b"* text eol=lf\n")
                for path, data in files.items():
                    parts = path.split("/")
                    self.assertIsNone(folder_hive.text_refusal(path, data), path)
                    self.assertTrue(path.endswith(".md") or path == ".gitattributes", path)
                    self.assertTrue(path in ("HIVE.md", ".gitattributes") or parts[0] == "shared", path)
                    self.assertFalse(any(part.startswith(".") for part in parts)
                                     and path != ".gitattributes", path)
                    self.assertNotIn(parts[-1].lower(), INSTRUCTION_FILES, path)
                    self.assertLessEqual(len(path), folder_hive.MAX_PATH)
                    text = data.decode("utf-8")
                    self.assertEqual(unicodedata.normalize("NFC", text), text, path)
                    self.assertNotIn("\r", text, path)
                    self.assertIsNone(LOCAL_PATH.search(text), path)

    def test_hive_md_is_a_placeholder_with_two_approvals_and_a_fields_hint(self) -> None:
        for slug, files in self.templates.items():
            with self.subTest(slug=slug):
                text = files["HIVE.md"].decode()
                meta, body = front(text)
                self.assertEqual(list(meta), ["hive", "version", "approvals", "fields"])
                self.assertEqual(meta["hive"], [], "the Hive id stays empty until creation")
                self.assertEqual((meta["version"], meta["approvals"], meta["fields"]), ("1", "2", FIELDS))
                self.assertNotRegex(text, r"\b[0-9a-f]{32,}\b")
                self.assertIn(f"`{slug}`", body)
                self.assertFalse(any(path.startswith(("members/", "requests/", "former/"))
                                     for path in files), "a template holds no members or requests")

    def test_tasks_are_one_file_each_and_link_their_dependencies(self) -> None:
        for slug, files in self.templates.items():
            with self.subTest(slug=slug):
                blueprint, _ = load_blueprint(slug)
                names = [path.rsplit("/", 1)[-1][:-3].casefold() for path in files if path.endswith(".md")]
                self.assertEqual(len(names), len(set(names)), "note names are unique for [[links]]")
                task_files = [path for path in files if path.startswith("shared/")
                              and not path.startswith("shared/casework/")]
                self.assertEqual(len(task_files), len(blueprint["tasks"]))
                for task in blueprint["tasks"]:
                    meta, body = front(files[f"shared/{task['team']}/{task['id']}.md"].decode())
                    self.assertEqual((meta["id"], meta["title"].strip('"')), (task["id"], task["title"]))
                    self.assertEqual(meta["status"], "blocked" if task["depends_on"] else "ready")
                    self.assertEqual(meta["depends_on"], task["depends_on"] or "[]")
                    for dependency in task["depends_on"]:
                        self.assertIn(f"[[{dependency}]]", body)
                    for output in task["outputs"]:
                        self.assertIn(f"`{output}`", body)
                for path, data in files.items():
                    if path.startswith("shared/casework/artifacts/"):
                        continue  # the starter's own text: `[[` in code is data, not a link
                    for target in folder_hive.LINK.findall(data.decode()):
                        self.assertIn(target.strip().casefold(), names, f"{path}: [[{target}]]")

    def test_artifacts_round_trip_to_the_exact_package_files(self) -> None:
        for slug, files in self.templates.items():
            with self.subTest(slug=slug):
                seed = published(slug)
                manifest = next(entry["content"] for entry in seed["files"] if entry["path"] == "seed.json")
                inventory = {entry["path"]: entry["sha256"] for entry in json.loads(manifest)["inventory"]}
                artifacts = [path for path in files if path.startswith("shared/casework/artifacts/")]
                self.assertEqual(len(artifacts), seed["counts"]["starterFiles"])
                for path in artifacts:
                    meta, body = front(files[path].decode())
                    source = meta["seed_file"]
                    self.assertTrue(source.startswith("templates/casework/work/starter/"), path)
                    self.assertTrue(body.startswith("\n"), path)
                    if source.endswith(".md"):
                        original = body[1:]
                    else:
                        fence = re.match(r"\n(`{3,})\n", body)
                        self.assertIsNotNone(fence, path)
                        closing = "\n" + fence.group(1) + "\n"
                        self.assertTrue(body.endswith(closing), path)
                        original = body[fence.end():-len(closing)] + "\n"
                    self.assertEqual(sha(original.encode()), meta["seed_sha256"], path)
                    self.assertEqual(inventory[source], meta["seed_sha256"], path)

    def test_every_starter_says_which_layers_it_touches(self) -> None:
        for slug in SEED_SLUGS:
            with self.subTest(slug=slug):
                organism = published(slug)["organism"]
                self.assertEqual(organism["status"], "starter-package-not-activated")
                self.assertEqual([layer["layer"] for layer in organism["layers"]], list(range(7)))
                for item in [*organism["layers"], *organism["across"], *organism["frozen"]]:
                    for word in re.split(r"\s*·\s*", item["health"]):
                        self.assertIn(word.split(":")[0], HEALTH_WORDS, item)
                organization = organism["layers"][2]
                self.assertEqual(organization["health"], "specified")
                self.assertTrue(all(gap in organization["touches"] for gap in ("G10", "G11", "G16")))
                self.assertIn("rapp-hive/1", organism["layers"][3]["touches"])
                self.assertEqual(organism["across"][0]["health"], "candidate")
                self.assertEqual(organism["frozen"][0]["id"], "rapp-hive/2")
                self.assertIsNone(organism["folderHive"]["hive"])
                self.assertEqual(organism["folderHive"]["approvals"], 2)
                self.assertTrue(organism["folderHive"]["notes"])
                page = next(entry["content"] for entry in published(slug)["files"]
                            if entry["path"] == "ORGANISM.md")
                for phrase in ("not an activated organization", "a reference in its own shape",
                               "frozen as a research record", "Hive agent", "G10"):
                    self.assertIn(phrase, page)


class SeedSuccessorTests(unittest.TestCase):
    """A successor adds files; its predecessor stays resolvable at its content addresses."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.pins = json.loads(PREDECESSORS.read_bytes())

    def earlier(self, slug: str) -> dict[str, Any]:
        return self.pins["seeds"][slug][-1]

    def test_packages_only_add_files(self) -> None:
        for slug in SEED_SLUGS:
            with self.subTest(slug=slug):
                earlier_path = ROOT / self.earlier(slug)["seed"]["path"]
                before = {entry["path"]: entry["sha256"] for entry in json.loads(earlier_path.read_bytes())["files"]}
                seed = build_seed(slug)
                after = {entry["path"]: entry["sha256"] for entry in seed["files"]}
                changed = {path for path in before if after.get(path) != before[path]}
                self.assertEqual(changed, {"seed.json"}, "only the inventory changes")
                added = set(after) - set(before)
                self.assertTrue(all(path == "ORGANISM.md" or path.startswith(f"{folder_hive.ROOM_ROOT}/")
                                    for path in added), added)
                self.assertEqual(len(added), seed["counts"]["folderHiveFiles"] + 1)

    def test_predecessors_stay_resolvable_outside_the_active_dialbook(self) -> None:
        dialbook = json.loads((ROOT / "api/hive-hub/v1/dialbook.json").read_bytes())
        active = {descriptor["path"] for descriptor in dialbook["records"]}
        index = json.loads((ROOT / "api/hive-hub/v1/organization-seeds.json").read_bytes())
        by_slug = {entry["slug"]: entry for entry in index["seeds"]}
        for slug in SEED_SLUGS:
            with self.subTest(slug=slug):
                earlier = self.earlier(slug)
                for name in ("record", "card", "camera_card", "legacy_card", "declaration", "seed", "archive"):
                    self.assertEqual(sha((ROOT / earlier[name]["path"]).read_bytes()), earlier[name]["sha256"], name)
                self.assertNotIn(earlier["record"]["path"], active)
                declaration = json.loads(
                    (ROOT / "public-src/skill-declarations" / f"seed-{slug}.json").read_bytes())
                named = declaration["extensions"]["predecessor"]
                self.assertEqual(named["dial_id"], earlier["dial_id"])
                for name in ("declaration", "record", "archive"):
                    self.assertEqual((named[name]["path"], named[name]["sha256"]),
                                     (earlier[name]["path"], earlier[name]["sha256"]))
                listed = by_slug[slug]["predecessors"]
                self.assertEqual([item["archive"]["sha256"] for item in listed], [earlier["archive"]["sha256"]])
                self.assertEqual(listed[0]["record"]["path"], earlier["record"]["path"])
                self.assertNotEqual(by_slug[slug]["archive"]["sha256"], earlier["archive"]["sha256"])


@unittest.skipUnless(PINNED_AGENT.is_file(), "needs the pinned Hive folder convention agent")
class PinnedConventionTests(unittest.TestCase):
    """Compare the restated rules with the convention's own agent file, read as data."""

    @classmethod
    def setUpClass(cls) -> None:
        data = PINNED_AGENT.read_bytes()
        cls.digest = sha(data)
        wanted = {"ATTRS", "TOPS", "INSTRUCTION_NAMES", "RESERVED", "SEGMENT", "PERSON", "FORMER",
                  "BAD_TEXT", "EMOJI", "EMOJI_OK", "DATAVIEWJS", "LINK", "MAX_FILE"}
        nodes: list[ast.stmt] = []
        for node in ast.parse(data.decode("utf-8")).body:
            if isinstance(node, ast.Assign):
                names = {target.id for target in node.targets if isinstance(target, ast.Name)}
                names |= {element.id for target in node.targets if isinstance(target, ast.Tuple)
                          for element in target.elts if isinstance(element, ast.Name)}
                if names & wanted:
                    nodes.append(node)
            elif isinstance(node, ast.ClassDef) and node.name == "Refused":
                nodes.append(node)
            elif isinstance(node, ast.FunctionDef) and node.name in {"name_rules", "text_rules"}:
                nodes.append(node)
        namespace: dict[str, Any] = {"re": re}
        exec(compile(ast.Module(body=nodes, type_ignores=[]), str(PINNED_AGENT), "exec"), namespace)
        cls.source = namespace

    def test_the_copy_is_the_pinned_commit(self) -> None:
        self.assertEqual(self.digest, folder_hive.CONVENTION["agent_sha256"])

    def test_restated_constants_match(self) -> None:
        for name in ("ATTRS", "TOPS", "INSTRUCTION_NAMES", "RESERVED", "EMOJI"):
            self.assertEqual(getattr(folder_hive, name), self.source[name], name)
        for name in ("SEGMENT", "PERSON", "FORMER", "BAD_TEXT", "EMOJI_OK", "DATAVIEWJS", "LINK"):
            ours, theirs = getattr(folder_hive, name), self.source[name]
            self.assertEqual((ours.pattern, ours.flags), (theirs.pattern, theirs.flags), name)
        self.assertEqual(
            (folder_hive.MAX_FILE, folder_hive.MAX_PATH, folder_hive.MAX_MEMBER_PATH),
            (self.source["MAX_FILE"], self.source["MAX_PATH"], self.source["MAX_MEMBER_PATH"]),
        )

    def test_the_convention_accepts_every_template_file(self) -> None:
        for slug, files in templates().items():
            for path, data in files.items():
                with self.subTest(slug=slug, path=path):
                    self.source["text_rules"](path, data)

    def test_restated_verdicts_match_on_refused_samples(self) -> None:
        samples = [
            ("shared/room/AGENTS.md", b"x"), ("shared/room/notes.txt", b"x"), ("shared/x.md", b"x"),
            ("top/room/a.md", b"x"), ("shared/room/aux.md", b"x"), ("shared/room/trailing..md", b"x"),
            ("shared/room/a.md", "a\u202eb".encode()), ("shared/room/a.md", b"```dataviewjs\n```"),
            ("shared/room/a.md", b"`$= 1`"), ("members/Bad Name/keys/phone.md", b"x"),
            ("shared/" + "r" * 60 + "/" + "n" * 60 + ".md", b"x"), ("shared/room/ok.md", b"fine"),
        ]
        for path, data in samples:
            with self.subTest(path=path):
                try:
                    self.source["text_rules"](path, data)
                    refused = False
                except self.source["Refused"]:
                    refused = True
                self.assertEqual(folder_hive.text_refusal(path, data) is not None, refused)


if __name__ == "__main__":
    unittest.main()
