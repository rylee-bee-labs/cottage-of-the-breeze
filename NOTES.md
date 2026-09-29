# NOTES — decisions and playtest notes (newest first)

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
