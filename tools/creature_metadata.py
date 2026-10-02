"""Restore structured metadata for creatures backed by Foundry actors."""

from __future__ import annotations

import json
import re
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
DEFENSE_VALUE_ROUTES = (
    ("Nonlethal Attacks", "/rule/nonlethal-attacks-rules-2311"),
    ("Death Effects", "/rule/death-effects-rules-2331"),
    ("Unconscious", "/condition/unconscious-player-core"),
    ("Restrained", "/condition/restrained-player-core"),
    ("Paralyzed", "/condition/paralyzed-player-core"),
    ("Fatigued", "/condition/fatigued-player-core"),
    ("Sickened", "/condition/sickened-player-core"),
    ("Grabbed", "/condition/grabbed-player-core"),
    ("Drained", "/condition/drained-player-core"),
    ("Doomed", "/condition/doomed-player-core"),
    ("Prone", "/condition/prone-player-core"),
    ("Adamantine", "/item/adamantine-weapon-gm-core"),
    ("Disease", "/trait/disease"),
    ("Healing", "/trait/healing"),
    ("Mental", "/trait/mental"),
    ("Poison", "/trait/poison"),
    ("Sleep", "/trait/sleep"),
    ("Sonic", "/trait/sonic"),
    ("Spirit", "/trait/spirit"),
    ("Vitality", "/trait/vitality"),
    ("Void", "/trait/void"),
    ("Fire", "/trait/fire"),
)


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


def link_defense_value(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    text = value
    for label, route in DEFENSE_VALUE_ROUTES:
        if route in text:
            continue
        text = re.sub(
            rf"(?<![\w\[])({re.escape(label)})(?![\w])",
            lambda match: f"[{match.group(0)}]({route})",
            text,
            flags=re.I,
        )
    return text


def link_language_details(value: Any) -> Any:
    """Link shared communication abilities without changing custom notes."""
    if not isinstance(value, str):
        return value
    route = GLOSSARY_ROUTES_BY_KEY.get(normalize("Telepathy"), "")
    if not route or route in value:
        return value
    return re.sub(
        r"(?<![\w\[])(telepathy)(?![\w])",
        lambda match: f"[{match.group(0).title()}]({route})",
        value,
        count=1,
        flags=re.I,
    )


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
        if data.get("languagesDetails"):
            data["languagesDetails"] = link_language_details(data["languagesDetails"])
        data["immunities"] = [
            link_defense_value(value) for value in data.get("immunities") or []
        ]
        for field in ("weaknesses", "resistances"):
            values = data.get(field)
            if isinstance(values, dict):
                data[field] = {
                    key: link_defense_value(value) for key, value in values.items()
                }
        return json.dumps(data, sort_keys=True) != before
    if metadata.get("senses"):
        data["senses"] = metadata["senses"]
    if metadata.get("recallKnowledge"):
        data["recallKnowledge"] = metadata["recallKnowledge"]
    if "languages" in metadata:
        data["languages"] = metadata["languages"]
    if metadata.get("languagesDetails"):
        data["languagesDetails"] = link_language_details(metadata["languagesDetails"])
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
    if metadata.get("movement"):
        data.setdefault("movement", {}).update(metadata["movement"])
    if metadata.get("items"):
        data["items"] = metadata["items"]

    data["immunities"] = [
        link_defense_value(value) for value in data.get("immunities") or []
    ]
    for field in ("weaknesses", "resistances"):
        values = data.get(field)
        if isinstance(values, dict):
            data[field] = {
                key: link_defense_value(value) for key, value in values.items()
            }

    ability_text = metadata.get("abilityText") or {}
    abilities = data.get("abilities") or {}
    if isinstance(abilities, dict):
        for entries in abilities.values():
            for ability in entries or []:
                replacement = ability_text.get(str(ability.get("name") or ""))
                if replacement:
                    ability["text"] = replacement
        remove_names = set(metadata.get("removeAbilities") or [])
        if remove_names:
            for category, entries in abilities.items():
                if isinstance(entries, list):
                    abilities[category] = [
                        ability
                        for ability in entries
                        if str(ability.get("name") or "") not in remove_names
                    ]
        for name, destination in (metadata.get("abilityCategories") or {}).items():
            selected = None
            for category, entries in abilities.items():
                if not isinstance(entries, list):
                    continue
                for index, ability in enumerate(entries):
                    if str(ability.get("name") or "") == name:
                        selected = entries.pop(index)
                        break
                if selected is not None:
                    break
            if selected is not None:
                abilities.setdefault(destination, []).append(selected)

    attack_types = metadata.get("attackTypes") or {}
    attack_traits = metadata.get("attackTraits") or {}
    for index, attack in enumerate(data.get("attacks") or []):
        supplied = attack_types.get(str(index))
        if supplied:
            attack["type"] = supplied
        supplied_traits = attack_traits.get(str(index))
        if supplied_traits:
            attack["traits"] = supplied_traits

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
