"""Portable Awara workflow recipe validation."""

import argparse
import json
from importlib.resources import files
from pathlib import Path

from jsonschema import Draft202012Validator


def schema() -> dict:
    return json.loads(files(__package__).joinpath("recipe.schema.json").read_text())


def validate(recipe: object) -> list[str]:
    """Return schema errors; an empty list means structurally valid."""
    return [
        f"{list(e.absolute_path)}: {e.message}"
        for e in Draft202012Validator(schema()).iter_errors(recipe)
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", action="version", version="awara 0.0.0")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("schema")
    sub.add_parser("validate").add_argument("file", type=Path)
    args = parser.parse_args()
    if args.command == "schema":
        print(json.dumps(schema(), indent=2))
        return 0
    try:
        errors = validate(json.loads(args.file.read_text()))
    except (OSError, ValueError) as exc:
        print(f"Error: {exc}")
        return 2
    print("\n".join(errors) if errors else "Valid Awara recipe")
    return int(bool(errors))
