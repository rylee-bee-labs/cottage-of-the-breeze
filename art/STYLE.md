# Cottage art — style and how we make it

Decisions are Rylee's; this file records them. The visual versions live on the
style board and the asset board (private artifacts); this is the durable copy.

## Decided (Rylee, 2026-10-01)

- **We make all the art ourselves** and credit ourselves: "Rylee and Claude".
- **Tiles are 96 px** (VEFR's tile size), **characters and items are 128 px**, transparent background.
- **Soft, darker-tone outlines**, never pure black.
- **The hero stays the same character** (the chibi archer with the red braids and green hooded cloak), **redrawn in the new style**. The current sprite is the reference for who she is, not for how she is drawn.
- **Colour:** dusk teal `#3F7E84` is the accent. The sampled palette (title picture) is on the style board.
- **The feeling:** "a fun, low bandwidth way to be able to be curious when I can't do anything but still want to do something" (BRIEF).

## Open

- Painted storybook, painted with soft outlines, or crisp pixel art: settled by looking at round 1
  (ground and wall in three treatments); the result is recorded here.
- Which hero proof to keep (round 3: the same hero redrawn in the chosen treatment).

## Never

- Anything copied from *Castle of the Winds* (art, names, text): we remake the systems, not the property.
- A different style per asset. A picture that doesn't match is redrawn.
- Rarity by colour alone (a glow, a word and a frame shape).

## How a picture gets made

1. **Proof with Codex** (ideas and proofs): the Codex CLI's built-in image generation, a few options per asset.
2. **Rylee picks.** Nothing is approved until she says so.
3. **Bulk with Wan 2.7 Image Pro**, using the approved proofs as style references (the 2026-09-30 bake-off found Wan Pro follows layout specs and keeps sprite frames most consistent).
4. **Process** to size and transparency; check it in the real build (weave and screenshot).
5. **Keep the record:** the original, the prompt and a credits line go in `art/source/`:

   `name.png · Rylee and Claude · tool: <which> · prompt: <the words> · <date> · status: draft | approved`

## Licensing note

Codex output is ours to use under OpenAI's terms as reported by third-party summaries (we could not read the terms page directly on 2026-10-01). Re-check the current terms before release and record the date here. Whether a purely AI-generated picture can be protected by copyright is unsettled; the parts Rylee describes, picks and finishes by hand are the strongest claim to authorship.
