# License provenance for Cottage of the Breeze

**Issue:** cottage-of-the-breeze#175 — "Clarify the CC0 scaffold boundary in the
pack-local license" (tracked at [`docs/BACKLOG.md`](../BACKLOG.md) as **#74**;
the earlier related issues are #14 and #16).

**Date:** 2026-10-16 · **Author:** agent, under Rylee's recorded decision
(issue comment 6221536797) · **Status:** research artifact. It backs the
licence-clarification PR beside it. It is not a legal opinion, not a clearance
to publish, and not permission to merge.

> **Owner decision (Rylee, 2026-10-16, issue comment 6221536797)**
>
> "For Cottage #175, I choose A: retain CC0 only for proven inherited original
> scaffold files. Keep original Cottage creative material outside that CC0
> dedication unless separately approved."
>
> This is approved licensing **scope** direction. It is not proof of
> provenance, legal clearance, or permission to merge, publish or deploy.

## The question

`worlds/cottage-of-the-breeze/LICENSE` grants CC0 by **path category** — it
names `world.json`, `map.md`, `voices/`, `lore/`, contracts, "and any prose or
JSON". Since 2026-09-26 those paths now hold mostly Cottage-authored material
(story, voices, lore, books, art, contract templates). Read literally, the
grant reads as covering that later work. The repo-level `LICENSE.md` already
says the narrower thing ("the scaffold content that came from the VEFR sample
world (Emberfield) keeps its CC0 dedication"), so the two files describe the
boundary at different widths.

So: **file by file, what in this pack actually came from the Emberfield
scaffold, and what may stay CC0?**

## Method

The Emberfield scaffold entered this repo in one commit — the new-game-kit
commit `cab23dd` (2026-09-26, *"init: Cottage of the Breeze, the studio's first
game"*), which describes itself as "a VEFR pack scaffolded by 'begin a new
world' (Emberfield demo frame, CC0, as placeholder)". That snapshot is the
ground truth for what was inherited. Four questions, each answered from git:

1. **Was the file in the scaffold?** `git ls-tree -r --name-only cab23dd`
2. **If so, does inherited text survive in it today?** A verbatim line-set diff
   for text files; a leaf-value comparison for JSON. Only text present
   *byte-identical in `cab23dd` and in `HEAD`* is claimed as inherited — no file
   is called inherited on the strength of a path name, a similar shape, or a
   commit subject.
3. **If it was added later, what put it there?** The first commit that added
   the file (`git log --diff-filter=A --reverse`).
4. **What do the repo's own provenance notes say?** `NOTES.md`,
   `docs/repo-map.md`, `art/README.md`, `art/source/**/RECORD.md`,
   `art/source/**/CREDITS-release1.md` and
   `worlds/cottage-of-the-breeze/sprites/CREDITS-release1.md`.

Every command is in [Appendix B](#appendix-b--the-commands-this-table-came-from),
so the table can be re-derived rather than trusted.

Two claims the issue asked to be verified, now verified:

- **The LICENSE text since the 2026-09-26 PRs.** `LICENSE.md` has not changed
  since `cab23dd`. `worlds/cottage-of-the-breeze/LICENSE` has changed exactly
  once, in `69e34e9` (2026-10-02, #53), which **deleted** the `assets/kenney/`
  CC0 section together with the vendored Kenney sheets. It did not alter the
  Emberfield CC0 grant.
- **The non-CC0 inherited sprite.** `b996eda` (2026-09-26, #16) removed
  `acts/act-1/town/sprites/Kitchen_Singles_32x32_1.png`, the one inherited
  image that was not CC0. No inherited binary survives in the pack.

## Findings

- **284 files** are tracked under `worlds/cottage-of-the-breeze/`.
- **12** of them were in the `cab23dd` Emberfield snapshot; **272** were added
  afterwards by Cottage work.
- **0** of the 12 are byte-identical to the scaffold today — every one has been
  edited since. **The CC0 boundary cannot be drawn at file granularity. It has
  to be drawn at fragment granularity.**
- **9** of the 12 still contain inherited text verbatim (§A below). Those
  fragments stay CC0; nothing else in those files does.
- **3** (`map.md`, `logbok.md`, `acts/act-1/town/map.md`) are fully rewritten:
  not one inherited line survives, so no CC0 content is left in them.
- **No image in the pack is inherited.** The scaffold's only binaries were
  `assets/kenney/*.png` (gone in `69e34e9`) and the Kitchen sprite (gone in
  `b996eda`). All 213 pack images were added by Cottage art commits.
- **1 file is marked Unknown**: `library/writing-a-book.md`, added in `21888b7`
  (#14) as "the engine's 'Writing a Book' how-to". It is engine-origin text —
  neither Emberfield scaffold nor Cottage creative material — and no licence
  for it is recorded anywhere in this repo. It is left Unknown rather than
  guessed.

## A. Files from the Emberfield scaffold (12 of 284)

Every one of these was modified after `cab23dd`.

| Path | Origin | Evidence | Current license |
| --- | --- | --- | --- |
| `LICENSE` | Inherited Emberfield scaffold — modified since, inherited text survives | `cab23dd` (2026-09-26) — init: Cottage of the Breeze, the studio's first game | CC0 for the listed fragments only; the rest Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `acts/act-1/town/contract.json` | Inherited Emberfield scaffold — modified since, inherited text survives | `cab23dd` (2026-09-26) — init: Cottage of the Breeze, the studio's first game | CC0 for the listed fragments only; the rest Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `acts/act-1/town/map.md` | Inherited Emberfield scaffold — fully rewritten since the scaffold snapshot | `cab23dd` (2026-09-26) — init: Cottage of the Breeze, the studio's first game | Reserved — no inherited text remains (Reserved — © 2026 Rylee Hulgan, all rights reserved) |
| `acts/act-1/town/voices/keeper.md` | Inherited Emberfield scaffold — modified since, inherited text survives | `cab23dd` (2026-09-26) — init: Cottage of the Breeze, the studio's first game | CC0 for the listed fragments only; the rest Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `acts/act-1/world.json` | Inherited Emberfield scaffold — modified since, inherited text survives | `cab23dd` (2026-09-26) — init: Cottage of the Breeze, the studio's first game | CC0 for the listed fragments only; the rest Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `ledger.md` | Inherited Emberfield scaffold — modified since, inherited text survives | `cab23dd` (2026-09-26) — init: Cottage of the Breeze, the studio's first game | CC0 for the listed fragments only; the rest Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `logbok.md` | Inherited Emberfield scaffold — fully rewritten since the scaffold snapshot | `cab23dd` (2026-09-26) — init: Cottage of the Breeze, the studio's first game | Reserved — no inherited text remains (Reserved — © 2026 Rylee Hulgan, all rights reserved) |
| `map.md` | Inherited Emberfield scaffold — fully rewritten since the scaffold snapshot | `cab23dd` (2026-09-26) — init: Cottage of the Breeze, the studio's first game | Reserved — no inherited text remains (Reserved — © 2026 Rylee Hulgan, all rights reserved) |
| `voices/keeper.fragments.md` | Inherited Emberfield scaffold — modified since, inherited text survives | `cab23dd` (2026-09-26) — init: Cottage of the Breeze, the studio's first game | CC0 for the listed fragments only; the rest Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `voices/keeper.md` | Inherited Emberfield scaffold — modified since, inherited text survives | `cab23dd` (2026-09-26) — init: Cottage of the Breeze, the studio's first game | CC0 for the listed fragments only; the rest Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `world-tree.md` | Inherited Emberfield scaffold — modified since, inherited text survives | `cab23dd` (2026-09-26) — init: Cottage of the Breeze, the studio's first game | CC0 for the listed fragments only; the rest Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `world.json` | Inherited Emberfield scaffold — modified since, inherited text survives | `cab23dd` (2026-09-26) — init: Cottage of the Breeze, the studio's first game | CC0 for the listed fragments only; the rest Reserved — © 2026 Rylee Hulgan, all rights reserved |
### What each inherited file still carries

The CC0 fragments, named so the licence can point at them exactly. Everything
else in these files is Cottage's and is reserved.

| Path | Inherited text still present verbatim (stays CC0) |
| --- | --- |
| `LICENSE` | The "World content (CC0)" grant itself: the `# License — worlds/sample-world (Emberfield)` heading, "Two kinds of thing live here, licensed separately.", the `## World content (CC0)` section, and the CC0 1.0 Universal dedication with its "attribution … not required" note. This is the notice; it is preserved unchanged by the PR. |
| `world.json` | 16 leaf values: `phases.dusk` and `phases.dawn` ("The day settles…" / "The day begins…"), `surface: "combat"`, `voices.keeper.strike` (the bell prompt), all six `bonds.{given,found,cold}.card` / `.prompt` strings, `bond_draw: ""`, `forge_texture: ""`. |
| `acts/act-1/world.json` | Structure carried over from the scaffold's single act: `id: "act-1"`, `regions`, `speakers.keeper.voice_file: "voices/keeper.md"`, and the empty `enemies` / `bosses` lists. Every *value* Cottage gave that structure — the keeper's name, position, `near`, and both seed lines — has been rewritten. |
| `acts/act-1/town/contract.json` | The scaffold's rendering defaults, verbatim: `tile: 32`, `bg: "#131311"`, `hero_color`, `speaker_color`, `speaker_head`, `sanctuary_tiles`, `water_by_phase`. The legend, `pois` and the whole `watch` block are Cottage's. |
| `ledger.md` | The four-line header: `# The Ledger - collected whispers` and "Whispers the engine keeps as voice anchors. Add freely; the / cadence compounds." The whispers under it are Cottage's. |
| `voices/keeper.fragments.md` | Lines 2–5 of the preamble (the composer's instructions: "The packaged composer / re-splices these when a game is woven with no pool and no model: … / the composer keeps the honest silence instead."). The fragment bullets are Cottage's. |
| `voices/keeper.md` | One line: `- No modern words. Never explain. Show only.` The character description and every other rule are Cottage's. |
| `acts/act-1/town/voices/keeper.md` | The same single line. This file is byte-identical to `voices/keeper.md`. |
| `world-tree.md` | The heading `## The World Tree`. The Emberfield walk record under it was deleted in `7b85c92`. |
| `map.md` | **Nothing.** Fully rewritten in `7b85c92`; no inherited line remains. |
| `logbok.md` | **Nothing.** Fully rewritten in `7b85c92`; no inherited line remains. |
| `acts/act-1/town/map.md` | **Nothing.** The 10×9 Emberfield grid was replaced by the Cottage town in `7b85c92` / `ae80a65`. |

### Derived from the scaffold, not inherited from it

`acts/act-1/cottage/contract.json` and `acts/act-1/tavern/contract.json` (both
added `9fc493c`) and `acts/act-1/town-after-the-cellar/contract.json` (added
`e2c5617`) are Cottage-authored files that copied the scaffold's rendering
defaults verbatim: `tile: 32`, `bg`, `hero_color`, `speaker_color`,
`speaker_head`, `water_by_phase`, and an empty `sanctuary_tiles`. They are
listed as Cottage original in §B, with this note as the evidence. They *derive*
from a CC0 file, so the defaults they carry are CC0 — but the files are not
inherited scaffold, and the distinction only matters if those defaults are ever
lifted out on their own.

## B. Files added after the scaffold snapshot (272 of 284)

File by file. "Cottage original" means the file was created by Cottage work
after `cab23dd`. It is not a claim about anything *inside* the file beyond the
credits records it points to — see [What this does not
prove](#what-this-does-not-prove).

#### the pack root — 3 file(s)

| Path | Origin | Evidence | Current license |
| --- | --- | --- | --- |
| `EDITS.md` | Cottage original (added after the scaffold snapshot) | `3474239` (2026-10-01) — game: the new art and five new residents in Cottage | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `blueprint.json` | Cottage tooling output (generated record, `vefr normalize`) | `a999c5b` (2026-10-02) — feat: creature records come from a Blueprint | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `blueprint.lock.json` | Cottage tooling output (generated record, `vefr normalize`) | `a999c5b` (2026-10-02) — feat: creature records come from a Blueprint | Reserved — © 2026 Rylee Hulgan, all rights reserved |

#### `acts/act-1/cottage/` — 2 file(s)

| Path | Origin | Evidence | Current license |
| --- | --- | --- | --- |
| `contract.json` | Cottage original (added after the scaffold snapshot) | `9fc493c` (2026-09-29) — pack: rooms inside | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `map.md` | Cottage original (added after the scaffold snapshot) | `9fc493c` (2026-09-29) — pack: rooms inside | Reserved — © 2026 Rylee Hulgan, all rights reserved |

#### `acts/act-1/cottage/tiles/` — 5 file(s)

| Path | Origin | Evidence | Current license |
| --- | --- | --- | --- |
| `cottage-wall.grid3x3.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `flagstones.grid3x3.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `floor-planks.grid3x3.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `way-door.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `way-stairs-down.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |

#### `acts/act-1/cottage/voices/` — 1 file(s)

| Path | Origin | Evidence | Current license |
| --- | --- | --- | --- |
| `hearth-cat.md` | Cottage original (added after the scaffold snapshot) | `3474239` (2026-10-01) — game: the new art and five new residents in Cottage | Reserved — © 2026 Rylee Hulgan, all rights reserved |

#### `acts/act-1/tavern/` — 2 file(s)

| Path | Origin | Evidence | Current license |
| --- | --- | --- | --- |
| `contract.json` | Cottage original (added after the scaffold snapshot) | `9fc493c` (2026-09-29) — pack: rooms inside | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `map.md` | Cottage original (added after the scaffold snapshot) | `9fc493c` (2026-09-29) — pack: rooms inside | Reserved — © 2026 Rylee Hulgan, all rights reserved |

#### `acts/act-1/tavern/tiles/` — 4 file(s)

| Path | Origin | Evidence | Current license |
| --- | --- | --- | --- |
| `hearthstone.grid3x3.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `tavern-planks.grid3x3.webp` | Cottage original (added after the scaffold snapshot) | `3474239` (2026-10-01) — game: the new art and five new residents in Cottage | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `tavern-wall.grid3x3.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `way-door.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |

#### `acts/act-1/tavern/voices/` — 1 file(s)

| Path | Origin | Evidence | Current license |
| --- | --- | --- | --- |
| `tavern-regular.md` | Cottage original (added after the scaffold snapshot) | `3474239` (2026-10-01) — game: the new art and five new residents in Cottage | Reserved — © 2026 Rylee Hulgan, all rights reserved |

#### `acts/act-1/town-after-the-cellar/` — 2 file(s)

| Path | Origin | Evidence | Current license |
| --- | --- | --- | --- |
| `contract.json` | Cottage original (added after the scaffold snapshot) | `e2c5617` (2026-10-12) — section 1: the household, the King who yields, and the to… | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `map.md` | Cottage original (added after the scaffold snapshot) | `e2c5617` (2026-10-12) — section 1: the household, the King who yields, and the to… | Reserved — © 2026 Rylee Hulgan, all rights reserved |

#### `acts/act-1/town-after-the-cellar/tiles/` — 4 file(s)

| Path | Origin | Evidence | Current license |
| --- | --- | --- | --- |
| `cobbles.grid3x3.webp` | Cottage original (added after the scaffold snapshot) | `2decb5e` (2026-10-12) — town: a bigger first village in Game Boy Advance pixel art | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `forest.grid3x3.webp` | Cottage original (added after the scaffold snapshot) | `2decb5e` (2026-10-12) — town: a bigger first village in Game Boy Advance pixel art | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `grass.grid3x3.webp` | Cottage original (added after the scaffold snapshot) | `2decb5e` (2026-10-12) — town: a bigger first village in Game Boy Advance pixel art | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `lane.grid3x3.webp` | Cottage original (added after the scaffold snapshot) | `2decb5e` (2026-10-12) — town: a bigger first village in Game Boy Advance pixel art | Reserved — © 2026 Rylee Hulgan, all rights reserved |

#### `acts/act-1/town/tiles/` — 4 file(s)

| Path | Origin | Evidence | Current license |
| --- | --- | --- | --- |
| `cobbles.grid3x3.webp` | Cottage original (added after the scaffold snapshot) | `2decb5e` (2026-10-12) — town: a bigger first village in Game Boy Advance pixel art | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `forest.grid3x3.webp` | Cottage original (added after the scaffold snapshot) | `2decb5e` (2026-10-12) — town: a bigger first village in Game Boy Advance pixel art | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `grass.grid3x3.webp` | Cottage original (added after the scaffold snapshot) | `3474239` (2026-10-01) — game: the new art and five new residents in Cottage | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `lane.grid3x3.webp` | Cottage original (added after the scaffold snapshot) | `2decb5e` (2026-10-12) — town: a bigger first village in Game Boy Advance pixel art | Reserved — © 2026 Rylee Hulgan, all rights reserved |

#### `acts/act-1/town/voices/` — 3 file(s)

| Path | Origin | Evidence | Current license |
| --- | --- | --- | --- |
| `dwarf-smith.md` | Cottage original (added after the scaffold snapshot) | `3474239` (2026-10-01) — game: the new art and five new residents in Cottage | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `fisher.md` | Cottage original (added after the scaffold snapshot) | `3474239` (2026-10-01) — game: the new art and five new residents in Cottage | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `gardener.md` | Cottage original (added after the scaffold snapshot) | `3474239` (2026-10-01) — game: the new art and five new residents in Cottage | Reserved — © 2026 Rylee Hulgan, all rights reserved |

#### `assets/` — 1 file(s)

| Path | Origin | Evidence | Current license |
| --- | --- | --- | --- |
| `title.webp` | Cottage original (added after the scaffold snapshot) | `fbf915f` (2026-09-26) — art: Cottage's own title picture | Reserved — © 2026 Rylee Hulgan, all rights reserved |

#### `library/` — 14 file(s)

| Path | Origin | Evidence | Current license |
| --- | --- | --- | --- |
| `a-burned-page.md` | Cottage original (added after the scaffold snapshot) | `5249d0a` (2026-09-29) — lore: the intro lives on floor-1 | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `a-candle-and-a-note.md` | Cottage original (added after the scaffold snapshot) | `5249d0a` (2026-09-29) — lore: the intro lives on floor-1 | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `a-coin-face-down.md` | Cottage original (added after the scaffold snapshot) | `5249d0a` (2026-09-29) — lore: the intro lives on floor-1 | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `a-letter-in-a-chest.md` | Cottage original (added after the scaffold snapshot) | `3d13610` (2026-09-29) — lore: a chest on floor-1 holds a letter | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `a-note-left-at-the-door.md` | Cottage original (added after the scaffold snapshot) | `559fa31` (2026-09-29) — pack: a note lies by the cottage door | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `a-note-under-the-seal.md` | Cottage original (added after the scaffold snapshot) | `5a99a64` (2026-10-03) — Release 1: the Keybearer ladder, the King's room, an endi… | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `a-scrap-in-the-dust.md` | Cottage original (added after the scaffold snapshot) | `5249d0a` (2026-09-29) — lore: the intro lives on floor-1 | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `about-this-game.md` | Cottage original (added after the scaffold snapshot) | `5a99a64` (2026-10-03) — Release 1: the Keybearer ladder, the King's room, an endi… | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `forty-winters.md` | Cottage original (added after the scaffold snapshot) | `e2c5617` (2026-10-12) — section 1: the household, the King who yields, and the to… | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `the-burnt-taverns-tab.md` | Cottage original (added after the scaffold snapshot) | `7b85c92` (2026-09-29) — pack: Act 1's story layer, drafted from NOTES | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `the-old-mushroom.md` | Cottage original (added after the scaffold snapshot) | `e2c5617` (2026-10-12) — section 1: the household, the King who yields, and the to… | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `the-pale-moth.md` | Cottage original (added after the scaffold snapshot) | `e2c5617` (2026-10-12) — section 1: the household, the King who yields, and the to… | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `the-stag-beetle.md` | Cottage original (added after the scaffold snapshot) | `e2c5617` (2026-10-12) — section 1: the household, the King who yields, and the to… | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `writing-a-book.md` | **Unknown** — engine how-to text copied into the pack | `21888b7` (2026-09-26) — pack: clear Emberfield's leftovers; add the how-to book | Unknown — not established |

#### `props/` — 42 file(s)

| Path | Origin | Evidence | Current license |
| --- | --- | --- | --- |
| `anvil.webp` | Cottage original (added after the scaffold snapshot) | `2decb5e` (2026-10-12) — town: a bigger first village in Game Boy Advance pixel art | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `bar.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `barrel-rack.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `barrel.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `barrels.webp` | Cottage original (added after the scaffold snapshot) | `2decb5e` (2026-10-12) — town: a bigger first village in Game Boy Advance pixel art | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `bed.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `bench-table.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `bench.webp` | Cottage original (added after the scaffold snapshot) | `2decb5e` (2026-10-12) — town: a bigger first village in Game Boy Advance pixel art | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `burned-tavern.webp` | Cottage original (added after the scaffold snapshot) | `2decb5e` (2026-10-12) — town: a bigger first village in Game Boy Advance pixel art | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `bush.webp` | Cottage original (added after the scaffold snapshot) | `2decb5e` (2026-10-12) — town: a bigger first village in Game Boy Advance pixel art | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `chimney-smoke.webp` | Cottage original (added after the scaffold snapshot) | `2decb5e` (2026-10-12) — town: a bigger first village in Game Boy Advance pixel art | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `cobweb.webp` | Cottage original (added after the scaffold snapshot) | `cf45f08` (2026-10-12) — Cellar decals dress the generated floors | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `cottage-house.webp` | Cottage original (added after the scaffold snapshot) | `2decb5e` (2026-10-12) — town: a bigger first village in Game Boy Advance pixel art | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `crates.webp` | Cottage original (added after the scaffold snapshot) | `2decb5e` (2026-10-12) — town: a bigger first village in Game Boy Advance pixel art | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `doormat.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `drawers.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `fallen-stones.webp` | Cottage original (added after the scaffold snapshot) | `cf45f08` (2026-10-12) — Cellar decals dress the generated floors | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `fireplace.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `floor-crack.webp` | Cottage original (added after the scaffold snapshot) | `cf45f08` (2026-10-12) — Cellar decals dress the generated floors | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `floor-grate.webp` | Cottage original (added after the scaffold snapshot) | `cf45f08` (2026-10-12) — Cellar decals dress the generated floors | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `floor-roots.webp` | Cottage original (added after the scaffold snapshot) | `cf45f08` (2026-10-12) — Cellar decals dress the generated floors | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `flowers.webp` | Cottage original (added after the scaffold snapshot) | `2decb5e` (2026-10-12) — town: a bigger first village in Game Boy Advance pixel art | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `forge.webp` | Cottage original (added after the scaffold snapshot) | `2decb5e` (2026-10-12) — town: a bigger first village in Game Boy Advance pixel art | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `hearth.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `kitchen-table.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `lamp-post.webp` | Cottage original (added after the scaffold snapshot) | `2decb5e` (2026-10-12) — town: a bigger first village in Game Boy Advance pixel art | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `market-stall.webp` | Cottage original (added after the scaffold snapshot) | `2decb5e` (2026-10-12) — town: a bigger first village in Game Boy Advance pixel art | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `pond.webp` | Cottage original (added after the scaffold snapshot) | `2decb5e` (2026-10-12) — town: a bigger first village in Game Boy Advance pixel art | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `puddle.webp` | Cottage original (added after the scaffold snapshot) | `cf45f08` (2026-10-12) — Cellar decals dress the generated floors | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `roped-road.webp` | Cottage original (added after the scaffold snapshot) | `2decb5e` (2026-10-12) — town: a bigger first village in Game Boy Advance pixel art | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `rug-oval.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `sheeted-crates.webp` | Cottage original (added after the scaffold snapshot) | `cf45f08` (2026-10-12) — Cellar decals dress the generated floors | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `shelf.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `signpost.webp` | Cottage original (added after the scaffold snapshot) | `2decb5e` (2026-10-12) — town: a bigger first village in Game Boy Advance pixel art | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `tavern-table.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `tavern.webp` | Cottage original (added after the scaffold snapshot) | `2decb5e` (2026-10-12) — town: a bigger first village in Game Boy Advance pixel art | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `temple-open.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `temple.webp` | Cottage original (added after the scaffold snapshot) | `2decb5e` (2026-10-12) — town: a bigger first village in Game Boy Advance pixel art | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `tree.webp` | Cottage original (added after the scaffold snapshot) | `2decb5e` (2026-10-12) — town: a bigger first village in Game Boy Advance pixel art | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `vegetable-garden.webp` | Cottage original (added after the scaffold snapshot) | `2decb5e` (2026-10-12) — town: a bigger first village in Game Boy Advance pixel art | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `wall-torch.webp` | Cottage original (added after the scaffold snapshot) | `cf45f08` (2026-10-12) — Cellar decals dress the generated floors | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `well.webp` | Cottage original (added after the scaffold snapshot) | `2decb5e` (2026-10-12) — town: a bigger first village in Game Boy Advance pixel art | Reserved — © 2026 Rylee Hulgan, all rights reserved |

#### `sections/` — 4 file(s)

| Path | Origin | Evidence | Current license |
| --- | --- | --- | --- |
| `cellar.json` | Cottage original (added after the scaffold snapshot) | `d8b55c3` (2026-10-08) — feat(dungeon): a DRAFT generated descent, so there is a S… | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `emberhall.json` | Cottage original (added after the scaffold snapshot) | `eadc5ec` (2026-10-09) — feat(sections): rootworks, siltworks and emberhall - the … | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `rootworks.json` | Cottage original (added after the scaffold snapshot) | `eadc5ec` (2026-10-09) — feat(sections): rootworks, siltworks and emberhall - the … | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `siltworks.json` | Cottage original (added after the scaffold snapshot) | `eadc5ec` (2026-10-09) — feat(sections): rootworks, siltworks and emberhall - the … | Reserved — © 2026 Rylee Hulgan, all rights reserved |

#### `skins/parchment-and-wood/` — 21 file(s)

| Path | Origin | Evidence | Current license |
| --- | --- | --- | --- |
| `backdrop-alt-1.webp` | Cottage original (added after the scaffold snapshot) | `f06b2a8` (2026-10-07) — feat(skin): the pack opts into the themed interface — Cri… | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `banner.webp` | Cottage original (added after the scaffold snapshot) | `3c3c6bd` (2026-10-02) — game: the parchment-and-wood skin is in the pack | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `bar-fill.webp` | Cottage original (added after the scaffold snapshot) | `3c3c6bd` (2026-10-02) — game: the parchment-and-wood skin is in the pack | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `bar-frame.webp` | Cottage original (added after the scaffold snapshot) | `3c3c6bd` (2026-10-02) — game: the parchment-and-wood skin is in the pack | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `button-disabled.webp` | Cottage original (added after the scaffold snapshot) | `3c3c6bd` (2026-10-02) — game: the parchment-and-wood skin is in the pack | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `button-hover.webp` | Cottage original (added after the scaffold snapshot) | `3c3c6bd` (2026-10-02) — game: the parchment-and-wood skin is in the pack | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `button-pressed.webp` | Cottage original (added after the scaffold snapshot) | `3c3c6bd` (2026-10-02) — game: the parchment-and-wood skin is in the pack | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `button.webp` | Cottage original (added after the scaffold snapshot) | `3c3c6bd` (2026-10-02) — game: the parchment-and-wood skin is in the pack | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `corner.webp` | Cottage original (added after the scaffold snapshot) | `3c3c6bd` (2026-10-02) — game: the parchment-and-wood skin is in the pack | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `cursor.webp` | Cottage original (added after the scaffold snapshot) | `3c3c6bd` (2026-10-02) — game: the parchment-and-wood skin is in the pack | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `divider.webp` | Cottage original (added after the scaffold snapshot) | `3c3c6bd` (2026-10-02) — game: the parchment-and-wood skin is in the pack | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `gold-plate.webp` | Cottage original (added after the scaffold snapshot) | `3c3c6bd` (2026-10-02) — game: the parchment-and-wood skin is in the pack | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `panel.webp` | Cottage original (added after the scaffold snapshot) | `3c3c6bd` (2026-10-02) — game: the parchment-and-wood skin is in the pack | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `skin.json` | Cottage original (added after the scaffold snapshot) | `3c3c6bd` (2026-10-02) — game: the parchment-and-wood skin is in the pack | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `slot.webp` | Cottage original (added after the scaffold snapshot) | `3c3c6bd` (2026-10-02) — game: the parchment-and-wood skin is in the pack | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `speech.webp` | Cottage original (added after the scaffold snapshot) | `3c3c6bd` (2026-10-02) — game: the parchment-and-wood skin is in the pack | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `tab-selected.webp` | Cottage original (added after the scaffold snapshot) | `3c3c6bd` (2026-10-02) — game: the parchment-and-wood skin is in the pack | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `tab.webp` | Cottage original (added after the scaffold snapshot) | `3c3c6bd` (2026-10-02) — game: the parchment-and-wood skin is in the pack | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `toggle-off.webp` | Cottage original (added after the scaffold snapshot) | `3c3c6bd` (2026-10-02) — game: the parchment-and-wood skin is in the pack | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `toggle-on.webp` | Cottage original (added after the scaffold snapshot) | `3c3c6bd` (2026-10-02) — game: the parchment-and-wood skin is in the pack | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `tooltip.webp` | Cottage original (added after the scaffold snapshot) | `3c3c6bd` (2026-10-02) — game: the parchment-and-wood skin is in the pack | Reserved — © 2026 Rylee Hulgan, all rights reserved |

#### `sprites/` — 147 file(s)

| Path | Origin | Evidence | Current license |
| --- | --- | --- | --- |
| `CREDITS-release1.md` | Cottage original (added after the scaffold snapshot) | `5a99a64` (2026-10-03) — Release 1: the Keybearer ladder, the King's room, an endi… | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `barrel-mimic-sheet.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `barrel-mimic.png` | Cottage original (added after the scaffold snapshot) | `5a99a64` (2026-10-03) — Release 1: the Keybearer ladder, the King's room, an endi… | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `barrel-mimic.sheet.json` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `barrel-mimic.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `bird-feather.png` | Cottage original (added after the scaffold snapshot) | `a54c4e3` (2026-10-09) — feat(album): the album keeps what still fits - 19 sticker… | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `bird-feather.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `candle-stub.png` | Cottage original (added after the scaffold snapshot) | `a54c4e3` (2026-10-09) — feat(album): the album keeps what still fits - 19 sticker… | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `candle-stub.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `cat-sheet.webp` | Cottage original (added after the scaffold snapshot) | `2decb5e` (2026-10-12) — town: a bigger first village in Game Boy Advance pixel art | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `cat.png` | Cottage original (added after the scaffold snapshot) | `3474239` (2026-10-01) — game: the new art and five new residents in Cottage | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `cat.sheet.json` | Cottage original (added after the scaffold snapshot) | `2decb5e` (2026-10-12) — town: a bigger first village in Game Boy Advance pixel art | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `cat.webp` | Cottage original (added after the scaffold snapshot) | `2decb5e` (2026-10-12) — town: a bigger first village in Game Boy Advance pixel art | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `cave-cricket-sheet.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `cave-cricket.png` | Cottage original (added after the scaffold snapshot) | `5a99a64` (2026-10-03) — Release 1: the Keybearer ladder, the King's room, an endi… | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `cave-cricket.sheet.json` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `cave-cricket.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `cellar-king-sheet.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `cellar-king.png` | Cottage original (added after the scaffold snapshot) | `5a99a64` (2026-10-03) — Release 1: the Keybearer ladder, the King's room, an endi… | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `cellar-king.sheet.json` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `cellar-king.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `cellar-spider-sheet.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `cellar-spider.png` | Cottage original (added after the scaffold snapshot) | `5a99a64` (2026-10-03) — Release 1: the Keybearer ladder, the King's room, an endi… | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `cellar-spider.sheet.json` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `cellar-spider.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `cobweb-wraith-sheet.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `cobweb-wraith.png` | Cottage original (added after the scaffold snapshot) | `5a99a64` (2026-10-03) — Release 1: the Keybearer ladder, the King's room, an endi… | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `cobweb-wraith.sheet.json` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `cobweb-wraith.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `cold-ember.png` | Cottage original (added after the scaffold snapshot) | `a54c4e3` (2026-10-09) — feat(album): the album keeps what still fits - 19 sticker… | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `cold-ember.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `copper-ladle.png` | Cottage original (added after the scaffold snapshot) | `5a99a64` (2026-10-03) — Release 1: the Keybearer ladder, the King's room, an endi… | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `copper-ladle.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `crock-mimic-sheet.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `crock-mimic.png` | Cottage original (added after the scaffold snapshot) | `5a99a64` (2026-10-03) — Release 1: the Keybearer ladder, the King's room, an endi… | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `crock-mimic.sheet.json` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `crock-mimic.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `dust-moth-sheet.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `dust-moth.sheet.json` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `dust-moth.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `dwarf-smith-sheet.webp` | Cottage original (added after the scaffold snapshot) | `2decb5e` (2026-10-12) — town: a bigger first village in Game Boy Advance pixel art | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `dwarf-smith.png` | Cottage original (added after the scaffold snapshot) | `3474239` (2026-10-01) — game: the new art and five new residents in Cottage | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `dwarf-smith.sheet.json` | Cottage original (added after the scaffold snapshot) | `2decb5e` (2026-10-12) — town: a bigger first village in Game Boy Advance pixel art | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `dwarf-smith.webp` | Cottage original (added after the scaffold snapshot) | `2decb5e` (2026-10-12) — town: a bigger first village in Game Boy Advance pixel art | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `fisher-sheet.webp` | Cottage original (added after the scaffold snapshot) | `2decb5e` (2026-10-12) — town: a bigger first village in Game Boy Advance pixel art | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `fisher.png` | Cottage original (added after the scaffold snapshot) | `3474239` (2026-10-01) — game: the new art and five new residents in Cottage | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `fisher.sheet.json` | Cottage original (added after the scaffold snapshot) | `2decb5e` (2026-10-12) — town: a bigger first village in Game Boy Advance pixel art | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `fisher.webp` | Cottage original (added after the scaffold snapshot) | `2decb5e` (2026-10-12) — town: a bigger first village in Game Boy Advance pixel art | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `gardener-sheet.webp` | Cottage original (added after the scaffold snapshot) | `2decb5e` (2026-10-12) — town: a bigger first village in Game Boy Advance pixel art | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `gardener.png` | Cottage original (added after the scaffold snapshot) | `3474239` (2026-10-01) — game: the new art and five new residents in Cottage | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `gardener.sheet.json` | Cottage original (added after the scaffold snapshot) | `2decb5e` (2026-10-12) — town: a bigger first village in Game Boy Advance pixel art | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `gardener.webp` | Cottage original (added after the scaffold snapshot) | `2decb5e` (2026-10-12) — town: a bigger first village in Game Boy Advance pixel art | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `gems.png` | Cottage original (added after the scaffold snapshot) | `5a99a64` (2026-10-03) — Release 1: the Keybearer ladder, the King's room, an endi… | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `gems.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `hearth-poker.png` | Cottage original (added after the scaffold snapshot) | `5a99a64` (2026-10-03) — Release 1: the Keybearer ladder, the King's room, an endi… | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `hearth-poker.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `hero-sheet.png` | Cottage original (added after the scaffold snapshot) | `26c21ee` (2026-10-04) — Release 1 polish: walk cycles, sound, bot checks | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `hero-sheet.webp` | Cottage original (added after the scaffold snapshot) | `2decb5e` (2026-10-12) — town: a bigger first village in Game Boy Advance pixel art | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `hero.png` | Cottage original (added after the scaffold snapshot) | `abab3e3` (2026-09-29) — art: the Spell Keeper and the hero, on the map | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `hero.sheet.json` | Cottage original (added after the scaffold snapshot) | `26c21ee` (2026-10-04) — Release 1 polish: walk cycles, sound, bot checks | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `hero.webp` | Cottage original (added after the scaffold snapshot) | `2decb5e` (2026-10-12) — town: a bigger first village in Game Boy Advance pixel art | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `jam-jar-lid.png` | Cottage original (added after the scaffold snapshot) | `a54c4e3` (2026-10-09) — feat(album): the album keeps what still fits - 19 sticker… | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `jam-jar-lid.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `keeper-sheet.webp` | Cottage original (added after the scaffold snapshot) | `2decb5e` (2026-10-12) — town: a bigger first village in Game Boy Advance pixel art | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `keeper.png` | Cottage original (added after the scaffold snapshot) | `abab3e3` (2026-09-29) — art: the Spell Keeper and the hero, on the map | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `keeper.sheet.json` | Cottage original (added after the scaffold snapshot) | `2decb5e` (2026-10-12) — town: a bigger first village in Game Boy Advance pixel art | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `keeper.webp` | Cottage original (added after the scaffold snapshot) | `2decb5e` (2026-10-12) — town: a bigger first village in Game Boy Advance pixel art | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `key-bell.png` | Cottage original (added after the scaffold snapshot) | `5a99a64` (2026-10-03) — Release 1: the Keybearer ladder, the King's room, an endi… | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `key-bell.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `key-helmet.png` | Cottage original (added after the scaffold snapshot) | `5a99a64` (2026-10-03) — Release 1: the Keybearer ladder, the King's room, an endi… | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `key-helmet.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `key-lantern.png` | Cottage original (added after the scaffold snapshot) | `5a99a64` (2026-10-03) — Release 1: the Keybearer ladder, the King's room, an endi… | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `key-lantern.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `keybearer-beetle-sheet.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `keybearer-beetle.png` | Cottage original (added after the scaffold snapshot) | `5a99a64` (2026-10-03) — Release 1: the Keybearer ladder, the King's room, an endi… | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `keybearer-beetle.sheet.json` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `keybearer-beetle.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `keybearer-moth-sheet.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `keybearer-moth.png` | Cottage original (added after the scaffold snapshot) | `5a99a64` (2026-10-03) — Release 1: the Keybearer ladder, the King's room, an endi… | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `keybearer-moth.sheet.json` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `keybearer-moth.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `keybearer-mushroom-sheet.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `keybearer-mushroom.png` | Cottage original (added after the scaffold snapshot) | `5a99a64` (2026-10-03) — Release 1: the Keybearer ladder, the King's room, an endi… | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `keybearer-mushroom.sheet.json` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `keybearer-mushroom.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `mended-boots.png` | Cottage original (added after the scaffold snapshot) | `5a99a64` (2026-10-03) — Release 1: the Keybearer ladder, the King's room, an endi… | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `mended-boots.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `moth-wing.png` | Cottage original (added after the scaffold snapshot) | `a54c4e3` (2026-10-09) — feat(album): the album keeps what still fits - 19 sticker… | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `moth-wing.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `moths.png` | Cottage original (added after the scaffold snapshot) | `8792d1a` (2026-10-01) — game: monsters wear their art | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `moths.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `music-box-spring.png` | Cottage original (added after the scaffold snapshot) | `a54c4e3` (2026-10-09) — feat(album): the album keeps what still fits - 19 sticker… | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `music-box-spring.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `patched-apron.png` | Cottage original (added after the scaffold snapshot) | `5a99a64` (2026-10-03) — Release 1: the Keybearer ladder, the King's room, an endi… | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `patched-apron.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `pot-lid-helm.png` | Cottage original (added after the scaffold snapshot) | `5a99a64` (2026-10-03) — Release 1: the Keybearer ladder, the King's room, an endi… | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `pot-lid-helm.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `potion.png` | Cottage original (added after the scaffold snapshot) | `92f3731` (2026-09-29) — pack: item drops and a bag | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `potion.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `quilted-coat.png` | Cottage original (added after the scaffold snapshot) | `5a99a64` (2026-10-03) — Release 1: the Keybearer ladder, the King's room, an endi… | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `quilted-coat.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `rat-sheet.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `rat-tooth.png` | Cottage original (added after the scaffold snapshot) | `a54c4e3` (2026-10-09) — feat(album): the album keeps what still fits - 19 sticker… | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `rat-tooth.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `rat.png` | Cottage original (added after the scaffold snapshot) | `8792d1a` (2026-10-01) — game: monsters wear their art | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `rat.sheet.json` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `rat.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `ring.png` | Cottage original (added after the scaffold snapshot) | `92f3731` (2026-09-29) — pack: item drops and a bag | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `ring.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `root-tangle-sheet.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `root-tangle.png` | Cottage original (added after the scaffold snapshot) | `5a99a64` (2026-10-03) — Release 1: the Keybearer ladder, the King's room, an endi… | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `root-tangle.sheet.json` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `root-tangle.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `rustle-sheet.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `rustle.png` | Cottage original (added after the scaffold snapshot) | `8792d1a` (2026-10-01) — game: monsters wear their art | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `rustle.sheet.json` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `rustle.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `seal-crown.png` | Cottage original (added after the scaffold snapshot) | `5a99a64` (2026-10-03) — Release 1: the Keybearer ladder, the King's room, an endi… | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `seal-crown.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `shade-sheet.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `shade.png` | Cottage original (added after the scaffold snapshot) | `8792d1a` (2026-10-01) — game: monsters wear their art | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `shade.sheet.json` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `shade.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `shoe-button.png` | Cottage original (added after the scaffold snapshot) | `a54c4e3` (2026-10-09) — feat(album): the album keeps what still fits - 19 sticker… | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `shoe-button.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `spider-silk.png` | Cottage original (added after the scaffold snapshot) | `a54c4e3` (2026-10-09) — feat(album): the album keeps what still fits - 19 sticker… | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `spider-silk.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `tavern-regular-sheet.webp` | Cottage original (added after the scaffold snapshot) | `2decb5e` (2026-10-12) — town: a bigger first village in Game Boy Advance pixel art | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `tavern-regular.png` | Cottage original (added after the scaffold snapshot) | `3474239` (2026-10-01) — game: the new art and five new residents in Cottage | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `tavern-regular.sheet.json` | Cottage original (added after the scaffold snapshot) | `2decb5e` (2026-10-12) — town: a bigger first village in Game Boy Advance pixel art | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `tavern-regular.webp` | Cottage original (added after the scaffold snapshot) | `2decb5e` (2026-10-12) — town: a bigger first village in Game Boy Advance pixel art | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `thimble.png` | Cottage original (added after the scaffold snapshot) | `a54c4e3` (2026-10-09) — feat(album): the album keeps what still fits - 19 sticker… | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `thimble.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `thread-bell.png` | Cottage original (added after the scaffold snapshot) | `5a99a64` (2026-10-03) — Release 1: the Keybearer ladder, the King's room, an endi… | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `thread-bell.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `toad-sheet.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `toad.png` | Cottage original (added after the scaffold snapshot) | `5a99a64` (2026-10-03) — Release 1: the Keybearer ladder, the King's room, an endi… | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `toad.sheet.json` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `toad.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `trader-sheet.webp` | Cottage original (added after the scaffold snapshot) | `2decb5e` (2026-10-12) — town: a bigger first village in Game Boy Advance pixel art | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `trader.png` | Cottage original (added after the scaffold snapshot) | `8857482` (2026-09-29) — pack: The Trader, a stall on the road | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `trader.sheet.json` | Cottage original (added after the scaffold snapshot) | `2decb5e` (2026-10-12) — town: a bigger first village in Game Boy Advance pixel art | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `trader.webp` | Cottage original (added after the scaffold snapshot) | `2decb5e` (2026-10-12) — town: a bigger first village in Game Boy Advance pixel art | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `wick-sprite-sheet.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `wick-sprite.png` | Cottage original (added after the scaffold snapshot) | `5a99a64` (2026-10-03) — Release 1: the Keybearer ladder, the King's room, an endi… | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `wick-sprite.sheet.json` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `wick-sprite.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |

#### `tiles/` — 11 file(s)

| Path | Origin | Evidence | Current license |
| --- | --- | --- | --- |
| `cellar-flagstone.grid3x3.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `cellar-wall.grid3x3.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `ember-flagstone.grid3x3.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `ember-wall.grid3x3.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `root-flagstone.grid3x3.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `root-wall.grid3x3.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `silt-flagstone.grid3x3.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `silt-wall.grid3x3.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `way-door.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `way-stairs-down.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `way-stairs-up.webp` | Cottage original (added after the scaffold snapshot) | `00f061b` (2026-10-12) — art: the rest of the GBA art set, drawn in OpenDesign | Reserved — © 2026 Rylee Hulgan, all rights reserved |

#### `voices/` — 1 file(s)

| Path | Origin | Evidence | Current license |
| --- | --- | --- | --- |
| `vendor.md` | Cottage original (added after the scaffold snapshot) | `8857482` (2026-09-29) — pack: The Trader, a stall on the road | Reserved — © 2026 Rylee Hulgan, all rights reserved |

## C. Outside the pack

The scaffold never reached the rest of the repo. `git ls-tree -r --name-only
cab23dd` lists exactly eleven files outside `worlds/`, and all eleven are
Cottage's own new-game kit — `AGENTS.md`, `BRIEF.md`, `DESIGN.md`,
`LICENSE.md`, `NOTES.md`, `README.md`, `STORY.md`, `.gitignore`,
`.project/CURRENT.md`, `art/mood/.gitkeep`, `art/source/.gitkeep`. There was
no vendored art, no sample license text and no third-party asset anywhere
outside the pack at the scaffold commit.

| Path | Origin | Evidence | Current license |
| --- | --- | --- | --- |
| `LICENSE.md`, `AGENTS.md`, `BRIEF.md`, `DESIGN.md`, `NOTES.md`, `README.md`, `STORY.md`, `.gitignore`, `.project/CURRENT.md` | Cottage original, written for this repo | In `cab23dd`; none descends from Emberfield | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `art/**` (originals, prompts, `.credits.txt`, `RECORD.md`, `PICKS.md`) | Cottage original — generated art and its provenance records | All added after `cab23dd` by art commits; every picture keeps its `.credits.txt` (see `art/README.md`) | Reserved — © 2026 Rylee Hulgan, all rights reserved |
| `docs/**`, `.github/**`, `.agent/**`, `tests/**`, `bin/**` | Cottage original — repo tooling and its own docs | All added after `cab23dd` | Reserved — © 2026 Rylee Hulgan, all rights reserved |

Two exclusions worth stating plainly, because they are the ones a reader might
expect to see in a CC0 list:

- **Kenney is gone.** `assets/kenney/` (CC0, prototyping-only) was removed in
  `69e34e9` (#53) after Rylee's 2026-10-02 art rule. No Kenney picture remains
  in the pack, so the pack LICENSE's old "Bundled art (`assets/`)" section was
  dropped in that same commit and is not restored here.
- **No LimeZu.** No LimeZu asset is present, consistent with the art rule in
  `AGENTS.md`.

## What this does not prove

Stated plainly, so the licence is not read as claiming more than the evidence
carries.

1. **This is provenance, not clearance.** The table establishes where each file
   came from. It does not establish that the scaffold could be relicensed,
   sublicensed, or shipped — CC0 already permits all of that, and this change
   does not attempt to alter a third-party licence.
2. **Inside the files, "Cottage original" is a git fact, not a copyright
   audit.** The 272 rows in §B record the commit that created each file. For
   the 213 pack images that record is backed by `art/source/**/CREDITS-release1.md`
   and `art/source/**/RECORD.md`; those records, not this table, are the
   attribution of record for each picture. Several pack images are cuts from
   bundled source sheets whose source file names differ from the cut names, so
   a per-file join has to be done by hand against the credits records.
3. **The credits' own training flags are unresolved.** The `training:` field in
   each `.credits.txt` (`not cleared` / `specialist-only` / `ok`) governs
   whether a picture may train a model. That question is separate from
   copyright and outside this issue; this table does not clear it.
4. **`library/writing-a-book.md` is Unknown, and stays Unknown.** It is
   engine how-to text copied into the pack in `21888b7` (#14). Whether VEFR
   ships it under CC0 is not recorded in this repo, and guessing would put an
   unevidenced licence claim into the pack. Resolving it means reading VEFR's
   own licence — a companion question for the engine repo, not this one.
5. **No public release is authorised by this.** Issue #175 is blocked on the
   before-any-public-release gate. This document and its PR do not cross it.
6. **Independent review before release.** Rylee's decision asks for the
   clarification to be backed by this manifest *and* independently reviewed
   before any public release. The manifest is the backing; the review is
   separate and still owed.

## Appendix A — the proposed licence wording

Applied in the same change. Both files keep every existing rights statement;
nothing is revoked and nothing is broadened.

### `worlds/cottage-of-the-breeze/LICENSE`

The inherited CC0 grant stays exactly where it is, in its own section, in the
order it arrived in. What replaces the path-wide reading is a new section
saying which fragments the grant reaches inside this pack:

> ## What this grant covers in this pack
>
> Added 2026-10-16 (cottage-of-the-breeze#175). The grant above is the
> Emberfield one, carried over with the scaffold and unchanged. It describes
> the sample world; this file was copied into this pack at `cab23dd` and
> renamed to `worlds/cottage-of-the-breeze/`.
>
> Only Emberfield scaffold text still present in this pack is CC0. Every path
> the grant names — `world.json`, `map.md`, `voices/`, `lore/`, contracts,
> "any prose or JSON" — now also holds Cottage's own writing, and none of that
> writing is CC0. The CC0 fragments, each byte-identical to `cab23dd`, are:
>
> | File | The CC0 fragment |
> | --- | --- |
> | `LICENSE` | this file's own CC0 grant (the notice itself) |
> | `world.json` | `phases.*`, `surface`, `voices.keeper.strike`, `bonds.*.card`, `bonds.*.prompt`, `bond_draw`, `forge_texture` |
> | `acts/act-1/world.json` | `id`, `regions`, `speakers.keeper.voice_file`, empty `enemies` / `bosses` |
> | `acts/act-1/town/contract.json` | `tile`, `bg`, `hero_color`, `speaker_color`, `speaker_head`, `sanctuary_tiles`, `water_by_phase` |
> | `ledger.md` | the four-line header |
> | `voices/keeper.fragments.md` | lines 2–5 of the preamble |
> | `voices/keeper.md`, `acts/act-1/town/voices/keeper.md` | `- No modern words. Never explain. Show only.` |
> | `world-tree.md` | the `## The World Tree` heading |
>
> Everything else in this pack — story, residents and their lines,
> `logbok.md`, the books in `library/`, lore, contract templates, maps, and
> every picture under `assets/`, `sprites/`, `props/`, `tiles/` and `skins/` —
> is © 2026 Rylee Hulgan, all rights reserved. One file,
> `library/writing-a-book.md`, is engine how-to text of unestablished licence
> and is recorded as unknown.
>
> File-by-file evidence: `docs/research/2026-10-16-license-provenance.md`.
>
> This section withdraws nothing. The CC0 dedication above stands for the
> scaffold text; it only says which text that is.

### `LICENSE.md` (repo root)

> Exception: the Emberfield scaffold text that still sits in the pack keeps
> the CC0 dedication it arrived with. `worlds/cottage-of-the-breeze/LICENSE`
> lists exactly which fragments those are, and
> `docs/research/2026-10-16-license-provenance.md` holds the file-by-file
> evidence. All original Cottage material — art, story, voices, lore,
> contract templates, books — is outside that dedication.

The old sentence "It is placeholder, to be replaced." goes: it is no longer
true. Nine of the twelve scaffold files were rewritten within three days of
the scaffold commit, and none of the 284 pack files is a scaffold placeholder
today.

## Appendix B — the commands this table came from

Run from the repo root.

```sh
# 1. The scaffold snapshot, and the files that are still in it
git ls-tree -r --name-only cab23dd -- worlds/cottage-of-the-breeze
git ls-files worlds/cottage-of-the-breeze | sort > now.txt
comm -12 <(git ls-tree -r --name-only cab23dd -- worlds/cottage-of-the-breeze | sort) now.txt

# 2. Which inherited files still hold inherited text, line for line
for f in $(git ls-tree -r --name-only cab23dd -- worlds/cottage-of-the-breeze); do
  case "$f" in *.json) continue ;; esac
  git ls-files --error-unmatch "$f" >/dev/null 2>&1 || continue
  echo "== $f"
  comm -12 <(git show cab23dd:"$f" | sed '/^[[:space:]]*$/d' | sort -u) \
           <(sed '/^[[:space:]]*$/d' "$f" | sort -u)
done

# 3. The same question for JSON: leaf values that did not change
python3 - <<'PY'
import json, subprocess
for f in ['worlds/cottage-of-the-breeze/world.json',
          'worlds/cottage-of-the-breeze/acts/act-1/world.json',
          'worlds/cottage-of-the-breeze/acts/act-1/town/contract.json']:
    walk = lambda o, p='': (
        [(p, o)] if not isinstance(o, (dict, list)) else
        [x for k, v in o.items() for x in walk(v, f'{p}.{k}' if p else k)] if isinstance(o, dict) else
        [x for i, v in enumerate(o) for x in walk(v, f'{p}[{i}]')])
    init = dict(walk(json.loads(subprocess.run(
        ['git', 'show', f'cab23dd:{f}'], capture_output=True, text=True).stdout)))
    head = dict(walk(json.load(open(f))))
    print('##', f)
    for p, v in init.items():
        if p in head and head[p] == v:
            print('  SAME   ', p, '=', repr(v)[:70])
PY

# 4. Nothing inherited is byte-identical any more
for f in $(comm -12 <(git ls-tree -r --name-only cab23dd -- worlds/cottage-of-the-breeze | sort) now.txt); do
  git diff --quiet cab23dd HEAD -- "$f" && echo "UNCHANGED $f" || echo "MODIFIED  $f"
done

# 5. The two licence histories the issue asked to be verified
git log --format='%h %ad %s' --date=short -- LICENSE.md
git log --format='%h %ad %s' --date=short -- worlds/cottage-of-the-breeze/LICENSE

# 6. Where each later file came from
git log --reverse --diff-filter=A --name-only --format='%h %ad %s' --date=short -- worlds/
```

## Where this leaves #175

- [x] File-by-file provenance inventory, with evidence, marked unknown where
      evidence is absent.
- [x] The narrowest clarification drafted: CC0 stays on the proven fragments,
      the path-wide wording is gone, no existing grant is revoked and none is
      broadened.
- [ ] **Independent review** before any public release (Rylee's decision).
- [ ] **`library/writing-a-book.md`** — resolve against VEFR's own licence, or
      replace it with Cottage's own words. Tracked as Unknown in the meantime.
- [ ] **Public release gate** — untouched; #175 stays blocked on it.

Related but deliberately not touched by this change:
[`docs/repo-map.md`](../repo-map.md) still says "The pack is still mostly
scaffold", which this research shows is no longer true (12 of 284 files trace
to the scaffold, and none is unmodified). Correcting that sentence is a docs
follow-up, not part of the licence clarification.
