# AGENTS.md — Cottage of the Breeze

A private game pack for the VEFR engine (`../vefr/`), and the studio's
first game: a learning remake of *Castle of the Winds*'s systems. This repo
owns the design kit and the pack content; it does not own engine code.
Read `README.md`, then `.project/CURRENT.md` (where things stand).

## The rules that matter

- **Rylee writes the stories.** Canon (`STORY.md`, the pack's `logbok.md`,
  names, characters, found books) is hers. Agents build machinery, suggest
  when asked, and never promote an idea into canon on their own.
  Suggestions go in `NOTES.md`, marked as an agent's ("Claude's note:"); `BRIEF.md`'s ✍️ parts
  are hers alone.
- **Remake the systems, not the property.** *Castle of the Winds* is Rick
  Saada's: its name, art, text and monster/item/place names are not ours to
  ship. Mechanics are. Nothing from the original's files goes in this repo.
- **The engine stays neutral.** Game-specific names never go into
  `../vefr/`. New engine features go through VEFR's ruleset checklist
  (`../vefr/docs/guides/rulesets.md`) and its ask-first rules.
- **The release is made in VEFR** (Rylee, NOTES 2026-09-26). Hand-made
  pictures and notes here are drafts and reference; the shipped game comes
  out of the studio (Folks room, studio modules, `ratatoskr weave`).
- **Every sitting ends with something alive:** a playable build, a book,
  a map, a note. Validate the pack after every pack edit (see Commands).
- Art: originals and their prompts go in `art/source/`.
- **Art we ship is art we made** (Rylee, 2026-10-02). We may distribute what we generate, and every piece is attributed (keep each `.credits.txt`). **Kenney is for prototyping only; never ship it.** **LimeZu** was bought to support the artist: use it only in a project Rylee names, with attribution. Neither is used in Cottage (the vendored Kenney sheets were removed 2026-10-02). If we need new sheets we generate them: Codex first, then Wan. Older "training: not cleared" or "not final art" notes in `art/` are stale for distribution (they are not rewritten; this rule wins).

## Map

| Path | What it is | Open it? |
|---|---|---|
| `BRIEF.md` | Stage 1 pitch (Rylee's words in ✍️ parts) | for design work |
| `DESIGN.md` | CotW systems checklist → VEFR rulesets | for design/engine work |
| `STORY.md` | canon — Rylee's words only | read, never write |
| `NOTES.md` | decisions + playtest notes, newest first | yes, before deciding anything |
| `.project/CURRENT.md` | stage + the one next step | yes, at session start |
| `worlds/cottage-of-the-breeze/` | the VEFR pack (`world.json`, `acts/`, `voices/`, `library/`, `logbok.md`) | yes, for pack work |
| `worlds/cottage-of-the-breeze/LICENSE` | CC0 terms for the Emberfield scaffold content | before reusing scaffold content |
| `art/source/`, `art/mood/` | originals + their prompts; mood references | for art work |
| `LICENSE.md` | all rights reserved, except the CC0 scaffold | before adding third-party content |
| `data/` | local index DB (gitignored, written by a tool) | no |

Much of the pack is still the Emberfield demo scaffold (CC0 placeholder),
meant to be replaced by Rylee's own content. Don't polish it as if it were canon.

## Commands

The pack's check is VEFR's validator, run from the VEFR checkout. The art
tools in `art/tools/` have their own unit tests (run those when you touch
them):

```sh
uv run --offline --with pillow python -m unittest discover -s art/tests -t .
```

There is no CI. Validate the pack:

```sh
cd ../vefr
VEFR_WORLD=cottage-of-the-breeze uv run norns validate --pack worlds/cottage-of-the-breeze
```

`vefr/worlds/cottage-of-the-breeze` is a local, gitignored symlink that
exists only in the primary VEFR checkout (`~/code/Rylee-Bee/vefr`) and points
at the **primary** cottage checkout. From a worktree, `../vefr` may be a VEFR
worktree without that symlink, or the wrong tree; pass this tree's pack path:

```sh
PACK="$(git rev-parse --show-toplevel)/worlds/cottage-of-the-breeze"
cd ~/code/Rylee-Bee/vefr && uv run norns validate --pack "$PACK"
```

## Publishing a playable build

`bin/publish-build.sh` weaves the pack into one HTML file and posts it to the dev
gallery (`https://gallery.hulganfamily.duckdns.org/cottage-of-the-breeze/`). It
weaves with the VEFR checkout at `~/code/Rylee-Bee/vefr`, so pull that first. Run
it after a merge, so the build's sha is a real commit.

## Boundaries

- **VEFR** (`../vefr/`, separate repo): the engine consumes this pack
  through the symlink above; the pack contract is what `norns validate`
  checks. Engine changes this game needs are VEFR work under its own
  AGENTS.md; record them as companion changes rather than editing `../vefr/`.
- **Estate `media_files/`** (root repo): art drafts and deliveries live
  there (`designs/vefr/art/cottage/`; studio casting call in
  `characters/vefr-residents/`). Commit those from the estate root, not here.
- Estate rules: `~/.agents/AGENTS.md`; nothing here restates them.

## Needs Rylee's approval here

- Anything that becomes canon: story, names, characters, found books, endings.
- Choosing a license or making the repo/game public (see `LICENSE.md`).
- Adding third-party content that is not CC0 or otherwise cleared.
- General gates (deploys, force-push, mass deletion): see the constitution.

## Done means

- The validator prints `ok: ... geometry, reachability, voices all pass`
  for the tree you edited.
- Decisions Rylee made are recorded in `NOTES.md`, her words quoted.
- `.project/CURRENT.md` names the stage and the one next step accurately.
- Something alive to show: a build in the studio, a book, a map, or a note.

## Handoff

Session state goes in `.project/CURRENT.md` (stage + next step) and
`NOTES.md` (decisions). There is no `.agent/` directory here.
