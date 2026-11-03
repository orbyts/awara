# A ride from camera card to editable telemetry title

Use this guide for a straight-cut cycling film edited in Resolve on a Mac. Make one native-rate, stabilized ProRes master per camera format. Put the graphics on the final vertical or horizontal timeline. Start with one rider, one FIT recording and 59.94 fps throughout. The portrait example was tested in Resolve Studio 21.1.2. Two-event field calibration still needs a ride test on the BSC300T.

## Before leaving

- Set Astra to the Kairo cycling preset: Wide, RockSteady off, D-Log M, square 3840×3840 at 59.94 for this workflow. Record five seconds and check the actual mode. Set each camera's date and local time and keep it consistent throughout the recording.
- Pair power, cadence and optional heart-rate sensors with the bike computer. Check that their live fields change. Identify the manual Lap control and verify with a short recording that the exported FIT contains a manual lap. Disable automatic laps or distinguish them by trigger and sequence. Ensure the ride timer is running during each sync event, including while stationary.
- At the start, start the bike computer and all cameras. While stopped, frame the computer and your finger clearly. Say “start sync,” press Lap once, and keep recording until the lap acknowledgement appears. At the end, repeat with “end sync” **before stopping the FIT recording**. Keep both clips even if they never enter the film. The rest of the camera footage can be intermittent.
- Each camera needs both events. If the cameras cannot see the same press, film a separate identifiable manual lap for each camera at each end and write down the order. For another rider or restarted FIT, keep a separate association. A third filmed lap midway gives you an independent check.

## Ingest and prepare

Mount WHISK and open Ghostty in your Kestreel checkout. Set these variables for the ride. Replace the card path, ride name and FIT filename with yours.

```sh
cd ~/Library/CloudStorage/Dropbox/matrix/packages/kestreel
ride=GGPark-next-ride
project="$WHISK/Movies/projects/$ride"
card=/Volumes/ASTRA
uv run kestreel project init "$ride"
uv run kestreel ingest "$card" --source-kind card --device Astra --dry-run
uv run kestreel ingest "$card" --source-kind card --device Astra
```

Take the verified manifest path from ingest. Copy that manifest to the project and copy the FIT exported by the bike computer. In the example below, replace INGEST_ID and ride-file.fit before running.

```sh
cp "$WHISK/Movies/originals/manifests/INGEST_ID/manifest.json" "$project/manifests/astra-ingest.json"
fit="$project/telemetry/bike-computers/igpsport-bsc300t/ride-file.fit"
cp "$HOME/Downloads/ride-file.fit" "$fit"
uv run kestreel verify "$project/manifests/astra-ingest.json"
uv run kestreel-title --laps "$fit"
```

Check the manual lap end timestamps printed in UTC against the order of the filmed presses. If the computer omitted a marker, label the alignment provisional. A speed peak or a later change in displayed cadence is a poor clock reference.

Open Resolve with local scripting enabled. Create the camera timeline once for a new Resolve project; inspect the plan by omitting `--apply` first. Use the input LUT installed on your machine. This example filters accidental 29.97 captures from a 59.94 ride.

```sh
uv run kestreel project camera-timelines "$project/manifests/astra-ingest.json" \
  --name "$ride" --capture-fps 59.94 --working-space dwg \
  --lut 'DJI/DJI_Action6_DLogM_to_DWG_Intermediate.cube' --apply
```

If Resolve has just opened an empty Untitled Project, add `--allow-empty-untitled` after checking it is empty. On a second camera, use its own ingest and normalization recipe. For the current title build, put only camera masters recorded at the delivery frame rate on V1.

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

1. Create the delivery timeline at **1080×1920** or **1920×1080**, using the master frame rate for this build. Import the master MOV on V1 and trim, reorder and reframe it. For an HLG story, view/transform the DWG master to Rec.2100 HLG once, and place graphics in the intended delivery space. Avoid sending already display-ready graphics through a camera input LUT. Check text brightness on your HDR monitor.
2. On Edit, drag a **Fusion Composition** from Effects onto V2. Extend it across the desired story range. Right-click it, select **Import Fusion Composition**, and choose [Vertical.comp](../../applications/resolve/fusion/ride-titles/Vertical.comp) or [Horizontal.comp](../../applications/resolve/fusion/ride-titles/Horizontal.comp). Keep one title composition on that item. Keep this title track over your camera cuts.
3. Open the V2 item in Fusion. **PanelPosition** moves the whole graphic; **PanelShape** controls width, height and corner radius; **Panel** controls opacity. Adjust the Text+ nodes' Center, Size, Font and Style to set spacing and hierarchy. Edit the label nodes freely. Keep the value node names `SpeedValue`, `PowerValue` and `CadenceValue`; Kestreel writes only their Styled Text. For heart rate, duplicate a value and label, rename the value **HeartRateValue**, label it “Heart rate BPM,” and merge the row before PanelPosition. Omit a metric by removing its row. Missing readings display a dash.
4. Save a reusable layout **before** populating real ride data: right-click the V2 item and export its Fusion composition to your template folder. Use a separate filename for each aspect ratio. A composition exported after refresh contains private rider keyframes. To make a reusable layout from an already-populated title, first remove animation from the value nodes' Styled Text and replace the values with dashes.
5. With the delivery timeline active, refresh the data. Replace the timeline name below. For two cameras, pass a second `--sync` with that camera's anchor file. Each imported master needs its matching, same-stem `.capture-map.json` next to the MOV.

```sh
uv run kestreel-title --timeline 'Vertical Story' \
  --sync "$project/sync/astra/igpsport-bsc300t/ride-title.json"
```

Play across each cut. The numbers should jump to the incoming shot's capture time and a missing FIT record older than three seconds displays a dash. Move the panel, refresh again, and confirm the layout stays where you placed it. Refresh after changing cuts. This build supports native-rate straight cuts, one FIT per camera per pass, a single footage track and V2 titles. Speed changes, dissolves, nested sequences, overlapping picture, and mixed frame rates need separate timing work.

## Export and check

In Deliver select Single Clip and your delivery timeline's full range. For the vertical HLG Story use QuickTime HEVC Main10, 1080×1920, timeline fps, BT.2020 primaries, HLG transfer and audio. Save the shareable file under the project's `deliveries/`. Play the exported file at the beginning, on both sides of each cut and on the last frame. Check framing, readability and gaps in telemetry. Inspect the file metadata with:

```sh
ffprobe -v error -show_entries stream=codec_name,profile,width,height,r_frame_rate,color_primaries,color_transfer -of json "$project/deliveries/Vertical-Story.mov"
```
