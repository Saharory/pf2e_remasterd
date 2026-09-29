"""Restore structured metadata for creatures backed by Foundry actors."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from creature_ability_glossary import GLOSSARY_ROUTES, normalize


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
GLOSSARY_ROUTES_BY_KEY = {normalize(key): value for key, value in GLOSSARY_ROUTES.items()}


def title(value: str) -> str:
    return " ".join(part.capitalize() for part in value.replace("_", "-").split("-"))


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
    if metadata.get("loreSkills"):
        data["loreSkills"] = metadata["loreSkills"]
        skills = data.get("skills")
        if isinstance(skills, dict):
            skills.pop("lore", None)
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

    ability_text = metadata.get("abilityText") or {}
    abilities = data.get("abilities") or {}
    if isinstance(abilities, dict):
        for entries in abilities.values():
            for ability in entries or []:
                replacement = ability_text.get(str(ability.get("name") or ""))
                if replacement:
                    ability["text"] = replacement

    linked_attack_abilities: set[str] = set()
    attack_effects = metadata.get("attackEffects") or {}
    for attack in data.get("attacks") or []:
        effects = attack_effects.get(str(attack.get("name") or "").casefold()) or []
        if not effects:
            continue
        rendered = []
        for effect in effects:
            name = title(str(effect))
            reference = GLOSSARY_ROUTES_BY_KEY.get(normalize(name), "")
            entry = {"name": name}
            if reference:
                entry["reference"] = reference
                linked_attack_abilities.add(normalize(name))
            rendered.append(entry)
        attack["effects"] = rendered

    # Shared strike riders such as Grab and Knockdown belong beside the attack
    # that grants them. Do not repeat them as disconnected offensive abilities.
    if linked_attack_abilities and isinstance(abilities, dict):
        for category, entries in abilities.items():
            if isinstance(entries, list):
                abilities[category] = [
                    ability
                    for ability in entries
                    if normalize(str(ability.get("name") or "")) not in linked_attack_abilities
                ]
    return json.dumps(data, sort_keys=True) != before
