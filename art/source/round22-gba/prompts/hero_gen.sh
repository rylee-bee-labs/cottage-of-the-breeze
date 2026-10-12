#!/usr/bin/env bash
# The hero's frames: six Codex strips (three walks, three action sets), three at a time.
set -euo pipefail
W=~/scratch/art/hero; mkdir -p "$W"
REF=~/scratch/art/ref-hero.png
cp ~/scratch/style-test/b-hero.png "$REF" 2>/dev/null || true
BASE="Game Boy Advance era pixel art sprite strip on a flat pure #00FF00 green background: exactly ONE ROW of six frames of the SAME character as the reference image (the girl in the moss-green hooded cloak with a brown satchel). Same proportions, same colours and the same size in every frame; all six stand on one shared ground line, evenly spaced, with green between them and nothing touching the image edges. Crisp hard-edged square pixels, every pixel visible, a limited warm storybook palette (umber, rust, amber, cream, soft moss green), a 1-pixel dark warm-brown outline, no anti-aliasing, no blur, no ground shadow, no text, no frame numbers."
gen() {  # name prompt
  ~/.agents/bin/offload image --model codex --ref "$REF" --size 1536x1024 -n 1 --out "$W/$1" --name "hero-$1" "$BASE $2" > "$W/$1.log" 2>&1 || echo "FAILED $1"
}
gen down "Front view, facing the viewer. Frames 1 and 2: standing idle; in frame 2 she breathes in (head and shoulders one pixel lower, the cloak settles). Frames 3 to 6: a walk cycle toward the viewer: right foot forward, passing (feet together, body one pixel higher), left foot forward, passing." &
gen up "Back view, seen from behind as she walks away: the back of the hood, the cloak and the satchel strap. Frames 1 and 2: standing idle; in frame 2 she breathes in (shoulders one pixel lower). Frames 3 to 6: a walk cycle away from the viewer: right foot forward, passing, left foot forward, passing." &
gen right "Side view, profile facing RIGHT. Frames 1 and 2: standing idle; in frame 2 she breathes in (shoulders one pixel lower). Frames 3 to 6: a walk cycle to the right: front foot forward, passing, other foot forward, passing; the cloak swings a little." &
wait
gen act-down "Front view, facing the viewer. Frame 1: ACT, she bends and reaches forward with both hands to pick something up. Frame 2: ACT, she holds a small glowing found thing up in both hands, pleased. Frames 3 to 5: ATTACK with a short wooden walking stick: wind-up with the stick raised over her right shoulder, mid-swing, follow-through low in front. Frame 6: HURT, she flinches back, eyes squeezed shut." &
gen act-up "Back view, seen from behind. Frame 1: ACT, reaching forward with both hands (as if opening a door or picking something up). Frame 2: ACT, holding a small glowing found thing up above her head. Frames 3 to 5: ATTACK away from the viewer with a short wooden walking stick: wind-up over the shoulder, mid-swing, follow-through. Frame 6: HURT, flinching, shoulders up." &
gen act-right "Side view, profile facing RIGHT. Frame 1: ACT, reaching forward with both hands to pick something up. Frame 2: ACT, holding a small glowing found thing up in front of her, pleased. Frames 3 to 5: ATTACK to the right with a short wooden walking stick: wind-up raised behind her, mid-swing, follow-through forward. Frame 6: HURT, flinching back to the left, eyes shut." &
wait
ls "$W"/*/
grep -l FAILED "$W"/*.log 2>/dev/null || true
echo DONE
