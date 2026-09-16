---
name: code-comments
description: Write code without explanatory comments in any language (PHP, Python, YAML/Ansible, shell, JS/TS). Keep a comment only if it captures a non-obvious WHY. Always applies when writing or editing code.
---

# Code comments

Default to no comment. Names, types, and small functions state what code does. A comment restating it rots.

## When to use

Every time you write or edit code.

## Keep a comment only if

It explains what the code cannot: a non-obvious reason, an upstream-bug workaround (link it), a business rule
with no other home, or a deliberate deviation from the obvious approach.

## Delete

1. Comments restating the next line (`// increment counter`).
2. Banners and step narration (`// --- Setup ---`, `# 1. Fetch data`, `// arrange`).
3. Comments duplicating an adjacent docblock, a type, or an Ansible task `name:`.
4. Commented-out code and changelog notes (`# added 2025-04, JT`). Git has both.

Need a comment to make a block readable? Extract a function, name a variable, or tighten a type instead.

## Keep

1. **Docblocks as contracts.** PHPDoc (`@param array<int, Foo>`, `@throws`), Python docstrings on public API,
   JSDoc the types cannot express. State purpose and contract, not a walkthrough.
2. **Tool directives.** `# noqa`, `# type: ignore`, `// eslint-disable`, `@phpstan-ignore`, `shellcheck disable`.
   Add the WHY on the same line when the suppression is non-obvious.
3. **Shebangs.** No comment on `set -euo pipefail`.

## Before finishing

Re-read every line you touched. Delete each comment that fails the test. Agents skip this step most.
