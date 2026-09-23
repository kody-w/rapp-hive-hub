"""Practice Shelf: a tiny command-line bookmark keeper.

This is deliberately imperfect practice material for the Autonomous Software
Improvement Lab. Read README.md before running it or its tests.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import os
import sys
from pathlib import Path
from typing import TextIO

VERSION = "0.1.0-practice"
WEB_SCHEMES = ("http://", "https://")
MAX_TITLE = 200


class ShelfError(Exception):
    """A problem the person using the shelf can act on."""


def data_dir() -> Path:
    override = os.environ.get("PRACTICE_SHELF_HOME")
    return Path(override) if override else Path.home() / ".practice-shelf"


def normalize_url(url: str) -> str:
    clean = url.strip()
    if not clean.lower().startswith(WEB_SCHEMES):
        raise ShelfError(f"only http and https links are supported: {clean!r}")
    return clean.rstrip("/")


def parse_id(text: str) -> int | None:
    text = text.strip()
    return int(text) if text.isdigit() else None


class Shelf:
    def __init__(self, path: Path | str | None = None) -> None:
        self.path = Path(path) if path is not None else data_dir() / "shelf.json"
        self.items: list[dict] = []
        self.next_id = 1
        if self.path.exists():
            data = json.loads(self.path.read_text(encoding="utf-8"))
            self.items = data["items"]
            self.next_id = data["next_id"]

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as handle:
            json.dump({"items": self.items, "next_id": self.next_id}, handle, indent=2)
            handle.write("\n")

    def find(self, url: str) -> dict | None:
        target = normalize_url(url)
        for item in self.items:
            if item["url"] == target:
                return item
        return None

    def add(
        self,
        url: str,
        title: str | None = None,
        tags: tuple[str, ...] | list[str] = (),
        allow_duplicates: bool = False,
    ) -> dict:
        clean = normalize_url(url)
        if not allow_duplicates and self.find(clean) is not None:
            raise ShelfError(f"already on the shelf: {clean}")
        item = {
            "id": self.next_id,
            "url": clean,
            "title": (title or clean)[:MAX_TITLE],
            "tags": sorted({tag.strip().lower() for tag in tags if tag.strip()}),
        }
        self.items.append(item)
        self.next_id += 1
        self.save()
        return item

    def remove(self, item_id: int | None) -> None:
        self.items = [item for item in self.items if item["id"] != item_id]
        self.save()

    def list(self, tag: str | None = None) -> list[dict]:
        if tag is None:
            return list(self.items)
        wanted = tag.strip().lower()
        return [item for item in self.items if wanted in item["tags"]]

    def export(self, fmt: str = "json") -> str:
        if fmt == "json":
            return json.dumps({"items": self.items}, indent=2) + "\n"
        if fmt == "csv":
            buffer = io.StringIO()
            writer = csv.writer(buffer, lineterminator="\n")
            writer.writerow(["id", "url", "title", "tags"])
            for item in self.items:
                writer.writerow([item["id"], item["url"], item["title"], " ".join(item["tags"])])
            return buffer.getvalue()
        raise ShelfError(f"unknown export format: {fmt}")

    def import_file(self, path: Path | str, allow_duplicates: bool = True) -> int:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        count = 0
        for entry in data["items"]:
            self.add(
                entry["url"],
                entry.get("title"),
                entry.get("tags", ()),
                allow_duplicates=allow_duplicates,
            )
            count += 1
        return count


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="shelf", description="Keep a small shelf of web links.")
    parser.add_argument("--version", action="version", version=VERSION)
    commands = parser.add_subparsers(dest="command", required=True)
    add = commands.add_parser("add", help="add a link")
    add.add_argument("url")
    add.add_argument("--title")
    add.add_argument("--tag", action="append", default=[], help="a tag; repeat for more")
    listing = commands.add_parser("list", help="list links in the order they were added")
    listing.add_argument("--tag", help="only links with this tag")
    remove = commands.add_parser(
        "remove", help="remove the link with this id; fails if there is no such link"
    )
    remove.add_argument("id")
    export = commands.add_parser("export", help="print the whole shelf as json or csv")
    export.add_argument("--format", choices=("json", "csv"), default="json")
    importer = commands.add_parser("import", help="add every link from a json export")
    importer.add_argument("file")
    return parser


def main(argv: list[str] | None = None, out: TextIO | None = None) -> int:
    out = out or sys.stdout
    args = build_parser().parse_args(argv)
    try:
        shelf = Shelf()
        if args.command == "add":
            item = shelf.add(args.url, args.title, args.tag)
            print(f"added {item['id']}: {item['url']}", file=out)
        elif args.command == "list":
            for item in shelf.list(args.tag):
                tags = ",".join(item["tags"])
                print(f"{item['id']}\t{item['url']}\t{item['title']}\t{tags}", file=out)
        elif args.command == "remove":
            shelf.remove(parse_id(args.id))
            print("removed", file=out)
        elif args.command == "export":
            out.write(shelf.export(args.format))
        elif args.command == "import":
            count = shelf.import_file(args.file)
            print(f"imported {count}", file=out)
    except Exception:
        print("error: operation failed", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
