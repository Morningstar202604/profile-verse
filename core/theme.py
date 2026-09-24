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


def starfield(width, height, n=90, seed=202604, color="#F5F0E6"):
    """Deterministic starry background: a set of faint dots (signature look)."""
    import random

    rnd = random.Random(seed)
    parts = []
    for _ in range(n):
        x = rnd.randint(0, width)
        y = rnd.randint(0, height)
        r = rnd.choice((0.5, 0.7, 1.0, 1.4))
        op = rnd.uniform(0.18, 0.75)
        parts.append('<circle cx="%d" cy="%d" r="%.2f" fill="%s" opacity="%.3f"/>' % (x, y, r, color, op))
    return "".join(parts)


def card_bg(width, height, seed=202604, rx=16):
    """Standard card frame: deep-blue gradient + starfield + thin border."""
    return (
        '<defs>'
        '<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/>'
        '</linearGradient>'
        '<radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">'
        '<stop offset="0" stop-color="%s" stop-opacity="0.35"/>'
        '<stop offset="1" stop-color="%s" stop-opacity="0"/>'
        '</radialGradient>'
        '</defs>'
        '<rect width="%d" height="%d" rx="%d" fill="url(#bg)" stroke="%s" stroke-width="1.5"/>'
        '%s'
    ) % (BG, CARD, GOLD, GOLD, width, height, rx, LINE, starfield(width, height, 80, seed))
