# Changelog

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versions follow
[Semantic Versioning](https://semver.org/).

## [0.5.1] - 2026-09-16

### Added

- `CHANGELOG.md` and a rule in `CLAUDE.md` to update it with every release.

## [0.5.0] - 2026-09-16

### Changed

- Tighten skill instructions.
- Inject skills into subagents.
- Force the TLDR output style.

## [0.4.0] - 2026-09-16

### Added

- TLDR output style.
- `tldr` reminder on every prompt.

## [0.3.0] - 2026-09-01

### Added

- `code-comments` skill.
- PostToolUse hook enforcing `code-comments`.

## [0.2.2] - 2026-08-30

### Fixed

- `recall`: delete `RECALL.md` after reading instead of asking.

## [0.2.1] - 2026-08-28

### Added

- SessionStart hook that loads the `tldr` skill automatically.

## [0.2.0] - 2026-08-28

### Added

- `portadesign-palette` skill.

## [0.1.0] - 2026-08-11

### Added

- Initial plugin with `tldr` and `recall` skills.
- `README.md` and `CLAUDE.md`.
