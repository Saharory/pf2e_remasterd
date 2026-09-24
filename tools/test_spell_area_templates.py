#!/usr/bin/env python3
"""Regression checks for derived structured spell-area templates."""

from __future__ import annotations

import json
from pathlib import Path

import json5

from spell_area_templates import parse_spell_area


REPO = Path(__file__).resolve().parents[1]
EXPECTED_AREA_SPELLS = 333
EXPECTED_CONFIGURED = 308
EXPECTED_SKIPPED = 25

PILOT_SPELLS = {
    "breathe-fire-player-core": ("15-foot cone", "cone", 15),
    "detect-magic-player-core": ("30-foot emanation", "sphere", 30),
    "fireball-player-core": ("20-foot burst", "sphere", 20),
    "lightning-bolt-player-core": ("120-foot line", "line", 120),
    "hellfire-plume-player-core-2": ("10-foot cylinder", "cylinder", 10),
    "spout-player-core-2": ("5-foot cube", "cube", 5),
}


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    records: dict[str, dict] = {}
    area_spells = 0
    configured = 0
    skipped = 0

    roots = (REPO / "compendium" / "packs", REPO / "compendium" / "ogl-packs")
    for root in roots:
        for path in sorted(root.glob("*/spells.json")):
            for record in load_json(path):
                slug = str(record.get("slug") or "")
                records[slug] = record
                data = record.get("data") or {}
                area = str(data.get("area") or "").strip()
                parsed = parse_spell_area(area)
                has_shape = "areaEffectShape" in data
                has_size = "areaEffectSize" in data
                assert has_shape == has_size, f"{slug}: incomplete area template"

                if not area:
                    assert not has_shape, f"{slug}: area-less spell has a template"
                    continue

                area_spells += 1
                if parsed is None:
                    skipped += 1
                    assert not has_shape, f"{slug}: exceptional area must remain manual"
                    continue

                configured += 1
                expected_shape, expected_size = parsed
                assert data["areaEffectShape"] == expected_shape, f"{slug}: wrong template shape"
                assert data["areaEffectSize"] == expected_size, f"{slug}: wrong template size"

    assert area_spells == EXPECTED_AREA_SPELLS, (
        f"area spell count changed: expected {EXPECTED_AREA_SPELLS}, got {area_spells}"
    )
    assert configured == EXPECTED_CONFIGURED, (
        f"configured spell count changed: expected {EXPECTED_CONFIGURED}, got {configured}"
    )
    assert skipped == EXPECTED_SKIPPED, (
        f"manual spell count changed: expected {EXPECTED_SKIPPED}, got {skipped}"
    )

    for slug, (area, shape, size) in PILOT_SPELLS.items():
        data = records[slug]["data"]
        assert data["area"] == area, f"{slug}: source-book area text changed"
        assert data["areaEffectShape"] == shape, f"{slug}: wrong template shape"
        assert data["areaEffectSize"] == size, f"{slug}: wrong template size"

    entities = json5.loads((REPO / "entities.json").read_text(encoding="utf-8"))
    spell = next(entity for entity in entities if entity.get("name") == "Spell")
    assert spell.get("loadable") is True, "Spell must be loadable for map placement"

    types = json5.loads((REPO / "types.json").read_text(encoding="utf-8"))
    shapes = set(types["AreaEffectShape"])
    configured_shapes = {
        record["data"]["areaEffectShape"]
        for record in records.values()
        if "areaEffectShape" in (record.get("data") or {})
    }
    assert configured_shapes <= shapes, "AreaEffectShape is missing a configured shape"

    form = json5.loads((REPO / "forms" / "spell.json").read_text(encoding="utf-8"))
    serialized_form = json.dumps(form)
    for attribute in ("data.areaEffectShape", "data.areaEffectSize"):
        assert attribute in serialized_form, f"spell form is missing {attribute}"

    print(
        f"spell area templates: {configured} configured, {skipped} manual, "
        f"{area_spells} total area spells OK"
    )


if __name__ == "__main__":
    main()
