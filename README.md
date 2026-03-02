# burntotile

A single-page tool for burning GeoJSON geometries into quadkeys.

## What it does

- Displays a full-screen slippy map (MapLibre GL + Overture Maps Foundation tiles via PMTiles)
- Overlays a dynamic quadkey grid that always shows ~4 quadkeys across the screen width, updating as you pan and zoom
- Accepts a GeoJSON file via drag-and-drop or file picker
- "Burns" the geometry into all quadkeys at a chosen zoom level (Z2–Z28), supporting Points, LineStrings, Polygons, MultiX variants, GeometryCollections, and FeatureCollections
- Displays the resulting quadkey list; click the box to copy all to clipboard

## Live site

Deployed to GitHub Pages at `https://<your-github-username>.github.io/burntotile/`

## Running locally

No build step required — it's a single `index.html`.

```bash
python -m http.server
# open http://localhost:8000
```

## Deployment

Pushing to `main` triggers the GitHub Actions workflow (`.github/workflows/deploy.yml`) which deploys to GitHub Pages automatically. Make sure GitHub Pages is configured to use **GitHub Actions** as the source in your repo settings.

## Tech stack

| Layer | Library |
|---|---|
| Map renderer | [MapLibre GL JS v4](https://maplibre.org/) |
| Tile format | [PMTiles v3](https://docs.protomaps.com/pmtiles/) |
| Basemap data | [Protomaps](https://protomaps.com/) public demo tiles (OpenStreetMap) |
| Basemap style | [protomaps-themes-base](https://github.com/protomaps/basemaps) "light" theme |
| Fonts/glyphs | [Protomaps basemaps-assets](https://github.com/protomaps/basemaps-assets) |

No bundler, no npm — all dependencies loaded from CDN.
