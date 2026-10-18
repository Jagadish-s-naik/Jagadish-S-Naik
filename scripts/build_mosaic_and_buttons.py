#!/usr/bin/env python3
"""Builds assets/mosaic.svg (dot portrait sampled from a reference image) and social buttons.
Usage: python scripts/build_mosaic_and_buttons.py [path/to/reference.png]
Needs: pip install pillow numpy"""
import os, random, sys
import numpy as np
from PIL import Image

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
SANS = "'Segoe UI', system-ui, -apple-system, Roboto, Helvetica, Arial, sans-serif"
MONO = "'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace"


def mosaic(src):
    a = np.asarray(Image.open(src).convert("RGB")).astype(int)
    ox, oy, px, py, nc, nr = 100.4, 34.9, 8.75, 8.75, 73, 48
    X0, Y0, W, H = 68, 15, 684, 450
    rnd = random.Random(7)
    out = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="{X0} {Y0} {W} {H}" role="img" aria-label="Animated dot-matrix portrait">
<defs><clipPath id="card"><rect x="{X0}" y="{Y0}" width="{W}" height="{H}" rx="22"/></clipPath>
<linearGradient id="sh" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#9ff5e8" stop-opacity=".16"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient></defs>
<rect x="{X0}" y="{Y0}" width="{W}" height="{H}" rx="22" fill="#0a0e13" stroke="#1c2a2e"/>''']
    for c in range(nc):
        cx = ox + c * px
        dots = []
        for r in range(nr):
            cy = oy + r * py
            patch = a[int(cy) - 1:int(cy) + 2, int(cx) - 1:int(cx) + 2].reshape(-1, 3)
            R, G, B = patch.mean(axis=0).astype(int)
            if R + G + B < 40:
                continue
            tw = ""
            if rnd.random() < 0.10:
                tw = (f'<animate attributeName="opacity" values="1;.25;1" dur="{rnd.uniform(2.2,5.5):.1f}s" '
                      f'begin="{rnd.uniform(3,9):.1f}s" repeatCount="indefinite"/>')
            dots.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="2.5" fill="#{R:02x}{G:02x}{B:02x}">{tw}</circle>'
                        if tw else f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="2.5" fill="#{R:02x}{G:02x}{B:02x}"/>')
        out.append(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{c*0.035:.2f}s" dur=".5s" fill="freeze"/>' + "".join(dots) + '</g>')
    out.append(f'<g clip-path="url(#card)"><rect x="{X0-120}" y="{Y0}" width="120" height="{H}" fill="url(#sh)">'
               f'<animate attributeName="x" values="{X0-120};{X0+W}" dur="4.5s" begin="3.5s" repeatCount="indefinite"/></rect></g>')
    out.append(f'<text x="{X0+W-22}" y="{Y0+H-16}" text-anchor="end" font-family="{MONO}" font-size="11" letter-spacing="2" fill="#4f7f79">JAGADISH NAIK</text></svg>')
    with open(os.path.join(OUT, "mosaic.svg"), "w") as f:
        f.write("".join(out))
    print("mosaic.svg", os.path.getsize(os.path.join(OUT, "mosaic.svg")) // 1024, "KB")


ICONS = {
    "linkedin": '<rect x="-11" y="-11" width="22" height="22" rx="5" fill="#fff"/><text y="6" text-anchor="middle" font-family="Arial,sans-serif" font-size="15" font-weight="800" fill="#0A66C2">in</text>',
    "linklee": '<g fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round"><rect x="-13" y="-6" width="15" height="12" rx="6"/><rect x="-2" y="-6" width="15" height="12" rx="6"/></g>',
    "x": '<path d="M-9 -9 L9 9 M9 -9 L-9 9" stroke="#fff" stroke-width="3.2" stroke-linecap="round"/>',
    "github": '<circle r="11" fill="#fff"/><text y="5" text-anchor="middle" font-family="Arial,sans-serif" font-size="13" font-weight="800" fill="#161b22">GH</text>',
    "email": '<rect x="-12" y="-8" width="24" height="16" rx="3" fill="none" stroke="#fff" stroke-width="2.4"/><path d="M-11 -6 L0 3 L11 -6" fill="none" stroke="#fff" stroke-width="2.4" stroke-linejoin="round"/>',
}
BUTTONS = [("linkedin", "LinkedIn", "#0A66C2", 160), ("linklee", "Linklee", "#0d9488", 146),
           ("x", "X / Twitter", "#111827", 166), ("github", "GitHub", "#24292f", 144), ("email", "Email", "#c2410c", 130)]


def buttons():
    for key, label, col, w in BUTTONS:
        h = 46
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{label}">
<defs><clipPath id="c"><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="23"/></clipPath>
<linearGradient id="s" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".35"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient></defs>
<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="23" fill="{col}"/>
<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="23" fill="none" stroke="#5eead4" stroke-opacity=".7"><animate attributeName="stroke-opacity" values=".25;.9;.25" dur="3s" repeatCount="indefinite"/></rect>
<g clip-path="url(#c)"><rect y="0" width="40" height="{h}" fill="url(#s)"><animate attributeName="x" values="-50;{w+10}" dur="3.2s" repeatCount="indefinite"/></rect></g>
<g transform="translate(30 23)">{ICONS[key]}</g>
<text x="{30+26}" y="28" font-family="{SANS}" font-size="15" font-weight="700" fill="#fff">{label}</text></svg>'''
        with open(os.path.join(OUT, f"btn-{key}.svg"), "w") as f:
            f.write(svg)
    print("buttons ok")


if __name__ == "__main__":
    buttons()
    if len(sys.argv) > 1:
        mosaic(sys.argv[1])
