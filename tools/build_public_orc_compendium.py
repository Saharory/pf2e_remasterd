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
    "Domain",
    "Hazard",
    "Language",
    "Vehicle",
}

# Deity records are predominantly proper-name/setting material.  Their rules
# can be added later only after a purpose-built Reserved Material scrubber.
EXCLUDED_KINDS = {"Deity"}

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
        return clean_foundry_markup(value)
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


def sanitize_entity(entity: dict[str, Any], expected_kind: str) -> dict[str, Any] | None:
    if entity.get("kind") != expected_kind:
        raise ValueError(f"expected {expected_kind}, found {entity.get('kind')!r}")
    if expected_kind in EXCLUDED_KINDS:
        return None

    result = scrub_tree(copy.deepcopy(entity))
    result["system"] = "pf2e-remaster"
    result.setdefault("attributes", {})["license"] = "ORC-1.0a"

    if expected_kind in STRIP_TOP_LEVEL_DESCRIPTION:
        result["descr"] = ""
    elif expected_kind == "Background":
        result["descr"] = background_mechanics(str(result.get("descr") or ""))

    data = result.get("data")
    if isinstance(data, dict) and expected_kind in {"Ancestry", "Class"}:
        data["summary"] = ""

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
    return (
        COMMUNITY_USE_NOTICE.read_text()
        .replace("in `compendium/packs`", "supplied with this module")
        .replace("`compendium/ORC-NOTICE.md`", "the accompanying `ORC-NOTICE.md`")
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


def build_module(source_dir: Path, output_dir: Path, source: dict[str, Any]) -> dict[str, int]:
    output_dir.mkdir(parents=True, exist_ok=True)
    counts: dict[str, int] = {}
    excluded = 0

    for path in sorted(source_dir.glob("*.json")):
        expected_kind = COLLECTION_KIND.get(path.name)
        if expected_kind is None:
            continue
        records = json.loads(path.read_text())
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

    if args.output.exists():
        shutil.rmtree(args.output)
    args.output.mkdir(parents=True)

    summary: dict[str, dict[str, int]] = {}
    for source_id, source in catalog.items():
        source_dir = args.source / source_id
        if not (source_dir / "module.json").is_file():
            raise SystemExit(f"approved source pack is missing: {source_dir}")
        summary[source_id] = build_module(source_dir, args.output / source_id, source)

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
