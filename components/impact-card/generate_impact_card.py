#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Impact Card — Profile Verse component
--------------------------------------------
Generates a beautiful SVG card showing a GitHub user's merged pull requests,
weighted by the star count of the repositories they contributed to.

Run:  python3 generate_impact_card.py
Env:  GH_TOKEN (required) · USERS (default Morningstar202604) · OUTPUT
      (default impact-card.svg) · MAX_PR (300) · MAX_TOP (5) · THEME (dark|light)

Part of Profile Verse: https://github.com/Morningstar202604/profile-verse
"""

import os
import sys
from collections import Counter
from datetime import datetime, timezone
from string import Template

_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, _ROOT)

from core import github as gh  # noqa: E402
from core import theme as th  # noqa: E402

OUTPUT = os.environ.get("OUTPUT", "impact-card.svg")
USERS = [u.strip() for u in os.environ.get("USERS", "Morningstar202604").split(",") if u.strip()]
MAX_PR = int(os.environ.get("MAX_PR", "300"))
MAX_TOP = int(os.environ.get("MAX_TOP", "5"))
THEME = os.environ.get("THEME", "dark")

FONT = th.FONT
TIERS = th.TIERS
esc = th.esc


def build_data():
    prs = []
    for user in USERS:
        prs.extend(gh.fetch_merged_prs(user, MAX_PR))

    # dedupe across accounts by (repo, number)
    seen, unique = set(), []
    for p in prs:
        key = (p["repo"], p["number"])
        if key not in seen:
            seen.add(key)
            unique.append(p)
    prs = unique

    if not prs:
        return None

    repo_names = sorted({p["repo"] for p in prs})
    stars = {r: gh.get_stars(r) for r in repo_names}
    repo_prs = Counter(p["repo"] for p in prs)

    tier_stats = []
    for i, (label, thr, range_text, color, bright) in enumerate(TIERS):
        upper = TIERS[i - 1][1] if i > 0 else float("inf")
        repos_in = [r for r in repo_names if thr <= stars[r] < upper]
        tier_stats.append((label, range_text, len(repos_in), sum(repo_prs[r] for r in repos_in), color, bright))

    top = sorted(repo_names, key=lambda r: -stars[r])[:MAX_TOP]

    return {
        "prs": prs,
        "stars": stars,
        "repo_prs": repo_prs,
        "tier_stats": tier_stats,
        "top": top,
        "impact": sum(stars.values()),
        "recent": max(prs, key=lambda p: p["merged_at"]),
    }


def tier_boxes(tier_stats, pal):
    out, x, w, gap = [], 30, 108, 10
    any_pr = any(t[3] for t in tier_stats)
    for label, range_text, repo_cnt, pr_cnt, color, bright in tier_stats:
        count_text = "%d \u4ed3 \u00b7 %d PR" % (repo_cnt, pr_cnt)
        count_fill = bright if any_pr and pr_cnt > 0 else pal["dim"]
        out.append(
            '<rect x="%d" y="220" width="%d" height="48" rx="8" fill="%s" fill-opacity="0.10" stroke="%s" stroke-opacity="0.55"/>'
            '<text x="%d" y="243" text-anchor="middle" font-family="%s" font-size="11.5" font-weight="700" fill="%s">%s %s</text>'
            '<text x="%d" y="260" text-anchor="middle" font-family="%s" font-size="10.5" fill="%s">%s</text>'
            % (x, w, color, color, x + w // 2, FONT, bright, esc(label), esc(range_text), x + w // 2, FONT, count_fill, esc(count_text))
        )
        x += w + gap
    return "".join(out)


def top_rows(top, stars, repo_prs, pal):
    out, y = [], 326
    for name in top:
        if len(name) > 42:
            name = name[:41] + "\u2026"
        star_color = pal["gold_bright"] if stars[name] >= 10000 else pal["row_sub"]
        out.append(
            '<text x="30" y="%d" font-family="%s" font-size="12.5" fill="%s">%s</text>'
            '<text x="610" y="%d" text-anchor="end" font-family="%s" font-size="12" font-weight="600" fill="%s">\u2605%s \u00b7 %d PR</text>'
            % (y, FONT, pal["text"], esc(name), y, FONT, star_color, gh.fmt_stars(stars[name]), repo_prs[name])
        )
        y += 26
    return "".join(out), y


def render(data):
    pal = th.palette(THEME)
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    user_label = " \u00b7 ".join(USERS)

    if data is None:
        return (
            '<svg xmlns="http://www.w3.org/2000/svg" width="640" height="210" viewBox="0 0 640 210" '
            'role="img" aria-label="Open Source Impact Card - %s">\n'
            '  <defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="%s"/>'
            '<stop offset="1" stop-color="%s"/></linearGradient></defs>\n'
            '  <rect width="640" height="210" rx="16" fill="url(#bg)" stroke="%s" stroke-width="1.5"/>\n'
            '  <text x="30" y="40" font-family="%s" font-size="15" font-weight="700" letter-spacing="2.5" fill="%s">OPEN SOURCE IMPACT</text>\n'
            '  <text x="610" y="40" text-anchor="end" font-family="%s" font-size="11" fill="%s">\u66f4\u65b0\u4e8e %s</text>\n'
            '  <text x="30" y="66" font-family="%s" font-size="17" font-weight="600" fill="%s">%s</text>\n'
            '  <line x1="30" y1="82" x2="610" y2="82" stroke="%s" stroke-width="1"/>\n'
            '  <text x="320" y="140" text-anchor="middle" font-family="%s" font-size="15" fill="%s">\u8fd8\u6ca1\u6709\u5df2\u5408\u5e76\u7684 PR</text>\n'
            '  <text x="30" y="180" font-family="%s" font-size="10.5" fill="%s">\u6570\u636e\u6765\u6e90 GitHub API \u00b7 \u6bcf\u65e5\u81ea\u52a8\u5237\u65b0 \u00b7 \u96f6\u670d\u52a1\u5668\u81ea\u52a8\u751f\u6210</text>\n'
            '</svg>\n' % (esc(user_label), pal["bg_top"], pal["bg_bottom"], pal["line"], FONT, pal["gold_bright"], FONT, pal["sub"], date, FONT, pal["text"], esc(user_label), pal["line"], FONT, pal["muted"], FONT, pal["dim"])
        )

    pr_count = len(data["prs"])
    repo_count = len(data["stars"])
    impact = "\u2248%s\u2605" % gh.fmt_stars(data["impact"])

    tier_html = tier_boxes(data["tier_stats"], pal)
    top_html, y_after = top_rows(data["top"], data["stars"], data["repo_prs"], pal)

    recent = data["recent"]
    recent_text = "\u6700\u8fd1\u5408\u5e76\uff1a%s #%d \u00b7 %s" % (
        recent["repo"], recent["number"], recent["merged_at"][:10],
    )
    if len(recent_text) > 58:
        recent_text = recent_text[:57] + "\u2026"
    recent_y = y_after + 14
    recent_html = (
        '<text x="30" y="%d" font-family="%s" font-size="11.5" fill="%s">%s</text>'
        % (recent_y, FONT, pal["muted"], esc(recent_text))
    )

    footer_y = recent_y + 30
    height = footer_y + 26

    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "card_template.svg.tpl"), encoding="utf-8") as f:
        tpl = Template(f.read())

    return tpl.safe_substitute(
        HEIGHT=str(height),
        DATE=date,
        USER=esc(user_label),
        PR_COUNT=str(pr_count),
        REPO_COUNT=str(repo_count),
        IMPACT=esc(impact),
        TIER_BOXES=tier_html,
        TOP_ROWS=top_html,
        RECENT_LINE=recent_html,
        FOOTER_Y=str(footer_y),
        BG_TOP=pal["bg_top"],
        BG_BOTTOM=pal["bg_bottom"],
        LINE=pal["line"],
        TEXT=pal["text"],
        MUTED=pal["muted"],
        DIM=pal["dim"],
        GOLD=pal["gold"],
        GOLD_BRIGHT=pal["gold_bright"],
        SUB=pal["sub"],
        PANEL="#0A0E1F" if THEME != "light" else "#F8F6F1",
    )


def main():
    if not gh.token():
        sys.stderr.write("error: GH_TOKEN is required (merged-PR search needs auth).\n")
        return 1
    pal = th.palette(THEME)
    try:
        data = build_data()
        svg = render(data)
        os.makedirs(os.path.dirname(os.path.abspath(OUTPUT)) or ".", exist_ok=True)
        with open(OUTPUT, "w", encoding="utf-8") as f:
            f.write(svg)
        print("OK: wrote %s (%d bytes, %d merged PRs, %d repos)" % (OUTPUT, len(svg), len(data["prs"]) if data else 0, len(data["stars"]) if data else 0))
        return 0
    except Exception as e:  # noqa: BLE001
        sys.stderr.write("error: %s\n" % e)
        try:
            with open(OUTPUT, "w", encoding="utf-8") as f:
                f.write(
                    '<svg xmlns="http://www.w3.org/2000/svg" width="640" height="120" viewBox="0 0 640 120">'
                    '<rect width="640" height="120" fill="%s" rx="12"/>'
                    '<text x="30" y="66" font-family="%s" font-size="14" fill="%s">\u751f\u6210\u5931\u8d25\uff1a%s</text></svg>'
                    % (pal["bg_top"], FONT, pal["gold_bright"], esc(str(e)))
                )
        finally:
            return 1


if __name__ == "__main__":
    sys.exit(main())
