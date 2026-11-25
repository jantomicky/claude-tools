#!/usr/bin/env python3
"""Consistency gate for the plugin. Run from the repo root: python3 scripts/lint.py

Checks what drifts in practice: broken JSON or frontmatter, a description over budget, a skill missing from the
README, a hook pointing at a missing script, a workspace-boundary regression, a change without a version bump and
changelog entry.
"""
import glob
import json
import os
import re
import subprocess
import sys

failures = []


def check(name, ok, detail=""):
    if not ok:
        failures.append(name)
        print(f"FAIL {name}" + (f" :: {detail[:400]}" if detail else ""))


def frontmatter(text):
    """Top-level keys of a YAML frontmatter block; folded (`>`, `|`) and indented continuation lines are joined."""
    fields, key = {}, None
    for line in text.split("---\n")[1].splitlines():
        match = re.match(r"^([\w-]+):\s*(.*)$", line)
        if match:
            key, value = match.groups()
            fields[key] = "" if value in (">", "|", ">-", "|-") else value.strip().strip('"')
        elif key and line.startswith((" ", "\t")):
            fields[key] = (fields[key] + " " + line.strip()).strip()
        elif line.strip():
            raise ValueError(f"unparsable frontmatter line: {line!r}")

    return fields


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True)


def version_bumped(version):
    base = git("merge-base", "HEAD", "origin/main").stdout.strip()
    if not base:
        return True
    changed = git("diff", "--name-only", base, "--", ".").stdout.split()
    changed += git("ls-files", "--others", "--exclude-standard").stdout.split()
    if not changed:
        return True
    base_manifest = git("show", f"{base}:.claude-plugin/plugin.json").stdout

    return not base_manifest or json.loads(base_manifest)["version"] != version


def main():
    for path in (".claude-plugin/plugin.json", "hooks/hooks.json"):
        try:
            json.load(open(path))
        except ValueError as error:
            check(f"{path} is valid JSON", False, str(error))

    readme = open("README.md").read()
    for path in sorted(glob.glob("skills/*/SKILL.md")):
        skill = os.path.basename(os.path.dirname(path))
        try:
            meta = frontmatter(open(path).read())
        except (ValueError, IndexError) as error:
            check(f"{path} has parsable frontmatter", False, str(error))
            continue
        check(f"{path} name matches its directory", meta.get("name") == skill)
        description = str(meta.get("description") or "")
        check(f"{path} has a description", bool(description))
        words = len(description.split())
        check(f"{path} description stays under 60 words", words < 60, f"{words} words")
        check(f"README lists skill {skill}", f"| `{skill}` |" in readme)

    events = json.load(open("hooks/hooks.json"))["hooks"]
    for event, groups in events.items():
        for hook in (hook for group in groups for hook in group["hooks"]):
            target = re.search(r'\$CLAUDE_PLUGIN_ROOT/([^"]+)', hook["command"])
            if target:
                check(f"{event} hook points at an existing script", os.path.exists(target.group(1)), hook["command"])
        check(f"README documents the {event} hook", f"| `{event}` |" in readme)

    suite = subprocess.run([sys.executable, "scripts/test_workspace_boundary.py"], capture_output=True, text=True)
    check("workspace boundary regression suite passes", suite.returncode == 0, suite.stdout + suite.stderr)

    version = json.load(open(".claude-plugin/plugin.json"))["version"]
    entries = re.findall(r"^## \[(\S+)\]", open("CHANGELOG.md").read(), re.M)
    check("plugin.json version matches the newest changelog entry", entries and version == entries[0],
          f"{version} vs {entries[:1]}")
    check("changelog versions are unique", len(entries) == len(set(entries)))
    check("a change since origin/main bumps the version", version_bumped(version), version)

    print(f"{len(failures)} failed")

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
