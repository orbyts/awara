import json
import subprocess
import unittest
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker
from awara import validate
ROOT = Path(__file__).resolve().parents[1]
class Catalog(unittest.TestCase):
    def test_recipes_and_references(self):
        for p in (ROOT / "recipes").glob("*/recipe.json"):
            data=json.loads(p.read_text())
            self.assertEqual(validate(data), [])
            settings=data["application"]["settings"]
            for path in settings["config_files"]+[settings["template"],settings["manual"]]:
                self.assertTrue((ROOT/path).is_file(),path)
            for dep in settings["dependencies"]:
                self.assertTrue((ROOT/f"resources/dependencies/{dep}.json").is_file())
    def test_dependencies(self):
        schema=json.loads((ROOT/"schemas/dependency.schema.json").read_text())
        validator=Draft202012Validator(schema,format_checker=FormatChecker())
        for p in (ROOT/"resources/dependencies").glob("*.json"):
            validator.validate(json.loads(p.read_text()))
    def test_private_assets_excluded(self):
        self.assertEqual(subprocess.run(["git","check-ignore","-q","awara-private/example.cube"],cwd=ROOT).returncode,0)
        tracked=subprocess.check_output(["git","ls-files","awara-private"],cwd=ROOT,text=True)
        self.assertEqual(tracked,"")
