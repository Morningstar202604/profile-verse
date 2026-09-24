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
     (default streak-card.svg)

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

W, H = 640, 360
CX, CY, R = 320, 195, 84


def ring_dots(n=12, r=R + 14, color=th.GOLD):
    out = []
    for i in range(n):
        a = 2 * math.pi * i / n
        out.append('<circle cx="%.1f" cy="%.1f" r="1.6" fill="%s" opacity="0.8"/>' % (CX + r * math.cos(a), CY + r * math.sin(a), color))
    return "".join(out)


def chip(x, w, value, label):
    return (
        '<rect x="%d" y="296" width="%d" height="40" rx="20" fill="%s" fill-opacity="0.10" stroke="%s" stroke-opacity="0.55"/>'
        '<text x="%d" y="312" text-anchor="middle" font-family="%s" font-size="15" font-weight="700" fill="%s">%s</text>'
        '<text x="%d" y="327" text-anchor="middle" font-family="%s" font-size="10.5" fill="%s">%s</text>'
        % (x, w, th.GOLD, th.GOLD, x + w // 2, th.FONT, th.GOLD_BRIGHT, th.esc(value), x + w // 2, th.FONT, th.MUTED, th.esc(label))
    )


def main():
    if not gh.token():
        sys.stderr.write("error: GH_TOKEN is required.\n")
        return 1
    try:
        total, days = gh.fetch_contribution_calendar(USER)
        cur, longest = gh.compute_streaks(days)
        date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        svg = (
            '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" role="img" aria-label="Streak — %s">'
            '%s'
            '<text x="30" y="40" font-family="%s" font-size="15" font-weight="700" letter-spacing="2.5" fill="%s">STREAK</text>'
            '<text x="610" y="40" text-anchor="end" font-family="%s" font-size="11" fill="%s">更新于 %s</text>'
            '<text x="30" y="64" font-family="%s" font-size="17" font-weight="600" fill="%s">%s</text>'
            '<line x1="30" y1="80" x2="610" y2="80" stroke="%s" stroke-width="1"/>'
            '<circle cx="%d" cy="%d" r="%d" fill="url(#glow)"/>'
            '<circle cx="%d" cy="%d" r="%d" fill="none" stroke="%s" stroke-opacity="0.5" stroke-width="1.5"/>'
            '<circle cx="%d" cy="%d" r="%d" fill="none" stroke="%s" stroke-opacity="0.18" stroke-dasharray="2 6"/>'
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
                th.card_bg(W, H),
                th.FONT, th.GOLD_BRIGHT,
                th.FONT, "#7C87A3", date,
                th.FONT, th.TEXT, th.esc(USER),
                th.LINE,
                CX, CY, R + 26,
                CX, CY, R,
                th.GOLD, CX, CY, R + 14, th.GOLD,
                ring_dots(),
                CX, CY - R - 14, th.GOLD_BRIGHT,
                CX, th.FONT, th.GOLD_BRIGHT, cur,
                CX, th.FONT, th.MUTED,
                chip(100, 170, "%d 天" % longest, "最长连续"),
                chip(370, 170, "%d 次" % total, "全年贡献"),
                340, th.FONT, th.DIM,
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
