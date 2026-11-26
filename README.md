# claude-tools

General-purpose Claude Code skills, hooks, and an output style, not tied to any stack or project.

## Skills

| Skill | Purpose |
|---|---|
| `tldr` | Shapes every response as an action, not prose. Answer first, no filler. Hook-injected, not model-invoked. |
| `code-comments` | No explanatory comments in any language. A comment survives only if it captures a non-obvious WHY. Hook-injected, not model-invoked. |
| `workspace-boundary` | Keeps file access inside the workspace: the project root and the folder above it. Documents, Downloads and system files need an explicit request; secrets (keys, keychain, tokens) are off limits. Hook-injected, not model-invoked. |
| `handoff` | Writes or resumes a `HANDOFF.md`, a clean-context brief for `/clear`, another machine or person. Same-machine restarts use `/restart` or `--continue`. |
| `portadesign-palette` | Default color palette for visual work (Artifacts, mockups, diagrams), extracted from portadesign.cz. |

## Hooks and output style

| Piece | Effect |
|---|---|
| `SessionStart` | Loads `tldr`, `code-comments` and `workspace-boundary` with the resolved workspace roots. Flags an existing `HANDOFF.md` on startup and `/clear`, not on resume or compact. |
| `SubagentStart` | Loads `tldr` and `workspace-boundary` into every subagent, `code-comments` only into those that can write code. |
| `UserPromptSubmit` | Reminds the agent to follow `tldr` on every prompt, so it doesn't fade in long sessions. `handoff-trigger.py` points the agent at the `handoff` skill when the prompt says "handoff". |
| `PreToolUse` | `workspace_boundary.py` denies a `Read`, `Edit`, `Write`, `Glob`, `Grep` or `Bash` call that touches a secret and makes the user confirm any other call that reaches outside the workspace. Never auto-allows. |
| `PostToolUse` | `check-code-comments.py` warns (never blocks) on `Write`/`Edit` comments that fail the WHY test. |
| `TLDR` output style | Applied automatically while the plugin is enabled (`force-for-plugin`). No `/config` step. |

## Workspace boundary

The workspace is the project root plus the folder directly above it (`~/Code` for `~/Code/my-project`). The parent
does not count when it is the home folder, a protected folder (`~/Documents`, `~/Downloads`, `~/Desktop`,
`~/Library`, `~/.ssh`, `~/.config` and similar) or a system folder. Temp folders and `~/.claude` are always inside.

Add roots in `settings.json`, either `permissions.additionalDirectories` or a `:`-separated list:

```json
{ "env": { "CLAUDE_WORKSPACE_ROOTS": "~/work:~/oss" } }
```

The hook has two tiers:

1. **Secrets, denied.** SSH and GPG keys (`~/.ssh/config`, `known_hosts` and `*.pub` only ask), keychains and the
   `security` command, browser, Mail and Messages data, shell history, CLI token files (`~/.aws/credentials`,
   `~/.npmrc`, `~/.netrc`, `~/.config/gh/hosts.yml` and similar) and token-printing commands (`gh auth token`).
   No prompt and no override: an explicit request can come from a planted README.
2. **Everything else outside, confirmed by the user.** File tools ask for every outside path. `Bash` asks for the
   home folder and for system paths on this machine that exist or that the call could create. A binary called by
   absolute path stays quiet, and so does whatever runs in a container or on another host (`docker exec`,
   `docker run`, `kubectl exec`, `ssh`). It also asks for `sudo`, app control (`osascript`) and global installs.

`Bash` is parsed heuristically and MCP tools are covered by the skill only, so the hook is a guardrail, not a
sandbox. `scripts/test_workspace_boundary.py` is the regression suite; `scripts/lint.py` runs it.

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
