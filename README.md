# claude-tools

General-purpose Claude Code skills, not tied to any stack or project.

## What's inside

| Skill | Purpose                                                                                                               |
|---|-----------------------------------------------------------------------------------------------------------------------|
| `tldr` | Shapes every response as an executable action, not prose. Lead with the answer, no filler.                            |
| `recall` | Stores or resumes a `RECALL.md` so a fresh session (or crash/restart) can pick up without replaying the conversation. |
| `portadesign-palette` | Default color palette for visual work (Artifacts, mockups, diagrams), extracted from portadesign.cz. |

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
