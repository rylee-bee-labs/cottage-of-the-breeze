# Cottage of the Breeze: demo guide

A small town-and-dungeon game made inside VEFR by Rylee and Claude. It is one file that runs in any browser, offline, with no account and no key.

## Play it

Open the single HTML file (or the playable build in the gallery). Press **Begin**.

| Key | What it does |
| --- | --- |
| Arrow keys | Walk one tile at a time (bump into a monster to strike it) |
| **F** | Use what you stand on: a door, stairs, a chest, a note; also trade with the Trader |
| **E** | Talk to someone close by (two tiles) |
| **Q** | Whisper: a rumour from the world |
| **B** | Open your bag |
| **O** | Explore on its own (autoexplore) |
| **V** | Toggle the fog of war |
| Menu button | Journal, books, settings |

On a touch screen the buttons on screen do the same things.

## The loop

1. **The cottage.** Walk to the door at the bottom (one tile left of where you start) and press F.
2. **The town.** Talk to the people (the Dwarf Smith, the Fisher, the Gardener). The **Trader** buys and sells: press F beside them. There are notes and a letter to find.
3. **The tavern.** The Spell Keeper and the Tavern Regular are here; the Keeper has a story for you.
4. **The cellar.** Stairs in the town's top-left corner lead down three floors. The floors are dark (fog of war): a rat, a damp shade, a nest of moths and a rustle guard what they drop. A cloudy potion heals you (open the bag).
5. Come back up, sell what you found, and read what you picked up.

## What is rough (so you are not surprised)

- The hero hops one tile at a time and does not yet have walking frames (the pictures are drawn; the engine does not play them yet).
- The tavern, town and cottage use the new look; a few doors and stairs are still the engine's own tiles.
- There are no sounds, no equipment slots yet, and no "when this happens" reactions (the cat just sits by the rug).
- Talking works offline with the characters' own lines. If you connect a small model (see the VEFR guide), they speak fresh lines.
- Nothing is saved to a server. Your bag and journal live in this browser.

## Credits

- Game, writing, pictures: **Rylee and Claude**.
- The pictures were drawn with an AI image tool (Codex) from our own briefs and references, as proofs. **They are not cleared for training other models** (see each picture's credits line under `art/source/`).
- The engine's own studio tiles (doors, stairs and a few floors) are the VEFR project's, shared under CC BY-SA 4.0 (see the VEFR repository, `web/art/README.md`).
- Fonts: Cinzel and Atkinson Hyperlegible Next.
- Engine: **VEFR** (the game of making a game).
