> Migrated lab reference. Use the current [manual setup](../getting-started/manual-setup.md) and recipe JSON for current configuration. Historical results below apply only to the tested samples. UI illustrations are being reviewed for a public edition.

# Nodes and multicamera assembly

Edition 0.2 | 2026-10-30

Working edition based on the guided lab; visual acceptance is not independent colorimetric validation.

## Make every node
input unambiguous

Current one-clip lab versus the proposed multicamera layout



The completed Spatial Film test uses two clip nodes: <b>Grade - DWG/I</b> and <b>Output - DWG to PQ</b>. There is no camera input node because the Edit-page plugin already provides DWG/I.

| Camera path | Before the common grade |
| --- | --- |
| Action 6 D-Log M | Original -> camera-specific Gamut DWG LUT |
| Osmo 360 D-Log M | OSV twin -> Spatial Film DJI 360 Reframe, Color = DWG/I |
| Already normalized DWG/I file | No second camera transform; verify provenance |
| Other cameras / stills | Establish actual primaries and transfer function first |

> An input LUT is not a creative look. D-Log is not a substitute for D-Log M. A Rec.709 container tag alone is not a safe input-space assignment for these DJI log sources.

## Scale to multiple
cameras

Proposed next assembly; not yet demonstrated in this lab

```text
Edit source processing -> Group Pre-Clip input (where needed) -> Clip DWG grade -> Group Post-Clip shared DWG grade -> Timeline look/trim -> one output CST
```

Group clips by actual input encoding and transform version, not just camera brand. Apply the Action 6 input LUT once in its group. Spatial Film clips already in DWG/I must not receive it.

For a single output timeline, move the output CST from each clip to the final Timeline node. Remove the old clip output CSTs when doing so. Then verify against the accepted single-clip render before adding other cameras.

> This graph is a proposed organization. Group and Timeline grades affect more than one clip; verify titles, stills and nested timelines too. Every element reaching the output stage must have a known working-space interpretation.

## One grade,
multiple deliverables

Separate input normalization, shot grade and delivery decisions

1. Build a camera-normalized DWG/I assembly. Balance each shot in the common working space and preserve a baseline version.
2. Create explicit delivery variants for PQ and HLG; each needs its own output rendering and matching monitoring/tags. Do not chain a PQ output CST into an HLG output CST.
3. For the first implementation, use named timeline variants and a controlled method of copying/linking shot grades. A duplicated timeline is not a promise that later edits or grades remain synchronized.
4. Keep 360 framing on the source clip effect. Make 16:9 and vertical framing decisions separately while retaining the same camera normalization.
5. Test reuse with a small project first. Power windows, tracking and spatial effects may depend on framing and need rechecking even when global color balance is reusable.

### Inputs still to validate

Sony A7S III video; iPhone 16 Pro and 17 Pro with the actual recording app/mode; linear Display P3 32-bit and Rec.2020/PQ 16-bit still exports. Codec or bit depth alone does not identify their transfer functions. The A7R V is the stills camera.

### The final portable example

Deliver the working project snapshot, manifest of all external media and transforms, install/relink instructions, screenshots, and per-output verification. Keep redistributable documentation separate from paid LUTs and downloaded media rights.

> The current project proves the Osmo 360 route and PQ test. A synchronized multicamera, multi-aspect, PQ/HLG project is the next integration milestone, not a completed claim.
