# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

`burntotile` is a single-page tool that lets users drag-and-drop GeoJSON onto a full-screen slippy map and get back a list of quadkeys (at a chosen zoom) that cover the geometry.

## Development

`index.html` runs directly with no build step:

```bash
python3 -m http.server   # open http://localhost:8000
```

The `Makefile` adds an optional build that inlines MapLibre JS + CSS so the output is a fully self-contained single file:

```bash
make build    # → dist/index.html  (MapLibre CSS+JS inlined via build.py)
make serve    # build + serve dist/ at :8000
make deploy   # build + force-push dist/index.html to the gh-pages branch
make clean    # rm -rf dist/
```

`dist/` is gitignored. `build.py` uses `curl` to fetch CDN assets and substitutes `<link stylesheet>` / `<script src>` tags with inline equivalents.

Deploy options:
- **GitHub Actions** (default): push to `main` triggers `.github/workflows/deploy.yml`, deploys from main. Ensure Pages source is set to **GitHub Actions**.
- **Manual gh-pages branch**: run `make deploy`, then set Pages source to the **gh-pages branch**.

## Architecture

Everything lives in `index.html`. The `<script>` block has distinct logical sections:

- **Map setup** — MapLibre GL v4. Basemap uses CARTO Light raster tiles (`basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png`) — free, no API key, wildcard CORS. Glyphs for the quadkey labels come from `protomaps.github.io/basemaps-assets/fonts`.
- **Quadkey grid overlay** — GeoJSON source (`qk-grid`) rebuilt on every `moveend`. Grid zoom is calculated so ~4 quadkeys span the viewport width at any zoom: `Z = round(log2(1440 / viewportWidthDegrees))`, clamped 1–28.
- **Left panel** — drag-and-drop / click-to-pick GeoJSON; zoom dropdown (2–28); clear button; output textarea (click-to-copy).
- **Burn logic** — `burnGeoJSON(geojson, z)` converts any GeoJSON geometry type to a deduplicated, sorted array of quadkey strings at zoom `z`. FeatureCollection processes all features. Polygon coverage uses `ringIntersectsTile` (vertex-in-bbox + corner-in-ring + edge-crossing). LineString coverage uses Bresenham's line traversal with recursive subdivision for long segments. Points map directly to a single tile. 500k-tile guard prevents runaway burns.
- **Error modal** — centered red/white overlay for validation and burn errors.

## Key CDN dependencies

| Library | CDN |
|---|---|
| MapLibre GL v4 | `https://unpkg.com/maplibre-gl@4/dist/maplibre-gl.{js,css}` |
| Basemap tiles | `https://{a,b,c}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png` (free, no key) |
| Glyphs | `https://protomaps.github.io/basemaps-assets/fonts/{fontstack}/{range}.pbf` |
