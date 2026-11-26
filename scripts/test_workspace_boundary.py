#!/usr/bin/env python3
"""Regression suite for hooks/workspace_boundary.py. Run from the repo root.

Each case pipes a PreToolUse payload to the hook under a fictional home folder and expects a block ("deny"), a
prompt ("ask") or silence ("pass").
"""
import json
import os
import subprocess
import sys

HOOK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "hooks", "workspace_boundary.py")
HOME = "/nonexistent-home/tester"
PROJECT = f"{HOME}/Code/claude-tools"
NESTED = f"{HOME}/Code/client/proj"
IN_DOCUMENTS = f"{HOME}/Documents/proj"
EXTRA_ROOTS = {"CLAUDE_WORKSPACE_ROOTS": f"{HOME}/work{os.pathsep}~/oss"}

FILE_CASES = [
    ("pass", "Read", {"file_path": f"{PROJECT}/README.md"}),
    ("pass", "Read", {"file_path": "README.md"}),
    ("pass", "Edit", {"file_path": f"{HOME}/Code/other/x.php"}),
    ("pass", "Write", {"file_path": "/tmp/x.txt"}),
    ("pass", "Read", {"file_path": f"{HOME}/.claude/projects/x/memory/MEMORY.md"}),
    ("pass", "Glob", {"pattern": "**/*.py"}),
    ("pass", "Glob", {"pattern": "src/**/*.py", "path": PROJECT}),
    ("pass", "Grep", {"pattern": "/etc/passwd|~/.ssh", "path": "."}),
    ("ask", "Read", {"file_path": f"{HOME}/.ssh/config"}),
    ("ask", "Read", {"file_path": f"{HOME}/.ssh/id_ed25519.pub"}),
    ("ask", "Read", {"file_path": f"{HOME}/.aws/config"}),
    ("deny", "Read", {"file_path": "~/.ssh/id_rsa"}),
    ("deny", "Grep", {"pattern": "PRIVATE", "path": f"{HOME}/.ssh"}),
    ("deny", "Read", {"file_path": f"{HOME}/.gnupg/private-keys-v1.d/a.key"}),
    ("deny", "Read", {"file_path": f"{HOME}/.aws/credentials"}),
    ("deny", "Read", {"file_path": f"{HOME}/.claude/.credentials.json"}),
    ("deny", "Read", {"file_path": f"{HOME}/Library/Application Support/Google/Chrome/Default/Cookies"}),
    ("deny", "Read", {"file_path": f"{HOME}/Library/Messages/chat.db"}),
    ("deny", "Edit", {"file_path": f"{HOME}/.npmrc"}),
    ("pass", "Read", {"file_path": f"{PROJECT}/.npmrc"}),
    ("pass", "Read", {"file_path": f"{PROJECT}/Library/Mail/fixture.eml"}),
    ("ask", "Read", {"file_path": f"{HOME}/Documents/a.pdf"}),
    ("ask", "Read", {"file_path": f"{HOME}/Downloads/a.zip"}),
    ("deny", "Read", {"file_path": f"{HOME}/.zsh_history"}),
    ("ask", "Read", {"file_path": f"{HOME}/.claude.json"}),
    ("deny", "Read", {"file_path": f"{HOME}/Library/Keychains/login.keychain-db"}),
    ("ask", "Read", {"file_path": "/etc/hosts"}),
    ("ask", "Read", {"file_path": "/usr/include/stdio.h"}),
    ("ask", "Write", {"file_path": "../../notes.txt"}),
    ("ask", "NotebookEdit", {"notebook_path": f"{HOME}/Desktop/a.ipynb"}),
    ("ask", "Glob", {"pattern": f"{HOME}/Documents/**/*.pdf"}),
    ("ask", "Glob", {"pattern": "../../**/*"}),
    ("ask", "Glob", {"pattern": "*", "path": HOME}),
    ("ask", "Grep", {"pattern": "x", "path": f"{HOME}/Library"}),
    ("deny", "Grep", {"pattern": "x", "glob": "../../.ssh/*"}),
]

BASH_CASES = [
    ("pass", "git status && python3 scripts/lint.py 2>/dev/null"),
    ("pass", f"cd {HOME}/Code/other && ls ../claude-tools"),
    ("pass", "/usr/bin/env python3 -V; /bin/ls /opt/homebrew/bin"),
    ("pass", "docker compose exec php cat /var/app-in-container/log/dev.log"),
    ("pass", "curl -s https://example.com/etc/passwd -o /tmp/x"),
    ("pass", "sed -i '' 's/a/b/' README.md && sed -n '/foo/p' README.md"),
    ("pass", "ls ~/.claude/plugins"),
    ("pass", "scp out.tar deploy@host.example:releases/"),
    ("pass", "npm install && npm run build && composer install"),
    ("pass", "git commit -m 'docs: explain sudo and osascript'"),
    ("pass", "grep -rn security src && pip install -r requirements.txt"),
    ("pass", "sed 's/,/ /g' README.md | tr '/' '_' | awk -F'/' '{print $2}'"),
    ("pass", "echo $((10 / 2)) && python3 -c 'print(7 // 2)'"),
    ("pass", 'ls "$dir"/ $(pwd)/ && git log --format="%h / %s"'),
    ("pass", "grep -E '/[a-z]+/' README.md"),
    ("pass", "node <<'EOF'\n// note\nconsole.log(4 / 2)\nEOF"),
    ("pass", "docker compose exec php cat /etc/hosts"),
    ("pass", "docker compose -f compose.yml run --rm -w /app php ls /etc /"),
    ("pass", "kubectl -n shop exec pod -- cat /etc/hosts"),
    ("pass", "ssh deploy@host.example 'ls /etc /' && git status"),
    ("pass", "grep -rn /etc/claude-tools-absent ."),
    ("ask", "ls /*.md"),
    ("ask", "cd / && ls"),
    ("ask", 'echo "$(ls /)"'),
    ("ask", "docker run -v ~/Documents:/data alpine ls /data"),
    ("ask", "docker compose exec php cat /etc/hosts > ~/Documents/hosts.txt"),
    ("ask", "docker compose exec php true; cat /etc/hosts"),
    ("ask", "ssh -i ~/Documents/key deploy@host.example ls"),
    ("ask", "cat ~/.ssh/config"),
    ("deny", "cat ~/.ssh/id_rsa"),
    ("deny", "ls -la $HOME/.ssh"),
    ("deny", "cat ../../.ssh/id_ed25519"),
    ("deny", "sqlite3 ~/Library/Application\\ Support/Firefox/Profiles/x/cookies.sqlite .dump"),
    ("deny", 'cp "~/Library/Application Support/Google/Chrome/Default/Login Data" /tmp/x'),
    ("deny", "tail -50 ~/.zsh_history"),
    ("deny", "cat ~/.config/gh/hosts.yml"),
    ("ask", "ls $HOME/Downloads | head"),
    ("ask", 'cat "${HOME}/Documents/x y.txt"'),
    ("ask", "cat ../../.zshrc"),
    ("ask", "cd ~ && ls"),
    ("ask", "cat /etc/hosts"),
    ("ask", "find / -name id_rsa"),
    ("deny", "docker run -v ~/.ssh:/root/.ssh alpine ls"),
    ("ask", "python3 -c \"print(open('/etc/passwd').read())\""),
    ("ask", "tar czf /tmp/a.tgz --directory=/etc ."),
    ("ask", f"ls {HOME}/Doc*"),
    ("deny", "security find-generic-password -s github -w"),
    ("ask", "cd src && osascript -e 'tell application \"Mail\" to quit'"),
    ("ask", "sudo rm -rf node_modules"),
    ("ask", "npm install -g typescript"),
    ("ask", "FOO=1 brew install jq"),
    ("deny", "echo $(gh auth token)"),
    ("ask", "pip install --user requests"),
]
if sys.platform == "darwin":
    BASH_CASES.append(("ask", "touch /Users/Shared/claude-tools-absent.txt"))

ROOT_CASES = [
    ("ask", "Read", {"file_path": f"{HOME}/.zshrc"}, {"project": f"{HOME}/proj"}),
    ("ask", "Read", {"file_path": f"{HOME}/.ssh/config"}, {"project": HOME}),
    ("deny", "Bash", {"command": "cat .ssh/id_rsa"}, {"project": HOME}),
    ("ask", "Bash", {"command": "ls Documents/"}, {"project": HOME}),
    ("pass", "Read", {"file_path": f"{HOME}/notes.txt"}, {"project": HOME}),
    ("ask", "Bash", {"command": "cat .ssh/../.ssh/config"}, {"project": HOME}),
    ("pass", "Read", {"file_path": f"{IN_DOCUMENTS}/a.md"}, {"project": IN_DOCUMENTS}),
    ("ask", "Read", {"file_path": f"{HOME}/Documents/other.md"}, {"project": IN_DOCUMENTS}),
    ("pass", "Read", {"file_path": f"{HOME}/work/a/b.md"}, {"env": EXTRA_ROOTS}),
    ("pass", "Read", {"file_path": f"{HOME}/oss/a.md"}, {"env": EXTRA_ROOTS}),
    ("ask", "Read", {"file_path": f"{HOME}/work2/a.md"}, {"env": EXTRA_ROOTS}),
    ("pass", "Read", {"file_path": f"{HOME}/Code/client/sibling/a"}, {"project": NESTED}),
    ("ask", "Read", {"file_path": f"{HOME}/Code/elsewhere/a"}, {"project": NESTED}),
]


def run(tool, tool_input, project=PROJECT, env=None):
    environment = {"PATH": os.environ.get("PATH", ""), "HOME": HOME, "CLAUDE_PROJECT_DIR": project, **(env or {})}
    payload = json.dumps({"tool_name": tool, "tool_input": tool_input, "cwd": project})
    result = subprocess.run([sys.executable, HOOK], input=payload, capture_output=True, text=True, env=environment)
    if result.returncode != 0:
        return f"crash: {result.stderr.strip()[-200:]}"
    if not result.stdout:
        return "pass"
    return json.loads(result.stdout)["hookSpecificOutput"]["permissionDecision"]


def main():
    cases = [(expected, tool, tool_input, {}) for expected, tool, tool_input in FILE_CASES]
    cases += [(expected, "Bash", {"command": command}, {}) for expected, command in BASH_CASES]
    cases += ROOT_CASES
    failed = 0
    for expected, tool, tool_input, options in cases:
        got = run(tool, tool_input, **options)
        if got != expected:
            failed += 1
            print(f"FAIL expected {expected}, got {got}: {tool} {tool_input} {options}")
    print(f"{len(cases)} cases, {failed} failed")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
