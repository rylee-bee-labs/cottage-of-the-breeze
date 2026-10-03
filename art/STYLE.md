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

## MiniMax prompt recipe (draft, tested 2026-10-02; Rylee reviews every picture)

An experiment, not a decision: Codex (proofs) and Wan (bulk) stay in the pipeline below, and nothing generated in the test is in this repo. This records what worked, so a future MiniMax call (`offload image`, or the MCP `text_to_image` tool) starts from it. Same seed, 1:1, one image per call.

**What worked for items, equipment and potions** (put the subject first, then this paragraph, every time):

> Hand-painted 2D digital illustration in the style of a stylized fantasy mobile-game item icon. A bold, uniform dark chocolate-brown outline of consistent medium thickness runs around the whole silhouette and every major inner shape. Cell-shaded painterly colour built from chunky mid-tone patches, simple blocky highlights and darker saturated shadow shapes, with one warm light from the upper left; visible dry-brush streaks on metal and leather, flat opaque fills on enamel and cloth. Warm palette of honey gold, deep amber, ochre, chestnut and russet leather, mossy green cloth and cream, with deep muted teal accents. Exaggerated chunky rounded shapes with simple, readable detail. The subject sits alone in the centre of the frame on one flat mid-teal background colour (hex 3F7E84), the background as plain and flat as a colour swatch.

**Creatures and characters: Rylee's preference (2026-10-02):** "I think I prefer the codex character designs. I enjoy the storybook and the cuter concepts for the mobs vs realism" and "I did rather enjoy the v6 guard style though. That was pretty cute!" So **cute storybook mobs are the goal, not naturalistic animals**, and **Codex stays the first choice for characters and creatures** (the hero and the cast). MiniMax is for items and equipment, and for cute-mob drafts when wanted. Two ways to steer a creature in MiniMax, both tested:
- **Cute and characterful** (what she liked: a large scarred old rat guardian in a little jacket and scarf, with a fierce face): use the item paragraph below, then describe a creature with personality ("a huge, old, grizzled rat on all four paws, powerful shoulders, a fierce face", "chibi", "friendly"). MiniMax adds clothes and accessories on its own; keep them if you like them. That is a lever, not a defect.
- **Plain animal** (only if a design calls for it): "the monster sprite of a giant cellar rat from a classic fantasy RPG bestiary, a fluffy tawny rodent on all four paws, three-quarter view" or "a real wild brown rat seen as an ordinary animal, bare tawny fur". This removes the clothes and makes the animal naturalistic.

**Lessons (each cost a round):**
- **The words are the lever; a reference image is not.** MiniMax's image-to-image (`--ref`) keeps the subject and the colours but not the style: every reference test came back as a photoreal 3D render.
- **Describe the style the way a vision model sees your art.** MiniMax's own image understanding called our art "cell-shaded, chunky mid-tone patches, blocky highlights, dry-brush streaks, a bold uniform dark-brown outline, a flat mid-teal field, a stylized fantasy mobile-game prop icon". Using those words beat my guesses ("smooth soft gradients" was wrong). Re-run that pass on new approved art before writing prompts.
- **Say only what you want.** Naming a thing you do not want draws it: "no clothes" gave the rat a coat, "nobody wearing it" put a boy in the hood. Write "an empty garment laid flat" and "an ordinary animal" instead.
- **"Sticker" is taken literally:** a white die-cut border and a drop shadow. Say "alone on a flat colour swatch".
- **"Chibi", "friendly" and "game" humanise animals** (scarves, jackets, a coat). That is how to get the cute mobs Rylee prefers; leave those words out, or say "classic RPG monster sprite", only when a plain animal is wanted.
- A faint floor shadow often survives; it cuts out easily. Teal hex codes are only roughly followed: expect a lighter teal and match it when cutting out.

Record each kept picture the usual way (original, prompt, credits line, `tool: MiniMax image-01`), and keep the `.json` that `offload image` writes beside it.

## How a picture gets made

1. **Proof with Codex** (ideas and proofs): the Codex CLI's built-in image generation, a few options per asset.
2. **Rylee picks.** Nothing is approved until she says so.
3. **Bulk with Wan 2.7 Image Pro**, using the approved proofs as style references (the 2026-09-30 bake-off found Wan Pro follows layout specs and keeps sprite frames most consistent).
4. **Process** to size and transparency; check it in the real build (weave and screenshot).
5. **Keep the record:** the original, the prompt and a credits line go in `art/source/`:

   `name.png · Rylee and Claude · tool: <which> · prompt: <the words> · <date> · status: draft | approved`

## Licensing note

Codex output is ours to use under OpenAI's terms as reported by third-party summaries (we could not read the terms page directly on 2026-10-01). Re-check the current terms before release and record the date here. Whether a purely AI-generated picture can be protected by copyright is unsettled; the parts Rylee describes, picks and finishes by hand are the strongest claim to authorship.
