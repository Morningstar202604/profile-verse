#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Badge Card — Profile Verse component
------------------------------------
A row of gold medal-style badges that replace the flat shields.io strip:
each badge is a pill with a golden gradient border and a star icon.
Signature look: golden medals, not flat pills.

Data: by default auto-computed from GitHub (merged PRs / yearly contributions /
public repos / followers); or pass your own via `badges` ("label=value;...").

Env: GH_TOKEN (required for auto mode) · USER (default Morningstar202604) ·
     BADGES (optional custom badges) · OUTPUT (default badge-card.svg) ·
     THEME (dark|light)

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

OUTPUT = os.environ.get("OUTPUT", "badge-card.svg")
USER = os.environ.get("USER", "Morningstar202604")
BADGES_RAW = os.environ.get("BADGES", "")
THEME = os.environ.get("THEME", "dark")

W, H = 640, 172
BADGE_W, BADGE_H = 136, 74
GAP = 12


def star_icon(cx, cy, r=7, fill="#C9A86A"):
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append("%.1f,%.1f" % (cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return '<polygon points="%s" fill="%s"/>' % (" ".join(pts), fill)


def badge(x, value, label, pal):
    return (
        '<defs>'
        '<linearGradient id="ge%d" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/>'
        '</linearGradient></defs>'
        '<rect x="%d" y="64" width="%d" height="%d" rx="20" fill="%s" fill-opacity="0.08" stroke="url(#ge%d)" stroke-width="1.6"/>'
        '%s'
        '<text x="%d" y="%d" text-anchor="middle" font-family="%s" font-size="22" font-weight="700" fill="%s">%s</text>'
        '<text x="%d" y="%d" text-anchor="middle" font-family="%s" font-size="11" fill="%s">%s</text>'
        % (x, pal["gold"], pal["gold_bright"],
           x, BADGE_W, BADGE_H, pal["gold"], x,
           star_icon(x + 20, 96, 7, pal["gold_bright"]),
           x + BADGE_W // 2, 100, th.FONT, pal["gold_bright"], th.esc(value),
           x + BADGE_W // 2, 121, th.FONT, pal["muted"], th.esc(label))
    )


def main():
    pal = th.palette(THEME)
    try:
        date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        if BADGES_RAW.strip():
            items = []
            for seg in BADGES_RAW.split(";"):
                seg = seg.strip()
                if not seg:
                    continue
                if "=" in seg:
                    label, value = seg.split("=", 1)
                    items.append((value.strip(), label.strip()))
                else:
                    items.append((seg.strip(), seg.strip()))
        else:
            if not gh.token():
                sys.stderr.write("error: GH_TOKEN is required when BADGES is not set.\n")
                return 1
            prof = gh.fetch_user(USER)
            prs = len(gh.fetch_merged_prs(USER))
            total, _ = gh.fetch_contribution_calendar(USER)
            items = [
                ("%d" % prs, "已合并 PR"),
                ("%d" % total, "全年贡献"),
                ("%d" % prof.get("public_repos", 0), "公开仓库"),
                ("%d" % prof.get("followers", 0), "关注者"),
            ]

        badges = []
        n = len(items[:5])
        total_w = n * BADGE_W + (n - 1) * GAP
        x0 = (W - total_w) // 2
        for i, (value, label) in enumerate(items[:5]):
            badges.append(badge(x0 + i * (BADGE_W + GAP), value, label, pal))

        svg = (
            '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" role="img" aria-label="Badges — %s">'
            '%s'
            '<text x="30" y="40" font-family="%s" font-size="15" font-weight="700" letter-spacing="2.5" fill="%s">BADGES</text>'
            '<text x="610" y="40" text-anchor="end" font-family="%s" font-size="11" fill="%s">更新于 %s</text>'
            '<line x1="30" y1="52" x2="610" y2="52" stroke="%s" stroke-width="1"/>'
            '%s'
            '<text x="30" y="%d" font-family="%s" font-size="10.5" fill="%s">%s</text>'
            '</svg>'
            % (
                W, H, W, H, th.esc(USER),
                th.card_bg(pal, W, H),
                th.FONT, pal["gold_bright"],
                th.FONT, pal["sub"], date,
                pal["line"],
                "".join(badges),
                H - 16, th.FONT, pal["dim"],
                th.esc("数据来源 GitHub API · 每日自动刷新 · 零服务器" if not BADGES_RAW.strip() else "自定义徽章 · 由输入参数生成 · 零服务器"),
            )
        )
        os.makedirs(os.path.dirname(os.path.abspath(OUTPUT)) or ".", exist_ok=True)
        with open(OUTPUT, "w", encoding="utf-8") as f:
            f.write(svg)
        print("OK: wrote %s (%d bytes, %d badges)" % (OUTPUT, len(svg), len(items)))
        return 0
    except Exception as e:  # noqa: BLE001
        sys.stderr.write("error: %s\n" % e)
        return 1


if __name__ == "__main__":
    sys.exit(main())
