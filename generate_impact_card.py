#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Impact Card Generator
----------------------------
Generates a beautiful SVG card showing a GitHub user's merged pull requests,
weighted by the star count of the repositories they contributed to.

Zero-server: run it in GitHub Actions on a schedule, commit the generated SVG,
then reference it from any README via raw.githubusercontent / GitHub Pages /
jsDelivr CDN. No server, no cost.

Environment variables:
  GH_TOKEN  GitHub token (recommended; required for paginated merged-PR search)
  USERS     comma-separated GitHub usernames (default: Morningstar202604)
  OUTPUT    output SVG path (default: impact-card.svg)
  MAX_PR    max merged PRs to scan per user (default: 300)
  MAX_TOP   max top repositories shown on the card (default: 5)

Tier boundaries (repository stars):
  S >= 50k   A >= 10k   B >= 1k   C >= 100   D < 100
"""

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.sax.saxutils as sax
from collections import Counter
from datetime import datetime, timezone
from string import Template

API = "https://api.github.com"
TOKEN = os.environ.get("GH_TOKEN", "").strip()
USERS = [u.strip() for u in os.environ.get("USERS", "Morningstar202604").split(",") if u.strip()]
OUTPUT = os.environ.get("OUTPUT", "impact-card.svg")
MAX_PR = int(os.environ.get("MAX_PR", "300"))
MAX_TOP = int(os.environ.get("MAX_TOP", "5"))

TIERS = [
    ("S", 50000, "\u226550k\u2605", "#C9A86A", "#E4C87F"),
    ("A", 10000, "\u226510k\u2605", "#5B8DEF", "#8FB4F5"),
    ("B", 1000, "\u22651k\u2605", "#4EC9A0", "#7ED9B8"),
    ("C", 100, "\u2265100\u2605", "#B48AE8", "#C3A6EF"),
    ("D", 0, "<100\u2605", "#6E7893", "#B9C0CE"),
]

FONT = "'Segoe UI',Helvetica,Arial,'PingFang SC','Microsoft YaHei',sans-serif"


def api(path, params=None):
    url = API + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "impact-card-generator",
            "Authorization": "Bearer " + TOKEN,
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_merged_prs(user):
    """Return merged PRs of `user` as list of dicts."""
    prs = []
    query = "is:pr author:%s is:merged" % user
    page = 1
    try:
        while True:
            data = api("/search/issues", {"q": query, "per_page": 100, "page": page, "sort": "updated", "order": "desc"})
            items = data.get("items", [])
            for it in items:
                merged_at = (it.get("pull_request") or {}).get("merged_at")
                if not merged_at:
                    continue
                repo_url = it.get("repository_url", "")
                full_name = repo_url.replace(API + "/repos/", "")
                if not full_name:
                    continue
                prs.append({
                    "repo": full_name,
                    "number": it.get("number"),
                    "merged_at": merged_at,
                    "url": it.get("html_url", ""),
                })
            total = data.get("total_count", 0)
            if not items or page * 100 >= total or len(prs) >= MAX_PR:
                break
            page += 1
    except urllib.error.HTTPError as e:
        if e.code == 422:  # `is:merged` not supported in this environment
            return fetch_merged_prs_closed(user)
        raise
    return prs[:MAX_PR]


def fetch_merged_prs_closed(user):
    """Fallback: search closed PRs and keep only merged ones."""
    prs = []
    query = "is:pr author:%s is:closed" % user
    page = 1
    while True:
        data = api("/search/issues", {"q": query, "per_page": 100, "page": page, "sort": "updated", "order": "desc"})
        items = data.get("items", [])
        for it in items:
            merged_at = (it.get("pull_request") or {}).get("merged_at")
            if not merged_at:
                continue
            repo_url = it.get("repository_url", "")
            full_name = repo_url.replace(API + "/repos/", "")
            if not full_name:
                continue
            prs.append({"repo": full_name, "number": it.get("number"), "merged_at": merged_at, "url": it.get("html_url", "")})
        total = data.get("total_count", 0)
        if not items or page * 100 >= total or len(prs) >= MAX_PR:
            break
        page += 1
    return prs[:MAX_PR]


def get_stars(repo):
    """Return stargazers_count of a repository."""
    data = api("/repos/" + repo)
    return int(data.get("stargazers_count", 0))


def fmt_stars(n):
    if n >= 1000:
        v = n / 1000.0
        s = ("%.1f" % v).rstrip("0").rstrip(".")
        return s + "k"
    return str(n)


def esc(text):
    return sax.escape(str(text))


def build_data():
    prs = []
    for user in USERS:
        prs.extend(fetch_merged_prs(user))

    # dedupe PRs across accounts by (repo, number)
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
    stars = {}
    for repo in repo_names:
        stars[repo] = get_stars(repo)

    repo_prs = Counter(p["repo"] for p in prs)

    # tier stats: list of (label, range_text, repo_count, pr_count, color, bright)
    tier_stats = []
    for i, (label, thr, range_text, color, bright) in enumerate(TIERS):
        upper = TIERS[i - 1][1] if i > 0 else float("inf")
        repos_in = [r for r in repo_names if thr <= stars[r] < upper]
        prs_in = sum(repo_prs[r] for r in repos_in)
        tier_stats.append((label, range_text, len(repos_in), prs_in, color, bright))

    top = sorted(repo_names, key=lambda r: -stars[r])[:MAX_TOP]
    impact = sum(stars.values())
    recent = max(prs, key=lambda p: p["merged_at"])

    return {
        "prs": prs,
        "stars": stars,
        "repo_prs": repo_prs,
        "tier_stats": tier_stats,
        "top": top,
        "impact": impact,
        "recent": recent,
    }


def tier_boxes(tier_stats):
    out, x, w, gap = [], 30, 108, 10
    any_pr = any(t[3] for t in tier_stats)
    for label, range_text, repo_cnt, pr_cnt, color, bright in tier_stats:
        count_text = "%d \u4ed3 \u00b7 %d PR" % (repo_cnt, pr_cnt)
        count_fill = bright if any_pr and pr_cnt > 0 else "#6E7893"
        out.append(
            '<rect x="%d" y="220" width="%d" height="48" rx="8" fill="%s" fill-opacity="0.10" stroke="%s" stroke-opacity="0.55"/>'
            '<text x="%d" y="243" text-anchor="middle" font-family="%s" font-size="11.5" font-weight="700" fill="%s">%s %s</text>'
            '<text x="%d" y="260" text-anchor="middle" font-family="%s" font-size="10.5" fill="%s">%s</text>'
            % (x, w, color, color, x + w // 2, FONT, bright, esc(label), esc(range_text), x + w // 2, FONT, count_fill, esc(count_text))
        )
        x += w + gap
    return "".join(out)


def top_rows(top, stars, repo_prs):
    out, y = [], 326
    for name in top:
        if len(name) > 42:
            name = name[:41] + "\u2026"
        star_color = "#E4C87F" if stars[name] >= 10000 else "#D5DAE4"
        out.append(
            '<text x="30" y="%d" font-family="%s" font-size="12.5" fill="#F5F0E6">%s</text>'
            '<text x="610" y="%d" text-anchor="end" font-family="%s" font-size="12" font-weight="600" fill="%s">\u2605%s \u00b7 %d PR</text>'
            % (y, FONT, esc(name), y, FONT, star_color, fmt_stars(stars[name]), repo_prs[name])
        )
        y += 26
    return "".join(out), y


def render(data):
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    user_label = " \u00b7 ".join(USERS)

    if data is None:
        return (
            '<svg xmlns="http://www.w3.org/2000/svg" width="640" height="210" viewBox="0 0 640 210" '
            'role="img" aria-label="Open Source Impact Card - %s">\n'
            '  <defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0B1026"/>'
            '<stop offset="1" stop-color="#131D38"/></linearGradient></defs>\n'
            '  <rect width="640" height="210" rx="16" fill="url(#bg)" stroke="#243356" stroke-width="1.5"/>\n'
            '  <text x="30" y="40" font-family="%s" font-size="15" font-weight="700" letter-spacing="2.5" fill="#E4C87F">OPEN SOURCE IMPACT</text>\n'
            '  <text x="610" y="40" text-anchor="end" font-family="%s" font-size="11" fill="#7C87A3">\u66f4\u65b0\u4e8e %s</text>\n'
            '  <text x="30" y="66" font-family="%s" font-size="17" font-weight="600" fill="#F5F0E6">%s</text>\n'
            '  <line x1="30" y1="82" x2="610" y2="82" stroke="#243356" stroke-width="1"/>\n'
            '  <text x="320" y="140" text-anchor="middle" font-family="%s" font-size="15" fill="#9AA3B5">\u8fd8\u6ca1\u6709\u5df2\u5408\u5e76\u7684 PR</text>\n'
            '  <text x="30" y="180" font-family="%s" font-size="10.5" fill="#6E7893">\u6570\u636e\u6765\u6e90 GitHub API \u00b7 \u6bcf\u65e5\u81ea\u52a8\u5237\u65b0 \u00b7 \u96f6\u670d\u52a1\u5668\u81ea\u52a8\u751f\u6210</text>\n'
            '</svg>\n' % (esc(user_label), FONT, FONT, date, FONT, esc(user_label), FONT, FONT)
        )

    pr_count = len(data["prs"])
    repo_count = len(data["stars"])
    impact = "\u2248%s\u2605" % fmt_stars(data["impact"])

    tier_html = tier_boxes(data["tier_stats"])
    top_html, y_after = top_rows(data["top"], data["stars"], data["repo_prs"])

    recent = data["recent"]
    recent_text = "\u6700\u8fd1\u5408\u5e76\uff1a%s #%d \u00b7 %s" % (
        recent["repo"], recent["number"], recent["merged_at"][:10],
    )
    if len(recent_text) > 58:
        recent_text = recent_text[:57] + "\u2026"
    recent_y = y_after + 14
    recent_html = (
        '<text x="30" y="%d" font-family="%s" font-size="11.5" fill="#9AA3B5">%s</text>'
        % (recent_y, FONT, esc(recent_text))
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
    )


def main():
    if not TOKEN:
        sys.stderr.write("error: GH_TOKEN is required (merged-PR search needs auth).\n")
        return 1
    try:
        data = build_data()
        svg = render(data)
        os.makedirs(os.path.dirname(os.path.abspath(OUTPUT)), exist_ok=True)
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
                    '<rect width="640" height="120" fill="#0B1026" rx="12"/>'
                    '<text x="30" y="66" font-family="%s" font-size="14" fill="#E4C87F">\u751f\u6210\u5931\u8d25\uff1a%s</text></svg>'
                    % (FONT, esc(str(e)))
                )
        finally:
            return 1


if __name__ == "__main__":
    sys.exit(main())
