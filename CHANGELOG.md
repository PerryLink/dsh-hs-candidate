# Changelog

## [0.1.0-alpha.13] — 2026-11-01

### Security / Fixes

- Release configuration hardening: wider host peer range and a build step before publish.


### Added

- `hs.rvc_report`: regional value content under the three rules-of-origin formulas (simple ratio, build-down, build-up) with a threshold verdict. Verified by `node --test test/*.test.mjs` (11/11).

## [Unreleased]

### Added

- `hs.code_check`: structural check of an HS 2022 code — 2/4/6/8/10 digits, chapter 01-97, 98/99 reserved, dot-insensitive normalisation with distinct error codes. Read-only; it does not assert classification correctness. Verified by `node --test test/*.test.mjs` (7/7).

## [0.1.0-alpha.8] — 2026-11-01

### Changed

- Documentation: five-language fixture/acceptance links now resolve on npm; added specific related-checker/tool links.
- Marketplace metadata: taxonomy category, archetype, domains and status; docs page now shows the same.

All notable changes to `dsh-hs-candidate` are documented here. The format follows Keep a Changelog; this project uses alpha versions.

## [0.1.0-alpha.7] — 2026-11-01

### Added

- Five-language READMEs: English, 简体中文, Español, Português, हिन्दी.
- Local workflow SVG at `docs/assets/dsh-hs-candidate-flow.svg`.
- Family cross-links (domain index, checker family, `dsh-kit`), compatibility, permissions, and related-work sections.
- Standard repository files: `SECURITY.md`, `PRIVACY.md`, `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, and `icon.svg`.

### Changed

- README aligned with the PerryLink DSH checker/plugin family style; package remains public/synthetic, alpha, not GA.

### Maintenance

- 2026-11-01: active again — feature work, hardening and fresh evidence resumed.

## [Earlier]

Earlier alpha builds are available from npm and GitHub Releases; this file starts at the family-standard documentation wave.
