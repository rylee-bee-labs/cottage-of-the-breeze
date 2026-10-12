# Round 22: Game Boy Advance pixel art (2026-10-12)

Rylee: "No art is sacred. Not even main npc. Do a full art set with motion and interactions but keep it in the same
gameboy advance era art style with our storybook please". After a side-by-side style test at phone size, her pick
was "B: GBA pixel art (Recommended)".

**Credit:** Rylee and Claude. Drawn with Codex image (gpt-image-2) through the estate's `offload image`, from the
prompts in `prompts/`; cut, cleaned into native pixels and animated by Claude with the pixel-art tools (vefr#426).

| Sheet | Made from | Used for |
|---|---|---|
| `style-a.webp`, `style-b.webp` | `prompts/style_test.sh` | the style test; **B** was picked, A was not used |
| `hero-down`, `hero-right`, `hero-act-down`, `hero-act-right`, `hero-act-up` | `prompts/hero_gen.sh` | the hero's sheet (`sprites/hero-sheet.webp`) |
| `hero-up` | `prompts/hero_gen.sh` | **not used**: the back view came out squashed to half height |
| `hero-up2` | a retry with "full height" | **not used**: a pointed hood that did not match the back of the action strip |
| `hero-up3` | a retry with two good back views as the reference | the back walk |
| `town-houses`, `town-works`, `town-props`, `town-pond`, `town-ground` | `prompts/town_gen.sh` | the town kit (`props/`, the town's `tiles/`); the temple's cross was removed |
| `npc-*` | `prompts/npc_gen.sh` | the seven residents' sheets (`sprites/<name>-sheet.webp`) |

The source sheets are kept here as WebP (quality 90); the game's pictures are lossless WebP at their native size.
