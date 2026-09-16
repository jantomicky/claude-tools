## Language

- Write all artifacts (skills, docs, commit messages, code comments) in English, whatever the conversation language.
- Use direct commands. Keep language clear and concise.

## Adding

- Follow `skills/tldr/SKILL.md`: action first, numbered steps, no filler, lists capped at 5. A skill that breaks
  `tldr` while telling the agent to follow it is a bug.
- Write a `SKILL.md` `description` that says what the skill does and when to invoke it.
- Structure skills like `recall/SKILL.md`: short intro, `## When to use`, numbered sections.
- Update `README.md` tables when you add or rename a skill, hook, or output style.

## Release

- Bump `version` in `.claude-plugin/plugin.json` in the same commit as any change. `/plugin update` compares
  versions, not content.
