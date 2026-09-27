"""Curated creature spellcasting used to validate linked spell references.

The source creature conversion currently keeps creature statistics and actions
but not Foundry's embedded spell entities.  Keep the first prototype explicit
and source-backed; once it is proven in Encounter+, the same shape can be
populated generically for every spellcasting creature.
"""

from __future__ import annotations

from typing import Any


PROTOTYPE_CREATURE_SLUG = "goblin-war-chanter-monster-core"

PROTOTYPE_SPELLCASTING: list[dict[str, Any]] = [
    {
        "name": "Occult Spontaneous Spells",
        "spellAttack": 7,
        "spellDC": 17,
        "spellGroups": [
            {
                "label": "1st (2 slots)",
                "spells": [
                    {
                        "name": "Bless",
                        "rank": 1,
                        "reference": "/spell/bless-player-core",
                    },
                    {
                        "name": "Soothe",
                        "rank": 1,
                        "reference": "/spell/soothe-player-core",
                    },
                ],
            },
            {
                "label": "Cantrips (1st)",
                "spells": [
                    {
                        "name": "Courageous Anthem",
                        "rank": 1,
                        "reference": "/spell/courageous-anthem-player-core",
                    },
                    {
                        "name": "Figment",
                        "rank": 1,
                        "reference": "/spell/figment-player-core",
                    },
                    {
                        "name": "Message",
                        "rank": 1,
                        "reference": "/spell/message-player-core",
                    },
                    {
                        "name": "Telekinetic Hand",
                        "rank": 1,
                        "reference": "/spell/telekinetic-hand-player-core",
                    },
                    {
                        "name": "Telekinetic Projectile",
                        "rank": 1,
                        "reference": "/spell/telekinetic-projectile-player-core",
                    },
                ],
            },
        ],
    }
]


def configure_creature_spellcasting(entity: dict[str, Any]) -> bool:
    """Add the tested linked-spell shape to the prototype creature."""
    if entity.get("slug") != PROTOTYPE_CREATURE_SLUG:
        return False
    data = entity.setdefault("data", {})
    data["spellcasting"] = PROTOTYPE_SPELLCASTING
    return True
