> Migrated lab reference. Use the current [manual setup](../getting-started/manual-setup.md) and recipe JSON for current configuration. Historical results below apply only to the tested samples. UI illustrations are being reviewed for a public edition.

# Action 6: RockSteady versus stabilization in Resolve

Working lab recipe, 2026-10-31. Resolve 21.1.2.10; Gyroflow OpenFX 2.1.1; metadata inspected with Gyroflow 1.6.3. This is a walking test, not approval of a bicycle-mounted capture preset.

## Capture and verified ingest

Preserve the complete card and verify source/destination SHA-256. For this test all 14 files passed. Source MP4s are 3840×3840, 59.94 fps, HEVC 10-bit. D-Log M is user-identified; Rec.709 container tags are not an input-transform specification.

| Clip | Capture | Parsed motion data |
|---|---|---|
| 0001 | Wide; RockSteady off | 221,712 orientation quaternions; DJI official square lens profile |
| 0002 | RockSteady on | No orientation samples or lens profile parsed |
| 0003 | Ultra Wide; RockSteady off | No orientation samples or lens profile parsed |

Gyroflow’s [documented DJI workflow](https://docs.gyroflow.xyz/app/getting-started/supported-cameras/dji) requires EIS off and Wide. These parser results support that workflow for our Wide take. They do not establish absence of every possible proprietary data representation. Keep the RockSteady take as the camera-stabilized baseline; its processing cannot be undone. Do not apply the Wide lens profile to Ultra Wide.

## Resolve setup

Create a separate manual **DaVinci YRGB** project. Use a square 3840×3840 timeline at 59.94 fps to avoid introducing an aspect-ratio crop into the initial test. Timeline color space: **DaVinci WG/Intermediate**. Output: **Rec.2100 HLG**, HDR mastering declaration 1000 nits. Project input/output LUT fields remain empty. In manual YRGB these declarations do not normalize D-Log M or replace the output CST.



Import archive originals. Our four short timelines use 599 frames starting at source frame 600: Wide/off original, identical Wide/off plus Gyroflow, RockSteady/on, and Ultra Wide/off. Only the first two are frame-matched; different walking takes are a qualitative comparison.

## Apply Gyroflow to the Wide/off candidate

1. On the Edit page, search Effects for **Gyroflow**, then drag it onto the timeline clip.
2. Select the clip; open **Inspector → Effects → Open FX**.
3. Click **Load for current file**. Wait for **Status: OK**.
4. Keep the loaded integration method **None** for this quaternion-based source. Do not force VQF merely because it was shown before loading.
5. Baseline parameters: Smoothness **50**, Zoom limit **130**, Lens correction **100**, Horizon lock **0**, FOV **1.000**, video speed **100**, rotation/pitch/yaw offsets **0**. These are tested settings, not universal capture recommendations.
6. Toggle the effect to compare the same frames. Lens correction 100 applies the full lens correction; the user observed both steadier motion and reduced lens curvature. Briefly comparing correction 0 versus 100 distinguishes that geometry change from stabilization. Keep 100 for this test.



No extra dewarp or Resolve stabilization is added. Gyroflow is an Edit-page effect before the Color-page grade. Source files remain unchanged; no pre-rendered stabilized intermediate is required. Check fast-motion blur, wobble, edge stretch, crop, zoom pumping and black borders in the exported result. Preview acceptance is not yet a cycling field test.

## Camera input, grade and HLG output

```text
Original D-Log M → Gyroflow geometry/stabilization → Action 6 DWG input LUT
→ grade in DWG/Intermediate → HLG output CST → 10-bit delivery
```

Color node 01: purchased **BaseLUT - DJI Osmo Action 6 - D-Log M to DWG**. Obtain it from [Gamut](https://gamut.io/product/baseluts-for-dji-osmo-action-6/); the paid file is not distributed with this guide. Node 02 holds the grade. Node 03 is a CST: input DaVinci Wide Gamut / DaVinci Intermediate; output Rec.2100 / Rec.2100 HLG. HDR Standard Conversions, HDR 203 Nits Diffuse White and White Point Adaptation enabled.



The user preferred **Tone Mapping: None** while shaping cloud contrast in node 02. Record that choice, not a claim that None always preserves more detail. CST color/gamma conversion still occurs. Gamut mapping is also None in this test. Verify output limits on scopes; the 1000-nit mastering declaration is not an automatic limiter. Matching a display rendering or visual preference does not independently validate scene colorimetry.

Use the same color grade for the geometry comparisons. Copy color grades only; copying all attributes could inadvertently copy stabilization to the baseline. Geometry and color choices remain separately editable.

## Render and verification

Custom Export, single clip, QuickTime H.265, **Main10**, 3840×3840, 59.94 fps; test bitrate request 100,000 Kb/s, AAC 48 kHz. Tag Rec.2020 primaries and Rec.2100 HLG transfer. These are working test exports, not an Instagram-specific delivery specification. File tags must describe the actual CST output.

Verify each file’s pixel format, frame count, cadence, primaries, transfer and full decode. Review motion from a local playback copy if the network stalls. Compare Wide/off original against its exact Gyroflow pair first, then compare the separate RockSteady take. The project remains source-based; delivery renders are viewing outputs, not replacement source media.

Pending: exported-motion acceptance, final capture preset, cycling test, and the corresponding PQ delivery variant. Preserve a DRP snapshot with the plugin installed and purchased LUT available on the receiving machine. A DRP alone is not a self-contained media/plugin archive.

## Verified export checkpoint

All four HLG v01 exports completed and passed full FFmpeg decoding. FFprobe reports HEVC Main10, yuv420p10le, 3840×3840, 599 frames, BT.2020 primaries and matrix (`bt2020nc`), and HLG transfer (`arib-std-b67`). This verifies encoding and declarations, not perceptual grading accuracy or platform acceptance. Separate local review copies avoid dependence on network playback.

Saved project: `Action6_Gyroflow_HLG_comparison_v03.drp`. Active timeline: `02 Wide OFF - Gyroflow HLG`. The same Color-page grade was copied to the other three tests without copying Edit-page Gyroflow. The user visually accepted stabilization and full lens correction in preview; exported-motion comparison remains pending.

## Capture decision — 2026-10-31

User selected **Wide + RockSteady off** as the intended Action 6 default for post stabilization. Ultra Wide/off is excluded from the gyro-based recipe: Gyroflow parsed neither orientation samples nor a lens profile in that take, consistent with its documented DJI mode requirements. Preserve the RockSteady-on baseline as a comparison, not the intended default. No confirmation of hardware reconfiguration has been received. Bicycle-mounted motion validation remains pending.

Next camera checkpoint: Osmo 360 projection/dewarp. Preserve the accepted Spatial Film recipe and compare only projection/lens-curve controls, holding pan/tilt/roll/zoom, color and stabilization constant. Distinguish straight-line correction, edge stretching and usable framing from RockSteady/Horizon Leveling. Do not add a second generic dewarp. Follow with save/reopen and source-path verification. Original sample tests do not establish real-world cycling capture or endurance.
