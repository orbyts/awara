> Migrated lab reference. Use the current [manual setup](../getting-started/manual-setup.md) and recipe JSON for current configuration. Historical results below apply only to the tested samples. UI illustrations are being reviewed for a public edition.

# DJI Osmo Action 6 input

Edition 0.2 | 2026-10-30

Working edition based on the guided lab; visual acceptance is not independent colorimetric validation.

## Action 6: a dedicated
DWG input LUT

Original D-Log M -> purchased camera-specific transform

Use <b>DJI/DJI_Action6_DLogM_to_DWG_Intermediate.cube</b>. The purchased header explicitly names DaVinci Wide Gamut / DaVinci Intermediate output. Cataloged version: 1.0, dated 2026-03-31; 65-point 3D LUT.

1. Keep the original D-Log M camera clip. Confirm its recording profile from camera/ingest records; do not infer it from the BT.709 container tags.
2. Open Project Settings > Color Management > Open LUT Folder. Copy the purchased DWG .cube there and choose Update Lists.
3. Use manual DaVinci YRGB and DWG/I timeline working space. Set 3D LUT interpolation to Tetrahedral.
4. On a simple clip graph, put this LUT on the first node, labeled Input - Action6 to DWG/I. Put the grade after it, then one DWG/I-to-delivery output CST.
5. For many matching Action 6 clips, move the input LUT to their Group Pre-Clip graph instead. Do not leave it on both the group and each clip.

> Do not use the Rec709 or ARRI709 variants for this DWG input step. Do not combine the DJI Rec.709 display LUT with the DWG input LUT. This Action 6 purchase does not establish compatibility with Osmo 360.

- [Gamut: Action 6 BaseLUTs purchase page](https://gamut.io/product/baseluts-for-dji-osmo-action-6/)

## Levels, provenance
and limits

Camera-specific evidence; UI screenshots for this card remain to capture

The two inspected Action 6 samples are 10-bit HEVC, 3840 x 3840 at 59.94 fps, flagged video range. Keep Video levels, or Auto only when it interprets them correctly. Forcing Full does not recover dynamic range and can shift the picture.

| Record | Value |
| --- | --- |
| LUT role | Camera D-Log M to DWG/I input normalization |
| Visual validation | User reports a successful result |
| Independent color measurement | Not performed |
| SHA-256 prefix | 3f5cf2dc3b6611614508ff79ec1a0984c |
| Full asset identity | See the private validation archive in the private repository |

### Existing experimental copies

Earlier Freeman Action 5-derived ProRes comparison copies are already transformed and are experimental. Do not apply this input LUT to them. For the selected workflow, use the original camera file plus the Action 6 LUT.

### Before mixing cameras

Normalize each camera appropriately, then balance exposure and white balance in DWG/I. A common working space does not automatically match sensor response, exposure, white balance or lens rendering.

### Publishing this guide

The guide can link to Gamut. The purchased LUT itself is not part of a distributable guide, public sample project or product for resale. Screenshots of the Action 6 installation and group assignment will be added during the multicamera pass.

> Source evidence: private the private validation archive, the purchased file header, and the two local footage probes. This card records an accepted practical workflow, not an independently calibrated input transform.

- [Gamut: Action 6 BaseLUTs purchase page](https://gamut.io/product/baseluts-for-dji-osmo-action-6/)
