#!/usr/bin/env python3
"""UserPromptSubmit: when the prompt says "handoff", point the agent at the handoff skill.

Matches "handoff", "hand-off" and Czech case endings (handoffu, handoffem, handoffy).
"""
import json
import re
import sys

DIRECTIVE = (
    "The user wrote \"handoff\". If they ask to write or load one, invoke the claude-tools:handoff skill first and"
    " write or read HANDOFF.md in the project root: no auto-memory, no reminder, no clarifying question. If they only"
    " discuss the skill or the word, answer normally."
)


def main():
    try:
        prompt = json.load(sys.stdin).get("prompt") or ""
    except (ValueError, AttributeError):
        return 0
    if re.search(r"\bhand-?off(u|em|y|ů)?\b", prompt, re.IGNORECASE):
        json.dump({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": DIRECTIVE}}, sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
