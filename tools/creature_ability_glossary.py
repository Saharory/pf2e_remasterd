"""Restore shared monster abilities and clean creature ability presentation."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


GLOSSARY_PATH = Path(__file__).with_name("creature-ability-glossary.json")
GLOSSARY: dict[str, str] = json.loads(GLOSSARY_PATH.read_text(encoding="utf-8"))
SEPARATOR = re.compile(r"\n\s*---\s*\n")


def normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.casefold())


GLOSSARY_BY_KEY = {normalize(code): text for code, text in GLOSSARY.items()}


def expanded_text(name: str, value: str) -> str:
    """Expand a flattened glossary token and remove artificial dividers."""
    text = str(value or "").strip()
    direct = GLOSSARY_BY_KEY.get(normalize(text))
    if direct:
        return direct

    parts = [part.strip() for part in SEPARATOR.split(text)]
    if len(parts) > 1:
        glossary = GLOSSARY_BY_KEY.get(normalize(parts[-1]))
        if glossary:
            parts[-1] = glossary
        elif normalize(parts[-1]) in {normalize(name), normalize("Effect " + name)}:
            parts.pop()
        text = "\n\n".join(part for part in parts if part)

    paragraphs = [part.strip() for part in text.split("\n\n")]
    if len(paragraphs) > 1 and normalize(paragraphs[-1]) in {
        normalize(name),
        normalize("Effect " + name),
    }:
        return "\n\n".join(part for part in paragraphs[:-1] if part)

    if not text:
        return GLOSSARY_BY_KEY.get(normalize(name), "")
    return text


def configure_creature_abilities(entity: dict[str, Any]) -> int:
    """Apply editable, complete ability text to an Action or Creature."""
    changed = 0
    if entity.get("kind") == "Action":
        original = str(entity.get("descr") or "")
        updated = expanded_text(str(entity.get("name") or ""), original)
        if updated != original:
            entity["descr"] = updated
            changed += 1

    if entity.get("kind") != "Creature":
        return changed
    abilities = entity.get("data", {}).get("abilities", {})
    if not isinstance(abilities, dict):
        return changed
    for entries in abilities.values():
        if not isinstance(entries, list):
            continue
        for ability in entries:
            if not isinstance(ability, dict):
                continue
            original = str(ability.get("text") or "")
            updated = expanded_text(str(ability.get("name") or ""), original)
            if updated != original:
                ability["text"] = updated
                changed += 1
    return changed
