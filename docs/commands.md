# Commands — Cottage of the Breeze

Reference detail moved out of `AGENTS.md` on 2026-10-09 so the router could stay
under its word budget. The rules stay in `AGENTS.md` verbatim: validate the pack
after every pack edit, edit the Blueprint rather than generated records, never
touch Rylee's written text, and record companion engine changes in VEFR.

## Check the pack (the gate)

The pack's check is VEFR's validator, run from the VEFR checkout:

```sh
# from a worktree with no ../vefr, cd ~/code/Rylee-Bee/vefr instead
cd ../vefr
VEFR_WORLD=cottage-of-the-breeze uv run norns validate --pack worlds/cottage-of-the-breeze
```

`vefr/worlds/cottage-of-the-breeze` is a local, gitignored symlink that exists
only in the primary VEFR checkout (`~/code/Rylee-Bee/vefr`) and points at the
**primary** cottage checkout. From a worktree, `../vefr` may be a VEFR worktree
without that symlink, or the wrong tree; pass this tree's pack path:

```sh
PACK="$(git rev-parse --show-toplevel)/worlds/cottage-of-the-breeze"
cd ~/code/Rylee-Bee/vefr && uv run norns validate --pack "$PACK"
```

A clean run prints `ok: geometry, reachability, voices all pass` for the tree you
edited. That string is what CI's validator step expects.

### What CI runs

`.github/workflows/validate-pack.yml` runs on every pull request (and on pushes
to `main`) against a **pinned** VEFR (`VEFR_REF`), which can lag current VEFR
`main`. It runs two steps:

1. `uvx --from "vefr @ git+https://github.com/rylee-bee-labs/vefr@${VEFR_REF}" norns validate --pack worlds/cottage-of-the-breeze`
2. `python3 tests/assert_chest_drops.py` — a drop id the item catalog does not
   name is discarded silently by the engine, so this assertion is a second gate
   over the same pack.

Run step 2 locally whenever you touch a drop; it needs no VEFR checkout:

```sh
python3 tests/assert_chest_drops.py
```

## Assert the pack's unapproved text is marked

`DEMO.md` tells players every name and line is a draft; cottage#159 made the
pack say the same, so `vefr check --release`'s draft list is the approval
queue. Stdlib-only, no VEFR checkout needed:

```sh
python3 tests/assert_draft_text.py
```

It fails if a book in `library/` loses `status: draft`, if anything writes a
status other than `draft` (only Rylee may approve text), or if a text-bearing
pack file exists that the inventory
[`docs/plans/release-1-0/DRAFT-TEXT.md`](plans/release-1-0/DRAFT-TEXT.md) does
not name. CI does not run it yet; `.github/workflows/` is read-only for agents.

## Assert the Key Warden's challenge comes before the ending note

The Act 1 Re-cut hung the warden's yield on the very note that ends the act;
the owner's order (2026-10-24) is the challenge first, then the note. This
checks that order in the pack's data. Stdlib-only, no VEFR checkout needed:

```sh
python3 tests/assert_warden_challenge.py
```

It fails if the challenge is the ending note, if the rule that ends the act
does not ask for the warden's flag, if the challenge is read off the warden's
floor, or if the gems the warden carries are not a real item with a real
sprite. The playthrough bot plays the order for real; this is the half of it
that runs without a browser.

## The art tools' own tests

The tools in `art/tools/` have unit tests in `art/tests/`. Run them when you
touch them:

```sh
uv run --offline --with pillow python -m unittest discover -s art/tests -t .
```

## Audit the pack's art and write image-agent briefs

Stdlib only, no VEFR checkout. `audit` fails when the pack names a picture it
does not have (the engine would draw a placeholder and validate clean). After
editing `art/manifest/slots.json`, regenerate the briefs; the art tests fail
when `art/requests/` is stale.

```sh
python3 art/tools/art_manifest.py audit
python3 art/tools/art_manifest.py wanted --loop 3
python3 art/tools/art_manifest.py brief --all
```

## Refresh the Blueprint

After editing `worlds/cottage-of-the-breeze/blueprint.json`, refresh and check
from a VEFR checkout that has `vefr normalize`:

```sh
PACK="$(git rev-parse --show-toplevel)/worlds/cottage-of-the-breeze"
cd ~/code/Rylee-Bee/vefr && uv run vefr normalize --pack "$PACK" --out "$PACK" && uv run vefr check --pack "$PACK"
```

A hand edit to a generated record makes `vefr check` (and CI) fail with the word
"stale". To leave the Blueprint, delete `blueprint.json` and
`blueprint.lock.json`; the records they generated already sit in the pack. Guide:
`vefr/docs/guides/blueprint.md` exists in the primary VEFR checkout
(`~/code/Rylee-Bee/vefr`); it is absent only from a bare worker worktree.

What the Blueprint owns on this tree is in
[`docs/repo-map.md`](repo-map.md#blueprint-generated-records).

## Publishing a playable build

`bin/publish-build.sh` weaves the pack into one HTML file and posts it to the
dev gallery. It weaves with the VEFR checkout at `~/code/Rylee-Bee/vefr` (or
`$VEFR_DIR`), so pull that first. Run it after a merge, so the build's sha is a
real commit.

Whether a build exists and what the gallery currently serves is **UNKNOWN** from
a plain clone: the script needs this machine's ssh key accepted by the gallery
host and the `gallery` CLI from `~/.agents/bin/`. `.project/CURRENT.md` asserts
no milestone build and no gallery URL for the same reason.

## Probes this repo cannot answer

Run from a clean clone or an agent sandbox, some of this file's claims are not
checkable — that is a fact about the environment, not about the pack:

- `uv` is not installed in every sandbox, so the art tests and the validator
  cannot be run there. A missing `uv` is not a failing test.
- The play bot's route and its report are `tests/playthrough/` (`README.md`
  there explains it); a claim about the game at play is that bot's or a player's,
  written down where it happened.

## Play the game headless (the playthrough bot)

From a VEFR checkout whose test venv has Playwright:

```sh
PACK="$(git rev-parse --show-toplevel)/worlds/cottage-of-the-breeze"
BOT="$(git rev-parse --show-toplevel)/tests/playthrough/run.py"
cd ~/code/Rylee-Bee/vefr
uv run --group test python "$BOT" --pack "$PACK" --viewport desktop
uv run --group test python "$BOT" --pack "$PACK" --viewport phone
```

Run it after any change to a map, a prop, a resident's place, a book or a rule.
CI does not run it.