# Current status

Last updated: 2026-09-29

- Branch: `remaster-community-base`
- Package version: `1.701.9` (unchanged since the last published release)
- Latest completed local work: the creature-stat audit now includes individual
  skill/language/defense/item links, item quantities, corrected attack and
  ability placement, nonduplicated ability-granted spells, and structured AoN
  action/trait metadata. Murajau, Lithic Locus, Solar Crow, Vault Builder, and
  Adult Executor Dragon are covered by focused regressions.
- Automated baseline: the public ORC/OGL packs, package definitions, creature
  links and spellcasting, area templates, and maintained UI regressions pass
  through `python3 tools/eplus_dev.py check --json`.
- Native-app verification still required: import `dist/test/pf2e-remaster.system`
  and check the reviewed creature pages, especially the new individual quick
  links and parameterized Versatile/Thrown trait destinations.
- Current product priority: continue the complete data audit and review upstream
  Encounter+ compatibility before releases. See `ROADMAP.md` for accepted,
  deferred, and completed feature decisions.

Update this file at a material handoff, app-test result, upstream merge, or
release. Do not use it as a chronological work log.
