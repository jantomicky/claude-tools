#!/usr/bin/env python3
"""UserPromptSubmit: when the prompt says "recall", force the recall skill before anything else."""
import json
import re
import sys

DIRECTIVE = (
    "The user wrote \"recall\". This means the claude-tools:recall skill and RECALL.md in the project root, nothing"
    " else. Invoke the claude-tools:recall skill as your first action this turn, then write (or read, if the user"
    " asked to load it) RECALL.md. Do not save to auto-memory, do not schedule a reminder or background task, do"
    " not ask what they mean, do not offer alternatives."
)


def main():
    try:
        prompt = json.load(sys.stdin).get("prompt", "")
    except (json.JSONDecodeError, AttributeError):
        return 0
    if re.search(r"recall", prompt, re.IGNORECASE):
        json.dump({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": DIRECTIVE}}, sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
