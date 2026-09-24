# Contributing to Profile Verse

Thanks for wanting to make Profile Verse better. Every card here follows the same rules — please read this before opening a PR.

## What we welcome

- **New card ideas** (a signature shape + real GitHub data) — open an issue with a rough sketch first.
- **Theme refinements** — palette changes live in `core/theme.py` (both `dark` and `light` must stay in sync).
- **Bug reports** — include the generated SVG (or a screenshot), the `generate_*.py` version, and what you expected vs. saw.
- **Docs & examples** — typos, better quickstart YAML, localization.

## Ground rules

1. **One glance, one signature.** Every card must have a distinctive shape. No clones of existing cards, no snake.
2. **Both themes, always.** Any change must render correctly in `dark` and `light` — add both previews.
3. **Real data only.** Never fake numbers. Data flows through `core/github.py`; cards stamp source + update time.
4. **No servers, no cost.** Cards are pure SVG + SMIL generated in GitHub Actions. No external services, no runtime API calls from the card itself.
5. **Deterministic output.** `generate_*.py` must produce the same SVG for the same input — no timestamps in the card body (only the stamped refresh date), no randomness in layout.
6. **480px rule.** Cards are ~640×N px, big numbers, few words, room to breathe.

## Development workflow

Each component lives in `components/<name>/` and is self-contained:

```
components/<name>/
├── generate_<name>.py   # builds the SVG (reads core/theme.py, core/github.py)
├── action.yml           # GitHub Action inputs
├── README.md            # per-component usage
└── preview/             # <name>.svg + <name>-light.svg (daily auto-refreshed)
```

```bash
# regenerate one card (dark and light)
GH_TOKEN=your_token USER=your_username THEME=dark  OUTPUT=components/x/preview/x.svg  python3 components/x/generate_x.py
GH_TOKEN=your_token USER=your_username THEME=light OUTPUT=components/x/preview/x-light.svg python3 components/x/generate_x.py

# validate the SVG XML
python3 -c "import xml.dom.minidom,sys; xml.dom.minidom.parse('components/x/preview/x.svg'); print('xml ok')"
```

When adding a card, also wire it into `examples/profile-verse.yml` (and the README gallery).

## PR checklist

- [ ] Card renders in **both** themes (verified, not assumed)
- [ ] SVG XML parses cleanly
- [ ] Data is real and stamped with source + update time
- [ ] README gallery entry added (dark + light previews)
- [ ] No server / external service introduced

## Code of conduct

Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). Be kind; this is a hobby-scale open-source project.
