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

## Decided in the art rounds (Rylee, 2026-10-01)

- **Painted storybook with soft darker-brown outlines** (round 1), in **muted earth tones** drawn with big shapes sized for a 96 px tile (round 2). Round 2 "sets the look".
- **Several variant tiles per surface** (3 recommended) to break repetition; the engine picks one deterministically per tile (see `../vefr/design/pack-art-proposal.md`).
- **The hero is the same character** (red braids, green hooded cloak, bow); round 3 shows her redrawn as a four-view turnaround and a four-frame walk cycle. Frames still need cutting out and aligning before the engine can use them.
- **A rug is one object, not a repeating tile.**

## Open

- Which hero variation to keep (round 3, v1 or v2), and the first walk-cycle direction to finish (right is drawn; left, up and down are in the turnaround).
- How many frames per walk (4 now) and the hop feel (see the engine proposal).
- Monsters (a cellar rat, shades and moths, a rustle) and the remaining items: not started.

## This file is a style kit

See `README.md`, "Swappable by design": the look, the anchors and the shared words belong to this game only; another game gets its own kit.

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
