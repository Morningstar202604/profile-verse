#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Streak Card — Profile Verse component
--------------------------------------
A differentiated streak card: the current streak is the star at the centre of
a golden orbital ring (a "star orbit"), with longest streak and yearly total
contributions as two constellation chips. Signature look: star-orbit ring.

Data is real, from the GitHub contribution calendar (GraphQL, full year).

Env: GH_TOKEN (required) · USER (default Morningstar202604) · OUTPUT
     (default streak-card.svg) · THEME (dark|light)

Part of Profile Verse: https://github.com/Morningstar202604/profile-verse
"""

import math
import os
import sys
from datetime import datetime, timezone

_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, _ROOT)

from core import github as gh  # noqa: E402
from core import theme as th  # noqa: E402

OUTPUT = os.environ.get("OUTPUT", "streak-card.svg")
USER = os.environ.get("USER", "Morningstar202604")
THEME = os.environ.get("THEME", "dark")

W, H = 640, 360
CX, CY, R = 320, 195, 84


def ring_dots(pal, n=12, r=R + 14):
    out = []
    for i in range(n):
        a = 2 * math.pi * i / n
        out.append('<circle cx="%.1f" cy="%.1f" r="1.6" fill="%s" opacity="0.8"/>' % (CX + r * math.cos(a), CY + r * math.sin(a), pal["gold"]))
    return "".join(out)


def chip(x, w, value, label, pal):
    return (
        '<rect x="%d" y="296" width="%d" height="40" rx="20" fill="%s" fill-opacity="0.10" stroke="%s" stroke-opacity="0.55"/>'
        '<text x="%d" y="312" text-anchor="middle" font-family="%s" font-size="15" font-weight="700" fill="%s">%s</text>'
        '<text x="%d" y="327" text-anchor="middle" font-family="%s" font-size="10.5" fill="%s">%s</text>'
        % (x, w, pal["gold"], pal["gold"], x + w // 2, th.FONT, pal["gold_bright"], th.esc(value), x + w // 2, th.FONT, pal["muted"], th.esc(label))
    )


def main():
    if not gh.token():
        sys.stderr.write("error: GH_TOKEN is required.\n")
        return 1
    pal = th.palette(THEME)
    try:
        total, days = gh.fetch_contribution_calendar(USER)
        cur, longest = gh.compute_streaks(days)
        date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        light = THEME != "dark"

        svg = (
            '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" role="img" aria-label="Streak — %s">'
            '%s'
            '<text x="30" y="40" font-family="%s" font-size="15" font-weight="700" letter-spacing="2.5" fill="%s">STREAK</text>'
            '<text x="610" y="40" text-anchor="end" font-family="%s" font-size="11" fill="%s">更新于 %s</text>'
            '<text x="30" y="64" font-family="%s" font-size="17" font-weight="600" fill="%s">%s</text>'
            '<line x1="30" y1="80" x2="610" y2="80" stroke="%s" stroke-width="1"/>'
            '<circle cx="%d" cy="%d" r="%d" fill="url(#glow)"/>'
            '<circle cx="%d" cy="%d" r="%d" fill="none" stroke="%s" stroke-opacity="%s" stroke-width="1.5"/>'
            '<circle cx="%d" cy="%d" r="%d" fill="none" stroke="%s" stroke-opacity="%s" stroke-dasharray="2 6"/>'
            '%s'
            '<circle cx="%d" cy="%d" r="4" fill="%s"/>'
            '<text x="%d" y="202" text-anchor="middle" font-family="%s" font-size="46" font-weight="700" fill="%s">%d</text>'
            '<text x="%d" y="226" text-anchor="middle" font-family="%s" font-size="12" fill="%s">当前连续 · 天</text>'
            '%s'
            '%s'
            '<text x="30" y="%d" font-family="%s" font-size="10.5" fill="%s">数据来源 GitHub 贡献日历 · 每日自动刷新 · 零服务器</text>'
            '</svg>'
            % (
                W, H, W, H, th.esc(USER),
                th.card_bg(pal, W, H),
                th.FONT, pal["gold_bright"],
                th.FONT, pal["sub"], date,
                th.FONT, pal["text"], th.esc(USER),
                pal["line"],
                CX, CY, R + 26,
                CX, CY, R,
                pal["gold"], 0.85 if light else 0.5, CX, CY, R + 14, pal["gold"], 0.4 if light else 0.18,
                ring_dots(pal),
                CX, CY - R - 14, pal["gold_bright"],
                CX, th.FONT, pal["gold_bright"], cur,
                CX, th.FONT, pal["muted"],
                chip(100, 170, "%d 天" % longest, "最长连续", pal),
                chip(370, 170, "%d 次" % total, "全年贡献", pal),
                340, th.FONT, pal["dim"],
            )
        )
        os.makedirs(os.path.dirname(os.path.abspath(OUTPUT)) or ".", exist_ok=True)
        with open(OUTPUT, "w", encoding="utf-8") as f:
            f.write(svg)
        print("OK: wrote %s (%d bytes, %s: current=%d longest=%d total=%d)" % (OUTPUT, len(svg), USER, cur, longest, total))
        return 0
    except Exception as e:  # noqa: BLE001
        sys.stderr.write("error: %s\n" % e)
        return 1


if __name__ == "__main__":
    sys.exit(main())
