#!/usr/bin/env bash
# Style test: the same six subjects in two looks, one Codex call each, in parallel.
#   A: our storybook painting, drawn with GBA-era RPG proportions.   B: true GBA pixel art in the storybook palette.
set -euo pipefail
W=~/scratch/style-test; rm -rf "$W"; mkdir -p "$W"
SP=~/code/Rylee-Bee/cottage-of-the-breeze/worlds/cottage-of-the-breeze/sprites
uv run --quiet --with pillow python - "$W/ref.png" "$SP/hero.png" "$SP/keeper.png" "$SP/trader.png" "$SP/gardener.png" <<'PY'
import sys
from PIL import Image
out, files = sys.argv[1], sys.argv[2:]
ims = [Image.open(f).convert("RGBA") for f in files]
h = 256
ims = [im.resize((round(im.width * h / im.height), h)) for im in ims]
sheet = Image.new("RGBA", (sum(i.width for i in ims) + 24 * (len(ims) + 1), h + 48), (0, 255, 0, 255))
x = 24
for im in ims:
    sheet.alpha_composite(im, (x, 24)); x += im.width + 24
sheet.convert("RGB").save(out)
print(out, sheet.size)
PY
STYLE="Hand-painted storybook game art, warm muted palette (umber, rust, amber, cream, soft moss green), soft painted edges, gentle dark warm-brown outline on objects and characters only, warm light from the top left, cozy and calm, no text, no harsh contrast, no photographic texture."
SUBJECTS="A game art kit sheet on a flat pure #00FF00 green background, a grid of 3 columns and 2 rows, each subject alone in its own cell with plenty of green around it and nothing touching the cell edges. Top row: (1) the hero, a young adventurer girl in a moss-green hooded cloak with a small satchel, standing facing the viewer, chibi proportions about 2.5 heads tall like a Game Boy Advance era RPG hero; (2) a small thatched storybook cottage in classic top-down RPG three-quarter view, the roof seen from above and the front wall with a round wooden door and two warm lit windows, a stone chimney; (3) a round leafy oak tree in top-down RPG three-quarter view, the trunk and its shadow at the bottom. Bottom row: (4) a round stone village well with a small wooden roof and a bucket, three-quarter view; (5) a square swatch of seamless meadow grass seen straight from above, filling a square in the middle of its cell, evenly lit; (6) a square swatch of a seamless packed-dirt village lane seen straight from above, filling a square in the middle of its cell, evenly lit. The figures match the reference characters' look."
( ~/.agents/bin/offload image --model codex --ref "$W/ref.png" --size 1536x1024 -n 1 --out "$W/A" --name style-a \
  "$SUBJECTS Style: $STYLE Proportions, silhouettes and the top-down three-quarter view of a Game Boy Advance era storybook RPG such as The Minish Cap, but painted, not pixelated." > "$W/A.log" 2>&1 ) &
( ~/.agents/bin/offload image --model codex --ref "$W/ref.png" --size 1536x1024 -n 1 --out "$W/B" --name style-b \
  "$SUBJECTS Style: true Game Boy Advance era pixel art like The Minish Cap and Mother 3: crisp hard-edged square pixels, every pixel visible, the hero about 32 pixels tall drawn large, a limited palette of about 16 colours per subject in warm storybook tones (umber, rust, amber, cream, soft moss green), 1-pixel dark warm-brown outlines, no anti-aliasing, no blur, no painterly brush texture, cozy and calm, no text." > "$W/B.log" 2>&1 ) &
wait
ls -la "$W"/A "$W"/B
tail -2 "$W/A.log" "$W/B.log"
