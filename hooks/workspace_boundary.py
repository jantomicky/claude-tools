#!/usr/bin/env python3
"""PreToolUse: deny secrets, and make the user confirm any other tool call that reaches outside the workspace.

Inside: the project root, the folder above it (unless that is the home folder, an ancestor of it, a protected or
system folder), the session cwd, `permissions.additionalDirectories`, `CLAUDE_WORKSPACE_ROOTS`, temp folders and
the Claude config folder. A protected home folder nested in a root stays outside, so a session started in the home
folder still asks for `~/Documents`.

Secrets are denied whatever the workspace is and whoever asked, because the request can come from a planted file:
SSH and GPG keys, keychains, browser, Mail and Messages data, shell history, CLI token files, and the commands that
print them.

File tools ask for every other outside path. Bash asks only for the home folder and for system data on this machine:
a path that exists, or one the call could create. A binary called by absolute path stays quiet, and so does whatever
runs in a container or on another host (`docker exec`, `docker run`, `kubectl exec`, `ssh`), apart from the flags
that name local paths. The root folder counts only as an unquoted word of its own, so a `/` in a `sed` expression,
a division or a comment stays quiet. Bash also asks for commands that leave the workspace without naming a path:
root, other apps, global installs.

The hook never answers "allow": an inside path falls through to the normal permission flow.
"""
import json
import os
import re
import sys
import tempfile

HOME = os.path.realpath(os.path.expanduser("~"))
CONFIG = os.path.realpath(os.environ.get("CLAUDE_CONFIG_DIR") or os.path.join(HOME, ".claude"))
PROTECTED = tuple(
    os.path.realpath(os.path.join(HOME, name))
    for name in (".ssh", ".gnupg", ".aws", ".kube", ".docker", ".config", ".netrc",
                 "Library", "Documents", "Downloads", "Desktop")
)
SYSTEM = ("/etc", "/var", "/private", "/Library", "/System", "/Volumes", "/Users", "/home", "/root", "/mnt",
          "/media", "/boot")
SECRET_PATHS = re.compile(
    "(?:"
    + re.escape(HOME)
    + "/(?:"
    + "|".join((
        r"\.ssh(?!/(?:config|known_hosts|authorized_keys)\b|/[\w.@-]+\.pub\b)\b",
        r"\.gnupg\b",
        r"Library/(?:Keychains|Mail|Messages|Safari|Cookies|Containers/com\.apple\.(?:mail|Safari|MobileSMS))\b",
        r"Library/Application Support/(?:Google/Chrome|Chromium|BraveSoftware|Microsoft Edge|Arc|Vivaldi|Firefox"
        r"|com\.operasoftware)",
        r"\.mozilla\b|\.config/(?:google-chrome|chromium|BraveSoftware|microsoft-edge)\b",
        r"\.[\w-]*history\b|\.histfile\b|\.zsh_sessions\b|\.local/share/fish/fish_history\b",
        r"\.aws/(?:credentials|sso)\b|\.netrc\b|\.npmrc\b|\.pypirc\b|\.git-credentials\b",
        r"\.docker/config\.json\b|\.kube/config\b|\.azure\b|\.terraform\.d/credentials",
        r"\.config/(?:gh/hosts\.yml|gcloud|composer/auth\.json)\b|\.composer/auth\.json\b",
    ))
    + ")|"
    + re.escape(CONFIG)
    + r"/\.credentials\.json\b|(?<![\w.-])/Library/Keychains\b)[^\s'\"]*"
)
PATH_KEYS = ("file_path", "notebook_path", "path")
GLOB_CHARS = re.compile(r"[*?\[{]")
SHELL_SPLIT = re.compile(r"[\s;|&<>()'\"`=:,]+")
TILDE = re.compile(r"(?<![\w/.~$-])~(?=[/\s'\"]|$)")
COMMAND_START = r"(?:^|[;&|(`\n]|\$\()\s*(?:\w+=\S*\s+)*"
SINGLE_QUOTED = r"'[^']*'"
DOUBLE_QUOTED = r"\"(?:\\.|[^\"\\])*\""
REMOTE = re.compile(
    COMMAND_START
    + r"(?:(?:docker|podman|nerdctl)(?:[ -]compose)?\b[^;&|<>\n]*?\s(?:exec|run)|kubectl\b[^;&|<>\n]*?\sexec|ssh)(?=\s)"
    + "((?:[^;&|<>\\n'\"]|" + SINGLE_QUOTED + "|" + DOUBLE_QUOTED + ")*)"
)
LOCAL_FLAGS = re.compile(r"(?<!\S)(?:-v|--volume|--mount|--env-file|--cidfile|-i|-F)[=\s]+(\S+)")
NOT_A_SHELL_WORD = re.compile(
    r"<<-?\s*(['\"]?)(\w+)\1.*?\n\s*\2\b|\$\(\(.*?\)\)|" + SINGLE_QUOTED + r"|\"(?:\\.|[^\"\\$`]|\$(?!\())*\"",
    re.DOTALL,
)
ROOT_WORD = re.compile(r"(?<![^\s;|&(=])/(?=$|[\s;|&)*?\[{])")


def commands(*labelled):
    return tuple((label, re.compile(COMMAND_START + "(?:" + pattern + ")")) for label, pattern in labelled)


SECRET_COMMANDS = commands(
    ("keychain (security)", r"security\s+\w"),
    ("CLI token", r"gh\s+auth\s+token\b|gcloud\s+auth\s+print-[\w-]*token\b|aws\s+configure\s+export-credentials\b"),
)
OUTSIDE_COMMANDS = commands(
    ("root (sudo)", r"sudo\b"),
    ("another app", r"(?:osascript|automator)\b|shortcuts\s+run\b"),
    (
        "global install",
        r"(?:npm|pnpm|bun)\b[^;&|]*\s(?:-g|--global)\b|(?:yarn|composer)\s+global\b"
        r"|brew\s+(?:install|uninstall|reinstall|upgrade|tap|link)\b|(?:pipx|cargo|gem|go)\s+install\b"
        r"|uv\s+tool\s+install\b|pip3?\s+install\b[^;&|]*\s--user\b",
    ),
)
MAX_REPORTED = 3


def expand_home(text):
    return TILDE.sub(lambda _: HOME, text.replace("${HOME}", HOME).replace("$HOME", HOME))


def resolve(path, cwd):
    return os.path.realpath(os.path.join(cwd, expand_home(path)))


def within(path, root):
    return path == root or path.startswith(root.rstrip("/") + "/")


def added_directories(project):
    found = []
    for settings in (
        os.path.join(CONFIG, "settings.json"),
        os.path.join(project, ".claude", "settings.json"),
        os.path.join(project, ".claude", "settings.local.json"),
    ):
        try:
            directories = json.load(open(settings))["permissions"]["additionalDirectories"]
        except (OSError, ValueError, KeyError, TypeError):
            continue
        if isinstance(directories, list):
            found += [directory for directory in directories if isinstance(directory, str)]
    return found + [root for root in os.environ.get("CLAUDE_WORKSPACE_ROOTS", "").split(os.pathsep) if root]


def workspace_roots(cwd):
    """Project root, session cwd, the project's parent folder and the folders the user added, in that order."""
    project = resolve(os.environ.get("CLAUDE_PROJECT_DIR") or cwd, cwd)
    roots = [project, resolve(cwd, cwd)]
    parent = os.path.dirname(project)
    if not (
        within(HOME, parent)
        or any(within(parent, folder) for folder in PROTECTED)
        or parent in {os.path.realpath(folder) for folder in SYSTEM}
    ):
        roots.append(parent)
    roots += [resolve(root, project) for root in added_directories(project)]
    return list(dict.fromkeys(roots))


def always_inside():
    temp = {os.path.realpath(path) for path in ("/tmp", "/var/tmp", tempfile.gettempdir())}
    return [CONFIG, *sorted(temp)]


def inside(path, roots):
    return any(
        within(path, root)
        and not any(folder != root and within(folder, root) and within(path, folder) for folder in PROTECTED)
        for root in roots
    )


def is_program(path):
    return os.path.isfile(path) and os.access(path, os.X_OK) and not any(within(path, f) for f in PROTECTED)


def on_this_machine(path):
    parent = os.path.dirname(path)
    return os.path.lexists(path) or (os.path.isdir(parent) and os.access(parent, os.W_OK))


def bash_outside(path):
    if is_program(path):
        return False
    if path == "/" or within(path, HOME):
        return True
    return any(within(path, os.path.realpath(folder)) for folder in SYSTEM) and on_this_machine(path)


def file_tool_paths(tool_name, tool_input, cwd):
    paths = [resolve(tool_input[key], cwd) for key in PATH_KEYS if isinstance(tool_input.get(key), str)]
    pattern = tool_input.get("pattern" if tool_name == "Glob" else "glob")
    if isinstance(pattern, str):
        base = resolve(tool_input["path"], cwd) if isinstance(tool_input.get("path"), str) else cwd
        static = GLOB_CHARS.split(pattern, maxsplit=1)[0]
        if static:
            paths.append(resolve(static, base))
    return paths


def local_part(command):
    """Drop what runs in a container or on another host, keeping the flag values that name local paths."""
    return REMOTE.sub(
        lambda match: match.group(0)[: match.start(1) - match.start(0)]
        + " "
        + " ".join(LOCAL_FLAGS.findall(match.group(1))),
        command,
    )


def bash_paths(command, cwd):
    command = expand_home(command)
    paths = ["/"] if ROOT_WORD.search(NOT_A_SHELL_WORD.sub("_", command)) else []
    for token in SHELL_SPLIT.split(command):
        token = GLOB_CHARS.split(token, maxsplit=1)[0]
        if token.strip("/") and ("/" in token or token == ".."):
            paths.append(resolve(token, cwd))
    return paths


def classify(payload):
    """Return (secrets, outside): what the call must never touch, and what the user has to confirm."""
    tool_input = payload.get("tool_input") or {}
    cwd = payload.get("cwd") or os.getcwd()
    roots = workspace_roots(cwd) + always_inside()
    if payload.get("tool_name") == "Bash":
        command = str(tool_input.get("command") or "")
        paths = bash_paths(command, cwd)
        secrets = [label for label, pattern in SECRET_COMMANDS if pattern.search(command)]
        secrets += [match.group(0) for match in SECRET_PATHS.finditer(expand_home(command).replace("\\ ", " "))]
        outside = [label for label, pattern in OUTSIDE_COMMANDS if pattern.search(command)]
        local = bash_paths(local_part(command), cwd)
        outside += [path for path in local if bash_outside(path) and not inside(path, roots)]
    else:
        paths = file_tool_paths(payload.get("tool_name"), tool_input, cwd)
        secrets = []
        outside = [path for path in paths if not inside(path, roots)]
    secrets += [path for path in paths if SECRET_PATHS.match(path)]
    return list(dict.fromkeys(secrets)), list(dict.fromkeys(outside))


def listing(found):
    extra = f" and {len(found) - MAX_REPORTED} more" if len(found) > MAX_REPORTED else ""
    return ", ".join(found[:MAX_REPORTED]) + extra


def main():
    try:
        payload = json.load(sys.stdin)
    except ValueError:
        return 0
    if not isinstance(payload, dict):
        return 0
    secrets, outside = classify(payload)
    tool = payload.get("tool_name")
    if secrets:
        decision = "deny"
        reason = (
            f"workspace-boundary: {tool} touches a secret: {listing(secrets)}. Keys, keychains, browser, Mail and "
            "Messages data, shell history and CLI tokens are blocked for every request, an explicit one included. "
            "Do not try another route. If the user needs it, they run the command themselves."
        )
    elif outside:
        decision = "ask"
        reason = (
            f"workspace-boundary: {tool} reaches outside the workspace: {listing(outside)}. "
            "Approve only if you asked for this."
        )
    else:
        return 0
    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": decision,
                "permissionDecisionReason": reason,
            }
        },
        sys.stdout,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
