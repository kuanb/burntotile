# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

`burntotile` is a single-page tool that lets users drag-and-drop GeoJSON onto a full-screen slippy map and get back a list of quadkeys (at a chosen zoom) that cover the geometry.

## Development

No build step — the project is a single `index.html`. Run locally with:

```bash
python -m http.server
```

Deploy to GitHub Pages via `.github/workflows/deploy.yml` (push to `main` triggers it). Ensure the repo's Pages setting uses **GitHub Actions** as the source.

## Architecture

Everything lives in `index.html`. The file is structured as one `<script type="module">` block with distinct logical sections:

- **Map setup** — MapLibre GL v4 (no PMTiles, no build step). Basemap uses CARTO Light raster tiles (`basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png`) — free, no API key, wildcard CORS. Glyphs for the quadkey labels come from `protomaps.github.io/basemaps-assets/fonts`.
- **Quadkey grid overlay** — GeoJSON source (`qk-grid`) rebuilt on every `moveend`. Grid zoom is calculated so ~4 quadkeys span the viewport width at any zoom: `Z = round(log2(1440 / viewportWidthDegrees))`, clamped 1–28.
- **Left panel** — drag-and-drop / click-to-pick GeoJSON; zoom dropdown (2–28); clear button; output textarea (click-to-copy).
- **Burn logic** — `burnGeoJSON(geojson, z)` converts any GeoJSON geometry type to a deduplicated, sorted array of quadkey strings at zoom `z`. FeatureCollection processes all features. Polygon coverage uses `ringIntersectsTile` (vertex-in-bbox + corner-in-ring + edge-crossing). LineString coverage uses Bresenham's line traversal with recursive subdivision for long segments. Points map directly to a single tile. 500k-tile guard prevents runaway burns.
- **Error modal** — centered red/white overlay for validation and burn errors.

## Key CDN dependencies

| Library | CDN |
|---|---|
| MapLibre GL v4 | `https://unpkg.com/maplibre-gl@4/dist/maplibre-gl.{js,css}` |
| MapLibre GL v4 | `https://unpkg.com/maplibre-gl@4/dist/maplibre-gl.{js,css}` |
| Basemap tiles | `https://{a,b,c}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png` (free, no key) |
| Glyphs | `https://protomaps.github.io/basemaps-assets/fonts/{fontstack}/{range}.pbf` |
