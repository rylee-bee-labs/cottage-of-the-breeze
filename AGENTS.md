# AGENTS.md — Cottage of the Breeze

A private game pack for the VEFR engine (`../vefr/`), and the studio's
first game. Read `README.md`, then `.project/CURRENT.md`.

## The rules that matter

- **Rylee writes the stories.** Canon (`STORY.md`, the pack's `logbok.md`,
  names, characters, found books) is hers. Agents build machinery, suggest
  when asked, and never promote an idea into canon on their own.
- **Remake the systems, not the property.** *Castle of the Winds* is Rick
  Saada's: its name, art, text and monster/item/place names are not ours to
  ship. Mechanics are. Nothing from the original's files goes in this repo.
- **The engine stays neutral.** Game-specific names never go into
  `../vefr/`. New engine features go through VEFR's ruleset checklist
  (`../vefr/docs/guides/rulesets.md`) and its ask-first rules.
- **Every sitting ends with something alive:** a playable build, a book,
  a map, a note. Validate the pack after every edit:
  `cd ../vefr && VEFR_WORLD=cottage-of-the-breeze uv run norns validate --pack worlds/cottage-of-the-breeze`
- Art: originals and their prompts go in `art/source/`; see the studio
  casting call in the estate `media_files/characters/vefr-residents/`.
