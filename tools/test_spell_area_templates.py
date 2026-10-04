#!/usr/bin/env python3
"""Regression checks for derived structured spell-area templates."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import json5

from spell_area_templates import parse_spell_area
from eplus_dev import validate_form_definition


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
    assert not validate_form_definition(form), "spell editor has invalid native form types"
    area_form = form["sections"][3]["fields"][8]["form"]
    size_section = area_form["sections"][1]
    assert size_section["type"] == "group", "area size must use a group section"
    size_field = size_section["fields"][0]
    assert size_field["type"] == "decimal", "area size must allow fractional values"
    assert size_field["units"] == "ft", "area size must support native unit conversion"

    # The screenshot failure must be caught at the same nested decoder path.
    broken = deepcopy(form)
    broken["sections"][3]["fields"][8]["form"]["sections"][1] = {
        "type": "decimal", "attribute": "data.areaEffectSize"
    }
    assert validate_form_definition(broken) == [
        "sections[3].fields[8].form.sections[1].type: invalid section type 'decimal'"
    ], "validation missed the spell editor decoding failure"

    # Check the same rules inside tabs, list row editors, and field containers.
    nested = {
        "tabs": [{"sections": [{
            "type": "list",
            "form": {"sections": [{"type": "group", "fields": [{
                "type": "hStack", "fields": [{"type": "decimal"}]
            }]}]},
        }]}]
    }
    assert not validate_form_definition(nested), "valid nested editors were rejected"
    nested["tabs"][0]["sections"][0]["form"]["sections"][0]["fields"][0]["fields"][0]["type"] = "group"
    assert validate_form_definition(nested) == [
        "tabs[0].sections[0].form.sections[0].fields[0].fields[0].type: invalid field type 'group'"
    ], "validation missed an invalid nested field type"

    serialized_form = json.dumps(form)
    for attribute in ("data.areaEffectShape", "data.areaEffectSize"):
        assert attribute in serialized_form, f"spell form is missing {attribute}"

    print(
        f"spell area templates: {configured} configured, {skipped} manual, "
        f"{area_spells} total area spells OK"
    )


if __name__ == "__main__":
    main()
