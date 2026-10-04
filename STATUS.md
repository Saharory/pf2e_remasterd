# Current status

Last updated: 2026-10-04

- Branch: `remaster-community-base`
- Package version: `0.9.01`; release preparation, version changes, push, tags,
  and publication require explicit user approval. No release approval yet.
- Current test package: `dist/test/pf2e-remaster.system`, rebuilt with the
  system-wide form refresh repair, readable spell duration labels/inline choices,
  and normal HTML display. All packaged forms
  match their source files; records, configuration, and version are unchanged.
  SHA-256: `69d96f5705d7509a40384b9ef81c2455433513a89c4eb82bb84c31671647b14c`.
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
- Duration display: spell editing/summary use built-in `DurationType` and
  `DurationUnit`, with native Saving Throw, source/target turn endings, Time,
  Until Dispelled, and None/reset. Native type registries are not overridden.
  User's latest screenshot exposes raw `DurationType.*`, `DurationUnit.*`,
  and `Common.Unit` keys; removing the package translations incorrectly assumed
  the engine supplied these labels to custom forms. Restored all expiry/unit
  labels and Unit in English/French, plus singular/plural
  `durationunit.<unit>.one/other` keys observed in the earlier native preview.
  The spell summary uses those singular/plural keys. The unbound help input
  remains removed; help uses the parent's subtitle. Descriptors and records
  are unchanged. The native preview's own label lookup still needs user testing.
- Time selection regression: the user reports the same delayed update when
  selecting Time. The user rejected the field-picker candidate because it
  added navigation and explicitly requested the native-looking inline list.
  Current Duration page directly lists Saving Throw, Source End Next Turn,
  Source Start Next Turn, Target End Next Turn, Target Start Next Turn, Time,
  and Until Dispelled, ordered through the existing collection mechanism.
  Duration value and inline unit choices expand below Time using the direct
  `data.durationType == 'time'` visibility condition. Full entity paths,
  restored readable labels, plural summaries, and existing data are preserved.
  No extra type/unit picker page or new custom controls. The focused spell
  suite and canonical check pass; the latest archive changes only the spell
  form and option ordering. Pending user test: press Time and confirm immediate
  expansion, then save/reopen two minutes and switch to Until Dispelled.
  Native immediate expansion remains unconfirmed; source checks do not prove it.
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
