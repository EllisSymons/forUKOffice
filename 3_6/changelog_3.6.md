---
layout: default
title: Changelog for v3.6
parent: Visual Changelogs
nav_order: 6
---

# Changelog for TUFLOW Plugin v3.6

* TOC
{:toc}

## New Features and Enhancements

### TUFLOW Viewer

##### Curtain Plots Support Vertical Velocity
{: .fs-4 : .fw-700}

Curtain vectors will now have a vertical component if 'W' output is found in results.

##### Support For Changing Result Order
{: .fs-4 : .fw-700}

Added option to shift order of open results via right-click context menu.

##### Remember Previous State for GUI Layout
{: .fs-4 : .fw-700}

'Remember Previous State' layout option.

##### Support For NetCDF Rasters
{: .fs-4 : .fw-700}

NetCDF grids now supported.

##### Support For Flood Modeller Python Exported Results
{: .fs-4 : .fw-700}

Adds Python exported CSV format for flood modeller time series results.

##### Support For ZZN Flood Modeller Results
{: .fs-4 : .fw-700}

Adds ZZN support for flood modeller time series results

### SCS to TUFLOW

##### Support For GIS Polygons
{: .fs-4 : .fw-700}

SCS method calculated from GIS polygons.

### Load Layers From TCF

##### Progress Bar
{: .fs-4 : .fw-700}

Added progress bar

##### Automatic TUFLOW Styling
{: .fs-4 : .fw-700}

Imported layers are automatically given TUFLOW styling

##### Grouping Options
{: .fs-4 : .fw-700}

Option to bring in layers 'grouped' or 'ungrouped'

### Sort / Filter Open Layers

##### Improved Sorting Algorithm
{: .fs-4 : .fw-700}

Improved speed and altered sorting algorithm slightly so that layers with the same name (w/o '_L', '_P', '_R' suffix) will be sorted by geometry in order of points, line, polygon.

### Convert TUFLOW Model GIS Format

##### Restrict Conversion by Scenario
{: .fs-4 : .fw-700}

Provides user with the option to restrict conversion by scenario name.

### Configure TUFLOW Project

##### New Icon
{: .fs-4 : .fw-700}

New icon and added to toolbar.

### TUFLOW Layer Styling

##### Adds Missing Styles
{: .fs-4 : .fw-700}

Added styling for 2d_qnl.

### TUFLOW Utilities

#####
{: .fs-4 : .fw-700}

TUFLOW to GIS will automatically find 2dm if using a post-processed XMDF.

## Bug Fixes

### TUFLOW Viewer

* Cross-section plot lines could become offset if start or end of line was outside the mesh
* Fixes bug for long section plotting of Flood Modeller results that could sometimes produce a python error
* Fixes bug in hiding inactive area on cross-section when M column header isn't defined in GIS file
* Fixes bug with cross-section plot that wouldn't update plot when a result type was deselected
* Fixes bug when loading results from TCF which could produce a python error when ~s~ flag was just before extension .tcf in the name
* Fixes 'load results from TCF' when output path is an absolute path
* Fix bug when loading TUFLOW release 2013 time series results which could produce a python error
* New method for loading results from TCF backported to be compatible with Python versions earlier than 3.9 and QGIS versions earlier than 3.22

### Other

* 1D Integrity Tool - Fixes a bug with the ouput symbol renderer in QGIS 3.26
* TUFLOW Utilities - Fixes bug with TUFLOW to GIS common tool using correct scalar/vector type and loading timesteps from a post-processed XMDF
* TUFLOW Styling - Fixes a bug that would not render TUFLOW style for GPKG layers
* Import Empty - Fixes a bug where open layers with the same name as the imported layer were removed from the workspace
* ReFH2 to TUFLOW - Fixes bug that would cause GUI to hang if 2 different output types (within rainfall or hydrograph) was selected (e.g. Direct Runoff and Total Runoff)
* ReFH2 to TUFLOW - Fixes python error that could occur if the selected GIS layer was removed
* Load From TCF - Fixes bug in new routine that wasn't finding all scenario names
