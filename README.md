# Pathfinder Second Edition Remaster system for Encounter+

![Pathfinder Remastered Compatible — Unofficial](pf2e-banner.png)

This repository tracks the Encounter+ game system and its public ORC rules
compendium. It includes entity schemas, forms, views, styles, scripts,
localization, packaging metadata, and the source-by-source content packs used
to build the public release.

The current branch is an unofficial community test build derived from
[`encounterplus/pf2e`](https://github.com/encounterplus/pf2e). It is intended
for testing and upstream review, and is not an official Encounter+ release or
an indication of endorsement by Encounter+ or Paizo.

## Install the test build

1. Open the [latest GitHub release](https://github.com/Saharory/pf2e_remasterd/releases/latest).
2. Under **Assets**, download **`pf2e-remaster.system`**. Do not download the
   automatically generated “Source code” archives; those are repository files,
   not Encounter+ installers.
3. Open the downloaded `.system` file with Encounter+ and confirm the import.
4. In Encounter+, select **Pathfinder 2E Remaster** as the game system for the
   campaign you want to test.

The installed system checks this repository's latest release manifest for
newer versions. When Encounter+ reports an update, install it through the app
to replace the system files while keeping campaign data separate. During the
testing period, keep a backup of any campaign you care about before updating.

## Bookmark the PF2E Operations Center

The Operations Center is designed to run as a compact reference panel over the
game screen:

1. Open **Library** in Encounter+.
2. Open **Pages**, then select **PF2E Operations Center**.
3. Open its main/home page and tap the **bookmark** icon in the page toolbar.
   Bookmark the home page rather than one of its individual rule pages.
4. Return to the game screen and open **Bookmarks**.
5. Select **PF2E Operations Center** to open it in the compact panel.

Use the tiles to navigate. The breadcrumb trail at the top returns to any
earlier Operations Center section, while explicit rule links open the complete
compendium entry when the short table reference is not enough.

## Repository boundary

Included here:

- Encounter+ system configuration and entity definitions
- forms and views, including Remaster-specific entity types
- light/dark presentation and accessibility-oriented styling
- character and creature presentation logic
- system icons, fonts, and visual assets currently inherited from upstream
  (pending asset-license review)
- 22 ORC source packs containing 17,289 mechanical records, with individual
  notices and attribution in [`compendium/`](compendium/); the normal release
  merges them into the `.system` package for a one-step baseline install
- 679 separately marked OGL 1.0a records from *Rage of Elements*, bundled into
  the same system installer with their complete license and attribution
- source-aware internal cross-links across the 17,968 shipped entries: the
  first meaningful reference opens the matching condition, action, trait,
  spell, item, feat, rule, or other compendium entry without repeating the
  same destination throughout a page
- one canonical rules entry for parameterized traits such as Deadly, Fatal,
  Two-Hand, Versatile, Capacity, Thrown, and Volley, while each item keeps its
  complete die, range, or damage-type label
- a project-authored GM Tools collection containing an interactive Encounter
  XP Planner with party-size budgets, creatures, hazards, weak/elite
  adjustments, transparent overrides, direct Remaster rule links, and a
  copy-ready handoff to Encounter+'s native Total Experience award sheet
- a bookmarkable PF2E Operations Center made from internal system Pages, with
  compact-panel navigation, persistent breadcrumbs, a fast Quick Reference,
  an A–Z fallback index, and task-oriented guides for encounters, checks,
  conditions, exploration, downtime, creatures, hazards, magic, equipment,
  party advancement, and GM subsystems; explicit links open the unchanged full
  compendium entries only when exact rule text is needed

Kept outside this repository:

- PDFs, EPUBs, extracted text, watermarks, and user-owned source files
- Archives of Nethys caches
- the PF2E for Foundry VTT source/data checkout
- installable `.system` archives and personal campaign data

## Publication status

The GitHub packages are community testing builds, not releases in Encounter+'s
official in-app catalogue. The ORC compendium source is publication-scoped and
validated separately from inherited system assets. Upstream maintainers must
review the changes and confirm the inherited code, font, and visual-asset
licensing before any official adoption or distribution through Encounter+.

This project is intended to remain free and non-commercial.

## Public rules compendium

The [`compendium/`](compendium/) directory contains only reviewed
ORC-licensed mechanics and functional rules text. It excludes private PDFs,
watermarks, setting chapters, adventure text, art, maps, creature lore,
background story prompts, deity narrative, and OGL-only material. The ORC packs
deliberately exclude *Rage of Elements* because its current source edition is
OGL-only, even though its rules are Remaster-compatible. Those records are
merged into the same installer for convenience but retain their OGL markers,
complete license, and COPYRIGHT NOTICE.

Every ORC source pack carries its own ORC and Community Use notices. The OGL
dataset carries its separate OGL license and attribution. Descriptive use of
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
Content records remain database-owned: rebuild and import the combined system
archive when testing a content change, including generated Pages. The
Operations Center source is maintained in `tools/build_operations_center.py`;
run it before packaging whenever its navigation or summaries change.

## Building release files

The normal build creates one `.system` installer containing the definitions,
all reviewed ORC records, and the separately marked *Rage of Elements* OGL
records, plus the project-authored GM tools. It also embeds both license notice
sets and creates the update manifest, checksums, and a machine-readable summary.

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
