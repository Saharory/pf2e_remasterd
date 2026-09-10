# Pathfinder Second Edition Remaster system for Encounter+

This repository tracks the Encounter+ game system and its public ORC rules
compendium. It includes entity schemas, forms, views, styles, scripts,
localization, packaging metadata, and the source-by-source content packs used
to build the public release.

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
- 22 ORC source packs containing 17,301 mechanical records, with individual
  notices and attribution in [`compendium/`](compendium/); the normal release
  merges them into the `.system` package for a one-step baseline install
- one separately licensed OGL 1.0a module for *Rage of Elements*, containing
  679 additional mechanical records

Kept outside this repository:

- PDFs, EPUBs, extracted text, watermarks, and user-owned source files
- Archives of Nethys caches
- the PF2E for Foundry VTT source/data checkout
- installable `.system` archives and personal campaign data

## Publication status

The ORC compendium source is publication-scoped and validated separately from
the inherited system assets. Do not publish or upload a stand-alone binary
release until the upstream code license, bundled font licenses, and
visual-asset provenance are resolved. The release workflow validates and
builds candidates inside its runner, but both artifact upload and public
publication require the exact legal-clearance confirmation documented by the
workflow.

This project is intended to remain free and non-commercial.

## Public rules compendium

The [`compendium/`](compendium/) directory contains only reviewed
ORC-licensed mechanics and functional rules text. It excludes private PDFs,
watermarks, setting chapters, adventure text, art, maps, creature lore,
background story prompts, deity narrative, and OGL-only material. The ORC packs
deliberately exclude *Rage of Elements* because its current source edition is
OGL-only, even though its rules are Remaster-compatible. It is supplied as a
separate OGL 1.0a module with its own complete license and COPYRIGHT NOTICE.

Every ORC source pack carries its own ORC and Community Use notices. The OGL
module carries its separate OGL license and attribution. Descriptive use of
Paizo-owned names remains Paizo property and does not imply endorsement.

## Fast development loop

Install the one small development dependency once:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
```

Then use the compact development helper:

```sh
# Syntax, metadata, ORC/OGL boundary, and record-integrity checks
.venv/bin/python tools/eplus_dev.py check --json

# Show only the files that differ from the installed Mac system
.venv/bin/python tools/eplus_dev.py status --json

# Preview a checksum sync; this never deletes installed files
.venv/bin/python tools/eplus_dev.py sync-system --json

# Apply the checked definition-file sync
.venv/bin/python tools/eplus_dev.py sync-system --apply --json
```

After an applied sync, use Encounter+'s **Reload System** action. The semantic
Computer Use helper in `tools/encounterplus_ui_helper.mjs` performs that action
and targeted library checks without screen coordinates or full UI dumps.
Content records remain database-owned: rebuild and import only the affected
module when testing a content change.

## Building release files

The normal build creates two installable packages: one `.system` containing
the definitions and all reviewed ORC records, plus one separately licensed
*Rage of Elements* OGL module. It also creates the two update manifests,
checksums, and a machine-readable summary.

```sh
.venv/bin/python tools/eplus_dev.py check --json
.venv/bin/python tools/package_public_release.py
.venv/bin/python tools/eplus_dev.py inspect-release --json
```

For maintenance or source-by-source testing, pass `--individual-modules` to
also build the 22 ORC modules under `dist/individual/`. Those are not part of
the normal community installation because publishing both layouts would
duplicate the same entity IDs.

For a local clean-install test, `--test-shell` additionally creates a
content-free temporary system under `dist/test/`. It exists only as an unload
target while replacing the active PF2E system and is never included in release
checksums or the GitHub workflow artifact.
