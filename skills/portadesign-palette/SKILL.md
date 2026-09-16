---
name: portadesign-palette
description: Default color palette for visual work (Artifacts, mockups, diagrams, dashboards), extracted from portadesign.cz's production CSS. Apply whenever the artifact-design or dataviz skill picks colors, unless the user names a different palette or brand.
---

# Porta Design Palette

Brand colors from portadesign.cz's live stylesheet.

## When to use

1. The `artifact-design` or `dataviz` skill reaches its color step. Use these tokens instead of its defaults.
2. Skip only when the user names other colors, a palette, or a brand.

## Tokens

| Token | Hex | Light theme | Dark theme |
|---|---|---|---|
| `black` | `#1c1c22` | Primary text | Background |
| `cream` | `#f6ede1` | Background | Primary text |
| `white` | `#ffffff` | Raised surface | — |
| `dim-grey` | `#4a4a5a` | Secondary text, borders | Raised surface, borders |
| `slate-grey` | `#7f7f92` | Large captions only | Tertiary text |
| `dark-grey` | `#adadc0` | — | Secondary text |
| `line` | `#adadc0` at 40% alpha | Hairlines | Hairlines |
| `tomato` | `#ff4942` | Accent | Accent |

## Rules

1. **One tomato accent per view.** It is the only saturated color. Never use it as decoration or as "danger".
2. **Mind tomato contrast on light grounds.** It reaches 2.9:1 on cream and 3.3:1 on white: use it for fills,
   icons, and large text; darken it for body-size links. On black it reaches 5.1:1.
3. **Add separate semantic hues** for error, warning, and success when needed.
4. **Keep the full design process.** The palette replaces only the color choice, not theming or contrast checks.
5. **Re-extract if stale.** `curl` https://www.portadesign.cz/, open the linked `porta1.webflow.shared.*.min.css`,
   `grep -o ':root{[^}]*}'`. Extracted 2026-08-27. Per-project case-study colors are not part of the brand.
