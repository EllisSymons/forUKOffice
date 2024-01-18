---
layout: default
title: Changelog for v3.8.2
parent: Visual Changelogs
nav_order: 3
---

# Changelog for TUFLOW Plugin v3.8.2

* TOC
{:toc}

<!--
<video style="max-width:640px" controls>
  <source src="assets/test.mp4" type="video/mp4">
</video>
-->

## New Features and Enhancements

### TUFLOW Viewer

## Bug Fixes

### TUFLOW Viewer

* Fixes bug that could cause strange plotting behaviour when 1D/2D results were both loaded and the reference time was changed for the 2D results 
* Fixes an issue where TUFLOW Viewer was not always picking up 1d_xs layers from GPKG
* Fixes bug that would sometimes not show all available groundwater PO outputs
* Fixes bug that could cause python error when trying to close a result just after TUFLOW is started overrided the same result layer

### Other

* Load from TCF - Fixes bug that could cause a load error if the output folder was a Windows path variable
* Load From TCF - MIF layers with 2 geometry types will now correctly load in line types which could sometimes not load in correctly
* ReFH2 to TUFLOW - Fixes tool not initialising correctly when plugin is loaded which was causing 'unexpected' error when the tool was opened by user
* Arch Bridge Editor - fixes bug that would not recognise GPKG input layers as 1d_nwk
* 1D Integrity Tool - fixes python error that could occur if no points where included when running the snapping tool
* 1D Integrity Tool - Fixes bug that could cause python error due to non-unique indexing internally
* Increment Layer - Fixes a bug that would lead to strange autofilled increment names (or python errors) when the source layer name was using letters along side version number e.g. '002b'
* Configure Project - Updates to latest vector file creation functions in QGIS. Projection.shp causes error in QGIS 3.30
