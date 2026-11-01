# Generate the scaffold with Kestreel

Requires the development checkout containing the Awara workflow adapter; PyPI 0.0.0 does not contain this integration.

```sh
uv run kestreel project init my-project --root /path/to/projects \
  --awara-root /path/to/awara --workflow resolve-multicamera-hdr
```

Run this from the Kestreel checkout. Alternatively configure paths.awara and paths.projects in ~/.config/kestreel/config.toml. Remove any project.folders override when selecting an Awara template. Add --recipe with a separate Kestreel asset-binding JSON to reference existing media.

Kestreel creates the template folders, a project ledger, SETUP.md, and a checksummed snapshot of explicitly referenced JSON/Markdown documents under manifests/awara. It does not copy paid dependencies or media. Changing Awara later does not change this snapshot. Initialization refuses existing project folders.

This completes the folder-and-manifest stage only. Resolve creation, media import, color settings, plugin parameters and LUT assignments remain pending. Follow the accompanying manual guide for those steps. The ledger deliberately reports scaffolded-settings-not-applied, not a completed application setup.


## Optional Resolve foundation adapter

The Kestreel development checkout now has a separate, explicit operation:

```sh
uv run kestreel project resolve /path/to/scaffold \
  --profile /path/to/awara/applications/resolve/automation/pq-foundation.json \
  --name 'My HDR Project'
```

Review the plan, then add `--apply`. The adapter creates a new Resolve project,
verifies exposed project settings by readback, imports supported media, creates
an empty timeline and exports a DRP without embedded LUTs. It refuses existing
project names and unsaved untitled projects. The supplied UHD 29.97 PQ profile is
an initial API mapping for Resolve 21.1.2; live verification is pending.

OSV preparation, OFX parameters, LUT assignment, grade nodes, output CST,
monitoring and final render remain manual. Read the result ledger before treating
any step as applied. A project color-space declaration does not convert pixels.
