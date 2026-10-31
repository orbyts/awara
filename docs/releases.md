# Release process

All three distributions share the canonical recipe schema and version. Run CI and inspect package contents before publishing. Version 0.0.0 is experimental.

- Python: `uv build` then `uv publish`. Future GitHub OIDC publishing uses owner `orbyts`, repository `awara`, workflow `release.yml`, environment `pypi`; configure this on PyPI before dispatching the workflow.
- npm: from `js/`, `npm ci`, `npm test`, `npm pack --dry-run`, then `npm publish --access public`. Authenticate locally; never commit tokens.
- Rust: `cargo test --manifest-path rust/Cargo.toml`, then `cargo publish --manifest-path rust/Cargo.toml`. Authenticate locally; never commit tokens.

Verify registry versions and test installed packages after publication. A schema-valid recipe is not evidence that settings are supported by an application or that a color transform is accurate. The application adapter must independently check compatibility before applying settings.
