---
name: recall
description: Write or resume from a RECALL.md that captures session context, key decisions, current state, open TODOs, and a summary of the last messages, so a fresh session or another person can resume without replaying the conversation. Invoke when the user asks to hand off, wrap up, save context, or continue elsewhere. Also invoke proactively before a destructive or hard-to-reverse action, when the user signals an interruption (restart, stepping away, ending for the day), or at the start of a session when a RECALL.md is found in the project root.
---

# Recall

Write `RECALL.md` in the project root. Lets a fresh session pick up exactly where this one left off, without
replaying the transcript.

## When to use

- User asks to hand off, save, store, or wrap up context before a task passes to another agent or session.
- Proactively, in the background once every few minutes. Inform the user that RECALL.md is being updated.
- Proactively, on an explicit interruption signal. The user states or implies they're about to be interrupted
  ("stepping away", "restarting my machine", "done for today"). Offer to save, triggered by the stated intent,
  not a guess.
- Session start: if `RECALL.md` exists and hasn't been read yet this session, surface it. Don't read it silently
  and don't ignore it. State its age from the `Version` line and ask before reading, e.g. "There's a RECALL
  file from 6 days ago (2026-08-05). Want me to read it?" No fixed staleness threshold. Let the user decide.
  After reading it, delete it. Don't ask, don't keep it "just in case" — its context is loaded, and a stale
  RECALL.md misleads the next session. State that you deleted it. Write a fresh one later if the session needs
  another handoff.
- Before a commit: if `RECALL.md` exists, flag it to the user and ask whether to include it in the commit or
  leave it out. Don't decide silently either way.

## Contents

1. **Version**: actual current ISO date and time (e.g. `Version: 2026-08-11 14:32`), not a placeholder.
2. **Feature/branch**: output of `git branch --show-current`, plus a short feature/task name, one line.
3. **What this is**: one paragraph, zero assumed context.
4. **Key decisions already made**: confirmed choices, especially ones likely to get re-litigated if lost.
5. **Current state**: verified with actual checks (`git status`, `ls`, read the file), not asserted from memory.
6. **Open TODOs**: ordered checklist, each item concrete enough to act on directly.
7. **Conventions/constraints**: anything a fresh session would get wrong by default (language, style, things
   NOT to do).
8. **Last messages**: condensed summary of the most recent exchange (default: last 5), enough to explain why
   the state is what it is, not a verbatim transcript.

## How to build the file

1. Scan the whole conversation for decisions and corrections, not just the last few messages. A confirmed
   choice from earlier outranks a recent aside.
2. Verify current state with tools rather than trusting recollection of what was done.
3. Keep it short. Use bullets over paragraphs. Skip anything derivable from `git log` or the code itself.
4. Match the project's working language for prose. Keep code and commands verbatim.
5. If a `RECALL.md` already exists, read it first. Update or replace it rather than appending a second
   narrative. If the branch has changed since that file was written, flag it instead of silently overwriting.
