# Cycling footage: commands from card to HDR

Updated November 6, 2026. Run these commands yourself in Ghostty, from the Kestreel checkout. This guide uses one Astra camera, manual Gyroflow, a DWG/Intermediate camera master, and a separate HDR project. Fusion designs are still being authored; the commands consume the current saved templates without changing them.

## One-time environment setup

These are prerequisites, not commands to repeat for every ride. Your shell already provides `WHISK` and `DROPBOX`. The actual WHISK mount on this Mac is `/Volumes/whisk`. Setting a variable does not mount a volume.

```bash
export WHISK="/Volumes/whisk"
export KESTREEL_ORIGINALS="$WHISK/Movies/originals"
export KESTREEL_PROJECTS="$WHISK/Movies/projects"
```

Alternatively, set `paths.originals` and `paths.projects` in `~/.config/kestreel/config.toml`; the environment overrides take precedence. Keep the existing Awara and Kairo configuration. Reconnect the share if Kestreel reports an unmounted volume. Do not create a local replacement directory. `/Movies/...` in an error usually means `$WHISK` was empty.

## 1. Start a ride session

**Example project name: `Example-ride`.** Replace that exact string throughout this guide with your ride name. It produces `Example-ride-retrim` for camera preparation and `Example-ride-HDR` for delivery. The same name is used in cleanup; do not switch names mid-workflow.

Run the blocks in order in the same Ghostty shell. Besides the project name, supply the actual recording date, ingest ID returned by ingestion, and FIT filename when those steps ask for them. Hardware-generated identifiers cannot be inferred from a project name.

```bash
cd "$DROPBOX/matrix/packages/kestreel"

ride_name="Example-ride"
capture_date="2026-11-06"  # Change to the CAMERA recording date.
prep_name="${ride_name}-retrim"
hdr_name="${ride_name}-HDR"
project="$WHISK/Movies/projects/$prep_name"
card="/Volumes/SD_Card"
```

Mount WHISK before continuing. The remaining workflow assumes your environment and Kestreel configuration are already set.

## 2. Make the recording setup repeatable

Before leaving home, save a cycling Custom Mode: D-Log M, 3840×3840, camera 60 fps (normally recorded as 60000/1001), Wide, EIS/RockSteady off, and the intended exposure compensation. PRO alone is not confirmation of the selected color mode.

Assign QS to **Lock Screen**, then use the physical shutter button during the ride. Avoid editing EV in the field by saving the preferred value ahead of time. SnapShot can start recording from powered off; test its configured recording mode once at home before relying on it. Screen Lock is not a documented lock on every physical control. See [DJI Action 6 support](https://www.dji.com/support/product/osmo-action-6) and the [manual](https://dl.djicdn.com/downloads/DJI_Osmo_Action_6/UM/1104/DJI_Osmo_Action_6_User_Manual_v1.0_en.pdf).

For the new handheld settings test, ingest it and inspect the original before applying any LUT. In Resolve bypass all grades and viewing transforms when comparing the source appearance. A flat-looking image is evidence, not a definitive recording-mode identifier. Ten-bit encoding and BT.709 container tags do **not** establish D-Log M: both were present on our known D-Log M and suspected Normal clips. Do not apply the D-Log M LUT to footage known to be Normal.

Optional technical inspection, after setting `clip` to an actual original:

```bash
clip="/absolute/path/to/your/test.MP4"
ffprobe -v error -select_streams v:0 \
  -show_entries stream=width,height,r_frame_rate,pix_fmt,color_primaries,color_transfer \
  -of json "$clip"
exiftool -G1 -s "$clip"
```

The new handheld recording has not been checked merely by following this guide. Keep it until its recording settings are confirmed.

## 3. Record synchronization evidence on rides

Start the bike computer recording. While stationary, film its display and the physical Lap press near the start and end, before stopping the FIT recording. Each camera needs its own identifiable events. Keep those source clips even if they are cut from the film. A middle event provides an independent drift check. A still photo of a lap screen alone may not identify the exact lap-press instant; record its uncertainty instead of treating it as frame-accurate sync.

For a handheld color test, FIT data is optional: complete the camera-master steps without it. The HDR-with-telemetry builder requires a real sync JSON; do not reuse another ride's calibration.

## 4. Ingest the card

Skip ingest if these files and their ingest manifest are already on WHISK.

```bash
uv run kestreel ingest "$card" \
  --device Astra --source-kind card --purpose production --no-proxies --dry-run

uv run kestreel ingest "$card" \
  --device Astra --source-kind card --purpose production --no-proxies
```

Copy the **manifest path printed by this run** into `ingest` below. Do not reuse a previous ride's ingest ID by habit.

```bash
ingest="$WHISK/Movies/originals/manifests/REPLACE_WITH_INGEST_ID/manifest.json"
uv run kestreel verify "$ingest"
```

Verification reads and hashes the listed files; large rides take time. New manifests use paths relative to the manifest's directory. Move the Movies folder structure together between machines. Do not blindly copy an ingest manifest into a project: its relative root must be recalculated, as below.

## 5. Initialize the retrim project and select the recording date

```bash
if [[ ! -f "$project/project.json" ]]; then
  uv run kestreel project init "$prep_name"
fi
manifest="$project/manifests/astra-ingest.json"
```

The card may contain several rides. This creates a project selection with a portable originals root while preserving the canonical ingest manifest. It selects the date across all formats; frame rates and dimensions will be read from the footage later.

```bash
uv run python - "$ingest" "$manifest" "$capture_date" <<'PY'
import json
import sys
from pathlib import Path
from kestreel.manifest_paths import originals_root, portable_ingest

source, target = map(Path, sys.argv[1:3])
day = sys.argv[3]
if not source.is_file():
    sys.exit(f"Ingest manifest not found: {source}")
data = json.loads(source.read_text(encoding="utf-8"))
root = originals_root(source, data)
data["files"] = [r for r in data["files"]
                 if r.get("capture_time", "").startswith(day + "T")]
clips = [r for r in data["files"] if r["role"] == "original"]
if not clips:
    sys.exit(f"No originals for {day}")
for row in data["files"]:
    media = root / row["destination_path"]
    if not media.is_file() or media.stat().st_size != row["size"]:
        sys.exit(f"Missing file or size mismatch: {media}")
target.parent.mkdir(parents=True, exist_ok=True)
with target.open("x", encoding="utf-8") as stream:
    json.dump(portable_ingest(data, target, root), stream, indent=2)
print(f"Selected {len(clips)} original clips: {target}")
PY

uv run kestreel verify "$manifest"
```

If the selection already exists, reuse and verify it. The script deliberately refuses to overwrite it. The canonical ingest retains undated companion records even when the date selection omits them.

## 6. Create the camera timeline

Open Resolve with local scripting enabled. Preview first:

```bash
uv run kestreel project camera-timelines "$manifest" \
  --name "$prep_name" --working-space dwg \
  --lut "DJI/DJI_Action6_DLogM_to_DWG_Intermediate.cube"
```

For confirmed D-Log M footage, create the project:

```bash
uv run kestreel project camera-timelines "$manifest" \
  --name "$prep_name" --working-space dwg \
  --lut "DJI/DJI_Action6_DLogM_to_DWG_Intermediate.cube" \
  --apply --allow-empty-untitled
```

`--allow-empty-untitled` permits only a checked empty placeholder. An existing project of the requested name is not overwritten. Native capture dimensions and FPS are detected; `--capture-fps 59.94` is an optional **filter**, not a way to set the footage rate. Different capture formats get separate prep timelines. The purchased LUT must be installed locally.

For a raw inspection project, omit `--lut`; its clips have not then been normalized to DWG/I, regardless of the timeline setting. Do not render that as a normalized master without an appropriate input conversion.

Apply Gyroflow **manually**, check moving footage, trim, and grade. Scripted `--gyroflow` remains experimental due to stretched/shaky results. It is intentionally omitted here. Camera preparation uses manual DaVinci YRGB and DWG/Intermediate working/output space, without a display-output transform.

## 7. Export the trimmed camera master and timing sidecars

Activate the finished PREP timeline. Replace its name if the detected format differs. Use a new master version directory for each export.

```bash
master_dir="$project/masters/astra/Astra-Master-v1"

uv run kestreel project camera-delivery "$manifest" \
  --timeline "PREP - astra - 3840x3840 - 59.94" \
  --output "$master_dir"
```

Kestreel prepares native-resolution/rate ProRes 422 HQ with PCM audio and exports FCPXML plus a capture map. Review Deliver, add the job, and **start rendering yourself**. Keep the MOV, `.fcpxmld` and `.capture-map.json` together. Native-rate straight cuts are supported; retimes require separate mapping work. The master is DWG/Intermediate; final HLG conversion belongs in the HDR project.

```bash
master="$master_dir/Astra-Master-v1.mov"
ffprobe -v error \
  -show_entries stream=codec_type,codec_name,profile,width,height,r_frame_rate,pix_fmt,nb_frames:format=duration \
  -of json "$master"
```

Check the frame count against `master_frames` in the capture map. The video color tags alone do not describe the complete DWG/I processing history.

## 8. Add FIT data and clock anchors

Replace the example FIT filename before running:

```bash
fit_name="REPLACE_WITH_RIDE_FILENAME.fit"
fit="$project/telemetry/bike-computers/igpsport-bsc300t/$fit_name"
mkdir -p "$(dirname "$fit")" "$project/sync/astra/igpsport-bsc300t"
cp -n "$HOME/Downloads/$fit_name" "$fit"
uv run kestreel-title --laps "$fit"
sync="$project/sync/astra/igpsport-bsc300t/ride-title.json"
```

Create `$sync` using the measured values described in [Record the two clock anchors](ride-field-to-fusion.md#record-the-two-clock-anchors). It refers to `../../../manifests/astra-ingest.json` and the FIT file relative to its location. Anchors use original filenames, zero-based source frames and FIT lap UTC timestamps. One anchor measures offset; two estimate drift; a third checks the estimate. Sensor delay is not clock drift. Never shift sync to force a remembered speed peak.

## 9. Build the separate HDR project

Only the rendered master is imported. The default creates **Horizontal HLG, 3840×2160**, and **Vertical HLG, 1080×1920**, at the master frame rate, with a timeline DWG/I → Rec.2100 HLG CST. Validate inputs first, without opening or changing Resolve:

```bash
uv run kestreel-hdr "$master" \
  --project "$hdr_name" --sync "$sync" --check
```

Then build it yourself:

```bash
uv run kestreel-hdr "$master" \
  --project "$hdr_name" --sync "$sync"
```

The HDR project name must be new. If Kestreel reports that it already exists, confirm the deletion dialog in Resolve’s Project Manager before retrying, or choose another `--project` name. Closing a project or opening its Delete dialog does not remove it. Expected HDR command errors now print a concise `kestreel-hdr:` message and exit with status 1. Preserve the retrim project for re-exporting the master. Imported overlays can be authored differently on each delivery timeline. After changing cuts, refresh each timeline's readings while retaining its layout:

```bash
uv run kestreel-title --timeline "Horizontal HLG" --sync "$sync"
uv run kestreel-title --timeline "Vertical HLG" --sync "$sync"
```

### Place the approved horizontal speedometer using configured borders

For a horizontal speed-only test, use this instead of the standard build above. The project name must be new:

```bash
uv run kestreel-hdr "$master" \
  --project "$hdr_name" --sync "$sync" \
  --orientation horizontal --speed full-square --position bottom-left
```

`--position` and widget flags select the configured layout engine. Its margins come from `profiles.horizontal.margins` in `applications/resolve/fusion/ride-titles/overlay-layout.json` (currently 64 pixels on all four sides). The complete panel is placed inside those borders; the old saved manual center coordinates are replaced. Full-square speed uses two rows by two columns at the configured cell size (currently 254×254 pixels overall). Its allowed horizontal positions are `bottom-left`, `bottom-right`, `top-left`, `top-right`, `center-left`, and `center-right`. Add `--check` to validate without creating a project.

Explicit `--speed full-square` selects only speed. With no widget flags, the modular configuration's preset may also select the draft power and cadence modules. Use `--speed compact-tall` for the future vertical two-row, one-column design; that design still requires visual approval. Telemetry animation is populated after placement, as before.

For optional modular overlay drafts and their current approval status, see [Modular tile plumbing](ride-field-to-fusion.md#modular-tile-plumbing--2026-11-05). The relevant commands are:

```bash
uv run kestreel-overlay --orientation horizontal --position bottom-left \
  --output /private/tmp/Horizontal-Modules.comp
uv run kestreel-overlay --orientation vertical --position bottom-left \
  --output /private/tmp/Vertical-Modules.comp
```

To opt into those drafts instead of the standard build, use this complete command with a new HDR project name:

```bash
uv run kestreel-hdr "$master" \
  --project "$hdr_name" --sync "$sync" \
  --overlay-config "$DROPBOX/matrix/awara/applications/resolve/fusion/ride-titles/overlay-layout.json" \
  --orientation both
```

Final HDR encoding/upload remains a user-reviewed Resolve delivery step; the project builder does not automatically render it.

## 10. Delete an unwanted test recording

Preview is the default. Camera/date selection includes every recording from that camera on that date across the configured library—not only the selected project's footage. It includes originals, LRF previews and matched DJI companions. The commands below use the same `Example-ride` session variables defined in step 1. Check `capture_date` before running: all Astra recordings on that date are selected, even if you created more than one project that day.

```bash
uv run kestreel delete \
  --project "$prep_name" \
  --camera astra --date "$capture_date" --purge
```

If you also created the HDR project, add `--project "$hdr_name"` to both filesystem-deletion commands below and `--name "$hdr_name"` to the Resolve archive command. Only include projects that actually exist.

If its Resolve library entry still exists, first close that project and open another project or the Project Manager. With Resolve running, export a backup and remove the library entry:

```bash
uv run kestreel project resolve-archive \
  --name "$prep_name" \
  --destination "$WHISK/Movies/deletion-backups/$ride_name-$(date +%Y%m%d-%H%M%S)" \
  --apply
```

Then permanently remove the previewed network files and project directory:

```bash
uv run kestreel delete \
  --project "$prep_name" \
  --camera astra --date "$capture_date" --purge --apply
```

Omit `--purge` to quarantine instead of freeing storage. For project-only removal use `--project NAME --apply`; for originals only use `--camera astra --date YYYY-MM-DD --apply`. Repeat `--project` for additional explicitly selected filesystem projects. Resolve library cleanup is a separate command, as above.

Active ingest manifests lose the removed entries; mixed-date manifests retain other recordings, and empty manifests disappear from the active collection. Journals and original manifest snapshots remain under `.kestreel-trash`. Known references in surviving project JSON files block deletion. This does not scan external Resolve databases or independent proxy caches, and does not delete camera-card copies or accidental local duplicates. Do not ingest/edit/delete the same library concurrently.

## What has been checked

The November 6 development checkout passed 155 tests, including portable-manifest relocation, deletion preview, retained dates, shared-project blocking, quarantine, and rollback on an ordinary manifest-write failure. The LandsEnd deletion preview selected eight videos and their previews/companions, approximately 92.9 GB, with no known surviving-project blockers. That preview did not delete anything. No claim is made here that the new handheld settings recording or all current Fusion drafts have been visually approved.

## Validated checkpoint and next widget milestone — November 6

The user accepted the horizontal speedometer build, animated telemetry, and the six-position test sequence. Pending deletion in Resolve correctly prevents reuse of a project name and now produces a friendly error rather than a traceback. Keep the approved horizontal design as the reference while authoring new modules.

Next steps, in order:

1. Author and approve the power widget, 1 row × 1 column.
2. Author and approve cadence, 1 row × 1 column.
3. **Test horizontal again with speed, power and cadence together:** check panel packing, margins, alignment and readings changing with the recorded FIT data. Confirm refresh preserves the authored design. This is a gate before vertical work.
4. Author speed, 2 rows × 1 column, for vertical use.
5. Set a separate vertical widget zoom/scale for 1080×1920 short-form viewing.
6. Test the complete horizontal and vertical assemblies.
7. Finish Fusion node-layout cleanup as the final housekeeping step.

Draft module definitions already exist; they still need visual authoring and approval. A successful packer test does not approve the design. Keep footage reframing separate from widget scale.
