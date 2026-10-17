# cottage-of-the-breeze backlog

This is the tracking document for work that was open as GitHub issues in this repository and was closed as not planned on 2026-10-07, so that the open-issue queue could reach zero.
The issue bodies themselves were not edited; every summary below is ours, written from those bodies.
To restart an item, reopen the linked issue or open a new one and delete its row from here.
It was built by one rule: every issue that was open on 2026-10-07 in this repository is listed below, newest first, with nothing added and nothing left out.

### #98 — Pilot VEFR Player Driver/session replay against the existing Cottage playthrough

- Issue: https://github.com/Rylee-Bee/cottage-of-the-breeze/issues/98
- Opened: 2026-10-06 · Labels: none
- Status on 2026-10-07: closed as not planned on 2026-10-07 — tracked here

Cottage is meant to be the first proving game for the VEFR Player Driver work that Rylee and Sol designed together on 2026-10-06: the session capsule, the action tape and checkpoint digests. It is blocked until the VEFR implementation slices exist, so nothing in this repository can move first. The issue argues the existing keyboard-only bot is an excellent migration target, because it already plays the real woven game through ordinary keys. It exposed the 1,651-keypress deep-state setup cost, it writes a report, and it catches real progression and balance problems. It also reads several ad-hoc VEFR globals and owns pack-specific route machinery, which is exactly the kind of coupling the Driver work would replace. The acceptance criteria are: record one real Cottage route as a logical action tape, capture its starting and current session capsules, replay it in a fresh browser context and match the VEFR checkpoint digests, then pause mid-replay and continue with ordinary keyboard control. No engine machinery would be added to this repo; the point is to prove the design without putting it here.

Next step, when this is picked up: Wait for the VEFR P1-P3 slices to exist, then record one real Cottage route as a logical action tape.

### #91 — Rework: Act 1 as 8-11 floors with a key warden; King moves to end of Act 3

- Issue: https://github.com/Rylee-Bee/cottage-of-the-breeze/issues/91
- Opened: 2026-10-04 · Labels: none
- Status on 2026-10-07: closed as not planned on 2026-10-07 — tracked here

This records a design decision Rylee made on 2026-10-04 rather than a code task. Act 1 is to be rebuilt as 8-11 floors with a key warden, keeping only the first floor map, the throne-room map and a few hand-drawn room shapes. The Cellar King stops being the Act 1 boss and becomes the Act 3 boss, placed before endless mode. The engine plan lives in the VEFR repository at `docs/plans/endless-dungeon/PLAN.md`, so the work is blocked on the VEFR epic. It is also coupled to the town rework: the changes it makes are to Act 1 only, and Acts 2-3 change the town per issue #87.

Next step, when this is picked up: Read the VEFR endless-dungeon plan and confirm Rylee still wants Act 1 at 8-11 floors with a key warden.

### #88 — Names: the three Keybearers, their keys, and every agent-draft line (Rylee)

- Issue: https://github.com/Rylee-Bee/cottage-of-the-breeze/issues/88
- Opened: 2026-10-04 · Labels: none
- Status on 2026-10-07: closed as not planned on 2026-10-07 — tracked here

All story text and names written during Release 1 are agent drafts, and `NOTES.md` lists them. The list covers the King's-room note, the gems, the Keeper and Regular lines that follow the ending, the tutorial and key lines, the About book, sticker names, gear names, and the Keybearers' plain descriptions. Rylee is asked to keep, rewrite or bin each one; these are data and can be swapped in minutes, so nothing here is structural. The issue notes that VEFR will gain a draft/approved status, recorded as discovery finding 1. Until Rylee rules on them, every one of these lines stays an agent draft rather than canon.

Next step, when this is picked up: Rylee goes through the `NOTES.md` list line by line and marks each keep, rewrite or bin.

Acts 2-3 deliberately deferred (owner decision 2026-10-15); reopen on go.

### #86 — Epic: the in-world interface (Cottage side): soft-wood skin art, Ledger type, opt-in

- Issue: https://github.com/Rylee-Bee/cottage-of-the-breeze/issues/86
- Opened: 2026-10-04 · Labels: none
- Status on 2026-10-07: closed as not planned on 2026-10-07 — tracked here

The direction and the rules for this live in `docs/plans/native-ui/PLAN.md`; the engine-side slices are tracked in the VEFR epic for the in-world interface. On the Cottage side the work is to identify and build the soft-wood skin from the art pieces under `art/source/round18/ui-soft/`, 22 Codex drawings made on 2026-10-04 that Rylee has not reviewed yet. There is a hard ordering constraint: embed nothing new until the engine's skin "fonts" part exists. After that the order is to opt Cottage in, then re-run the bot, the fit check and the axe. The skin type follows the Ledger direction recorded with issue #84.

Next step, when this is picked up: Have Rylee review the 22 unreviewed pieces in `art/source/round18/ui-soft/`.

### #85 — credits: 41 tracked credits files hold /tmp paths (privacy); clean them and fix codex_batch.sh

- Issue: https://github.com/Rylee-Bee/cottage-of-the-breeze/issues/85
- Opened: 2026-10-04 · Labels: none
- Status on 2026-10-07: closed as not planned on 2026-10-07 — tracked here

The credits files for art rounds 11 through 13 carry absolute paths from the generator, and some of them name a session scratch folder. That is a privacy problem rather than a tidiness one. The fix has three parts: clean the existing files to repo-relative references, fix `art/tools/codex_batch.sh` so it writes repo-relative references in future, and add `art/tests/test_credits_clean.py` to keep it that way. The plan is slice A0 of the VEFR tighten-shapes plan, and the art ledger in slice A1 will forbid absolute paths permanently.

Next step, when this is picked up: Rewrite the round 11-13 credits files with repo-relative paths and fix the generator that wrote them.

### #76 — Make draft, playable, canon, and release-ready story status explicit

- Issue: https://github.com/Rylee-Bee/cottage-of-the-breeze/issues/76
- Opened: 2026-10-03 · Labels: none
- Status on 2026-10-07: closed as not planned on 2026-10-07 — tracked here

Cottage deliberately uses playable drafts while Rylee decides what becomes canon, and that workflow works, but the status currently lives mostly in prose scattered across `STORY.md`, `NOTES.md`, `.project/CURRENT.md` and the agent guidance. The live dev pack already contains story and dialogue that is playable while parts of it are still described as agent drafts, and `STORY.md` separately says canon is Rylee's words only. The issue asks to keep the four states distinct rather than merge them: draft, approved, playable, canon, release-ready. The missing piece is a reliable release boundary. The goal is to keep development builds permissive while making it hard to mistake known draft text for release or canon material. Acceptance: define the smallest authoritative place to record story-content status, preserve the rule that agents cannot promote content to canon, and let development builds stay permissive.

Next step, when this is picked up: Decide the smallest authoritative place to record story-content status across `STORY.md`, `NOTES.md` and `.project/CURRENT.md`.

### #74 — Clarify the CC0 scaffold boundary in the pack-local license

- Issue: https://github.com/Rylee-Bee/cottage-of-the-breeze/issues/74
- Opened: 2026-10-03 · Labels: none
- Status on 2026-10-07: closed as not planned on 2026-10-07 — tracked here

The repo-level `LICENSE.md` says only the inherited Emberfield scaffold remains CC0, but `worlds/cottage-of-the-breeze/LICENSE` still describes broad path categories such as `world.json`, contracts, voices, lore, and any prose or JSON, as CC0. Those paths now also contain substantial Cottage-authored material, so the two files no longer describe the boundary with the same precision. The issue is careful to call this a license and provenance ambiguity, not a claim about the legal status of any existing file, and the work should be done before any public release. Acceptance: identify which remaining material is actually inherited from Emberfield, replace path-wide wording that could be read as covering later Cottage work, keep the original CC0 notice where it genuinely applies, and make the repo-level and pack-level statements consistent. **Resolved 2026-10-17:** the pack `LICENSE` now points to CC BY-SA 4.0 (`LICENSE-CONTENT.md`), with the CC0 fragments excepted.

Next step, when this is picked up: List which files under `worlds/cottage-of-the-breeze/` are genuinely inherited Emberfield scaffold.

### #66 — Containerfile unverified

- Issue: https://github.com/Rylee-Bee/cottage-of-the-breeze/issues/66
- Opened: 2026-10-02 · Labels: none
- Status on 2026-10-07: closed as not planned on 2026-10-07 — tracked here

The issue is a one-line flag that the Containerfile has never been built or run. It is marked UNVERIFIED rather than claimed to work, so nothing about it has been proven. There is no Containerfile in the current tree, so the file it referred to is not present here today. Nothing in the game or the release depends on it. The point is only to record the gap honestly so nobody later assumes the container path was tested.

Next step, when this is picked up: Either build the Containerfile once and record the result, or drop it as no longer relevant.
