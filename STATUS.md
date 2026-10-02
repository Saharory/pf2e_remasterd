# Current status

Last updated: 2026-10-03

- Branch: `remaster-community-base`
- Package version: `1.701.9` (unchanged since the last published release)
- Latest completed local work: Recall Knowledge now derives every official
  identification subject from each creature's imported traits instead of using
  isolated overrides. The subject text remains plain because the same traits
  are already linked in the tag row, while accepted skills retain their internal
  quick links. The editable model supports multiple subjects; 1,633 creatures
  now have subjects and 124 correctly have more than one (for example, Dragon
  and Undead). The preceding Solar Crow, Vault Builder, Adult Executor Dragon,
  defense, attack-trait, prepared-spell, and named-Lore repairs remain intact.
- Automated baseline: the public ORC/OGL packs, package definitions, creature
  links and spellcasting, area templates, and maintained UI regressions pass
  through `python3 tools/eplus_dev.py check --json`.
- Native-app verification still required: import `dist/test/pf2e-remaster.system`
  and inspect the plain Elemental subject on Solar Crow/Vault Builder, Humanoid
  on Murajau, Dragon on Adult Executor Dragon, and Dragon + Undead on Wyrmwraith.
  Confirm the subjects remain editable, the skill names remain internal links,
  and the subject words do not duplicate the linked trait tags. The preceding
  creature repair checks still apply.
- Current product priority: continue the complete data audit and review upstream
  Encounter+ compatibility before releases. See `ROADMAP.md` for accepted,
  deferred, and completed feature decisions.

Update this file at a material handoff, app-test result, upstream merge, or
release. Do not use it as a chronological work log.
