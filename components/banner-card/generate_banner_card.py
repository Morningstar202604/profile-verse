#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Banner Card — Profile Verse component
-------------------------------------
A wide hero banner for the top of your profile: your name glowing in gold over
a starfield, with a comet trail crossing the sky. Signature look: glowing name
+ comet trail. No API needed — pure visual.

Env: USER (default Morningstar202604) · TEXT (subtitle, default below) ·
     OUTPUT (default banner-card.svg) · THEME (dark|light)

Part of Profile Verse: https://github.com/Morningstar202604/profile-verse
"""

import os
import random
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, _ROOT)

from core import theme as th  # noqa: E402

OUTPUT = os.environ.get("OUTPUT", "banner-card.svg")
USER = os.environ.get("USER", "Morningstar202604")
TEXT = os.environ.get("TEXT", "Code under the stars, ship with the dawn")
THEME = os.environ.get("THEME", "dark")

W, H = 960, 240


def stars(pal, n=120, seed=11):
    rnd = random.Random(seed)
    out = []
    for _ in range(n):
        x = rnd.uniform(8, W - 8)
        y = rnd.uniform(8, H - 8)
        r = rnd.choice([0.7, 1.0, 1.3, 1.7])
        op = rnd.uniform(0.12, 0.5)
        out.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" opacity="%.2f"/>' % (x, y, r, pal["star"], op))
    return "".join(out)


def comet(pal):
    """A comet trail arcing across the banner."""
    return (
        '<path d="M -60 208 Q 300 26 640 118 T 1030 52" fill="none" stroke="%s" stroke-width="1.6" stroke-opacity="0.55" stroke-dasharray="1 9" stroke-linecap="round"/>'
        '<path d="M 640 118 Q 700 132 762 108" fill="none" stroke="%s" stroke-width="2.2" stroke-opacity="0.8" stroke-linecap="round"/>'
        '<circle cx="762" cy="108" r="3.2" fill="%s"/>'
        '<circle cx="762" cy="108" r="8" fill="%s" opacity="0.25"/>'
        % (pal["gold"], pal["gold_bright"], pal["gold_bright"], pal["gold_bright"])
    )


def main():
    pal = th.palette(THEME)
    try:
        name = USER if len(USER) <= 24 else USER[:23] + "\u2026"
        svg = (
            '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" role="img" aria-label="%s">'
            '<defs>'
            '<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>'
            '<radialGradient id="glow" cx="0.5" cy="0.5" r="0.6">'
            '<stop offset="0" stop-color="%s" stop-opacity="0.20"/>'
            '<stop offset="1" stop-color="%s" stop-opacity="0"/></radialGradient>'
            '<linearGradient id="gtext" x1="0" y1="0" x2="1" y2="0">'
            '<stop offset="0" stop-color="%s"/><stop offset="0.5" stop-color="%s"/>'
            '<stop offset="1" stop-color="%s"/></linearGradient>'
            '<filter id="blur" x="-30%%" y="-30%%" width="160%%" height="160%%">'
            '<feGaussianBlur stdDeviation="3.4"/></filter>'
            '</defs>'
            '<rect width="%d" height="%d" fill="url(#bg)"/>'
            '<rect width="%d" height="%d" fill="url(#glow)"/>'
            '%s'
            '<rect x="0.5" y="0.5" width="%d" height="%d" fill="none" stroke="%s" stroke-width="1"/>'
            '%s'
            '<text x="480" y="122" text-anchor="middle" font-family="%s" font-size="46" font-weight="800" fill="%s" filter="url(#blur)">%s</text>'
            '<text x="480" y="122" text-anchor="middle" font-family="%s" font-size="46" font-weight="800" fill="url(#gtext)">%s</text>'
            '<line x1="440" y1="142" x2="520" y2="142" stroke="%s" stroke-width="1.5"/>'
            '<text x="480" y="170" text-anchor="middle" font-family="%s" font-size="13.5" fill="%s">%s</text>'
            '<text x="28" y="224" font-family="%s" font-size="9.5" fill="%s">PROFILE VERSE · banner-card</text>'
            '</svg>'
            % (
                W, H, W, H, th.esc(USER),
                pal["bg_top"], pal["bg_bottom"],
                pal["gold"], pal["bg_top"],
                pal["gold_bright"], pal["gold"], pal["gold_bright"],
                W, H, W, H,
                stars(pal),
                W - 1, H - 1, pal["line"],
                comet(pal),
                th.FONT, pal["gold_bright"], th.esc(name),
                th.FONT, th.esc(name),
                pal["gold"],
                th.FONT, pal["muted"], th.esc(TEXT),
                th.FONT, pal["dim"],
            )
        )
        os.makedirs(os.path.dirname(os.path.abspath(OUTPUT)) or ".", exist_ok=True)
        with open(OUTPUT, "w", encoding="utf-8") as f:
            f.write(svg)
        print("OK: wrote %s (%d bytes, %s)" % (OUTPUT, len(svg), USER))
        return 0
    except Exception as e:  # noqa: BLE001
        sys.stderr.write("error: %s\n" % e)
        return 1


if __name__ == "__main__":
    sys.exit(main())
