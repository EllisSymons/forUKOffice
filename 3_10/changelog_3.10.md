---
layout: default
title: Changelog for v3.10
parent: Visual Changelogs
nav_order: 3
---


# Changelog for TUFLOW Plugin v3.10

* TOC
{:toc}

<!--
<video style="max-width:640px" controls>
  <source src="videos/test.mp4" type="video/mp4">
</video>
-->

## New Features and Enhancements

### TUFLOW Viewer

### Import Empty

### TUFLOW Context Menu

### Processing Toolbox

## Bug Fixes

### TUFLOW Viewer

* Fixes bug where Flood Modeller cross-sections weren't plotting due to the change in inactive area handling in TUFLOW Plugin v3.9
* Fixes bug when loading a cross-section that starts with a valid float number in the header
* Fixes python error that prevented TUFLOW Viewer from loading when there was a 1d_xs
* Fixes hover over plot labelling for matplotlib 3.7
* fixes a bug that stopped loading tpc result when a '#' was present in the flow regime result
* Removes duplicate result types from 2d_bc_tables
* Static NetCDF grid results no longer affect the time slider
* Optimised code relating to feature selection when viewing time series results
* Long profile results are not shown if only 2D results are available (Time Series results)

### Other

* Import Empty (Toobox) - Fixes bug that could potentially not correctly bring in new GPKG layer if GPKG contained more than one layer
* Import Empty (Toolbox) - Removes duplicate empty types from list
* Apply GPKG Name - Fixes bug where name wasn't applied to raster layers where the database only containes one raster layer
* Increment Layer - Fixes bug that would cause python error if a layer group was selected
* Convert TUFLOW Model GIS Format - Fixes bug on tool initialisation when using network drivers (caused python error)
* Load from TCF - Fixes python error that would occur if an xf layer was being referenced
* 1D Integrity Tool - Vector layer input comboxes will no longer reset if a layer is added/removed from workspace
* 1D Integrity Tool - Error is shown to user if selected channels are not connected when using the flow trace tool. Previously this would error silently and progress bar looked to hang.
* 1D Integrity Tool - Remembers selected DEM which could reset if layers were added/removed from workspace
* 1D Integrity Tool - Fixes python error that could occur if an aerial image was accidentally used as ground surface
* Run TUFLOW - Fixes bug that can cause Python error when browsing for TUFLOW.exe
* Copy TUFLOW Command - A little more clever when searching for control files in case it finds an erroneous 'TUFLOW' folder
