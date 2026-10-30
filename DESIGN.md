# DESIGN — the systems to rebuild

> Stage 2 grows this file. For now it's the checklist of *Castle of the
> Winds* systems, described in our own words from public descriptions of
> the game. Names, numbers and story are ours to decide.

## The soul (Rylee, 2026-10-08)

Her words: "No existing work is sacred except the soul of it". The soul, which
she confirmed when it was read back to her ("Yes, that's it"): curious,
low-bandwidth exploring; the thrill of opening something and finding something
fun; a cozy storybook world; no reflexes and nothing to memorize; 30 minutes
that turns into four hours. Judge every change against it.

## Where each system stands (2026-10-04, revised 2026-10-08)

| System | State |
| --- | --- |
| Town | Built: a cottage, a tavern with the Spell Keeper, the Trader's shop, a temple (where you wake) and the burned old tavern, seven residents. No identifier or bank yet; the temple has no inside yet. |
| Floors | Six floors: three authored, three generated at build time. The cellar is act 1, ending with the Cellar King, a sealed door and a room beyond (built). Per-run generation: phase 1 built. |
| Inventory | A bag (use, sell) and a worn-gear section with five slots (built). Carrying is decided as slots plus bag upgrades (2026-10-08); the grid-and-shapes design this file carried before is replaced, and bag upgrades are decided, not built yet. |
| Items | Potions, keys, a seal, gems and eight wearable items with painted icons. Rarity, traits and identifying are not built. |
| Growth | Built and on: classic levels. |
| Spells | Not built. |
| Time | Not built. |
| Books & notes | Built: ten, read in the game, plus a 25-sticker album, nine soft sounds and a walking hero. |

## Loop
Rest in town → go down → find things → come back up to trade, heal and
learn → go deeper.

## Systems

| System | What it does | VEFR ruleset |
|---|---|---|
| Town | Shops, a temple to heal, someone who identifies things, a bank. What the town gives is decided as "Rest, trade, identify" (2026-10-08); the bank is not part of that answer | existing town + Talk (later) |
| Floors | Each floor deeper and harder; stairs up and down | **Delve** (new) |
| Inventory | Slots plus bag upgrades (decided 2026-10-08). ~~Limits by weight *and* bulk, not slots; packs, belts and bags hold more~~ — replaced, struck | Delve |
| Items | Plain, cursed or enchanted; unknown until identified | Delve + Vault |
| Spells | Six schools (attack, defense, healing, movement, divination, other); learn one per level, or from spellbooks you find | Delve |
| Time | Time spent changes what merchants stock | Delve |
| Books & notes | Things you find and keep, written by Rylee | **Library** (new, first) |

## Decided
- **Losing:** the player picks Cozy (wake in the temple) or Classic (death
  is real) at the start; Classic can switch to Cozy, never back.
- **Time:** turn-based. Each step or action is one turn; then monsters act.
- **Carrying:** "Simpler: slots plus bag upgrades" (Rylee, 2026-10-08). Slots,
  and bags that upgrade into more slots. **Replaces** the grid-and-shapes design
  this file carried before (small grids per container, shaped items, a weight
  limit): it is gone from this list, and the Systems table row is struck.
  Decided, not built yet — the bag you can use and sell is built, bag upgrades
  are not. (Rylee loves inventory games: "I'm a diablo sucker".)
- **Town:** "Rest, trade, identify" (Rylee, 2026-10-08) — what the town gives
  you for going back up. Rest and trade exist (the temple, the Trader's shop);
  identify is decided, not built yet.
- **Danger:** "Rising" (Rylee, 2026-10-08) — gentle near the top, some fights to
  fear deeper down. Decided; the depth curve itself is not built yet.
- **Mood:** "Change by section" (Rylee, 2026-10-08) — each Section carries its
  own mood. Decided, not built yet.
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

## Decided (Rylee, 2026-10-30, after her first Gate 0 run)

Her words on the build: "I guess it feels easy? But it also feels like the levels
need some randomness. There are almost straight lines to every staircase". Then two
picks, in the words of the options she chose:

- **Floors:** "Rooms anywhere (Recommended)": rooms scatter over the whole map, and
  the way from stair to stair is a random walk that turns, climbs and can double
  back. Built as VEFR's `"layout": "wander"` (ADR 0022); the cellar uses it.
- **Difficulty:** "Harder (Recommended)": fights take 2-3 blows all the way down,
  rats stay gentle, deep spiders and fat rats hit through armour, levels come a bit
  slower, potions and Rest start to matter. The numbers are a first pass for her
  next run to correct (`NOTES.md`, 2026-10-30).

## Decided (Rylee, 2026-10-29)

Sixteen questions in four rounds; her picks in her words, and the full table in
[`docs/plans/release-1-0/LOOPS.md`](docs/plans/release-1-0/LOOPS.md#rylees-answers-2026-10-29).
Decided, not built yet.

- **Hits:** "Classic: misses and crits", rolled from the run's seed. Guard stays
  as armour.
- **Magic:** "spells and books with a mana cost for learned books and charges for
  spells": mana for spells learned from books, charges for spell things found.
- **Falling:** "Satchel contents" wait where you fell; levels, spells, books and
  worn gear are kept.
- **Going back down:** "Deepest landing only".
- **Traits:** "Mostly stats, some tricks".
- **Curses:** "Take it off at any time and any cursed items have a deliberate
  upside to deliberate": removable any time, every curse a trade-off.
- **Carrying:** "Bags in town upgrade by 5s. In dungeons bags can drop rarely with
  more slots or slots + enchantments". Base 10 slots (Claude's call).
- **Identify:** "The Spell Keeper".
- **Fight row:** "Strike, Cast if known".
- **Wardens:** "Each its own way". **Keybearers:** "Asleep in Section 1".
- **Sections 2–4:** "You decide. Best game 💗": rebuilt as canon's Long Well,
  Banked Fire and Blue Door; Section 4 is generated floors past the Blue Door to
  the unburnt room (Claude's calls, made at her request).
- **New words:** "I draft, you approve batches". **Engine work:** "One big PR per
  gate".

## Order
1. **Library**: books and notes found in the world, kept, fed to the book export.
2. **Delve**: floors, items, weight, spells, turns (what the VEFR ruleset
   covers; what you carry is slots plus bag upgrades, above).
3. **Loot**, then **spells**, then the E8 vaults (Rylee, 2026-10-08): loot
   comes "Before E8 vaults", spells "After loot". Decided; not built yet.
