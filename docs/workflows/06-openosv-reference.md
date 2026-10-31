> Migrated lab reference. Use the current [manual setup](../getting-started/manual-setup.md) and recipe JSON for current configuration. Historical results below apply only to the tested samples. UI illustrations are being reviewed for a public edition.

# OpenOSV reference experiment

Edition 0.2 | 2026-10-30

Working edition based on the guided lab; visual acceptance is not independent colorimetric validation.

## An alternative
we tested

Excluded from the selected main workflow

OpenOSV decoded, stitched, stabilized and reframed the OSV inside Resolve using an OpenOSV Source generator. The tested build was 0.6.4 at commit d46b2bc9803f90779ac319fdad81d358efb68a2e.



For the SDR comparison, OpenOSV Rec.709 output with the DJI look was compared to DJI Studio Color Recovery. The user accepted a near-identical visual match after disabling DJI Studio Dewarp; a small orientation discrepancy remained tolerable.

DJI Studio needed the imported clip placed on its timeline and selected before Adjust appeared. Color Recovery used D-Log M (Recommended), intensity 100, other grading controls neutral. This was a display-rendering comparison, not an input-transform calibration.

> Why not the main route: the guided workflow needed a practical Osmo 360 DWG/I input stage. Spatial Film supplies that option and was selected. This does not establish that OpenOSV is unusable; the experimental adapter was simply not approved for the main guide.

- [OpenOSV repository](https://github.com/Kemerd/OpenOSV)

## Preserve the
reference, not the dependency

Installation, comparison limits and recovery notes



This test used a launcher that sets OFX_PLUGIN_PATH to the user-local OpenOSV bundle. Opening Resolve normally produced the missing org.openosv.osvsource message. The launcher restored it. Spatial Film is installed in the system OFX directory and does not depend on that launcher.

Keep the accepted SDR project snapshot and DJI reference exports. Do not apply the Action 6 LUT to Osmo 360. The existing OpenOSV-derived experimental LUT/DCTL remains labeled experimental and is not part of the approved Spatial Film path.

The DJI Studio reference export is 30 fps while the source is 29.97 fps. First-frame comparisons were useful; frame-for-frame motion equivalence over the entire duration was not established. A display-LUT match alone says nothing definitive about HDR scene accuracy.

> Historical docs/openosv-hdr-walkthrough.md and docs/openosv-comparison.md describe an earlier experiment. Use this guide as the entry point to that history, not as setup instructions for the main HDR project.

- [Pinned OpenOSV source](https://github.com/Kemerd/OpenOSV/tree/d46b2bc9803f90779ac319fdad81d358efb68a2e)
