

# ===========================================================================
# interface slice 4: the parts a skin may carry and the loader ignores today
#
# `maplab.SKIN_PARTS` accepts all nine and `cli._baked_skin` bakes their picture
# keys as data URIs; what is missing is that applySkin() writes no CSS for them.
# The `parts` page of the harness is a skin carrying every part: the four the
# player draws today plus these nine. The `skinned` page carries only the four,
# and is the negative control.
# ===========================================================================

def _rules(css):
    """(selector, body) for every rule inside the guard, a multi-line selector
    list kept whole and the guard's own block not mistaken for a rule."""
    text = css
    if GUARD in css:
        open_at = css.index("{", css.index(GUARD))
        text = css[open_at + 1:css.rindex("}")]
    return re.findall(r"([^{}]+)\{([^{}]*)\}", text)


def _guard_span(css):
    """The (first, last) offsets of the guard's own block."""
    open_at = css.index("{", css.index(GUARD))
    depth = 0
    for i in range(open_at, len(css)):
        if css[i] == "{":
            depth += 1
        elif css[i] == "}":
            depth -= 1
            if depth == 0:
                return open_at + 1, i
    return open_at + 1, len(css)


def _pictures():
    """Every one of the nine parts' pictures: (part, picture key, data URI).
    `slice` is a number, not a picture, so only the named files are listed."""
    return [(part, key, mk.picture_uri(fname))
            for part, spec in mk.PARTS_SKIN.items() for key, fname in spec.items()
            if isinstance(fname, str)]


def _drawn(css, part, key, *selector_groups, idiom=("border-image", "background")):
    """The rules that paint this part's own picture, onto the element the
    selector names, in one of the idioms the existing panel/button/bar rules use.

    Each group is the set of acceptable spellings for one thing the selector has
    to say (`".npc-box"` or `"#npc-box"`); every group has to match at least one.
    """
    uri = mk.picture_uri(mk.PARTS_SKIN[part][key])
    return [(sel, body) for sel, body in _rules(css)
            if uri in body
            and any(word in body for word in idiom)
            and all(any(spelling in sel for spelling in group) for group in selector_groups)]


def _need(hits, what):
    assert hits, f"the loader writes no rule that paints {what}"


# What each part paints, as the selectors the player already uses for it. A
# rule that names one of these is a rule about that part, whether or not it
# carries a picture, so the rules-that-never-bend tests below can see it.
PART_ELEMENTS = {
    "slot": (".equip-row",),
    "tab": ("#menu .pm button",),
    "toggle": (".phase-rail", "#fog-toggle"),
    "tooltip": (".gbtn--tool[title]",),
    "speech": (".npc-box", "#npc-box"),
    "divider": ("header.game-head",),
    "banner": (".toasts",),
    "corner": ("::before", "::after"),
    "gold-plate": (".cta--gold", ".gbtn--gold", "button.primary"),
}


def _new_rules(css):
    """Every rule that draws one of the nine parts' pictures."""
    uris = [uri for _part, _key, uri in _pictures()]
    return [(sel, body) for sel, body in _rules(css) if any(uri in body for uri in uris)]


def _part_rules(css):
    """Every rule that is about one of the nine parts: it names the part's
    element, or it carries the part's picture."""
    uris = [uri for _part, _key, uri in _pictures()]
    elements = [e for spellings in PART_ELEMENTS.values() for e in spellings]
    return [(sel, body) for sel, body in _rules(css)
            if any(uri in body for uri in uris) or any(e in sel for e in elements)]


def test_the_fixture_skin_carries_exactly_the_nine_parts(ran):
    """The `parts` page is the skin the rest of this section reads: the four the
    player already drew, plus the nine of interface slice 4. A part added or
    dropped here changes what every test below is about."""
    assert tuple(mk.PARTS_SKIN) == NEW_PARTS, tuple(mk.PARTS_SKIN)
    assert set(mk.ALL_SKIN["parts"]) == set(mk.SKIN["parts"]) | set(NEW_PARTS)
    assert "has-skin" in ran["parts"]["bodyClass"]


def test_the_slot_paints_the_equipment_rows(ran):
    """`slot` is a worn thing's row in the Bag panel: the plain file on the row,
    `hover` under the pointer, `selected` on the row that is worn - the one
    carrying the Take off control."""
    css = ran["parts"]["css"]
    _need(_drawn(css, "slot", "file", (".equip-row",)), "the slot picture on .equip-row")
    _need(_drawn(css, "slot", "hover", (".equip-row",), (":hover",)),
          "the slot hover picture on .equip-row:hover")
    _need(_drawn(css, "slot", "selected", (".equip-row",), ('[data-action="takeoff"]',)),
          "the slot selected picture on the worn row (the one with Take off)")


def test_the_tab_paints_the_menu_tabs(ran):
    """`tab` is a menu tab: the plain file, and `selected` on the tab that is
    the current one."""
    css = ran["parts"]["css"]
    _need(_drawn(css, "tab", "file", ("#menu .pm button",)), "the tab picture")
    _need(_drawn(css, "tab", "selected", ("#menu .pm button",), ('[aria-current="true"]',)),
          "the tab selected picture on the current tab")


def test_the_toggle_paints_the_phase_rail_and_the_fog_switch(ran):
    """`toggle` is the phase rail and the fog switch: `off` is how a switch
    rests, `on` is the state it is pressed into."""
    css = ran["parts"]["css"]
    for element in (".phase-rail button", "#fog-toggle"):
        _need(_drawn(css, "toggle", "off", (element,)), f"the toggle-off picture on {element}")
        _need(_drawn(css, "toggle", "on", (element,), ('[aria-pressed="true"]',)),
              f"the toggle-on picture on {element}[aria-pressed=true]")


def test_the_tooltip_paints_the_tool_buttons_that_carry_a_title(ran):
    """`tooltip` is the small tool buttons' tooltip, on hover and on keyboard
    focus, so the keyboard sees what the pointer sees."""
    css = ran["parts"]["css"]
    _need(_drawn(css, "tooltip", "file", (".gbtn--tool[title]",), (":hover",)),
          "the tooltip picture on .gbtn--tool[title]:hover")
    _need(_drawn(css, "tooltip", "file", (".gbtn--tool[title]",), (":focus-visible",)),
          "the tooltip picture on .gbtn--tool[title]:focus-visible")


def test_the_speech_part_paints_the_speech_box_like_a_panel(ran):
    """`speech` is a nine-slice like `panel`, and the words inside it keep the
    skin's ink rather than taking a colour of their own."""
    css = ran["parts"]["css"]
    _need(_drawn(css, "speech", "file", (".npc-box", "#npc-box"), idiom=("border-image",)),
          "the speech picture as a nine-slice on the speech box")
    ink = mk.ALL_SKIN["ink"]["on_panel"]
    assert any(ink in body for sel, body in _rules(css)
               if (".npc-box" in sel or "#npc-box" in sel) and "color:" in body), (
        "the words inside the speech box must keep the skin's declared ink")


def test_the_divider_paints_the_rule_under_the_game_head(ran):
    """`divider` is the rule under the game head: its bottom edge, by border
    image or by a bottom border picture."""
    css = ran["parts"]["css"]
    _need(_drawn(css, "divider", "file", ("header.game-head",),
                 idiom=("border-image", "border-bottom")),
          "the divider picture on header.game-head's bottom edge")


def test_the_banner_paints_the_messages_and_leaves_the_map_alone(ran):
    """`banner` is the message panel. It is a picture behind the messages; it
    must not repaint the map canvas or the HUD frame that sit on the map."""
    css = ran["parts"]["css"]
    _need(_drawn(css, "banner", "file", (".toasts",), idiom=("background",)),
          "the banner picture behind the messages")
    assert "#town-canvas" not in css
    assert ".hud-frame" not in css and "#hud-frame" not in css


def test_the_corner_paints_the_four_studs(ran):
    """`corner` replaces the flat accent dot on the four corner studs with the
    corner picture - all four of them, so no panel keeps a plain dot."""
    css = ran["parts"]["css"]
    for stud in (".carved::before", ".carved::after", "#config::before", "#config::after"):
        _need(_drawn(css, "corner", "file", (stud,)), f"the corner picture on {stud}")


def test_the_gold_plate_paints_the_gold_controls(ran):
    """`gold-plate` is a plate behind the words on a gold control. The words
    stay real text on top of it, so the picture may not be a picture of words."""
    css = ran["parts"]["css"]
    for control in (".cta--gold", ".gbtn--gold", ".stage button.primary"):
        _need(_drawn(css, "gold-plate", "file", (control,)), f"the gold plate on {control}")
    assert "content: url(" not in css


def test_every_new_part_rule_sits_inside_the_media_guard(ran):
    """prefers-contrast: more and forced colours return the plain flat style, so
    every painted rule is inside the one guard - and the guard is still the
    first thing in the sheet, before it but after any @font-face."""
    css = ran["parts"]["css"]
    assert GUARD in css
    lo, hi = _guard_span(css)
    for part, _key, uri in _pictures():
        assert uri in css, f"the {part} picture is never drawn at all"
        assert lo <= css.index(uri) < hi, f"the {part} rule is outside the media guard"
    before = css[:css.index(GUARD)].strip()
    assert before == "" or before.startswith("@font-face"), before


def test_a_part_the_skin_does_not_carry_is_left_alone(ran):
    """The negative half, which is the half that is easy to get wrong. The
    `skinned` page carries only panel, button, bar and cursor, so none of these
    nine pictures may appear anywhere in its CSS and none of the elements they
    paint may be named at all. Every picture is its own solid colour, so "the
    rule is absent" is a plain string test."""
    css = ran["skinned"]["css"]
    for part, key, uri in _pictures():
        assert uri not in css, (
            f"the default skin carries no {part} picture, yet a rule draws it ({key})")
    for element in (".equip-row", "header.game-head", ".toasts", ".phase-rail",
                    "#fog-toggle", ".cta--gold", ".gbtn--gold", ".gbtn--tool[title]",
                    "::before", "::after"):
        assert element not in css, f"a skin without the matching part writes a {element} rule"
    assert _new_rules(css) == []


def test_no_new_part_rule_invents_a_colour(ran):
    """Every colour on a skinned surface is the skin's declared ink or a colour
    the player already has. The loader must not invent one for the tab, the
    toggle, the slot, the tooltip, the speech box, the divider, the banner, the
    corner or the gold plate."""
    css = ran["parts"]["css"]
    assert _new_rules(css), "the loader draws no rule for any of the nine parts"
    allowed = {c.lower() for c in re.findall(r"#[0-9A-Fa-f]{3,8}\b", PLAYER_CSS)}
    allowed |= {c.lower() for c in mk.ALL_SKIN["ink"].values()}
    # Not colours: references to a colour the player or the skin already sets.
    borrows = {"currentcolor", "inherit", "transparent", "unset", "initial"}
    offenders = []
    for sel, body in _part_rules(css):
        for value in re.findall(r"(?<![-\w])color:\s*([^;}]+)", body):
            value = value.replace("!important", "").strip().lower()
            if value.startswith("var(") or value in borrows:
                continue
            hexes = re.findall(r"#[0-9a-f]{3,8}\b", value)
            if not hexes or any(h not in allowed for h in hexes):
                offenders.append(f"{sel.strip()} -> color: {value}")
    assert not offenders, "a skin part may not bring its own text colour:\n  " + \
        "\n  ".join(offenders)


def test_no_new_part_rule_shrinks_a_target_below_44px(ran):
    """The picture can be smaller than its hit area; the hit area may not be
    smaller than 44 px."""
    css = ran["parts"]["css"]
    assert _new_rules(css), "the loader draws no rule for any of the nine parts"
    for sel, body in _part_rules(css):
        if not any(word in sel for word in CONTROLS):
            continue
        for prop, value in re.findall(
                r"(?<![-\w])(min-height|min-width|height|width)\s*:\s*([0-9.]+)px", body):
            assert float(value) >= 44, (
                f"{sel.strip()} sets {prop}: {value}px, under the 44 px target floor")


def test_the_new_parts_leave_the_focus_ring_and_the_motion_alone(ran):
    """A skin may add a decoration and never take the focus ring away, and it
    adds no motion of its own: the player's reduced-motion blanket already
    covers everything."""
    css = ran["parts"]["css"]
    assert _new_rules(css), "the loader draws no rule for any of the nine parts"
    assert "outline: none" not in css.replace(" :", ":")
    for sel, body in _part_rules(css):
        assert "transition" not in body and "animation" not in body, (
            f"{sel.strip()} adds motion of its own")
    assert "@media (prefers-reduced-motion: reduce)" in PLAYER_CSS


# ---- the contrast floor, measured on the colours the loader actually uses ----

def _button_face(css):
    """The (text colour, background colour) of the player's button face."""
    for sel, body in _rules(css):
        if sel.strip() == ".gbtn, .cta, .verb-row button" and "color:" in body:
            ink = re.search(r"color:\s*(#[0-9A-Fa-f]{6})\s*!important", body)
            base = re.search(r"background-color:\s*(#[0-9A-Fa-f]{6})\s*!important", body)
            if ink and base:
                return ink.group(1), base.group(1)
    raise AssertionError("the skin sheet writes no button face")


@pytest.mark.parametrize("page", ["skinned", "parts"])
def test_the_skins_ink_clears_four_and_a_half_on_the_panel_ground(ran, page):
    """`ink.on_panel` against the flat ground the loader falls back to under a
    panel - the colour that is there when the picture's middle cannot be read."""
    css = ran[page]["css"]
    ink = mk.ALL_SKIN["ink"]["on_panel"]
    ground = re.search(r"var\(--vefr-skin-ground,\s*(#[0-9A-Fa-f]{6})\)", css)
    assert ground, f"the {page} skin writes no panel ground"
    got = contrast(ink, ground.group(1))
    assert got >= 4.5, (
        f"{page}: ink {ink} on the panel ground {ground.group(1)} is {got:.2f}:1")


@pytest.mark.parametrize("page", ["skinned", "parts"])
def test_the_button_ink_clears_four_and_a_half_on_the_buttons_own_base(ran, page):
    """The words on a skin button, against the base the loader puts under the
    picture (so the words survive a checker that cannot see the picture)."""
    css = ran[page]["css"]
    ink, base = _button_face(css)
    got = contrast(ink, base)
    assert got >= 4.5, f"{page}: button ink {ink} on {base} is {got:.2f}:1"


# ===========================================================================
# interface slice 5: the HUD icons and the speech portrait
# ===========================================================================

def test_a_skinned_page_draws_one_icon_beside_each_hud_word(ran):
    """Five small inline SVGs in currentColor, one for each HUD line. They sit
    BESIDE the line, in the same HUD block, and never inside it - so a line
    that is hidden today (this world neither grows nor trades) still has its
    icon, and the words do not move when the line appears."""
    icons = ran["parts"]["icons"]
    for name in ICONS:
        icon = icons[name]
        assert icon["count"] == 1, (
            f"expected exactly one svg[data-icon=\"{name}\"], found {icon['count']}")
        assert icon["beside"] is True, f"the {name} icon is not beside its HUD line"
        assert icon["inside"] is False, f"the {name} icon is a child of its HUD line"
        assert icon["viewBox"], f"the {name} icon has no viewBox"
        assert icon["shapes"] >= 1, f"the {name} icon draws nothing"


def test_every_icon_is_decoration_painted_in_the_words_own_ink(ran):
    """An icon adds nothing a screen reader needs to hear, and it is painted in
    currentColor so it follows the words it sits beside (the house style for
    `.gbtn--tool svg` in 020-style.css is fill: none; stroke: currentColor)."""
    for name in ICONS:
        icon = ran["parts"]["icons"][name]
        assert icon["ariaHidden"] == "true", f"the {name} icon is not aria-hidden"
        assert icon["alt"] is None, f"the {name} icon carries an alt attribute"
        assert (icon["text"] or "").strip() == "", f"the {name} icon has text in it"
        assert icon["currentColor"] is True, (
            f"the {name} icon is not painted in currentColor in its own markup")


def test_the_words_survive_their_icons(ran):
    """The icon is decoration beside the words. The words are still the words."""
    hud = ran["parts"]["hud"]
    assert hud["gold"] == "5 gold"
    assert "Health" in hud["hp"]
    assert hud["menuOpen"] == "Menu"
    # The same page with no skin says exactly the same things: the icons changed
    # nothing about the text.
    plain = ran["plain"]["hud"]
    assert plain["gold"] == hud["gold"]
    assert plain["hp"] == hud["hp"]
    assert plain["menuOpen"] == hud["menuOpen"]


def test_the_bag_icon_is_not_a_child_of_the_bag_strip(ran):
    """One thing carried is one pip in the strip - the same count
    tests/test_combat_loop.py pins on a no-skin pack. The icon is beside the
    strip, never one of the things in it."""
    hud = ran["parts"]["hud"]
    assert hud["bagChildren"] == 1, hud["bagChildTags"]
    assert "svg" not in hud["bagChildTags"]
    assert ran["plain"]["hud"]["bagChildren"] == 1
    assert ran["parts"]["icons"]["bag"]["inside"] is False


def test_a_speaker_with_a_picture_gets_a_decorative_portrait(ran):
    """A speech box shows a portrait when the speaker has one. It is
    decoration: the speaker's name is already real text in .speaker."""
    box = ran["parts"]["npcBox"]
    assert box["error"] is None, box["error"]
    shown = box["withPortrait"]
    assert shown["hidden"] is False
    assert shown["speaker"] == "marta"
    assert shown["images"] == 1, (
        f"the speech box draws no portrait for a speaker the pack gave a picture: "
        f"{shown['children']}")
    assert shown["srcs"] == [box["expectedSrc"]], shown["srcs"]
    assert shown["alts"] == [""], shown["alts"]
    assert shown["ariaHidden"] == ["true"], shown["ariaHidden"]


def test_a_speaker_with_no_picture_gets_no_portrait_slot(ran):
    """And no empty one, and no broken one: a speaker the pack gave no picture
    leaves the box exactly as it is, including after a speaker who had one."""
    box = ran["parts"]["npcBox"]
    assert box["error"] is None, box["error"]
    shown = box["withoutPortrait"]
    assert shown["speaker"] == "nobody"
    assert shown["images"] == 0, f"a portrait with no picture is still a portrait: {shown}"
    assert shown["srcs"] == []
    assert shown["portraitSlots"] == 0
    assert shown["children"] == ["p#npc-name", "p#npc-line", "p#npc-note", "button#npc-close"]


def test_the_three_argument_call_still_works(ran):
    """showSpeech(speaker, line, note) is what every player path calls
    (tests/fixtures/overlay_interact_harness.mjs calls it with three arguments).
    The third argument is still the note, and nothing else is now required."""
    for page in ("parts", "plain"):
        box = ran[page]["npcBox"]
        assert box["error"] is None, f"{page}: {box['error']}"
        for half, who in (("withPortrait", "marta"), ("withoutPortrait", "nobody")):
            shown = box[half]
            assert shown["hidden"] is False, f"{page}/{half}"
            assert shown["speaker"] == who
            assert shown["line"].startswith("A line from ")
            assert shown["noteHidden"] is True


def test_a_page_with_no_skin_has_no_icons_and_no_portrait(ran):
    """The icons belong to a skin: a pack with no skin plays exactly as it did."""
    for name in ICONS:
        assert ran["plain"]["icons"][name]["count"] == 0, name
    assert ran["plain"]["npcBox"]["withPortrait"]["images"] == 0


def test_a_pack_with_no_skin_gains_no_element_of_any_kind(ran):
    """No style element, no has-skin class, no icon, no portrait, and the HUD
    row is the row the shell builds."""
    plain = ran["plain"]
    assert plain["hasStyle"] is False and plain["css"] == ""
    assert "has-skin" not in (plain["bodyClass"] + " " + plain["htmlClass"])
    assert plain["hud"]["hudTlChildren"] == [
        "hud-hp", "hud-level", "hud-gold", "bag-strip", "light-live"]
    assert plain["hud"]["bagChildren"] == 1
    assert plain["npcBox"]["withPortrait"]["children"] == [
        "p#npc-name", "p#npc-line", "p#npc-note", "button#npc-close"]
