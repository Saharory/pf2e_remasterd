#!/usr/bin/env python3
"""Validate creature ability text and editable spell/ritual summaries."""

from __future__ import annotations

import json
import re
from pathlib import Path

import json5

from creature_ability_glossary import GLOSSARY, GLOSSARY_ROUTES


REPO = Path(__file__).resolve().parents[1]
SEPARATOR = re.compile(r"\n\s*---\s*\n")


def normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.casefold())


def records(name: str) -> list[dict]:
    result: list[dict] = []
    for base in (REPO / "compendium" / "packs", REPO / "compendium" / "ogl-packs"):
        for path in base.glob(f"**/{name}"):
            result.extend(json.loads(path.read_text(encoding="utf-8")))
    return result


def field_attributes(partial: dict) -> set[str]:
    return {
        str(field.get("attribute"))
        for section in partial.get("sections", [])
        for field in section.get("fields", [])
        if field.get("attribute")
    }


def form(name: str) -> dict:
    return json5.loads(
        (REPO / "forms" / name).read_text(encoding="utf-8"),
        allow_duplicate_keys=False,
    )


def main() -> int:
    if len(GLOSSARY) != 55:
        raise SystemExit("shared monster ability glossary is incomplete")
    glossary_keys = {normalize(code) for code in GLOSSARY}

    creatures = records("creatures.json")
    by_slug = {record["slug"]: record for record in creatures}
    ability_count = 0
    shared_reference_count = 0
    for creature in creatures:
        for entries in creature.get("data", {}).get("abilities", {}).values():
            for ability in entries or []:
                ability_count += 1
                text = str(ability.get("text") or "")
                shared_reference_count += int(bool(ability.get("reference")))
                name = str(ability.get("name") or "")
                if SEPARATOR.search(text):
                    raise SystemExit(f"creature ability retains artificial divider: {creature['slug']}: {name}")
                if normalize(text) in glossary_keys:
                    raise SystemExit(f"creature ability retains a glossary token: {creature['slug']}: {name}")
                tail = text.split("\n\n")[-1]
                if normalize(tail) in {normalize(name), normalize("Effect " + name)}:
                    raise SystemExit(f"creature ability retains a duplicate reference label: {creature['slug']}: {name}")
                for code in GLOSSARY_ROUTES:
                    if GLOSSARY[code] and GLOSSARY[code] in text:
                        raise SystemExit(
                            f"creature repeats linked shared rule {code}: {creature['slug']}: {name}"
                        )

    if shared_reference_count < 1500:
        raise SystemExit("creature shared-rule references are unexpectedly incomplete")

    moon_hag = by_slug["moon-hag-monster-core-2"]
    abilities = {
        ability["name"]: ability
        for entries in moon_hag["data"]["abilities"].values()
        for ability in entries
    }
    required_phrases = {
        "Coven": "[Spirit Blast](/spell/spirit-blast-player-core) to their coven's spells.",
        "Rend": "Claw",
        "Change Shape": "The moon hag can take on the appearance",
        "Dreadful Prediction": "once per round; **Effect** The moon hag",
        "Moonlight's Kiss": "[Quickened](/condition/quickened-player-core)",
        "Ride the Moonbeams": "[fly Speed](/rule/fly-speed-rules-2350)",
    }
    for name, phrase in required_phrases.items():
        if phrase not in str(abilities.get(name, {}).get("text") or ""):
            raise SystemExit(f"Moon Hag ability is incomplete: {name}")

    required_references = {
        "Coven": "/action/coven-monster-core",
        "Ferocity": "/action/ferocity-monster-core",
        "Rend": "/action/rend-monster-core",
        "Change Shape": "/action/change-shape-monster-core",
    }
    for name, reference in required_references.items():
        if abilities.get(name, {}).get("reference") != reference:
            raise SystemExit(f"Moon Hag shared ability name is not linked: {name}")

    if "At-Will Spells" in abilities:
        raise SystemExit("Moon Hag repeats at-will casting as a separate ability")
    if "form a coven" in abilities["Coven"]["text"] or "A Rend entry lists" in abilities["Rend"]["text"]:
        raise SystemExit("Moon Hag repeats a linked shared ability")
    if "\n\n**Effect**" in abilities["Dreadful Prediction"]["text"]:
        raise SystemExit("Moon Hag separates Effect from its ability metadata")
    for expected in (
        "[Stride](/action/stride-player-core)",
        "[Strike](/action/strike-player-core)",
        "[Fly](/action/fly-player-core)",
    ):
        if expected not in abilities["Moonlight's Kiss"]["text"]:
            raise SystemExit(f"Moon Hag is missing AoN-style inline reference: {expected}")

    bibliodaemon = by_slug["bibliodaemon-shining-kingdoms"]
    thoughtsense = next(
        ability
        for entries in bibliodaemon["data"]["abilities"].values()
        for ability in entries
        if ability["name"] == "Thoughtsense"
    )
    if "Thoughtsense allows" in thoughtsense["text"]:
        raise SystemExit("creature-specific Thoughtsense repeats its glossary definition")

    actions = {record["slug"]: record for record in records("actions.json")}
    for slug in ("at-will-spells-monster-core", "ferocity-monster-core", "rend-monster-core"):
        description = str(actions.get(slug, {}).get("descr") or "")
        if not description or normalize(description) in glossary_keys:
            raise SystemExit(f"shared monster action is incomplete: {slug}")

    action_slugs = {record["slug"] for record in actions.values()}
    for route in GLOSSARY_ROUTES.values():
        if route.rsplit("/", 1)[-1] not in action_slugs:
            raise SystemExit(f"shared monster ability link is missing: {route}")

    ability_form = form("partials/ability.json")
    if field_attributes(ability_form) != {"name", "actions", "traits", "text", "reference"}:
        raise SystemExit("ability form does not expose every rendered ability field")

    ability_view = (REPO / "views/partials/ability.md").read_text(encoding="utf-8")
    attack_view = (REPO / "views/partials/attack.md").read_text(encoding="utf-8")
    if "ability.reference" not in ability_view:
        raise SystemExit("shared creature ability names are not linked")
    if "/trait/{{trait}}" not in ability_view or "/trait/{{trait}}" not in attack_view:
        raise SystemExit("creature ability or attack traits are not linked")

    creature_form = form("creature.json")
    required_lists = {
        "data.abilities.interaction",
        "data.abilities.defensive",
        "data.abilities.offensive",
    }
    sections = {
        section.get("attribute"): section
        for section in creature_form.get("sections", [])
        if section.get("attribute")
    }
    for attribute in required_lists:
        if sections.get(attribute, {}).get("custom", {}).get("itemDetail"):
            raise SystemExit(f"ability list should remain name-only: {attribute}")

    spellcasting = form("partials/spellcasting.json")
    spell_groups = next(
        section for section in spellcasting["sections"] if section.get("attribute") == "spellGroups"
    )
    if spell_groups.get("custom", {}).get("itemTitle") != "{{label}}" or "spell.name" not in spell_groups.get("custom", {}).get("itemDetail", ""):
        raise SystemExit("spell groups do not preview their rank and spell names")

    rituals = form("partials/rituals.json")
    ritual_groups = next(
        section for section in rituals["sections"] if section.get("attribute") == "ritualGroups"
    )
    if ritual_groups.get("custom", {}).get("itemTitle") != "{{label}}" or "ritual.name" not in ritual_groups.get("custom", {}).get("itemDetail", ""):
        raise SystemExit("ritual groups do not preview their rank and ritual names")

    print(
        f"Validated {ability_count} editable creature abilities, "
        f"{shared_reference_count} shared-rule links, {len(GLOSSARY)} shared rules, "
        "and spell/ritual editor previews"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
