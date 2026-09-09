# Pathfinder Second Edition Remaster system for Encounter+

This repository tracks the **game-system layer only**: Encounter+ entity
schemas, forms, views, styles, scripts, localization, and packaging metadata.
Compendium entries generated from rulebooks, Archives of Nethys, or other data
sources are deliberately maintained as separate modules and are not part of
this repository.

The current branch is a local development baseline derived from
[`encounterplus/pf2e`](https://github.com/encounterplus/pf2e). It is not yet a
publication-ready open-source release. See [LEGAL-REVIEW.md](LEGAL-REVIEW.md)
for the licensing issues that must be resolved before a public release.

## Repository boundary

Included here:

- Encounter+ system configuration and entity definitions
- forms and views, including Remaster-specific entity types
- light/dark presentation and accessibility-oriented styling
- character and creature presentation logic
- system icons, fonts, and visual assets currently inherited from upstream
  (pending asset-license review)

Kept outside this repository:

- PDFs, EPUBs, extracted text, watermarks, and user-owned source files
- generated compendium modules and packaged `.module` archives
- Archives of Nethys caches
- the PF2E for Foundry VTT source/data checkout
- installable `.system` archives and personal campaign data

## Publication status

The base system is safe to develop and version locally. Do not publish a
release until the upstream code license, bundled font licenses, visual-asset
provenance, Paizo notices, and project contact information are resolved.

This project is intended to remain free and non-commercial.
