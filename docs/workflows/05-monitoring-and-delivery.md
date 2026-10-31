> Migrated lab reference. Use the current [manual setup](../getting-started/manual-setup.md) and recipe JSON for current configuration. Historical results below apply only to the tested samples. UI illustrations are being reviewed for a public edition.

# HDR monitoring and delivery

Edition 0.2 | 2026-10-30

Working edition based on the guided lab; visual acceptance is not independent colorimetric validation.

## Declare the
working and output spaces

Manual YRGB project settings | Tested PQ branch



| Setting | Tested value |
| --- | --- |
| Color science | DaVinci YRGB |
| Timeline color space | DaVinci WG/Intermediate |
| Output color space | Rec.2100 ST2084 (not Scene) |
| HDR mastering is for | 1000 nits |
| Project input/output/monitor LUTs | None |

Manual YRGB does not automatically normalize the camera or create the output transform. The plugin/LUT and CST perform those pixel conversions. Keep the output declaration consistent with the actual final node.

> PQ can encode luminance up to 10,000 nits. Our chosen mastering/output target is 1,000 nits. The mastering checkbox is not a brightness multiplier or a substitute for a tone map, and it does not prove that an exported file contains all HDR10 metadata.

- [Dolby: output declaration in manual DaVinci YRGB](https://professionalsupport.dolby.com/s/article/Best-Practices-Resolve-output-color-space-setting-using-Color-science-DaVinci-YRGBBest-Practices-Resolve-output-color-space-setting-using-Color-science-DaVinci-YRGB)

## Configure the
PQ output CST

Actual captured settings; preserve this baseline before changing it



Input: DaVinci Wide Gamut / DaVinci Intermediate. Output: Rec.2020 / ST2084. Tone Mapping: DaVinci. Custom Max Input off; Custom Max Output on, 1000 nits; Adaptation 9.00. HDR Standard Conversions and HDR 203 Nits Diffuse White on. White Point Adaptation on.

> Gamut Mapping was None in this test. That is a recorded setting, not a guarantee that every saturated color stays inside the destination gamut. Review gamut excursions and highlight behavior before a production preset is approved.

## View the actual
HDR output

Resolve GUI viewer on Apple Pro Display XDR





The user also confirmed True Tone was disabled and visually compared QuickTime with Resolve on this display. Keep the viewing conditions consistent; avoid automatic appearance/brightness changes during evaluation.

The P3 display preset describes the monitor. The delivered pixels remain Rec.2020/PQ. Do not switch export primaries to P3 just because the physical monitor uses P3. The monitor cannot validate all colors outside its gamut.

> The Rec.709 Scene QuickTime-match option was enabled in the screenshot; it is not the PQ conversion switch. Screenshots may be SDR representations of the UI and cannot establish HDR luminance accuracy.

- [Apple: display reference modes](https://support.apple.com/en-nz/108321)

## Render and
inspect the file

Short PQ test recipe | One final encode from source

| Control | Requested test setting |
| --- | --- |
| Render / Format / Codec | Single clip / QuickTime / H.265 |
| Profile / Raster / FPS | Main10 / 3840 x 2160 / 29.97 |
| Quality | Restrict to 80,000 Kb/s; Optimize for speed off |
| Data levels / Pixel aspect | Video / Square |
| Color space tag / Gamma tag | Rec.2020 / ST2084 |
| Use optimized / proxy / cached media | Off for the verification render |
| Bypass re-encode when possible | Off for this test |



Set the filename and project masters destination. Select Entire Timeline, Add to Render Queue, then Render All. The source clip here is 149 frames, approximately five seconds. Use separate filenames for the static and animated tests.

> The 80 Mb/s setting is a requested limit, not an expected measured average. The static file averaged about 29 Mb/s for video. Its decoded output has video levels, BT.2020 primaries/non-constant matrix, and SMPTE ST2084 transfer.

## Close the test;
finish delivery separately

Verified result and the remaining PQ/HLG work

| Test | Result |
| --- | --- |
| Static PQ file | Main10 / yuv420p10le / 3840 x 2160 / 30000:1001 / 149 frames |
| Decode and playback | All static frames decode; user confirms QuickTime matches Resolve |
| Animated file | User confirms 0 -> 180 degree pan; HEVC/PQ tags and full decode also checked |
| Audio in static test | 48 kHz stereo 24-bit PCM |
| HDR10 static metadata | Not detected in the initial stream/first-frame probe; not certified complete |

### PQ / YouTube next

YouTube specifies Rec.2020 primaries, non-constant matrix and PQ or HLG, with 10/12-bit video. For PQ, it also asks for mastering-display information. Finish the export metadata recipe, inspect the bitstream, and verify HDR processing after a test upload. Do not invent MaxCLL/MaxFALL measurements.

### HLG / Instagram next

Build a separate output branch from the DWG/I grade using an HLG output transform, not merely different tags on the PQ file. Validate display rendering, tone mapping, metadata and the actual upload/device path. HLG is the intended Instagram delivery, not yet a verified platform preset.

> This edition documents a successful local PQ workflow. It does not yet claim complete HDR10 mastering metadata or validated platform delivery. Camera accuracy and display calibration remain separate from encoding checks.

- [YouTube: HDR upload requirements](https://support.google.com/youtube/answer/7126552?hl=en)
