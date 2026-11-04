# claude-tools

General-purpose Claude Code skills, hooks, and an output style, not tied to any stack or project.

## Skills

| Skill | Purpose |
|---|---|
| `tldr` | Shapes every response as an action, not prose. Answer first, no filler. |
| `code-comments` | No explanatory comments in any language. A comment survives only if it captures a non-obvious WHY. |
| `handoff` | Writes or resumes a `HANDOFF.md`, a clean-context brief for `/clear`, another machine or person. Same-machine restarts use `/restart` or `--continue`. |
| `portadesign-palette` | Default color palette for visual work (Artifacts, mockups, diagrams), extracted from portadesign.cz. |

## Hooks and output style

| Piece | Effect |
|---|---|
| `SessionStart` | Loads `tldr` and `code-comments`. Flags an existing `HANDOFF.md` on startup and `/clear`, not on resume or compact. |
| `SubagentStart` | Loads `tldr` and `code-comments` into every subagent. |
| `UserPromptSubmit` | Reminds the agent to follow `tldr` on every prompt, so it doesn't fade in long sessions. `handoff-trigger.py` points the agent at the `handoff` skill when the prompt says "handoff". |
| `PostToolUse` | `check-code-comments.py` warns (never blocks) on `Write`/`Edit` comments that fail the WHY test. |
| `TLDR` output style | Applied automatically while the plugin is enabled (`force-for-plugin`). No `/config` step. |

## Installation

```
/plugin marketplace add jantomicky/claude-tools
/plugin install claude-tools@jantomicky
```

Update:

```
/plugin marketplace update
/plugin update claude-tools
```
