# Changelog for TUFLOW Plugin v3.9

* TOC
{:toc}

## New Features and Enhancements

### TUFLOW Viewer

#### Viewing Support for 2d_bc_tables_check.csv

TUFLOW Viewer now support loading and viewing the2d_bc_tables_check.csv file.

<video style="max-width:640px" controls>
  <source src="videos/test.mp4" type="video/mp4">
</video>

#### User Defined Time Formatting in Animation Export

The animation export now supports user defined time formatting.

#### Flood Modeller Result Shown on Cross-Sections With the Same Name

Flood modeller results can now be shown on cross-section even if they don't intersect the PLOT_P points if they have the same name.

### ReFH2 to TUFLOW

#### Support for FEH2022 Rainfall

Rainfall model FEH2022 now supported in tool.

### TUFLOW Plugin Downloader

#### Copy Download Path to Clipboard

Adds button to copy the download path to the clipboard.

### Import Empty

#### Missing Empty Types Added for Tooltips

Adds new/missing empty types to the empty tooltips (2d_bg, 1d_bg, 1d_lc)

### TUFLOW Context Menu - Layers Panel

Adds TUFLOW context menu when a layer is right-clicked in the Layers Panel

#### Increment Layer (Layer Context Menu)

New tool in layer context menu (new tools but similar to existing import empty tool).

#### Filter Messages by ID

Adds Filter Message by ID to TUFLOW context menu for messages_P layers.

#### Copy TUFLOW Command

Adds 'Copy TUFLOW Command' tool to TUFLOW context menu.

### TUFLOW Utilities

#### GPKG Raster Support

GPKG rasters now supported when adding opened layers

### Load Layers From TCF

#### Support for Old Auto Estry Command

Older style 'ESTRY CONTROL FILE AUTO' syntax now supported.

### Apply GPKG Layer Names

#### Support for GPKG Rasters

GPKG rasters now supported.

### TUFLOW Layer Styling

#### Support ccA_L Result File

_ccA_L result file now has default styling

### ARR to TUFLOW

#### Support for LIMB Data

LIMB data will now be processed if available

#### Remove Longitude Limit

Removes longitude limit (>153.2999)

### Increment Layer

#### User Check Before Overwriting Existing Layers

Adds user check when overwriting an existing layer in a GPKG.

### Processing Toolbox

#### Import Empty (Processing Toolbox)

New tool in TUFLOW processing toolbox (very similar to existing import empty).

#### Create Project (Processing Toolbox)

New tool in TUFLOW processing toolbox (very similar to configure project).

