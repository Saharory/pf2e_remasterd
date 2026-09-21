"""Small, reviewed mechanics supplements for the published hazard/vehicle packs.

Strikes come from the corresponding ORC-compatible hazard records in the
Pathfinder 2e Foundry source.  Their narrative descriptions are not copied.
The fixture is keyed by the unique published slug, never by a fuzzy name.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any


STRIKES = json.loads(
    (Path(__file__).resolve().parents[1] / "compendium/hazard-strikes.json").read_text()
)


def supplement(entity: dict[str, Any], kind: str) -> None:
    data = entity.get("data")
    if not isinstance(data, dict):
        return
    if kind == "Hazard":
        strikes = STRIKES.get(entity.get("slug"))
        if strikes and not data.get("attacks"):
            data["attacks"] = copy.deepcopy(strikes)
    elif kind == "Vehicle":
        price = data.get("price")
        if isinstance(price, (int, float)) and not isinstance(price, bool):
            if price > 0:
                data["price"] = f"{price:,} gp"
            else:
                # Zero in these records denotes an unspecified price, not a
                # free vehicle.  Do not suggest a false market value.
                data["price"] = ""
