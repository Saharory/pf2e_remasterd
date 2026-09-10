# Pathfinder Second Edition Remaster system for Encounter+

This repository tracks the Encounter+ game system and its public ORC rules
compendium. It includes entity schemas, forms, views, styles, scripts,
localization, packaging metadata, and separately installable content packs.

The current branch is a community-maintained baseline derived from
[`encounterplus/pf2e`](https://github.com/encounterplus/pf2e). It is not yet a
stand-alone publication-ready release because the inherited code and visual
assets still need explicit license confirmation. See
[LEGAL-REVIEW.md](LEGAL-REVIEW.md) for that remaining review.

## Repository boundary

Included here:

- Encounter+ system configuration and entity definitions
- forms and views, including Remaster-specific entity types
- light/dark presentation and accessibility-oriented styling
- character and creature presentation logic
- system icons, fonts, and visual assets currently inherited from upstream
  (pending asset-license review)
- 22 ORC rules modules containing 17,302 mechanical records, with individual
  notices and attribution in [`compendium/`](compendium/)
- one separately licensed OGL 1.0a module for *Rage of Elements*, containing
  679 additional mechanical records

Kept outside this repository:

- PDFs, EPUBs, extracted text, watermarks, and user-owned source files
- Archives of Nethys caches
- the PF2E for Foundry VTT source/data checkout
- installable `.system` archives and personal campaign data

## Publication status

The ORC compendium source is publication-scoped and validated separately from
the inherited system assets. Do not publish a stand-alone binary release until
the upstream code license, bundled font licenses, and visual-asset provenance
are resolved.

This project is intended to remain free and non-commercial.

## Public rules compendium

The [`compendium/`](compendium/) directory contains only reviewed
ORC-licensed mechanics and functional rules text. It excludes private PDFs,
watermarks, setting chapters, adventure text, art, maps, creature lore,
background story prompts, deity narrative, and OGL-only material. The ORC packs
deliberately exclude *Rage of Elements* because its current source edition is
OGL-only, even though its rules are Remaster-compatible. It is supplied as a
separate OGL 1.0a module with its own complete license and COPYRIGHT NOTICE.

Every module carries its own ORC and Community Use notices. Descriptive use of
Paizo-owned names remains Paizo property and does not imply endorsement.

To validate or package the reviewed tree:

```sh
python3 tools/validate_public_orc_compendium.py
python3 tools/validate_public_ogl_compendium.py
python3 tools/package_public_release.py
```
