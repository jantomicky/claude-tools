#!/usr/bin/env python3
"""Warn (never block) when a Write/Edit adds explanatory code comments.

Reads a PostToolUse hook payload on stdin, scans the text the tool wrote for line
comments that fail the WHY test, and emits them as additionalContext so the agent
can clean them up. PHPDoc blocks, Python docstrings and tooling directives are
left alone.
"""
import json
import re
import sys

HASH_LANGS = {".py", ".yml", ".yaml", ".sh", ".bash", ".zsh", ".rb", ".tf", ".toml", ".conf", ".ini"}
SLASH_LANGS = {".php", ".js", ".jsx", ".ts", ".tsx", ".go", ".java", ".c", ".cpp", ".h", ".rs", ".css", ".scss"}
SKIP_PATH = re.compile(r"/(vendor|node_modules|\.git|var/cache|dist|build)/")
DIRECTIVE = re.compile(
    r"(noqa|type:\s*ignore|fmt:\s*(on|off)|pylint|mypy|ruff|isort|black|coverage|pragma|eslint|ts-ignore|"
    r"ts-expect-error|prettier|phpcs|phpstan|psalm|codeCoverageIgnore|shellcheck|hadolint|yamllint|ansible-lint|"
    r"!/|-\*-|encoding:|region|endregion)",
    re.IGNORECASE,
)
MAX_REPORTED = 12
STRING_LITERAL = re.compile("'[^']*'" + '|"[^"]*"')


def strip_strings(line):
    return STRING_LITERAL.sub("''", line)


def trailing_comment(line, markers):
    bare = strip_strings(line)
    for marker in markers:
        index = bare.find(" " + marker)
        if index > 0 and bare[:index].strip():
            return line[index:].strip()
    return None


def added_text(payload):
    name = payload.get("tool_name", "")
    ti = payload.get("tool_input", {}) or {}
    if name == "Write":
        return ti.get("content", "") or ""
    if name == "Edit":
        if ti.get("replace_all") is None and "edits" in ti:
            return "\n".join(e.get("new_string", "") for e in ti.get("edits", []))
        return ti.get("new_string", "") or ""
    if name in {"MultiEdit", "NotebookEdit"}:
        return "\n".join(e.get("new_string", "") for e in ti.get("edits", [])) or ti.get("new_source", "") or ""
    return ""


def suffix_of(path):
    dot = path.rfind(".")
    return path[dot:].lower() if dot != -1 else ""


def offenders(text, suffix):
    found = []
    in_block = False
    for number, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line:
            continue
        if suffix in SLASH_LANGS:
            if in_block:
                if "*/" in line:
                    in_block = False
                continue
            if line.startswith("/**"):
                if "*/" not in line:
                    in_block = True
                continue
            if line.startswith("/*"):
                if "*/" not in line:
                    in_block = True
                continue
            if line.startswith("//") or (suffix == ".php" and line.startswith("#") and not line.startswith("#[")):
                if not DIRECTIVE.search(line):
                    found.append((number, line))
                continue
            tail = trailing_comment(line, ("//",))
            if tail and not DIRECTIVE.search(tail):
                found.append((number, tail))
            continue
        if suffix in HASH_LANGS:
            if line.startswith("#"):
                if not DIRECTIVE.search(line) and line != "#":
                    found.append((number, line))
                continue
            tail = trailing_comment(line, ("#",))
            if tail and not DIRECTIVE.search(tail):
                found.append((number, tail))
    return found


def main():
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0

    path = ((payload.get("tool_input") or {}).get("file_path")) or ""
    suffix = suffix_of(path)
    if not path or SKIP_PATH.search(path) or (suffix not in HASH_LANGS and suffix not in SLASH_LANGS):
        return 0

    hits = offenders(added_text(payload), suffix)
    if not hits:
        return 0

    shown = hits[:MAX_REPORTED]
    listing = "\n".join(f"  {n}: {t}" for n, t in shown)
    extra = f"\n  ... and {len(hits) - len(shown)} more" if len(hits) > len(shown) else ""
    message = (
        f"code-comments check: {len(hits)} comment line(s) in {path} may violate the no-comments rule.\n"
        f"{listing}{extra}\n"
        "Re-read each one. Keep it only if it explains a non-obvious WHY (workaround, business rule, deliberate "
        "deviation) or is a tooling directive; otherwise delete it or replace it with a better name. Do not "
        "announce this check to the user — just fix the file."
    )
    json.dump(
        {"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": message}},
        sys.stdout,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
