# claude-tools

General-purpose Claude Code skills, hooks, and an output style, not tied to any stack or project.

## Skills

| Skill | Purpose |
|---|---|
| `tldr` | Shapes every response as an action, not prose. Answer first, no filler. |
| `code-comments` | No explanatory comments in any language. A comment survives only if it captures a non-obvious WHY. |
| `recall` | Writes or resumes a `RECALL.md` so a fresh session picks up without replaying the conversation. |
| `portadesign-palette` | Default color palette for visual work (Artifacts, mockups, diagrams), extracted from portadesign.cz. |

## Hooks and output style

| Piece | Effect |
|---|---|
| `SessionStart` | Loads `tldr` and `code-comments`. Flags an existing `RECALL.md`. |
| `SubagentStart` | Loads `tldr` and `code-comments` into every subagent. |
| `UserPromptSubmit` | Reminds the agent to follow `tldr` on every prompt, so it doesn't fade in long sessions. |
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
