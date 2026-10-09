# CURRENT — Cottage of the Breeze

This file is a **router, not a snapshot**.

Cottage of the Breeze is a VEFR game/world pack. Game content and canon live
here; reusable engine capability lives in VEFR.

## Stable orientation

- `BRIEF.md` describes the game/pitch.
- `DESIGN.md` describes the systems and experience.
- `STORY.md` is the canon surface; agent-authored playable text is not canon
  until Rylee accepts it.
- `NOTES.md` preserves dated decisions and playtest history.
- VEFR owns reusable engine behavior.

## Current truth

| Question | Source |
| --- | --- |
| code, branches, PRs, issues | Git + GitHub |
| current work / owner attention | Project Home + GitHub Issues |
| game identity and scope | `BRIEF.md` + `DESIGN.md` |
| canon | `STORY.md` |
| dated owner decisions / playtest history | `NOTES.md` |
| active build plans | `docs/plans/` + their owning issues |
| engine behavior / capability | current `Rylee-Bee/vefr` |
| published/runtime evidence | current build/runtime evidence, never this file |

## Resume

Run `lab enter` or `now-block --print .`, then inspect the issue/PR you are
actually working on. Read only the matching plan and the newest relevant owner
decision.

The previous Release-1 snapshot and dated NEXT/verification ledger remain in
Git history. Do not recreate a rolling build/status ledger here.

If runtime or deployment evidence is missing, say **UNKNOWN**.

## Latest activity

- **2026-10-08:** the soft-wood skin merged to `main` as cottage#107
  (see `NOTES.md` 2026-10-08 for the full entry); the cuts (`PROVENANCE.md` /
  `PROVENANCE.tsv`) and the built skin are on `main`.
- **2026-10-08:** town `[1,1]` has exactly one way down now — the generated
  Section descent (`cellar-0-1`). The hand-authored cellar (`floor-1`..
  `floor-6`, `king-room`) is gone, so the Keybearer ladder, the Cellar King,
  the sealed door and Act 1's ending are no longer in the pack; the generated
  descent has no keys or ending until E8 lands (see `NOTES.md` 2026-10-08,
  "one way down"). Verified with VEFR's play kit; log in
  `docs/playtests/2026-10-08-descent-104.md`.
