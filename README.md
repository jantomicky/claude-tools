# claude-tools

General-purpose Claude Code skills, not tied to any stack or project.

## What's inside

| Skill | Purpose                                                                                                               |
|---|-----------------------------------------------------------------------------------------------------------------------|
| `tldr` | Shapes every response as an executable action, not prose. Lead with the answer, no filler.                            |
| `code-comments` | Language-agnostic no-comments rule (PHP, Python, YAML/Ansible, shell, JS/TS). A comment survives only if it captures a non-obvious WHY. |
| `recall` | Stores or resumes a `RECALL.md` so a fresh session (or crash/restart) can pick up without replaying the conversation. |
| `portadesign-palette` | Default color palette for visual work (Artifacts, mockups, diagrams), extracted from portadesign.cz. |

`tldr` and `code-comments` load automatically at every session start via a `SessionStart` hook (`hooks/hooks.json`) — no slash call needed.

A `PostToolUse` hook (`hooks/check-code-comments.py`) additionally scans every `Write`/`Edit` for comment lines that fail the WHY test and warns the agent. It never blocks an edit; PHPDoc blocks, Python docstrings and tooling directives (`# noqa`, `// eslint-disable`, ...) are ignored. Subagents inherit it, which `SessionStart` context does not.

## Installation

```
/plugin marketplace add jantomicky/claude-tools
/plugin install claude-tools@jantomicky
```

Update later:
```
/plugin marketplace update
/plugin update claude-tools
```

Bump `version` in `.claude-plugin/plugin.json` with every change you push. `/plugin update` compares versions, not content.
