# Current status

Last updated: 2026-10-04

- Branch: `remaster-community-base`
- Package version: `0.9.01` (release not yet published)
- Latest completed local work: the creature editor now exposes lossless,
  structured controls for special senses, searchable inventory items and
  quantities, immunity references/custom text, and ritual lists. Named Lore is
  edited inside the same Skills page, Recall Knowledge binds its complete
  knowledge-to-skill pairs, language and special-save notes have clear labels,
  weakness/resistance entries use Type and Value, empty immunity and ritual
  states are explicit, and creature abilities have an optional Effect field.
  Existing source fields remain intact and the rendered stat-block information
  is preserved through generated editor mirrors and a compatibility migration.
  The Skills editor is nested in a valid Encounter+ group section, fixing the
  `sections[4].type` decoding error seen when opening Edit Creature, and its
  nested skill-map control now uses the same valid grouping. Creature ability
  editors separate source-backed Description, Trigger, and Effect fields while
  retaining the original text as a compatibility fallback; Trigger remains
  optional because both reactions and free actions can use it.
- Automated baseline: the public ORC/OGL packs, package definitions, creature
  links and spellcasting, area templates, and maintained UI regressions pass
  through `python3 tools/eplus_dev.py check --json`.
- Spell editor compatibility: fixed the nested area-size input that caused
  `sections[3].fields[8].form.sections[1].type` to reject `decimal`. Size is now
  a decimal field in a group, with native feet conversion in its editor and
  summary. Source checks validate section and field types recursively across
  every form and partial, including tabs, list editors, and field containers.
  This definition-only repair applies to existing/custom spells without a data
  migration. Upstream asset conversion remains deferred.
- Spell token loading: all 1,404 published spells now preserve printed duration
  prose in `data.durationText` and expose editable native effect-duration
  controls. The builders and focused population script configure 809 clear
  timers/next-turn endings using numeric `data.duration`, `data.durationUnit`,
  and `data.durationType`; the 308 map-area templates are unchanged. Sustained
  durations supply a maximum timer, not automatic Sustain. Instantaneous,
  ambiguous, daily-preparation, and other unsupported endings stay unset rather
  than receive invented timers. The user's preference for reminder effects on
  those spells is still open; the documented native Load action requires a
  duration, so a supported no-expiry loading contract is also needed.
- Existing/custom spell migration: `migrations/0.9.02.js` is prepared and tested
  against the same 1,404 duration strings as the Python builder. It preserves
  prose and existing native GM settings and is idempotent. The package remains
  `0.9.01`; the new migration cannot run until a future release claims its
  version. Legacy duration text remains readable and editable in the meantime.
- Spell verification: full source checks pass. `dist/test/pf2e-remaster.system`
  includes the new spell records/editor for user testing, at the unchanged
  `0.9.01` version. No visual app inspection is requested. Native loading/expiry
  still needs verification: select a token and load Haste, Shield, and Command;
  check timer units, turn endings, and the effect's caster/source for
  source-relative expiry. With no token selected, verify Fireball/Detect Magic
  still place areas. Check effect-duration editing and creature spell links.
- Native-app verification still required: import `dist/test/pf2e-remaster.system`
  and confirm Edit Creature opens without a decoding error, that Skills opens
  with its values and named Lore, and that a creature's rendered stat block is
  unchanged while Special
  Senses, Items, Immunities, Rituals, Lore, Recall Knowledge, and the optional
  ability Trigger and Effect fields can be edited through their new controls.
  In particular,
  verify the Item reference search, item quantity, the empty Immunities `None`
  row, the empty Rituals `New Entry` row, Recall Knowledge values, Lore inside
  Skills, and Type/Value labels for weakness and resistance entries.
- Current product priority: continue the complete data audit and review upstream
  Encounter+ compatibility before releases. See `ROADMAP.md` for accepted,
  deferred, and completed feature decisions.

Update this file at a material handoff, app-test result, upstream merge, or
release. Do not use it as a chronological work log.
