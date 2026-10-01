# NOTES — decisions and playtest notes (newest first)

## 2026-10-01 (evening) — Rylee's first playtest of the demo

Her words, in order: "the humonguously big cat made me giggle." "the little bugs were kinda fun." "the first book renders when you leave the house, so you have to walk over your front door (something with the internal vs external cells)." "the wander around and fight things loop feels VERY castle of the winds to me, which I consider a win." "the ui is... coming along <3.... it just really tickles me. the notes, the characters, the items. I can't wait to make it a full thing."

- **Fixed (agent):** the note "A Note Left at the Door" sat at town tile (4,4), which is inside the little house's footprint behind the town door at (4,5); you arrive outside at (4,6). It now sits at (5,6) in the town, one step right of where you arrive, so you find it without going through your own door. Tested by stepping right from the arrival tile.
- **Claude's note, for Rylee to decide:** the cat is drawn as tall as the hero because the player draws every character at the same height (1.5 tiles). It made her giggle, so it has not been changed. Options: keep it as a running joke, or give each sprite a size (a pack-level scale), which is a small engine change.
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

