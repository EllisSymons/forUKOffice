---
layout: default
title: Changelog for v3.3
parent: Visual Changelogs
nav_order: 2
---

# Changelog for TUFLOW Plugin v3.3

* TOC
{:toc}

## New Features and Enhancements

### TUFLOW Viewer

## Bug Fixes

### TUFLOW Viewer

* Orevent scrambling of datasets in plot window due to bug in matplotlib 3.5.1 (packaged with QGIS 3.24.1)
* Colour bar is now always displayed for curtain plot (if legend is on) - previously if there was no data (i.e. section was dry) the colour bar wasn't shown. Mostly affects animations.
* Fixed colour bar label which broke with an update to the matplotlib library
* TUFLOW FV XMDF outputs now will correctly show maximums
* Fixed bug that could cause Python error if _PLOT_ layers were removed from workspace while TUFLOW Viewer was closed
* Fixed bug with icon size setting introduced in v3.2 for QGIS versions < 3.16 that would cause error when trying to load
* Hover over labelling is broken in latest QGIS python/matplotlib version - now fixed
* Fixed bug that could occur when loading from a qgz/qgs

### Other

* ReFH2 Tool - fixed bug that broke ReFH2 GUI from opening in previous release
* Import Empty - TUFLOW empty type list will be properly updated after user uses 'browse' to select a directory
* Insert TUFLOW attributes - TUFLOW empty type list will be properly updated after user uses 'browse' to select a directory
* Configure Project - Displayed paths now show correct operating system slashes
* TUFLOW utilities - Common functions - can now specify an output name without specifying an output directory
* TUFLOW utilities - Common functions - output name in TUFLOW_to_GIS was not working
* 1D Integrity Tool - No longer need a line layer to check for empty geometries in points or cross section layers
* Load From TCF - Will now load layers from 'Create TIN Zpts' command
* Auto Label - Fixed tooltip when mouse hovers over toolicon in plugin toolbar
* SCS Tool - now unloads properly
* TUFLOW Menu under Plugins - now unloads properly
