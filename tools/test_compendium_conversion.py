#!/usr/bin/env python3
"""Focused regression tests for source-to-compendium text and price conversion."""

from __future__ import annotations

import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_aon_orc_staging import item_price
from foundry_markup import has_conversion_artifact, replace_foundry_directives


class FoundryMarkupTests(unittest.TestCase):
    def test_nested_damage_type_and_options(self) -> None:
        rendered = replace_foundry_directives(
            "Creatures take @Damage[10d6[bludgeoning]|options:area-damage] damage."
        )
        self.assertEqual(rendered, "Creatures take 10d6 bludgeoning damage.")
        self.assertFalse(has_conversion_artifact(rendered))

    def test_template_includes_shape_and_distance(self) -> None:
        self.assertEqual(
            replace_foundry_directives("a @Template[line|distance:60] of stones"),
            "a 60-foot line of stones",
        )

    def test_roll_with_nested_healing_type(self) -> None:
        self.assertEqual(
            replace_foundry_directives("[[/r 4d8[healing] #Treat Wounds]] Hit Points"),
            "4d8 healing Hit Points",
        )

    def test_dynamic_formula_uses_readable_variable_name(self) -> None:
        rendered = replace_foundry_directives(
            "@Damage[(@item.rank+1)d8[acid]|options:area-damage]"
        )
        self.assertEqual(rendered, "(spell rank+1)d8 acid")
        self.assertNotIn("current value", rendered)

    def test_dynamic_formula_is_evaluated_for_the_record_level(self) -> None:
        rendered = replace_foundry_directives(
            "@Damage[(floor((@actor.level -1)/2) +2)d4[slashing]]",
            {"@actor.level": 5},
        )
        self.assertEqual(rendered, "4d4 slashing")
        self.assertFalse(has_conversion_artifact(rendered))

    def test_conditional_formula_is_evaluated_for_the_record_level(self) -> None:
        rendered = replace_foundry_directives(
            "@Damage[(ternary(gte(@actor.level,20),10,9))d10[bludgeoning]]",
            {"@actor.level": 18},
        )
        self.assertEqual(rendered, "9d10 bludgeoning")

    def test_template_type_property_is_humanized(self) -> None:
        self.assertEqual(
            replace_foundry_directives("@Template[type:burst|distance:20]"),
            "20-foot burst",
        )


class ItemPriceTests(unittest.TestCase):
    def test_variant_price_fallback_matches_base_level(self) -> None:
        record = {
            "level": 3,
            "markdown": """
                <title level="2" right="Item 3">Base Item</title>
                **Price** 50 gp
                <title level="2" right="Item 7">Greater Item</title>
                **Price** 360 gp
            """,
        }
        self.assertEqual(item_price(record), "50 gp")

    def test_missing_printed_price_stays_blank(self) -> None:
        self.assertEqual(item_price({"level": 5, "markdown": "No price listed."}), "")

    def test_zero_price_is_preserved(self) -> None:
        self.assertEqual(item_price({"price": 0}), "0 gp")


if __name__ == "__main__":
    unittest.main()
