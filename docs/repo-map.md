# Repo map — Cottage of the Breeze

Reference detail moved out of `AGENTS.md` on 2026-10-09 so the router could stay
under its word budget. Nothing here is a rule: every MUST/NEVER/DO NOT and every
Rylee decision stays in `AGENTS.md`, verbatim. If this page and `AGENTS.md` ever
disagree, `AGENTS.md` wins.

Every row was checked against this tree on 2026-10-09; the command that checks it
is in the last column. A row with no command is a claim about the estate or the
engine checkout, not about this repo — those are UNKNOWN from here.

## What each path is

| Path | What it is | Open it? | Check |
|---|---|---|---|
| `BRIEF.md` | Stage 1 pitch (Rylee's words in ✍️ parts) | for design work | `ls BRIEF.md` |
| `DESIGN.md` | CotW systems checklist → VEFR rulesets | for design/engine work | `ls DESIGN.md` |
| `STORY.md` | canon — Rylee's words only | read, never write | `ls STORY.md` |
| `NOTES.md` | decisions + playtest notes, newest first | yes, before deciding anything | `ls NOTES.md` |
| `DEMO.md` | the running-demo writeup | for demo/engine work | `ls DEMO.md` |
| `docs/` | plans (`plans/`), playtest reports with logs and screenshots (`playtests/`), story drafts (`story/`), the language study (`language-architecture/`), backlog (`BACKLOG.md`) | when the work is in one of them | `find docs -type f` |
| `.project/CURRENT.md` | stage + the one next step; a router, not a snapshot | yes, at session start | `cat .project/CURRENT.md` |
| `worlds/cottage-of-the-breeze/` | the VEFR pack: `world.json`, `acts/`, `sections/`, `sprites/`, `assets/`, `voices/`, `library/`, `skins/`, `blueprint.json`, `blueprint.lock.json`, `logbok.md`, `map.md`, `ledger.md`, `EDITS.md`, `world-tree.md` | yes, for pack work | `ls worlds/cottage-of-the-breeze/` |
| `worlds/cottage-of-the-breeze/sections/` | the four descent Sections: `cellar.json`, `rootworks.json`, `siltworks.json`, `emberhall.json` | for descent work | `ls worlds/cottage-of-the-breeze/sections/` |
| `worlds/cottage-of-the-breeze/skins/parchment-and-wood/` | the game's interface pictures — 20 `.webp` + `skin.json`, 21 files — declared by `"skin"` in `acts/act-1/world.json`; source and raw textures in `art/skins/` | for skin work | `ls worlds/cottage-of-the-breeze/skins/parchment-and-wood/ \| wc -l` |
| `worlds/cottage-of-the-breeze/LICENSE` | CC0 terms for the Emberfield scaffold content | before reusing scaffold content | `cat worlds/cottage-of-the-breeze/LICENSE` |
| `art/` | `source/` (originals + prompts, by round), `skins/` (raw UI textures + mock renders), `mood/` (**empty** — `.gitkeep` only), `briefs/` (per-batch art briefs), `tools/` + `tests/` (the skin pipeline and its unit tests), `STYLE.md` | for art work | `ls art/` |
| `LICENSE.md` | all rights reserved, except the CC0 scaffold | before adding third-party content | `cat LICENSE.md` |
| `bin/publish-build.sh` | weaves the pack into one HTML file and posts it to the dev gallery | after a merge | `head -30 bin/publish-build.sh` |
| `tests/` | `assert_chest_drops.py` (runs on every PR), `test_pr_scope.py`, `playthrough/` (the headless bot that plays the pack) | when you touch drops or routes | `ls tests/` |
| `.github/workflows/` | `validate-pack.yml` (pinned VEFR validation + the chest-drop assertion), `secret-scan.yml` | read, don't edit | `ls .github/workflows/` |
| `data/` | gitignored in `.gitignore`, **not in this tree**, and no tool in this repo writes it — who creates it is **UNKNOWN** | no | `ls data/` fails; `grep -rn 'data/' --include='*.py' --include='*.sh' .` finds nothing |

## Layout

```
cottage-of-the-breeze/
  BRIEF.md  DESIGN.md  STORY.md  NOTES.md  DEMO.md   the new-game kit
  docs/                                             plans, playtests, story drafts
  art/source/ art/skins/ art/mood/                   originals, textures, (empty)
  worlds/cottage-of-the-breeze/                      the VEFR pack
  tests/                                            chest-drop gate + the play bot
  bin/publish-build.sh                               weave one HTML file, post it
  .project/CURRENT.md                                where things stand
```

## The pack is still mostly scaffold

Much of the pack is still the Emberfield demo scaffold (CC0 placeholder),
meant to be replaced by Rylee's own content. Don't polish it as if it were canon.

The hand-authored cellar (`floor-1`..`floor-6`, `king-room`) is **gone** as of
2026-10-08 (cottage#118): there are no floor contracts left in the pack. The
descent is generated from `sections/*.json` — cellar, rootworks, siltworks,
emberhall, nine floors each. Check with `find worlds -name '*floor*'` (returns
only two tile files) and `.project/CURRENT.md`.

## Blueprint-generated records

`blueprint.json` is the source; `blueprint.lock.json` records its
`source_sha256` and the records `vefr normalize` wrote from it. On this tree
the lock records exactly one output: the pack root's `world.json`, pointers
`/items/cellar-gems` and `/items/crown-seal`. Check:

```sh
python3 -c "import json;print(json.load(open('worlds/cottage-of-the-breeze/blueprint.lock.json'))['outputs'])"
grep -n 'cellar-gems\|crown-seal' worlds/cottage-of-the-breeze/world.json
```

The `enemies` list in `worlds/cottage-of-the-breeze/acts/act-1/world.json` is
`[]` — the descent's creatures come from the Blueprint families
(`blueprint.json` → `families`, 32 entries) named by the Sections, not from
hand-written `enemies` lists. Check with
`grep -n '"enemies"' worlds/cottage-of-the-breeze/acts/act-1/world.json`.

The engine's Blueprint guide is `vefr/docs/guides/blueprint.md`, a path inside
the VEFR checkout. There is no VEFR checkout in this worktree, so its existence
is **UNKNOWN** from here.

## Boundaries in full

- **VEFR** (`../vefr/`, separate repo): the engine consumes this pack through
  a local, gitignored symlink; the pack contract is what `norns validate`
  checks. Engine changes this game needs are VEFR work under its own AGENTS.md;
  record them as companion changes rather than editing `../vefr/`.
- **Estate `media_files/`** (root repo): art drafts and deliveries live there
  (`designs/vefr/art/cottage/`; studio casting call in
  `characters/vefr-residents/`). Commit those from the estate root, not here.
  Those paths are not in this repo, so from this checkout they are **UNKNOWN**.
- Estate rules: `~/.agents/AGENTS.md`; nothing here restates them. That file is
  outside this checkout: **UNKNOWN** from here.
- The VEFR ruleset checklist `AGENTS.md` names is likewise a path in the VEFR
  checkout, not in this repo: **UNKNOWN** from here.

## Handoff

Session state goes in `.project/CURRENT.md` (stage + next step) and `NOTES.md`
(decisions). There is no `.agent/` directory here (`ls -a` confirms). The
previous Release-1 snapshot and dated NEXT/verification ledger remain in git
history; do not recreate a rolling status ledger.