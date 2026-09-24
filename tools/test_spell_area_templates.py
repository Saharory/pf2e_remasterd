#!/usr/bin/env python3
"""Regression checks for the small structured spell-area prototype."""

from __future__ import annotations

import json
from pathlib import Path

import json5


REPO = Path(__file__).resolve().parents[1]

PILOT_SPELLS = {
    "breathe-fire-player-core": ("15-foot cone", "cone", 15),
    "detect-magic-player-core": ("30-foot emanation", "emanation", 30),
    "fireball-player-core": ("20-foot burst", "sphere", 20),
    "lightning-bolt-player-core": ("120-foot line", "line", 120),
    "hellfire-plume-player-core-2": ("10-foot cylinder", "cylinder", 10),
    "spout-player-core-2": ("5-foot cube", "cube", 5),
}


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    records: dict[str, dict] = {}
    structured_slugs: set[str] = set()
    for path in sorted((REPO / "compendium" / "packs").glob("*/spells.json")):
        for record in load_json(path):
            slug = str(record.get("slug") or "")
            records[slug] = record
            data = record.get("data") or {}
            if "areaEffectShape" in data or "areaEffectSize" in data:
                structured_slugs.add(slug)

    assert structured_slugs == set(PILOT_SPELLS), (
        "structured spell-area prototype drifted: "
        f"expected {sorted(PILOT_SPELLS)}, got {sorted(structured_slugs)}"
    )

    for slug, (area, shape, size) in PILOT_SPELLS.items():
        data = records[slug]["data"]
        assert data["area"] == area, f"{slug}: source-book area text changed"
        assert data["areaEffectShape"] == shape, f"{slug}: wrong template shape"
        assert data["areaEffectSize"] == size, f"{slug}: wrong template size"

    entities = json5.loads((REPO / "entities.json").read_text(encoding="utf-8"))
    spell = next(entity for entity in entities if entity.get("name") == "Spell")
    assert spell.get("loadable") is True, "Spell must be loadable for map-tool testing"

    types = json5.loads((REPO / "types.json").read_text(encoding="utf-8"))
    shapes = set(types["AreaEffectShape"])
    expected_shapes = {shape for _, shape, _ in PILOT_SPELLS.values()}
    assert expected_shapes <= shapes, "AreaEffectShape is missing a pilot shape"

    form = json5.loads((REPO / "forms" / "spell.json").read_text(encoding="utf-8"))
    serialized_form = json.dumps(form)
    for attribute in ("data.areaEffectShape", "data.areaEffectSize"):
        assert attribute in serialized_form, f"spell form is missing {attribute}"

    print("spell area template prototype: 6 pilot spells OK")


if __name__ == "__main__":
    main()
