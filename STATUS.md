# Current status

Last updated: 2026-10-04

- Branch: `remaster-community-base`
- Package version: `0.9.01`; release preparation, version changes, push, tags,
  and publication require explicit user approval. No release approval yet.
- Current test package: `dist/test/pf2e-remaster.system`, rebuilt with the
  system-wide form refresh repair, explicit duration option maps/inline choices,
  and normal HTML display. All packaged forms
  match their source files; records, configuration, and version are unchanged.
  SHA-256: `f22e831dd12f7e2fb1365a9bae4279d8c7d643b6c4843a590fd5b45dc28c7fb9`.
- Source checks: the canonical `python3 tools/eplus_dev.py check --json` passes
  with 82 definition files and every maintained validator, including 22 ORC
  packs / 17,359 records, 681 OGL records, creature editability/spellcasting,
  spell durations/areas, hazard/vehicle mechanics, and four UI regression files.
  This host's virtualenv points to a missing Python. Run with
  `PYTHONPATH=/private/tmp/pf2e-verification-deps` (pinned `json5==0.15.0`) and
  `NODE=/Users/saharyona/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node`.
- Native testing: user tests on Mac, Encounter+ 5.0.8 (4530). The user performs
  all further app tests; do not run agent UI automation or visual app inspection.
  Analyze an attached image/recording only when explicitly requested.

- Confirmed refresh repair: object-bound nested forms retained stale rows and
  summaries after mutations. Immunities New Entry/Delete reached the editor
  data but required leaving/reopening to redraw, as shown in the user's
  supplied recording. A native-view-only diagnostic did not help; HTML display
  was ruled out for that failure. The next candidate removed the object scope
  from the Skills/Immunities parent forms and qualified their controls through
  the full entity paths. The user confirms that candidate works and explicitly
  requested applying it throughout the system. Treat that as confirmation of
  the tested redraw behavior, not proof of the app's internal cause.
- System-wide application: all 22 nested form pages now retain the parent
  context. Movement (Ancestry, Character, Creature), Recall Knowledge, and item
  activation use fully qualified paths. Field-level list pages for creature
  senses/weaknesses/resistances, deity lists, and hazard/vehicle immunities now
  use explicit form wrappers with root-bound list sections. Skills/Immunities
  retain the confirmed repair; spell Area/Duration already used root context.
  Entry forms remain relative to their own list row, including references and
  quantities. A before/after traversal verified that every resolved storage
  path is identical, including all list-entry paths. No content rebuild or
  migration is needed. The maintained creature suite checks context preservation
  throughout the forms and guards the shared movement/activation/recall paths.
  Skills/Immunities are native-confirmed; other extensions need user spot checks.
- Separate text-edit persistence issue: small name edits and selecting existing
  text then pasting a replacement can fail to save. The user reproduced the
  single-character saving failure in official D&D as well. Clearing the text
  first, then pasting, works even if the final name differs by one letter;
  there is no demonstrated minimum edit-size rule. Waiting/focus changes and
  a larger textArea control did not help. Keep normal name controls. This issue
  is not claimed fixed by the refresh repair; retain the confirmed workaround
  unless a new user test establishes otherwise.
- Creature editor: lossless structured controls expose special senses, inventory
  item references/quantities, immunity references/custom text, rituals, named
  Lore inside Skills, and Recall Knowledge subject/skill pairs. Language and
  special-save notes are labeled, defenses use Type/Value, and abilities expose
  Description, optional Trigger, and Effect while retaining source compatibility.
  Existing source fields remain intact through generated mirrors. The earlier
  Skills section decoding error is fixed; native Edit Creature/Skills opens.
  Confirmed user passes: Lore modifier persistence, Items quantity editing,
  Items/Immunities removal through Mac's Copy/Delete context menu, and Resilient
  Form Effect editing, save/reopen, and stat-block rendering with Trigger intact.
- Reference repair: native selections can include source-name spaces, e.g.
  `/item/chest-player-core/player core`. All nine dynamic creature Markdown
  destinations now use angle wrappers, preserving valid links with spaces or
  parentheses. Foundation Markdown checks and the maintained regression pass.
  The user confirms Chest renders correctly and opens the expected item.
  Other editor reference types still need native verification.

- Spell editor compatibility: the nested area-size input is a decimal field
  inside a valid group, with native feet conversion in the editor and summary.
  Source checks recursively validate native section/field types. This fixes the
  earlier area-form decoder error without changing stored spell data.
- Spell loading: all 1,404 spells preserve printed prose in `data.durationText`.
  Native duration descriptors configure 809 clear timers/next-turn endings;
  595 spells load as manually removed reminders with only
  `data.durationUnit: "round"`, no value or expiry type. Read-only inspection
  of the installed loader established support for that unit-only descriptor.
  Sustained durations supply a maximum timer, not automatic Sustain. The 308
  map-area templates remain intact; deferred upstream conversion is unchanged.
- Duration regression, latest native result: the user confirms readable spell
  and status-effect duration names after restoring explicit option maps; the
  other requested duration checks pass (save/reopen and preview). Only Spell
  Time still requires leaving/reopening before value/unit controls appear.
  The native status-effect editor expands immediately. The rejected field-picker
  candidate added navigation; retain inline choices and expanding controls.
- D&D comparison and current regular package: the installed `dnd5e.system` and local
  `../dnd5e-source/forms/spell.json` use an unbound parent form, full entity
  paths, package-declared picker maps in `types.json`, and a full template
  returning `true` for visible timer sections. PF2E already shares the context
  pattern; it had removed its own duration maps and used bare visibility
  comparisons. Restore the complete `DurationType` / `DurationUnit` maps (also
  present in `../upstream-pf2e/types.json`) and use
  `{% if data.durationType == 'time' %}true{% endif %}` for both timer sections.
  Stored native values stay identical. Ordering lists all seven native types
  and four units. English/French labels, singular/plural summaries, None/reset,
  and parent help remain intact. No additional picker screens or controls.
  D&D also shows timer controls for an unset type, so this comparison does not
  prove PF2E's live Time transition. Source checks guard complete option maps,
  labels, ordering, layout, and storage. The user confirms the option-map repair,
  but matching the visibility template did not repair live Time expansion.
  The user also confirms that official 5e Instantaneous to Concentration
  requires leaving/re-entering its Duration page before timer controls appear.
  The same failure is therefore reproduced in an official system; distinguish
  this shared conditional-form refresh issue from the fixed PF2E option labels.
  Focused and canonical checks pass. The rebuilt archive changes only
  `forms/spell.json` and `types.json`; all other entries are identical.
- Native status-duration inspection: the working editor is app-owned. PF2E's
  `forms/status-effect.json` adds stage/rarity/traits/printed duration; it does
  not define the expiry picker or expanding timer controls. The bundled 5e
  archive has no corresponding status-effect duration form. Read-only Swift
  metadata inspection of the installed app identifies a separate `DurationForm`
  with `_duration`, `_durationUnit`, and `_durationType` properties, alongside
  `StatusEffectForm`. Generic custom editors instead use `EntityEmbeddedForm`
  and `EntityFormSection` with a definition and `_data`. This confirms separate
  components, not the internal cause of the missed redraw. The public
  [FormDefinition schema](https://docs.encounter.plus/reference/schema/form-definition/)
  exposes no duration field or hook to embed/call `DurationForm`. No supported
  way to reuse that native page in a spell's JSON form was found. Keep the
  root-form diagnostic pending; do not invent unsupported refresh keys or
  claim the native component was copied/fixed.
- Focused refresh diagnostic: `dist/test/pf2e-remaster-duration-root-test.system`
  temporarily moves the same three duration sections directly into the main
  Spell form. It changes only `forms/spell.json` in the regular archive, keeps
  the same stored paths/labels/visibility expressions, and remains `0.9.01`.
  Source: `dist/test/diagnostics/spell-duration-root-form.json`; native form
  definition validation passes. SHA-256:
  `479a20798aae760aad8c9479a5902ee7cc8596b471258c8f38713c8656bac157`.
  No main-form layout change has been applied to the regular source/package.
  Next user test: open Edit Spell, scroll to Token Effect Duration directly on
  the main page, select Until Dispelled then Time, and report whether the value
  and units appear immediately. This distinguishes a nested-page refresh
  failure from general section visibility. Do not repeat the confirmed 5e test.
- Existing/custom spell migration: `migrations/0.9.02.js` is prepared and tested
  against all 1,404 durations; it preserves prose and GM settings and is
  idempotent. It remains inactive while the package is `0.9.01`. Legacy duration
  prose remains readable/editable, and previously converted spells with empty
  settings gain a manual descriptor when the future migration runs.
- Confirmed native spell passes: Haste's 1-minute timer; Shield's expiry at the
  start of the loaded token's next turn; Command surviving through the target's
  next turn and expiring at its end; Heal/Mystic Armor without countdowns,
  persisting through several turns, and manual removal. Switching a timer to
  manual persists and behaves correctly, although its preview was stale before
  the display/refresh changes. Distinct caster/source assignment remains untested.

- Next user checks after importing the regular test package: Weaknesses and
  Resistances New Entry/Delete, Recall Knowledge, speed editing, item activation,
  and a representative deity/hazard/vehicle list. Verify immediate redraw plus
  save/reopen; source checks alone do not establish native passes. Remaining
  earlier coverage: special-sense/reference editing, empty Immunities/Rituals,
  ritual links, creature spell links, native duration labels/preview, custom
  manual spell loading, distinct caster/source-relative expiry, and Fireball /
  Detect Magic area placement with no token selected. Avoid repeating confirmed
  passes unless a new regression or scope change warrants it.
- Current product priority: continue the complete data audit and review upstream
  compatibility before releases. See `ROADMAP.md` for product decisions.

Update this file at a material handoff, app-test result, upstream merge, or
release. Do not use it as a chronological work log.
