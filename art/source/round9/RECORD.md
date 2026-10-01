# Round 9: what was run (2026-10-01)

`status: draft` — Rylee picks; nothing here is approved by a machine.
`training: not cleared` — Codex output is game art only until its terms are read at the source (`art/STYLE.md`, Licensing note).

Round 9 was run by the orchestrator from one script of 21 batched calls (2 to 4 pictures each, 72 pictures in all), not from per-group briefs. The exact prompt, the
reference pictures, the tool and the date of every picture are in its `.credits.txt` beside it in `art/source/round9/<group>/`. That is the source of truth for how a picture was made.
(A foreman also drafted seven longer briefs; they described a different set of batches than the ones that ran, so they were not kept.)

## Groups and sizes

| Group | Folder | Pictures | Drawn at | Cut to |
| --- | --- | --- | --- | --- |
| Items from Rylee's sentences | `sentence-items/` | 15 | one object, 128 px | `ready-128px/` |
| Map objects | `map-objects/` | 10 | one object, 128 px | `ready-128px/` |
| Portraits | `portraits/` | 8 | head and shoulders, 256 px | `ready-256px/` |
| Menu and HUD icons, slot outlines, panel frame | `menu-icons/` | 14 | flat, 256 px | `ready-256px/` (icons only) |
| Hero poses | `hero-poses/` | 5 | 128 px | `ready-128px/` |
| Effects and weather | `effects/` | 6 | glows 128 px, overlays 288 px | `ready-128px/` (glows only) |
| Rune stones, spell icons, parchment page, blank tablet | `spellbook-runes/` | 14 | 128 px (page 288 px) | `ready-128px/` |

## The style words every batch used

Cozy painted storybook, soft cel shading, soft darker-brown outlines (never pure black), muted low-saturation earth tones, dusk teal `#3F7E84` accent, moss greens `#4F7870` and `#648B77`,
earth browns `#433A2A` and `#76633E`, a touch of lantern amber `#B79D51`, warm calm light, and **"plain flat light grey background (not white, not a checkerboard), no text, no border, no shadow"**.
Reference pictures came from the accepted rounds: the round 7 hero and item anchors, and the round 8 picked residents and spellbook pictures.

## Lessons from this round

- The "plain flat light grey, not a checkerboard" wording worked: no picture came back with a drawn checkerboard (round 8 had three).
- The overlays (fog, rain, dusk) came back with REAL transparency and feathered edges. The rain is too faint (strongest alpha about 120 of 255) and needs a second try.
- Pale line drawings with an empty middle (the slot outlines, the panel frame) trip the sprite checker's "light background left behind" check by design. They go through the UI skin tools (`design/ui-skin.md` in the vefr repo), not the sprite tools.
- Pictures in a batch come back in any order: identify each by looking (the rune stones especially) before you rely on a file name.

## After the batch

```sh
uv run --offline --with pillow art/tools/process_sprites.py IN.png OUT.png --size 128
uv run --offline --with pillow art/tools/check_sprites.py DIR --size 128
uv run --offline --with pillow art/tools/contact_sheet.py OUT.jpg DIR/*.png
```
