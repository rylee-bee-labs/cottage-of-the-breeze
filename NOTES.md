# NOTES — decisions and playtest notes (newest first)

## 2026-10-04 (later) — interface direction: parchment and soft wood, Ledger type (Rylee)

- **Her words:** "Scrapbook pages I think is my fav. It's working better now! Can we fix the font to be a little more 'cottage' and less stardew valley?" Then: "Oh I don't like the tape. Back to parchment and soft wood. Let's say 'ledger' font?" Earlier she had said of the first painted kit: "I prefer the older style over this", and asked for "radically different ui styles to help me visually narrow down. Not a picker, a system to help me refine."
- **Claude's note (agent):** the interface lab now defaults to "Parchment & soft wood" with the Ledger voice (Crimson Pro). Nothing is built into the game yet; the plan is `docs/plans/native-ui/PLAN.md`.

## 2026-10-04 (after the first night) — what changed, and what Rylee decided

- **Release 1 is a complete polished Act 1.** After the entry below was written, the same night added the album (25 stickers), nine soft synthesized sounds with a switch in Menu > Display, a four-direction walk cycle for the hero, eight unique cast monsters, seven pieces of gear with Codex art, and an accessibility pass. Published build `26c21ee`. Verification and state: `.project/CURRENT.md`.
- **Acts 2 and 3 were left for later by Rylee's decision.** They remain part of the three-act direction. The release is not evidence that VEFR could not support them; act advance and status effects are the next engine capabilities because those acts will want them. Plan: `docs/plans/acts-2-3/PLAN.md`.
- **Her order of work (chat, 2026-10-04):** "Ship act 1, then plan 2 and 3"; refactor `web/packaged.html` first; fire is the first effect; "I'd like all of act 1 to be very high quality. With all systems and art and everything." (She also asked for a research task on RPG interface styles; the result is in the artifact she was sent.)
- **Her interface direction (chat, 2026-10-04):** "anything running 'inside the game' to be in a themed ui for that game and only controls and such", with HUD icons currently floating over the page background; then, of a handheld-frame mock: "I don't want an actual frame around it. I want the ui to pretend it's ported from another system but be native hahaha! It should feel like a part of the vefr world. This feels like a square mechanical ui overlayed over a warm soft game." Recorded as `docs/plans/native-ui/PLAN.md`.
- **Claude's note (agent):** the sound default (on where a pack opts in, with a visible switch) was my choice and is not yet ruled on by Rylee.

## 2026-10-03 (overnight) — release 1: the ladder, the King's room and an ending (agent drafts, Rylee decides)

Rylee asked for a complete, polished, playable first release built through VEFR. Built tonight (all on branch `release-1/ladder`; plan in `docs/plans/release-1/PLAN.md`). **Everything below that is story text is an agent draft, not canon. Keep, rewrite or bin any of it; each is data, so swapping words takes minutes.**

- **The Keybearer ladder.** Floors 3, 4 and 5 each hold one Keybearer, a tougher variant of an existing family carrying that floor's key; the Cellar King on floor 6 carries the crown seal. Placed by BFS in a far room (floor 3 at 6,6; floor 4 at 2,2; floor 5 at 1,29; the King at 26,3). The stairs 3 to 4, 4 to 5 and 5 to 6 now need the key (`requires`); keys are `keep` and have **no value** (a sold key would soft-lock the game). Guardian names are descriptive placeholders ("the Keybearer, a great pale moth"); **proper names and epithets are yours**. Art picks: `art/source/round11/PICKS.md` (moth, mushroom elder, stag beetle; the mole and the robed rat are held back for later).
- **The King's room and the ending.** A sealed door on floor 6 at (11,1), opened by the crown seal, leads to `king-room`: a small chest with **gems** (treasure is a draft), a draft lore note (`library/a-note-under-the-seal.md`) and a stair home to town. Reading the note fires one rule: it sets `act-1-complete`, shows the end card (VEFR's new `complete-act` action: "Keep exploring" or "Start over", once per save) and says one narrator line. It does not start act 2 (ADR 0006 is unbuilt). The Keeper and the Tavern Regular have one new draft line each after the end.
- **Tutorial moments, an About book, the cat.** Draft lines from rules (`tutorial-*`, `first-key-*`, `the-cat-notices`); an "About This Game" book on the cottage shelf (credits, tools, fonts). The brass ring is now a charm (+1 attack).
- **Deep floors dressed.** Floors 4-6 and the King's room use the round-13 deep flagstone and wall; floor 6 map was hand-edited for the sealed door (a `vefr delve` rerun would overwrite it).
- **Not done (and why).** *(Written early that night; superseded the same night: the album, sound, the hero's walking frames and the round-12 cast monsters all landed later, see the entry above.)* What remained: stakes (no engine mechanic), acts 2 and 3 (deferred by Rylee after Act 1), per-run floors, the mole and beetle proofs as town folk.
- **Existing saves:** new enemies change signatures, so floors repopulate on an old save. Start over for a clean run.

## 2026-10-02 (late) — art direction after the MiniMax test (Rylee)

- **Her words:** "I think I prefer the codex character designs. I enjoy the storybook and the cuter concepts for the mobs vs realism." And of the dressed scarred-rat guardian (a MiniMax draft): "I did rather enjoy the v6 guard style though. That was pretty cute!" And: "you're also more than welcome to use codex, was just an experiment!"
- **What that means (agent's reading):** cute, characterful storybook mobs are the target; Codex stays first choice for characters and creatures; MiniMax is for items and equipment (and cute-mob drafts when asked). Nothing from the test is in the pack. The recipe is in `art/STYLE.md` (PR for review).

## 2026-10-02 (late) — the language campaign, and the first lock (Rylee)

- **Answers, in chat:** the first lock is **floor 3 to floor 4**; the key is **an actual key**; the guardians are "variants with names based on their art/abilities". Names are not chosen yet; nothing here is canon until she says.
- **Creature records now come from a Blueprint** (VEFR's new optional source). `blueprint.json` is the edited truth for the 69 monsters; the floor contracts' `enemies` lists are generated and read-only. The trial passed its exit threshold (508 authored values became 277, 45.5% fewer, every record equal to before, the woven game identical). Follow-up (agent, for her review): the repeated potion drop moves into the families that carry it, 257 values (49.4% fewer), still every record equal and no floor contract changed. She asked for it merged: PR #68.
- **Rule state survives a reload** (`saves.rules: persist`, `legacy: from-log`): a rule that fired stays fired, so a beat she already saw does not replay (PR #70). `from-log` uses the Why log, which keeps 20 entries, so an older beat could replay once.
- **Published** for her demo: build `2026-10-02-8a48788` on the dev gallery.
- The engine can lock a stair now (VEFR #229); Cottage does not use it yet.

## 2026-10-02 — growth and the day's goal (Rylee)

Her goal for the day: "a full 1-2 act structure with multiple mobs, working inventory, and a loop that feels rewarding, some kind of experience/learning/growing methodology." On growth she chose: "can we wire in classic xp and growth and learn-by-doing into the engine, but I think that cottage should be standard. just don't lose the learn by doing.. that's important for another game I'm working on". So VEFR gets both as neutral capabilities; Cottage uses classic XP. She also asked to start with "repo health/docs/engine in offload foremen so we can work on the structure together".

- **Docs brought in line (agent):** `AGENTS.md` (art tests exist), `.project/CURRENT.md` (engine landed, Cottage has no rules yet), `docs/GAME-PLAN.md` (rules no longer blocked).
- **Letter -> Keeper wired (agent):** two rules in `world.json`. `the-letter-read` (when the hero reads "A Letter, Folded Small", set a flag, one narrator line). `the-keeper-knows` (when the hero is next to the Spell Keeper and has read it: she says her line once). Checked by firing both events into the woven file: she says nothing before the letter, and the Why record names each rule. **The two lines are agent drafts, not canon.** Keeper: "Oh. You found my letter. I did say I'd come back. I only took the long way round. Here, I kept one back for you." Hers to keep, rewrite or bin. Not yet played by walking to the chest.
- **Rylee, 2026-10-02:** "wire the letter and Keeper reaction first. and for this run let's mimic castle of the winds pretty directly to help me learn while we learn and as we build our engine". Claude's note: this means copying the systems (kills give XP, levels, town and descent loop); our own names, numbers and text, per the repo rule.
- **Fuller cellar (Rylee: "it feels empty in the dungoen right now"):** floors 1, 2 and 3 now hold 6, 10 and 12 monsters (were 1, 2, 2). Only four monster pictures exist (rat, shade, moths, rustle), so variety is name and stat variants: a fat cellar rat, a deep shade, a loud rustle (more health and bite, some carry a potion). Placed by a seeded script on open floor, at least 7 tiles from the stairs and chests and 5 apart. **Tuning numbers are first guesses**; new monster pictures are an art task.
- **Her UI notes, same day (queued in VEFR):** the bottom text is noisy ("text on the bottom of the screen that basically never goes away and you can't move it"), the hero's hop is "cute but weird" (chose: much smaller), "full wasd support", and Trade should close without Esc or the mouse. Art: "most of the art could use some love"; she chose a full art pass later.
- **Act 2, built as a deeper zone (Rylee: "Both, zone first"):** only the first act plays in VEFR today (ADR 0006, real act advance, is proposed). So floors 4, 5 and 6 hang off a new stair down at floor 3 (tile 2,2, the far corner from the arrival), generated by `vefr delve` (seed `cottage-deeper-zone`, 48x32, 10 rooms) and dressed with fog and 12, 14 and 15 tougher monsters (new: a hollow shade 12 hp / 3 atk, a howling rustle). They live in act 1's region list so they can move into a real act 2 when ADR 0006 is built (queued as the next engine job). **Looks:** the new floors use the engine's plain dungeon tiles, not the authored flagstone, so they look flatter than floors 1-3; an art task. **Not checked by eye:** I could not jump into the new floors in a browser (the region switch is private to the player), so their look is UNVERIFIED; the pack validates and bakes.
- **Open for Rylee, story:** `docs/story-spine-notes.md` put the last room (the realization) at the bottom of floor 3, which was an agent proposal and is not built. With six floors, where does the bottom of the story live: floor 3, or floor 6? Nothing is built either way; no canon changed.
- **Gating (Rylee):** after learning the word (progression gating; soft = power curve, hard = lock and key) she asked "is it more rewarding to have one tougher mob with the key that you have to find? I do want the levels and mobs to be generated, not sure how that applies here. wasn't cotw generated?". Claude's answer: yes, a key guardian is more rewarding; generate the filler, place the guardian by the generator; the engine cannot lock a stair yet. Design: `../vefr/design/gates-and-guardians.md` (proposed). Her call still open: which stair is the first lock, and what the key looks like.
- **Art rights (Rylee, 2026-10-02):** "we are allowed to distribute the art we generate, but we will attribute all of it. leave out the kenny and limezu assets, only use what we have made ourself." Then: "kenny is only for prototyping, and limezu I might use in a project and attribute it but mostly I wanted to support them and it was a sale". Recorded as a rule in `AGENTS.md`. The vendored `assets/kenney/` sheets in the pack are unused (no reference in any pack JSON); left in place, removal is hers to ask for. Art is scattered across `media_files/designs/vefr/art/`, `../vefr/web/art/` and `art/source/` (she: "sorry it's messy"); pick sheets are in the gallery (Art picks).
- **Growth is on in Cottage (Rylee: "turn on growth in cottage"):** classic levels, the Castle-of-the-Winds-style systems copy she asked for, our own numbers. `world.json` `growth`: 8 levels at 0, 6, 15, 30, 55, 95, 150, 230 experience; each level gives +2 health and +1 attack (hero starts 6 hp / 2 atk). Every monster on floors 1-6 has `xp = round(hp x atk / 2)`, at least 1 (rat 2, fat rat 3, deep shade 8, hollow shade 18; 314 in all). If you clear a floor you reach: floor 1 level 2, floor 2 level 4, floor 3 level 5, floor 4 level 6, floor 5 level 7, floor 6 level 8. **First guesses to tune by playing.** The surface is still the cozy one (you cannot lose), so levels are felt, not needed; turning on stakes and the key guardians is what makes them matter (`../vefr/design/gates-and-guardians.md`). Practice mode (learn by doing) stays in the engine for her other game; Cottage does not use it.
- **Handoff written (2026-10-02 evening):** `.project/CURRENT.md` now holds the restart steps, what is built, what waits on Rylee, and the foreman recipe; VEFR's matching refresh is in `../vefr/.project/CURRENT.md`.
- **Guardians approved, and where the story's last room goes (Rylee, 2026-10-02):** "the guardians are great" (the five round-11 proofs: the Reeve mole, the Bailiff moth, the Warden mushroom elder, the Marshal beetle, the Seneschal robed rat). On the last room: "his seal opens like a treasure room with a lore note and a 'back to town' before you start the next set of dungeons?" So: beating the Cellar King opens a room with a treasure, a lore note, and a way back to town, and act 2 (the next set of dungeons) starts after it. **Structure only; the lore note's words are not written and nothing is canon until Rylee writes or picks them.** This replaces the agent's earlier guess that the realization room sat at the bottom of floor 3 (`docs/story-spine-notes.md` is updated).
- **Round 12, the cellar cast (Codex, two batched calls, drafts; Rylee picks):** eight new regular monsters, files identified by looking (the batch returns them in any order): `cast_shallow_v1` cellar toad in a flowerpot hat, `_v2` crock mimic (a grinning clay jar), `_v3` wick sprite (a living candle stub), `_v4` cellar spider in a cobweb scarf; `cast_deep_v1` cobweb wraith, `_v2` cave cricket, `_v3` barrel mimic, `_v4` root tangle. In `art/source/round12/cast/`, gallery set "Round 12". Not yet cut to 128 px or wired; random floors will pick monsters from per-depth tables, so each depth wants its own cast.
- **Round 13, the gaps (Codex, 8 batched calls, 27 drafts; Rylee: "I will just review and tell you to remove any that are not in our style"):** none removed so far, all 27 looked on-style when checked. Files by what they show (the batch returns them in any order), in `art/source/round13/<batch>/`: `deep_ground` v1 damp flagstone with a moss sheen, v2 mossy rectangular stones, v3 cracked stone with pale roots; `deep_wall` v1 plain, v2 mossy, v3 ivy and roots; `doors` v1 cellar door closed, v2 open, v3 trapdoor, v4 the Cellar King's sealed stone door with the crown seal; `keys_a` v1 the Bailiff's bell key, v2 the Reeve's iron key, v3 the Warden's lantern key; `keys_b` v1 the Seneschal's wax-sealed key, v2 the King's crown seal, v3 the Marshal's helmet key; `treasure` v1 chest closed, v2 chest open and glowing, v3 gold coins, v4 gems; `props_a` v1 crates and sacks, v2 cobweb corner, v3 wall torch, v4 barrels; `props_b` v1 puddle with a drip, v2 broken pot, v3 glowing mushrooms, v4 roots through stone. Notes: the ground tiles are more detailed and show a faint quilted texture compared with the authored flagstone; the trapdoor is drawn in perspective. Not cut or wired yet (the 9 pictures at 288 px grid need `process_tiles.py`, items `process_sprites.py`).
- **The parchment-and-wood skin is in the game (Rylee: "GO", 2026-10-02):** the pack now carries `skins/parchment-and-wood/` (the 19 pictures `skin.json` names, 128 KB; the raw textures and preview stay in `art/skins/`) and `world.json` has `"skin": "skins/parchment-and-wood"`. Two edits to the pack's copy of `skin.json`: the panel's `fill: "parchment"` was removed (VEFR reads `fill` as a picture file; the player ignores a panel fill, so nothing changes visually) and the credit now says "Rylee and Claude; Codex proofs" (the old text said "training: not cleared", which her rights rule replaced). The source in `art/skins/` is untouched. **Rendered and measured** (real game, Playwright, desktop 1280x800 and phone 390x844): 59 and 51 text elements measured against the pixels behind them, none below 4.5:1, the lowest 5.3:1; no console errors, no missing images, no overflow, no target under 44 px; axe-core clean; keyboard focus ring visible (2 px teal); with `prefers-contrast: more` and forced colours the plain UI returns; the skin adds no animation. Getting there needed four fixes in VEFR itself (#211): the declared ink never reached the text inside panels (reader text was 1.4:1), a 32 px panel patch was tiled into stripes behind the text, the menu's left column was missed, and the gold Whisper button kept a gold background under the wood. **Honest leftovers:** a faint lighter band just inside the carved border (cosmetic; the flat fill is slightly lighter than the picture's edge); the Dusk/Dawn pills, the Messages button and the d-pad are still the plain dark style; on a phone the Dusk/Dawn rail covers the level text (127 px, identical without the skin; the planned declutter fixes it); teal headings in the plain menu measure 3.8-4.3:1 with or without the skin (Rylee's accent colour, a design decision); Cottage's `art/tests` has 19 failures on `main`, all from the three briefs written today not following the brief template (and the tests still demand the stale phrase "training: not cleared").
- **The declutter is in (Rylee: "go ahead with the declutter", 2026-10-02):** Interact is the one big button; Talk, Whisper, Bag and Explore are small icon buttons (words kept for screen readers, a tiny key letter each); the Dusk/Dawn rail moved into Menu > Display ("Time of day"); the top bar is just Menu. This fixed the phone overlap listed above (the rail covered the level text) and two more found while measuring (the health/level/gold row ran under the Menu button; the phone Messages panel sat on the wrapped HUD). Real browser, Cottage with the skin: no two controls overlap at 390/360/320 px wide or at 1280/900; 0 text elements under 4.5:1; no target under 44 px; axe clean. Still true: the Messages button and the d-pad keep the plain dark style under the skin; in phone landscape the place name can sit over the d-pad's top button for 4 seconds (taps pass through); the teal menu headings are the accent-colour decision above.
- **Claude's note:** an offload research worker failed on this VM (`no MiniMax key`); engine foremen should run on Bazzite.

## 2026-10-01 (evening) — Rylee's first playtest of the demo

Her words, in order: "the humonguously big cat made me giggle." "the little bugs were kinda fun." "the first book renders when you leave the house, so you have to walk over your front door (something with the internal vs external cells)." "the wander around and fight things loop feels VERY castle of the winds to me, which I consider a win." "the ui is... coming along <3.... it just really tickles me. the notes, the characters, the items. I can't wait to make it a full thing."

- **Fixed (agent):** the note "A Note Left at the Door" sat at town tile (4,4), which is inside the little house's footprint behind the town door at (4,5); you arrive outside at (4,6). It now sits at (5,6) in the town, one step right of where you arrive, so you find it without going through your own door. Tested by stepping right from the arrival tile.
- **Claude's note, for Rylee to decide:** the cat is drawn as tall as the hero because the player draws every character at the same height (1.5 tiles). It made her giggle, so it has not been changed. Options: keep it as a running joke, or give each sprite a size (a pack-level scale), which is a small engine change.
- **Characters have their own size now (Rylee's pick):** after the giant cat she chose "Make characters their own size". The engine now reads `player.sprite_scale` (0.2 to 2; 1 is standard, 1.5 tiles tall). Cottage sets the cat 0.45, rat 0.5, moths 0.65, rustle 0.85, shade 0.9, dwarf smith 0.85; everyone else stays 1. Claude's note: these numbers are a first guess to tune by eye (the rat may want to be a little bigger). The engine change is in VEFR (PR #186); a game on an older engine just ignores the setting.
- **What worked:** the walk-around-and-fight loop reads as Castle of the Winds, which is the goal. The monsters (the moths especially), the notes, the characters and the items landed.

## 2026-10-01 (later) — the story spine, from Rylee's picks

Rylee picked these from options the agent drafted out of the cellar notes already in the pack. Her picks, quoted exactly as she chose them:

- **Truth one** (what the town will not say about the old tavern that burned): "The fire was meant to hold something down".
- **Truth two** (what the town will not say about the one who went down on purpose): "They came back, and they are in town". **Who:** "The Spell Keeper".
- **The realization at the end:** "What is held down is the town's own kindness".

Claude's note: this matches her earlier notes ("2 pieces of truth and then a realization at the end"; the Keeper "knows what the hero learns at the end from the beginning"). Working notes and a reveal map are in `docs/story-spine-notes.md`; none of it is canon until Rylee moves it into `STORY.md`. Still hers to decide: who the letter's "keeper" is, what exactly was held down (a room, a creature, a fire or a feeling), whether the hero remembers going down before, and how long the ending is.

## 2026-10-01 (later) — the new art and residents in the game (agent drafts, waiting on Rylee)

Rylee kept seven residents from the round 8 pictures (the keeper with the staff, the tavern regular, the trader, the cat, the fisher, the gardener, and the dwarf smith redrawn chibi) and picked hero walk version 1 and the geometric rug. **The names ("The Tavern Regular", "The Cat", "The Fisher", "The Gardener", "The Dwarf Smith"), their voice files and their dusk and dawn first lines are agent drafts**, written to make the loop playable. They are hers to keep, rename, rewrite or bin. The four notes still unwritten for the story are listed in `docs/story-spine-notes.md`.

Claude's note: this repo now also holds `art/tools/` and `art/tests/` (sprite and tile and UI-skin tools with unit tests; run `uv run --offline --with pillow python -m unittest discover -s art/tests -t .`). `AGENTS.md` still says the repo has no tests of its own; that line is Rylee's to update.

## 2026-10-01 — the Spell Keeper draft is approved (Rylee)

Rylee told the agent on 2026-10-01 that she worked through the 2026-09-29 agent draft (the Spell Keeper, her lines and seed bank, the two books, the three-rule `logbok.md`, the world description and creed) with an agent and that it is **approved**. It no longer waits on her. `STORY.md` is still hers to write; nothing was added to it. If a line changes again, record it here.

Playtest note (agent, 2026-10-01, woven offline build, desktop): the title screen and the first room load with no console errors. The hero starts bottom right of the cottage room; one arrow press moves her one tile (she starts at tile 4,5; the "about four tiles" look came from the display scale of up to 3x plus held-key repeat, corrected 2026-10-01 after a foreman measured it), and the exit is a door below the bottom wall that needs the hero lined up with it and Interact (F) pressed. The Strike / Console / Hurl an insult buttons show with nothing to fight. Claude's note: both worth a look, neither is a decision.

## 2026-09-29 — agent draft: the story layer (waiting on Rylee)

Built through the studio: Act 1's town map (the Map Room's own check +
build), plus one book. The words below are an **agent draft drawn only
from Rylee's own NOTES** — not canon. `STORY.md` stays hers; every line
is hers to keep, change or bin.

Drafted (all draft):
- `world.json` description (Rylee's BRIEF pitch, verbatim) and creed.
- `logbok.md` — three plain rules.
- the spell keeper: `voices/keeper.md`, the two seed lines, the offline
  fragment bank, and the ledger anchors. Renamed "The Keeper" to
  "The Spell Keeper"; she stands at the shop door.
- one book she hands over: `library/the-burnt-taverns-tab.md`, and one lying
  by the cottage door (`library/a-note-left-at-the-door.md`, a map find).
- the Emberfield leftovers (map note, world-tree history) cleared.

The woven game now draws the people, not just the map: the Spell Keeper
appears on her tile so you can see who is there to talk to.

Read the spell keeper's lines against your notes before they ship.

## 2026-09-26
- **The pitch is written** (Rylee, BRIEF.md): "a fun, low bandwidth way to
  be able to be curious when I can't do anything but still want to do
  *something*." Verb: explore. Done when "I lost an evening to it."
- **Title picture and colour** (Rylee's picks): the dusk cottage with one
  stair going down (`assets/title.webp`), and dusk teal `#3F7E84`.
- **Things Rylee wants to find while exploring**: a piece of history (a
  story, a trinket or picture), a hidden door, a spell book, armor or a
  weapon. Painted as stickers (media_files, `designs/vefr/art/cottage/finds/`).
- **Ideas, not decided yet** (Rylee): "I always liked how there were hidden
  rooms in cotw", and "you could randomly teleport as a form of hard mode".
  Claude's note: an opt-in hard mode would keep the default low bandwidth.
- **How hidden rooms felt in CotW** (Rylee): "I used wasd mostly, lots of
  hitting walls and hoping the spiders didn't get me." Claude's note:
  walking into a wall as the only "search" keeps controls simple.
- **Progression** (Rylee): "a normal everquest-like progression is good."
- **The town** (Rylee): "a lone tavern with a few npc's in it", as an
  interior, "and evidence of an older tavern that burned down".
- **Where the stair starts** (Rylee): "right out of the cottage, like you
  just couldn't help but keep going down. maybe you're a bit of an
  outcast because of it".
- **The ending's shape** (Rylee): "2 pieces of truth and then a realization
  at the end"; the realization changes how you see the town, the cottage
  and yourself ("all of the above"). What the truths are is still open.
- **The tavern's feel** (Rylee): "cozy but wary of you".
- **The one who isn't wary** (Rylee): the spell keeper. "she gives you a
  little discount and maybe a baked good and a happy word when you see her".
  And "she's the one that probably knows what the hero learns at the end
  from the beginning".
  "She loves to bake little loaves of pound cakes with cinnamon and honey."
  Her look (Rylee's pick of three drafts, "spell keeper C"): plump and
  cheerful, dark curly hair tied in a teal scarf, freckles, a brown cardigan
  with rune buttons, a tiny glowing rune above her palm. Draft art only
  (media_files `designs/vefr/art/cottage/drafts/spell-keeper/`).
- **Decision: the release is made IN VEFR** (Rylee: "I want the actual
  release to be made IN vefr, ok?"). Hand-made pictures and notes are drafts,
  reference and templates. The shipped game comes out of the studio:
  characters through the Folks room, pictures from studio modules, the file
  from `ratatoskr weave`.
- **Playing CotW** (Rylee): most essential to recreate first are going
  down the stairs, loot and mystery items, and carrying and packing.
  Inventory in CotW and Diablo is "not terribly rewarding"; the reward is
  opening and finding something fun. Decisions in DESIGN.md.
- **Models help in the studio; the game is a finished artifact** (Rylee).
  Residents and local models help while the game is being made, inside
  templates and structure, and Rylee approves what they draft. The shared
  game plays completely without a model. Cottage of the Breeze doesn't
  offer one (VEFR's default); see VEFR `docs/adr/0003`.
- **Losing: the player chooses** (Rylee). At the start: Cozy (you faint
  and wake in the temple, losing a little gold or an unidentified item,
  never progress) or Classic (death is real; load a save). A Classic run
  can switch to Cozy later, never back.
- **Time: turn-based** (Rylee), like the original. Nothing moves until the
  player acts; then monsters take their turn.
- **Working title: Cottage of the Breeze** (Rylee). A cozy name of its own,
  so a shared version never needs renaming.
- The game's home is this private repo. The pack was scaffolded by VEFR's
  "begin a new world": it currently holds the **Emberfield demo frame**
  (CC0; see `worlds/cottage-of-the-breeze/LICENSE`) as placeholder: map,
  keeper voice, logbok. All of it is meant to be replaced by Rylee's own.
- Structural order (Rylee): this home → the Library ruleset → Spark (the
  local brain).

## 2026-09-25
- The first studio game is a *Castle of the Winds* remake, built inside
  VEFR, step by step, as the way to build VEFR (estate vision doc Q9).
- Rylee writes the stories; Urðr keeps the Library.

Also: the town is drawn (through the Map Room's own route): the cottage
with its stair down just outside the door (the real stair tile), the lone
tavern where the Spell Keeper is, a path between them, the burned walls of
the old tavern, and the temple with its rug. Grass outdoors, wood floors
inside, cobbled walls.

The map now has a camera (vefr): the town still shows whole, and a bigger
map would scroll with the hero. The characters are sprites from Rylee's art.

There are rooms inside now (vefr regions + transitions): step on the
cottage door to enter the cottage, the tavern door to enter the tavern -
the Spell Keeper is in there, behind the bar.

The stair goes down now: a first dungeon floor (30x20) hangs off the
top-left stair, with a stone floor, walls, rubble and an up-stair back to
town. The named places answer when you use them. Doors are used (press
Interact), not walked through.

**floor-1 is the authored floor.** Like the original's fixed first level,
floor-1 is written by hand, not generated - it is where the introduction
lives. Deeper floors can be built from rules later.

Intro lore drafted there (agent draft, Rylee's to keep): four notes found
on the floor - a scrap about two things the town will not say, a burned
page about the old tavern, a candle and a note left by someone who went
down before you, and a coin set face-down.

**Generated floors begin.** floor-2 and floor-3 were drawn by the engine's
new generator from the seed 'cottage-1' (norns delve), hung off floor-1's
down-stair. floor-1 stays authored; these came out of rules. Rerun with a
different seed for a different dungeon - or hand-fix any of the maps.

Fog of war on the floors (vefr): only what you have walked is drawn - a
lit radius around you, your path remembered dimmer, the rest black.
floor-1/2/3 have it; the town and rooms stay bright.

The floors are big now: 48x32, 16 rooms, and a foggy floor is read a
screen at a time and scrolls. Deeper floors can be made bigger or
tighter.

Something to fight: enemies on the three floors (a cellar rat; shades and
moths; a rustle), the hero has health 6 / attack 2, and dying is Cozy -
you wake in the temple with everything that mattered. Walk into a monster
to hit it; it will come at you when it sees you.

Things to find and carry: the rat on floor-1 drops a cloudy potion, a
floor-2 monster drops a brass ring, and the chest's letter comes with a
ring. Walk onto a drop to take it; the Bag (in the menu) lists what you
carry. Item art from the painted Delve set.

The reward end: The Trader keeps a stall on the road (Interact to trade -
sell what you carried, buy a potion). Gold and the bag persist; the Bag has
its own button and the B key. A cloudy potion can be drunk from the Bag to
heal. No identifying or haggling yet.

## 2026-10-01: the new art and residents are in the game

- **Hero** is the new idle pose (round 9). **Residents:** the Spell Keeper wears the old-keeper picture, the Trader the trader, and five new people were added with the studio's own
  `place_character` route on a copy of this pack: the Tavern Regular (tavern), the Cat (cottage, by the rug), the Fisher, the Gardener and the Dwarf Smith (town). `EDITS.md` records them.
- **Ground:** the town's grass and cobbled street, the tavern's dark planks and the cellar floors are 3x3 grid pictures (one scene, so they do not repeat tile by tile). The cottage's
  rug is ONE object (the geometric rug laid on the floor as a 3 x 2 grid), so its map block `DDD` sits at x 3 to 5 and y 2 to 3 (a grid picks its cell by position: x mod 3, y mod 2).
  The cottage, tavern and town walls and houses use the round 2 stone and wood. The tavern's tables and bar are the round table and the bookshelf on the plank floor.
- **Sprites are keyed by the speaker's id** (`hearth-cat`, `vendor`, `tavern-regular`, ...): the woven player draws a speaker with the sprite named like its id; a speaker's own `sprite` field is
  not read (the loader drops it). So the cat's picture is `sprites/cat.png` under the key `hearth-cat`.
- Two engine bugs found by doing this with the real route are fixed in vefr (#183: a write on a multi-room pack threw away the room list; #184: placement checks used the home room's map).

