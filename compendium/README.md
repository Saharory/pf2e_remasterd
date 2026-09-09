# Public ORC compendium

This directory contains Encounter+ modules made from game mechanics and
functional rules text that Paizo released under the Open RPG Creative (ORC)
License. It intentionally does not contain source PDFs, extracted page text,
watermarks, book art, maps, setting chapters, adventures, or creature lore.

The generated modules live in `packs/`. Each pack carries its own ORC and
Community Use notices so those terms and credits travel with an individual
`.module` file. The aggregate ORC notice is in
[ORC-NOTICE.md](ORC-NOTICE.md), and the upstream source and license review is
recorded in [sources.json](sources.json).

## What is included

- actions, rules, traits, conditions, and afflictions
- ancestries, heritages, backgrounds, classes, archetypes, and feats
- spells and rituals
- equipment and other items
- mechanical creature, NPC, hazard, and vehicle statistics
- functional text required to use those game elements

## What is excluded

- all source-book art, maps, page images, fonts, and trade dress
- creature and ancestry lore, class introductions, setting prose, and
  background story prompts
- deity records and other predominantly setting-based records
- private PDF extraction fields and source-site implementation identifiers
- OGL-only books, including *Rage of Elements*

Names that identify Paizo game elements are descriptive references only and
remain Paizo property. See [COMMUNITY-USE-NOTICE.md](COMMUNITY-USE-NOTICE.md).

## Rebuilding and validation

The repository does not contain private source files. Given a separately
prepared structured staging directory, rebuild and validate with:

```sh
python3 tools/build_public_orc_compendium.py --source /path/to/private/structured-modules
python3 tools/validate_public_orc_compendium.py
```

The builder uses a fail-closed source allowlist. A new book is not included
until its ORC status, required attribution, and record types are reviewed.
