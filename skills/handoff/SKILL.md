---
name: handoff
description: Write or resume from HANDOFF.md in the project root, a clean-context brief for a fresh session, another machine or another person. Invoke when the user says "handoff" in any language, asks to hand off, wrap up or save context for a new session, before a destructive action, and at session start when HANDOFF.md exists. Never auto-memory.
---

# Handoff

Write `HANDOFF.md` in the project root: a brief that lets a session with an empty context continue the work. It is
not a transcript backup. `claude --continue`, `claude --resume` and `/restart` already restore the full conversation,
so a handoff earns its place only where they cannot: after `/clear`, on another machine, for another person or tool,
or when a long, compacted conversation should be traded for a clean context.

## When to use

1. **Handoff request.** User says "handoff", or asks to hand off or save context for a new session. Write it, do not
   ask. Discussing the skill itself is not a request.
2. **Restart or break.** User is restarting, stepping away or done for today. Do not write; say in one line that
   `/restart` or `claude --continue` resumes this conversation. Write only if they want a clean context or another
   machine.
3. **Before a destructive or hard-to-reverse action.** Write it first.
4. **Session start with `HANDOFF.md` present.** State its age from the `Written` line and ask before reading
   ("Handoff from 6 days ago (2026-08-05). Read it?"). After reading, delete it and say so.
5. **Before a commit with `HANDOFF.md` present.** Leave it out unless the user wants it committed.

## Contents

1. **Written**: current date and time (`Written: 2026-08-11 14:32`).
2. **Branch and task**: `git branch --show-current` and the task in one line.
3. **Goal and context**: what done looks like, in one paragraph a newcomer understands.
4. **Decisions**: confirmed choices and rejected alternatives, with the reason, so they are not re-litigated.
5. **Next**: an ordered checklist of concrete actions, open questions for the user, and conventions a fresh
   session would get wrong.

## How to write it

1. Scan the whole conversation. An earlier confirmed decision outranks a recent aside.
2. Verify state with tools (`git status`, file reads), not memory.
3. Leave out what `git log`, the diff, `CLAUDE.md` or the code already say. Point at paths instead.
4. Write prose in the project's working language. Keep code and commands verbatim.
5. If `HANDOFF.md` exists, read it and replace it. Flag it if its branch differs from the current one.
