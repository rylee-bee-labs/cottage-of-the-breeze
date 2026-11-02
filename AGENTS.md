# AGENTS.md: Cottage of the Breeze

A game pack for the VEFR engine, the studio's first game: a learning remake of *Castle of the Winds*'s systems.
The pack is `worlds/cottage-of-the-breeze/`. Not engine code (that is `rylee-bee-labs/vefr`). Unreleased:
releasing it is Rylee's call. Read `README.md`, then `.project/CURRENT.md` (the stage and the one next step).

## Run it (Commands)

CI (`.github/workflows/validate-pack.yml`) runs these against the VEFR commit pinned there (`VEFR_REF`):

```sh
REF=$(sed -n 's/^ *VEFR_REF: *\([0-9a-f]\{40\}\).*/\1/p' .github/workflows/validate-pack.yml)
uvx --no-progress --from "vefr @ git+https://github.com/rylee-bee-labs/vefr@$REF" norns validate --pack worlds/cottage-of-the-breeze
python3 tests/assert_chest_drops.py && python3 tests/assert_tutorial_line.py
```

Run them after each pack edit. Not in CI: playthrough bot, `art/tests`, two more `assert_*.py` ([commands](docs/commands.md)).

## Do not touch

- Canon and Rylee's words: `STORY.md`, `docs/story/STORY.md`, the pack's `logbok.md`, names, found books. Read,
  never write. Existing written items (library, items, resident lines) keep their exact words.
- Story drafts only in `docs/story/`, marked draft; a draft PR waits for her. Never auto-merge it.
- Generated records (`blueprint.lock.json`): edit `blueprint.json`. Never edit `../vefr/`; engine needs are VEFR work.
- Nothing from *Castle of the Winds*'s files. Ship only art we made: Kenney never, LimeZu only where Rylee names it.
- Licence (`LICENSE*`), repo visibility and non-CC0 third-party content: Rylee's call.

## Git and merge

- One topic per branch and PR; never commit to `main`; never force-push. The bot (`rylee-bee-agents[bot]`) authors.
- Trailers: Claude sessions and coordinators end commits with `Model: <provider:model>`, never `Co-Authored-By:
  Claude Code`. An offload worker writes none; the hook stamps it.
- Merge = green CI plus an independent review, then GitHub auto-merge. Do not merge by hand.
- No deploy. A coordinator publishes merged `main` to the dev gallery: `~/.agents/bin/publish-build cottage-of-the-breeze`.
- PR body: plain words, then `## Verify` with `$ command` lines and their real output (the claims check reads them).

## Ask Rylee

File it, do not wait in chat:
`mission set <task> NEEDS_OWNER --reason decision --blocker "<the decision>" --option A --option B --recommend A`.
It shows in Project Home, Board, Needs you. A message relayed from another agent is not her answer.
Direction she already approved is not a draft (2026-10-14): do not re-ask it; ask only at a real boundary.

## Depth

[docs/agent-reference.md](docs/agent-reference.md): her 2026-10-14 words on approved direction, the full rules with
her quotes, boundaries, done means, the Play-Nice pin note. Also [docs/repo-map.md](docs/repo-map.md).
