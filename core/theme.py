# -*- coding: utf-8 -*-
"""Profile Verse — shared design tokens for every card.

Two full palettes: "dark" (deep-blue + gold brand, default) and "light"
(paper-white + deep gold, for profiles on light themes). Every component
reads `theme` input -> THEME env -> th.palette(THEME).
"""

import xml.sax.saxutils as sax

FONT = "'Segoe UI',Helvetica,Arial,'PingFang SC','Microsoft YaHei',sans-serif"

# --------------------------------------------------------------------------
# brand palettes
# --------------------------------------------------------------------------
PALETTES = {
    "dark": {
        "bg_top": "#0B1026",
        "bg_bottom": "#131D38",
        "line": "#243356",
        "text": "#F5F0E6",
        "muted": "#9AA3B5",
        "dim": "#6E7893",
        "gold": "#C9A86A",
        "gold_bright": "#E4C87F",
        "sub": "#7C87A3",        # small header meta text
        "star": "#F5F0E6",       # starfield dots
        "star_op": 0.35,
        "row_sub": "#D5DAE4",    # secondary row text (impact-card)
    },
    "light": {
        "bg_top": "#FFFFFF",
        "bg_bottom": "#F4F1EA",
        "line": "#E2DCCF",
        "text": "#16213E",
        "muted": "#5F6B7F",
        "dim": "#8A93A6",
        "gold": "#B08D3E",
        "gold_bright": "#8F6F2C",
        "sub": "#8A93A6",
        "star": "#C9A86A",
        "star_op": 0.16,
        "row_sub": "#3C4858",
    },
}

# aliases for backward-compatible reads inside generators that still use
# module-level tokens (each generator should switch to pal[...] eventually)
BG = PALETTES["dark"]["bg_top"]
CARD = PALETTES["dark"]["bg_bottom"]
LINE = PALETTES["dark"]["line"]
TEXT = PALETTES["dark"]["text"]
MUTED = PALETTES["dark"]["muted"]
DIM = PALETTES["dark"]["dim"]
GOLD = PALETTES["dark"]["gold"]
GOLD_BRIGHT = PALETTES["dark"]["gold_bright"]


def palette(name):
    """Return the palette dict for a theme name; unknown -> dark."""
    key = (name or "").strip().lower()
    return PALETTES.get(key, PALETTES["dark"])


def esc(s):
    """XML-escape a string for safe embedding in SVG."""
    return sax.escape(s, {'"': "&quot;"})


# --------------------------------------------------------------------------
# starfield & card background
# --------------------------------------------------------------------------
STARS = [
    (24, 30, 1.4), (47, 74, 1.1), (72, 28, 1.5), (95, 58, 1.2), (121, 88, 1.0),
    (148, 42, 1.3), (172, 70, 1.1), (196, 32, 1.5), (221, 64, 1.2), (247, 24, 1.0),
    (269, 82, 1.4), (294, 46, 1.1), (318, 26, 1.5), (343, 76, 1.2), (369, 52, 1.0),
    (394, 34, 1.4), (419, 72, 1.1), (445, 28, 1.5), (471, 60, 1.2), (495, 40, 1.0),
    (522, 78, 1.4), (546, 30, 1.1), (572, 64, 1.5), (597, 44, 1.2), (622, 34, 1.0),
    (34, 116, 1.0), (88, 108, 1.3), (141, 122, 1.1), (197, 106, 1.4), (252, 118, 1.0),
    (307, 108, 1.3), (364, 124, 1.1), (421, 104, 1.4), (478, 120, 1.0), (536, 110, 1.3),
    (596, 122, 1.1), (26, 164, 1.2), (79, 150, 1.0), (131, 174, 1.3), (186, 158, 1.1),
    (240, 170, 1.2), (296, 152, 1.0), (351, 176, 1.3), (406, 162, 1.1), (462, 172, 1.2),
    (518, 156, 1.0), (574, 168, 1.3), (622, 150, 1.1), (31, 210, 1.1), (83, 224, 1.4),
    (138, 206, 1.0), (193, 222, 1.2), (248, 210, 1.1), (303, 226, 1.4), (358, 208, 1.0),
    (413, 224, 1.2), (468, 212, 1.1), (524, 228, 1.4), (578, 214, 1.0), (631, 220, 1.2),
    (28, 262, 1.3), (82, 278, 1.1), (136, 260, 1.2), (191, 276, 1.0), (246, 264, 1.3),
    (301, 280, 1.1), (356, 262, 1.2), (411, 278, 1.0), (466, 266, 1.3), (521, 282, 1.1),
    (576, 264, 1.2), (631, 278, 1.0), (35, 316, 1.0), (89, 330, 1.2), (144, 318, 1.1),
    (199, 332, 1.3), (254, 320, 1.0), (309, 334, 1.2), (364, 322, 1.1), (419, 336, 1.3),
    (474, 324, 1.0), (529, 338, 1.2), (584, 326, 1.1), (37, 372, 1.2), (92, 388, 1.0),
    (147, 376, 1.3), (202, 390, 1.1), (257, 378, 1.2), (312, 392, 1.0), (367, 380, 1.3),
    (422, 394, 1.1), (477, 382, 1.2), (532, 396, 1.0), (587, 384, 1.3),
]


def starfield(pal, w, h):
    """Star-dot field sized to (w, h), in palette color."""
    dots = []
    for x, y, r in STARS:
        if x < w - 4 and y < h - 4:
            dots.append('<circle cx="%d" cy="%d" r="%g" fill="%s" opacity="%s"/>' % (x, y, r, pal["star"], pal["star_op"]))
    return "".join(dots)


def card_bg(pal, w, h):
    """Full background: vertical gradient + starfield + subtle inner glow."""
    return (
        '<defs>'
        '<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/>'
        '</linearGradient>'
        '<radialGradient id="glow" cx="0.5" cy="0.5" r="0.75">'
        '<stop offset="0" stop-color="%s" stop-opacity="0.16"/>'
        '<stop offset="1" stop-color="%s" stop-opacity="0"/>'
        '</radialGradient>'
        '</defs>'
        '<rect width="%d" height="%d" fill="url(#bg)"/>'
        '<rect width="%d" height="%d" fill="url(#glow)"/>'
        '%s'
        '<rect x="0.5" y="0.5" width="%d" height="%d" fill="none" stroke="%s" stroke-width="1"/>'
        % (
            pal["bg_top"], pal["bg_bottom"],
            pal["gold"], pal["gold_top"] if "gold_top" in pal else pal["bg_top"],
            w, h, w, h,
            starfield(pal, w, h),
            w - 1, h - 1, pal["line"],
        )
    )


# --------------------------------------------------------------------------
# star tiering for impact-card (same across themes)
# --------------------------------------------------------------------------
TIERS = [
    ("S", 50000, "\u226550k\u2605", "#C9A86A", "#E4C87F"),
    ("A", 10000, "\u226510k\u2605", "#5B8DEF", "#8FB4F5"),
    ("B", 1000, "\u22651k\u2605", "#4EC9A0", "#7ED9B8"),
    ("C", 100, "\u2265100\u2605", "#B48AE8", "#C3A6EF"),
    ("D", 0, "<100\u2605", "#6E7893", "#B9C0CE"),
]

# GitHub-style language colors for tech-stack-card
LANGUAGE_COLORS = {
    "Python": "#3572A5", "TypeScript": "#3178C6", "JavaScript": "#F1E05A",
    "HTML": "#E34C26", "CSS": "#563D7C", "SCSS": "#C6538C", "Vue": "#41B883",
    "Java": "#B07219", "C": "#555555", "C++": "#F34B7D", "C#": "#178600",
    "Go": "#00ADD8", "Rust": "#DEA584", "Shell": "#89E051", "Markdown": "#083FA1",
    "Jupyter Notebook": "#DA5B0B", "PHP": "#4F5D95", "Ruby": "#701516",
    "Swift": "#F05138", "Kotlin": "#A97BFF", "Dart": "#00B4AB",
    "Dockerfile": "#384D54", "Makefile": "#427819", "Other": "#8B949E",
}


def lang_color(lang):
    return LANGUAGE_COLORS.get(lang, LANGUAGE_COLORS["Other"])
