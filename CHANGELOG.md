# Changelog

All notable changes to Profile Verse are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/).
Versioning follows [Semantic Versioning](https://semver.org/lang/zh-CN/).

## [1.2.0] - 2026-09-24

### Added
- **year-review-card** — the 9th component: a golden annual ring (12 month-stars
  sized/brightened by real monthly contributions, halo on the peak month), the
  year's total glowing at the center, and four star-medals (peak month / longest
  streak / merged PRs / top language). Data from the 365-day contribution
  calendar + merged PRs + repo languages.
- Showcase walls rebuilt to 9 cards (dark + light).
- update.yml now refreshes **all 18 previews** (9 cards × dark/light) daily.

## [1.1.0] - 2026-09-24

### Added
- **Gold brocade texture layer** (`filigree()` in `core/theme.py`) — fine diamond lattice under the starfield, low opacity, on every card in both themes.
- **Inner hairline frame** (double-border framing) on all cards.
- **Corner diamond studs** inside the four gold L-shaped corner marks.
- **Semantic version footer** on every card (`banner-card · v1.1.0` … `impact-card · v1.1.0`).
- `core/theme.py` exports `VERSION` as the single design-system version source.
- `VERSIONING.md` — official release & reference rules (`@v1`, `@v1.1.0`, `@main`).
- `examples/profile-verse.yml` — copy-paste whole-homepage workflow.
- `assets/showcase/wall-dark.png` / `wall-light.png` — dual-theme showcase walls.
- CI workflow `.github/workflows/ci.yml` — regenerates all 16 previews + XML validation on every push/PR.

### Changed
- README rewritten (English primary) + README.zh.md, hero image, comparison table, badges.
- Repo metadata: description, homepage (live demo), 8 search topics.

## [1.0.0] - 2026-09-24

First stable release of the monorepo suite.

### Added
- 8 components: `impact-card`, `stats-card`, `streak-card`, `typing-card`,
  `contrib-grid-card`, `tech-stack-card`, `banner-card`, `badge-card`.
- Shared design system `core/`: GitHub API layer, contribution calendar,
  star tiers, dual-theme palettes (dark / light).
- 3-stop sky gradient, gold/blue nebulas, film grain, 4-ray sparkles,
  gradient numbers, gold corner ticks.
- GitHub Actions `action.yml` per component — zero-server generation.
- Daily auto-refresh workflow `update.yml` for the 16 previews.
- `git subtree split`-ready monorepo layout ("先合后拆").
- Live demo on [Morningstar202604 homepage](https://github.com/Morningstar202604/Morningstar202604).

[1.2.0]: https://github.com/Morningstar202604/profile-verse/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/Morningstar202604/profile-verse/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/Morningstar202604/profile-verse/releases/tag/v1.0.0
