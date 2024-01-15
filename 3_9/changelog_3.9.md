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

## Bug Fixes

### TUFLOW Viewer

* Time series results are now loaded correctly using 'utf-8' encoding which enables handling of special characters
* Loading NetCDF Grids will now try and load all selected layers before reporting errors
* Results with only maximums will now appear in relevant plot menus
* Fixes loading netCDF raster as mesh
* XS deactivation was only working when using the MAT approach
* Loading mesh layers on when TUFLOW Viewer is opened was getting tangled if layers of different types (vector layers / mesh layers) had the same name
* Fixes flood modeller result cross-sections not loading when X,Y coordinate did not contain a space between them in DAT file
* Fixes animations with embedded plots not working in QGIS 3.30
* Fixes bug introduced in 3.8.2 that prevented NetCDF grid results from being loaded (produced python error about missing 'events' argument)

### Other

* TUFLOW Utilities - Fixes bug in asc_to_asc brkline tool where the vector layer was being passed into the utility instead of the raster layer
* TUFLOW Utilities - Fixes bug where no 'browse' buttons were working
* TUFLOW Utilities - Downloader was hanging indefinitely due to a python error on a separate thread in QGIS 3.32 (caused by new numpy version)
* Configure Project - Fixes bug that would not correctly save empty file location for TUFLOW FV
* TUFLOW Styling - Fixes default styling for sac_check_R
* TUFLOW Styling - ISIS 1d_nwk layers are now given a single styling previously would cause python error because they are not guaranteed to have the standard 1d_nwk fields
* Convert Model GIS Format - Fixes bug that cause new filepaths to be incorrect when convert filename that were only a number (e.g. 001.tgc)
* Load from TCF - fixes bug that would not load layers if brackets were included in file path
* Load from TCF - fixes issue that would cause a python error if there was a '|' at the end of a GIS input command
