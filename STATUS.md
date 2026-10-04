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
- Verification resumed 2026-10-04 at source commit `db52118`: canonical checks
  pass with 82 definition files and all maintained validators. This host's
  existing virtualenv points to a missing Python; verification used the pinned
  `json5==0.15.0` in `/private/tmp/pf2e-verification-deps` via `PYTHONPATH` and
  the bundled Node executable via `NODE`. A temporary deterministic rebuild
  matched the original test package byte for byte. Original package SHA-256:
  `6641cb21a9ef1c90191a3f4c16815f3a004d73c4d48e77e602d270be6e31719f`.
  Native testing is in progress; no native pass is inferred from source checks.
  Release preparation awaits user approval; version changes, push, and publication
  also require explicit approval. The `0.9.02` migration remains inactive in
  this `0.9.01` test package.
- Native Skills/Lore result (user report, 2026-10-04): the Lore editor is
  reachable and the modifier change saves, but its list summary requires
  leaving and reopening Skills to redraw (image shows Mining Lore +25).
  Follow-up reveals a separate persistence failure: adding or deleting one
  letter in a Lore name or Items name does not persist even after reopening;
  larger edits such as a whole word do persist. Item quantity edits work
  without issues. Name editing is therefore failing native verification;
  the earlier successful modifier save does not establish name persistence.
  Waiting two seconds and moving focus to Quantity did not rescue the
  single-letter edit in the earlier package. User confirms testing on Mac;
  the local app is Encounter+ 5.0.8 (4530). No package
  script filters short name edits. The delayed summary redraw and lost text
  edits remain unresolved; a native input-commit/refresh issue is only a
  hypothesis. The `textArea` trial did not help, and the user found the larger
  boxes awkward; both name fields are restored to the normal text controls.
  Before the user stopped agent visual testing, a separate native copy named
  `Adamantine Dragon — Verification` was created (slug
  `adamantine-dragon---verification`). Its Lore row remained stale after a
  whole-name paste, but leaving Skills updated the main editor summary.
  Replacing the whole name with a value differing by one letter also reached
  that summary. These tests did not establish persistence after final Save;
  the copy's Lore edits were left unsaved when agent app interaction stopped.
  The automation's direct value setter did not commit an edit and is not
  equivalent to user typing. Follow-up user test: selecting existing text and
  pasting its replacement still fails to save. Explicitly deleting the text
  first, then pasting the new name, saves even when the final name differs by
  only one letter. This confirms clear-then-paste as a working user workaround;
  there is no demonstrated minimum edit-size rule. A missed native change
  notification/dirty-state update is a hypothesis, not a diagnosed cause. No
  documented text replacement or change-notification option was found in the
  form schema. Keep normal text fields and do not add another speculative
  control change. Native refresh and text replacement persistence remain
  unresolved. Chest rendering and navigation now pass by user confirmation.
  Continue the remaining creature and spell tests using the confirmed
  workaround as needed. Resilient Form's Trigger/Effect editing, save/reopen,
  and stat-block rendering pass by user confirmation (2026-10-04); editing
  Effect leaves Trigger unchanged. Haste's 1-minute native timer and Shield's
  expiry at the start of the loaded token's next turn pass by user confirmation
  (2026-10-04). Command's expiry at the end of the target's next turn and
  Heal/Mystic Armor reminders without countdowns, persistence through several
  turns, and manual removal also pass by user confirmation. Next user check:
  verify native duration choices/labels after the display repair, then confirm
  custom manual spell loading and Fireball/Detect Magic area placement with no
  token selected. Changing a timer to manual behaves correctly and persists
  by user report, but its native preview retains the previous timer label.
  Release preparation remains pending resolution and approval. The user will
  perform all further app testing; do not run visual inspection or UI automation.
- Broader native list result (user report, 2026-10-04): New Entry does not
  display immediately in Immunities, Weaknesses, or Resistances; leaving and
  reopening the section reveals it. User confirms these results on Mac with
  the rebuilt candidate. New-row refresh fails; data loss for the newly added
  entries is not established. Removal passes by user confirmation: right-click
  an Items or Immunities entry and use the native Copy/Delete menu. The earlier
  missing-delete report was an undiscovered UI gesture, not a missing feature.
  All affected arrays use native `list` controls. Official form documentation
  assigns add/remove behavior to the native list and exposes no separate
  deletion or refresh setting. No supported JSON refresh callback was found;
  do not claim field-type changes fixed the issue. Keep this package unreleased.
- Refresh comparison (user report, 2026-10-04): the built-in status editor
  saves and updates immediately, while PF2E spell/creature form summaries
  require leaving and reopening their screens. Treat this as a shared form
  problem to investigate separately from duration option labels. Read-only
  comparison with the installed official `dnd5e.system` found the same supported
  patterns: root-context spell Duration/Area forms without a parent attribute,
  object-bound nested monster forms with relative child paths, default text
  fields bound to `name`, and no explicit field/section IDs. Those patterns
  alone therefore do not identify a PF2E defect. Creature view transforms only
  derive armor, initiative, and combat details; they do not rewrite these edits.
  Controlled D&D user test now reports the same single-character saving
  failure, but immediate redraw for adding values/pressing plus. Text-edit
  persistence is therefore not unique to PF2E; delayed redraw still differs
  between the tested systems. Do not treat these as one diagnosed failure.
  One configuration difference remains to isolate: PF2E defaults to HTML
  detail views, while bundled D&D uses native views. A separate diagnostic
  `dist/test/pf2e-remaster-native-refresh-test.system` changes only its archived
  `config.json`, explicitly selecting native Creature and Spell views. All
  forms, records, scripts, and the `0.9.01` version are byte-identical to the
  regular test package; source configuration and the regular package are
  unchanged. Its SHA-256 is
  `67b16858b6b911ea4031d544a70daadca8a57516697dcf02dd21643638517c24`.
  Native layouts may look different during this test. Pending user check:
  import the diagnostic, edit a Lore modifier and return one level, then use
  Immunities New Entry; check immediate row refresh in both. Reimport the
  regular package to restore HTML views afterward. This is a diagnostic,
  not a claimed fix; no renderer change has been adopted for release. No
  further agent UI tests were made. Release preparation remains unapproved.
- Native editor reference result (user report, 2026-10-04): selecting Chest
  through the Items Reference picker renders literal Markdown in the saved
  stat block: `[Chest](/item/chest-player-core/player core) (2)`.
  The template interpolated a destination containing a raw source-name space.
  Apple Foundation's Markdown parser reproduces the failure and recognizes
  an angle-wrapped destination as a link to
  `/item/chest-player-core/player%20core`, keeping `Chest (2)` visible. The
  same parser check passes for a source suffix with parentheses and a route
  without a source suffix. Creature reference templates now wrap all nine
  dynamic destinations (Items, senses/acuity, immunities, abilities/attack
  effects, spells, and both ritual paths). The maintained creature regression
  protects these destinations. No record rewrite or migration is needed.
  Native app rendering and tapping Chest to open its correct item reference
  pass by user confirmation (2026-10-04). Other editor reference types still
  require native verification. Canonical source checks pass with all maintained
  validators. `dist/test/pf2e-remaster.system` was
  rebuilt at unchanged `0.9.01` with the duration display repair and normal name
  fields; types, spell form, duration summary, and both language files match
  the packaged copies. Current test package SHA-256:
  `daae2ea6ef1aca6db488ba1e76e5e46ff0f99b03a8a7dbc911a1fcbd20fc231a`.
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
  durations supply a maximum timer, not automatic Sustain. The other 595 spells
  load as manually removed reminders, as requested by the user. Their native
  descriptor contains only `data.durationUnit: "round"`, with no duration value
  or expiry type. Read-only inspection of the installed 5.0.8 loader confirms
  that a unit-only descriptor is recognized and passes absent value/type into
  the status effect; existing manual effects in the API also omit expiry data.
  This supplies no countdown or stat modifiers. The duration editor labels the
  empty expiry choice `None` using the native type registry and hides timer
  controls for it. `Until Dispelled` is also available as an explicit native
  expiry choice. Existing unit-only reminders retain their absent expiry type.
- Existing/custom spell migration: `migrations/0.9.02.js` is prepared and tested
  against the same 1,404 duration strings as the Python builder. It preserves
  prose and existing native GM settings and is idempotent. The package remains
  `0.9.01`; the new migration cannot run until a future release claims its
  version. Legacy duration text remains readable and editable in the meantime.
  Previously converted spells with empty native settings also gain a manual
  descriptor; GM-authored timers and expiry choices remain intact.
- Spell verification: full source checks pass. `dist/test/pf2e-remaster.system`
  includes the new spell records/editor for user testing, at the unchanged
  `0.9.01` version. No visual app inspection is requested. Native loading/expiry
  is partly verified by the user: Haste shows its 1-minute timer, and Shield
  persists until the start of the loaded token's next turn, then expires.
  Command persists through the target's next turn and expires at its end.
  Heal and Mystic Armor have no countdown, persist through several turns,
  and can be removed manually. Distinct caster/source assignment for
  source-relative expiry still needs verification. Switching a timer to manual
  persists and behaves correctly by user report; its preview label remains
  stale. Custom spell creation with manual duration still needs confirmation.
  With no token selected, verify Fireball/Detect Magic still place areas. Check
  effect-duration editing and creature spell links.
- Duration editor display repair (2026-10-04): the user's screenshots show
  stale native preview text `1 durationunit.minute.one` after a working manual
  change, and a spell-only menu that differs from the native effect editor.
  Spell editing and its summary now use Encounter+'s built-in `DurationType`,
  with native Saving Throw, source/target turn endings, Time, Until Dispelled,
  and None/reset for absent expiry. Removed the package's `DurationType` and
  `DurationUnit` definitions and their localization overrides so the engine
  supplies its own option labels and plural-aware unit strings. Removed the
  unbound help-text input which rendered as a misleading None row; help now
  uses the parent field's subtitle. No spell records or expiry descriptors
  were rewritten. The maintained spell suite protects the native registry,
  summaries, and preservation of the newly exposed native choices. All
  maintained validators pass through the canonical source check.
  Proper unit labels and native option parity still need user retesting;
  the broader stale native preview is unresolved, not claimed fixed by labels.
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
  Confirmed native passes so far: Lore modifier persistence (with stale row
  redraw), Items quantity editing, Items/Immunities removal via the Mac
  context menu, Chest reference rendering/navigation, and Resilient Form
  Trigger/Effect editing/persistence/rendering. The remaining controls and
  source-relative spell expiry still need user verification. Agent visual
  testing is disabled at the user's request.
- Current product priority: continue the complete data audit and review upstream
  Encounter+ compatibility before releases. See `ROADMAP.md` for accepted,
  deferred, and completed feature decisions.

Update this file at a material handoff, app-test result, upstream merge, or
release. Do not use it as a chronological work log.
