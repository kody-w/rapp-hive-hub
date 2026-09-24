#!/usr/bin/env python3
"""Keep superseded organization-seed publications resolvable, byte for byte.

A Dial Record commits, through its declaration, to the exact seed JSON, and the seed JSON embeds
the package ZIP and its inventory. So a package that gains files needs a successor record. This
script copies each predecessor's published closure from one git revision into public-src/historical/
(record, public card, camera and legacy core cards, declaration, seed document, and the ZIP as
bounded base64 chunks), plus the published receipts that name a superseded record. It lists every
object in public-manifest.json and pins the lineage in seed-src/SEED_PREDECESSORS.json.
Predecessors stay at their content addresses, outside the active dialbook.

    python3 -B scripts/seed_predecessors.py preserve [--base REV]   write objects, entries and pins
    python3 -B scripts/seed_predecessors.py check    [--base REV]   compare them with the revision

Reads only committed public output of this repository through git. Standard library only.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.file_integrity import read_regular_bytes  # noqa: E402
from scripts.organization_seeds import SEED_SLUGS  # noqa: E402

PREDECESSOR_COMMIT = "e579f9cea54d7c577189f45ed2309da322911b54"
PUBLICATION = "rapp-seeds-e579f9c"
PINS = ROOT / "seed-src" / "SEED_PREDECESSORS.json"
API = "api/hive-hub/v1"
# Base64 chunks stay far below the core's 64 KiB JSON string bound.
CHUNK = 49_152
REASON = (
    "Each package gained ORGANISM.md and an inert folder-Hive template while every earlier file "
    "kept its bytes. A Dial Record commits to its exact package, so each starter has a successor "
    "record; this earlier record and its closure stay at their content addresses."
)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_show(revision: str, path: str) -> bytes:
    return subprocess.run(
        ["git", "-c", "core.fsmonitor=false", "show", f"{revision}:{path}"],
        cwd=ROOT, check=True, capture_output=True,
    ).stdout


def exact(revision: str, descriptor: dict[str, Any]) -> tuple[str, bytes]:
    path = descriptor["path"]
    data = git_show(revision, path)
    digest = descriptor.get("sha256") or descriptor["ref"].removeprefix("sha256:")
    if sha(data) != digest:
        raise SystemExit(f"{path} at {revision} does not match its content reference")
    return path, data


def archive_document(data: bytes) -> bytes:
    """A published ZIP as a JSON object the build writes back byte for byte."""
    encoded = base64.b64encode(data).decode("ascii")
    document = {
        "kind": "historical-seed-archive",
        "mediaType": "application/zip",
        "bytes": len(data),
        "sha256": sha(data),
        "base64Chunks": [encoded[index:index + CHUNK] for index in range(0, len(encoded), CHUNK)],
    }
    return (json.dumps(document, ensure_ascii=False, allow_nan=False, sort_keys=True,
                       separators=(",", ":")) + "\n").encode()


def closure(revision: str) -> tuple[dict[str, dict[str, Any]], list[tuple[str, str, bytes]]]:
    """The pins per seed and every (manifest id, kind, bytes) object to keep."""
    index = json.loads(git_show(revision, f"{API}/organization-seeds.json"))
    by_slug = {entry["slug"]: entry for entry in index["seeds"]}
    objects: list[tuple[str, str, bytes]] = []
    pins: dict[str, dict[str, Any]] = {}
    record_refs: dict[str, str] = {}
    for slug in SEED_SLUGS:
        entry = by_slug[slug]
        card_path, card_bytes = exact(revision, entry["card"])
        card = json.loads(card_bytes)
        record_path, record_bytes = exact(revision, card["record"])
        record = json.loads(record_bytes)
        camera_path, camera_bytes = exact(revision, card["cameraAiCard"])
        legacy_path, legacy_bytes = exact(revision, card["legacySkillCard"])
        declaration_path, declaration_bytes = exact(revision, card["skillDeclaration"])
        seed_path, seed_bytes = exact(revision, entry["seed"])
        archive_path, archive_bytes = exact(revision, entry["archive"])
        if json.loads(seed_bytes)["archive"]["sha256"] != sha(archive_bytes):
            raise SystemExit(f"{slug}: seed document and published ZIP disagree at {revision}")
        archive = archive_document(archive_bytes)
        objects.extend([
            (f"historical-seed-record-{sha(record_bytes)}", "historical-object", record_bytes),
            (f"historical-seed-card-{sha(card_bytes)}", "historical-object", card_bytes),
            (f"historical-core-card-{sha(camera_bytes)}", "historical-object", camera_bytes),
            (f"historical-core-card-{sha(legacy_bytes)}", "historical-object", legacy_bytes),
            (f"historical-seed-declaration-{sha(declaration_bytes)}", "historical-object",
             declaration_bytes),
            (f"historical-seed-document-{sha(seed_bytes)}", "historical-object", seed_bytes),
            (f"historical-seed-archive-{sha(archive_bytes)}", "historical-object", archive),
        ])
        record_refs[card["record"]["ref"]] = slug
        pins[slug] = {
            "reason": REASON,
            "source_commit": revision,
            "dial_id": card["legacySkillDialId"],
            "record": {"path": record_path, "sha256": sha(record_bytes),
                       "dial_id": record["dialId"], "chant": record["chants"][0]["value"]},
            "card": {"path": card_path, "sha256": sha(card_bytes)},
            "camera_card": {"path": camera_path, "sha256": sha(camera_bytes)},
            "legacy_card": {"path": legacy_path, "sha256": sha(legacy_bytes)},
            "declaration": {"path": declaration_path, "sha256": sha(declaration_bytes),
                            "bytes": len(declaration_bytes)},
            "seed": {"path": seed_path, "sha256": sha(seed_bytes)},
            "archive": {"path": archive_path, "sha256": sha(archive_bytes),
                        "bytes": len(archive_bytes)},
        }
    receipts = json.loads(git_show(revision, f"{API}/receipts/index.json"))
    for descriptor in receipts["receipts"]:
        _, data = exact(revision, descriptor)
        receipt = json.loads(data)
        subject = receipt.get("subject") or {}
        if subject.get("ref") in record_refs:
            objects.append((f"historical-receipt-{sha(data)}", "historical-receipt", data))
    return pins, objects


def planned(revision: str) -> tuple[dict[str, Any], dict[str, bytes], list[dict[str, Any]]]:
    pins, objects = closure(revision)
    files = {f"public-src/historical/{PUBLICATION}/{sha(data)}.json": data for _, _, data in objects}
    entries = [
        {"classification": "public", "id": entry_id, "kind": kind,
         "path": f"historical/{PUBLICATION}/{sha(data)}.json", "sha256": sha(data)}
        for entry_id, kind, data in objects
    ]
    document = {
        "schema": "hive-hub-seed-predecessors/1",
        "publication": PUBLICATION,
        "seeds": {slug: [pin] for slug, pin in pins.items()},
    }
    return document, files, entries


def encoded(document: dict[str, Any]) -> bytes:
    return (json.dumps(document, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode()


def canonical_manifest(manifest: dict[str, Any]) -> bytes:
    return (json.dumps(manifest, ensure_ascii=False, allow_nan=False, sort_keys=True,
                       separators=(",", ":")) + "\n").encode()


def preserve(revision: str) -> dict[str, Any]:
    document, files, entries = planned(revision)
    folder = ROOT / "public-src" / "historical" / PUBLICATION
    for stale in sorted(folder.glob("*.json")) if folder.is_dir() else []:
        if str(stale.relative_to(ROOT)) not in files:
            stale.unlink()
    for relative, data in files.items():
        target = ROOT / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            if read_regular_bytes(target) != data:
                raise SystemExit(f"{relative} exists with different bytes")
            continue
        target.write_bytes(data)
    manifest_path = ROOT / "public-manifest.json"
    manifest = json.loads(read_regular_bytes(manifest_path))
    kept = [entry for entry in manifest["entries"]
            if not entry["path"].startswith(f"historical/{PUBLICATION}/")]
    manifest["entries"] = sorted([*kept, *entries], key=lambda item: item["id"])
    manifest_path.write_bytes(canonical_manifest(manifest))
    PINS.write_bytes(encoded(document))
    return {"objects": len(files), "seeds": len(document["seeds"]), "mode": "preserved"}


def check(revision: str) -> dict[str, Any]:
    document, files, entries = planned(revision)
    for relative, data in files.items():
        if read_regular_bytes(ROOT / relative) != data:
            raise SystemExit(f"{relative} differs from {revision}")
    folder = ROOT / "public-src" / "historical" / PUBLICATION
    extra = sorted(str(path.relative_to(ROOT)) for path in folder.glob("*.json")
                   if str(path.relative_to(ROOT)) not in files)
    if extra:
        raise SystemExit(f"unexpected preserved files: {extra}")
    manifest = json.loads(read_regular_bytes(ROOT / "public-manifest.json"))
    listed = {entry["id"]: entry for entry in manifest["entries"]
              if entry["path"].startswith(f"historical/{PUBLICATION}/")}
    if listed != {entry["id"]: entry for entry in entries}:
        raise SystemExit("public-manifest.json does not list the preserved objects exactly")
    if read_regular_bytes(PINS) != encoded(document):
        raise SystemExit("seed-src/SEED_PREDECESSORS.json is stale")
    return {"objects": len(files), "seeds": len(document["seeds"]), "mode": "checked"}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("action", choices=("preserve", "check"))
    parser.add_argument("--base", default=PREDECESSOR_COMMIT)
    args = parser.parse_args()
    result = (preserve if args.action == "preserve" else check)(args.base)
    print(json.dumps({**result, "base": args.base}, sort_keys=True))


if __name__ == "__main__":
    main()
