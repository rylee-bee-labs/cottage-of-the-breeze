# DRAFT-v2 — notes for Claude

The companion to `docs/story/DRAFT-v2.md`. Nothing here is canon either; this is
the reasoning that sits behind the draft, so that Claude can review the choices
and Rylee can read them.

**Read this first: what I could and could not open.** The sandbox this draft was
written in could not reach `/var/home/agent/missions/…` at all, and the clone had
no `origin` remote, so `git show origin/docs/story-draft:docs/story/DRAFT.md`
failed. **PR #111's draft text, both worker returns, and the two Rylee decision
files were not available to me.** Everything I used from those four sources came
from the packet's own verbatim "Decisions in force" section, which the
coordinator states it verified against the files. Where that mattered I checked
the claim against the repo itself and cite it below. The one place I could not
substitute is the prose of #111, and the consequences are in
[§ Passages carried across](#passages-carried-across).

---

## Contradictions

Every conflict between PR #111's draft and a decision Rylee has made since. The
decision wins in each row; #111's version is what the draft gives up.

| # | #111 said | v2 says | Rylee's decision, quoted | Date |
| --- | --- | --- | --- | --- |
| 1 | The letter in the chest is the Spell Keeper's. | Oren wrote it. The Spell Keeper came back from her own earlier descent; this is not her hand. | "Oren, the Fisher's brother, went down some years ago, after the Spell Keeper had already returned from her own descent." / "His disappearance remains unresolved." | 2026-10-08 |
| 2 | (unused) | (unused) | "Do not modify STORY.md, promote draft material to canon, or rewrite existing story items without my explicit approval." | 2026-10-08 |
| 3 | (unused) | (unused) | "Preserve existing written items unless I explicitly approve changes. Existing book, note, sticker and resident text stays word for word." | 2026-10-08 |
| 4 | (unused) | (unused) | "If a story direction conflicts with existing text, explain the conflict and propose a resolution. Do not silently rewrite the original material." | 2026-10-08 |
| 5 | (unused) | (unused) | "The kept room remains revisitable." | 2026-10-08 |
| 6 | (unused) | (unused) | "Time does not age things inside the kept room." | 2026-10-08 |
| 7 | (unused) | (unused) | "Do not introduce aging-related harm to Bramble as a surprise consequence of bringing him home. I want him to have a peaceful life at the cottage." / "And Bramble comes home. That part matters." | 2026-10-08 |
| 8 | (unused) | (unused) | "Bramble comes home safely and does not suffer sudden aging." | 2026-10-08 |
| 9 | (unused) | (unused) | "For Cottage specifically, the final section ends at the Blue Door and the kept room, without a final boss." | 2026-10-08 |
| 10 | (unused) | (unused) | "A cold, wet traveler arrives. Someone makes room at the table. 'There's room.' No speech, confession scene, kindness score, or obligatory moral explanation. The world remains imperfect. The player can keep exploring afterward." | 2026-10-08 |
| 11 | (unused) | (unused) | "The player brings the coal home. The town gradually becomes warmer through small, practical acts of hospitality." / "Stagger improvements across returns to town rather than triggering everything simultaneously." | 2026-10-08 |
| 12 | (unused) | (unused) | "Forty years ago, during a severe winter, nineteen townspeople agreed to close the travelers' room and reserve dwindling resources for themselves. The communal hearth was banked and the passage beneath it sealed. The Breeze later burned when the banked fire was left untended." / "They thought kindness was something they could run out of." | 2026-10-08 |
| 13 | (unused) | (unused) | "Merrin went down voluntarily before the passage was sealed." / "Merrin's eventual fate remains unresolved." | 2026-10-08 |
| 14 | (unused) | (unused) | "Please preserve the cat's opinion of all this." | 2026-10-08 |
| 15 | (unused) | (unused) | "I like the sanctuary gradually welcoming others", and "I like it!" for the ending feeling (relayed by Sol, relay #21). | 2026-10-09 |

**Corrections to this table, found by me and not in the reconcile worker's work:**
rows 1, 12, 13 are the only ones where a decision names something #111 is known
to have said differently. Rows 2–11 and 14–15 are standing constraints, not
contradictions of #111; they are listed because the packet asks for the full set
of decisions in force, and because a reader checking a row finds the governing
sentence rather than having to go hunting.

The four contradictions the packet named explicitly:

| Packet item | Resolution in v2 |
| --- | --- |
| #111's reading that the letter is the Spell Keeper's | Dropped. Verified against `worlds/cottage-of-the-breeze/library/a-letter-in-a-chest.md:18` — "It is signed with a name you do not know." |
| #111's Section 3 note "I am going to go back down for him" | Cut. It was the rescue quest Rylee refused. |
| #111's final town speech scene | Cut. The ending is the Blue Door and the kept room. |
| #111 makes Merrin the town's appointed jailer who failed | Rewritten. He is a man who went down on purpose to keep the room open, before the seal, fate unresolved. |

## Witnesses

One row per person. "Knows" means: what the draft says this person is shown to
have seen, or to have said out loud, by the end of Section 4.

| Person | Came down? | Came back? | What they know | Status |
| --- | --- | --- | --- | --- |
| The Spell Keeper | Yes, once, earlier than the others | **Yes** | That someone went down on purpose and meant to return; that the room for travellers was sealed. She keeps one pound cake back for whoever comes up the stair. | Back in town; running the shop |
| Oren, the Fisher's brother | Yes, on purpose. His letter says "I meant to come back" | **Unknown** | The promise about the cakes. He wrote the letter and signed it with a name the reader does not know. | **Disappearance unresolved** |
| Merrin | Yes, voluntarily, before the seal | **Unknown** | Whatever he went down for. Someone kept his coat on a hook, which means somebody still owns it. | **Fate unresolved** |
| The nineteen | No | — | That they agreed to close the room and bank the hearth. Only Oren's decision is quoted. | Dead or gone; unresolved |
| The Cellar King | — | — | Nothing. He is the door, not a witness. He carries the seal. | Falls when the seal breaks |
| The Cat | No | — | Everything, and approves of very little. | Unchanged; its opinion is preserved |
| The cold, wet traveller | No | — | Nothing yet. They arrive at the end and are let in. | New, at the final line |
| Bramble | Brought home by the player | Not applicable | Not applicable. He is safe in the kept room. | **At the cottage; does not age** |
| The player | Yes, four times or more | Yes, always | The whole thing, and is told no more than that | The one who carries the coal up |

**What stays unresolved, on purpose:** Oren's fate. Merrin's fate. Who the six
places at the table are for. Whether the town meant to put the fire over the room
or merely left it untended (see [§ Needs Rylee](#needs-rylee)). None of these is
answered in prose anywhere in v2.

## Passages carried across

**This section is a shortfall, and it is the honest one.**

PR #111's `docs/story/DRAFT.md` could not be read in the sandbox this draft was
written in — the clone has no `origin` remote, so the `git show
origin/docs/story-draft:…` the packet prescribed could not run, and the file is
not in this clone on any branch. **Therefore no passage of #111's prose is
carried across word for word, and the list the packet asked for is empty.**

What did survive, because the packet describes it rather than quotes it:

- **The premise** — a wary town, a stair you cannot help going down, and the
  realization that what is held down is the town's own kindness. Survives
  intact; it is in `docs/story-spine-notes.md:13` and Rylee has never revoked it.
- **The four sections** — the beat structure survives; the titles and the prose
  inside them are new.
- **Residents are lines, not geometry** — survives as a named device with its
  own heading at the end of the draft.
- **"An object that means more the second time you read it"** — survives, and is
  still carried by the letter about the cakes. It is already in the game as a
  riddle sticker: `worlds/cottage-of-the-breeze/world.json:383` — "Someone kept a
  promise about cakes."
- **The unsaid thing** — survives in function, changed in content; see
  [§ The unsaid thing](#the-unsaid-thing).
- **The engine list** — carried over and corrected below.

One line the packet wanted word for word that I could not restore: Merrin's
coat on the hook. The draft marks the spot with an explicit placeholder rather
than inventing a sentence in Rylee's voice. Every other "keep word for word" item
in the packet's §5 list was already an existing written item in the pack, not
something I was writing — so the instruction is satisfied by **not touching any
of them**, which is checked in the next section.

## The unsaid thing

#111 deliberately left one sentence unsaid so that a part 2 had somewhere to go.

**In v2 the held-back sentence is: whether anyone the town sealed in ever came
back up.**

The draft says the Spell Keeper came back. It says Oren went down and is not
accounted for. It says Merrin went down before the seal and that nobody knows.
It sets six places at a table and declines to say who they are for. It never
states any relationship between those three facts, and it never asks the player
to infer one.

Why it is still held back: the answer ought to cost something, and it cannot cost
anything in the first hour of a game whose whole subject is a room that was
sealed and then unsealed. It also has to survive the new ending — an ending that
ends on *"There's room."* If the unsaid thing were answered, the six places would
become a roster, and the roster would be a twist, and the ending would be a
punchline. It has to stay a table with room at it.

## Smaller calls

Under twenty, as asked. Each is the question, the answer, and the reason in one
line.

1. **Where does the kept room physically sit?** Under the common hearth, below the Blue Door, in the cottage. — It is what was sealed, and the Blue Door is the way back up.
2. **Who says "There's room"?** Unnamed; a townsperson already known. — Rylee wrote "Someone makes room at the table"; naming the speaker turns an act into a character beat.
3. **Does the Spell Keeper know about the letter?** She reacts to it; v2 does not say she authored it. — `world.json:239` currently has her say "You found my letter," which is exactly the line at risk. Listed, not changed.
4. **Are the three Keybearers awake, dead, or asleep in v2?** Asleep. — They are the descent's household texture, not its stakes; "wake, take key, sleep again" keeps them harmless, which matches "nobody down here wants anything from you."
5. **Is the Cellar King the moral of the story?** No. He is the door. — A named antagonist would make the town the villain; the point is that the town was not being villainous.
6. **Does the player ever go back down after the ending?** Yes, freely. — Rylee's "The player can keep exploring afterward."
7. **Are the three signs of welcome (blanket, bread, gift) given by named people?** No. — Rylee's "No speech, confession scene… or obligatory moral explanation"; a named giver turns it into a reward.
8. **Are two different townspeople at the table on the second return?** Yes, two, not six. — "Different townspeople sometimes at the table"; six would fill every place and answer the question v2 is holding back.
9. **Does the kept room ever get a name on screen?** No. — Naming it would make it a place in a list rather than a room you find.
10. **Where does "Bramble comes home" land in the draft?** As a stated fact with no cost attached, in Section 4. — "I want him to have a peaceful life at the cottage" and "That part matters."
11. **Is Bramble described concretely?** Barely — only that he is at the cottage and can sit in one of the six places. — I could not read the 2026-10-08 decision file, so I do not know who or what he is; inventing detail would be inventing canon.
12. **Does the town ever apologize?** No. — "The world remains imperfect"; the warmth shows as a door held open, not as an admission.
13. **Does the player get a count of how warm the town is?** No score, no meter, no percentage. — "No… kindness score."
14. **Is the blue door ever explained?** Only that it is blue the way deep water is. — Rylee named it but did not say why; the colour is given, the cause is left to the player.
15. **Does the draft state the winter was forty years ago?** Yes, once, plainly. — Rylee's own framing, quoted; the draft should not be vaguer than the decision.
16. **Does the draft use the number nineteen?** Yes, twice. — It is in the decision; giving it up would soften the thing that matters, that this was a decision and not a mood.
17. **Is the letter read twice in play, or once with hindsight?** Once, with hindsight. — This is how "an object that means more the second time you read it" works without an engine change; the object is unchanged, the reader is not.
18. **Does v2 keep the ending's narrator line?** It drops "Far above, a window is a little brighter than it was." — `world.json:261`. The ending moves to the Blue Door and the kept room, so the lit-window image belongs to an earlier ending.

## Anything that would change an existing written item or STORY.md

**I changed none of them. This is the list of what would have to change for v2 to
be true, with the exact wording at risk, so Rylee can rule on each one.**

| Path | Line | Exact wording at risk | Why v2 conflicts |
| --- | --- | --- | --- |
| `worlds/cottage-of-the-breeze/world.json` | 239 | `"line": "Oh. You found my letter. I did say I'd come back. I only took the long way round. Here, I kept one back for you."` | The Spell Keeper claims the letter is hers. v2 makes it Oren's. **Highest-risk line in this PR.** |
| `worlds/cottage-of-the-breeze/world.json` | 245–262 | the whole `the-seal-note-read` rule, including `{"set": "act-1-complete"}`, `{"complete-act": "act-1"}` and `{"say": "Far above, a window is a little brighter than it was."}` | v2's ending is the Blue Door and the kept room, not the seal note. Reading the seal note should not end the act. |
| `worlds/cottage-of-the-breeze/world.json` | 198 | `"act-1-complete": "the note under the Cellar King's seal has been read"` | The description of the flag names the old ending trigger. |
| `worlds/cottage-of-the-breeze/world.json` | 311, 335 | `{"flag": "act-1-complete", ...}` in `keeper-after-the-end` and `regular-after-the-end` | Those two lines are warmth after the end, not story. They survive v2 as written. **Listed only because they key off the flag above.** |
| `docs/story-spine-notes.md` | 12, 27, 29 | "the Spell Keeper. She is the one who is glad you keep going down. The letter in the chest … is hers." / "its author is not yet named" / "**Truth two revealed:** the Keeper is the one who came back \| The Keeper herself, after you carry the letter back to her" | Working notes, not canon and not a pack item, but they now contradict the letter's own text. Worth a one-line correction when Rylee next edits that file. |
| `STORY.md` | — | — | **Nothing to change.** It is empty and stays empty. Nothing in this PR proposes writing to it. |
| `NOTES.md` | — | — | **Nothing to change.** No existing entry is contradicted by v2 that is not already contradicted by a decision; those decisions are already recorded at `NOTES.md:963` for the spine and belong in Rylee's own words. |
| Every item in `worlds/cottage-of-the-breeze/library/` | — | — | **Untouched.** All ten files are byte-identical. `git diff --name-only origin/main` names only the two new files. |
| Every `voices/*.md` | — | — | **Untouched.** Including `worlds/cottage-of-the-breeze/acts/act-1/cottage/voices/hearth-cat.md`, whose cat persona v2 explicitly preserves ("Please preserve the cat's opinion of all this."). |

## Needs Rylee

1. **The fire question — escalated to Claude as architecture, not settled here.**
   `worlds/cottage-of-the-breeze/library/a-note-under-the-seal.md:16` says the
   town "put a fire over the room." Rylee's decision says the hearth was banked
   and "The Breeze later burned when the banked fire was left untended." Those
   are different: intent versus accident. v2 quotes the note exactly, states the
   accidental fire as decided, and **does not say which of the two the town
   meant**. The draft contains the contradiction rather than resolving it. It
   needs Claude's architecture ruling, and then either the note or the prose
   changes — not both, and not here.
2. **Who or what Bramble is.** v2 keeps Bramble at the cottage, safe and
   unaging, and invents no further detail, because I could not read the decision
   file that defines him.
3. **Merrin's coat line.** #111's exact words, to be restored into the marked
   placeholder in Section 2.
4. **Whether the Blue Door is the town stair at `[1,1]`**, or a door of its own.
   v2 treats it as the way back up, which is what "the final section ends at the
   Blue Door and the kept room" implies, but the pack has no blue door: the
   cottage's own door is at `acts/act-1/cottage/contract.json:24` and the descent
   entry is town `[1,1]`. A blue door is art and data this PR does not contain.
5. **The ending's length.** `docs/story-spine-notes.md:46` still lists "how long
   the ending is" as open. v2 answers it (a room, revisitable) but that is Claude
   and I, not Rylee.

## Feasibility

**This is a survey, not an implementation. This PR contains no engine change and
no game-data change.** Two new markdown files under `docs/story/` are the whole
diff. Every "cost if new" below is an estimate for Rylee to weigh, not work that
has been done. Carried over from the vefr-sanctuary worker's return where the
sandbox allowed, and surveyed directly against this repo where it did not; rows
marked *(mine)* were read out of the files cited and had no worker return to come
from.

| Feature | Exists today | Where | Cost if new |
| --- | --- | --- | --- |
| Persistent world state across visits | Yes | `worlds/cottage-of-the-breeze/library/about-this-game.md:14` — bag, gear, album and journal are saved in the browser | Low. Flags already persist; nothing new. |
| Persistent flags a rule can read | Yes | `worlds/cottage-of-the-breeze/world.json:210` (`"set": "read-the-letter"`), `:234` (`"set": "keeper-came-back"`), `:255` (`"set": "act-1-complete"`) | Low. One `set` per new beat. |
| Returning to a room | Yes | `worlds/cottage-of-the-breeze/acts/act-1/world.json` `transitions` — town↔cottage, town↔tavern, each with `from`/`at`/`to`/`to_at` | Low. The Blue Door is one more transition. |
| A room that is not on the way anywhere | Partly | `acts/act-1/cottage/contract.json:23` has a `pois` map (`"4,6": "the cottage door"`, `"4,3": "the hearth"`) | Low. A new region and a contract, as the cottage has. |
| An NPC living in the cottage | Yes, and already | `worlds/cottage-of-the-breeze/acts/act-1/cottage/voices/hearth-cat.md:1`; placed via `worlds/cottage-of-the-breeze/EDITS.md:2`; a speaker keyed `hearth-cat` in `acts/act-1/world.json` | Low. One voice file and one speaker entry. |
| Bramble as a second resident | No | — | Low-medium. Bramble is not a creature and may not want a sprite or a fight table; a sprite-only speaker is the easy path, a resident with behaviour is not. |
| A fire in the room | Partly | `acts/act-1/cottage/contract.json:25` — `"4,3": "the hearth"` is a named POI | Low if it is a tile; higher if the engine has no lit-object concept. |
| Per-visit variation | **No** | Every rule in `worlds/cottage-of-the-breeze/world.json` is `"once": true` (`:216`, `:243`, `:275`, `:290`, `:308`, `:332`) | **The real cost.** Three signs of welcome need three non-`once` triggers, and the engine's rule vocabulary is `starts`, `reads`, `comes-near`, `if flag` — there is no "on each visit to region X, pick a different thing". This is a VEFR gap, not a pack gap. |
| Staggering improvements across returns | No | Same as above | Medium. Same gap. `once` rules cannot produce "the town is a little warmer each time". |
| No chores, no deadlines, no check-in | Yes, by absence | The engine has no timer, counter or streak in any rule the pack uses | Zero, but it is a standing constraint on whoever writes the new rules. |
| Ending that is not a cutscene | Partly | `docs/plans/release-1/C7-brief.md:11` — the end card is `#act-end` and offers **Keep exploring**; `docs/plans/release-1/HANDOFF.md:20` — `complete-act` fires the card **once per save** | Low. But "once per save" is the wrong shape for a revisitable ending; v2 wants the ending to be a *place*, not a card. |
| Sticker/album reactions to story beats | Yes | `worlds/cottage-of-the-breeze/world.json:374`–`:413` — `the-letter`, `the-warm-page`, `cat-notices`, `about-book`, each with a `when` and a `riddle` | Low. Three more entries for the three signs of welcome. |
| Multiple things happening across acts | **No** | `docs/plans/acts-2-3/PLAN.md:9` — "The engine plays one act. **Act advance is unbuilt** (VEFR ADR 0006)" | High, and out of scope. Part 2 is blocked on ADR 0006. |
| `sanctuary_tiles` | Key exists, unread | All three contracts carry it: `acts/act-1/cottage/contract.json:28` (empty), `tavern/contract.json:36` (empty), `town/contract.json:67` → `["D"]` | Unknown. The town already sets it and nothing in the pack documents a reader. **Worth one question to VEFR before anyone builds on it.** |

## What is waiting on the engine

Carried over from #111's own section and corrected against this repo. Each line
names the gap, not a workaround.

1. **Per-visit variation.** Three signs of welcome, staggered across returns.
   Every rule in the pack is `once: true`; the engine's triggers are `starts`,
   `reads`, `comes-near` and `if flag`. Nothing fires twice. *(Gap, not a bug.)*
2. **A revisitable ending rather than a one-shot card.** `complete-act` is once
   per save (`docs/plans/release-1/HANDOFF.md:20`). v2 wants the kept room to
   outlive the card.
3. **Act advance, for part 2.** ADR 0006, unbuilt
   (`docs/plans/acts-2-3/PLAN.md:9`). The unsaid thing has nowhere to go until it
   exists.
4. **Ageing, explicitly not wanted.** "Time does not age things inside the kept
   room" is currently satisfied by there being no ageing system to disable. If
   one is ever added, it must exclude the kept room.
5. **A resident who is not a creature.** Bramble may need a resident that has no
   fight table and no spawn.
6. **`sanctuary_tiles`.** Asked once, noted, nothing depends on it in this PR.
7. **A door that is blue.** No art or data for it is in this PR, and none is
   proposed. Listed so it is not mistaken for something v2 already has.

### On PR #111's branch

The packet is right that it must not be built on: `docs/story-draft` is behind
`main` and re-adds the `acts/act-1/floor-1`..`floor-6` and `king-room` records
that cottage#110 deleted. Building v2 on it would resurrect them. This branch is
based on `origin/main` and adds two files.