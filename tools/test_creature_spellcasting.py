#!/usr/bin/env python3
"""Validate the single-creature linked-spell prototype."""

from __future__ import annotations

import json
from pathlib import Path

from creature_spellcasting import PROTOTYPE_CREATURE_SLUG, PROTOTYPE_SPELLCASTING


REPO = Path(__file__).resolve().parents[1]


def records(name: str) -> list[dict]:
    result: list[dict] = []
    for path in (REPO / "compendium").glob(f"**/{name}"):
        result.extend(json.loads(path.read_text(encoding="utf-8")))
    return result


def main() -> int:
    creatures = records("creatures.json")
    creature = next(
        (record for record in creatures if record.get("slug") == PROTOTYPE_CREATURE_SLUG),
        None,
    )
    if creature is None:
        raise SystemExit(f"missing prototype creature: {PROTOTYPE_CREATURE_SLUG}")
    if creature.get("data", {}).get("spellcasting") != PROTOTYPE_SPELLCASTING:
        raise SystemExit("prototype creature spellcasting does not match its source mapping")

    spell_slugs = {record.get("slug") for record in records("spells.json")}
    linked = 0
    for entry in PROTOTYPE_SPELLCASTING:
        for group in entry["spellGroups"]:
            for spell in group["spells"]:
                reference = spell["reference"]
                prefix = "/spell/"
                if not reference.startswith(prefix) or reference[len(prefix):] not in spell_slugs:
                    raise SystemExit(f"unresolved spell reference: {reference}")
                linked += 1

    group_form = json.loads(
        (REPO / "forms/partials/spellcasting-group.json").read_text(encoding="utf-8")
    )
    spell_list = group_form["sections"][1]
    if spell_list.get("attributeType") != "Spell":
        raise SystemExit("spellcasting group must use Encounter+'s Spell picker")

    view = (REPO / "views/partials/spellcasting.md").read_text(encoding="utf-8")
    if "spell.reference" not in view or "spellGroups" not in view:
        raise SystemExit("spellcasting view does not render linked spell groups")
    if "{% elsif" in view or "{% elseif" in view:
        raise SystemExit("spellcasting view uses a template tag unsupported by Encounter+")

    print(f"Validated {linked} linked spells on Goblin War Chanter")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
