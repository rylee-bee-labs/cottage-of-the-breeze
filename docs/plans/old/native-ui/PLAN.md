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

## UI4 checks and captures
- These live on their own branch, `ui4-proof`, not on the pack opt-in: the
  before/after screenshots and the browser harness that produced them are
  proof of the interface work, and the skin opt-in that hangs off it is a
  separate change with a separate review. The paths below are that branch's.
- `VEFR_WOVEN=/tmp/weave/cottage-after.html uv run --group test pytest tests/browser/test_cottage_containment.py` — check stage fit at seven view sizes.
- `VEFR_WOVEN=/tmp/weave/cottage-after.html uv run --group test pytest tests/browser/test_cottage_bot.py` — exercise the offline play view, menu, and message response.
- `uv run --group test python scripts/capture_ui4.py --before /tmp/weave/cottage-before.html --after /tmp/weave/cottage-after.html --out /tmp/ui4-shots` — capture play, two menu tabs, and reachable messages at desktop and phone sizes.
- The pin matters here and to the pack: `VEFR_REF` moved to `61490b0`
  (vefr #316, after #306), where a skinned panel's contrast-aware fallback is
  restored. Against `77d8f68` the menu labels and the HUD value boxes render
  at 1.14:1.

## Update 2026-10-04 (later): Rylee's picks
- She preferred the older painted/parchment look over the first Codex kit. From fifteen researched directions and an interface lab of eleven worlds she first liked **Scrapbook pages**, then decided against the tape: **back to parchment and soft wood** (the game's own look, rounder and quieter), with the **Ledger** type voice (**Crimson Pro**, a calm book serif). Her words: "Oh I don't like the tape. Back to parchment and soft wood. Let's say 'ledger' font?"
- Earlier type note, still true: "a little more 'cottage' and less stardew valley". Handwriting faces are for short labels only, never long reading. Alternates seen in the lab: Fraunces + Alegreya, Cormorant Garamond + Lora, IM Fell English + IM Fell DW Pica.
- Direction: parchment panels in gentle rounded wood, solid (not ridged) borders, soft shadows, real text; still inside one stage, no device frame. The lab (an artifact, state saved there) is where the rest is refined.
