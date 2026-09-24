"""RAPP hub tests: every starter has its cards, and every template obeys the Hive file rules.

tools/build.py already refuses a template that breaks the hive-md file rules. These tests add what
a RAPP starter must also hold: a placeholder HIVE.md with 2 approvals and the fields hint, one
note per task with its dependencies linked, and artifacts that round-trip to exact bytes. When a
pinned copy of the convention's agent is present (kody-w/rapp-model-hive at 2bd7c95, as
agents/hive_agent.py under HIVE_MD_AGENT or .hive-hub/deps/rapp-model-hive), the tests read it as
data and run its own name and text rules over every file a Hive would hold.
"""

from __future__ import annotations

import ast
import hashlib
import importlib.util
import os
import re
import sys
import unittest
from pathlib import Path
from types import ModuleType
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STARTERS = ROOT / "starters"
AGENT_SHA256 = "e9a2d7243da31fd2388f140bb8138c3d8d2db428ad09075530eb049a0355e8dd"
PINNED_AGENT = Path(os.environ.get(
    "HIVE_MD_AGENT", ROOT / ".hive-hub" / "deps" / "rapp-model-hive" / "agents" / "hive_agent.py"))
FIELDS = "id=id; title=title; status=status; owner=owner,assignee; depends on=depends_on"
PLACEHOLDER = "<filled at create time>"
LINK = re.compile(r"\[\[([^\]|#\n]+)")


def load_builder() -> ModuleType:
    spec = importlib.util.spec_from_file_location("hub_build_rapp", ROOT / "tools" / "build.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


build = load_builder()


def front(text: str) -> tuple[dict[str, Any], str]:
    """The Hive agent's lenient frontmatter reading: `key: value`, or `key:` then `  - item`."""
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


def template_files(slug: str) -> dict[str, bytes]:
    """The files a Hive made from this starter could hold: everything but its README.md."""
    base = STARTERS / slug
    return {path.relative_to(base).as_posix(): path.read_bytes()
            for path in sorted(base.rglob("*")) if path.is_file()
            and path.relative_to(base).as_posix() != "README.md"}


class StarterCardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cards = {(card.kind, card.slug): card for card in build.load(ROOT)[3]}

    def test_each_starter_has_one_starter_card_and_one_org_card(self) -> None:
        folders = sorted(path.name for path in STARTERS.iterdir() if path.is_dir())
        self.assertEqual(len(folders), 12)
        for slug in folders:
            with self.subTest(starter=slug):
                starter = self.cards[("starter", slug)].fields
                org = self.cards[("organization", slug)].fields
                self.assertEqual((starter["status"], starter["template"], starter["org"]),
                                 ("experimental", f"starters/{slug}/", slug))
                self.assertEqual((org["status"], org["hive"], org["starter"]),
                                 ("specified", "template", slug))
                body = self.cards[("organization", slug)].body
                for gap in ("G10", "G16"):
                    self.assertIn(gap, body)
                self.assertIn("grants nothing", body)

    def test_hive_cards_are_honest(self) -> None:
        rapp = self.cards[("hive", "rapp-hive")].fields
        self.assertEqual((rapp["status"], rapp["protocol"]), ("experimental", "hive-md"))
        self.assertTrue({"hive", "root", "founder", "public_copy"} <= set(rapp))
        self.assertNotIn("address", rapp)  # no published shared copy, so nobody can join yet
        self.assertIn("no join requests", rapp["channel"])
        contoso = self.cards[("hive", "contoso-model-hive")].fields
        self.assertEqual(contoso["status"], "experimental")
        self.assertIn("no live shared copy", contoso["channel"])
        self.assertEqual(self.cards[("protocol", "rapp-hive/2")].fields["status"], "frozen")


class StarterTemplateTests(unittest.TestCase):
    def test_hive_md_is_a_placeholder_with_two_approvals_and_the_fields_hint(self) -> None:
        for starter in sorted(STARTERS.iterdir()):
            with self.subTest(starter=starter.name):
                text = (starter / "HIVE.md").read_text("utf-8")
                meta, body = front(text)
                self.assertEqual(list(meta), ["hive", "version", "approvals", "fields"])
                self.assertEqual((meta["hive"], meta["version"], meta["approvals"], meta["fields"]),
                                 (PLACEHOLDER, "1", "2", FIELDS))
                self.assertNotRegex(text, r"\b[0-9a-f]{32,}\b", "a template holds no real id")
                self.assertIn(f"`{starter.name}`", body)

    def test_tasks_link_their_dependencies_and_names_are_unique(self) -> None:
        for starter in sorted(STARTERS.iterdir()):
            with self.subTest(starter=starter.name):
                files = template_files(starter.name)
                names = [path.rsplit("/", 1)[-1][:-3].casefold() for path in files
                         if path.endswith(".md")]
                self.assertEqual(len(names), len(set(names)), "[[links]] resolve by name alone")
                tasks = {path: front(data.decode())[0] for path, data in files.items()
                         if path.startswith("shared/") and not path.startswith("shared/casework/")}
                self.assertTrue(tasks)
                ids = {meta["id"] for meta in tasks.values()}
                for path, meta in tasks.items():
                    self.assertEqual(list(meta), ["id", "title", "status", "depends_on"], path)
                    self.assertEqual(path.rsplit("/", 1)[-1], f"{meta['id']}.md")
                    depends = [] if meta["depends_on"] == "[]" else meta["depends_on"]
                    self.assertTrue(set(depends) <= ids, path)
                    self.assertEqual(meta["status"], "blocked" if depends else "ready", path)
                    body = files[path].decode()
                    for dependency in depends:
                        self.assertIn(f"[[{dependency}]]", body)
                for path, data in files.items():
                    if path.startswith("shared/casework/artifacts/"):
                        continue  # the starter's own text: `[[` inside code is data, not a link
                    for target in LINK.findall(data.decode()):
                        self.assertIn(target.strip().casefold(), names, f"{path}: [[{target}]]")

    def test_artifacts_round_trip_to_their_exact_files(self) -> None:
        for starter in sorted(STARTERS.iterdir()):
            with self.subTest(starter=starter.name):
                files = template_files(starter.name)
                artifacts = [path for path in files if path.startswith("shared/casework/artifacts/")]
                self.assertTrue(artifacts)
                for path in artifacts:
                    meta, body = front(files[path].decode())
                    self.assertEqual(list(meta), ["file", "sha256"], path)
                    self.assertTrue(path.endswith(meta["file"] + ("" if meta["file"].endswith(".md")
                                                                  else ".md"))
                                    or re.search(r"-\d+\.md$", path), path)
                    self.assertTrue(body.startswith("\n"), path)
                    if meta["file"].endswith(".md"):
                        original = body[1:]
                    else:
                        fence = re.match(r"\n(`{3,})\n", body)
                        self.assertIsNotNone(fence, path)
                        assert fence is not None
                        closing = "\n" + fence.group(1) + "\n"
                        self.assertTrue(body.endswith(closing), path)
                        original = body[fence.end():-len(closing)] + "\n"
                    self.assertEqual(hashlib.sha256(original.encode()).hexdigest(), meta["sha256"])

    def test_readme_is_documentation_outside_the_hive(self) -> None:
        for starter in sorted(STARTERS.iterdir()):
            with self.subTest(starter=starter.name):
                text = " ".join((starter / "README.md").read_text("utf-8").split())
                for phrase in ("never brought into a Hive", "Pin `shared/`, not this folder",
                               "(specified)", "`rapp-hive/1` Private Hive (in force)",
                               f"npx degit kody-w/rapp-hive-hub/starters/{starter.name}#"):
                    self.assertIn(phrase, text)


@unittest.skipUnless(PINNED_AGENT.is_file(), "needs the pinned Hive folder convention agent")
class PinnedConventionTests(unittest.TestCase):
    """Run the convention's own name and text rules, read as data from the pinned agent file."""

    @classmethod
    def setUpClass(cls) -> None:
        data = PINNED_AGENT.read_bytes()
        cls.digest = hashlib.sha256(data).hexdigest()
        wanted = {"TOPS", "INSTRUCTION_NAMES", "RESERVED", "SEGMENT", "PERSON", "FORMER",
                  "BAD_TEXT", "EMOJI", "EMOJI_OK", "DATAVIEWJS", "MAX_FILE"}
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
        self.assertEqual(self.digest, AGENT_SHA256)

    def test_the_convention_accepts_every_template_file(self) -> None:
        for starter in sorted(STARTERS.iterdir()):
            for path, data in template_files(starter.name).items():
                with self.subTest(starter=starter.name, path=path):
                    self.assertLessEqual(len(data), self.source["MAX_FILE"])
                    self.source["text_rules"](path, data)


if __name__ == "__main__":
    unittest.main()
