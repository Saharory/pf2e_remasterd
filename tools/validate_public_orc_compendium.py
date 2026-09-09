#!/usr/bin/env python3
"""Fail closed when public compendium data contains known private residue."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[1]
COMPENDIUM = REPO / "compendium"
PACKS = COMPENDIUM / "packs"
CATALOG = COMPENDIUM / "sources.json"

BANNED_KEYS = {
    "rawText",
    "foundryId",
    "aonId",
    "aonUrl",
    "pdfPath",
    "sourcePath",
    "watermark",
}
BANNED_TEXT = (
    "@UUID[",
    "@Embed[",
    "@Check[",
    "@Damage[",
    "@Template[",
    "@Localize[",
    "Compendium.pf2e.",
    "[[/",
    "/Users/",
    "user's local source library",
    "PF2E for Foundry VTT contributors",
)
EMAIL = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)
UUID = re.compile(r"^[0-9A-F]{8}-[0-9A-F]{4}-[1-5][0-9A-F]{3}-[89AB][0-9A-F]{3}-[0-9A-F]{12}$")
STRIPPED_DESCRIPTION_KINDS = {
    "Ancestry",
    "Class",
    "Creature",
    "Domain",
    "Hazard",
    "Language",
    "Vehicle",
}


def inspect(value: Any, location: str, errors: list[str]) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if key in BANNED_KEYS:
                errors.append(f"{location}: banned key {key}")
            inspect(child, f"{location}.{key}", errors)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            inspect(child, f"{location}[{index}]", errors)
    elif isinstance(value, str):
        for marker in BANNED_TEXT:
            if marker in value:
                errors.append(f"{location}: banned text marker {marker!r}")
        if EMAIL.search(value):
            errors.append(f"{location}: possible email/private watermark")


def main() -> int:
    sources = json.loads(CATALOG.read_text())
    source_ids = {record["id"] for record in sources}
    pack_ids = {path.name for path in PACKS.iterdir() if path.is_dir()}
    errors: list[str] = []

    if source_ids != pack_ids:
        errors.append(f"pack/catalog mismatch: expected {sorted(source_ids)}, found {sorted(pack_ids)}")
    if "rage-of-elements" in pack_ids:
        errors.append("OGL-only Rage of Elements must not appear in the ORC packs")

    total = 0
    ids: set[str] = set()
    by_kind: dict[str, list[dict[str, Any]]] = {}
    collection_counts: dict[str, dict[str, int]] = {}
    for path in sorted(PACKS.rglob("*.json")):
        value = json.loads(path.read_text())
        inspect(value, str(path.relative_to(REPO)), errors)
        if path.name not in {"module.json", "source.json"}:
            if not isinstance(value, list):
                errors.append(f"{path}: entity collection is not an array")
            else:
                total += len(value)
                source_id = path.parent.name
                collection_counts.setdefault(source_id, {})
                for record in value:
                    if not isinstance(record, dict):
                        continue
                    kind = str(record.get("kind") or "")
                    collection_counts[source_id][kind] = collection_counts[source_id].get(kind, 0) + 1
                    by_kind.setdefault(kind, []).append(record)
                    record_id = str(record.get("id") or "")
                    if not UUID.match(record_id):
                        errors.append(f"{path}: invalid entity UUID {record_id!r}")
                    if record_id in ids:
                        errors.append(f"{path}: duplicate entity UUID {record_id}")
                    ids.add(record_id)
                    if not record.get("name") or not record.get("slug"):
                        errors.append(f"{path}: record lacks a name or slug")
                    if record.get("system") != "pf2e-remaster":
                        errors.append(f"{path}: wrong entity system")
                    if not isinstance(record.get("sources"), list) or not record["sources"]:
                        errors.append(f"{path}: {record.get('name')} lacks source attribution")
                    if record.get("attributes", {}).get("license") != "ORC-1.0a":
                        errors.append(f"{path}: {record.get('name')} lacks its ORC marker")
                    if kind == "Deity":
                        errors.append(f"{path}: Deity record was not excluded")
                    if kind in STRIPPED_DESCRIPTION_KINDS and record.get("descr"):
                        errors.append(f"{path}: {kind} lore description was not stripped")
                    if kind in {"Ancestry", "Class"} and record.get("data", {}).get("summary"):
                        errors.append(f"{path}: {kind} summary lore was not stripped")

    for source_id in sorted(pack_ids):
        notice = PACKS / source_id / "ORC-NOTICE.md"
        if not notice.is_file() or "TX 9-307-067" not in notice.read_text():
            errors.append(f"{source_id}: missing complete ORC notice")
        community_notice = PACKS / source_id / "COMMUNITY-USE-NOTICE.md"
        if not community_notice.is_file():
            errors.append(f"{source_id}: missing Community Use notice")
        else:
            community_text = community_notice.read_text()
            if "expressly prohibited from charging" not in community_text or "Saharory" not in community_text:
                errors.append(f"{source_id}: incomplete Community Use notice")
        source_meta = json.loads((PACKS / source_id / "source.json").read_text())
        if source_meta.get("counts") != collection_counts.get(source_id, {}):
            errors.append(f"{source_id}: source.json counts do not match entity files")
        module = json.loads((PACKS / source_id / "module.json").read_text())
        if module.get("system") != "pf2e-remaster" or not UUID.match(str(module.get("id") or "")):
            errors.append(f"{source_id}: invalid module metadata")
        if module.get("communityUseNotice") != "COMMUNITY-USE-NOTICE.md":
            errors.append(f"{source_id}: module does not identify its Community Use notice")

    backgrounds = by_kind.get("Background", [])
    for background in backgrounds:
        descr = str(background.get("descr") or "").casefold()
        if "attribute boost" not in descr and "ability boost" not in descr:
            errors.append(f"background mechanics were lost: {background.get('name')}")

    classes = by_kind.get("Class", [])
    if len(classes) != 24:
        errors.append(f"expected 24 ORC Remaster class records, found {len(classes)}")
    for class_record in classes:
        data = class_record.get("data", {})
        advancement = str(data.get("classAdvancement") or "")
        rows = [line for line in advancement.splitlines() if line.startswith("| ")][2:]
        if len(rows) != 20:
            errors.append(f"incomplete class advancement table: {class_record.get('name')}")
        features = data.get("classFeatures")
        if not isinstance(features, list) or not features or not all(feature.get("text") for feature in features):
            errors.append(f"incomplete class features: {class_record.get('name')}")

    traits = by_kind.get("Trait", [])
    if len(traits) < 428 or not all(trait.get("descr") for trait in traits):
        errors.append("trait catalog is incomplete")

    create_undead = next(
        (ritual for ritual in by_kind.get("Ritual", []) if ritual.get("name") == "Create Undead"),
        None,
    )
    if not create_undead or "| Creature Level | Spell Rank Required | Cost |" not in str(create_undead.get("descr")):
        errors.append("Create Undead ritual table is missing or flattened")

    if total < 14000:
        errors.append(f"public ORC record count is unexpectedly low: {total}")

    if errors:
        print("Public compendium validation failed:", file=sys.stderr)
        for error in errors[:100]:
            print(f"- {error}", file=sys.stderr)
        if len(errors) > 100:
            print(f"- ...and {len(errors) - 100} more", file=sys.stderr)
        return 1

    print(f"Validated {len(pack_ids)} ORC modules and {total} entity records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
