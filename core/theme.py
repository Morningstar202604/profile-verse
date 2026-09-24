# -*- coding: utf-8 -*-
"""Profile Verse — shared design tokens for every card (deep-blue + gold brand)."""

import xml.sax.saxutils as sax

FONT = "'Segoe UI',Helvetica,Arial,'PingFang SC','Microsoft YaHei',sans-serif"

# brand palette
BG = "#0B1026"
CARD = "#131D38"
LINE = "#243356"
TEXT = "#F5F0E6"
MUTED = "#9AA3B5"
DIM = "#6E7893"
GOLD = "#C9A86A"
GOLD_BRIGHT = "#E4C87F"

# star tiers: (label, min_stars, range_text, color, bright)
TIERS = [
    ("S", 50000, "\u226550k\u2605", "#C9A86A", "#E4C87F"),
    ("A", 10000, "\u226510k\u2605", "#5B8DEF", "#8FB4F5"),
    ("B", 1000, "\u22651k\u2605", "#4EC9A0", "#7ED9B8"),
    ("C", 100, "\u2265100\u2605", "#B48AE8", "#C3A6EF"),
    ("D", 0, "<100\u2605", "#6E7893", "#B9C0CE"),
]


def esc(text):
    """XML-escape text for safe embedding in SVG."""
    return sax.escape(str(text))
