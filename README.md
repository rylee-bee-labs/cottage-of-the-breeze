# Cottage of the Breeze 🌬️🏡

The VEFR studio's first game: a cozy town-and-dungeon roguelike, rebuilt
room by room inside the [VEFR](https://github.com/Rylee-Bee/vefr) studio.
It's a learning remake of *Castle of the Winds* (1989): the systems are
rebuilt, and the name, story, art and words are our own.

It is also how the studio learns to make games, one handbook stage at a
time, and how VEFR grows: each new ruleset this game needs goes into the
engine, and every later game gets it for free.

| Want to… | Open |
|---|---|
| Know what this game is | [`BRIEF.md`](BRIEF.md) (stage 1: the pitch) |
| See the systems to rebuild | [`DESIGN.md`](DESIGN.md) |
| Read the canon | [`STORY.md`](STORY.md) (Rylee's words only) |
| See decisions + playtest notes | [`NOTES.md`](NOTES.md) |
| Know where things stand | [`.project/CURRENT.md`](.project/CURRENT.md) |
| Rules for agents | [`AGENTS.md`](AGENTS.md) |

## Play it in the studio

The pack lives in `worlds/cottage-of-the-breeze/`. The VEFR checkout sees it
through a symlink (`vefr/worlds/cottage-of-the-breeze` → this pack), so it
shows up on the Studio home's walls. Put it on the table there, or:

```sh
cd ../vefr
VEFR_WORLD=cottage-of-the-breeze uv run norns validate --pack worlds/cottage-of-the-breeze
```

## Layout

```
cottage-of-the-breeze/
  BRIEF.md  DESIGN.md  STORY.md  NOTES.md      the new-game kit
  art/mood/  art/source/                        references; originals + prompts
  worlds/cottage-of-the-breeze/                 the VEFR pack
  .project/CURRENT.md                           where things stand
```
