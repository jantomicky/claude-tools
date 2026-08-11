## Language

- Write all artifacts (skill files, docs, commit messages, code comments) in English, no matter what language
  the conversation uses.
- Use direct commands. Avoid unnecessary em-dashes. Keep language clear and concise.

## Adding

- Follow the `tldr` skill's own rules (`skills/tldr/SKILL.md`). Lead with the action. Number steps. Skip preamble
  and filler. Cap lists at 5. Be concrete, not vague. A skill file that breaks `tldr` while telling the agent to
  follow `tldr` is a bug.
- Write a specific `SKILL.md` frontmatter `description`. State what the skill does and when to invoke it, not
  just its name.
- Reuse existing patterns (`recall/SKILL.md`, `tldr/SKILL.md`). Structure: short intro, `## When to use`,
  numbered content and how-to sections.
- Update `README.md`'s skill table when you add or rename a skill.

## Release

- Bump `version` in `.claude-plugin/plugin.json` in the same commit as any change. `/plugin update` compares
  versions, not content. An unbumped version means installed copies silently stay stale.
