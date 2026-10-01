# Round 9 proofs (2026-10-01): nothing picked yet

Codex proofs in 21 batched calls (`training: not cleared`; see each `.credits.txt`). Not final art. Rylee has not picked from this round yet.
Ready-to-use cuts (128 px, or 256 px for portraits and menu icons) are in each group's `ready-*px/` folder; all pass `check_sprites.py`.

## What is here
- `sentence-items/`: teacup, Spooncalibur, apple, cheese, torch, key, gold coins, rope, three gems (red square, teal oval, amber hexagon), four map fragments (four quarters of one chart).
- `map-objects/`: stairs down and up, signpost, fence, tree, berry bush, mossy rock, pond, hidden bookshelf panel, lantern post.
- `portraits/`: head and shoulders of the seven residents and the hero (256 px).
- `menu-icons/`: satchel, journal, books, compass, whisper, heart, coin, map scroll, five empty slot outlines (hand, body, head, feet, charm), a panel frame.
- `hero-poses/`: idle, attack, hurt, cheer, sleeping in bed.
- `effects/`: strike spark, heal sparkle, pickup glint, fog, rain, dusk tint.
- `spellbook-runes/`: eight rune stones, four spell icons, a parchment page, a blank rune tablet.

## Notes from review
- **The rain overlay is too faint** (its strongest alpha is about 120 of 255); it needs a second try with stronger streaks.
- The fog and dusk overlays have real transparency and feather to the edges: they are full-frame washes, not tiles.
- The slot outlines and the panel frame are pale line drawings with an empty middle; `check_sprites.py` flags them as "a light background left behind" by design. Use the UI skin tools (`design/ui-skin.md` in the vefr repo) for them.
- Pictures in a batch come back in any order: the rune stones' order (light, water, fire, wind, earth, growth, memory, rest) should be identified by looking before use; the file names do not follow the request order.
