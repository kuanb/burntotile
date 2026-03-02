#!/usr/bin/env python3
"""
Inline CDN <link stylesheet> and <script src> tags into a self-contained HTML file.

Usage:
    python3 build.py [src=index.html] [dst=dist/index.html]

Runtime tile/glyph URLs (CARTO, Protomaps fonts) are left as-is; only
build-time library assets (MapLibre GL JS + CSS) are inlined.
"""

import re
import subprocess
import sys


def fetch(url: str) -> str:
    print(f"  fetch {url}")
    result = subprocess.run(
        ["curl", "-fsSL", "--max-time", "30", url],
        capture_output=True, text=True, check=True,
    )
    return result.stdout


def build(src: str = "index.html", dst: str = "dist/index.html") -> None:
    html = open(src, encoding="utf-8").read()

    # <link ... href="https://...css"> → <style>...</style>
    def inline_css(m: re.Match) -> str:
        return f"<style>\n{fetch(m.group(1))}\n</style>"

    html = re.sub(
        r'<link[^>]+href="(https://[^"]+\.css)"[^>]*>',
        inline_css,
        html,
    )

    # <script src="https://..."></script> → <script>...</script>
    # (only bare src= tags, not type="module" blocks)
    def inline_js(m: re.Match) -> str:
        return f"<script>\n{fetch(m.group(1))}\n</script>"

    html = re.sub(
        r'<script\s+src="(https://[^"]+)"[^>]*></script>',
        inline_js,
        html,
    )

    with open(dst, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"wrote {dst} ({len(html):,} bytes)")


if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "index.html"
    dst = sys.argv[2] if len(sys.argv) > 2 else "dist/index.html"
    build(src, dst)
