# Set up Resolve manually

Recipe resolve-multicamera-hdr 0.1.0. This is a supported reading path without Kestreel. The JSON files contain the same settings for the future Kestreel adapter; the adapter is not yet implemented. PDFs accompany these instructions as a portable reference.

Source -> camera geometry and input normalization -> DWG/Intermediate -> grade -> PQ or HLG output transform -> encode and verify.

## 1. Files and dependencies
Create a project folder with manifests, workspace/resolve, workspace/intermediates, masters and deliveries. Keep originals separately under YYYY/YYYY-MM/YYYY-MM-DD; retain companions and a verified ingest manifest. Device identity belongs to Kairo, ingestion to Kestreel. Do not rewrite originals to add authorship: use sidecars. Use local SSD cache when useful; a network share is not a substitute for backup.

Install Resolve and each required dependency from resources/dependencies. Record exact versions. Restart Resolve after OFX installation. Paid LUTs and plugin installers remain local under awara-private; public recipes provide links only.

## 2. Resolve project
Create a new project in your Resolve project library. Media Location is not the project database location. Export a .drp snapshot to workspace/resolve at checkpoints; it does not contain source media, plugins or licensed LUTs.

Before creating the timeline choose frame rate to suit the delivery/source (the Action 6 test used 59.94; Osmo 360 used 29.97). Choose the required raster, not a universal square master. In Project Settings > Color Management select DaVinci YRGB, timeline DaVinci WG/Intermediate, no project input/output LUT, and Tetrahedral LUT interpolation. Select the output declaration for the branch being rendered: Rec.2100 ST2084 or Rec.2100 HLG. This declares interpretation; manual YRGB still needs explicit pixel transforms.

Color-managed YRGB can automate supported input/output conversions. This recipe deliberately uses manual YRGB to make plugin and LUT responsibilities explicit. Do not switch modes without redesigning the input/output chain.

## 3. Action 6
Use camera-original D-Log M; Rec.709 container tags do not define its transfer function. For the tested post-stabilization workflow use Wide with RockSteady off. Preserve motion metadata. Apply Gyroflow on the Edit clip, Load for current file, and check Status OK, camera motion and matching lens profile. Lens correction 100 performs dewarp; do not stack an unrelated second dewarp. See the action6 profile for the baseline controls. RockSteady-on footage is already stabilized; do not assume it contains usable post-stabilization metadata.

Purchase the Gamut Action 6 DWG BaseLUT using resources/dependencies/gamut-action6.json. Preserve its vendor original. In Project Settings > Color Management > Open LUT Folder, install a copy as DJI/DJI_Action6_DLogM_to_DWG_Intermediate.cube, then Update Lists. This is a local filename convention, not a DJI-manufactured LUT. Existing projects using the old filename must be reassigned. Use the DWG variant, not Rec.709 or ARRI709.

On Color, apply that LUT once on the first clip node (or Group Pre-Clip for matching clips). Follow it with a neutral Grade node. Never apply it both places. Do not assign the Action 6 LUT to Osmo 360.

## 4. Osmo 360
Keep the OSV. Use Spatial Film OSV Converter to make the importable MP4 twin in workspace/intermediates. The tested twin was byte-identical; verify rather than assuming every conversion is lossless. Import the MP4; fisheyes before the plugin are expected. Place the clip on a timeline. In Edit apply Spatial Film DJI 360 Reframe, open Inspector > Effects > Open FX, and use the osmo360 profile settings. Select Color = DaVinci Wide Gamut/Intermediate. The plugin handles input conversion, stitching, geometry and its stabilization controls; do not add a D-Log M input LUT afterward.

Set Pan Angle keyframes at the beginning and later in the clip, such as 0 and 180 degrees for the test. Keep Tilt/Roll at zero initially. Check intermediate frames, horizon, seam and turn direction. Lens Curve changes projection appearance; it is not a color control. Disable the plugin Proxy checkbox before final export. See the detailed Osmo 360 reference for the tested settings.

## 5. Grade and output
Grade normalized clips in DWG/Intermediate. Camera normalization does not automatically match exposure or white balance. For a single-clip test, use input (if needed), Grade, Output nodes. For a mixed timeline use camera-specific inputs, clip grades, then one final timeline output CST. Avoid simultaneous clip and timeline output transforms.

Apply the selected applications/resolve/delivery JSON settings to the output CST. PQ uses DWG/I -> Rec.2020/ST2084, DaVinci tone mapping and custom maximum output 1000 nits. HLG uses DWG/I -> Rec.2100/Rec.2100 HLG; the recorded Action 6 test used tone mapping None. None requires deliberate control of highlights; it is not an automatic gamut or peak safeguard. Both tests used gamut mapping None, which needs review on new content. The project 1000-nit mastering declaration alone does not limit pixels.

Create separate delivery timelines/settings for PQ and HLG. Do not simply retag PQ as HLG. Duplicate timelines do not provide automatic editorial inheritance. Shared grades and variant synchronization remain a separate development task; preserve independent framing decisions.

## 6. Monitor, render and verify
For the tested Mac/XDR path enable Resolve 10-bit viewers and Mac display color profiles. Use HDR Video (P3-ST 2084) reference mode; disable automatic brightness and True Tone. Monitor P3 does not change Rec.2020 delivery primaries. A screenshot is not a luminance measurement.

Deliver > Custom Export: set a distinct filename and masters/deliveries destination, Single clip, QuickTime, H.265, Main10, chosen timeline raster/frame rate, Video levels, and explicit matching Rec.2020 + ST2084 or HLG tags. Turn off optimized/proxy/cached media for the verification render. Turn off Spatial Film Proxy too. Add to Render Queue and Render All.

Inspect exported metadata and decode the whole file; compare playback on a suitable display. Check duration, framing animation, seams and stability. PQ tags do not prove full HDR10 metadata. Mastering-display/MaxCLL/MaxFALL and platform upload verification are pending; do not invent measurements. The guide records practical visual acceptance, not independent colorimetric accuracy.

## Acceptance and portability
Record source hashes, dependency versions, recipe commit, actual settings and deviations in manifests. Save the project and export a fresh .drp. Reopen it and check media/plugin/LUT availability. Repeat on another machine before claiming portability. Keep paid assets in your own private storage; each user obtains their dependencies from the vendors.
