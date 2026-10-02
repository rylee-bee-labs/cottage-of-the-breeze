# DESIGN — the systems to rebuild

> Stage 2 grows this file. For now it's the checklist of *Castle of the
> Winds* systems, described in our own words from public descriptions of
> the game. Names, numbers and story are ours to decide.

## Where each system stands (2026-10-02)

| System | State |
| --- | --- |
| Town | Built: a cottage, a tavern with the Spell Keeper, the Trader's shop, a temple (where you wake) and the burned old tavern, seven residents. No identifier or bank yet; the temple has no inside yet. |
| Floors | Six floors: three authored, three generated at build time. The cellar is act 1, ending with the Cellar King (designed). Per-run generation: phase 1 built. |
| Inventory | A simple bag (use, sell). The grid-and-shapes design below is not built. |
| Items | Two kinds (a potion and a ring), eight icons and a set of gear and key pictures drawn. Rarity, traits and identifying are not built. |
| Growth | Built and on: classic levels. |
| Spells | Not built. |
| Time | Not built. |
| Books & notes | Built: eight, read in the game. |

## Loop
Rest in town → go down → find things → come back up to trade, heal and
learn → go deeper.

## Systems

| System | What it does | VEFR ruleset |
|---|---|---|
| Town | Shops, a temple to heal, someone who identifies things, a bank | existing town + Talk (later) |
| Floors | Each floor deeper and harder; stairs up and down | **Delve** (new) |
| Inventory | Limits by weight *and* bulk, not slots; packs, belts and bags hold more | Delve |
| Items | Plain, cursed or enchanted; unknown until identified | Delve + Vault |
| Spells | Six schools (attack, defense, healing, movement, divination, other); learn one per level, or from spellbooks you find | Delve |
| Time | Time spent changes what merchants stock | Delve |
| Books & notes | Things you find and keep, written by Rylee | **Library** (new, first) |

## Decided
- **Losing:** the player picks Cozy (wake in the temple) or Classic (death
  is real) at the start; Classic can switch to Cozy, never back.
- **Time:** turn-based. Each step or action is one turn; then monsters act.
- **Carrying:** grids inside containers. Each container is its own small
  grid (a backpack 6×4, a belt 4×1 for quick potions, a pouch 2×2) and
  items have shapes (a sword 1×3, armor 2×3, a ring 1×1). A bigger pack
  or another pouch is a real upgrade. A gentle weight limit keeps hauling
  armor home feeling heavy. (Rylee loves inventory games: "I'm a diablo
  sucker".)
- **Floors:** generated from rules and a seed once per game, then
  remembered for that playthrough. Hand-drawn floors can replace any
  generated one.
- **Loot:** rolled, not placed. Base item + rarity (common, fine, rare,
  heroic, mythic: shown as a glow, a word and a frame shape, never colour
  alone) + random traits named from word tables. Rarity shows right away;
  traits stay hidden until identified. Opening a chest and identifying an
  item are small reveal moments (instant with motion off, a spin with
  motion on). Rylee: the fun of "opening and finding something fun", with
  randomized loot fed by the floor generator. Rules only; models help
  write the word lists in the studio.
- **Models:** none while playing. Every rule and number is fixed; every
  line is Rylee's or drafted in the studio and approved, then baked in.

## Order
1. **Library**: books and notes found in the world, kept, fed to the book export.
2. **Delve**: floors, items, weight, spells, turns.
