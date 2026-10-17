# AGENTS.md — Cottage of the Breeze

A private game pack for the VEFR engine (`../vefr/`), the studio's
first game: a learning remake of *Castle of the Winds*'s systems. This repo
owns the design kit and pack content, not engine code.
Read `README.md`, then `.project/CURRENT.md`. Canon is `docs/story/STORY.md`
(promoted 2026-10-09); it and the root `STORY.md` are Rylee's alone: read them,
never write them. Reference detail moved to
[`docs/repo-map.md`](docs/repo-map.md) (each path, its check, handoff) and
[`docs/commands.md`](docs/commands.md) (validate, refresh, publish).

## Owner-confirmed direction is not a draft

**Rylee's instruction (2026-10-14):** "If you and I work on something together in a chat and refine it it’s not a draft ok? It’s direction". A design or product decision refined with ChatGPT and explicitly selected/accepted by Rylee is **approved owner direction**. Treat it as the implementation brief, not as an unapproved idea for another review cycle. Do not re-ask settled questions, downgrade the decision to "proposed", or park it without a new owner decision. Track code, testing and release readiness separately: **agreed direction ≠ implemented ≠ verified ≠ shipped**.

This does **not** waive the existing protection for specific story/canon text, names, existing library words, art approval, license/publication or other explicit owner gates. New author-written content remains subject to those boundaries. **The 1.0 finish line is active:** [release roadmap](docs/plans/release-1-0/ROADMAP.md) and [release epic #170](https://github.com/rylee-bee-labs/cottage-of-the-breeze/issues/170). Favor the smallest polished implementation over growing scope.

### Approval carries across collaborators and handoffs

**Rylee's further clarification (2026-10-14):** "If we submit to Claude it’s still us collaborating ok? I’m jsut saying when we do stuff I still have to approve it like 3 more times and that’s silly".

ChatGPT, Claude, delegated coding agents, GitHub issues/PRs and Project Home are **continuations of one owner-directed collaboration**, not separate authorities that can demand a fresh sign-off on the same settled design choice. The original owner-approved decision and its scope **travel with the handoff**. A relay or mission should link the source decision and say **OWNER-APPROVED DIRECTION / IMPLEMENTATION AUTHORIZED WITHIN SCOPE**, not "unapproved draft" or "please approve again".

- Execute ordinary investigation, implementation, refactoring needed for the task, tests, docs and PR preparation within the approved scope without an additional human design approval. Technical reviewers validate **correctness and evidence**, not re-approve the concept.
- Follow existing repository review/merge and deployment permissions; do not invent extra owner approval checkpoints. Direction approval is not blanket authorization to bypass branch rules, ignore failed CI, publish the private game, alter protected canon, expose secrets, or take a newly consequential action without an existing grant.
- **Ask again only at a real boundary:** material scope change, contradiction between approved decisions, owner-protected canon/text/licensing, public release, irreversible/security-sensitive change, or an action not already delegated. Explain the changed boundary and ask for the **minimum single decision** needed. Group related choices, do not serially seek three confirmations.
- In a handoff, preserve: **decision/source**, **approved intent**, **scope/exclusions**, **autonomous work allowed**, **acceptance tests**, and **only unresolved owner gate (if any)**. Track statuses as Direction approved, Implementing, Verified, Released, not successive "awaiting approval" states for the same choice.

## The rules that matter

- **Rylee writes the stories.** Canon (`STORY.md`, the pack's `logbok.md`,
  names, characters, found books) is hers. Agents build machinery, suggest
  when asked, and never promote an idea into canon on their own.
- **Existing written content is preserved word for word** (Rylee, 2026-10-08:
  "Preserve existing written items unless I explicitly approve changes").
  The notes, letters and books in `library/`, sticker and item names, and resident
  lines that already exist keep their exact text. Move them, re-home them or give
  them a new place to be found, but do not reword them. A change to their wording
  needs her explicit approval, named in `NOTES.md`. This replaces her earlier
  "Anything may change" for these items.
- **Story drafts are drafts** (Rylee, 2026-10-08: "approved for further
  exploration, not canon. I alone approve changes to STORY.md"). Agents may draft
  the story in `docs/story/` (for example `DRAFT.md`, `DRAFT-v2.md`), marked draft,
  and new player-facing words stay draft until she approves them. A story-draft PR
  is opened as a draft and held for her, never auto-merged.
  Suggestions go in `NOTES.md`, marked as an agent's ("Claude's note:"); `BRIEF.md`'s ✍️ parts
  are hers alone.
- **Remake the systems, not the property.** *Castle of the Winds* is Rick
  Saada's: its name, art, text and monster/item/place names are not ours to
  ship. Mechanics are. Nothing from the original's files goes in this repo.
- **The engine stays neutral.** Game-specific names never go into
  `../vefr/`. New engine features go through VEFR's ruleset checklist
  (`../vefr/docs/guides/rulesets.md`, present in the primary VEFR checkout ~/code/Rylee-Bee/vefr; a bare worker worktree may have no ../vefr)
  and its ask-first rules.
- **The release is made in VEFR** (Rylee, NOTES 2026-09-26). Hand-made
  pictures and notes here are drafts and reference; the shipped game comes
  out of the studio (Folks room, studio modules, `ratatoskr weave`).
- **Every sitting ends with something alive:** a playable build, a book,
  a map, a note. Validate the pack after every pack edit (see Commands).
- Art: originals and their prompts go in `art/source/`.
- **Art we ship is art we made** (Rylee, 2026-10-02). We may distribute what we generate, and every piece is attributed (keep each `.credits.txt`). **Kenney is for prototyping only; never ship it.** **LimeZu** was bought to support the artist: use it only in a project Rylee names, with attribution. Neither is used in Cottage (the vendored Kenney sheets were removed 2026-10-02). If we need new sheets we generate them: Codex first, then Wan. Older "training: not cleared" or "not final art" notes in `art/` are stale for distribution (they are not rewritten; this rule wins).

## Commands

The pack's check is VEFR's validator, run from a VEFR checkout; run `art/tests`
when you touch `art/tools/`, and the playthrough bot (`tests/playthrough/`) when
you touch a map, a prop, a resident's place, a book or a rule. Commands and what CI runs:
[`docs/commands.md`](docs/commands.md).

## Generated records are the Blueprint's

`blueprint.json` is the source, `blueprint.lock.json` records what `vefr
normalize` wrote from it. Edit the Blueprint, never a generated record by hand.
To leave the Blueprint, delete both files; their records sit in the
pack. What is generated on this tree, and the refresh command:
[`docs/repo-map.md`](docs/repo-map.md), [`docs/commands.md`](docs/commands.md).

## Boundaries

- **VEFR** (`../vefr/`): engine changes this game needs are VEFR work — record
  them as companion changes, never by editing `../vefr/`.
- Estate art (`media_files/`) is committed from the estate root, not here.
  Estate rules: `~/.agents/AGENTS.md`; nothing here restates them.

## Needs Rylee's approval here

- Anything that becomes canon: story, names, characters, found books, endings.
- Changing the license (MPL-2.0 code + CC BY-SA 4.0 content, chosen 2026-10-17: see `LICENSE`, `LICENSE-CONTENT.md`) or the repo's visibility.
- Adding third-party content that is not CC0 or otherwise cleared.
- General gates (deploys, force-push, mass deletion): see the constitution.

## Done means

- The validator prints `ok: ... geometry, reachability, voices all pass`.
- The playthrough bot passes on desktop and phone, or each red check is a named
  open issue.
- Decisions Rylee made are recorded in `NOTES.md`, her words quoted.
- `.project/CURRENT.md` names the stage and the one next step accurately.

## Play-Nice pin and verification

The [adoption manifest](.project/contracts/adoption.yaml) pins the common behavioral floor and applicable contracts. Read the [shared floor](https://github.com/rylee-bee-labs/play-nice-contracts/blob/main/contracts/everyone/FLOOR.md) and applicable packs before consequential changes. [Freshness CI](.github/workflows/contract-freshness.yml) checks the pin, **not** source test, human acceptance or deployment. `playnice check .` requires a verified Play-Nice checkout and supplies separate evidence for any eventual badge; do not claim its result without running it. Repo-local permissions, game canon, security and release gates remain in force.
