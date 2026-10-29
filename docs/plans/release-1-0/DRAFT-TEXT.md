# Draft-text inventory — cottage#159

`DEMO.md` tells players **"Every name and line of story you read is a draft that
Rylee has not signed off on."** Before this inventory, the pack said the same
thing nowhere: nothing carried `status: draft`, so `vefr check --release`
reported *"no drafts — every word in this pack is approved"* while `DEMO.md`
called the whole pack unapproved. Both cannot be true.

**Owner decision (Rylee, 2026-10-16, recorded on cottage#159).** Offered the
recommendation to mark the unapproved lines rather than soften `DEMO.md`,
Rylee answered: **"Use your recommendations."** So the pack marks its drafts.
This inventory is the "exact inventory" the release check is verified against.

**What this is not.** Design approval of a status model. It does not approve
story text, does not promote anything, and does not reword a single existing
line. Prose is byte-for-byte unchanged; only metadata lines were added. Nothing
here may be flipped to `approved` without Rylee signing off on that exact text
(`AGENTS.md`: Rylee writes the stories; agents never promote).

## Marked — the release check lists these

Every book and note in `worlds/cottage-of-the-breeze/library/` now carries
`status: draft` in its front matter, next to `title`. Fourteen files, the whole
of the library (it held thirteen before the Key Warden's challenge added one),
and the two notes parked in `act-3/` carry the same mark:

| Path | Player finds it as |
| --- | --- |
| `worlds/cottage-of-the-breeze/library/a-burned-page.md` | note on the town map |
| `worlds/cottage-of-the-breeze/library/a-candle-and-a-note.md` | note, cellar floor 5 |
| `worlds/cottage-of-the-breeze/library/a-coin-face-down.md` | note, cellar floor 3 |
| `worlds/cottage-of-the-breeze/library/a-letter-in-a-chest.md` | chest note, cellar floor 1 |
| `worlds/cottage-of-the-breeze/library/a-note-left-at-the-door.md` | note, town map |
| `worlds/cottage-of-the-breeze/library/a-note-for-the-next-one-down.md` | chest note, cellar floor 8; Act 1 ending |
| `worlds/cottage-of-the-breeze/act-3/a-note-under-the-seal.md` | parked for Act 3; `region: act-3-unplaced` |
| `worlds/cottage-of-the-breeze/library/a-scrap-in-the-dust.md` | note, cellar floor 1 |
| `worlds/cottage-of-the-breeze/library/about-this-game.md` | book, cottage shelf |
| `worlds/cottage-of-the-breeze/act-3/forty-winters.md` | parked for Act 3; `region: act-3-unplaced` |
| `worlds/cottage-of-the-breeze/library/the-burnt-taverns-tab.md` | resident book, keeper |
| `worlds/cottage-of-the-breeze/library/the-old-mushroom.md` | note, cellar floor 7 |
| `worlds/cottage-of-the-breeze/library/the-pale-moth.md` | note, cellar floor 5 |
| `worlds/cottage-of-the-breeze/library/the-rule-the-warden-keeps.md` | note, cellar floor 8; the Key Warden's rule |
| `worlds/cottage-of-the-breeze/library/the-stag-beetle.md` | note, cellar floor 8 |
| `worlds/cottage-of-the-breeze/library/writing-a-book.md` | book, no `found` (a shelf book) |

New draft text in `a-note-for-the-next-one-down.md` was supplied verbatim by
Rylee in cottage#173 on 2026-10-24. The sticker `next-one-down` and its name
in `world.json` are new draft words introduced for this ending.

`the-rule-the-warden-keeps.md` and the new line `world.json` speaks when it
is read are new draft words introduced with the Key Warden's challenge (the
challenge the owner put before the ending note on 2026-10-24). The rule the
warden keeps — "You do not take what is kept." — is the owner's recorded
design intent for that challenge; the words around it are an agent's.

The library is where the engine reads a text record's own metadata, so this is
where `status: draft` is a fact the release check can read rather than a
promise in a document. `tests/assert_draft_text.py` keeps this list honest.

## Unmarked — same words, no place to put the mark yet

These are player-facing and unapproved exactly like the library, but their
format has no front matter the engine parses, so no `status` was invented for
them. Marking them needs an engine decision (a VEFR issue), not an agent's
guess; until then they are drafts by `DEMO.md`, not by metadata.

| Path | The unapproved words in it |
| --- | --- |
| `worlds/cottage-of-the-breeze/acts/act-1/cottage/voices/hearth-cat.md` | resident voice prompt |
| `worlds/cottage-of-the-breeze/acts/act-1/tavern/voices/tavern-regular.md` | resident voice prompt |
| `worlds/cottage-of-the-breeze/acts/act-1/town/voices/dwarf-smith.md` | resident voice prompt |
| `worlds/cottage-of-the-breeze/acts/act-1/town/voices/fisher.md` | resident voice prompt |
| `worlds/cottage-of-the-breeze/acts/act-1/town/voices/gardener.md` | resident voice prompt |
| `worlds/cottage-of-the-breeze/acts/act-1/town/voices/keeper.md` | resident voice prompt |
| `worlds/cottage-of-the-breeze/ledger.md` | the whispers a player hears with Q |
| `worlds/cottage-of-the-breeze/world.json` | `title`, `description`, `creed`, the dusk/dawn phase lines, the bond cards and prompts, each voice's `strike`, every rule's `say`, every item `name`; since 2026-10-29 also the trait words, spell names and school words of [`WORDS-BATCH-1.md`](WORDS-BATCH-1.md) |
| `worlds/cottage-of-the-breeze/acts/act-1/cottage/contract.json` | place names, `poi_text`, `legend` |
| `worlds/cottage-of-the-breeze/acts/act-1/tavern/contract.json` | place names, `legend` |
| `worlds/cottage-of-the-breeze/acts/act-1/town/contract.json` | place names, `poi_text`, `legend` |
| `worlds/cottage-of-the-breeze/acts/act-1/town-after-the-cellar/contract.json` | place names, `poi_text`, `legend` |
| `worlds/cottage-of-the-breeze/acts/act-1/world.json` | region and act labels; the fight-row labels "Strike" and "Cast" ([`WORDS-BATCH-1.md`](WORDS-BATCH-1.md)) |
| `worlds/cottage-of-the-breeze/blueprint.json` | every family's mob `name` (33 families) and the two thing names |
| `worlds/cottage-of-the-breeze/sections/cellar.json` | Section name and place-of-interest labels |
| `worlds/cottage-of-the-breeze/sections/emberhall.json` | Section name and place-of-interest labels |
| `worlds/cottage-of-the-breeze/sections/rootworks.json` | Section name and place-of-interest labels |
| `worlds/cottage-of-the-breeze/sections/siltworks.json` | Section name and place-of-interest labels |

Two paths are deliberately **not** marked and must not be:

- `worlds/cottage-of-the-breeze/logbok.md` — Rylee's own words; agents read it
  and never write it (`AGENTS.md`). Its status is hers to say, not ours to
  record.
- `worlds/cottage-of-the-breeze/map.md`, `worlds/cottage-of-the-breeze/EDITS.md`
  — pack development notes, never shown to a player.

`blueprint.json` is the Blueprint source: its lock is byte-hashed, so it is
edited only together with `vefr normalize` on a host with the engine, and
never by hand here.

## How this is checked

`tests/assert_draft_text.py` is the repo-local half of the gate:

```sh
python3 tests/assert_draft_text.py
```

It fails if a book loses `status: draft`, if any book carries some other status
(a machine may not write `approved`), or if a text-bearing pack file exists
that this inventory does not name — so a new book, voice or Section cannot
join the pack unlisted. It cannot run `vefr check --release` itself; that needs
a VEFR checkout, which a bare worker worktree does not have.

## What a real release check still needs

Confirm on a host with the engine that `vefr check --release` lists these
sixteen drafts, and that promoting one book to an approved status is what
makes it leave that list. Until that run exists, this inventory and the test
are the evidence; the engine's own report is the host's to produce.
