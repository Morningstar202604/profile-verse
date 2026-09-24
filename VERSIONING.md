# Versioning

Profile Verse follows [Semantic Versioning](https://semver.org/): `MAJOR.MINOR.PATCH`.

## Version of record

- `core/theme.py` exports `VERSION` — the design system version, stamped in
  every card footer (`<name>-card · vX.Y.Z`).
- Git tags are the release of record: `vX.Y.Z`.
- `CHANGELOG.md` documents each release.

## How a release happens

1. Bump `VERSION` in `core/theme.py`.
2. Update the `· vX.Y.Z` footer literal in **every** component generator
   (`grep -l "· v" components/*/generate_*.py` must match all 8, plus
   `components/impact-card/card_template.svg.tpl`).
3. Regenerate all previews (dark + light) and validate XML.
4. Commit → tag `vX.Y.Z` → move the `vX` alias tag to the same commit → push.

## Reference rules for users

| Reference | Meaning | Use case |
| --- | --- | --- |
| `@main` | rolling edge, always latest | trying new features |
| `@v1` | **recommended** — latest of major v1, gets minor/patch fixes automatically | production profiles |
| `@v1.1.0` | pinned exact version | reproducible builds / showcase |

`@v1` is a lightweight alias tag moved on every minor/patch release of major 1.
`@main` should not be used where stability matters (previews in READMEs of
profiles that visitors see daily are fine with `@main` since GitHub Actions
pins the checked-out repo, but pinning `@v1` is always safer).

## Component versioning

- Components have no independent version field; the repo version is the suite
  version. A breaking change to a single component bumps `MAJOR` (e.g. v2.0.0).
- `action.yml` files intentionally contain no version — the `@tag` on `uses:`
  is the version.
- Forks / subtrees keep their own version lineage after split.
