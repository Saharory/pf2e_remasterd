"""Keep creature senses concise and link shared sense definitions."""

from __future__ import annotations

import re
from typing import Any


# These are the shared senses AoN links directly from creature stat blocks.
# Creature-specific senses remain plain text because their explanation belongs
# to that creature's editable ability rather than a different generic rule.
SENSE_ROUTES = (
    (re.compile(r"(?<![\w])greater[ -]darkvision(?![\w])", re.I), "/action/greater-darkvision-monster-core"),
    (re.compile(r"(?<![\w])low[ -]light vision(?![\w])", re.I), "/action/low-light-vision-monster-core"),
    (re.compile(r"(?<![\w])all[ -]around vision(?![\w])", re.I), "/action/all-around-vision-monster-core"),
    (re.compile(r"(?<![\w])darkvision(?![\w])", re.I), "/action/darkvision-monster-core"),
    (re.compile(r"(?<![\w])lifesense(?![\w])", re.I), "/action/lifesense-monster-core"),
    (re.compile(r"(?<![\w])scent(?![\w])", re.I), "/action/scent-monster-core"),
    (re.compile(r"(?<![\w])tremorsense(?![\w])", re.I), "/action/tremorsense-monster-core"),
    (re.compile(r"(?<![\w])wavesense(?![\w])", re.I), "/action/wavesense-monster-core"),
)

EMBEDDED_METADATA = re.compile(
    r"(?:^|;\s*)(?:Recall Knowledge\b|Languages\b).*$", re.I | re.S
)
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\([^)]+\)")


def strip_embedded_metadata(value: str) -> str:
    """Remove fields an old importer appended to the senses string."""
    match = EMBEDDED_METADATA.search(value)
    if match:
        value = value[: match.start()]
    return value.strip().strip(";").strip()


def link_shared_senses(value: str) -> str:
    """Link each shared sense once without touching creature-specific senses."""
    text = value
    linked_routes = set(re.findall(r"\[[^\]]+\]\((/[^)]+)\)", text))
    for pattern, route in SENSE_ROUTES:
        if route in linked_routes:
            continue
        protected = [
            (match.start(), match.end()) for match in MARKDOWN_LINK.finditer(text)
        ]
        match = next(
            (
                candidate
                for candidate in pattern.finditer(text)
                if not any(
                    candidate.start() < end and candidate.end() > start
                    for start, end in protected
                )
            ),
            None,
        )
        if match is None:
            continue
        text = (
            text[: match.start()]
            + f"[{match.group(0)}]({route})"
            + text[match.end() :]
        )
        linked_routes.add(route)
    return text


def configure_creature_senses(entity: dict[str, Any]) -> bool:
    """Separate imported metadata and add available internal sense links."""
    if entity.get("kind") != "Creature":
        return False
    data = entity.get("data")
    if not isinstance(data, dict):
        return False
    original = str(data.get("senses") or "")
    configured = link_shared_senses(strip_embedded_metadata(original))
    if configured == original:
        return False
    data["senses"] = configured
    return True
