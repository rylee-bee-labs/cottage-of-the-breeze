# UI6 interface slices 4 and 5: the tests, rescued

## What happened

These tests were written, verified and committed in the worktree
`/var/home/rylee/worktrees/offload/vefr-ui6-foreman-ui6-brief-20261004-151816-5443-ui6-tests-20261004-154915-0761`
as commit `555c3fbb35e8e369d2cb6b7cbc109dfef3bd1790`
("test(skin): remaining parts, HUD icons, speech portrait (fails today)").

About a minute after that commit, the vefr primary checkout
(`/var/home/rylee/code/Rylee-Bee/vefr`) and every vefr worktree under
`/var/home/rylee/worktrees/offload/` were deleted from disk by another process on
this machine (a `docs/orchestration/simplify/` handoff appeared in
`/var/home/rylee/code/Rylee-Bee/` at 16:07-16:08 the same minute). No copy of
the git object store survives anywhere on the machine, so the commit is gone.
This directory is the work, preserved so it can be reapplied.

## How to reapply

    python3 patch_tests.py /path/to/a/vefr/checkout
    bash tests/run.sh tests/test_skin_apply.py tests/test_skin_validator.py

`patch_tests.py` copies the two fixture files verbatim and makes the same
surgical edits to the two test files. Every edit asserts its anchor first, so a
checkout that has drifted fails loudly rather than half-applying.

- `tests/fixtures/skin_apply_harness.mjs` - final content (was rewritten)
- `tests/fixtures/make_skin_pack.py` - final content (nine-part fixture skin added)
- `blocks/skin_apply_append.py` - the block appended to `tests/test_skin_apply.py`
- `blocks/skin_validator_append.py` - the block appended to `tests/test_skin_validator.py`

## What was verified, before the deletion

`bash tests/run.sh tests/test_skin_apply.py tests/test_skin_validator.py`
-> **17 failed, 61 passed, 1 skipped**

Every failure is a new test saying the feature does not exist yet:

    FAILED tests/test_skin_apply.py::test_the_slot_paints_the_equipment_rows
    FAILED tests/test_skin_apply.py::test_the_tab_paints_the_menu_tabs
    FAILED tests/test_skin_apply.py::test_the_toggle_paints_the_phase_rail_and_the_fog_switch
    FAILED tests/test_skin_apply.py::test_the_tooltip_paints_the_tool_buttons_that_carry_a_title
    FAILED tests/test_skin_apply.py::test_the_speech_part_paints_the_speech_box_like_a_panel
    FAILED tests/test_skin_apply.py::test_the_divider_paints_the_rule_under_the_game_head
    FAILED tests/test_skin_apply.py::test_the_banner_paints_the_messages_and_leaves_the_map_alone
    FAILED tests/test_skin_apply.py::test_the_corner_paints_the_four_studs
    FAILED tests/test_skin_apply.py::test_the_gold_plate_paints_the_gold_controls
    FAILED tests/test_skin_apply.py::test_every_new_part_rule_sits_inside_the_media_guard
    FAILED tests/test_skin_apply.py::test_no_new_part_rule_invents_a_colour
    FAILED tests/test_skin_apply.py::test_no_new_part_rule_shrinks_a_target_below_44px
    FAILED tests/test_skin_apply.py::test_the_new_parts_leave_the_focus_ring_and_the_motion_alone
    FAILED tests/test_skin_apply.py::test_a_skinned_page_draws_one_icon_beside_each_hud_word
    FAILED tests/test_skin_apply.py::test_every_icon_is_decoration_painted_in_the_words_own_ink
    FAILED tests/test_skin_apply.py::test_a_speaker_with_a_picture_gets_a_decorative_portrait
    FAILED tests/test_skin_validator.py::test_every_part_the_validator_accepts_is_a_part_the_player_draws

Still green in the same run, and in the other three required runs:

    bash tests/run.sh tests/test_skin_kit.py tests/test_skin_docs.py tests/test_player_build.py
    -> 67 passed, 5 skipped
    bash tests/run.sh tests/test_combat_loop.py tests/test_light.py tests/test_web_packaged.py tests/test_teal_contrast.py
    -> 45 passed
    uv run python scripts/build_player.py --check
    -> ok: web/packaged.html is exactly its 6908 lines of parts
    (also: tests/test_overlay_interact.py tests/test_interact_play.py
     tests/test_quiet_ui.py tests/test_web_dom.py -> 33 passed)

## The contract is satisfiable

Before committing, all 25 new tests in `test_skin_apply.py` and the one new
failing test in `test_skin_validator.py` were run against a throwaway prototype
of the feature (written in /tmp, never in `web/`): a script that appended one
rule per part inside the media guard, inserted the five SVGs beside their HUD
lines, and wrapped `showSpeech` to add a portrait when `VEFR_SPRITES` has one.
**All 26 passed.** Three deliberate violations were then injected
(`height: 30px` on a control, `color: #B0B0B0` on a part rule, `outline: none`
plus a `transition`) and the three rules-that-never-bend tests each failed, so
those pins bite. The prototype is not part of this bundle; it was scaffolding.
