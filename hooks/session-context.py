#!/usr/bin/env python3
"""Inject the always-on skills, the workspace roots (and a HANDOFF.md notice) into a session or subagent.

Usage: session-context.py SessionStart|SubagentStart
"""
import json
import os
import re
import sys
from pathlib import Path

import workspace_boundary

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
ALWAYS_ON = ("tldr", "code-comments", "workspace-boundary")
READ_ONLY_AGENTS = {"Explore", "Plan", "claude-code-guide", "web-fetch", "statusline-setup", "pimcore-code:reviewer"}


def handoff_notice(source):
    if source not in ("startup", "clear"):
        return ""
    handoff = Path(os.environ.get("CLAUDE_PROJECT_DIR", ".")) / "HANDOFF.md"
    if not handoff.is_file():
        return ""
    match = re.search(r"(?:Written|Version)\W*:?\**\s*(.+)$", handoff.read_text(errors="replace"), re.MULTILINE)
    written = match.group(1).strip() if match else "unknown date"
    return f"\n\nHANDOFF.md exists in the project root (Written: {written}). Follow the handoff skill."


def main():
    event = sys.argv[1] if len(sys.argv) > 1 else "SessionStart"
    try:
        payload = json.load(sys.stdin)
    except ValueError:
        payload = {}
    if not isinstance(payload, dict):
        payload = {}
    source = payload.get("source", "startup")
    names = ALWAYS_ON
    if event == "SubagentStart" and payload.get("agent_type") in READ_ONLY_AGENTS:
        names = tuple(name for name in ALWAYS_ON if name != "code-comments")
    skills = "\n\n".join(
        (PLUGIN_ROOT / "skills" / name / "SKILL.md").read_text().split("---\n", 2)[2].strip() for name in names
    )
    roots = ", ".join(workspace_boundary.workspace_roots(payload.get("cwd") or os.getcwd()))
    context = skills + f"\n\nWorkspace roots: {roots}." + (handoff_notice(source) if event == "SessionStart" else "")
    json.dump({"hookSpecificOutput": {"hookEventName": event, "additionalContext": context}}, sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
