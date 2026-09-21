---
name: recall
description: Write or resume from a RECALL.md (context, decisions, state, TODOs, last messages) so a fresh session or another person can resume without replaying the conversation. Invoke when the user asks to hand off, wrap up, or save context; proactively before a destructive action or when the user signals an interruption; at session start when RECALL.md exists in the project root; and whenever the user says "recall" in any language ("ulož recall", "načti recall", "save recall"). The word always means RECALL.md, never auto-memory.
---

# Recall

Write `RECALL.md` in the project root so a fresh session resumes where this one stopped.

"Recall" means this file, not the auto-memory directory. Never save a recall as memory entries: a fresh session
looks for `RECALL.md` and reports nothing found.

## When to use

1. **Handoff request.** User asks to hand off, save, or wrap up context.
2. **Interruption signal.** User says they're stepping away, restarting, or done for today. Offer to save.
3. **Before a destructive or hard-to-reverse action.** Save first.
4. **Session start with `RECALL.md` present.** State its age from the `Version` line and ask before reading
   ("RECALL from 6 days ago (2026-08-05). Read it?"). After reading, delete it without asking and say so.
5. **Before a commit with `RECALL.md` present.** Ask whether to commit it or leave it out.

## Contents

1. **Version**: real current date and time (`Version: 2026-08-11 14:32`).
2. **Branch and task**: `git branch --show-current` plus a one-line task name.
3. **Context**: one paragraph, zero assumed knowledge.
4. **Decisions**: confirmed choices, especially ones likely to be re-litigated.
5. **State and TODOs**: state verified with tools (`git status`, file reads); an ordered checklist of concrete
   next actions; conventions a fresh session would get wrong; a summary of the last ~5 messages.

## How to write it

1. Scan the whole conversation. An earlier confirmed decision outranks a recent aside.
2. Verify state with tools, not memory.
3. Use bullets. Skip anything derivable from `git log` or the code.
4. Write prose in the project's working language. Keep code and commands verbatim.
5. If `RECALL.md` exists, read it and replace it. Flag it if its branch differs from the current one.
