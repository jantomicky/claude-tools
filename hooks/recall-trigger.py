#!/usr/bin/env python3
"""UserPromptSubmit: when the prompt says "recall", force the recall skill before anything else.

Matches the bare word and its Czech case endings (recallu, recallem), not "recalled" or "recalling".
"""
import json
import re
import sys

DIRECTIVE = (
    "The user wrote \"recall\": invoke the claude-tools:recall skill as your first action this turn, then write"
    " RECALL.md in the project root (or read it, if asked to load it). No auto-memory, no reminder or background"
    " task, no clarifying question, no alternatives. Ignore this only when the word is plainly the English verb or"
    " the metric."
)


def main():
    try:
        prompt = json.load(sys.stdin).get("prompt") or ""
    except (ValueError, AttributeError):
        return 0
    if re.search(r"\brecall(u|em|y)?\b", prompt, re.IGNORECASE):
        json.dump({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": DIRECTIVE}}, sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
