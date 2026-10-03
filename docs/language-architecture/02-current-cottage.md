# 02 · Current Cottage (reverified 2026-10-02)

Private companion to the public Phase A packet in the VEFR repo (`docs/research/language-architecture/`, PR #219). Structure only: no story is read, invented or promoted here. Canon is Rylee's.

| Fact | Evidence |
|---|---|
| `main` is `c86c18a`, no open PRs when checked | `git log`, `git status -sb` |
| Pack lives at `worlds/cottage-of-the-breeze/` (`world.json`, `acts/`, `assets/`, `library/`) | `ls` |
| 9 region contracts: town, tavern, cottage, floors 1–6 | `acts/*/*/contract.json` |
| 69 enemy records | summed from the contracts |
| Growth: classic `levels`, XP table `[0,6,15,30,55,95,150,230]` (8 levels), gain hp +2 atk +1 | `world.json` `growth` |
| 2 rules: `the-letter-read` (`reads`) and `the-keeper-knows` (`comes-near`), both `once`, both `set` then `say` | `world.json` `rules` |
| 8 files in `library/` | `ls library` |
| `world.json` has no version or schema key | key list |
| Top-level keys: bond_draw, bonds, creed, description, flags, forge_texture, growth, items, name, phases, player, rules, skin, surface, title, voices | key list |

Floors 1–3 are authored; 4–6 are generated and dressed (per the plan; not rechecked here).

## Repetition that matters

Groups where every scalar (`name`, `sprite`, `hp`, `atk`, `xp`) is identical within a region:

| Region | Creature | Count | Shared scalars |
|---|---|---|---|
| floor-2 | moths | 3 | a nest of moths, hp 3, atk 1, xp 2 |
| floor-2 | shade | 3 | a damp shade, hp 5, atk 1, xp 3 (each also has `drops`) |
| floor-3 | moths | 2 | same as floor-2 moths |
| floor-4 | moths | 2 | hp **4** |
| floor-4, 5, 6 | rat | 2 each | a fat cellar rat, hp 6, atk 1, xp 3 (each has `drops`) |
| floor-5, 6 | moths | 3 each | hp 4 |

Only `id`, `at` and sometimes `drops` differ inside a group. Across regions the same creature recurs with a depth-dependent `hp` (moths 3 on floors 2–3, 4 on floors 4–6). That is the case a family with a per-depth override fits.

Floor 1 is not uniform (rats there differ in stats), so a runner that assumes a uniform group fails on `floor-1/rat`. This is expected, not a bug.

## Not checked

The other region contracts' map rows, the library text, `STORY.md`, guardians (unwired), and the second rule through the engine.
