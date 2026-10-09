# Cottage of the Breeze 🌬️🏡

The VEFR studio's first game: a cozy town-and-dungeon roguelike, rebuilt
system by system inside the [VEFR](https://github.com/Rylee-Bee/vefr) studio.
It's a learning remake of *Castle of the Winds* (1989): the systems are
rebuilt, and the name, story, art and words are our own.

It is also how the studio learns to make games, one handbook stage at a
time, and how VEFR grows: each new ruleset this game needs goes into the
engine, and every later game gets it for free.

| Want to… | Open |
|---|---|
| Know what this game is | [`BRIEF.md`](BRIEF.md) (stage 1: the pitch) |
| See the systems to rebuild | [`DESIGN.md`](DESIGN.md) |
| Read the canon | [`STORY.md`](STORY.md) (Rylee's words; none yet) |
| See decisions + playtest notes | [`NOTES.md`](NOTES.md) |
| Know where things stand | [`.project/CURRENT.md`](.project/CURRENT.md) |
| Rules for agents | [`AGENTS.md`](AGENTS.md) |

## Play it in the studio

The pack lives in `worlds/cottage-of-the-breeze/`. Rylee's VEFR checkout
sees it through a local, gitignored symlink; a fresh clone has neither.
Whether the Studio home shows it is UNKNOWN. Validate as CI does:

```sh
uvx --from "vefr @ git+https://github.com/Rylee-Bee/vefr@b5ed13dbe444d9eb0ee1e0cb1bf03300135dea3f" norns validate --pack worlds/cottage-of-the-breeze
```

## Layout

```
cottage-of-the-breeze/
  BRIEF.md  DESIGN.md  STORY.md  NOTES.md      the new-game kit
  art/mood/  art/source/                        empty; originals + prompts
  worlds/cottage-of-the-breeze/                 the VEFR pack
  .project/CURRENT.md                           where things stand
```
