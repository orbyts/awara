# A ride from camera card to editable telemetry title

For the current executable sequence, see **[Cycling footage: commands from card to HDR](ride-command-guide.md)** (updated November 6, 2026). It covers mounted storage, portable date selections, separate retrim/HDR projects, and deletion. The Fusion authoring notes below remain intact.

Use this guide for a straight-cut cycling film edited in Resolve on a Mac. Make one native-rate, stabilized ProRes master per camera format. Put the graphics on the final vertical or horizontal timeline. Start with one rider, one FIT recording and 59.94 fps throughout. The portrait example was tested in Resolve Studio 21.1.2. Two-event field calibration still needs a ride test on the BSC300T.

## Before leaving

- Set Astra to the Kairo cycling preset: Wide, RockSteady off, D-Log M, square 3840×3840 at 59.94 for this workflow. Record five seconds and check the actual mode. Set each camera's date and local time and keep it consistent throughout the recording.
- Pair power, cadence and optional heart-rate sensors with the bike computer. Check that their live fields change. Identify the manual Lap control and verify with a short recording that the exported FIT contains a manual lap. Disable automatic laps or distinguish them by trigger and sequence. Ensure the ride timer is running during each sync event, including while stationary.
- At the start, start the bike computer and all cameras. While stopped, frame the computer and your finger clearly. Say “start sync,” press Lap once, and keep recording until the lap acknowledgement appears. At the end, repeat with “end sync” **before stopping the FIT recording**. Keep both clips even if they never enter the film. The rest of the camera footage can be intermittent.
- Each camera needs both events. If the cameras cannot see the same press, film a separate identifiable manual lap for each camera at each end and write down the order. For another rider or restarted FIT, keep a separate association. A third filmed lap midway gives you an independent check.

## Ingest and prepare

Follow [steps 1–6 of the command guide](ride-command-guide.md#1-start-a-ride-session). That is the maintained command sequence. In particular, do not copy a relative-path ingest manifest directly into a project folder: use the selection script, which recalculates its originals root. Use the separate retrim project and apply Gyroflow manually.

The command guide sets `project` to the retrim project directory and stores its selection at `manifests/astra-ingest.json`, matching the examples below.

## Record the two clock anchors

Open each sync clip in the source viewer. Step to the same physical instant for each press, such as first visible button depression. Record the **zero-based source frame counted from the original clip's first displayed frame**. Source frame 0 is the first image. A timeline frame number or the camera's time-of-day timecode needs conversion first. You can place the untrimmed sync clip alone on a temporary native-rate timeline starting at frame zero and use a frame-count display.

Save `ride-title.json` under `sync/astra/igpsport-bsc300t/`. Replace every example value with the actual original filename from the ingest manifest, measured frame, and FIT lap end UTC. Paths are relative to this JSON. The two example timestamps below are illustrative.

```json
{
  "fit": "../../../telemetry/bike-computers/igpsport-bsc300t/ride-file.fit",
  "manifest": "../../../manifests/astra-ingest.json",
  "fps": "60000/1001",
  "anchors": [
    {"original": "FIRST_SYNC_CLIP.MP4", "frame": 120, "utc": "2026-11-04T17:00:02Z"},
    {"original": "LAST_SYNC_CLIP.MP4", "frame": 180, "utc": "2026-11-04T19:00:03Z"}
  ]
}
```

Kestreel computes camera time as the manifest clip start plus source frame divided by capture fps. One anchor supplies a constant offset. Two anchors also fit the ratio of elapsed FIT time to elapsed camera time. Compare the predicted UTC of the optional middle press with its recorded UTC. Whole-second FIT timestamps, filename clock precision and button visibility all limit accuracy. If the middle press agrees but cadence or power lags the filmed action, treat that as sensor/reporting delay. If a camera clock was reset, split that recording period and calibrate separately.

## Trim, stabilize and render the camera master

1. On the camera prep timeline apply Gyroflow manually to each original. Play moving footage and check the frame shape and stabilization before trimming. Keep the original ingest and sync clips available.
2. Apply the camera-to-DWG/Intermediate input conversion once and grade in DWG/Intermediate. For a **DWG/Intermediate ProRes master**, use manual DaVinci YRGB and set both timeline and output color space to **DaVinci WG/Intermediate**. On an existing ACEScct prep timeline, bypass only its final DWG-to-ACEScct timeline CST. A change to the output-space setting alone does not undo a baked conversion. Preserve creative nodes and clip input transforms.
3. With the trimmed prep timeline active, run the command below. Replace PREP_TIMELINE with the exact name in Resolve. Kestreel prepares Single Clip, full timeline, native size and rate, QuickTime ProRes 422 HQ and PCM audio. Inspect Deliver, then add the job and render. Keep the MOV, FCPXML and capture map together under `masters/<camera>/<version>/`. For handoff include a note specifying **DaVinci Wide Gamut primaries / DaVinci Intermediate transfer**, native fps, and whether stabilization and creative grades are baked. A generic MOV tag cannot convey that whole description.

```sh
uv run kestreel project camera-delivery "$project/manifests/astra-ingest.json" --timeline 'PREP_TIMELINE'
```

Re-import the new master as DWG/Intermediate and compare a frame to the prep through the same viewing transform. Check frame count against `master_frames` in the capture map. When an external facility specifically requests linear ACES interchange, agree on an **ACES2065-1 (AP0/linear) OpenEXR** delivery; this guide's ProRes preset is for the log intermediate. [ACES encodings](https://docs.acescentral.com/encodings/overview/)

## Edit the film and author its title

1. Create the delivery timeline at **1080×1920** or **3840×2160**, using the master frame rate for this build. Import the master MOV on V1 and trim, reorder and reframe it. For these HLG layouts, composite the overlay with the DWG/Intermediate footage, then use the final timeline CST to convert DWG/Intermediate to Rec.2100 HLG. Check text brightness through that final transform on your HDR monitor.
2. On Edit, drag a **Fusion Composition** from Effects onto V2. Extend it across the desired story range. Right-click it, select **Import Fusion Composition**, and choose [Vertical.comp](../../applications/resolve/fusion/ride-titles/Vertical.comp) or [Horizontal.comp](../../applications/resolve/fusion/ride-titles/Horizontal.comp). Keep one title composition on that item. Keep this title track over your camera cuts.
3. Open the V2 item in Fusion. **PanelPosition** moves the whole graphic; **PanelShape** controls the shared panel center, width, height and corner radius; **Panel** controls opacity. All six Text+ Center expressions follow PanelShape. Edit their expression offsets, Size, Font and Style to set spacing and hierarchy. Edit the label nodes freely. Keep the value node names `SpeedValue`, `PowerValue` and `CadenceValue`; Kestreel writes only their Styled Text. For heart rate, duplicate a value and label, rename the value **HeartRateValue**, label it “Heart rate BPM,” and merge the row before PanelPosition. Omit a metric by removing its row. Missing readings display a dash.
4. Save a reusable layout **before** populating real ride data: right-click the V2 item and export its Fusion composition to your template folder. Use a separate filename for each aspect ratio. A composition exported after refresh contains private rider keyframes. To make a reusable layout from an already-populated title, first remove animation from the value nodes' Styled Text and replace the values with dummy readings.
5. With the delivery timeline active, refresh the data. Replace the timeline name below. For two cameras, pass a second `--sync` with that camera's anchor file. Each imported master needs its matching, same-stem `.capture-map.json` next to the MOV.

```sh
uv run kestreel-title --timeline 'Vertical Story' \
  --sync "$project/sync/astra/igpsport-bsc300t/ride-title.json"
```

Play across each cut. The numbers should jump to the incoming shot's capture time and a missing FIT record older than three seconds displays a dash. Move the panel, refresh again, and confirm the layout stays where you placed it. Refresh after changing cuts. This build supports native-rate straight cuts, one FIT per camera per pass, a single footage track and V2 titles. Speed changes, dissolves, nested sequences, overlapping picture, and mixed frame rates need separate timing work.

## Approved first draft and next design pass

The horizontal and vertical compositions above are the approved first draft from November 3, 2026. Both have a shared background at alpha 0.189, corner radius 0.276 and text RGB 0.501960784313725. Each retains its authored typography, spacing and panel position. Reusable files contain dummy speed 25.0 MPH, power 250 W and cadence 90 RPM. Ride keyframes and Resolve cache paths have been removed.

The existing kestreel-title refresh command animates SpeedValue, PowerValue and CadenceValue after importing the appropriate template on V2. It also supports HeartRateValue when that node is present. These drafts contain three fields. Refresh populates the current composition; import the desired template first when starting a new title. Re-importing a template resets its readings to the dummy values until the next refresh.

File checks confirmed dimensions, six panel-relative expressions and valid node references in both templates. A synthetic test of Kestreel's existing refresh function confirmed changing speed, power and cadence on two mock titles and a successful repeat refresh. Live Resolve refresh and final HLG appearance require a user-run check.

The next design pass will author each widget separately while using one shared panel, with optional separator lines to be judged visually. Planned widgets include a speed dial and numeric reading, power, cadence, heart rate and heart-rate zone. Whether the zone is separate remains open. Planned configuration will hold independent horizontal and vertical layouts, widget sizes, gaps, order and six user-authored anchor coordinates for bottom-left, bottom-right, top-left, top-right, center-left and center-right. Kestreel will eventually select requested metrics and stack the enabled widgets. Metric flags, config-driven placement and numeric dial animation are pending implementation after Fusion authoring.

## Speedometer widget refresh

Import `applications/resolve/fusion/ride-titles/widgets/Speedometer.comp` on V2 to use the standalone speedometer. The development checkout of Kestreel now detects `SpeedometerControls` and refreshes its `NumberIn1` current speed and `NumberIn2` running average, both in MPH. It preserves the widget's Styled Text expressions, colors, `NumberIn3` maximum and `NumberIn4` red threshold. The same `kestreel-title --timeline NAME --sync FILE` command supports this widget and the original text layouts. Numeric keys hold readings across cuts and data gaps. Missing values use -1 internally, display a dash and hide active arcs.

The running average is time-weighted recorded speed from the beginning of the FIT recording, including recorded zero-speed stops. Each record contributes until the next record or three seconds, whichever comes first. Longer gaps and invalid readings contribute no duration. This definition can differ from a bike computer's timer-based or moving average. The average follows original ride time when footage is reordered. Real ride parsing and camera-map matching have been checked privately, alongside synthetic regression tests for reordered shots, gaps and repeat refresh. Live Resolve refresh remains to be checked by the user.

### Speedometer appearance and placement

The November 4 revision puts the background around the complete widget stack. The speedometer supplies a transparent 1000×1000 image and the optional numeric power widget has the same 1000-pixel width and an editable height (default 320, minimum 240). `PanelControls` selects speedometer and power using 0/1 controls and sets power height, gap and padding. Speedometer is enabled and power is disabled by default. With 40-pixel padding, speed alone creates a 1080×1080 panel; adding power with a 24-pixel gap makes it 1080×1424. Disabled widgets leave no vacant row.

`Panel` supplies the single black background at alpha 0.189, and `PanelShape` supplies its rounded rectangle. Change Panel alpha to zero for transparent backing while retaining all widget graphics. `PanelPosition` is the final Merge of the assembled stack onto the transparent 3840×2160 `FrameCanvas`; use its Center and Size for the entire stack. Its initial Size is 0.5 at Center 0.14, 0.22. Internal widget positions are calculated from the enabled heights and padding, so moving or scaling the panel moves all widgets together. The controller nodes use Fusion's registered `Custom` tool type. PowerValue retains its standard name for the existing Kestreel refresh. Six-anchor config selection and additional widget types remain planned.

The single current-speed arc switches its entire color above the threshold (default 30 MPH). It has no separate red endpoint or red segment. Zero and missing readings hide the active arc at its Merge so a zero-length stroke cannot leave a visible cap. Current and average speed inputs and their real-data refresh remain the same.

`CurrentTint`, `HighSpeedTint`, `AverageTint`, `TextTint` and `TrackTint` define base colors. `BrightnessControls` supplies overall and relative component RGB gains. Expressions uniformly limit the gain using the largest color channel so rendered source RGB stays at or below 0.49 while preserving the tint's channel ratios. These are source signal values, not measured luminance or a promise of 49% HLG display brightness. `DetailControls` exposes the two arc widths and the speed, average, unit and scale font sizes. Text and icon brightness are independently adjustable even though they share TextTint.

The template contains synthetic demo animation. Import it, then run the same kestreel-title refresh to populate real ride readings. Syntax, connections, threshold behavior, zero/missing visibility and RGB limits have been checked, and the existing refresh regression tests pass. The updated render, the disappearance of the startup warning in the saved project and the reported cyan shift through the user's live timeline still require Resolve verification.

## Export and check

In Deliver select Single Clip and your delivery timeline's full range. For the vertical HLG Story use QuickTime HEVC Main10, 1080×1920, timeline fps, BT.2020 primaries, HLG transfer and audio. Save the shareable file under the project's `deliveries/`. Play the exported file at the beginning, on both sides of each cut and on the last frame. Check framing, readability and gaps in telemetry. Inspect the file metadata with:

```sh
ffprobe -v error -show_entries stream=codec_name,profile,width,height,r_frame_rate,color_primaries,color_transfer -of json "$project/deliveries/Vertical-Story.mov"
```

## Modular authoring requirements (November 4)

The current Fusion prototype's placement is not yet visually validated: the user's review showed the widget separated from its panel. The replacement assembler must combine the local widget stack and its background before one shared placement/scale transform. Moving the panel must move every widget, including when background opacity is zero.

Each widget declares a common width, its own height, editable geometry/text/style and separate telemetry bindings. Only selected widgets occupy space. Panel height is the sum of selected heights, gaps and top/bottom padding; speed alone produces a square panel. One translucent rounded background surrounds the stack, with optional separators. Opacity, position, overall scale and relative component brightness remain independent controls.

Planned Kestreel selectors include `--speed --power --cadence --heartrate` and six mutually exclusive positions: bottom-left/right, top-left/right and center-left/right. These CLI selectors and the modular assembler are requirements, not implemented interfaces. Configuration stores widget order, dimensions, padding/gaps and separate horizontal 3840×2160 and vertical 1080×1920 profiles. The user authors each profile's scale and six anchor coordinates. Corner anchors attach to panel edges; center-side anchors attach to the side midpoint, so changing stack height preserves placement intent.

Speed uses current and running-average arcs, a central gauge icon and numeric MPH. Maximum defaults to 50 MPH; above an editable 30 MPH threshold the whole current arc changes to its editable high-speed color. There is no red endpoint dot. Native Fusion animation continues to use real-data numeric inputs, independent of appearance edits. Initial source RGB stays below .5 with an editable overall gain and component-relative gains; this is not a display-luminance guarantee.

### Photoshop design capture

Use the scripts under `scripts/photoshop/` to create editable vector/text PSD samples and export exact layout JSON. The 1000×1000 master defines local widget geometry. Review documents show provisional scales of .5 (horizontal) and .3 (vertical), with one shared panel and bottom-left placement. These are independent documents, not linked instances. Other anchors and widgets remain to be authored.

Keep `layout.slot.speed` (zero opacity) as the explicit allocation rectangle. Visible ink bounds are not a widget's layout dimensions. Preserve named groups and layers. Move/scale the entire `overlay` group in a review document to keep panel and widget together. Put exported video stills inside `reference.drop-footage-here`; reference layers are excluded from metadata export.

After saving edits, run `export-telemetry-layout.jsx` through File > Scripts > Browse. It writes adjacent `.layout.json` with document size/profile, layer hierarchy, bounds, opacity, native vector anchors/handles, fill descriptors and live text properties. This supports measured reconstruction; the automatic JSON-to-Fusion importer is still pending. Rasterized text, warped layers and arbitrary effects are outside the initial reconstruction contract.

Documents are 32-bit linear sRGB proofs. The footage still's encoding/profile must be known before judging its appearance. Photoshop and Resolve's DWG/Intermediate-to-HLG pipeline may differ materially; approve geometry in Photoshop and approve final brightness/color/opacity over animated footage in Resolve. The sample values are dummy readings, not live telemetry.

### Horizontal Photoshop comparison test

`applications/resolve/fusion/ride-titles/widgets/Speedometer-Horizontal-Authored.comp` is the speed-only test built from the user's November 4 horizontal Photoshop capture. The original generic Speedometer.comp remains separate. Rebuild with `python3 scripts/fusion/build-horizontal-speedometer.py INPUT.layout.json OUTPUT.comp`.

The authored widget slot is 333.608 pixels square, centered at frame pixel (255.611, 1079.996). The panel's own vector contour is slightly inset within that slot; its alpha is 0.7294118. The average label has its authored above-left position. All graphics and the panel are assembled on one 1000×1000 transparent canvas, then `PanelPosition` applies scale 0.333608137 and normalized center (0.066565270, 0.500001990) over the 3840×2160 output. Adjust this final Merge to move/scale the entire overlay. Adjust `Panel.TopLeftAlpha` to change only the backing opacity.

For a same-frame comparison, the initial readings are static 28.0 MPH and AVG 19.5, matching the Photoshop sample. `SpeedometerControls` retains numeric inputs 1/2 for real-data refresh, 3 for maximum (50 MPH), and 4 for the red threshold (30 MPH). On a V2 title, the existing Kestreel refresh replaces only the current/average data. The test has no power widget or power controls. Compare the static design before refreshing, since the real readings on the reference frame may differ.

Static contour anchors and handles come directly from the captured PSD. Animated arcs use the captured tracks' centerlines with native Fusion WriteLength; their cap rendering may differ from Photoshop's filled contours. Text uses the effective transformed font sizes and measured ink centers; font metrics/rasterization need visual verification. RGB numbers are copied as provisional input values, not a linear-sRGB-to-DWG color transform. Retain the existing timeline color-management pipeline for the first comparison and adjust only after reviewing the reference frame. Lua syntax and all 43 tool references were checked; the live Resolve render is pending.

The first same-frame user comparison showed Fusion text approximately two-thirds the Photoshop size relative to the panel. The builder now exposes `DetailControls.NumberIn7` (Photoshop text size calibration), default 1.5, multiplied into all five Text+ sizes. This is empirical calibration pending another visual check, not a universal type-size conversion. Panel alpha and position remain unchanged; the user plans to move the overlay lower.

### Main inspector controls

The next horizontal revision adds `MainControls`: panel opacity, normalized center X/Y, overall scale, and background-track RGB. RGB defaults to neutral .30 and remains subject to BrightnessControls' track gain and .49 source ceiling. These controls affect both unfilled dial tracks, not the active average/current arc colors. Panel alpha is clamped to 0–1; scale has a positive minimum. Placement operates on the entire assembled square widget.

For an existing comp, run `scripts/fusion/add-speedometer-main-controls.lua` in the Fusion Lua Console. It captures the current static placement, size and panel opacity, adds the controller and connects expressions; it does not replace telemetry inputs or change detail settings. Do not use it to migrate animated panel transforms: it captures the values at the current frame. It refuses to add a duplicate MainControls. Syntax is checked; live execution needs verification in Resolve.

The rebuilt template adopts the screenshot's .047/.018 arc widths, .251792/.078463/.091/.102 font sizes and 1.072/.964/1.065 overall/current/average gains. Its text multiplier is now 1 to avoid applying the earlier 1.5 calibration twice. The rebuilt file still starts with the captured Photoshop placement/opacity; the in-place script preserves the more recent live settings instead.

Both dial background tracks now use open, full-length stroked centerlines, matching the native rounded caps of their animated arcs. Their widths follow the same current/average DetailControls inputs. For an existing comp, `scripts/fusion/round-speedometer-tracks.lua` copies the current arc paths into the corresponding track masks and sets full-length strokes. Panel opacity, placement, colors, fonts and telemetry are untouched. The rebuilt template has the same change. Syntax and path/width connections are verified; live rendering of the patch remains to be checked.

## Approved horizontal speedometer default (November 4)

The working live Fusion composition was exported after the user confirmed rounded background arcs. Its exact tool graph is now `applications/resolve/fusion/ride-titles/Horizontal.comp`, the path already loaded by Kestreel's `hdr_project.py`. The same graph is stored separately as `widgets/Speedometer-Horizontal-Default.comp` for the speed module. The previous multi-value text layout is preserved as `Horizontal-Text-Legacy.comp`; Vertical.comp is unchanged. This saved live default supersedes the earlier Photoshop comparison template and its provisional defaults.

Approved MainControls: opacity .316, center (.059, .254), scale .254, track RGB (.3, .3, .3). DetailControls: current/average widths .047/.018; speed/average/unit/scale fonts .251792/.078463/.091/.102; text multiplier 1. Brightness gains: overall 1.072, current .964, average 1.065, text/icon/track 1. The current and average arcs retain numeric telemetry bindings, editable maximum 50 MPH and threshold 30 MPH, with rounded full-length background tracks.

The export removes project cache paths, editor workspace state and ride-specific duration limits. The reusable preset starts at dummy 28 MPH / AVG 19.5, with no recorded ride keyframes. Kestreel's HDR builder imports Horizontal.comp and then runs refresh; the standalone kestreel-title command refreshes an existing comp without replacing its appearance.

Verification: the configured Kestreel Awara root points at this checkout. The default parses as Lua, all 60 saved tools/modifiers have valid source references, and the standalone speed module is identical to the horizontal default. Three existing telemetry regression tests pass. A live refresh on Horizontal HLG populated one title and sampled 101 frames: current speed, running average and rendered arc WriteLength varied; all MainControls, DetailControls and BrightnessControls values remained unchanged. The Resolve project was saved. This validates the data bindings in the working comp; a complete new-project build was not performed.

### Module roadmap

Speedometer is the first approved module and the only enabled module in this horizontal default. Next: independently author power and cadence; then heart rate and heart-rate zone. All are optional and will contribute their own height to the shared panel only when selected. A route/location map is future work. `horizontal-default.json` records the enabled speed module and planned registry, but the dynamic assembler and metric-selection flags remain pending. Do not treat the current speed-only default as a permanent monolithic design.

### Revised threshold behavior

The user revised the requirement: only the portion above the speed threshold changes color. The normal current arc remains underneath a separate HighSpeedArc segment. ZoneControls exposes threshold MPH and normal/above-threshold RGB. SpeedometerControls.NumberIn4 references the threshold for compatibility. The high segment starts at clamped threshold / maximum, has length max(0, clamped speed - clamped threshold) / maximum, and its Merge is hidden at or below threshold to avoid a zero-length dot. Both colors retain brightness gain and source ceiling. Rounded stroke caps remain.

This revision was applied to the live Horizontal HLG comp, saved to the Resolve project, and captured into Horizontal.comp and Speedometer-Horizontal-Default.comp with telemetry keyframes removed from the reusable defaults. Live evaluation checked 301 ride frames, including two above-threshold frames: segment start, length and visibility matched the formulas. ZoneControls defaults to 30 MPH and preserves the previous normal/high RGB tints. This supersedes the earlier whole-arc color-switch requirement. The Photoshop comparison generator and reusable Lua upgrade script also implement the new behavior.

### Independent above-threshold HSB controls

ZoneControls inputs 5–7 now expose hue (degrees, wrapped at 360), saturation (0–1) and HSV brightness (0–.49), replacing the high segment's RGB controls. Inputs 2–4 remain normal-arc RGB. This is HSV brightness, not HSL lightness or measured HDR luminance. Lower saturation moves the high segment toward grey; lower brightness dims it independently. Existing overall/current gain and the .49 source RGB ceiling still apply downstream.

The live upgrade preserved the previous color by converting its RGB to HSV: hue 0°, saturation .6695652062, brightness .4509803951. A live test checked green hue, zero-saturation grey and lower red brightness, then restored the authored values. Main/Detail/Brightness controls and 101 samples of current speed, average speed, both arc lengths, high-segment start and visibility were unchanged. The Resolve project and reusable Horizontal.comp / Speedometer-Horizontal-Default.comp were saved. The Photoshop builder uses the same HSV expressions. The earlier Lua zone-installer creates the older RGB controls; `scripts/fusion/add-speedometer-hsb.py` upgrades those, while new builds use HSV directly.

## JSON-driven horizontal design

`applications/resolve/fusion/ride-titles/horizontal-default.json` is now schema version 2 and is consumed by Kestreel's HDR project builder. The enabled module list currently contains only `speed`. Its module entry selects `widgets/Speedometer-Horizontal-Default.comp`, retaining native editable geometry, masks and expressions. JSON `settings` stores 49 authored design inputs: MainControls, DetailControls, BrightnessControls, ZoneControls, maximum speed, average/text tint RGB, and the five text layers' fonts, styles and centers. `control_labels` explains the numbered Fusion inputs. The latest captured high-zone HSV is 0°, .221 saturation and .473 brightness.

Build order: validate JSON and resolve its module template before creating the project; import the horizontal native comp; apply and read back every configured design value; then refresh current/average speed from the ride. Vertical generation remains unchanged. Invalid or unsupported widget selections fail explicitly until optional module assembly exists. Paths are confined to the overlay asset folder. Telemetry fields, text expressions and geometry are not accepted as JSON setting overrides.

Use `scripts/fusion/capture-horizontal-design.py` with Kestreel's Python environment to capture later Inspector edits from the single speedometer on the current Horizontal HLG timeline. It updates the design JSON only. Editing JSON changes subsequent project builds; the normal kestreel-title refresh continues to preserve the existing live design rather than resetting it to defaults. The native module supplies structural values such as vector control points; changing those requires updating the module template as well.

Kestreel implementation: `overlay_config.py` validates and applies the settings; `hdr_project.py` loads this config for horizontal builds. Tests cover valid loading, unsupported modules, prohibited telemetry overrides, invalid numeric ranges and preservation of telemetry/text expressions. Five overlay/telemetry tests pass and the changed Python files pass lint. A full new delivery project was not created during this update.

Live validation also passed: applying and reading back all 49 JSON inputs preserved the current design exactly; real-data refresh then left those settings unchanged. Current speed and above-threshold arc length varied across 101 sampled frames. The Resolve project was saved and both reusable horizontal comp files were synchronized to the captured config, without ride keyframes.

### Controls Underlay and exporting future tweaks

The approved horizontal template includes a native `SPEEDOMETER_CONTROLS` Underlay containing MainControls, DetailControls, BrightnessControls, ZoneControls, SpeedometerControls, AverageTint and TextTint. The live layout was arranged with the Flow API and the Underlay fitted through Fusion's Select Tool command around the selected nodes. This is visual organization only.

After changing panel position, scale, opacity, arc/font sizes, HSB or the included tints/text centers, run this in the Fusion Lua Console with the horizontal speedometer open:

```lua
dofile("/Users/suhail/Library/CloudStorage/Dropbox/matrix/awara/scripts/fusion/export-horizontal-design.lua")
```

The script captures 49 current design inputs into `applications/resolve/fusion/ride-titles/horizontal-default.json`, preserves the previous file as `horizontal-default.json.previous`, and atomically replaces the JSON. It does not export ride readings or keyframes, and does not modify the comp. Kestreel uses the exported settings on the next horizontal build. This captures current values, not animation curves for design controls. Native shape changes still require updating the Fusion module template.

The exporter was executed in live Fusion and its resulting JSON was parsed and compared with the prior config: all 49 values matched, and the backup was present. The Underlay is saved in both default comp files. All design values and changing real-data speed were rechecked after node organization.


## Modular tile plumbing — 2026-11-05

The modular build is opt-in through `overlay-layout.json`. The approved standalone
horizontal speedometer remains available. Dimensions below are **rows × columns**;
JSON uses explicit `rows` and `columns` to avoid ambiguity.

| Variant | Dimensions | Horizontal anchors | Vertical anchors |
| --- | --- | --- | --- |
| full-square | 2×2 | Corners, center-left/right | Unsupported |
| compact-tall | 2×1 | Corners, center-left/right | Corners, center-left/right |
| compact-wide | 1×2 | All eight | Corners, center-top/bottom |
| minimal-square | 1×1 | All eight | All eight |

Whole-panel constraints apply in addition to each widget's constraints. Initially,
center-top/bottom allow only one row. The config also supplies separate orientation
frame sizes, tile sizes and edge margins. These initial margin/scale values require
visual review. Layout calculates the completed panel bounds before positioning it.
No automatic shrinking, rotated variants or empty cells are allowed.

Initial presets:

- Horizontal: full-square speed above separate minimal-square power and cadence;
  three rows by two columns.
- Vertical: compact-tall speed on the left, power above cadence on the right;
  two rows by two columns.

Packing follows requested order, row-major, trying the configured maximum width
then narrower widths. Full-square speed plus power alone is rejected. Power alone
is valid. Two compact-wide widgets are geometrically compatible where allowed,
but building requires authored templates; unavailable variants fail explicitly.

### Configuration boundaries

`applications/resolve/fusion/ride-titles/overlay-layout.json` declares the variant
matrix, orientation profiles, shared background/separators, presets and registry.
`modules/<metric>/<variant>.json` declares dimensions, renderer, design settings,
output node and data bindings. Power and cadence are independent modules.

Native Fusion modules use `fusion-template`, optional legacy speed `design_config`,
and generic per-node `inputs` overrides. Node names must be unique across modules.
The `numeric-tile` renderer currently creates editable 1×1 text widgets. New modules
can reuse either renderer without changing the packer. New visual renderers and new
telemetry sources still require an implementation; extensibility does not imply an
automatically available map renderer or new data adapter.

Bindings map data sources to Fusion inputs, for example Power → PowerValue.StyledText.
The generated composition embeds `Kestreel.BindingsJSON`; the HDR builder also sets
it explicitly. Refresh uses these bindings, retaining legacy discovery for old comps.
Speed/average remain numeric animation inputs; power/cadence use text animation.
Shared panel controls act after widget assembly, so placement/scale affects all tiles;
background opacity does not reduce widget opacity. Separators appear only between
occupied modules, not through a multi-cell widget.

### Build and review

From the Kestreel package directory:

```bash
uv run kestreel-overlay --orientation horizontal --position bottom-left \
  --output /private/tmp/Horizontal-Modules.comp
uv run kestreel-overlay --orientation vertical --position bottom-left \
  --output /private/tmp/Vertical-Modules.comp
```

With no metric flags, these use orientation-specific presets. Explicit selection:
`--speed compact-tall --power minimal-square --cadence minimal-square` for vertical.
Bare `--speed` selects full-square and is therefore invalid for vertical.
Each build also writes a `.layout.json` containing computed geometry and bindings.
To use the modular configuration in the existing HDR build, add
`--overlay-config /Users/suhail/Library/CloudStorage/Dropbox/matrix/awara/applications/resolve/fusion/ride-titles/overlay-layout.json`;
`--orientation horizontal|vertical|both` restricts the generated delivery formats.
Other existing HDR build arguments, including ride synchronization, still apply.

Generated drafts are under `ride-titles/previews/`. Full-square speed retains the
approved design. Compact-tall speed, power and cadence are **draft designs**, not
visually approved. Automated tests cover packing, anchors, placement restrictions,
empty-cell rejection, configuration and telemetry binding validation. Live Resolve
verification of these new assemblies remains pending: scripting connection was
unavailable at the final check. Do not treat static demo numbers as ride animation.

The existing horizontal Lua exporter captures the original 49 speed design inputs;
it is not a complete modular-layout exporter. Layout margins, tile sizes and the new
module definitions currently remain authored in JSON. A modular capture/export flow
is a separate follow-up before relying on Fusion tweaks as new module defaults.

Next: visually author/approve the compact-tall speed and the independent power and
cadence minimal tiles, then verify both assemblies against synchronized footage.
Later: heart rate and heart-rate zone modules; route/map support remains future work.
