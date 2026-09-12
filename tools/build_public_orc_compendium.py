#!/usr/bin/env python3
"""Build publishable Encounter+ packs from a private structured staging area.

The private staging data may contain text extracted from owned PDFs, source-site
identifiers, and non-mechanical book prose.  None of those fields are copied
directly.  This builder keeps ORC-licensed rules and functional descriptions,
removes known Reserved Material fields, and writes deterministic JSON packs.

This is a publication aid, not legal advice.  New entity kinds and source books
must be reviewed before they are added to the allowlists below.
"""

from __future__ import annotations

import argparse
import copy
import json
import re
import shutil
import uuid
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = REPO.parent / "structured-modules"
DEFAULT_OUTPUT = REPO / "compendium" / "packs"
SOURCE_CATALOG = REPO / "compendium" / "sources.json"
ROOT_NOTICE = REPO / "compendium" / "ORC-NOTICE.md"
COMMUNITY_USE_NOTICE = REPO / "COMMUNITY-USE-NOTICE.md"

COLLECTION_KIND = {
    "actions.json": "Action",
    "afflictions.json": "Affliction",
    "ancestries.json": "Ancestry",
    "archetypes.json": "Archetype",
    "backgrounds.json": "Background",
    "classes.json": "Class",
    "conditions.json": "StatusEffect",
    "creatures.json": "Creature",
    "deities.json": "Deity",
    "domains.json": "Domain",
    "feats.json": "Feat",
    "hazards.json": "Hazard",
    "heritages.json": "Heritage",
    "items.json": "Item",
    "languages.json": "Language",
    "rituals.json": "Ritual",
    "rules.json": "Rule",
    "spells.json": "Spell",
    "traits.json": "Trait",
    "vehicles.json": "Vehicle",
}

# These kinds have a clean mechanical representation in ``data``.  Their
# top-level descriptions are primarily lore, appearance, history, or setting
# prose and are therefore removed wholesale.
STRIP_TOP_LEVEL_DESCRIPTION = {
    "Ancestry",
    "Class",
    "Creature",
    "Deity",
    "Hazard",
    "Vehicle",
}

# Deity narrative is removed wholesale. The structured rules block contains
# only the fields a GM needs to adjudicate cleric and sanctification mechanics;
# proper-name references remain Paizo Reserved Material under the accompanying
# community-use notice and are not offered under the ORC License.
EXCLUDED_KINDS: set[str] = set()

PRIVATE_OR_PROVENANCE_KEYS = {
    "rawText",
    "foundryId",
    "aonId",
    "aonUrl",
    "pdfPath",
    "sourcePath",
    "watermark",
}

FOUNDRY_MARKERS = (
    "@UUID[",
    "@Embed[",
    "@Check[",
    "@Damage[",
    "@Template[",
    "@Localize[",
    "Compendium.pf2e.",
    "[[/",
)

# Parameterized traits carry a value on the item (for example Deadly d8 or
# Versatile P), but the value does not create a different rules concept. Keep
# the complete label on the item and route every variant to one canonical trait
# entry. This also prevents the Traits collection from filling with identical
# descriptions for each die, range, or damage type.
PARAMETERIZED_TRAIT_NAMES = {
    "additive": "Additive",
    "attached": "Attached",
    "capacity": "Capacity",
    "deadly": "Deadly",
    "deflecting": "Deflecting",
    "entrench": "Entrench",
    "fatal": "Fatal",
    "fatal-aim": "Fatal Aim",
    "hefty": "Hefty",
    "integrated": "Integrated",
    "jousting": "Jousting",
    "scatter": "Scatter",
    "shield-throw": "Shield Throw",
    "thrown": "Thrown",
    "two-hand": "Two-Hand",
    "versatile": "Versatile",
    "volley": "Volley",
}

PARAMETERIZED_TRAIT_PATTERNS = (
    (re.compile(r"additive-?\d+$"), "additive"),
    (re.compile(r"attached-to-.+$"), "attached"),
    (re.compile(r"capacity-\d+$"), "capacity"),
    (re.compile(r"deadly-d\d+$"), "deadly"),
    (re.compile(r"deflecting-.+$"), "deflecting"),
    (re.compile(r"entrench-(?:melee|ranged)$"), "entrench"),
    (re.compile(r"fatal-aim-d\d+$"), "fatal-aim"),
    (re.compile(r"fatal-d\d+$"), "fatal"),
    (re.compile(r"hefty-\d+$"), "hefty"),
    (re.compile(r"integrated-.+$"), "integrated"),
    (re.compile(r"jousting-d\d+$"), "jousting"),
    (re.compile(r"scatter-\d+$"), "scatter"),
    (re.compile(r"shield-throw-\d+$"), "shield-throw"),
    (re.compile(r"thrown-\d+$"), "thrown"),
    (re.compile(r"two-hand-d\d+$"), "two-hand"),
    (re.compile(r"versatile-[a-z]+$"), "versatile"),
    (re.compile(r"volley-\d+$"), "volley"),
)

# Generic Core traits added from AoN originally received source-qualified
# slugs because their parameterized forms already occupied the short names.
GENERIC_TRAIT_SLUG_ALIASES = {
    "attached-player-core-trait-trait-539": "attached",
    "deadly-player-core-trait-trait-570": "deadly",
    "fatal-player-core-trait-trait-597": "fatal",
    "jousting-player-core-trait-trait-638": "jousting",
    "two-hand-player-core-trait-trait-718": "two-hand",
    "versatile-player-core-trait-trait-724": "versatile",
    "volley-player-core-trait-trait-730": "volley",
}

LEGACY_TRAIT_REPLACEMENTS: dict[str, str | None] = {
    "locathah": "athamaru",
    "metamagic": "spellshape",
    "negative": "void",
    "no-alignment": None,
    "positive": "vitality",
}

# Filled from the complete approved staging catalog before packs are built.
# This lets every source-qualified trait route resolve to the one canonical
# short slug even when the referenced trait lives in another source pack.
TRAIT_SLUG_ALIASES: dict[str, str] = dict(GENERIC_TRAIT_SLUG_ALIASES)
CANONICAL_TRAIT_SLUGS: set[str] = set()

TRAIT_ROUTE = re.compile(r"(/trait/)([a-z0-9-]+)")
INTERNAL_MARKDOWN_LINK = re.compile(r"\[([^\]]+)\]\((/[a-z-]+/[^)\s]+)\)")
RICH_TEXT_KEYS = {
    "classDescription",
    "classFeaturesText",
    "description",
    "rulesText",
    "summary",
    "text",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def load_catalog() -> dict[str, dict[str, Any]]:
    records = json.loads(SOURCE_CATALOG.read_text())
    if not isinstance(records, list):
        raise ValueError("compendium/sources.json must be a JSON array")
    result: dict[str, dict[str, Any]] = {}
    for record in records:
        if not isinstance(record, dict) or not record.get("id"):
            raise ValueError("each source must be an object with an id")
        source_id = str(record["id"])
        if source_id in result:
            raise ValueError(f"duplicate source id: {source_id}")
        if record.get("license") != "ORC-1.0a":
            raise ValueError(f"source is not ORC-approved: {source_id}")
        result[source_id] = record
    return result


def title_from_slug(value: str) -> str:
    return " ".join(part.capitalize() for part in value.replace("_", "-").split("-") if part)


def normalized_trait_token(value: str) -> str:
    value = value.strip().casefold().replace("_", "-").replace(" ", "-")
    return re.sub(r"-+", "-", value)


def parameterized_trait_family(value: str) -> str | None:
    token = normalized_trait_token(value)
    if token in PARAMETERIZED_TRAIT_NAMES:
        return token
    alias = GENERIC_TRAIT_SLUG_ALIASES.get(token)
    if alias:
        return alias
    for pattern, family in PARAMETERIZED_TRAIT_PATTERNS:
        if pattern.fullmatch(token):
            return family
    return None


def canonical_trait_slug(value: str) -> str:
    token = normalized_trait_token(value)
    replacement = LEGACY_TRAIT_REPLACEMENTS.get(token, token)
    if replacement is None:
        return token
    return (
        TRAIT_SLUG_ALIASES.get(token)
        or parameterized_trait_family(token)
        or replacement
    )


def normalize_trait_routes(value: str) -> str:
    def replace(match: re.Match[str]) -> str:
        return match.group(1) + canonical_trait_slug(match.group(2))

    return TRAIT_ROUTE.sub(replace, value)


def normalize_trait_values(traits: list[str]) -> list[str]:
    normalized_traits: list[str] = []
    seen: set[str] = set()
    for trait in traits:
        token = normalized_trait_token(trait)
        replacement = LEGACY_TRAIT_REPLACEMENTS.get(token, token)
        if replacement is None or replacement in seen:
            continue
        seen.add(replacement)
        # Parameter values remain on the item; only explicitly legacy names
        # are replaced in the displayed tag list.
        normalized_traits.append(replacement if token in LEGACY_TRAIT_REPLACEMENTS else trait)
    return normalized_traits


def normalize_trait_arrays(value: Any) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if key in {"traits", "tags"} and isinstance(child, list) and all(
                isinstance(item, str) for item in child
            ):
                value[key] = normalize_trait_values(child)
            else:
                normalize_trait_arrays(child)
    elif isinstance(value, list):
        for child in value:
            normalize_trait_arrays(child)


def add_trait_links(data: dict[str, Any]) -> None:
    traits = data.get("traits")
    if not isinstance(traits, list) or not all(isinstance(trait, str) for trait in traits):
        return
    normalized_traits = normalize_trait_values(traits)
    data["traits"] = normalized_traits
    data["traitLinks"] = []
    for trait in normalized_traits:
        slug = canonical_trait_slug(trait)
        data["traitLinks"].append(
            {
                "label": trait,
                "slug": slug if not CANONICAL_TRAIT_SLUGS or slug in CANONICAL_TRAIT_SLUGS else "",
            }
        )


def simple_trait_slug(value: str) -> str:
    value = value.casefold().replace("’", "'")
    value = re.sub(r"['\u2019]", "", value)
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-")


def trait_source_score(
    source_id: str,
    record: dict[str, Any],
    catalog: dict[str, dict[str, Any]],
) -> tuple[int, int, int]:
    """Prefer the record housed with the source named in its attribution."""
    pack_name = simple_trait_slug(str(catalog[source_id].get("name") or ""))
    credited = [
        simple_trait_slug(str(source.get("name") or ""))
        for source in record.get("sources", [])
        if isinstance(source, dict)
    ]
    source_match = any(name and (name in pack_name or pack_name in name) for name in credited)
    attrs = record.get("attributes") or {}
    foundry_id = str(attrs.get("foundryId") or "")
    return (
        int(source_match),
        int(not foundry_id.startswith("derived-Trait-")),
        int(bool(attrs.get("aonId"))),
    )


def canonical_trait_catalog(
    source_root: Path,
    catalog: dict[str, dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    """Build one globally canonical trait catalog, grouped by source pack."""
    candidates: dict[str, list[tuple[str, dict[str, Any]]]] = {}
    parameter_templates: dict[str, tuple[str, dict[str, Any]]] = {}

    for source_id in catalog:
        path = source_root / source_id / "traits.json"
        if not path.is_file():
            continue
        records = json.loads(path.read_text())
        if not isinstance(records, list):
            raise ValueError(f"{path} must contain a JSON array")
        for record in records:
            if not isinstance(record, dict):
                raise ValueError(f"{path} contains a non-object entry")
            prepared = copy.deepcopy(record)
            old_slug = normalized_trait_token(str(prepared.get("slug") or ""))
            family = parameterized_trait_family(old_slug or str(prepared.get("name") or ""))
            if family:
                TRAIT_SLUG_ALIASES[old_slug] = family
                is_generic = normalized_trait_token(str(prepared.get("name") or "")) == family
                if not is_generic:
                    parameter_templates.setdefault(family, (source_id, prepared))
                    continue
                prepared["name"] = PARAMETERIZED_TRAIT_NAMES[family]
                canonical_slug = family
            else:
                canonical_slug = simple_trait_slug(str(prepared.get("name") or ""))
                if not canonical_slug:
                    continue
                legacy = LEGACY_TRAIT_REPLACEMENTS.get(canonical_slug, canonical_slug)
                if legacy is None or legacy != canonical_slug:
                    TRAIT_SLUG_ALIASES[old_slug] = legacy or canonical_slug
                    continue

            TRAIT_SLUG_ALIASES[old_slug] = canonical_slug
            prepared["slug"] = canonical_slug
            candidates.setdefault(canonical_slug, []).append((source_id, prepared))

    for family, (source_id, template) in parameter_templates.items():
        if family in candidates:
            continue
        prepared = copy.deepcopy(template)
        prepared["id"] = str(
            uuid.uuid5(uuid.NAMESPACE_URL, f"pf2e-remaster:canonical-trait:{family}")
        ).upper()
        prepared["name"] = PARAMETERIZED_TRAIT_NAMES[family]
        prepared["slug"] = family
        candidates[family] = [(source_id, prepared)]

    grouped: dict[str, list[dict[str, Any]]] = {source_id: [] for source_id in catalog}
    CANONICAL_TRAIT_SLUGS.clear()
    CANONICAL_TRAIT_SLUGS.update(candidates)
    for records in candidates.values():
        source_id, selected = max(
            records,
            key=lambda item: trait_source_score(item[0], item[1], catalog),
        )
        grouped[source_id].append(selected)
    for records in grouped.values():
        records.sort(
            key=lambda record: (
                str(record.get("name") or "").casefold(),
                str(record.get("slug") or ""),
            )
        )
    return grouped


def dedupe_entity_links(result: dict[str, Any]) -> None:
    """Keep only the first link to each destination in one displayed entry.

    Identical mirrored text (notably deity ``descr`` and ``rulesText``) is
    rewritten identically instead of treating the storage copy as a second
    displayed mention.
    """
    seen: set[str] = set()
    rewritten: dict[str, str] = {}

    def dedupe_text(value: str) -> str:
        if value in rewritten:
            return rewritten[value]

        def replace(match: re.Match[str]) -> str:
            label, route = match.groups()
            if route in seen:
                return label
            seen.add(route)
            return match.group(0)

        updated = INTERNAL_MARKDOWN_LINK.sub(replace, value)
        rewritten[value] = updated
        return updated

    result["descr"] = dedupe_text(str(result.get("descr") or ""))

    def visit(value: Any) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                if key in RICH_TEXT_KEYS and isinstance(child, str):
                    value[key] = dedupe_text(child)
                elif isinstance(child, (dict, list)):
                    visit(child)
        elif isinstance(value, list):
            for child in value:
                if isinstance(child, (dict, list)):
                    visit(child)

    visit(result.get("data"))


def clean_foundry_markup(value: str) -> str:
    """Convert leftover VTT-only references into readable plain text."""
    text = value

    def action(match: re.Match[str]) -> str:
        label = match.group(2)
        if label:
            return label
        return title_from_slug(match.group(1))

    def roll(match: re.Match[str]) -> str:
        label = match.group(2)
        formula = re.split(r"\s+#", match.group(1), maxsplit=1)[0].strip()
        return label or formula

    text = re.sub(
        r"\[\[/act\s+([a-z0-9-]+)(?:\s+[^\]]*)?\]\](?:\{([^}]+)\})?",
        action,
        text,
        flags=re.I,
    )
    text = re.sub(
        r"\[\[/(?:r|gmr)\s+(.+?)(?:\s+#[^\]]*)?\]\](?:\{([^}]+)\})?",
        roll,
        text,
        flags=re.I,
    )
    text = re.sub(r"@Embed\[[^\]]+\](?:\{([^}]+)\})?", lambda m: m.group(1) or "", text)
    text = re.sub(r"@UUID\[[^\]]+\](?:\{([^}]+)\})?", lambda m: m.group(1) or "referenced entry", text)
    text = re.sub(r"@Check\[([^\]]+)\](?:\{([^}]+)\})?", lambda m: m.group(2) or m.group(1).split("|")[0], text)
    text = re.sub(r"@Damage\[([^\]]+)\](?:\{([^}]+)\})?", lambda m: m.group(2) or m.group(1), text)
    text = re.sub(r"@Template\[[^\]]+\](?:\{([^}]+)\})?", lambda m: m.group(1) or "area", text)
    text = re.sub(r"@Localize\[([^\]]+)\]", lambda m: title_from_slug(m.group(1).rsplit(".", 1)[-1]), text)
    text = re.sub(r"\bCompendium\.pf2e\.[A-Za-z0-9_-]+\.Item\.", "", text)
    text = re.sub(r"\[\[/[^\]]+\]\](?:\{([^}]+)\})?", lambda m: m.group(1) or "", text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r" {2,}", " ", text)
    return text.strip()


def scrub_tree(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: scrub_tree(child)
            for key, child in value.items()
            if key not in PRIVATE_OR_PROVENANCE_KEYS
        }
    if isinstance(value, list):
        return [scrub_tree(child) for child in value]
    if isinstance(value, str):
        return normalize_trait_routes(clean_foundry_markup(value))
    return value


def background_mechanics(value: str) -> str:
    """Drop biographical prompts while preserving the selectable rules."""
    paragraphs = [part.strip() for part in re.split(r"\n\s*\n", value) if part.strip()]
    for index, paragraph in enumerate(paragraphs):
        folded = paragraph.casefold().replace("’", "'")
        if (
            "attribute boost" in folded
            or "ability boost" in folded
            or folded.startswith("you gain three free attribute")
            or folded.startswith("you and the gm can work out")
        ):
            return "\n\n".join(paragraphs[index:])
    return ""


def deity_rules_text(data: dict[str, Any]) -> str:
    """Create one display-only mechanics block without deity narrative prose."""
    # The staging cross-link pass may already have produced this mechanical
    # summary with safe Encounter+ links. Preserve it instead of flattening the
    # same structured values a second time.
    existing = str(data.get("rulesText") or "").strip()
    if existing:
        return existing

    def values(value: Any) -> str:
        if isinstance(value, dict):
            return ", ".join(str(item) for item in value.values() if item)
        if isinstance(value, list):
            return "; ".join(str(item) for item in value if item)
        return str(value or "")

    lines = []
    for label, key in (
        ("Areas of Concern", "areasOfConcern"),
        ("Edicts", "edicts"),
        ("Anathema", "anathema"),
        ("Divine Attribute", "divineAttribute"),
        ("Divine Font", "clericFont"),
        ("Sanctification", "sanctificationOptions"),
        ("Divine Skill", "divineSkill"),
        ("Favored Weapon", "favoredWeapon"),
        ("Domains", "domains"),
        ("Alternate Domains", "alternateDomains"),
        ("Cleric Spells", "spells"),
    ):
        rendered = values(data.get(key))
        if rendered:
            lines.append(f"**{label}** {rendered}")
    return "\n\n".join(lines)


def sanitize_entity(entity: dict[str, Any], expected_kind: str) -> dict[str, Any] | None:
    if entity.get("kind") != expected_kind:
        raise ValueError(f"expected {expected_kind}, found {entity.get('kind')!r}")
    if expected_kind in EXCLUDED_KINDS:
        return None

    result = scrub_tree(copy.deepcopy(entity))
    normalize_trait_arrays(result)
    result["system"] = "pf2e-remaster"
    result.setdefault("attributes", {})["license"] = "ORC-1.0a"

    if expected_kind in STRIP_TOP_LEVEL_DESCRIPTION:
        result["descr"] = ""
    elif expected_kind == "Background":
        result["descr"] = background_mechanics(str(result.get("descr") or ""))

    data = result.get("data")
    if isinstance(data, dict):
        add_trait_links(data)
    if isinstance(data, dict) and expected_kind in {"Ancestry", "Class"}:
        data["summary"] = ""
    if isinstance(data, dict) and expected_kind == "Deity":
        data["rulesText"] = deity_rules_text(data)
        # Keep deity mechanics in Encounter+'s original description field so
        # they render reliably in both the detail view and editor.
        result["descr"] = data["rulesText"]

    dedupe_entity_links(result)

    return result


def module_notice(source: dict[str, Any]) -> str:
    extra = "\n".join(f"- {line}" for line in source.get("additionalAttributions", []))
    if extra:
        extra = "\n" + extra
    return f"""# ORC Notice

This module is licensed under the ORC License located at the Library of
Congress at TX 9-307-067 and available online at various locations including
https://paizo.com/orclicense and https://azoralaw.com/orclicense. All
warranties are disclaimed as set forth therein.

## Attribution

This module is based on the following Licensed Material:

- {source['attribution']}{extra}

If you use the Adapted Licensed Material in this module in your own published
work, please credit it as follows:

Pathfinder Second Edition Remaster system for Encounter+ community compendium
© 2026 Saharory and contributors.

## Reserved Material

Reserved Material elements include all trademarks, registered trademarks,
proper nouns and terms derived from proper nouns, artwork, characters,
dialogue, settings, locations, organizations, plots, storylines, trade dress,
and all other elements designated as Reserved Material under the ORC License.
Paizo-owned names and marks appearing as descriptive references are not offered
under the ORC License and remain Paizo property; their use is governed by the
included Community Use notice.

## Expressly Designated Licensed Material

This module contains no Expressly Designated Licensed Material. The game
mechanics and functional rules text in this module are Adapted Licensed
Material under the ORC License.
"""


def module_community_use_notice() -> str:
    """Make the repository notice self-contained inside a module archive."""
    common = COMMUNITY_USE_NOTICE.read_text().split(
        "This notice applies to descriptive references", 1
    )[0]
    return (
        common
        + "This notice applies to descriptive references to Paizo-owned names and marks.\n"
        + "The game mechanics and functional rules text supplied with this module are\n"
        + "separately licensed under the ORC License; see the accompanying\n"
        + "`ORC-NOTICE.md`.\n"
    )


def aggregate_notice(catalog: dict[str, dict[str, Any]]) -> str:
    attributions: list[str] = []
    for source in catalog.values():
        attributions.append(f"- {source['attribution']}")
        attributions.extend(f"- {line}" for line in source.get("additionalAttributions", []))
    joined = "\n".join(attributions)
    return f"""# ORC Notice

The game-mechanics compendium in this directory is licensed under the ORC
License located at the Library of Congress at TX 9-307-067 and available
online at various locations including https://paizo.com/orclicense and
https://azoralaw.com/orclicense. All warranties are disclaimed as set forth
therein.

## Attribution

This compendium is based on the following Licensed Material:

{joined}

If you use the Adapted Licensed Material in this compendium in your own
published work, please credit it as follows:

Pathfinder Second Edition Remaster system for Encounter+ community compendium
© 2026 Saharory and contributors.

## Reserved Material

Reserved Material elements include all trademarks, registered trademarks,
proper nouns and terms derived from proper nouns, artwork, characters,
dialogue, settings, locations, organizations, plots, storylines, trade dress,
and all other elements designated as Reserved Material under the ORC License.
Paizo-owned names and marks appearing as descriptive references are not offered
under the ORC License and remain Paizo property; their use is governed by the
included Community Use notice.

## Expressly Designated Licensed Material

This compendium contains no Expressly Designated Licensed Material. The game
mechanics and functional rules text in the generated packs are Adapted Licensed
Material under the ORC License.
"""


def build_module(
    source_dir: Path,
    output_dir: Path,
    source: dict[str, Any],
    trait_records: list[dict[str, Any]],
) -> dict[str, int]:
    output_dir.mkdir(parents=True, exist_ok=True)
    counts: dict[str, int] = {}
    excluded = 0

    for path in sorted(source_dir.glob("*.json")):
        expected_kind = COLLECTION_KIND.get(path.name)
        if expected_kind is None:
            continue
        records = trait_records if expected_kind == "Trait" else json.loads(path.read_text())
        if not isinstance(records, list):
            raise ValueError(f"{path} must contain a JSON array")
        cleaned: list[dict[str, Any]] = []
        for record in records:
            if not isinstance(record, dict):
                raise ValueError(f"{path} contains a non-object entry")
            entity = sanitize_entity(record, expected_kind)
            if entity is None:
                excluded += 1
            else:
                cleaned.append(entity)
        if cleaned:
            (output_dir / path.name).write_text(
                json.dumps(cleaned, ensure_ascii=False, indent=2) + "\n"
            )
            counts[expected_kind] = len(cleaned)

    original_module = json.loads((source_dir / "module.json").read_text())
    module = {
        "id": original_module["id"],
        "system": "pf2e-remaster",
        "systemVersion": original_module.get("systemVersion", "1.2.10"),
        "name": source["name"],
        "slug": f"pf2e-remaster-{source['id']}",
        "category": "other",
        "descr": "ORC-licensed game mechanics and functional rules text for Encounter+.",
        "author": "Paizo Inc.; Encounter+ adaptation by Saharory and contributors",
        "version": original_module.get("version", "1.2.10"),
        "license": "ORC-1.0a",
        "licenseFile": "ORC-NOTICE.md",
        "communityUseNotice": "COMMUNITY-USE-NOTICE.md",
    }
    (output_dir / "module.json").write_text(json.dumps(module, ensure_ascii=False, indent=2) + "\n")
    (output_dir / "source.json").write_text(
        json.dumps(
            {
                "id": source["id"],
                "name": source["name"],
                "system": "pf2e-remaster",
                "license": "ORC-1.0a",
                "verification": source["verification"],
                "counts": counts,
                "excludedReservedMaterialRecords": excluded,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n"
    )
    (output_dir / "ORC-NOTICE.md").write_text(module_notice(source))
    (output_dir / "COMMUNITY-USE-NOTICE.md").write_text(module_community_use_notice())
    return counts


def main() -> int:
    args = parse_args()
    catalog = load_catalog()
    if not args.source.is_dir():
        raise SystemExit(f"private staging directory not found: {args.source}")

    trait_catalog = canonical_trait_catalog(args.source, catalog)

    if args.output.exists():
        shutil.rmtree(args.output)
    args.output.mkdir(parents=True)

    summary: dict[str, dict[str, int]] = {}
    for source_id, source in catalog.items():
        source_dir = args.source / source_id
        if not (source_dir / "module.json").is_file():
            raise SystemExit(f"approved source pack is missing: {source_dir}")
        summary[source_id] = build_module(
            source_dir,
            args.output / source_id,
            source,
            trait_catalog[source_id],
        )

    summary_path = args.output.parent / "summary.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    ROOT_NOTICE.write_text(aggregate_notice(catalog))

    total = sum(sum(counts.values()) for counts in summary.values())
    print(f"Built {len(summary)} ORC modules with {total} records in {args.output}")
    print(f"Excluded sources not in the ORC allowlist, including Rage of Elements (OGL-only)")
    print(f"Aggregate notice: {ROOT_NOTICE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
