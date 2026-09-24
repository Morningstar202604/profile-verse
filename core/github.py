# -*- coding: utf-8 -*-
"""Profile Verse — shared GitHub API layer used by every component."""

import json
import os
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.github.com"


def token():
    return os.environ.get("GH_TOKEN", "").strip()


def api(path, params=None):
    url = API + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "profile-verse",
            "Authorization": "Bearer " + token(),
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_merged_prs(user, max_pr=300):
    """Merged PRs of `user` as a list of dicts: repo, number, merged_at, url."""
    prs = []
    query = "is:pr author:%s is:merged" % user
    page = 1
    try:
        while True:
            data = api(
                "/search/issues",
                {"q": query, "per_page": 100, "page": page, "sort": "updated", "order": "desc"},
            )
            for it in data.get("items", []):
                merged_at = (it.get("pull_request") or {}).get("merged_at")
                if not merged_at:
                    continue
                full_name = it.get("repository_url", "").replace(API + "/repos/", "")
                if not full_name:
                    continue
                prs.append({
                    "repo": full_name,
                    "number": it.get("number"),
                    "merged_at": merged_at,
                    "url": it.get("html_url", ""),
                })
            total = data.get("total_count", 0)
            if not data.get("items") or page * 100 >= total or len(prs) >= max_pr:
                break
            page += 1
    except urllib.error.HTTPError as e:
        if e.code == 422:  # `is:merged` unsupported in this environment
            return fetch_merged_prs_closed(user, max_pr)
        raise
    return prs[:max_pr]


def fetch_merged_prs_closed(user, max_pr=300):
    """Fallback: search closed PRs and keep only merged ones."""
    prs = []
    query = "is:pr author:%s is:closed" % user
    page = 1
    while True:
        data = api(
            "/search/issues",
            {"q": query, "per_page": 100, "page": page, "sort": "updated", "order": "desc"},
        )
        for it in data.get("items", []):
            merged_at = (it.get("pull_request") or {}).get("merged_at")
            if not merged_at:
                continue
            full_name = it.get("repository_url", "").replace(API + "/repos/", "")
            if not full_name:
                continue
            prs.append({
                "repo": full_name,
                "number": it.get("number"),
                "merged_at": merged_at,
                "url": it.get("html_url", ""),
            })
        total = data.get("total_count", 0)
        if not data.get("items") or page * 100 >= total or len(prs) >= max_pr:
            break
        page += 1
    return prs[:max_pr]


def get_stars(repo):
    """stargazers_count of a repository."""
    return int(api("/repos/" + repo).get("stargazers_count", 0))


def fmt_stars(n):
    """1000 -> 1k, 189900 -> 189.9k."""
    if n >= 1000:
        v = n / 1000.0
        s = ("%.1f" % v).rstrip("0").rstrip(".")
        return s + "k"
    return str(n)
