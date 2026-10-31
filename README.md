# Awara

Portable creative workflow recipes, schemas, and validation tools.

Version 0.0.0 is a functional experimental release: validate a recipe, export its JSON Schema, or use the validator as a library. It does not configure Resolve, ingest media, apply LUTs, or verify color accuracy. Settings are application-defined data, not checked against application APIs.

## CLI

```sh
awara validate examples/resolve-manual-dwg.json
awara schema
awara --version
```

Exit codes: 0 valid/success, 1 schema validation failed, 2 file/JSON/usage error.

Python: `uv tool install awara`. JavaScript: `npx awara validate recipe.json`. Rust: `cargo install awara`. Each provides the same command name; install one CLI implementation per environment.

## Libraries and website use

Python: `from awara import validate, schema`.
JavaScript: `import {validate, schema} from 'awara'` (browser-bundler compatible).
Rust: `awara::validate(&serde_json::Value)` and `awara::SCHEMA`.

Validation is read-only and never executes recipe steps. The JavaScript library has no Node filesystem dependency; filesystem access is confined to its CLI. A website can use the same schema for forms and validation later.

## Ownership

Awara describes reusable application workflows. Kairo owns device identities/capture settings. Kestreel owns ingestion/project scaffolding and may consume Awara recipes. No paid LUTs, plugins, personal media, or credentials are distributed here.

## Development

`uv run python -m unittest discover -s tests`; `cd js && npm ci && npm test`; `cargo test --manifest-path rust/Cargo.toml`.

The canonical schema lives in `schemas/recipe.schema.json`; package copies must match. Shared contract fixtures test all three implementations. Schema version 1 is experimental and may evolve before a stable release.

MIT licensed.


## Workflow catalog

Start with [manual Resolve setup](docs/getting-started/manual-setup.md) or the [versioned recipe](recipes/resolve-multicamera-hdr/recipe.json). Awara owns configurations and accompanying manual guides/PDFs. Kestreel owns ingestion and project scaffolding; Kairo owns device identity and capture presets. Awara-driven automatic application is under development.

Personal purchases live in `awara-private/`, ignored by Git. Never force-add that directory. Public dependencies are links, not licensed payloads. Preserve vendor originals; installation may use descriptive aliases.

[Current manual reference PDF](output/pdf/awara-resolve-manual-reference.pdf) accompanies the manual setup. Rebuild it with `uv run --with reportlab python scripts/build_reference.py`. Historical lab guides remain under docs/workflows; screenshot review for the public illustrated edition is pending.

Kestreel development now supports [recipe-driven folder and manifest scaffolding](docs/getting-started/kestreel-setup.md). Applying settings to Resolve remains pending.
