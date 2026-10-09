# Mock renders: drawings of the skin, NOT pictures of the game

Nothing in this folder is evidence that the skin looks right in play. Every
picture here was drawn by a tool from the skin's own files. The pictures that
*are* play evidence live one directory up, in `parchment-and-wood/`, and they
were taken by running the game:

| File | What it is |
| --- | --- |
| `mock-look-phone.png` | `mock_skin.py` drawing the assembled skin at 390x844 |
| `mock-look-desktop.png` | `mock_skin.py` drawing the assembled skin at 1280x800 |
| `preview.html` | the parts drawn one at a time in a browser |
| `preview-2026-10-01-round-10.png` | a screenshot of `preview.html`, dated, showing the round-10 art |

They are here because they are useful. A mock is a fast way to see the chrome
assembled - a nine-slice rim that thins out when a panel is wide, two tab chips
that stop being the same shape - without a browser, and it is how the
round-two `tab-selected` pick was first caught. What a mock cannot do is tell
you how the *player* places a part. It does not read VEFR, it does not know
that `.toasts` is 210 px wide and as tall as the messages make it, and it got
both the banner and the slot wrong in exactly the way the real game showed:
a picture it stretches over a box it has no shape for.

So: a mock is a rendering aid. `check_ui.py` decides whether a skin is legal,
and `look-*.png` in `../parchment-and-wood/` is what a player would see. See
`../README.md` for how each one was made.

Regenerate the mocks:

```sh
uv run --offline --with pillow art/tools/mock_skin.py \
    ../../worlds/cottage-of-the-breeze/skins/parchment-and-wood \
    mock-look-phone.png --size phone
```