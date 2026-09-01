---
name: code-comments
description: Write code without explanatory comments — in any language (PHP, Python, YAML/Ansible, shell, JS/TS). A comment survives only if it captures a non-obvious WHY. Always applies when writing or editing code.
---

# Code comments

Default is **no comment**. Well-named identifiers, types, and small functions already state what the code does;
a comment restating that is noise that rots out of sync with the code.

## The WHY test

Keep a comment only if it explains something the code cannot: a non-obvious reason, a workaround for an upstream
bug (link it), a business rule with no other home, a deliberate deviation from the obvious approach.

Delete on sight:

1. Restating the next line (`// increment counter`, `# set the variable`).
2. Section banners and step narration (`// --- Setup ---`, `# 1. Fetch data`, `// arrange/act/assert`).
3. Line comments duplicating an adjacent docblock.
4. Commented-out code — git has it.
5. Changelog notes in code (`# added 2025-04, JT`) — that is what commits are for.

## Instead of a comment

Extract a named function or variable, tighten the type, or rename the identifier. If a block needs a comment to be
readable, that is a signal to restructure it, not to annotate it.

## Per language

- **PHP**: no `//` narration. PHPDoc blocks (`/** ... */`) are fine and stay — they carry what the signature
  cannot (`@param array<int, Foo>`, `@throws`, PHPStan generics) and IDEs read them. Keep them factual: a
  `@param`/`@return`/`@throws` contract, not a prose walkthrough of the method body.
- **Python**: docstrings on public modules, classes, and functions are a convention — keep them, but state purpose
  and contract, not a line-by-line walkthrough. Inline `#` comments follow the WHY test like everywhere else.
- **YAML / Ansible**: a task's `name:` is the documentation — never pair it with a `#` comment saying the same
  thing. Group headers above a block of tasks are banners; delete them.
- **Shell**: shebang and `set -euo pipefail` need no explanation. Comment only genuinely cryptic expansions.
- **JS/TS**: types replace type comments. JSDoc only where it adds a contract the types cannot express.

## Tool directives are not comments

`# noqa`, `# type:`, `# fmt: off`, `// eslint-disable`, `// @ts-expect-error`, `@phpstan-ignore`, `shellcheck disable`
are instructions to tooling. Keep them, and where the suppression is non-obvious add the WHY on the same line.

## Before finishing

Re-read every line you touched and delete each comment failing the WHY test. This is a mandatory last step, not an
optional polish pass — it is the rule agents violate most.
