# Release 1 build plan (overnight 2026-10-03/04)

Plan builder: Opus, 2026-10-03 ~23:00 CDT. Deadline 07:00. Coordinator integrates; foremen build on Bazzite.
Story text written tonight is an **agent draft** (not canon): it is listed in `NOTES.md` ("Claude's note:") and in the morning report.

## 0. Corrections to the brief (checked against the repos)

| Brief said | Reality (evidence) |
|---|---|
| VEFR main `99ecf2f` | **origin/main is `b5294ee`**, 15 commits ahead. The primary checkout `~/code/Rylee-Bee/vefr` is clean, on `main`, and **behind**. `bin/publish-build.sh` weaves from it. Run `git -C ~/code/Rylee-Bee/vefr pull --ff-only` first. |
| Equipment "proposed only" | **Built and playable**: A1 #244, A2 #247 (`VEFR_EQUIP_ENGINE`), A3 #249 (Bag "You" section), step 4 docs #251. Only step 5 (pack data) is left. The brass ring can become a `charm` today. Keys may not be worn. |
| Guardians named from court ranks | **Superseded 2026-10-03** (VEFR `DECISIONS.md`): the role word is **"the Keybearer"** (Diablo III Keywarden precedent). Each one gets a proper name and an epithet, and both are hers. Per-run weighted guardians are an approved *campaign*, not tonight's work. Its own note says the ladder "stays authored" until then. |
| "5 approved proofs" | 5 **sheets** (`guardians_v1..v5.png`, 1254 px), each showing all five creatures. Pick one sheet. The Seneschal is a robed **shade**, not a rat. Cellar King art: `art/source/round8/monsters-and-boss/cellar_king_v1.webp`. |
| `surface` is cozy "costume" | `surface` is `"combat"`. Cozy comes from the act's `floor` being absent (default `costume`). **The player has no stakes branch.** `HERO_HP <= 0` always calls `cozyDeath()` (`web/packaged.html` ~3119), so turning stakes on means building engine work first. |
| Cottage CI validates the pack | It validates against a **pinned VEFR `a916ce4`**, which is older than locks and equipment. Any new rule action fails CI until `VEFR_REF` is bumped. |
| — | `complete-act` as a rule action was approved with the act-2 plan (VEFR `.project/CURRENT.md`, 2026-10-02 night). It is **not** recorded in `DECISIONS.md` yet; record it there. |
| — | Item `value` makes an item sellable (`sellItem`). **A key with a `value` can be sold away, and that softlocks the game.** Keys get no value. |
| — | Sprite size already exists: `player.sprite_scale` (0.2–2) per sprite key. Big guardians need no engine change. |

## 1. Definition of "first complete release"

**Must ship** (a real start-to-end game):
1. **Lock ladder on floors 3→6.** The floor 3→4 stair, the 4→5 stair and the 5→6 stair each carry `requires {item}` plus `locked_text`. One Keybearer per floor (3, 4, 5) drops that floor's key. Every key has `keep: true` and no `value`.
2. **The Cellar King on floor 6.** He drops `the-cellar-seal`. A new sealed door on floor 6 needs the seal.
3. **The king room** (new region `king-room`). It holds one chest book with the lore note (draft) plus the treasure (draft item), and a way back to town.
4. **The ending.** Reading the note fires a rule: `complete-act` (new VEFR action), then `set act-1-complete`, then `say`. The end card offers **Keep exploring** and **Start over**.
5. **About/credits.** A library book in the cottage: who made the game, the tools, "made with VEFR", and a pointer to the art credits.
6. **Tutorial moment**, built from existing rules. A `starts` line plus `point-to` the cellar. An `enters floor-1` line that teaches fighting and Interact. A `picks-up` line on the first key. The floor-3 `locked_text` teaches the lock.
7. **Gates green in both repos**, with the full verification in §5.

**Cheap, ships if on time:** the brass ring as a `charm` (`mods {"atk":1}`). Cat, Regular and Smith reactions using existing `comes-near` rules (draft lines). Deep ground and wall tiles on floors 4–6.

**Deferred, and why:**
- **Album.** No frozen contract exists, CURRENT says to write the contract first, and the sticker names are hers.
- **Sound.** The engine has zero audio. It would be a new subsystem plus a pack-contract change, and VEFR's own finding on #144 says it must be designed first. Not possible responsibly tonight.
- **Stakes.** There is no engine mechanic yet, and she said "not yet".
- **Act advance / act 2.** ADR 0006 is unbuilt. Tonight `complete-act` shows the card and records the completion; it does not advance acts.
- **Per-run guardians and weighted descent.** An approved campaign, multi-slice.
- **The cottage's lit window.** `show` only drops an item at the hero's feet, so this needs a new surface.
- **Walking frames, the round-12 cast monsters, the mole and beetle proofs.** Cut-line material.

## 2. Capability gaps

| Need | Kind | Smallest design | Engine work? |
|---|---|---|---|
| Key-carrying guardian | pack data | Blueprint family `extends` an existing family; the instance has `properties.drops: ["<key>"]`; bigger via `sprite_scale` | **None** (enemy `drops` + `keep` + `requires` exist) |
| Locks 3→4, 4→5, 5→6, seal door | pack data | `requires {"item": …}` + `locked_text` on a transition | None (#229) |
| King room + way back | pack data | new region, a chest book with `drops`, a plain transition to town | None |
| **Ending / complete state** | **VEFR rule action** | `{"complete-act": "<act id>"}`, value is a declared act id. The pure engine accepts and passes it through (`validAction`). `performRuleAction` opens an end card **on the existing overlay surface** (title = act title + world title; one neutral line; **Keep exploring**, which Interact continues per checklist item 6; **Start over**, the existing action). Fires once per save under `saves.rules: persist`. `window.VEFR_ACT_COMPLETE` is a harness snapshot (precedent: `VEFR_COMBAT`). No advance. | **Yes, V1** |
| "Can this pack be finished?" | VEFR authoring check | In `vefr check` (not `norns validate`, so no contract change): a fixpoint over regions from `start`. A lock opens once its key is obtainable in a reached region (enemy `drops`, chest-book `drops`, shop stock, or any rule `give`/`set`). It reports unreachable regions behind a lock, keys that can never be found, and **a lock key that has a `value` (it can be sold)**. New module `src/vefr/locks.py`, hooked in by one line. | **Yes, V2** (cut-able) |
| Synonym watch | — | `bosses` stays inert (do not revive it). There is no `guardians` block: the authored ladder makes it unnecessary, and the block is an ask-first contract change. Do not add an `ending` field: ending prose = the note book + `say`. The `act-completes` event from ADR 0006 is not needed; the action covers it. | — |

V1 follows `docs/guides/rulesets.md`. Touch points: `maplab.RULE_ACTION_KEYS` plus a value check against act ids, `cli.py` (action shape check near line 1445), the engine `validAction` (~3485), `performRuleAction` (~2150), `docs/guides/rules.md` ("twelve actions"), the glossary, a `docs/features.json` entry (drift check), and ROADMAP. Neutral fixtures only: VEFR is public.

## 3. Workstreams (mission tasks)

Tests are written first, committed and frozen (`--runxfail`). One brief per slice. Foremen run as `nice -n 10 offload foreman -m foreman --repo ~/worktrees/<name> --plan <brief> --budget 8 --minutes M --accept "<cmd>"` (MiniMax M3.1, per the 2026-10-03 decision). **At most 2 foremen at once.**

| id | repo | owner | deps | box | acceptance | off/keep |
|---|---|---|---|---|---|---|
| W0 setup | both | coordinator | — | 23:00–23:20 | `git -C vefr log -1` = `b5294ee`; worktrees `vefr-complete-act`, `vefr-locks-check`, `cottage-release-1` on Bazzite | keep |
| W1 art pick | cottage | coordinator | — | 23:20–23:40 | picks recorded in `art/source/round11/PICKS.md` (sheet, keys, door, chest) | keep (judgment) |
| V1-T tests | vefr | coordinator | W0 | 23:20–00:10 | `tests/test_complete_act.py` + `tests/fixtures/make_act_end_pack.py` + `act_end_harness.mjs`; PR merged | keep |
| V1 build | vefr | foreman A | V1-T | 00:10–02:40 | `bash tests/run.sh tests/test_complete_act.py tests/test_rules_engine.py tests/test_rules_validator.py tests/test_overlay_interact.py --runxfail` | offload |
| V2-T tests | vefr | coordinator | W0 | 00:10–00:40 | `tests/test_lock_reachability.py` (solvable pack passes; key behind its own lock fails; unobtainable key fails; sellable key fails; pack with no `requires` unchanged) | keep |
| V2 build | vefr | foreman B | V2-T | 00:40–02:40 | `bash tests/run.sh tests/test_lock_reachability.py tests/test_locked_stairs.py --runxfail` | offload |
| C1 art cut | cottage | worker on Bazzite (`offload agent`) | W1 | 23:40–01:15 | `art/tools/process_sprites.py` outputs land in `sprites/` (3 Keybearers + King at 256 px, 4 key icons + seal at 128 px, sealed-door and chest tiles); each output keeps a `.credits.txt`; `art/tests` pass; `art/tools/mock_room.py` contact sheet reviewed by the coordinator | offload + keep review |
| C2 briefs tests (#63) | cottage | cheap worker | — | 23:40–00:30 | drop the stale `training: not cleared` assertion; bring `guardians.md`, `gaps.md` and `cellar-cast.md` to the brief shape; `uv run --offline --with pillow python -m unittest discover -s art/tests -t .` gives 0 failures (19 today) | offload |
| C3 ladder | cottage | coordinator | W1 | 23:40–01:30 | Blueprint families `keybearer-moth` (extends `nest-of-moths`, floor 3), `keybearer-mushroom` (extends `rustle`, floor 4), `keybearer-shade` (extends `hollow-shade`, floor 5), `cellar-king` (extends `cellar-rat`, floor 6). Each is placed in the room farthest from that floor's arrival stair (BFS via `maplab.reach`). First-guess stats: 16/2/20, 22/3/30, 28/3/40, 40/4/80. Display names are descriptive, e.g. "the Keybearer, a great pale moth" (no proper names). `normalize && vefr check && norns validate` print ok | keep |
| C4 king room | cottage | coordinator | C3 | 01:30–03:00 | `acts/act-1/king-room/{map.md,contract.json,tiles}`; sealed door in `floor-6/map.md` (comment that delve output was hand-edited); transitions; `library/<note>.md` (chest, drops treasure); rules; `vefr probe --fire "defeats:what=<king id>" --fire "reads:what=<note>"` shows the chain | keep (story drafts) |
| C5 tutorial, about, reactions | cottage | coordinator | — | 02:00–03:00 | ≤ 12 rules in total (cap 40); validator ok; draft lines listed in NOTES | keep |
| C6 pin + repro (#75) | cottage | coordinator | V1 merged | 03:00–03:20 | `VEFR_REF` set to merged VEFR main; CI green; the build records the VEFR sha | keep |
| C7 playthrough bot | cottage `tests/playthrough/` | foreman or worker on Bazzite | C3 (data shape) | 00:30–03:00 | `cd ~/code/Rylee-Bee/vefr && uv run --group test python <cottage>/tests/playthrough/run.py --html build.html --viewport desktop,phone` writes `report.json`. Reads map/hero/enemies **only from test-side window globals** (`VEFR_COMBAT`); presses keys only | offload |
| C8 polish | cottage | worker | C1 | 03:00–04:30 | deep tiles in `floor-4..6/tiles`, ring `slot`; validator ok | offload, cut-able |
| R review | both | coordinator (+ Opus call 2) | V1, V2 | 02:40–03:30 | diff read by hand; stray `PLAN.md` removed; full VEFR gate | keep |
| D docs | both | coordinator | all | 05:30–06:40 | CURRENT (both repos), NOTES, DEMO, `docs/plans/release-1/HANDOFF.md`, VEFR `DECISIONS.md` (`complete-act`), issues #63, #64, #75, #77 updated, morning report | keep |

**VM rule:** the full VEFR suite (~150 s) and the Playwright runs never overlap, and neither runs while a foreman runs locally. Foremen run on Bazzite.

## 4. Critical path and timeline

**Critical path:** V1-T → V1 build → review → VEFR merge → C6 pin bump → C4 `complete-act` rule → full playthrough → Cottage merge → `bin/publish-build.sh`.

- **00:10** V1 and V2 tests merged, both foremen running. C1, C2 and C7 dispatched.
- **T+2h (01:00)** ladder data validates with placeholder sprites. Art cut reviewed.
- **T+4h (03:00)** V1 and V2 reviewed, PRs green, merged. Pin bumped. King room authored.
- **T+5.5h (04:30)** first full bot playthrough on desktop and phone. The bug loop starts.
- **06:00 freeze.** No features after this; only fixes for failing gates.
- **06:00–06:40** merge, publish, docs, report. 06:40–07:00 is buffer.

**Cut-lines:**
- V1 not green by **03:30**: ship the ending without the card (the note sets `act-1-complete`, `say`, `point-to` the way home). The game is still complete. Leave the V1 PR open.
- V2 not done by 03:30: drop it and rely on the bot.
- C1 late: use the existing family sprites at a larger `sprite_scale`.
- C8, the ring and reactions are first to go.
- **Never cut:** locks + keys + King + king room + way back + about + clean gates.

## 5. Verification

1. **Static.**
   - VEFR: `uv sync --group test && uv run --group test ruff check src tests scripts && uv run --group test pytest -q && python3 scripts/check_public_surface.py && uv run norns validate --pack worlds/sample-world`.
   - Cottage: `norns validate`, `vefr normalize … && vefr check` (now including the lock-reachability check), the `art/tests` unittest, and pinned CI green.
2. **Rule chain.** `vefr probe` fires `defeats` (each Keybearer, then the King), `picks-up` (each key), `reads` (the note). The why-log must show each rule once.
3. **Look.** `vefr look --pack <pack> --steps …` for a screenshot per region. The new art must sit on the tile grid at a sensible scale next to ordinary mobs.
4. **Bot playthrough** (C7, real Chromium, keyboard only):
   - Fresh profile. Begin, and the tutorial line appears.
   - Walk town → floor 3. Try the locked stair: `locked_text` appears and the region is unchanged.
   - Defeat Keybearer 1, take the key, the stair opens. Repeat on floors 4 and 5.
   - King → seal → sealed door → note → end card. Interact closes it. Walk home.
   - **Reload** once after the first key (key in bag, guardian still dead, flags kept) and once after the end (card not shown again, flag set).
   - **Start over** clears keys and respawns the guardians.
   - Run at 1280×800 and at 390×844 (the phone pass taps the Interact button).
   - Fail on any `console.error` or `pageerror`, any interaction that does nothing, or a stuck overlay.
5. **Residue.** grep the woven HTML and the pack for `debugger`, `console.log(`, `TODO`, `FIXME`, `agent draft`, `localhost`. Drafts are marked in NOTES, never on screen.
6. **Accessibility.** The V1 tests run axe on the end card. Spot-check contrast on the new door and chest tiles with `vefr look`.
7. **Human pass.** The coordinator watches one recorded bot run end to end before the merge.

## 6. Risks

- **The `gh pr merge` classifier may deny merges.** Then the Cottage pin points at the pushed V1 PR head SHA, and the build is woven from a VEFR worktree, not via `publish-build.sh`. Say so in the morning report.
- **Foreman failure or OOM.** Each has a time box. If V1 has no green slice by 01:45, the coordinator takes it over: it is small, about four seams.
- **Softlock.** Mitigated by keys without value, the V2 check, and the bot.
- **Hand-edited delve output** (`floor-6/map.md`). A future `vefr delve` rerun overwrites it. Note this in the map file and NOTES.
- **Existing saves.** New enemies change signatures, so the floors repopulate. Acceptable; note it.
- **Canon.** Every line written tonight is a draft. Nothing goes in `STORY.md`.

## 7. Questions only Rylee can answer (morning, non-blocking)

1. **The draft ending** (the King's last line, the king-room note, the treasure, the Keeper after the ending): keep it, rewrite it, or bin it? *Recommendation:* keep it as a placeholder until she writes her own. It is data, so swapping it in takes minutes.
2. **The three Keybearers' proper names and epithets, and their keys' names.** They ship as descriptive placeholders. *Recommendation:* she names them from the art; agent proposals go in NOTES only if she asks.
