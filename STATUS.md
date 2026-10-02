# Current status

Last updated: 2026-10-03

- Branch: `remaster-community-base`
- Package version: `1.701.9` (unchanged since the last published release)
- Latest completed local work: Solar Crow, Vault Builder, and Adult Executor
  Dragon now retain their published Recall Knowledge choices, attack traits,
  defenses, sanctification mechanics, and reach values. Telepathy, weapon
  adamantine, ability mechanics, and parameterized attack traits resolve to
  internal references; degree-of-success outcomes are visually grouped; and
  repeated prepared spell slots display once with an editable multiplication
  count. Recall Knowledge now stores and displays an editable creature subject,
  with Solar Crow and Vault Builder correctly identified as Elementals. The
  official GM Core Adamantine Weapon reference is included in-app.
- Automated baseline: the public ORC/OGL packs, package definitions, creature
  links and spellcasting, area templates, and maintained UI regressions pass
  through `python3 tools/eplus_dev.py check --json`.
- Native-app verification still required: import `dist/test/pf2e-remaster.system`
  and inspect the Elemental Recall Knowledge line on Solar Crow and Vault
  Builder, Solar Crow's Blinding Heat and attacks, Vault Builder's Telepathy,
  resistance, crystal shard, Craft Crystal Wand, and compact spell slots, and
  Adult Executor Dragon's sanctification, save/weakness fields, and reach links.
- Current product priority: continue the complete data audit and review upstream
  Encounter+ compatibility before releases. See `ROADMAP.md` for accepted,
  deferred, and completed feature decisions.

Update this file at a material handoff, app-test result, upstream merge, or
release. Do not use it as a chronological work log.
