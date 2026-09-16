#!/usr/bin/env python3
"""Inject the always-on skills (and a RECALL.md notice) into a session or subagent.

Usage: session-context.py SessionStart|SubagentStart
"""
import json
import os
import re
import sys
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
ALWAYS_ON = ("tldr", "code-comments")


def recall_notice():
    recall = Path(os.environ.get("CLAUDE_PROJECT_DIR", ".")) / "RECALL.md"
    if not recall.is_file():
        return ""
    match = re.search(r"Version\W*:?\**\s*(.+)$", recall.read_text(errors="replace"), re.MULTILINE)
    version = match.group(1).strip() if match else "unknown date"
    return f"\n\nRECALL.md exists in the project root (Version: {version}). Follow the recall skill."


def main():
    event = sys.argv[1] if len(sys.argv) > 1 else "SessionStart"
    skills = "\n\n".join(
        (PLUGIN_ROOT / "skills" / name / "SKILL.md").read_text() for name in ALWAYS_ON
    )
    context = skills + (recall_notice() if event == "SessionStart" else "")
    json.dump({"hookSpecificOutput": {"hookEventName": event, "additionalContext": context}}, sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
