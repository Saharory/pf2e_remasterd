"""Restore structured metadata for creatures backed by Foundry actors."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


CATALOG_PATH = Path(__file__).with_name("creature-metadata.json")
CATALOG = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))["creatures"]
TRAIT_IMMUNITIES = {
    "mindless": ["Mental"],
    "swarm": ["Grabbed", "Prone", "Restrained"],
    "construct": [
        "Bleed", "Death Effects", "Disease", "Doomed", "Drained",
        "Fatigued", "Healing", "Mental", "Nonlethal Attacks", "Paralyzed",
        "Poison", "Sickened", "Spirit", "Unconscious", "Vitality", "Void",
    ],
}


def merge_unique(existing: list[Any], supplied: list[Any]) -> list[Any]:
    result: list[Any] = []
    seen: set[str] = set()
    for value in [*existing, *supplied]:
        key = str(value).casefold()
        if key not in seen:
            seen.add(key)
            result.append(value)
    return result


def configure_creature_metadata(entity: dict[str, Any]) -> bool:
    if entity.get("kind") != "Creature":
        return False
    metadata = CATALOG.get(str(entity.get("slug") or ""))
    data = entity.get("data")
    if not isinstance(data, dict):
        return False

    before = json.dumps(data, sort_keys=True)
    derived: list[str] = []
    for trait in data.get("traits") or []:
        derived.extend(TRAIT_IMMUNITIES.get(str(trait), []))
    if derived:
        data["immunities"] = merge_unique(data.get("immunities") or [], derived)
    if not metadata:
        return json.dumps(data, sort_keys=True) != before
    if metadata.get("senses"):
        data["senses"] = metadata["senses"]
    if "languages" in metadata:
        data["languages"] = metadata["languages"]
    if metadata.get("languagesDetails"):
        data["languagesDetails"] = metadata["languagesDetails"]
    for target, source in (("ac", "acDetails"), ("hp", "hpDetails"), ("saves", "savesDetails")):
        if metadata.get(source):
            data.setdefault(target, {})["details"] = metadata[source]
    if metadata.get("hardness"):
        data["hardness"] = metadata["hardness"]
    if metadata.get("immunities"):
        data["immunities"] = merge_unique(data.get("immunities") or [], metadata["immunities"])
    for field in ("weaknesses", "resistances"):
        if metadata.get(field):
            data.setdefault(field, {}).update(metadata[field])
    if metadata.get("movementOther"):
        movement = data.setdefault("movement", {})
        current = str(movement.get("other") or "")
        supplied = str(metadata["movementOther"])
        if supplied.casefold() not in current.casefold():
            movement["other"] = "; ".join(filter(None, (current, supplied)))
    return json.dumps(data, sort_keys=True) != before
