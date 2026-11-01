> Migrated lab reference. Use the current [manual setup](../getting-started/manual-setup.md) and recipe JSON for current configuration. Historical results below apply only to the tested samples. UI illustrations are being reviewed for a public edition.

# Camera-agnostic HDR workflow

Edition 0.2 | 2026-10-30

Working edition based on the guided lab; visual acceptance is not independent colorimetric validation.

## One working space.
Two delivery paths.

Start here | The color architecture

Normalize each camera into <b>DaVinci Wide Gamut / DaVinci Intermediate (DWG/I)</b>. Grade there, then render that grade for PQ or HLG. A different camera changes the input stage; a different delivery changes the output stage.

```text
Camera originals -> camera-specific normalization -> DWG/I -> grade (still DWG/I) -> PQ OR HLG output -> encode/tag/verify
```

> DWG is the RGB gamut; Intermediate is the working transfer function. There is no second conversion into DWG/I after grading: the grade remains in that space.

For Osmo 360, Spatial Film handles stitching, stabilization, reframing and DWG/I output on the Edit page before our Color-page grade. This block diagram describes color intent, not an assertion that geometry always happens after grading.

## Choose who owns
the transforms

Manual YRGB is the selected workflow in this guide

| Mode | Use it when / responsibility |
| --- | --- |
| DaVinci YRGB (manual) | Use explicit camera LUTs, plugins and CSTs when you need visible control of the chain. You own both input normalization and the final output transform. |
| DaVinci YRGB Color Managed (RCM) | Useful when camera input definitions are supported and reliably assigned. Resolve manages input -> timeline -> output. Automatic tags still need checking; external plugins need an ordering test. |

### Why manual here

The Action 6 uses a purchased DWG input LUT. The Osmo 360 plugin supplies DWG/I directly. Keeping these inputs explicit makes the two paths easy to inspect without assuming that a Rec.709 container tag describes D-Log M.

### Declarations are not transformations

In manual YRGB, set Timeline Color Space to DWG/I to describe the working environment. Set Output Color Space to the actual delivery encoding for monitoring and tagging. These declarations do not replace the input LUT or output CST. Export tags label the rendered pixels; they do not change those pixels.

### Moving to RCM later

Do not simply enable RCM over this manual graph. Remove or bypass the manual output conversion only as part of a controlled migration. Confirm what pixels reach RCM and where a plugin operates. Genuine pre-normalized DWG/I files can be assigned DWG/I as their input; a camera file plus an Edit-page effect needs separate testing.

- [Dolby: output declaration in manual DaVinci YRGB](https://professionalsupport.dolby.com/s/article/Best-Practices-Resolve-output-color-space-setting-using-Color-science-DaVinci-YRGBBest-Practices-Resolve-output-color-space-setting-using-Color-science-DaVinci-YRGB)

## Files that survive
the next project

Library structure and portable handoffs

Use a configured originals root with date folders and device-qualified filenames. Preserve camera metadata and companions in verified manifests. Kestreel owns this ingest policy; avoid manually renaming without a source-to-destination ledger.

| Root-relative location | Purpose |
| --- | --- |
| originals/YYYY/YYYY-MM/YYYY-MM-DD/camera-a/card-001/ | Verified original camera files, sidecars and telemetry |
| samples/publisher/camera/ | Downloaded test originals with source/license records |
| projects/project-name/workspace/resolve/ | Versioned .drp project snapshots |
| projects/project-name/workspace/spatial-film-source/ | Byte-identical MP4 twins for this OSV test |
| projects/project-name/masters/ | Test and approved renders; distinguish them in names |
| projects/project-name/docs/ and manifests/ | Screenshots, settings, checksums and verification |

The active Resolve project lives in its <b>Project Library</b>. The shared .drp is an exported snapshot, not the live project and not a media bundle. Saving the project does not refresh an older .drp. Export another version after milestones.

For relocation: import the .drp, relink media, install the exact plugins and licensed LUTs, and check every timeline. Path mappings in our JSON are for our tools; Resolve does not automatically read them. Put regenerable caches on local SSD storage when performance work begins.

> Copy and verify ingest; preserve originals. A public sample project must exclude purchased LUTs and unlicensed review footage. Provide dependencies and purchase/download links instead.

## What this edition
actually establishes

Read the evidence before reusing the recipe

| Checkpoint | Evidence / status |
| --- | --- |
| OSV -> MP4 twin | SHA-256 and byte count match the original. This copy did not re-encode. |
| Spatial Film -> DWG/I | Plugin selection captured in screenshots; independent characterization not measured. |
| PQ static render | HEVC Main10, Rec.2020/PQ/video tags and full decode checked. User confirms QuickTime matches Resolve on XDR. |
| Animated 0 -> 180 pan | Endpoint keyframes shown; user confirms exported animation. |
| Action 6 input LUT | Correct DWG file header cataloged; user reports successful visual result. Separate camera guide. |
| HLG / platform uploads | Not yet tested in this guided project. |
| Proxy/cache performance | Separate next test; network playback was slow. Bottleneck not isolated. |

### Guide map

02: Action 6 input. 03: Osmo 360 source, stabilization and animation. 04: nodes and multicamera assembly. 05: monitoring, export and checks.

> A visual match is useful workflow evidence. It does not prove scene-linear response, maximum retained dynamic range, chart accuracy, calibration or all-camera equivalence. Use the same tested versions when reproducing this lab.
