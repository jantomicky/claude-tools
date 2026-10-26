# Changelog

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versions follow
[Semantic Versioning](https://semver.org/).

## [0.10.0] - 2026-10-26

### Added

- `tldr`: rule 6, answer only what was asked, tangents get one `Separately: X` line.
- `tldr`: pre-send deletion of announcing openers, recap/offer closers, sidebars and empty hedges.

## [0.9.0] - 2026-10-26

### Changed

- `tldr`: findings are numbered plain lines (`01. ❌ ...`), numbered across the reply; icon definitions carry no label
  words.

## [0.8.2] - 2026-10-26

### Fixed

- `tldr`: icon definitions no longer pair the icon with its label word (`❌ issue`), which models copied into
  findings. Explicit ban on label words after the icon.

## [0.8.1] - 2026-10-23

### Changed

- `tldr`: findings lead with the icon alone, without the `issue`/`suggestion`/`question`/`praise` label word.

## [0.8.0] - 2026-10-13

### Changed

- `tldr`: word budget (~80 words, ~150 after multi-step work), results instead of process, no closing offers, no
  headers or tables in short replies, audits capped at the 5 most severe findings.
- `UserPromptSubmit` reminder and TLDR output style carry the budget, not just a pointer to the skill.

### Fixed

- `check-code-comments.py`: trailing comment after a string literal was reported cut off.

## [0.7.1] - 2026-10-13

### Changed

- `tldr` and the TLDR output style: review findings reach the user with their icon and label (❌ ⚠️ ❔ ✅), also
  when relayed from a subagent.

## [0.7.0] - 2026-09-28

### Changed

- `tldr`: 7 rules merged into 5, so the skill obeys its own list cap. Dropped the confirm-before-destructive
  exception; the harness already carries it.
- `code-comments`: the two keep sections merged into one, `When to use` dropped as a repeat of the description.
- `recall`: description cut from 82 to 52 words.
- `session-context.py` injects the skill bodies without their frontmatter: 456 to 318 words per session and per
  subagent.
- TLDR output style reduced to a pointer at the `tldr` skill plus the subagent-relay rule.
- `portadesign-palette`: `When to use` folded into the intro.

### Fixed

- `recall-trigger.py`: crashed on a `null` prompt; fired on "recalled" and "recalling". Now matches the word and its
  Czech case endings only, and lets the agent ignore the English verb and the metric.

### Removed

- `session-context.py`: the "recall means RECALL.md" sentence on every session start. The skill description and
  `recall-trigger.py` already say it.
- `check-code-comments.py`: duplicate `/**` branch.

## [0.6.0] - 2026-09-27

### Added

- `recall-trigger.py` `UserPromptSubmit` hook: any prompt containing "recall" forces the `recall` skill and forbids
  auto-memory or reminders. The skill description alone kept getting ignored.

## [0.5.2] - 2026-09-21

### Fixed

- `recall`: trigger on the word "recall" and forbid saving it as auto-memory, which left fresh sessions with no `RECALL.md`.

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
