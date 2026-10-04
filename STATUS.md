# Current status

Last updated: 2026-10-05

- Follow-up in a separate chat: the user reported import bugs in **TRADE
  DEATH FOR LIFE** and **TREE OF LIFE AND DEATH** on 2026-10-05. Details and
  reproduction will be supplied there; neither issue has been investigated
  or fixed in this chat.
- Branch: `remaster-community-base`
- Package version: `0.9.01`; release preparation, version changes, push, tags,
  and publication require explicit user approval. No release approval yet.
- Requested baseline push completed on 2026-10-05: `4ea2835` is on
  `origin/remaster-community-base`, including the saved editor design roadmap.
  The subsequent spell-editor redesign is a separate local step.
- Standing user instruction (2026-10-05): always package each completed system
  implementation/fix for testing, even during the native-testing pause. Keep
  only the latest `.system` in `dist/test`; validate the replacement before
  deleting older systems. This supersedes the earlier pause-related package
  delivery restriction and is saved in `AGENTS.md`. Native testing remains
  user-controlled; no agent app automation is authorized.
- Current test package: `dist/test/pf2e-remaster.system`, rebuilt on 2026-10-05
  with the creature, item, and spell editor redesigns and previous system-wide
  refresh repairs, plus the improved attack/casting/usage summaries.
  Archive inspection/CRC/checksums pass; all 198 packaged source files match
  current source. It includes 18,041 records, including 1,404 spells. Version
  remains `0.9.01`. The three older named test systems were removed after the
  replacement passed verification; this is the only `.system` in `dist/test`.
  Companion manifest, summary, and checksums were refreshed.
  SHA-256: `2c1ac0de8439babd03252c3a30dd9df95c581797e1afba4ea0602cf2aeed507c`.
- Source checks: the canonical `python3 tools/eplus_dev.py check --json` passes
  with 83 definition files and every maintained validator, including 22 ORC
  packs / 17,359 records, 681 OGL records, creature editability/spellcasting,
  spell durations/areas, hazard/vehicle mechanics, and four UI regression files.
  Revalidated on 2026-10-05 with the repaired virtualenv and bundled Node via
  `../tools/project-env python tools/eplus_dev.py check --json`.
- Spell editor efficiency: source complete, native verification pending.
  Type/rank/rarity/traits now share the opening group. **Casting** keeps
  variable action selection and traditions direct, with casting notes,
  requirements, cost, and trigger in a root-context **Casting details** editor
  whose summary shows populated values. **Range & effect** keeps range, printed
  area, targets, defense, and printed duration direct. **Map & token effects**
  groups the existing template/timer links without adding a navigation level.
  Unconfigured casting details and map templates show localized **None**.
  All 21 controls retain their storage paths, input/picker types, visibility,
  defaults, and units. English/French labels are included; spell-area/duration
  and creature-editability checks pass, as does the canonical check. Records,
  migrations, native loading, and versions are unchanged. Item editor source
  work is now complete as described below.
  Pending user checks after the existing hotfix pause ends: open a new spell
  and add casting details; edit/save/reopen populated notes, requirements,
  cost, and trigger and inspect summary refresh/stat-block text; retain multiple
  cast-action selections; check direct range/defense/printed-duration edits;
  edit template shape/fractional size and numeric token expiry independently
  and verify summaries/save/reopen; check an older custom spell with prose in
  `data.duration`. These are future checks, not a request to resume testing.
- Item editor efficiency: source complete, user approved on 2026-10-05.
  The user reports no issues and much better organization. Individual
  save/reopen checks below were not separately reported.
  Category/level/rarity/traits/subcategory share the opening group. Price,
  usage, bulk, description, and category-specific equipment stats remain
  direct. Ammunition, onset, and crafting requirements share a root-context
  **Additional details** editor with a populated summary or localized **None**;
  it remains accessible for empty/custom items of every category. Equipment
  sections also expose populated exceptional properties after category changes,
  preserving zero-valued numeric stats. **Primary activation** edits the original
  `data.activation` fields; **Additional activations** keeps the separate named
  list at `data.activations`. Both remain available when empty. The primary
  summary now includes traits. The original `data.types` list is labeled
  **Variants**, with its entry schema unchanged. Top-level sections decrease
  from 12 to 10 and typical non-category rows from 15 to 13. All 38 bound
  controls preserve paths, input types, defaults, and units. English/French
  labels, focused editability regression, and canonical source checks pass.
  No content, migration, stat-block, or version changes were required.
  Pending user checks when native testing resumes: inspect new gear, armor,
  shields, and weapons; add/edit/clear ammunition, onset, and crafting details
  and verify summary refresh and save/reopen; edit primary activation including
  traits, create/delete named activations, and confirm they remain independent;
  edit variants and their level/price/bulk/crafting fields; change a category
  with populated equipment stats and ensure those values remain editable.
  No agent app automation is authorized. The user selected creatures next,
  ahead of shared abilities; no ability-editor redesign has begun.
- Creature editor efficiency: source complete, user tests pass on 2026-10-05.
  The user approved the four-tab layout and explicitly reported all tests
  passing. This native pass covers the layout/refresh iteration delivered in
  package SHA-256 `3a94378992e3f12f740c09a3cbfae84f97613e75f386659f7c9329dc5b88377b`;
  new summary rendering is a separate pending check below.
  Four native tabs organize the existing editors: **Identity** holds combined
  level/rarity/size/traits, Recall Knowledge, inventory, and interaction
  abilities; **Statistics** holds perception, senses, Skills/Lore, Speed,
  attribute modifiers, and languages/notes; **Defenses** holds AC/HP/hardness
  with explicitly labeled notes, saves/special modifiers, immunities,
  weaknesses/resistances, and automatic/reactive abilities; **Actions & Magic**
  holds attacks, spellcasting, rituals, and offensive/proactive abilities.
  Sections decrease from 18 to 15, at most four per tab. No additional subform
  layer, visibility restriction, or binding scope was introduced. Existing
  Skills/Lore, senses, immunity, weakness/resistance, movement, item, ability,
  attack/damage, spellcasting, and ritual editors remain intact. All 118 resolved
  bound controls, including nested list-entry partials, retain their paths,
  types, defaults, units, visibility, and list metadata in a before/after audit.
  The maintained creature regression now traverses tabs and guards every inline
  attribute, direct ordinary statistics, and all three separate ability lists.
  Focused editability/spellcasting and canonical source checks pass.
  English/French labels are included, and the Ractive typo is corrected.
  Content, migrations, rendering, and native loading are unchanged.
  The previously pending tab navigation, ordinary stats/notes, save/reopen,
  Lore/immunity/weakness/resistance/Speed refresh, inventory, ability-list,
  attack component, and grouped spell/ritual checks are covered by the user's
  reported all-tests pass. No agent app automation is authorized.
- Existing entry summaries: source complete, native verification pending.
  Attack rows now preview type/action cost, signed attack modifier, damage
  components with their original connectors and types/effects, and named
  effects; legacy printed damage and component formulas retain display
  fallbacks. Component rows explicitly show formula plus type/effect.
  Casting previews show DC, signed attack, focus points, and original rank-group
  labels; cleared text values omit their labels while zero remains visible.
  Ritual previews retain DC/rank groups. Spell and ritual group rows
  add at-will and usage/constant notes to their names. Entry rows localize rank
  and at-will labels, retain rank/modifier zero, and omit missing-rank labels.
  Character attack/casting rows use the same summaries; its navigation is
  unchanged. A before/after comparison verifies nine affected/referenced form
  trees preserve controls, bindings, types, defaults, units, visibility,
  picker mappings, and routes. Native if/for tags are balanced in 29 inspected
  row templates. The maintained editability regression guards summary coverage
  and zero-value visibility; focused editability/spellcasting and canonical
  source checks pass.
  Existing structured editors, ability name-only rows, tabs, references,
  content, migrations, stat blocks, and load behavior remain intact. No new
  nested screens were added; weakness/resistance wrappers retain the earlier
  native-confirmed implementation.
  Pending user check for this step: inspect attack previews with multiple
  damage types/effects, spellcasting DC/attack/focus/rank labels, and spell or
  ritual usage notes; change a value and verify its parent preview refreshes
  and persists on save/reopen. Check narrow-width wrapping and custom entries
  with missing ranks or zero modifiers. Native rendering is not confirmed by
  source checks. No agent app automation is authorized.
- Recent native feedback (2026-10-05): the user said the spell layout looks
  good apart from Cast actions offering Custom Options, and approved the item
  layout with no issues. The user subsequently approved creature tabs and
  reported all creature tests passing. Cast actions remains unchanged after
  the user aborted the attempted workaround; app picker behavior is deferred
  to another chat.
  This feedback does not confirm the earlier hotfix or a new app version.
- Native testing: user tests on Mac, Encounter+ 5.0.8 (4530). The user performs
  all further app tests; do not run agent UI automation or visual app inspection.
  Analyze an attached image/recording only when explicitly requested.
- Native testing stopped by the user on 2026-10-04. The user relays that the
  Encounter+ developer confirmed these issues are a bug introduced by the
  recent app update and expects a hotfix later on 2026-10-04. This is a reported
  upstream diagnosis/plan, not confirmation that a fix is released or passes.
  Await the user's return after installing the hotfix; do not request more
  testing or schedule monitoring automatically. Package completed system
  changes under the newer standing user instruction above.
  Preserve all existing passes, source checks, and failed-case reproduction.

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
  Skills/Immunities, creature Weaknesses/Resistances, and creature Speed are native-confirmed;
  other extensions need user spot checks.
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
  The user also confirms the complete Weaknesses/Resistances test: New Entry
  appears immediately, type/value edits update on return to the list, saved
  values persist and render in the stat block, and context-menu deletion
  redraws immediately and remains deleted after saving/reopening.
  Creature Speed also passes: Walk/Fly editing, immediate summary updates,
  save/reopen, and stat-block rendering. Recall Knowledge deletion works, but
  subject/skill picker checkmarks appear only after leaving/re-entering Recall
  Knowledge, so selection feedback fails. Its entry controls correctly use the
  row-relative `subject` / `skills` paths, a standard pattern also used by 5e
  list-entry forms. No binding error was identified. Clarification deferred
  while native testing is stopped:
  whether the selected value displayed in the entry editor updates immediately
  or also requires reopening. DC/stat-block/save verification is not yet
  confirmed; do not mark the whole Recall Knowledge test passed.
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
  The explicit option-map repair is native-confirmed; its visibility-template
  change did not fix the nested page. See the new partial candidate below.
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
  way to reuse that native page in a spell's JSON form was found. Do not invent
  unsupported refresh keys or claim the native component was copied/fixed.
- Confirmed root-form diagnostic: `dist/test/pf2e-remaster-duration-root-test.system`
  temporarily moves the same three duration sections directly into the main
  Spell form. It changes only `forms/spell.json` in the regular archive, keeps
  the same stored paths/labels/visibility expressions, and remains `0.9.01`.
  Source: `dist/test/diagnostics/spell-duration-root-form.json`; native form
  definition validation passes. SHA-256:
  `479a20798aae760aad8c9479a5902ee7cc8596b471258c8f38713c8656bac157`.
  The user confirms immediate Time expansion works there, and asks why the
  controls moved out of their section. The move was only to isolate the nested
  page. Do not adopt that main-page layout as the final design or repeat this
  confirmed test. The regular source retains the dedicated Duration page.
- Failed duration-page candidate: move its existing three sections to
  `forms/partials/spell-effect-duration.json` and reference that partial from
  the unbound parent form, matching the confirmed Skills/Immunities pattern.
  Resolving this partial exactly reproduces the previous JSON definition:
  layout, labels, conditions, summaries, and every stored path are identical.
  Read-only app metadata distinguishes `EntityPartialForm` (own model and
  form data) from `EntityEmbeddedForm` (definition and data). This supports
  testing a partial page; it does not establish which route the app selects
  or prove the redraw is fixed. The spell suite checks the dedicated partial
  route and all existing duration behavior. Focused and canonical checks pass
  (83 definitions, nine validators). The rebuilt archive adds only the new
  partial and changes `forms/spell.json`; every other entry is identical.
  Latest user result: it still requires leaving/re-entering to reveal Time
  controls. A partial reference does not avoid the missed redraw. Do not repeat
  this candidate or claim that the dedicated page now works. The main-page
  diagnostic remains the only confirmed immediate Time expansion.
- Duration-field decision: the user explicitly chose to keep printed duration
  and token expiry separate after the feasibility report. Do not consolidate.
  Audited all 1,404 spells: 694 plain timers, 56 turn-relative endings, 59 timed
  descriptions with additional wording, and 595 manual reminders covering 22
  distinct descriptions (including empty). The native value/type/unit fields
  alone are lossy: Haste's `1 minute` and Buzzing Bites' `sustained up to 1 minute`
  both store the same 1-minute timer; Mystic Armor's `until your next daily
  preparations` and Restyle's `unlimited` both store the same unit-only manual
  reminder. `data.durationText` retains the full descriptions. Do not delete or
  silently replace source duration prose. No consolidation was implemented.
- Nested Time refresh disposition: no reliable package fix preserving the
  existing dedicated page has been found. Keep that layout and use leaving /
  reopening as the workaround. The user accepts waiting for the Encounter+
  developer if this cannot be solved here; do not send further speculative
  packages or repeat the confirmed experiments. The local developer report
  is `NATIVE-FORM-REFRESH.md`, with exact steps, official 5e reproduction,
  passing controls, and a bounded inference about nested section invalidation.
  Nothing has been submitted or sent externally. Continue other verification
  independently; this known issue remains unresolved and no release approval
  has been given.
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

- On user-requested resumption after the app hotfix: record the new app version /
  build, then retest the previously failing cases first: nested Duration Time
  expansion, Recall Knowledge selection checkmarks/displayed values, and small
  text edits / selected-text paste persistence. Do not assume the hotfix resolves
  them until the user verifies. Then finish Recall Knowledge persistence /
  stat-block checks and continue item activation,
  and a representative deity/hazard/vehicle list. Verify immediate redraw plus
  save/reopen; source checks alone do not establish native passes. Remaining
  earlier coverage: special-sense/reference editing, empty Immunities/Rituals,
  ritual links, creature spell links, custom
  manual spell loading, distinct caster/source-relative expiry, and Fireball /
  Detect Magic area placement with no token selected. Avoid repeating confirmed
  passes unless a new regression or scope change warrants it.
- Current product priority: continue the complete data audit and review upstream
  compatibility before releases. See `ROADMAP.md` for product decisions.

Update this file at a material handoff, app-test result, upstream merge, or
release. Do not use it as a chronological work log.
