"""Preserve linked deity metadata while rendering the live editable fields."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


FIELDS = {
    "Areas of Concern": "areasOfConcern", "Edicts": "edicts",
    "Anathema": "anathema", "Divine Attribute": "divineAttribute",
    "Divine Font": "clericFont", "Sanctification": "sanctificationOptions",
    "Divine Skill": "divineSkill", "Favored Weapon": "favoredWeapon",
    "Domains": "domains", "Alternate Domains": "alternateDomains",
    "Cleric Spells": "spells",
}
LINK = re.compile(r"\[([^]]+)\]\(([^)]+)\)")


def linked_value(value: str, links: list[tuple[str, str]]) -> str:
    """Link matching words without changing their text or nesting Markdown."""
    if LINK.search(value):
        return value
    spans: list[tuple[int, int, str]] = []
    for label, route in sorted(links, key=lambda item: -len(item[0])):
        for match in re.finditer(r"(?<!\w)" + re.escape(label) + r"(?!\w)", value, re.I):
            if any(match.start() < end and match.end() > start for start, end, _ in spans):
                continue
            spans.append((match.start(), match.end(), route.strip("<>")))
    for start, end, route in sorted(spans, reverse=True):
        value = value[:start] + f"[{value[start:end]}](<{route}>)" + value[end:]
    return value


def configure_deity_editor_data(entity: dict[str, Any]) -> bool:
    """Derive reference caches from the linked import summary, never GM prose.

    Views use a cache entry only while its value still equals the current field;
    new/edited values render directly, so old rules cannot override an edit.
    """
    if entity.get("kind") != "Deity" or not isinstance(entity.get("data"), dict):
        return False
    data = entity["data"]
    before = json.dumps(data, sort_keys=True)
    # One legacy source uses rank -> spell rather than the editor's string list.
    if isinstance(data.get("spells"), dict):
        data["spells"] = [f"{rank}: {spell}" for rank, spell in data["spells"].items()]
    links_by_field = {}
    for paragraph in str(data.get("rulesText") or "").split("\n\n"):
        heading = re.match(r"^\*\*([^*]+)\*\*\s*(.*)", paragraph, re.S)
        if heading and heading[1] in FIELDS:
            links_by_field[FIELDS[heading[1]]] = LINK.findall(heading[2])
    catalog = {}
    keys = {}
    for field, links in links_by_field.items():
        values = data.get(field) or []
        if not isinstance(values, list):
            values = [values]
        entries = []
        for value in dict.fromkeys(str(value) for value in values):
            text = linked_value(value, links)
            if text != value:
                entries.append({"value": value, "text": text})
        if entries:
            catalog[field] = entries
            keys[field] = [entry["value"] for entry in entries]
    data["deityReferences"] = catalog
    data["deityReferenceKeys"] = keys
    return before != json.dumps(data, sort_keys=True)


def main() -> None:
    repo = Path(__file__).resolve().parents[1]
    count = files = 0
    for path in sorted((repo / "compendium/packs").glob("*/deities.json")):
        records = json.loads(path.read_text())
        changed = sum(configure_deity_editor_data(record) for record in records)
        if changed:
            path.write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n")
            files += 1
            count += changed
    print(json.dumps({"deities": count, "collections": files}))


if __name__ == "__main__":
    main()
