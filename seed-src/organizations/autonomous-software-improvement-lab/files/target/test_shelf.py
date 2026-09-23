"""Tests for Practice Shelf.

Deliberately imperfect practice material: read README.md before running.
Run from this directory: python3 -B -m unittest -v test_shelf
"""

from __future__ import annotations

import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import shelf


class ShelfTests(unittest.TestCase):
    def setUp(self) -> None:
        self.workspace = tempfile.TemporaryDirectory()
        self.path = Path(self.workspace.name) / "shelf.json"
        self.shelf = shelf.Shelf(self.path)

    def tearDown(self) -> None:
        self.workspace.cleanup()

    def test_add_and_list(self) -> None:
        item = self.shelf.add("https://example.org/a", "A page", ["Reading"])
        self.assertEqual(item["id"], 1)
        self.assertEqual(self.shelf.list(), [item])

    def test_add_normalizes_url_title_and_tags(self) -> None:
        item = self.shelf.add("  https://example.org/b/  ", None, [" Work ", "work", ""])
        self.assertEqual(item["url"], "https://example.org/b")
        self.assertEqual(item["title"], "https://example.org/b")
        self.assertEqual(item["tags"], ["work"])

    def test_add_refuses_a_duplicate_url(self) -> None:
        self.shelf.add("https://example.org/c")
        with self.assertRaises(shelf.ShelfError):
            self.shelf.add("https://example.org/c/")

    def test_rejects_links_that_are_not_web_links(self) -> None:
        for url in ("ftp://example.org/file", "javascript:alert(1)", "example.org"):
            with self.subTest(url=url), self.assertRaises(shelf.ShelfError):
                self.shelf.add(url)

    def test_list_filters_by_tag_case_insensitively(self) -> None:
        self.shelf.add("https://example.org/d", tags=["Music"])
        self.shelf.add("https://example.org/e", tags=["news"])
        self.assertEqual([i["url"] for i in self.shelf.list("MUSIC")], ["https://example.org/d"])

    def test_remove_an_existing_link(self) -> None:
        first = self.shelf.add("https://example.org/f")
        second = self.shelf.add("https://example.org/g")
        self.shelf.remove(first["id"])
        self.assertEqual(self.shelf.list(), [second])

    def test_ids_increase_and_persist(self) -> None:
        self.shelf.add("https://example.org/h")
        self.shelf.add("https://example.org/i")
        reloaded = shelf.Shelf(self.path)
        self.assertEqual([i["id"] for i in reloaded.list()], [1, 2])
        self.assertEqual(reloaded.add("https://example.org/j")["id"], 3)

    def test_export_json_and_csv(self) -> None:
        self.shelf.add("https://example.org/k", "K, with a comma", ["b", "a"])
        exported = json.loads(self.shelf.export("json"))
        self.assertEqual(exported["items"][0]["tags"], ["a", "b"])
        rows = self.shelf.export("csv").splitlines()
        self.assertEqual(rows[0], "id,url,title,tags")
        self.assertEqual(rows[1], '1,https://example.org/k,"K, with a comma",a b')
        with self.assertRaises(shelf.ShelfError):
            self.shelf.export("xml")

    def test_import_round_trip(self) -> None:
        self.shelf.add("https://example.org/l", "L", ["x"])
        self.shelf.add("https://example.org/m", "M")
        export_path = Path(self.workspace.name) / "export.json"
        export_path.write_text(self.shelf.export("json"), encoding="utf-8")
        fresh = shelf.Shelf(Path(self.workspace.name) / "fresh.json")
        self.assertEqual(fresh.import_file(export_path), 2)
        self.assertEqual([i["url"] for i in fresh.list()], [i["url"] for i in self.shelf.list()])


class CommandLineTests(unittest.TestCase):
    """End-to-end checks through main(), the way a person uses the shelf."""

    def run_cli(self, *argv: str) -> tuple[int, str]:
        out = io.StringIO()
        return shelf.main(list(argv), out=out), out.getvalue()

    def test_add_list_and_remove(self) -> None:
        code, added = self.run_cli("add", "https://example.org/cli-check", "--tag", "Practice")
        self.assertEqual(code, 0)
        self.assertTrue(added.startswith("added "))
        item_id = added.split()[1].rstrip(":")
        code, listing = self.run_cli("list", "--tag", "practice")
        self.assertEqual(code, 0)
        self.assertIn("https://example.org/cli-check", listing)
        code, removed = self.run_cli("remove", item_id)
        self.assertEqual((code, removed.strip()), (0, "removed"))
        code, listing = self.run_cli("list")
        self.assertNotIn("https://example.org/cli-check", listing)

    def test_version(self) -> None:
        with self.assertRaises(SystemExit) as raised, mock.patch("sys.stdout", io.StringIO()):
            shelf.main(["--version"])
        self.assertEqual(raised.exception.code, 0)


if __name__ == "__main__":
    unittest.main()
