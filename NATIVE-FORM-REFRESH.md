# Nested duration form does not refresh conditional sections

Original reproduction environment: Encounter+ 5.0.8 (4530), Mac.
Current installed app: 5.0.9 (4536), confirmed from read-only metadata on
2026-10-07. PF2E Remaster test package 0.9.01.
All native results below were reported by the user; no automated app testing
was performed.

Current status on 2026-10-07: the user reports that the app update fixed all
save-issue bugs. Imported named activation editing, save/reopen/rendering,
addition/deletion, and preservation of the other entry also pass. The user then
confirmed immediate nested Duration Time expansion and Recall Knowledge
selection checkmarks. The reported save/refresh failures are resolved in these
native tests. Retain the reproduction below as historical evidence.
The current explicit list bindings preserve the original storage paths;
removing the outer form scope does not leave entries unbound. No restoration
of that extra scope is recommended without a demonstrated regression.

Status on 2026-10-04: the user stopped native testing after the Encounter+
developer confirmed a bug introduced by the recent app update, with a hotfix
expected later that day. This diagnosis and release plan were relayed by the
user. At that point the hotfix had not been verified; the update above records
the later installed version and user result.

Update on 2026-10-05: the user resumed other functional verification without
the hotfix. Installed-app metadata still reports 5.0.8 (4530). These known
native failures remain unresolved; track redraw, persistence, and rendered
content separately while testing the remaining features.

## Reproduction

1. Edit a spell and open Token Effect Duration.
2. Select Until Dispelled. Leave and reopen this page to establish that the
   duration value and unit controls are hidden.
3. Select Time.

Expected: the duration value and unit choices appear immediately below the
type choices.

Actual in the original reproduction: Time is selected and persists, but those controls remain hidden until
the Duration page is closed and reopened. Names, saving, reopened values, and
duration previews now work correctly.

The user also reproduces this in official 5e: in Edit Spell → Duration, changing
Instantaneous to Concentration requires leaving/re-entering before the duration
value and units appear.

## Controls and isolation

- The app's status-effect Duration editor expands correctly on selecting Time.
- Moving the same PF2E duration sections to the main spell form makes the
  expansion immediate. No stored paths or conditions were changed.
- The nested parent has no `attribute`; controls use the full paths
  `data.durationType`, `data.duration`, and `data.durationUnit`.
- Bare comparisons and the full visibility template used by official 5e show
  the same delayed refresh.
- Referencing a standalone form partial instead of inline sections also fails.
- All maintained package source checks pass. They do not verify native redraw.

Current conditional sections use:

```json
{
  "visibleIf": "{% if data.durationType == 'time' %}true{% endif %}"
}
```

Implementation references: `forms/spell.json`,
`forms/partials/spell-effect-duration.json`. The confirmed main-page diagnostic
is `dist/test/pf2e-remaster-duration-root-test.system`; its source is
`dist/test/diagnostics/spell-duration-root-form.json`.

## Area to investigate

The results point to conditional-section invalidation/data observation inside
the generic nested entity form. This is an inference, not a confirmed internal
cause. The app-owned status duration page is a separate component; the public
[FormDefinition interface](https://docs.encounter.plus/reference/schema/form-definition/)
provides no documented hook to embed that native duration page or force a
generic nested page to refresh.

Original workaround while preserving the existing nested layout: select Time, leave
Duration, and reopen it. The printed spell duration and token expiry fields
remain separate to preserve PF2E duration qualifiers.

## Additional Recall Knowledge selection feedback

Before the app update, the user reported that the subject/skill selection checkmark did not appear
until leaving/re-entering Recall Knowledge. Deleting an entry works correctly.
Whether the displayed selected value also stays stale remains unconfirmed;
the user confirmed immediate checkmarks after the 5.0.9 update on 2026-10-07.
This is not yet established as the same internal issue as Duration visibility.

Relevant source: `forms/partials/recall-knowledge-entry.json`. Its single picker
binds to the list row's `subject`; its multi-picker binds to `skills`. Those are
the existing stored paths, not paths into a separate editor object.
