#!/usr/bin/env python3
"""Keep PF2E duration prose and derive Encounter+'s native effect duration."""

from __future__ import annotations

import re
from typing import Any


NATIVE_DURATION_FIELDS = ("duration", "durationType", "durationUnit")
TURN_DURATIONS = {
    "until the start of your next turn": "sourceStartNextTurn",
    "until the beginning of your next turn": "sourceStartNextTurn",
    "until the end of your next turn": "sourceEndNextTurn",
    "until the start of the target's next turn": "targetStartNextTurn",
    "until the end of the target's next turn": "targetEndNextTurn",
    "until the end of your target's next turn": "targetEndNextTurn",
}
TIMED_DURATION = re.compile(
    r"(?:(?:sustain(?:ed)?\s+(?:for\s+)?)?up to\s+)?"
    r"(\d+)\s+(round|minute|hour|day|week)s?"
    r"(?:\s*\(see text\)|\s+or until (?:expended|used|discharged))?",
    re.I,
)


def parse_spell_duration(text: str) -> dict[str, Any]:
    """Derive only a clear timer or a native next-turn expiration.

    A sustained/up-to duration is a maximum, not automatic Sustain. Alternative
    durations, daily preparations, calendar months/years, and current-turn
    endings need a GM decision; they must not acquire a guessed countdown.
    """
    normalized = " ".join(text.lower().split())
    if normalized in TURN_DURATIONS:
        # Supply a numeric duration to the generic entity loader; the native
        # turn-relative type controls expiry rather than this round count.
        return {
            "duration": 1, "durationType": TURN_DURATIONS[normalized],
            "durationUnit": "round",
        }
    match = TIMED_DURATION.fullmatch(normalized)
    if not match:
        return {}
    value, unit = int(match[1]), match[2]
    if value <= 0:
        return {}
    if unit == "week":
        value, unit = value * 7, "day"
    return {"duration": value, "durationType": "time", "durationUnit": unit}


def configure_spell_load_data(entity: dict[str, Any]) -> bool:
    """Convert legacy prose once; leave GM-authored native values untouched."""
    if entity.get("kind") != "Spell" or not isinstance(entity.get("data"), dict):
        return False
    data = entity["data"]
    if not isinstance(data.get("duration"), str):
        return False
    # Preserve existing native settings rather than overwrite a GM's choice.
    if data.get("durationType") or data.get("durationUnit"):
        return False
    text = data["duration"]
    data.setdefault("durationText", text)
    for field in NATIVE_DURATION_FIELDS:
        data.pop(field, None)
    data.update(parse_spell_duration(text))
    return True
