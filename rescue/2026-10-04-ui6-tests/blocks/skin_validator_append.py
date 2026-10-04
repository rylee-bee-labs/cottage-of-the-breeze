

# ---- interface slice 4: the nine parts the player used to ship and ignore ----
# design/ui-skin.md draws these in Cottage's skin, maplab.SKIN_PARTS already
# accepts them and the baker already inlines their picture keys, so the fixture
# skin carries one of each. Nothing in the engine needs to change to accept a
# part; the part still has to be painted, which is the test at the end of this
# file.

SLICE_4_PARTS = ("slot", "tab", "toggle", "tooltip", "speech",
                 "divider", "banner", "corner", "gold-plate")


def test_every_part_of_interface_slice_4_is_a_part_the_validator_accepts():
    for part in SLICE_4_PARTS:
        assert part in maplab.SKIN_PARTS, part
    # and nothing new crept in: the table is exactly the thirteen parts the
    # design note names (four drawn, nine not, and the backdrop).
    assert set(maplab.SKIN_PARTS) == {
        "panel", "button", "tab", "toggle", "bar", "slot", "speech", "tooltip",
        "gold-plate", "divider", "banner", "corner", "cursor", "backdrop"}


def test_a_skin_carrying_every_part_validates(tmp_path):
    pack = mk.build_parts(tmp_path)
    assert errors(pack) == []


def test_the_baker_inlines_every_picture_of_every_part(tmp_path):
    """Each part's picture keys (file, hover, selected, on, off) become data
    URIs; `slice` is carried through as written."""
    baked = json.loads(_baked(cli.weave_html(mk.build_parts(tmp_path))))
    for part, spec in mk.PARTS_SKIN.items():
        assert part in baked["parts"], part
        for key, value in spec.items():
            if key == "slice":
                assert baked["parts"][part][key] == value
                continue
            assert baked["parts"][part][key].startswith("data:image/png;base64,"), (
                f"{part}.{key} is not baked")
    assert "http://" not in _baked(cli.weave_html(mk.build_parts(tmp_path / "again")))


def test_a_missing_state_picture_is_refused_by_name(tmp_path):
    """The states are pictures too: a `tab` that names a `selected` picture
    which is not there is refused the same way a part's `file` is."""
    skin = copy.deepcopy(mk.ALL_SKIN)
    skin["parts"]["tab"]["selected"] = "not-here.png"
    assert has(errors(mk.build(tmp_path, skin=skin, files=mk.ALL_FILES,
                               colours=mk.PARTS_COLOURS)),
               "tab", "not-here.png")


@pytest.fixture(scope="module")
def parts_page(tmp_path_factory):
    """The woven player with a skin carrying every part, played in jsdom."""
    if shutil.which("node") is None:
        pytest.skip("node not installed")
    home = tmp_path_factory.mktemp("skin-parts-validate")
    page = home / "parts.html"
    page.write_text(cli.weave_html(mk.build_parts(home)), encoding="utf-8")
    run = subprocess.run(
        ["node", str(ROOT / "tests/fixtures/skin_apply_harness.mjs"),
         "parts", str(page)],
        capture_output=True, text=True, timeout=240)
    assert run.returncode == 0, run.stderr + run.stdout
    return json.loads(run.stdout)["parts"]


def test_every_part_the_validator_accepts_is_a_part_the_player_draws(parts_page):
    """A part the validator accepts but the player ignores is a picture a pack
    ships and nobody ever sees. The validator's table is the list here, so a
    part added to SKIN_PARTS has to be drawn or this test says so."""
    css = parts_page["css"]
    bodies = re.findall(r"([^{}]*)\{([^{}]*)\}", css)
    missing = []
    for part in maplab.SKIN_PARTS:
        if part == "backdrop":
            continue                     # its own page; see test_skin_apply.py
        uris = [mk.picture_uri(fname) for fname in _pictures_of(part)]
        if not any(uri in body for _sel, body in bodies for uri in uris):
            missing.append(part)
    assert not missing, (
        "these parts validate and bake, but the player writes no rule that "
        f"draws them: {', '.join(missing)}")


def _pictures_of(part):
    """The fixture picture names of a part, if it is one the fixture carries."""
    spec = mk.ALL_SKIN["parts"].get(part) or mk.PARTS_SKIN.get(part)
    if part == "panel":
        return ["panel.png"]
    if part == "button":
        return ["button.png", "button-hover.png", "button-pressed.png"]
    if part == "bar":
        return ["bar-frame.png", "bar-fill.png"]
    if part == "cursor":
        return ["cursor.png"]
    return [f for f in (spec or {}).values() if isinstance(f, str)]
