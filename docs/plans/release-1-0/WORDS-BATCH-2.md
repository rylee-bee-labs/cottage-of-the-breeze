# Words, batch 2: monster skills and something to throw

**Status: draft, waiting for Rylee.** Her rule (answer 14) is "I draft, you
approve batches". Nothing in this batch is in the game yet except the engine's
own sentences (the last section), which VEFR ships for every game and she may
veto. The thing to throw waits for her pick: once she approves a name, it goes
into `world.json` in its own PR.

## Something to throw (her pick: "Throw things")

One kind of thing, found on rats and spiders. It is thrown at the nearest
monster within 5 tiles, does 2, and lands where it struck, so she can pick it
up again. It goes on the quick bar, and a **Throw** button joins the fight row
while she carries one.

| Option | Name the player reads | Why |
|---|---|---|
| **A (recommended)** | **a stale bun** | cozy and a little silly: the cellar's rats would know a bun when it hits them |
| B | a smooth pebble | plain and believable |
| C | a clay marble | a found toy, like the shoe button and the thimble |

Each needs a small picture. Until one is made it shows as the bag's plain dot.
The picture brief goes to Momma's image agent once a name is picked.

## The fight row

| Button | Word | Note |
|---|---|---|
| throw | **Throw** | shows only while she carries something that can be thrown |

## What each monster now does (no new pack words)

These are the four cellar families' skills (DESIGN.md, 2026-10-30). The words
they say are VEFR's engine sentences, listed below.

| Monster | Skill | What happens |
|---|---|---|
| a cobweb-scarfed spider | web | from up to 3 tiles away, on a clear line: stuck for 2 turns, at most once every 6 of its turns |
| a cobweb-scarfed spider | spit | from up to 4 tiles away: a hit for 2 (guard takes from it), at most once every 4 of its turns |
| a cellar rat | festering bite | 30 in 100 of its bites that land: 1 a turn for 3 turns |
| a nest of moths | dust | 40 in 100 of its blows that land: her blows miss 25 in 100 more often for 3 turns |
| a fat cellar rat | squeal for help | once, when struck to half its health: every monster within 16 tiles wakes |

## Engine sentences the player now reads

VEFR's own defaults (ADR 0024), not pack words:

- "{monster} throws a web over you: you are stuck for {n} turns."
  "You struggle in the web." / "You pull free of the web."
- "{monster} spits at you for {n}." / "{monster} spits at you and misses."
- "The bite festers: {n} a turn for {t} turns."
  "The poison takes {n} from you." / "The festering wound closes."
- "Dust gets in your eyes: your blows go wide for {t} turns."
  "Your eyes clear."
- "{monster} squeals for help!" / "… squeals for help, and nothing answers."
- "You throw {thing} at {monster} for {n}." / "You throw {thing} at {monster} and miss."
  "There is nothing in reach to throw {thing} at." / "You carry nothing to throw."
- On the state line beside her health: "Webbed (2 turns left)", "Festering
  (poison, 2 turns left)", "Dusted (3 turns left)".
