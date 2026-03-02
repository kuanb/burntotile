# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

`burntotile` is a single-page tool that lets users drag-and-drop GeoJSON onto a full-screen slippy map and get back a list of quadkeys (at a chosen zoom) that cover the geometry.

## Development

No build step — the project is a single `index.html`. Run locally with:

```bash
python -m http.server
```

Deploy to GitHub Pages via the gh-pages branch (GitHub Actions workflow in `.github/workflows/deploy.yml`).

## Architecture

Everything lives in `index.html`. The file is structured as one `<script type="module">` block with distinct logical sections:

- **Map setup** — MapLibre GL v4 with PMTiles protocol; Overture Maps Foundation tiles (2025-12-17 release) as three sources: `ov-base`, `ov-transport`, `ov-buildings`.
- **Quadkey grid overlay** — GeoJSON source (`qk-grid`) rebuilt on every `moveend`. Grid zoom is calculated so ~4 quadkeys span the viewport width at any zoom: `Z = round(log2(1440 / viewportWidthDegrees))`, clamped 1–28.
- **Left panel** — drag-and-drop / click-to-pick GeoJSON; zoom dropdown (2–28); clear button; output textarea (click-to-copy).
- **Burn logic** — `burnGeoJSON(geojson, z)` converts any GeoJSON geometry type to a deduplicated array of quadkey strings at zoom `z`. FeatureCollection processes all features. Tile coverage uses a recursive tile-split approach.
- **Error modal** — centered red/white overlay for validation and burn errors.

## Key CDN dependencies

| Library | CDN |
|---|---|
| MapLibre GL v4 | `https://unpkg.com/maplibre-gl@4/dist/maplibre-gl.{js,css}` |
| PMTiles v3 | `https://unpkg.com/pmtiles@3/dist/pmtiles.js` (ES module) |

## Overture tile layer names (source-layer values)

| Source | Layer name |
|---|---|
| `ov-base` | `land`, `land_use`, `land_cover`, `water`, `infrastructure` |
| `ov-transport` | `segment` (roads), `connector` (intersections) |
| `ov-buildings` | `buildings` |
