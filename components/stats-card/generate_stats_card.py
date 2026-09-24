#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Profile Stats Card — Profile Verse component
---------------------------------------------
A differentiated "stats" card: three hero numbers (followers / public repos /
total stars) sitting on golden orbit arcs over a starfield. Signature look:
planets-on-orbits, not a plain grid.

Env: GH_TOKEN (required) · USER (default Morningstar202604) · OUTPUT
     (default stats-card.svg)

Part of Profile Verse: https://github.com/Morningstar202604/profile-verse
"""

import os
import sys
from datetime import datetime, timezone

_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, _ROOT)

from core import github as gh  # noqa: E402
from core import theme as th  # noqa: E402

OUTPUT = os.environ.get("OUTPUT", "stats-card.svg")
USER = os.environ.get("USER", "Morningstar202604")

W, H = 640, 300


def orbit(x, y, rx, ry, rot):
    return '<ellipse cx="%d" cy="%d" rx="%d" ry="%d" fill="none" stroke="%s" stroke-opacity="0.35" transform="rotate(%d %d %d)"/>' % (
        x, y, rx, ry, th.GOLD, rot, x, y)


def main():
    if not gh.token():
        sys.stderr.write("error: GH_TOKEN is required.\n")
        return 1
    try:
        prof = gh.fetch_user(USER)
        followers = int(prof.get("followers", 0))
        repos = int(prof.get("public_repos", 0))
        prs = len(gh.fetch_merged_prs(USER))
        date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        blocks = [
            (120, str(followers), "关注者"),
            (320, str(repos), "公开仓库"),
            (520, str(prs), "已合并 PR"),
        ]
        nums = "".join(
            '<text x="%d" y="186" text-anchor="middle" font-family="%s" font-size="34" font-weight="700" fill="%s">%s</text>'
            '<text x="%d" y="212" text-anchor="middle" font-family="%s" font-size="12" fill="%s">%s</text>'
            '<circle cx="%d" cy="228" r="2" fill="%s"/>'
            % (x, th.FONT, th.GOLD_BRIGHT, th.esc(v), x, th.FONT, th.MUTED, th.esc(label), x, th.GOLD)
            for x, v, label in blocks
        )

        svg = (
            '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" role="img" aria-label="Profile Stats — %s">'
            '%s'
            '<text x="30" y="40" font-family="%s" font-size="15" font-weight="700" letter-spacing="2.5" fill="%s">PROFILE STATS</text>'
            '<text x="610" y="40" text-anchor="end" font-family="%s" font-size="11" fill="%s">更新于 %s</text>'
            '<text x="30" y="64" font-family="%s" font-size="17" font-weight="600" fill="%s">%s</text>'
            '<line x1="30" y1="80" x2="610" y2="80" stroke="%s" stroke-width="1"/>'
            '%s'
            '%s'
            '<text x="30" y="%d" font-family="%s" font-size="10.5" fill="%s">数据来源 GitHub API · 每日自动刷新 · 零服务器</text>'
            '</svg>'
            % (
                W, H, W, H, th.esc(USER),
                th.card_bg(W, H),
                th.FONT, th.GOLD_BRIGHT,
                th.FONT, "#7C87A3", date,
                th.FONT, th.TEXT, th.esc(USER),
                th.LINE,
                orbit(320, 170, 300, 70, -6) + orbit(320, 170, 300, 70, 6) + orbit(320, 170, 300, 52, 0),
                nums,
                276, th.FONT, th.DIM,
            )
        )
        os.makedirs(os.path.dirname(os.path.abspath(OUTPUT)) or ".", exist_ok=True)
        with open(OUTPUT, "w", encoding="utf-8") as f:
            f.write(svg)
        print("OK: wrote %s (%d bytes, %s: followers=%d repos=%d prs=%d)" % (OUTPUT, len(svg), USER, followers, repos, prs))
        return 0
    except Exception as e:  # noqa: BLE001
        sys.stderr.write("error: %s\n" % e)
        return 1


if __name__ == "__main__":
    sys.exit(main())
