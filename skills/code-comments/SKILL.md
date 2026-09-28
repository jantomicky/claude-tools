---
name: code-comments
description: Write code without explanatory comments in any language. Keep a comment only if it captures a non-obvious WHY. Always applies when writing or editing code.
---

# Code comments

Default to no comment. Names, types, and small functions state what code does. Need a comment to make a block
readable? Extract a function, name a variable, or tighten a type instead.

## Keep

1. **A non-obvious WHY.** An upstream-bug workaround (link it), a business rule with no other home, a deliberate
   deviation from the obvious approach.
2. **Docblocks as contracts.** PHPDoc (`@param array<int, Foo>`, `@throws`), docstrings on public API, JSDoc the
   types cannot express. State purpose and contract, not a walkthrough.
3. **Tool directives.** `# noqa`, `// eslint-disable`, `@phpstan-ignore`, shebangs. Add the WHY on the same line
   when a suppression is non-obvious.

## Delete

1. Comments restating the code (`// increment counter`).
2. Banners and step narration (`// --- Setup ---`, `# 1. Fetch data`, `// arrange`).
3. Comments duplicating an adjacent docblock, a type, or an Ansible task `name:`.
4. Commented-out code and changelog notes (`# added 2025-04, JT`). Git has both.

## Before finishing

Re-read every line you touched. Delete each comment that fails the test.
