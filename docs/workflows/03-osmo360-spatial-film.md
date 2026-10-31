> Migrated lab reference. Use the current [manual setup](../getting-started/manual-setup.md) and recipe JSON for current configuration. Historical results below apply only to the tested samples. UI illustrations are being reviewed for a public edition.

# Osmo 360: source to HDR

Edition 0.2 | 2026-10-30

Working edition based on the guided lab; visual acceptance is not independent colorimetric validation.

## Start from the
original OSV

Selected route | Spatial Film 1.3.2 + Resolve Studio 21.1.2

This is the main Osmo 360 workflow. DJI Studio served as a comparison reference; it is not an intermediate-render requirement for this selected route. OpenOSV remains in guide 06 only.

1. Install the signed Spatial Film Immersive Utility package and its OSV Converter. Restart Resolve after installing so it can scan the OFX plugin.
2. Keep the downloaded or camera-original OSV untouched. Use the converter to create its MP4 twin under the project workspace/spatial-film-source folder.
3. Import that MP4 into the Media Pool. Its unprocessed image can look like a fisheye hemisphere; this is expected before the reframe effect.
4. Create an ordinary flat 3840 x 2160 timeline at 29.97 fps for this sample. Place the MP4 on the timeline before selecting its Inspector effects.
5. On Edit, apply Spatial Film DJI 360 Reframe to the original clip. Select the clip, then Inspector > Effects > Open FX.

> For this file, the OSV and MP4 are byte-identical: 2,612,241,573 bytes. SHA-256 begins 35ff74cdc54a1c2285c45f9484b239e3. The copy preserved both HEVC streams and metadata; it was not a second compression pass.

The sample has two 3840 x 3840 HEVC 10-bit streams at 30000/1001 fps plus audio/data. The source identity and full hash are in the private validation archive

- [Spatial Film: official control reference](https://spatial.film/resolve/guide/)

## Set the source
processing once

Edit-page Inspector | Actual test settings



Keep Perspective = Free View; RockSteady, Horizon Leveling and Seam Refinement on. Seam Blend = DJI Default (slower); Optical Flow Stitching off. Color = DaVinci Wide Gamut/Intermediate. Lens Accessory = Auto (as recorded).

> This plugin supplies the camera-to-working-space conversion. Do not add another D-Log M LUT or input CST afterward. Keep the plugin Proxy option off for the final render.

Retain the complete source and its motion metadata. RockSteady stabilization and the deliberate reframing move are separate controls. We did not add Resolve stabilization on top of the plugin in this test.

## Check the picture
before grading

The Edit effect supplies DWG/I; Color nodes handle grade and delivery



1. On the Color page, keep a clean node labeled Grade - DWG/Intermediate. Start with neutral controls.
2. Add a serial Output - DWG to PQ node using Color Space Transform. Use the exact settings in guide 05.
3. Confirm project color science is DaVinci YRGB, timeline space DWG/I, and output declaration Rec.2100 ST2084.
4. Confirm monitoring as shown in guide 05, render the short static test, then compare the exported file with Resolve.

> The static export passed file checks and the user confirmed a matching appearance on Pro Display XDR. A screenshot of log-looking or contrasty pixels alone is not proof of their encoding.

## Animate a half turn

0 degrees -> 180 degrees | Two endpoint keyframes





Duplicate the static test timeline before animating. At the first frame, click the Pan Angle diamond to store 0 degrees. Move later in the clip, set 180 degrees, and confirm the second diamond. Scrub between the endpoints.

> The suggested endpoint was 01:00:04:00, but these cropped screenshots do not prove keyframe times. Record actual timing in the final project snapshot. The user confirmed the animated export; the renamed file is SpatialFilm_PQ_1000nit_pan180_v02.mov.

## Shape the move;
keep the grade

Reframing is an edit decision, not a new camera input

Our captured controls use Keyframe Animation = None and Smooth Keyframes off. Resolve keyframes therefore drive the move directly. For a gentler start/stop, adjust easing after the basic two-keyframe test. Keep color nodes unchanged.

A 180-degree turn in roughly five seconds is a useful stress test, not necessarily the final editorial pace. Inspect the horizon, seam crossings, edge distortion and subject motion in the rendered file, especially where previews stutter.

### Angles and framing

Pan controls horizontal view; Tilt and Roll control vertical direction and rotation. Zoom and lens curvature change framing. Avoid interpreting the plugin zoom number as a physical focal length. Watch direction when crossing the -180/+180 boundary; use continuous angle values for the intended path.

### Performance is a separate test

The user could not play this network-based source smoothly. We have not isolated storage, decoding, GPU stitching or cache as the bottleneck. Do not label the network as the proven cause.

1. First test a verified local SSD copy of the same source and compare playback.
2. Evaluate the plugin Proxy switch and Resolve preview-resolution settings separately. Restore full quality before rendering.
3. Consider a local SSD render cache. A generic camera proxy may not retain the dual-stream/gyro data that this plugin needs; verify the actual source path used.
4. Record the chosen performance recipe in its own guide after testing.

- [Spatial Film: official control reference](https://spatial.film/resolve/guide/)

## Reproduce the
accepted result

What was tested and what stays outside this recipe

| Item | Current evidence |
| --- | --- |
| Static PQ test | 149 frames; 4.971633 seconds; Main10 HEVC; Rec.2020/PQ; video range; full decode passed. |
| Animated pan | 0/180 endpoint keys shown; user accepted animation. Actual animated file also passed full decode and PQ tag checks. |
| Source preservation | MP4 twin and OSV SHA-256 match. No lossy intermediate render. |
| Stabilization | RockSteady and Horizon Leveling enabled; user accepted footage. No quantified motion analysis. |
| Color accuracy | No independent chart/scene calibration; practical visual acceptance only. |

### The files to keep

Keep the source OSV, MP4 twin, manifests, screenshots, plugin version record, licensed transform dependencies, and a new .drp snapshot. Preserve the earlier static render as a baseline.

A final render compresses the processed image once from the original source path. Optional proxies/caches do not alter the originals, but their use at export must be deliberate. Screenshots in this guide are UI evidence, not reference HDR images.

> The main path is Spatial Film. No OpenOSV adapter or DJI Studio Rec.709 export is used as the HDR input. HLG, proxy tuning and a mixed-camera timeline remain separate validation tasks.

- [Spatial Film: official control reference](https://spatial.film/resolve/guide/)
