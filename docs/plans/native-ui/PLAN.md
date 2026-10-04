# A native, in-world interface (direction from Rylee, 2026-10-04)

## What she said
- Everything running inside the game should be in the game's themed UI; only real controls live outside it. Today HUD icons and buttons float over the page background beside the map.
- It should feel like a game that could run on a small handheld (a fixed, tidy layout), **but with no literal device frame**: it should be native to the VEFR world, "like a part of the world", not "a square mechanical UI overlaid on a warm soft game".
- Cute, minimal, warm.

## Design rules (proposed from that)
1. **One screen.** The play area keeps a fixed shape and scales to fit the window; HUD, messages, buttons and menus are drawn inside it. The page around it is only a quiet backdrop (the dusk-teal of the title picture). Nothing sits on the page.
2. **Painted, not boxed.** HUD pieces are small painted objects (a heart, a coin, a star, a leaf ribbon, a hanging wooden tag), soft-edged and slightly irregular, with the same dark-brown outline as the art. No hard rectangles, no flat bars with square ends.
3. **Controls are objects in the world.** On a phone the d-pad is four little stones or a clover; action buttons are round pebble tokens; Menu and Bag are a satchel and a book. On desktop the same objects show as small key hints.
4. **Speech is a bubble with a tail** from the speaker, with the portrait beside it, not a rectangle at the bottom.
5. **Menus are pages.** The menu opens as paper on the screen (parchment, ribbon tabs, slots as little pockets).
6. **Rules that never bend:** all words are real text; 4.5:1 contrast; 44 px targets (the painted object can be smaller than its hit area); a visible focus ring; reduced motion respected; a high-contrast mode drops the decoration.

## Art needed (Codex, original; round 17)
HUD: heart (full, half, empty), coin plate, experience star, a leaf ribbon behind the numbers, a hanging name tag. Controls: four d-pad stones, two round pebble buttons, a satchel and a book token, a speech bubble with tail. Existing and reusable: menu icons (satchel, journal, books, compass, whisper, heart, coin, map scroll), slot outlines, portraits, effects (`art/source/round9`), the skin pieces (`round10/ui`).

## Engine work (VEFR, tests first; after a mock is approved)
Skin parts for `hud` icons, `controls`, `bubble`; apply the unused skin parts (slot, tab, toggle, tooltip, divider, banner); a fixed-aspect stage that scales to the window with everything inside; portraits in the speech bubble; strike, heal and pickup flashes. Then the `packaged.html` split.

## Order
1. Mock on real art (this branch: art kit, artifact for Rylee). 2. Rylee picks the look. 3. Tests, then foremen. 4. Bot checks for fit at seven sizes (the measurement script in the handoff) and axe.
