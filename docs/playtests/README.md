# Playtest and validation records

Plain-text records kept so a check can be repeated, and so what the engine
actually said is on the record rather than a paraphrase of it.

## `vefr-main-validation.txt`

The Cottage pack validated against VEFR `main` (not the older ref CI pins) on
2026-10-08. The file holds the exact command, the VEFR sha it ran against, and
the complete untrimmed stdout and stderr of the run. Both commands printed
`ok: ... geometry, reachability, voices all pass` and exited 0. The first `ok`
line is `norns validate`, the second is `vefr check`.

Notes on how it was run, so the record is honest about the environment:

- The machine had no VEFR checkout at `~/code/Rylee-Bee/vefr`, so one was cloned
  there (read-only: no commits, no branches, nothing pushed in VEFR) and pulled
  to `main` at `122b48066cc1ebd111d6d2e234e655901f3798a9`.
- `uv` was not installed either; it was installed into the user environment to
  run the command as written.
- The pack path passed to the commands is this worktree's
  `worlds/cottage-of-the-breeze`, per `AGENTS.md` — the `vefr/worlds/` symlink
  exists only in the primary checkout and is not used from a worktree.

No pack file was changed to make this pass.