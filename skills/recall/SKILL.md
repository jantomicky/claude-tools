---
name: recall
description: Write or resume from a RECALL.md that captures session context, key decisions, current state, open TODOs, and a summary of the last messages, so a fresh session or another person can resume without replaying the conversation. Invoke when the user asks to hand off, wrap up, save context, continue elsewhere — proactively before a destructive/hard-to-reverse action or when the user signals an interruption (restart, stepping away, ending for the day) — or at the start of a session when a RECALL.md is found in the project root.
---

# Recall

Produce one file, `RECALL.md` in the project root, that lets a fresh session pick up exactly where this one left off —
without reading the full transcript.

## When to use

- User asks to hand off, save context, wrap up, or continue in a new session/by someone else
- Before a task passes to another agent or session
- **Proactively, before a destructive/hard-to-reverse action** — same category as the `tldr` skill's
  "Destructive/hard-to-reverse action: confirm first" rule (force-push, `reset --hard`, dropping data, etc.) — ask
  whether to save first, don't block on it if declined
- **Proactively, on an explicit interruption signal** — user states or implies they're about to be interrupted (e.g.
  "musím pryč", "restartuju stroj", "končím na dnes") — offer to save, triggered by the stated intent, not a guess
- **Session start**: if `RECALL.md` exists in the project root and hasn't been read yet this session, don't read it
  silently and don't ignore it either — mention its age from the `Last saved` line (e.g. "poslední záznam je z
  2026-08-05, 6 dní starý") and ask the user first, e.g. "Vidím, že existuje RECALL soubor ze 6 dní, mám jej přečíst?"
  (match their language). Read it only after they confirm. There is no fixed staleness threshold — surface the age
  and let the user judge.
- Not a permanent doc: note at the top of the file that it should be deleted or folded into README/CLAUDE.md once read

## Contents

1. **Last saved** — ISO date and time this file was written (e.g. `Last saved: 2026-08-11 14:32`), so a later session
   can judge staleness at a glance
2. **Feature/branch** — the git branch the work belongs to (`git branch --show-current`), plus the feature/task name in
   one line
3. **What this is** — one paragraph, zero assumed context
4. **Key decisions already made** — confirmed choices, especially ones likely to get re-litigated if lost
5. **Current state** — verified with actual checks (`git status`, `ls`, read the file), not asserted from memory
6. **Open TODOs** — ordered checklist, each item concrete enough to act on directly
7. **Conventions/constraints** — anything a fresh session would get wrong by default (language, style, things NOT to do)
8. **Last messages** — condensed summary of the most recent exchange (default: last 5), enough to explain *why* the
   state is what it is — not a verbatim transcript

## How to build it

1. Scan the whole conversation for decisions and corrections, not just the literal last N messages — a confirmed choice
   from earlier outranks a recent aside
2. Verify current state with tools rather than trusting recollection of what was done
3. Put the actual current date/time on the `Last saved` line — don't leave a placeholder
4. Run `git branch --show-current` and put the result (plus a short feature name) right after — a fresh session should
   know which branch this recall belongs to before reading anything else
5. Keep it short: bullets over paragraphs, nothing derivable from `git log` or the code itself
6. Match the project's working language for prose; keep code/commands verbatim
7. If a `RECALL.md` already exists, read it first — update/replace rather than appending a second narrative; if the
   branch has changed since that file was written, flag it instead of silently overwriting
