# DRAFT-v2 — notes for Claude

The companion to `docs/story/DRAFT-v2.md`. Nothing here is canon either; this is
the reasoning that sits behind the draft, so that Claude can review the choices
and Rylee can read them.

**Read this first: what this pass had to work from.** The sandbox the first pass was
written in could not reach `/var/home/agent/missions/…` at all and the clone had no
`origin` remote, so `git show origin/docs/story-draft:docs/story/DRAFT.md` failed and
**no prose of #111 reached the first pass at all.** That was the first pass's main
failure and the coordinator named it.

**This second pass had the full text of #111**, quoted verbatim in the packet, and
`docs/story/DRAFT.md` is still not on any branch in this clone. So the restoration below
is against the packet's quotation, which the coordinator transcribed. Two things follow
and both are worth stating plainly:

- Everything quoted here from #111 is quoted from **the packet's transcript of it**,
  not from a file I opened. The coordinator should diff it against the real file before
  this is read as an exact restoration.
- The Rylee decision files are still not readable from here. Every decision quoted in
  this notes file and in the draft comes from the packet's verbatim "Decisions in
  force", which the coordinator states it verified against the files. Where a claim was
  checkable against the repo itself I checked it and cite it below.

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
| #111's Section 3 note "I am going to go back down for him" | Cut. It was the rescue quest Rylee refused. "I am not going to be able to bring it up myself" remains. |
| #111's final town speech scene | Cut. The ending is the Blue Door and the kept room, and the last line is somebody making room at the table. |
| #111 makes Merrin the town's appointed jailer who failed | Rewritten. The ledger no longer says "Merrin of The Breeze will hold the room. He has a dog and a kettle and he can be relied on." He is a man who went down on purpose before the seal, and his fate is unresolved. |

**Four further corrections this pass made, all of them the first pass's errors rather
than #111's:**

1. **Bramble was undefined and, in one line, wrong.** The first pass had him as an
   unnamed "he" and wrote *"If you brought someone down here, they are safe here."*
   Nobody brought anybody down. See [§ Bramble](#bramble).
2. **#111's prose had not been carried across at all.** Now restored; see
   [§ Passages carried across](#passages-carried-across).
3. **The four-section shape had been lost.** v1 ran door → Down → banked hearth → kept
   room, and the Long Well, the Banked Fire and the Blue Door had no identity of their
   own. All four are the spine again.
4. **"No villain standing in the snow nineteen years later"** contradicted the forty-year
   setting. The line is now forty years. It is the only timeline number in the draft
   that was wrong.

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
| Bramble, the old tavern's dog | No. He has been in the doorway of the kept room for four decades, since before the sealing. | Not applicable — he never left it | That the room is unburnt; that the coal opens the Blue Door; that a cold wet traveller can be let in | **At the cottage; does not age; comes home** |
| The player | Yes, four times or more | Yes, always | The whole thing, and is told no more than that | The one who carries the coal up |

**What stays unresolved, on purpose:** Oren's fate. Merrin's fate. Who the six
places at the table are for. Whose note is the one by the fire in the Banked Fire.
Whose hand the second line on the ledger's last page is in. None of these is answered
in prose anywhere in v2. (The fire itself is settled and is not on this list: the town
banked a fire over the room on purpose and The Breeze burned decades later by
accident. See [§ Needs Rylee](#needs-rylee).)

**The four-section spine, and who is in it.** The Cellar King falls when the seal
breaks. The Longneck stands and will keep standing after you leave. Old Longsleep is
asleep and has been for a hundred years. Bramble gets up once and moves aside. **None
of the four is the villain**, and none of the four is killed.

## Passages carried across

**This section is the answer to the first pass's main failure.** It was empty then
because no prose of #111 had reached it. It is filled now.

#111's file is still not readable in this clone. Everything in the "from #111"
column below is quoted from **the packet's verbatim transcript of #111**, not from
the file. The coordinator should diff it against the real `docs/story/DRAFT.md`
before treating this as an exact restoration.

### Carried across word for word

| Passage | #111 | In v2 now | Changed, and why |
| --- | --- | --- | --- |
| The premise, in one sentence | `draft:17-21` | `## The premise, in one sentence` | Unchanged. "You live in the cottage at the end of the road because nobody else wanted it, there is a stair in the corner of the kitchen, and you keep going down because somebody should." | **No.** Rylee has never touched this sentence. |
| Why you go down, and it is a small reason | `draft:23-31` | same heading | Unchanged. | **No.** |
| What you are carrying up is heat | `draft:33-35` | same | Unchanged. | **No.** This is the "The player brings the coal home" decision, in #111's words. |
| The town, opening paragraph | `draft:39-41` | `## The town` | Unchanged. | **No.** |
| The townspeople table, all seven rows | `draft:45-53` | `### Who is there, and what each of them wants` | All seven rows verbatim, including the Fisher and the Hearth Cat. | **No.** The table is preserved item by item, not summarised. |
| What the town is losing, slowly | `draft:57-73` | same heading | First paragraph unchanged; the last two paragraphs extended with Rylee's forty-year winter account, marked as an addition. | **Extended, not replaced.** #111 had no winter; Rylee's decision is quoted in the draft. |
| How it plays | `draft:57-61` | `**How it plays.**` in the town section | Unchanged. | **No.** |
| The sections preamble | `draft:79-81` | `## The sections` | Unchanged. | **No.** |
| S1 — the place | `draft:85-89` | `### Section 1 — The Cellar Under the Cottage` | Unchanged. | **No.** |
| S1 — the mood | `draft:91-95` | same | Unchanged, including "It is the gentlest place in the game and the first one you are not afraid of." | **No.** |
| S1 — the guardian, the Cellar King | `draft:97-101` | same | Unchanged, including that his name is Rylee's to choose. | **No.** |
| S1 — the vault's seal note | `draft:103-106` | quoted in full in S1's vault | **Now quoted verbatim in the draft**, because it is an existing pack item and the draft should show the exact words it is preserving. | Quoting only. The note itself is untouched in `library/a-note-under-the-seal.md`. |
| "But read it again at the bottom and it does" | `draft:108-111` | same, in S1 | Unchanged. | **No.** |
| The letter, in the chest | `draft:113-115` | quoted in full in S1 | **Now quoted verbatim.** | Quoting only. Untouched in `library/a-letter-in-a-chest.md`. |
| S2 — the place | `draft:121-127` | `### Section 2 — The Long Well` | Unchanged, in full. | **No.** |
| S2 — the mood | `draft:129-133` | same | Unchanged. | **No.** |
| S2 — the guardian, the Longneck | `draft:135-139` | same | Unchanged, in full, including "it has never once been in a hurry". | **No.** |
| S2 — the vault, the bread oven and the ledger | `draft:141-144` | same | Unchanged as the description; **the ledger's last page is rewritten.** | The page carried no winter and named Merrin as the town's appointed holder of the room. Rylee's decision is a severe winter and nineteen people doing arithmetic, and Merrin is not a jailer. |
| S3 — the place | `draft:151-157` | `### Section 3 — The Banked Fire` | Unchanged, in full. | **No.** |
| S3 — the mood | `draft:159-163` | same | Unchanged, including "that is exactly when things start to hurt". | **No.** |
| S3 — the guardian, Old Longsleep | `draft:165-169` | same | Unchanged, in full, including "It is a hearth that learned to breathe and was never told to stop." | **No.** |
| S3 — the vault, the chest and the coal | `draft:171-174` | same | Unchanged; **Oren's net added to the chest's contents**, since #111 had the net as an item and nowhere put it. | One item moved into the room it belongs to. |
| S4 — the place, the blue door and the coal opening it | `draft:179-181` | `### Section 4 — The Blue Door` | Unchanged, in full. | **No.** |
| S4 — it is unburnt | `draft:183-185` | same | Unchanged, in full. | **No.** |
| S4 — the mood | `draft:187-189` | same | Unchanged, in full. | **No.** |
| S4 — the guardian, Bramble | `draft:191-196` | same | The first four sentences are **verbatim**. The two sentences that made him a bereaved watchdog ("has been in the doorway for four decades because a man he loved went through it and never came back") are rewritten, and the reason is below. | Rylee: "Merrin's eventual fate remains unresolved." |
| S4 — the vault, the room itself | `draft:198-201` | same | Unchanged, in full. | **No.** |
| S4 — what you read: nothing | `draft:203-206` | same | Unchanged, including "the note was in the cellar, written by somebody who came down before you". | **No.** |
| S4 — the answer | `draft:208-211` | same | Unchanged, in full. | **No.** |
| What each depth reveals, preamble | `draft:215-217` | `## What each depth reveals` | Unchanged. | **No.** |
| The unsaid paragraph under the reveal ladder | `draft:219-221` | same | Unchanged, in full. | **No.** |
| The final resolve, first paragraph | `draft:225-227` | `## The final resolve` | Unchanged: "You take the coal up. That is the whole mechanical resolve and it is deliberately small: one warm thing in your bag, and the stairs home are long." | **No.** |
| The part-2 door | `draft:245-249` | `## The part-2 door` | Unchanged, in full, including "Bramble will look at it when you take him up." | **No.** |
| The two devices, both | `draft:255-267` | `## The two devices, kept` | Unchanged in substance; the letter paragraph is anchored to Oren and to the Spell Keeper's cake instead of to her authorship. | **Rylee's decision 1** (the letter is Oren's). |
| Words this implies: books and notes | `draft:271-291` | `### Books and notes found in the world` | All eight existing items and all six new items, verbatim, **with the existing eight explicitly marked as untouched and listed for reference only.** | Marked, not changed. |
| Words this implies: stickers | `draft:305-311` | `### Stickers` | All six, verbatim. | **No.** |
| Words this implies: items | `draft:313-319` | `### Items` | All five, verbatim. | **No.** |
| What is waiting on the engine | `draft:323-331` | `## What is waiting on the engine` | Carried over and corrected against this repo; one line added for the part-2 stair. | Corrected, not rewritten. |

### Carried across in substance, with the wording changed

| Passage | What changed and why |
| --- | --- |
| S2's answer, *"The fire was set on purpose. By the town. To hold down a room."* | **Cut.** Rylee: the sealing was deliberate, the burning was not. v2 states the sealing as decided and the burning as accidental, and the two do not conflict. The seal note's *"it put a fire over the room, and a seal over the fire"* **is** the banking, done on purpose that winter; the Breeze burned four decades later when that same banked fire was left untended. Deliberate banking, accidental burning. The note stands word for word; see [§ Needs Rylee](#needs-rylee). |
| S3's note, *"I am going to go back down for him."* | **Cut, one clause of it.** It was the rescue quest Rylee refused. What is left is *"I am not going to be able to bring it up myself"* — the same writer, the same warmth, the same refusal to die on stage, without sending anybody back down. |
| S3's answer, *"The letter in the cellar is hers. So is the coal."* | **Cut.** The letter is Oren's and the draft says so. The coal is unnamed: v2 says the coal is the note-writer's and does **not** decide who wrote the note. |
| S4's Bramble, the two sentences about grief | **Rewritten.** See [§ Bramble](#bramble) below. |
| The reveal ladder, beats 2 and 3 | Beat 2 lost *"Nineteen people signed for it, and one of them owned the room"* — one of them did not own the room; they closed it. Beat 3 lost *"She is alive. She is in town."* — she came back earlier than Oren and is not the letter's author. |
| The final resolve's town scene | The tavern speech, the confession, and the Spell Keeper's *"I wrote that on the ninth step"* are **all cut.** What remains is the Regular's one changed line, the Smith's forge, the Keeper's cake, and Bramble coming up the stairs. Staggered, not simultaneous, per Rylee. |
| The Tavern Regular's row in the townspeople table | **Kept verbatim**, including that he wants the truth told out loud. He does not get it in v2, and the draft says so; the table is preserved as written and the ending overrides it. That tension is deliberate and is Rylee's to resolve. |
| The Fisher's line | **Cut.** *"Oren went down to look for the fire. Nobody sent him. I always thought he was a fool"* assigns both a motive and a verdict. Rylee asked for neither. |
| The Gardener's line | **Cut.** *"There's something under this bed that has been growing"* cannot be reconciled with a room where nothing ages. |
| The Spell Keeper's letter line | **Cut.** *"I wrote that on the ninth step. I wasn't brave either"* is the authorship claim Rylee decided against. It survives only as the item "Her ninth step", which is hers because she went down, not because she wrote the letter. |

### Bramble

The first pass had Bramble as an unnamed "he" and invented a thing that does not exist —
*"If you brought someone down here, they are safe here"* — on the assumption that a
player brings somebody down. Nobody brings anybody down. **Bramble is the old tavern's
dog**, from #111's own section 4, and v2 now says so and quotes him.

What he is not: he was never lost, nobody brought him down, and he has been holding that
doorway since before the sealing. What he does: he comes home, up the same stair, in
daylight. He does not age — Rylee: *"Time does not age things inside the kept room"*
and *"Do not introduce aging-related harm to Bramble as a surprise consequence of bringing
him home."* The room is where time does not apply, and the dog has been sitting in it
for four decades without being a day older, which is why the sentence works rather than
needing an exemption.

The sentence the first pass wrote is gone. What replaces it: *"Nothing in the kept room
ages. Not the bread, not the blanket, not Merrin's coat on its hook, and not the dog in
the doorway."* That keeps the rule, keeps the dog in it, and invents nothing.

### The cat

"Please preserve the cat's opinion of all this" is honoured by keeping the Hearth Cat's
table row verbatim, by keeping her device role (she is not a guide), and by giving her
the last word about Bramble. She remains the cat who permits you to live here, on
condition that you are occasionally ridiculous. No `voices/*.md` file is touched.

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
3. **Does the Spell Keeper know about the letter?** She reacts to it; Oren wrote it. — `world.json:239` has her say "You found my letter," and that stands word for word, because it is true: the letter's last line is *"Tell the keeper I kept my word about the cakes"*, so it is addressed to her in the only line that matters and it is hers to call hers. **Not changed, and no longer at risk.**
4. **Are the three Keybearers awake, dead, or asleep in v2?** Asleep. — They are the descent's household texture, not its stakes; "wake, take key, sleep again" keeps them harmless, which matches "nobody down here wants anything from you."
5. **Is the Cellar King the moral of the story?** No. He is the door. — A named antagonist would make the town the villain; the point is that the town was not being villainous.
6. **Does the player ever go back down after the ending?** Yes, freely. — Rylee's "The player can keep exploring afterward."
7. **Are the three signs of welcome (blanket, bread, gift) given by named people?** No. — Rylee's "No speech, confession scene… or obligatory moral explanation"; a named giver turns it into a reward.
8. **Are two different townspeople at the table on the second return?** Yes, two, not six. — "Different townspeople sometimes at the table"; six would fill every place and answer the question v2 is holding back.
9. **Does the kept room ever get a name on screen?** No. — Naming it would make it a place in a list rather than a room you find.
10. **Where does "Bramble comes home" land in the draft?** In Section 4, stated plainly, with the room's non-ageing as the reason it costs nothing. — "I want him to have a peaceful life at the cottage" and "That part matters."
11. **Is Bramble described concretely?** Yes — #111's own four sentences, verbatim, plus the fact that he was never lost and never brought down here. — He is the old tavern's dog. The first pass's failure to define him is fixed.
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
| `worlds/cottage-of-the-breeze/world.json` | 239 | `"line": "Oh. You found my letter. I did say I'd come back. I only took the long way round. Here, I kept one back for you."` | **Nothing to change — the line stands word for word.** Oren wrote the letter, and it ends *"Tell the keeper I kept my word about the cakes"*; it is addressed to her in that last line, so "my letter" is hers to say and v2 agrees. |
| `worlds/cottage-of-the-breeze/world.json` | 245–262 | the whole `the-seal-note-read` rule, including `{"set": "act-1-complete"}`, `{"complete-act": "act-1"}` and `{"say": "Far above, a window is a little brighter than it was."}` | v2's ending is the Blue Door and the kept room, not the seal note. Reading the seal note should not end the act. |
| `worlds/cottage-of-the-breeze/world.json` | 198 | `"act-1-complete": "the note under the Cellar King's seal has been read"` | The description of the flag names the old ending trigger. |
| `worlds/cottage-of-the-breeze/world.json` | 311, 335 | `{"flag": "act-1-complete", ...}` in `keeper-after-the-end` and `regular-after-the-end` | Those two lines are warmth after the end, not story. They survive v2 as written. **Listed only because they key off the flag above.** |
| `docs/story-spine-notes.md` | 12, 27, 29 | "the Spell Keeper. She is the one who is glad you keep going down. The letter in the chest … is hers." / "its author is not yet named" / "**Truth two revealed:** the Keeper is the one who came back \| The Keeper herself, after you carry the letter back to her" | Working notes, not canon and not a pack item, but they now contradict the letter's own text. Worth a one-line correction when Rylee next edits that file. |
| `STORY.md` | — | — | **Nothing to change.** It is empty and stays empty. Nothing in this PR proposes writing to it. |
| `NOTES.md` | — | — | **Nothing to change.** No existing entry is in conflict with v2 that is not already settled by a decision; those decisions are already recorded at `NOTES.md:963` for the spine and belong in Rylee's own words. |
| Every item in `worlds/cottage-of-the-breeze/library/` | — | — | **Untouched.** All ten files are byte-identical. `git diff --name-only cc71db7 --` names only the two v2 markdown files. (This clone has no `origin/main` ref; `cc71db7` is main.) |
| Every `voices/*.md` | — | — | **Untouched.** Including `worlds/cottage-of-the-breeze/acts/act-1/cottage/voices/hearth-cat.md`, whose cat persona v2 explicitly preserves ("Please preserve the cat's opinion of all this."). |

## Needs Rylee

1. **The fire question — settled; nothing under `worlds/` changes.**
   `worlds/cottage-of-the-breeze/library/a-note-under-the-seal.md:16` says the
   town "put a fire over the room, and a seal over the fire." Rylee's decision
   says the hearth was banked and "The Breeze later burned when the banked fire
   was left untended." These are not two accounts in conflict. The town
   **deliberately banked** its hearth over the sealed passage in the winter, on
   purpose — which is exactly what the note describes — and **The Breeze burned
   four decades later, by accident**, when that same banked fire was left
   untended in a building nobody used. v2 now says so in one paragraph, the note
   stands word for word, and no shipped text is touched.
2. **Whether the Blue Door is the town stair at `[1,1]`**, or a door of its own.
   v2 treats it as the way back up, which is what "the final section ends at the
   Blue Door and the kept room" implies, but the pack has no blue door: the
   cottage's own door is at `acts/act-1/cottage/contract.json:24` and the descent
   entry is town `[1,1]`. A blue door is art and data this PR does not contain.
3. **Whose note is the one by the fire, and whose hand the second ledger line is
   in.** Both are unnamed in v2 on purpose. Neither is collapsed onto the Spell
   Keeper, because she came back, and neither is collapsed onto Oren, because
   his letter is in section 1 and this is section 3. Rylee may want to close both.
4. **Whether Bramble is a resident, a sprite, or a POI.** The draft only requires
   that he can be at the cottage, walk down to the kept room, and sit in one of
   the six places. See [§ Feasibility](#feasibility) — this is the one open item
   with a real build cost behind it.
5. **The Tavern Regular's want.** His table row — preserved verbatim — is that the
   truth about the fire be told out loud in the tavern. v2 does not give him that.
   He gets one changed line instead. That conflict is visible and unresolved.

**Resolved since the first pass:** who or what Bramble is (he is the old tavern's
dog, and v2 says so in #111's words), and Merrin's coat line (restored — *"Old
Merrin's coat on a hook, forty years dry"* — no placeholder remains in the draft).

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
based on `cc71db7` (main, as of this pass) and touches two files. The branch is
also not present in this clone, which is why #111's prose was restored from the
packet's transcript — see [§ Passages carried across](#passages-carried-across).