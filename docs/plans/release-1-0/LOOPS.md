# Cottage 1.0: the fifteen loops

**What this is.** Every loop a player lives in, from the one-second bump to the
whole 36-floor story, judged from the player's chair: what it feels like today,
whether it is good, and the smallest change that makes it satisfying. It sorts
each loop into **Keep**, **Refine**, **Rethink** or **Build**, and says who does
the work: this pack, the VEFR engine, Rylee's words, or new art.

**Status: analysis and plan (Claude, 2026-10-29).** It sits under
[Cottage #168](https://github.com/rylee-bee-labs/cottage-of-the-breeze/issues/168),
which is owner-approved direction, and the [five-gate roadmap](ROADMAP.md). It
adds no new feature to that direction: every loop below is one #168 already
names, or one the game already has. It changes no canon and no existing words.
**Nothing here is built by this page.** Direction approved ≠ implemented ≠
verified ≠ shipped.

**Evidence it rests on.**

- A full monsters-on run by the playthrough bot: **44 of 44 checks** at 1280 × 720,
  all eight cellar floors, Cottage `288bfe8` + VEFR `db3df92` (2026-10-29), with
  screenshots looked at by eye.
- A code-level audit of the VEFR player at `db3df92` (`web/player/parts/*.js`,
  `src/vefr/shapes.py`). File names below are in that tree. The key claims were
  re-checked in the source.
- The canon ([`docs/story/STORY.md`](../../story/STORY.md)), the playtest of
  2026-10-09 ([`docs/playtests/2026-10-09-descent.md`](../../playtests/2026-10-09-descent.md)),
  `NOTES.md`, `DESIGN.md` and the open issues.

---

## The short version

**What is already good, and must not be lost.** The town reads instantly and is
genuinely lovely. Finding a book is still the best beat in the game. The
walk-and-bump loop "feels VERY Castle of the Winds" (Rylee, 2026-10-01). The
Key Warden that yields instead of fighting is the game's own idea and a good one.
Section 1 is completable, start to end card, with monsters on.

**What is thin.** The descent is 36 floors of the same three numbers. Monster
stats do not rise with depth (`curve` is unwired), loot has no mechanical effect
(rarity and traits are words in the name only), gold only comes from selling, and
the Trader sells everything forever at the price he pays. The bot finished the
cellar with a bag full of candle stubs, shoe buttons and moth wings, none of
which can be sold. On floor 3 the hero was at 2 of 14 health with no way to heal
that costs anything; on the warden floor nothing says *this is the warden floor*.

**What needs rethinking, not polishing.**

1. **Going home and coming back.** Every return to town starts the next trip at
   floor 1 (`397-the-descent.js`: landings are recorded but nothing reads them).
   Over 36 floors that turns "one more trip" into "walk it all again". This is the
   single biggest loop-killer, and it blocks loops 7, 8, 9 and 12.
2. **Loot that matters.** Today a kill always drops exactly one thing, chosen
   evenly, and rarity changes nothing. The approved direction (Diablo-lite traits,
   a few legendaries, builds) needs traits that *do* something.
3. **Healing that costs a turn.** Potions, spells and resting are free actions, so
   any heal is a pause button in the middle of a fight. Tactics need it to cost a
   turn.
4. **Sections 2 to 4 follow canon.** The pack's rootworks, siltworks and emberhall
   are agent labels from before canon was promoted. Canon's Sections are the
   **Long Well** (wet, listening, enormous), the **Banked Fire** (soot, chimneys,
   the first warm place) and the **Blue Door**. The creatures, tiles and wardens of
   2 to 4 should be rebuilt to canon's places. **One decision is Rylee's** (below).

**The one card a player needs** (the "easy core systems"; everything else is
discovered, never memorised):

> Walk into things: a monster to strike it, a chest to open it, a person to talk.
> You have **Health**, **Attack** and **Guard**. Gear goes in five slots; how rare a
> thing is shows as a frame, a word and a glow, and what it really does shows once
> it is identified. You know a few **spells**, each with a few charges that come
> back when you rest. Your **satchel** has slots and can grow. If you fall, you wake
> at home and your satchel waits where you fell. Before you go down, pick a
> **Wind** at the Windrose.

---

## The fifteen loops at a glance

| # | Loop | Cadence | Today | Verdict | Mostly needs |
|---|---|---|---|---|---|
| 1 | Peek into the dark | seconds | fog, autoexplore, decals | **Refine** | pack + art |
| 2 | Bump and topple | seconds | hp/atk only, flat by depth | **Rethink** | VEFR |
| 3 | Open it and gasp | seconds | 1 forced drop per kill, rarity is text | **Rethink** | VEFR + art |
| 4 | Try it on | minutes | 5 slots, hp/atk mods | **Refine** | VEFR + pack |
| 5 | What is it really? | minutes | free identify exists, unused | **Build** (pack) | pack |
| 6 | Learn and cast | minutes | heal-only, free, unlimited | **Rethink** | VEFR + pack |
| 7 | One more floor? | minutes | no way home but the vault | **Rethink** | VEFR |
| 8 | Haul it home | a trip | junk unsellable, shop sells all | **Rethink** | VEFR + pack |
| 9 | Hearth and rest | a trip | rest moves the clock, no heal | **Refine** | VEFR + pack |
| 10 | Face the warden | a Section | Section 1 good; 2–4 borrowed | **Refine** | pack + art + words |
| 11 | Secrets and sleepers | a Section | Keybearers unplaced, secrets unwired | **Build** | VEFR + pack |
| 12 | Fall and fetch | a trip | wake on the floor, lose nothing | **Rethink** | VEFR |
| 13 | Fill the album | the game | strong; a few stickers unreachable | **Keep** | pack |
| 14 | Home grows warmer | the game | one town state | **Build** | pack + words |
| 15 | Pick the Wind | replay | not built | **Build** (Gate 3) | VEFR + pack |

Five **Keep/Refine**, five **Rethink**, five **Build**. That is fifteen loops,
four of which (1, 2, 10, 13) already work and are worth protecting.

---

## The loops, one by one

Each card: **the moment** (what the player does and feels), **today** (what the
code does, with evidence), **to make it satisfying** (smallest first), **who**,
and the roadmap **gate**.

### 1. Peek into the dark

**The moment.** You step, the fog peels back a little, and something glints at the
edge of the light. You go and look.

**Today.** Fog radius per Section, autoexplore (O), decals (cobwebs, torches,
puddles). What the light reveals is mostly more corridor: the 2026-10-09 playtest's
B1 "a generated floor has nothing in it to find" still holds. Walls and floors are
both cobbles and read as one texture (seen on floors 3 and 8; cottage#166).

**To make it satisfying.**
- Something worth walking to in most rooms: chests (loop 3), a dropped satchel
  (loop 12), a book, a resting Keybearer (loop 11). The generator already computes
  chests and secret rooms (`396-engine-delve-v3.js`); the player drops them.
- Walls that read as walls: art slots `cellar-wall-2`, `well-wall`.
- `pois` names ("the banked fire", "a chair nobody sat in") shown as a place line
  when you step into the room. They are written and validated, and unwired.

**Who.** VEFR (chests, secrets, pois on generated floors) · art · pack.
**Gate.** 0 for walls (#166); 1 for things to find.

### 2. Bump and topple

**The moment.** Walk into a rat. *"You hit a cellar rat for 3. It falls."* One
line, one kill, one number that went up. Then, deeper, a fight you have to think
about for two seconds: that one is armoured, hit it with the shovel; those three
come together, fight them in the doorway.

**Today.** Bump attack, sleep/wake/noise, chase, flee at a third of health, all
built (`430-loot-on-the-floor.js`, `420-how-a-monster-thinks.js`). Damage is
exactly your Attack: no Guard, no misses, no weakness on generated monsters, and
`curve`, `elites` and `groups` are validated but unwired (`shapes.py`,
`wired=False`). So monsters are the Blueprint's numbers on floor 1 and floor 36,
while the hero levels: the danger curve Rylee decided ("Rising") runs backwards.
The default verb row also offers "Console" and "Hurl an insult", because
`acts/act-1/world.json` names no `verbs`.

**To make it satisfying.**
- **Wire `curve`** so each Section rises gently, as decided.
- **Guard**: one flat number off every hit, never below 1. Body, head and feet gear
  give it. That alone makes gear choices real.
- **One weakness or resistance per creature**, read off its family
  (`resist`/`weak` on Blueprint families; the engine already has damage types in
  `425-the-elements.js`, only not for generated monsters).
- **Elites and linked groups**, already in the Section schema: a named elite now
  and then ("a stubborn cellar rat", +50% health, a guaranteed good drop), and
  groups that wake together.
- Pack: set `verbs` to just the strike, unless Rylee wants the others.

**Who.** VEFR (curve, guard, monster resist/weakness, elites, groups) · pack
(numbers, verbs) · art (`creatures-deep` batch, so 2 to 4 have their own animals).
**Gate.** 1.

### 3. Open it and gasp

**The moment.** A chest in the corner. You open it, it glows, and the thing inside
has a frame you have not seen before. The thrill Rylee named: "opening something
and finding something fun".

**Today.** A generated kill drops **exactly one** id from the family's list, chosen
evenly, every time (`397-the-descent.js`). Rarity and traits can be rolled, but they
only change the item's name text (`180-gold.js` `carriedName`). The only chests are
library books with `chest: yes`. No gold ever drops.

**To make it satisfying.**
- **Drop chance and weights**, so a drop is a small event, not a receipt.
- **Chests on generated floors** (the generator already places them), with a
  rarer chest on `treasure` specials.
- **Rarity that does something**: common 0 traits, fine 1, rare 2, heroic 2 with
  one strong, mythic 3 with one unique. Shown as frame shape + word + glow, never
  colour alone (DESIGN.md). A few **legendary** named items per Section, authored.
- **Gold on the floor** (`coin-pile`).
- **Keepsakes go to the album pouch, not the bag**, so the fun junk never crowds out
  the gear.
- The reveal moment: a spin with motion on, instant with motion off (decided).

**Who.** VEFR (drop chance, chests, trait effects, gold, rarity frames) · pack
(trait tables, legendaries; trait *names* are words, so Rylee approves them) · art
(`loot-and-chests`, `items-gear-1`, `ui-rarity`).
**Gate.** 1. This is the heart of the build loop.

### 4. Try it on

**The moment.** You hold the new coat up against the old one, see the numbers that
would change, and put it on. You feel it on the next floor.

**Today.** Five slots (hand, body, head, feet, charm) with `hp`/`atk` mods
(`370-engine-equip.js`). Eight wearable items in the game, all fixed.

**To make it satisfying.**
- A compare line when you pick something up: `Attack 4 → 5, Guard 1 → 0`.
- Traits that change *how* you play, not only how much: "your first hit each fight
  strikes twice", "a kill warms you for 1 health", "fire weakness creatures take
  double". This is where #168's combos live: a few bounded reactions, each logged
  in plain words, never chaining past a cap.
- Charms carry the strangest traits; that is what makes a charm exciting.

**Who.** VEFR (compare, trait effects, reaction cap and log) · pack (trait tables)
· art (`items-gear-1`).
**Gate.** 1.

### 5. What is it really?

**The moment.** You come home with three things you do not understand yet. You lay
them on the reading desk and learn that the plain ring is the best thing you own.

**Today.** A free identify service exists for any resident with `identify: "true"`
(`195-the-identify-service.js`). No Cottage resident has it, and nothing rolls
hidden traits, so there is nothing to identify yet.

**To make it satisfying.**
- Give one resident the service (the Spell Keeper fits canon's "she has known how
  this ends"; Rylee's call if a different person).
- Once loot rolls traits (loop 3), they stay hidden until identified: in town for
  free, or in the field with a scroll (`identify-scroll`).

**Who.** Pack, the moment loop 3 exists. One line of `acts/act-1/world.json`.
**Gate.** 1.

### 6. Learn and cast

**The moment.** A spellbook in a chest. You read it and now you can *do* something
new: light the room, slow the thing chasing you, mend a scrape. You have three goes
before you rest, so you think about when.

**Today.** Spells exist but only heal, cast for free, without limit, without
spending a turn (`225-spells.js`). The Spell Keeper keeps no spells.

**To make it satisfying.**
- **Charges, not mana**: each spell has two or three, back on a rest or at a
  landing. One number per spell, nothing to manage.
- **Casting takes a turn.**
- **About eight spells** across the six schools DESIGN.md names (attack, defense,
  healing, movement, divination, other), learned from found books and from the
  Spell Keeper. Effects the engine already half-has: light/reveal (`460-light.js`),
  burn (`425-the-elements.js`), heal. Spell *names* and words are Rylee's.

**Who.** VEFR (charges, turn cost, effect kinds) · pack (the spell list) · art
(`items-reading`).
**Gate.** 1.

### 7. One more floor?

**The moment.** Half health, a full satchel, the stair down right there. Go home
now and keep it all, or push one more floor for the landing? A real, small choice
every trip.

**Today.** The only ways up are the up-stairs, floor by floor, and the vault stair
at the end of the Section (playtest M4). A landing's up-stair goes straight to
town, but the next trip **starts at floor 1 again** (`397-the-descent.js`: nothing
reads `landings()`). The bag has a size (`bag.size`) and Cottage does not set it.

**To make it satisfying.**
- **The lift back down**: from home, start at any landing you have reached. This is
  the most important engine change on this page.
- **A way home from any floor** (`way-home-charm`), costly enough to be a decision.
- **Satchel slots plus upgrades** (decided 2026-10-08): set `bag.size`, sell
  `satchel-2` and `satchel-3`.

**Who.** VEFR (lift down to a landing; recall item) · pack (bag size, items) · art.
**Gate.** 1 for the lift and bag; 2 needs it across all four Sections.

### 8. Haul it home

**The moment.** You tip your satchel out on the Trader's stall, he pays without
asking where any of it came from, and you buy the thing you have been eyeing.

**Today.** Buy and sell work (`190-the-trade-panel.js`), but buying lists **every
priced item in the game, unlimited, at exactly the price he pays**, so selling a
ring and buying it back costs nothing. Ten of the drops (the album keepsakes) have
no `value`, so the bot's whole haul was worth nothing.

**To make it satisfying.**
- **A stock list** per Trader, refreshed each trip home, and growing as the town
  does (loop 14).
- **Buy at about twice the sell price.**
- **Gold drops** (loop 3) so a trip pays even with nothing to sell.
- Something to save up for: satchels, the way-home charm, a spell, a Windrose
  upgrade.

**Who.** VEFR (stock, margin, gold drops) · pack (prices, stock).
**Gate.** 1.

### 9. Hearth and rest

**The moment.** Home. You sit by the fire, your health comes back, the light changes
from dusk to dawn, someone says a line that is different now. You feel ready.

**Today.** Resting moves the clock but **does not heal** (`255-time-rest.js`); the
temple you wake in is shut until the cellar is done; there is no inn or temple heal.
Cozy death heals you fully, so today the only full heal is falling over.

**To make it satisfying.**
- **Rest heals and refills spell charges**, at the cottage hearth. That is the home
  ritual: heal, sell, identify, talk, go.
- A small, cheap field heal (`tea-flask`) so the potion is not the only answer.

**Who.** VEFR (a rest that heals) · pack (where, and the flask) · art.
**Gate.** 0 to 1. Cheap and high-value.

### 10. Face the warden

**The moment.** The floor is different: a dais, braziers, something large and
patient. Each Section ends on a guardian you remember, and not every one is a
fight.

**Today.** Section 1's Key Warden is a `rule` challenge that yields; the bot plays
it and it ends the act (good, and the game's own idea). On screen the warden floor
looks like every other floor. Sections 2 to 4 have plain-fight wardens wearing
borrowed pictures: the Root Warden is a root tangle, the Silt Warden a barrel mimic,
and the Ember Warden named a sprite that did not exist, so the last boss drew as a
plain placeholder figure (**fixed in this change**: it now wears the shade, as
interim).

**To make it satisfying.**
- A warden floor that **looks** like one: `warden-dais`, `vault-floor`.
- Each warden its own picture (`wardens-well-fire`) and its own way to be met:
  the engine already supports `challenge: defeat | rule`, `yields`, `fightable`.
- Canon's answers arrive here, twice: once read, once said by a resident.

**Who.** pack (warden setup) · art · **Rylee's words** for each Section's answer.
**Gate.** 2.

### 11. Secrets and sleepers

**The moment.** A draught from a crack in the wall. Behind it, asleep on a pile of
moth-wings, Ashwing, with a key. You do not have to fight it. You just have to find
it.

**Today.** The three Keybearers are in canon and in the Blueprint, with art, but no
Section places them. Their key books give the keys on reading. Secret rooms are
generated but never saved or shown; `specials` (treasure, infested, hub) are labels
with no effect; locked doors and keys work only in hand-made regions.

**To make it satisfying.**
- `special` floors that mean something: **treasure** has a better chest, **infested**
  has an elite group and a better drop, **hub** has a resting spot.
- **Secret walls** you find by looking (`secret-crack`), never by pressing every wall.
- **Keybearers placed** on a special floor as sleeping, non-fight guardians, and a
  **vault door** (`vault-door`) their key opens on a later floor.

**Who.** VEFR (special effects, secrets, sleeper placement, locked doors on
generated floors) · pack · art (`ways-secret`).
**Gate.** 2.

### 12. Fall and fetch

**The moment.** You fall. You wake at home, safe, everything you *learned* kept. The
satchel you were carrying is on the floor where you fell, sparkling. Going back for
it is a little quest of your own.

**Today.** Cozy death heals you fully and wakes you **on that same floor's
up-stair** with nothing lost (`430-loot-on-the-floor.js`, `397-the-descent.js`).
That is gentler than #168's approved direction ("Death returns the player to town;
dropped resources are recoverable") and removes all tension from a fight.

**To make it satisfying.**
- Fall → wake at home; levels, spells, gear worn, books, album kept.
- The satchel's contents (not worn gear) wait on that floor as `dropped-satchel`,
  marked on the map, once. Fall again before fetching it and the older one is gone.
- Classic mode (death is real) stays the opt-in DESIGN.md decided; it is a later
  engine slice.

**Who.** VEFR · art (`dropped-satchel`).
**Gate.** 1 (a trustworthy defeat/recovery loop is one of Gate 1's exit proofs).

### 13. Fill the album

**The moment.** A sticker. A riddle you can almost answer. A page with three gaps
you now want to fill. Books you can reread at your own pace.

**Today.** Strong and working: 18 stickers in Section 1, riddles, a foil shine, 14
books, a Library you can reread. The bot found 15 of 18; three are chance drops.
Stickers are text-only (no picture in the album).

**To make it satisfying.**
- Keep it. Add stickers for each Section's creatures and places as Sections 2 to 4
  are built (words: Rylee).
- Album pages by Section, so "three left on this page" is visible.
- A bestiary page is a cheap later win (it is the same data).

**Who.** pack · words.
**Gate.** 2.

### 14. Home grows warmer

**The moment.** Each time you come back from a deeper place, home is a little
different: the smith has work again, the Gardener grows a flower, a keepsake from
the warden sits on your shelf, someone says the thing nobody would say.

**Today.** One town state (`town-after-the-cellar`: the temple door propped open)
and one line per resident after Act 1. The engine's `town_states` swaps a whole
region per flag, which is enough.

**To make it satisfying.**
- One town state per Section's end (four total), each adding **one service** and
  **one visible change**: Section 1, identify at the reading desk; Section 2,
  the Smith mends and upgrades (`mending-rack`; mending recipes exist in
  `186-the-mending.js`); Section 3, a fuller Trader; Section 4, the ending's warmth.
- A **keepsake shelf** in the cottage that fills, one thing per warden.
- Kindness that changes a line: canon's "each answer arrives twice".

**Who.** pack (states, rules) · **Rylee's words** (every new line) · art
(`town-services`).
**Gate.** 2.

### 15. Pick the Wind

**The moment.** Before you go down, you turn the Windrose to Gust. This trip the
floors are longer and the loot richer; next time you will try Squall. Once in a
while a passing Wind changes one floor, and once in a great while, a Zephyr.

**Today.** Not built. The engine has an unwired `omens` schema in Python only
(`shapes.py`), and Winds are VEFR #489's to build generically.

**To make it satisfying (and no bigger than this).** One readable difference per
Wind, using knobs loops 1 to 3 already need: fog radius, room count, monster groups,
loot chance, special-floor chance. One passing-Wind floor event. A few Zephyr
surprises. Effects end with the expedition; the treasure stays (decided).

**Who.** VEFR (expedition-scoped modifiers) · pack (the five Winds' tables) · art
(`windrose`, `ui-winds`).
**Gate.** 3. Do not start before Gate 2.

---

## The engine companion list (for VEFR #489)

Engine work this game needs, recorded here as companion changes per `AGENTS.md`
(never edited from this repo). Smallest and highest-value first. Each is generic:
no Cottage names.

| # | Change | Unblocks loops | Today's evidence |
|---|---|---|---|
| E1 | **Start a trip at any reached landing** | 7, 8, 9, 12 | `397-the-descent.js`: `landings()` recorded, never read |
| E2 | **Rest heals and refills charges** | 9, 6 | `255-time-rest.js` moves the phase only |
| E3 | **Heal, use and cast cost a turn** | 2, 6 | `480-town-input-and-turns.js`: only step, bump, verb spend a turn |
| E4 | **Wire `curve`** on generated floors | 2 | `shapes.py` `wired=False` |
| E5 | **Drop chance + weights; gold drops** | 3, 8 | `397-the-descent.js`: one uniform drop per kill; `addGold` only in trades |
| E6 | **Shop stock list and margin** | 8 | `190-the-trade-panel.js`: every priced item, buy = sell |
| E7 | **Guard stat** (gear `mods.guard`) | 2, 4 | `370-engine-equip.js`: hp and atk only |
| E8 | **Traits with effects** + rarity frames, bounded reactions with a why-log | 3, 4, 15 | `180-gold.js`: traits are name text only |
| E9 | **Chests and secrets on generated floors** | 1, 3, 11 | `396-engine-delve-v3.js` computes both; the player drops them |
| E10 | **Monster resist/weakness, elites, groups** on generated floors | 2 | `shapes.py` `wired=False`; `410-the-living-hazards.js` never copies `resist` |
| E11 | **Spell charges and effect kinds** (light, burn, slow, ward) | 6 | `225-spells.js`: heal only |
| E12 | **Fall → home, satchel waits** | 12 | `430-loot-on-the-floor.js`: wakes on that floor, nothing lost |
| E13 | **`specials` and `pois` do something** | 1, 11 | labels only |
| E14 | **Sleeping guardians placed by a Section** | 11 | not placeable off the warden floor (GAP.md slice 6) |
| E15 | **Interface icon slot for a pack** (rarity frames, Wind marks) | 3, 15 | no pack UI icon slot; the skin covers panels only |
| E16 | **Expedition-scoped modifiers (Winds)** | 15 | `omens` schema, Python only |

E1 to E3 are small and change how every trip feels. E4 to E8 are the Gate 1 build
loop. E9 to E14 are Gate 2. E15 and E16 are Gate 3.

## Pack work that needs no engine change

Safe to do now, each validated with `norns validate` and the playthrough bot:

- **Fixed in this change:** the Ember Warden's sprite (`blueprint.json`), which
  named a picture that did not exist.
- Give one resident `identify: "true"` once traits roll (loop 5).
- Set `verbs` to the strike alone in `acts/act-1/world.json`, if Rylee agrees the
  "Console" and "Hurl an insult" buttons do not belong (loop 2).
- Set `bag.size` once satchel upgrades exist to buy (loop 7).
- Keep album keepsakes out of the economy until E6 lands: giving them a `value` now
  would also put them on sale, unlimited.
- Draw the art the loops need: `art/manifest/slots.json` and the briefs in
  `art/requests/` (see `art/manifest/README.md`).

## The one decision that is Rylee's

Everything above is either approved direction (#168) or an implementation detail
chosen the smallest compatible way. One thing is canon, so it is hers:

> **Sections 2 to 4 are rebuilt to canon's places: the Long Well, the Banked Fire
> and the Blue Door.** Today's rootworks, siltworks and emberhall are agent labels
> that predate the canon. Canon describes the Blue Door as one door and the unburnt
> room behind it; the 1.0 plan gives Section 4 nine floors. **What are Section 4's
> nine floors?** (For example: the passage behind the Blue Door, or the Banked
> Fire's far side leading up to it.) The art requests for Section 4's own creatures
> and warden wait on that answer; the Long Well's and the Banked Fire's are
> drafted.

Names, spell and trait words, and every new line stay drafts until she approves
them, as always.

## Parked (not 1.0)

From the roadmap's parked list, restated so this page cannot grow them: endless
mode, a big Wind catalogue, crafting beyond the mending recipes, classes, farming or
life-sim chores, bank, branching quests, multiplayer, native app. Ideas that came up
while writing this and are parked here, not built: a bestiary page, sticker pictures
in the album, pack audio files, ranged and spell-casting monsters, traps.
