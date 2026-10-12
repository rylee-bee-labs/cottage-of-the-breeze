#!/usr/bin/env bash
# The residents: one strip each, the old sprite for who they are and the new hero for how they are drawn.
set -euo pipefail
W=~/scratch/art/npc; mkdir -p "$W"
SP=~/code/Rylee-Bee/cottage-of-the-breeze/worlds/cottage-of-the-breeze/sprites
HERO=~/scratch/art/hero/down/hero-down.png
uv run --quiet --with pillow python - "$W" "$HERO" "$SP" <<'PY'
import sys
from PIL import Image
w, hero, sp = sys.argv[1], sys.argv[2], sys.argv[3]
strip = Image.open(hero).convert("RGB")
style = strip.crop((0, 0, strip.width // 6, strip.height))          # the hero's first frame
for name in ["gardener", "trader", "dwarf-smith", "fisher", "keeper", "tavern-regular", "cat"]:
    who = Image.open(f"{sp}/{name}.png").convert("RGBA")
    who.thumbnail((style.height, style.height))
    ref = Image.new("RGB", (who.width + style.width + 60, style.height), (0, 255, 0))
    ref.paste(who, (20, (style.height - who.height) // 2), who)
    ref.paste(style, (who.width + 40, 0))
    ref.save(f"{w}/ref-{name}.png")
PY
BASE="Game Boy Advance era pixel art sprite strip on a flat pure #00FF00 green background. The reference shows two figures: on the LEFT is WHO to draw (keep their look: build, age, clothes, colours, hair, beard, hat and props), on the RIGHT is HOW to draw (copy exactly that pixel-art style, outline, palette, proportions and size: a chibi figure about 2.5 heads tall). Draw exactly ONE ROW of six frames of the LEFT character in the RIGHT character's style, the same size as the right character in every frame, all six on one shared ground line, evenly spaced with green between them, nothing touching the image edges. Crisp hard-edged square pixels, limited warm storybook palette, 1-pixel dark warm-brown outline, no anti-aliasing, no ground shadow, no text."
FRAMES="Frames 1 and 2: standing idle facing the viewer; in frame 2 they breathe in (head and shoulders one pixel lower). Frames 3 and 4: talking, facing the viewer: mouth open and one hand raised in a small friendly gesture, then the other. Frame 5: standing idle seen from the side, facing RIGHT. Frame 6: standing idle seen from behind."
gen() { ~/.agents/bin/offload image --model codex --ref "$W/ref-$1.png" --size 1536x1024 -n 1 --out "$W/$1" --name "npc-$1" "$BASE $2 $FRAMES" > "$W/$1.log" 2>&1 || echo "FAILED $1"; }
gen gardener "The gardener, a kindly village woman who grows vegetables." &
gen trader "The trader who keeps the market stall." &
gen dwarf-smith "The dwarf blacksmith: short and broad, a big beard, a leather apron." &
wait
gen fisher "The old fisher with his rod." &
gen keeper "The Spell Keeper who runs the tavern bar, warm and motherly." &
gen tavern-regular "The tavern regular, a tired, friendly drinker." &
wait
~/.agents/bin/offload image --model codex --ref "$W/ref-cat.png" --size 1536x1024 -n 1 --out "$W/cat" --name npc-cat "Game Boy Advance era pixel art sprite strip on a flat pure #00FF00 green background. The reference shows two figures: on the LEFT is WHO to draw (this cat: keep its colours and markings), on the RIGHT is HOW to draw (copy exactly that pixel-art style, outline and palette). Draw exactly ONE ROW of six frames of the cat, small (about half the height of the right figure), all on one shared ground line, evenly spaced with green between them, nothing touching the image edges. Frames 1 and 2: sitting, facing the viewer, the tail curled; in frame 2 the tail tip flicks. Frames 3 and 4: sitting facing the viewer, mewing (mouth open), then blinking slowly. Frame 5: sitting seen from the side, facing RIGHT. Frame 6: sitting seen from behind. Crisp hard-edged square pixels, limited warm storybook palette, 1-pixel dark warm-brown outline, no anti-aliasing, no ground shadow, no text." > "$W/cat.log" 2>&1 || echo "FAILED cat"
ls "$W"/*/*.png
echo DONE
