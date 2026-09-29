"""Compact Player Core skill references used by creature quick links."""

from __future__ import annotations

import uuid


SKILLS = (
    ("Acrobatics", 34, "Balance, maneuver in flight, squeeze, and tumble through."),
    ("Arcana", 35, "Recall arcane knowledge, identify arcane magic, and learn arcane spells."),
    ("Athletics", 36, "Climb, force open, grapple, high jump, reposition, shove, swim, and trip."),
    ("Crafting", 37, "Craft, identify, and repair items; recall knowledge about crafting."),
    ("Deception", 38, "Create a diversion, impersonate, lie, and feint."),
    ("Diplomacy", 39, "Gather information, make an impression, and request help."),
    ("Intimidation", 40, "Coerce and demoralize creatures."),
    ("Lore", 41, "Recall knowledge and earn income within a specialized subject."),
    ("Medicine", 42, "Administer first aid, recall medical knowledge, treat disease, poison, and wounds."),
    ("Nature", 43, "Command animals, identify primal magic, and recall natural knowledge."),
    ("Occultism", 44, "Decipher occult writing, identify occult magic, and recall occult knowledge."),
    ("Performance", 45, "Perform before an audience using an appropriate form of expression."),
    ("Religion", 46, "Decipher religious writing, identify divine magic, and recall religious knowledge."),
    ("Society", 47, "Create forgeries, decipher writing, subsist, and recall societal knowledge."),
    ("Stealth", 48, "Conceal an object, hide, and sneak."),
    ("Survival", 49, "Sense direction, subsist, track, and cover tracks."),
    ("Thievery", 50, "Palm objects, steal, disable devices, and pick locks."),
)


def skill_reference_records() -> list[dict]:
    records = []
    for name, aon_id, summary in SKILLS:
        slug = f"{name.casefold()}-skill-player-core"
        url = f"https://2e.aonprd.com/Skills.aspx?ID={aon_id}"
        records.append(
            {
                "id": str(uuid.uuid5(uuid.NAMESPACE_URL, f"pf2e-remaster:{slug}")).upper(),
                "kind": "Rule",
                "system": "pf2e-remaster",
                "systemVersion": "1.2.10",
                "name": name,
                "slug": slug,
                "type": "skill",
                "descr": f"{summary}\n\n[Complete {name} reference]({url})",
                "data": {"type": "skill", "referenceUrl": url},
                "attributes": {"remaster": True, "sourceId": "player-core"},
                "tags": ["player-core", "remaster", "rule", "skill"],
                "sources": [{"name": "Player Core", "url": url}],
                "modifiers": [],
                "created": "2026-09-07T00:00:00Z",
                "modified": "2026-09-07T00:00:00Z",
            }
        )
    return records
