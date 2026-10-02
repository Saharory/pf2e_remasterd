#!/usr/bin/env python3
"""Validate creature ability text and editable spell/ritual summaries."""

from __future__ import annotations

import json
import re
from pathlib import Path

import json5

from build_public_orc_compendium import parameterized_trait_family
from creature_ability_glossary import GLOSSARY, GLOSSARY_ROUTES
from creature_senses import SENSE_ROUTES, link_shared_senses


REPO = Path(__file__).resolve().parents[1]
SEPARATOR = re.compile(r"\n\s*---\s*\n")


def normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.casefold())


def linked_labels(values: list) -> set[str]:
    return {
        re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", str(value)).casefold()
        for value in values
    }


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
    sense_reference_count = 0
    for creature in creatures:
        senses = str(creature.get("data", {}).get("senses") or "")
        if re.search(r"(?:^|;\s*)(?:Recall Knowledge|Languages)\b", senses, re.I):
            raise SystemExit(f"creature metadata remains embedded in senses: {creature['slug']}")
        if link_shared_senses(senses) != senses:
            raise SystemExit(f"creature shared sense is not linked: {creature['slug']}")
        sense_reference_count += sum(
            int(route in senses) for _, route in SENSE_ROUTES
        )
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
        for attack in creature.get("data", {}).get("attacks", []):
            shared_reference_count += sum(
                int(bool(effect.get("reference")))
                for effect in attack.get("effects", [])
                if isinstance(effect, dict)
            )

    if shared_reference_count < 1500:
        raise SystemExit("creature shared-rule references are unexpectedly incomplete")

    moon_hag = by_slug["moon-hag-monster-core-2"]
    if moon_hag["data"].get("senses") != "[Darkvision](/action/darkvision-monster-core)":
        raise SystemExit("Moon Hag senses are not separated and linked")
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

    murajau = by_slug["murajau-rage-of-elements"]
    murajau_data = murajau["data"]
    expected_items = "[Spear](/item/spear-player-core) (3), [Mesmerizing Opal](/item/mesmerizing-opal-gm-core), [Potency Crystal](/item/potency-crystal-gm-core), [Shark Tooth Charm](/item/shark-tooth-charm-gm-core)"
    if murajau_data.get("items") != expected_items:
        raise SystemExit("Murajau item links or quantities are incomplete")
    if murajau_data["attacks"][2].get("type") != "ranged":
        raise SystemExit("Murajau thrown spear is not a ranged Strike")
    if any(ability.get("name") == "Retract" for ability in murajau_data["abilities"]["defensive"]):
        raise SystemExit("Murajau Retract is still classified as defensive")
    if not any(ability.get("name") == "Retract" for ability in murajau_data["abilities"]["offensive"]):
        raise SystemExit("Murajau Retract is missing from its active abilities")

    lithic = by_slug["lithic-locus-rage-of-elements"]
    lithic_spells = {
        spell["name"]
        for casting in lithic["data"].get("spellcasting", [])
        for group in casting.get("spellGroups", [])
        for spell in group.get("spells", [])
    }
    if lithic_spells != {"One with Stone", "Daze"}:
        raise SystemExit("Lithic Locus repeats Echo the Past spells in innate spellcasting")
    if any(
        ability.get("name", "").startswith("Tremorsense")
        for ability in lithic["data"]["abilities"]["interaction"]
    ):
        raise SystemExit("Lithic Locus repeats Tremorsense as an interaction ability")

    solar = by_slug["solar-crow-rage-of-elements"]
    solar_abilities = {
        ability["name"]: ability
        for entries in solar["data"]["abilities"].values()
        for ability in entries
    }
    if "[concealment](/condition/concealed-player-core)" not in solar_abilities["Glinting Wing"]["text"]:
        raise SystemExit("Solar Crow Glinting Wing is missing its concealment link")
    if solar["data"].get("recallKnowledge") != {
        "dc": 27,
        "subject": "elemental",
        "skills": ["arcana", "nature"],
    }:
        raise SystemExit("Solar Crow has the wrong elemental Recall Knowledge skills")
    if [attack.get("traits") for attack in solar["data"].get("attacks", [])] != [
        ["finesse"],
        ["agile", "finesse"],
    ]:
        raise SystemExit("Solar Crow natural Strikes retain the incorrect unarmed trait")
    solar_outcomes = str(solar_abilities["Blinding Heat"].get("text") or "")
    for label in ("Critical Success", "Success", "Failure", "Critical Failure"):
        if f"\u2003**{label}**" not in solar_outcomes:
            raise SystemExit(f"Solar Crow outcome is not grouped under Blinding Heat: {label}")

    vault = by_slug["vault-builder-rage-of-elements"]
    vault_data = vault["data"]
    vault_abilities = {
        ability["name"]: ability
        for entries in vault_data["abilities"].values()
        for ability in entries
    }
    if vault_data.get("movement", {}).get("burrow") != 25:
        raise SystemExit("Vault Builder has the wrong burrow Speed")
    if vault_data.get("recallKnowledge") != {
        "dc": 51,
        "subject": "elemental",
        "skills": ["arcana", "nature"],
    }:
        raise SystemExit("Vault Builder has the wrong elemental Recall Knowledge skills")
    if vault_data.get("languagesDetails") != "[Telepathy](/action/telepathy-monster-core) 300 feet":
        raise SystemExit("Vault Builder telepathy is not linked to its internal rule")
    expected_resistance = "20 (except [Adamantine](/item/adamantine-weapon-gm-core))"
    if vault_data.get("resistances", {}).get("physical") != expected_resistance:
        raise SystemExit("Vault Builder physical resistance lacks its adamantine exception link")
    if vault_abilities.get("Reactive Strike", {}).get("reference") != "/action/reactive-strike-monster-core":
        raise SystemExit("Vault Builder does not use the remastered Reactive Strike reference")
    craft_text = str(vault_abilities.get("Craft Crystal Wand", {}).get("text") or "")
    for expected in (
        "[earth](/trait/earth)",
        "[greater striking](/item/striking-greater-gm-core)",
    ):
        if expected not in craft_text:
            raise SystemExit(f"Vault Builder Craft Crystal Wand is missing: {expected}")
    shard = next(attack for attack in vault_data["attacks"] if attack["name"] == "Crystal Shard")
    if shard.get("traits") != ["earth", "finesse", "magical", "range-increment-100"]:
        raise SystemExit("Vault Builder crystal shard is missing finesse or its range increment")
    prepared = vault_data["spellcasting"][0]["spellGroups"]
    prepared_spells = {
        (spell["name"], spell.get("details"))
        for group in prepared
        for spell in group["spells"]
    }
    for repeated in (("Disintegrate", "×2"), ("Earthquake", "×2"), ("Haste", "×2")):
        if repeated not in prepared_spells:
            raise SystemExit(f"Vault Builder prepared spell is not compacted: {repeated[0]}")
    if "+1 Status to All Saves vs. Magic" in vault_abilities or "+4 Status to All Saves vs. Earth" in vault_abilities:
        raise SystemExit("Vault Builder repeats save details as empty abilities")

    executor = by_slug["adult-executor-dragon-draconic-codex-creature-creature-4139"]
    executor_abilities = {
        ability["name"]: ability
        for entries in executor["data"]["abilities"].values()
        for ability in entries
    }
    aura = executor_abilities.get("Aura of Authority", {})
    if "temporarily immune" not in aura.get("text", "") or aura.get("traits") != ["aura", "emotion", "mental"]:
        raise SystemExit("Adult Executor Dragon Aura of Authority is incomplete")
    expected_executor_traits = {
        "Rage of the Divine": ["divine", "sanctified", "spirit"],
        "Change Shape": ["concentrate", "divine", "polymorph"],
        "Divine Utterance": ["divine", "sonic"],
    }
    for name, traits in expected_executor_traits.items():
        ability = executor_abilities.get(name, {})
        if ability.get("traits") != traits or re.match(
            r"\*\*(?:Reaction|Single Action|Two Actions)\*\*",
            ability.get("text", ""),
            re.I,
        ):
            raise SystemExit(f"Adult Executor Dragon action metadata is not structured: {name}")
    executor_data = executor["data"]
    sanctification = str(executor_abilities["Divine Sanctification"].get("text") or "")
    if "[holy](/trait/holy)" not in sanctification or "[unholy](/trait/unholy)" not in sanctification:
        raise SystemExit("Adult Executor Dragon sanctification choices are not linked")
    if executor_data.get("saves", {}).get("details") != "+2 status to all saves vs. [divine](/trait/divine)":
        raise SystemExit("Adult Executor Dragon is missing its divine save bonus")
    if executor_data.get("weaknesses", {}).get("divine-sanctification") != 10:
        raise SystemExit("Adult Executor Dragon is missing its opposing sanctification weakness")
    executor_attacks = {attack["name"]: attack for attack in executor_data["attacks"]}
    if "reach-10" not in executor_attacks["jaws"]["traits"] or "reach-15" not in executor_attacks["tail"]["traits"]:
        raise SystemExit("Adult Executor Dragon reach values are incomplete")

    army_ants = by_slug["army-ant-swarm-monster-core"]
    if "[Scent](/action/scent-monster-core) ([imprecise](/rule/imprecise-senses-rules-2407)) 30 feet" not in army_ants["data"]["senses"]:
        raise SystemExit("Army Ant Swarm is missing its scent acuity")
    if not {"grabbed", "precision", "prone", "restrained", "swarm mind"}.issubset(
        linked_labels(army_ants["data"].get("immunities") or [])
    ):
        raise SystemExit("Army Ant Swarm is missing explicit or swarm immunities")

    bone_prophet = by_slug["bone-prophet-monster-core"]
    if "([imprecise](/rule/imprecise-senses-rules-2407)) 30 feet" not in bone_prophet["data"].get("senses", ""):
        raise SystemExit("Bone Prophet is missing its scent acuity")
    if bone_prophet["data"].get("languagesDetails") != "[Telepathy](/action/telepathy-monster-core) 100 feet":
        raise SystemExit("Bone Prophet is missing its language details")

    adamantine_dragon = by_slug["adamantine-dragon-young-monster-core"]
    dragon_data = adamantine_dragon["data"]
    dragon_senses = dragon_data.get("senses", "")
    if "[Scent](/action/scent-monster-core) ([imprecise](/rule/imprecise-senses-rules-2407)) 60 feet" not in dragon_senses or "[Tremorsense](/action/tremorsense-monster-core) ([imprecise](/rule/imprecise-senses-rules-2407)) 60 feet" not in dragon_senses:
        raise SystemExit("Adamantine Dragon is missing structured sense acuity")
    if any(
        ability.get("name", "").startswith("Tremorsense")
        for ability in dragon_data["abilities"]["interaction"]
    ):
        raise SystemExit("Adamantine Dragon repeats Tremorsense as an interaction ability")
    if dragon_data.get("resistances", {}).get("physical") != "10 (except [adamantine](/item/adamantine-weapon-gm-core))":
        raise SystemExit("Adamantine Dragon is missing its printed physical resistance")
    dragon_abilities = {
        ability["name"]: ability
        for entries in dragon_data["abilities"].values()
        for ability in entries
    }
    avalanche = str(dragon_abilities.get("Avalanche Breath", {}).get("text") or "")
    for phrase in ("8d8 bludgeoning", "30-foot [cone]", "DC 28 [basic Reflex save]", "1d4 rounds"):
        if phrase not in avalanche:
            raise SystemExit(f"Adamantine Dragon Avalanche Breath is incomplete: {phrase}")
    attacks = {attack["name"]: attack for attack in dragon_data["attacks"]}
    if attacks["Jaws"].get("effects") != [{"name": "Grab", "reference": "/action/grab-monster-core"}]:
        raise SystemExit("Adamantine Dragon Grab is not attached to its jaws Strike")
    if attacks["Claw"].get("effects") != [{"name": "Knockdown", "reference": "/action/knockdown-monster-core"}]:
        raise SystemExit("Adamantine Dragon Knockdown is not attached to its claw Strike")
    if "Grab" in dragon_abilities or "Knockdown" in dragon_abilities:
        raise SystemExit("Adamantine Dragon repeats its Strike effects as separate abilities")
    if dragon_data.get("loreSkills") != [{"name": "Mining Lore", "value": 16}]:
        raise SystemExit("Adamantine Dragon is missing its named Lore skill")

    animated_armor = by_slug["animated-armor-monster-core"]
    if animated_armor["data"].get("hardness") != 9:
        raise SystemExit("Animated Armor is missing Hardness")
    if not {"mental", "vitality", "void"}.issubset(linked_labels(animated_armor["data"].get("immunities") or [])):
        raise SystemExit("Animated Armor is missing construct immunities")

    zombie = by_slug["zombie-shambler-monster-core"]
    if "mental" not in linked_labels(zombie["data"].get("immunities", [])):
        raise SystemExit("Zombie Shambler is missing its mindless immunity")

    for creature in creatures:
        data = creature.get("data", {})
        traits = set(data.get("traits") or [])
        immunities = linked_labels(data.get("immunities") or [])
        if "mindless" in traits and "mental" not in immunities:
            raise SystemExit(f"mindless creature is missing Mental immunity: {creature['slug']}")
        if "swarm" in traits and not {"grabbed", "prone", "restrained"}.issubset(immunities):
            raise SystemExit(f"swarm creature is missing condition immunities: {creature['slug']}")

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
    creature_view = (REPO / "views/partials/creature-primary.md").read_text(encoding="utf-8")
    if "ability.reference" not in ability_view:
        raise SystemExit("shared creature ability names are not linked")
    if (
        "/trait/{{trait}}" not in ability_view
        or (
            "/trait/{{trait}}" not in attack_view
            and "/trait/{% if trait" not in attack_view
        )
    ):
        raise SystemExit("creature ability or attack traits are not linked")
    if (
        "/action/recall-knowledge-player-core" not in creature_view
        or "data.recallKnowledge.dc" not in creature_view
        or "/trait/{{data.recallKnowledge.subject}}" not in creature_view
        or "data.languages" not in creature_view
        or "/rule/languages-rules-2080" not in creature_view
        or "/rule/skills-rules-2276" not in creature_view
        or "/rule/{{key}}-skill-player-core" not in creature_view
        or "/rule/lore-skill-player-core" not in creature_view
        or "/language/{{language}}" not in creature_view
    ):
        raise SystemExit("creature identity fields are not separated in the stat block")
    if (
        "data.skills or data.loreSkills" not in creature_view
        or "[{{skill.name}}](/rule/lore-skill-player-core)" not in creature_view
        or "[**Lore**](/rule/lore-skill-player-core)" in creature_view
    ):
        raise SystemExit("named Lore skills are not integrated into the Skills field")

    secondary_view = (REPO / "views/partials/creature-secondary.md").read_text(encoding="utf-8")
    if "/rule/immunity-rules-2313" not in secondary_view or "/rule/resistance-rules-2318" not in secondary_view:
        raise SystemExit("creature defenses are missing quick-rule links")
    if (
        "[{{immunity|lowercase}}](/rule/immunity-rules-2313)" in secondary_view
        or "[{{ key|map: 'Damage'|lowercase }}](/rule/resistance-rules-2318)" in secondary_view
    ):
        raise SystemExit("individual creature defenses still point to a generic category rule")
    if " contains " in attack_view:
        raise SystemExit("creature attack view uses an unsupported template expression")
    for route_fragment in (
        "range-and-reach-rules-2379",
        "trait == 'reach-10'",
        "trait == 'reach-15'",
    ):
        if route_fragment not in attack_view:
            raise SystemExit(f"creature attack view is missing parameterized routing: {route_fragment}")

    trait_slugs = {record["slug"] for record in records("traits.json")}
    attack_trait_routes: dict[str, str] = {}
    for expression, destination in re.findall(
        r"\{% if ([^%]+) %\}([a-z][a-z0-9-]*)\{% else %\}",
        attack_view,
    ):
        for slug in re.findall(r"trait == '([^']+)'", expression):
            attack_trait_routes[slug] = destination
    for creature in creatures:
        for attack in creature.get("data", {}).get("attacks", []):
            for trait in attack.get("traits", []):
                slug = str(trait).strip().casefold().replace("_", "-").replace(" ", "-")
                family = parameterized_trait_family(slug)
                if family and (
                    attack_trait_routes.get(slug) != family
                    or family not in trait_slugs
                ):
                    raise SystemExit(
                        f"parameterized attack trait has no canonical destination: "
                        f"{creature['slug']}: {slug}"
                    )

    skill_rules = {
        rule["slug"]: rule
        for rule in records("rules.json")
        if rule.get("slug", "").endswith("-skill-player-core")
    }
    if len(skill_rules) != 17:
        raise SystemExit("individual Player Core skill quick references are incomplete")
    for slug, rule in skill_rules.items():
        description = str(rule.get("descr") or "")
        if (
            len(description) < 200
            or "Complete " in description
            or re.search(r"\]\(https?://", description)
            or rule.get("attributes", {}).get("contentOrigin") != "Player Core (ORC)"
            or rule.get("data", {}).get("referenceUrl")
        ):
            raise SystemExit(f"skill reference is not imported Player Core content: {slug}")

    items = {record["slug"]: record for record in records("items.json")}
    adamantine_weapon = items.get("adamantine-weapon-gm-core", {})
    if (
        adamantine_weapon.get("name") != "Adamantine Weapon"
        or adamantine_weapon.get("data", {}).get("subcategory") != "preciousMaterialWeapon"
        or adamantine_weapon.get("attributes", {}).get("contentOrigin") != "GM Core (ORC)"
        or re.search(r"\]\(https?://", str(adamantine_weapon.get("descr") or ""))
    ):
        raise SystemExit("Adamantine Weapon is not an imported internal GM Core reference")

    creature_form = form("creature.json")
    creature_fields = field_attributes(creature_form)
    if not {
        "data.hardness",
        "data.languagesDetails",
        "data.loreSkills",
        "data.recallKnowledge.subject",
    }.issubset(creature_fields):
        raise SystemExit("creature editor does not expose restored metadata")
    if "data.hardness" not in secondary_view:
        raise SystemExit("creature view does not render Hardness")

    attack_form = form("partials/attack.json")
    if "effects" not in {
        str(section.get("attribute")) for section in attack_form.get("sections", [])
    }:
        raise SystemExit("attack editor does not expose linked Strike effects")
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
        f"{sense_reference_count} linked senses, and spell/ritual editor previews"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
