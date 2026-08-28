---
name: portadesign-palette
description: Default color palette for visual work — Artifacts, mockups, diagrams, dashboards — extracted from portadesign.cz's production CSS. Always applies when the artifact-design or dataviz skill's color step runs, unless the user explicitly names a different palette or brand.
---

# Porta Design Palette

Brand colors extracted from portadesign.cz's live stylesheet. Use as the default color
token set for any visual output — Artifacts, HTML mockups, diagrams, dashboards.

## When to use

1. Any time the `artifact-design` or `dataviz` skill reaches its color-choice step, use
   these tokens instead of a generic/default palette.
2. Skip it only when the user explicitly names a different palette, brand, or specific
   colors for that piece of work — an explicit request always wins.

## Tokens

| Role | Hex | Use |
|---|---|---|
| `black` | `#1c1c22` | Primary ink / dark ground |
| `cream` | `#f6ede1` | Light ground |
| `tomato` | `#ff4942` | Sole accent — CTAs, links, emphasis |
| `dark-grey` | `#adadc0` | Secondary text on dark ground |
| `slate-grey` | `#7f7f92` | Tertiary text, captions |
| `dim-grey` | `#4a4a5a` | Muted text, borders |
| `white` | `#ffffff` | Raised surface on light ground |
| `line` | `#adadc0` at 40% alpha | Hairline dividers |

## Usage rules

1. **Tomato stays singular.** It's the only saturated color in the system. Use it for one
   accent role per view (a button, a highlighted state) — not decoration, not spread across
   multiple elements competing for attention.
2. **Neutrals carry structure.** Black/white/cream/grey do the typography and layout work;
   tomato marks what needs attention.
3. **Semantic color is separate.** Error/warning/success states get their own hues when a UI
   needs them — don't overload tomato as both "the accent" and "danger".
4. **Still run the full design process.** This palette replaces the *color* choice inside
   `artifact-design` / `dataviz`, not the methodology — theme support (light/dark tokens),
   contrast checks, and layout craft still apply in full.
5. **Re-extract if stale.** If this looks out of date, pull fresh values from the live site:
   `curl` the homepage, find the linked Webflow shared CSS, `grep -o ':root{[^}]*}'` for the
   custom-property block.

## Source

Extracted 2026-08-27 from `:root` custom properties in `porta1.webflow.shared.*.min.css`
(Webflow-hosted, linked from https://www.portadesign.cz/). Case-study imagery on the site
carries its own per-project accent colors (blues, teal, gold) — those are NOT part of the
brand system and should not be pulled in here.
