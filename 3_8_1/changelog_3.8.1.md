---
layout: default
title: Changelog for v3.8.1
parent: Visual Changelogs
nav_order: 8
---

# Changelog for TUFLOW Plugin v3.8.1

* TOC
{:toc}

## Bug Fixes

### TUFLOW Viewer

* A rogue import statement was causing the plugin to not load
* Fixes bug that would not correctly update newly selected result in open result widget
* Fixes bug when importing results from TCF when some input layers are using absolute path references that could cause a python error
* No longer prompt user about saving default styles - could prompt (many times) when saving a project

### Other

* TUFLOW Toolbox - tmo_to_points wasn't being loaded
* Utilities - Fixes issue when running 'info' function and non-ascii characters are logged which may cause the tool to error
