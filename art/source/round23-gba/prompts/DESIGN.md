# Cottage of the Breeze: GBA art set

Every run in this project reads this file. It is the style contract (copied from the game's `art/STYLE.md`,
decided by Rylee on 2026-10-12). Consistency comes from this file and the reference images, not from the model.

## The look

- True Game Boy Advance era pixel art in a warm storybook palette, like *The Minish Cap* and *Mother 3*.
- Crisp hard-edged square pixels, every pixel visible, no anti-aliasing, no blur, no gradients.
- 1-pixel dark warm-brown outlines on objects and creatures (never pure black).
- Limited warm palette: umber, rust, amber, cream, soft moss green; dusk teal `#3F7E84` as the accent.
- Light from the top left. No ground shadows (the engine adds none and they cut out badly).
- Classic top-down RPG view: floors seen from above; furniture, walls and buildings face the viewer squarely
  (front face straight down the screen). NEVER isometric, never at an angle.
- Creatures are cute storybook mobs, not naturalistic animals (Rylee 2026-10-02: "I enjoy the storybook and the
  cuter concepts for the mobs vs realism").

## The scale

- A tile is 32 x 32 art pixels. People are 48 px tall in 64 x 64 frames. Objects are drawn at their own size.
- The pipeline downscales each generated picture to this grid with nearest-neighbour and locks it to one
  64-colour palette, so draw big, chunky, readable shapes that survive that.

## References (in `reference/`)

- `style-b.png`: the approved style test. This is HOW everything is drawn.
- `hero-down.png`: the hero. Sets the size and outline of a person.
- `town-props.png`, `town-houses.png`: the shipped town kit. New kits must sit beside these.

## How a sheet is generated

- Always generate with the image tool, passing `reference/style-b.png` (and the closest shipped sheet) as
  reference images.
- One sheet per kit: subjects in a clear grid, each alone on a flat pure `#00FF00` green background, plenty of
  green around each one, nothing touching the image edges or another subject.
- Tile textures instead fill their whole cell edge to edge, evenly lit, so they repeat without seams.
- No text, letters or numbers anywhere. No religious symbols.
- Never anything from *Castle of the Winds* (art, names, text).
- Save every sheet into `sheets/` with a short kebab-case name, and write the exact prompt used beside it as
  `sheets/<name>.prompt.txt`.

## Lessons that cost a round

- Say "front face straight down the screen, NOT isometric" or furniture comes back at an angle.
- Name only what you want: naming a thing you do not want draws it.
- Grids of 12 or more merge when cut by shape; keep clear green gutters so each cell cuts cleanly.
- A "cuter" redraw can come back more realistic: compare against the reference before keeping it.

## Saving the images (OpenDesign runs)

The image tool's result carries no image data back to the run. Each picture still lands on disk in
`~/.codex/generated_images/<session>/exec-*.png`: after each call, copy the newest file there into `sheets/`.
