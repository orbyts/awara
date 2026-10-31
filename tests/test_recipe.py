import json
import unittest
from pathlib import Path

from awara import validate

ROOT = Path(__file__).resolve().parents[1]


class Recipes(unittest.TestCase):
    def test_contract(self):
        for case in json.loads((ROOT / "tests/cases.json").read_text()):
            with self.subTest(case=case["name"]):
                self.assertEqual(not validate(case["recipe"]), case["valid"])

    def test_schema_copies(self):
        canonical = (ROOT / "schemas/recipe.schema.json").read_bytes()
        for path in [
            "src/awara/recipe.schema.json",
            "js/recipe.schema.json",
            "rust/recipe.schema.json",
        ]:
            self.assertEqual(canonical, (ROOT / path).read_bytes())
