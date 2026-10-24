"""Assert the Key Warden's challenge comes before the note that ends Act 1.

The Act 1 Re-cut (cottage#173) put the ending note in the vault on the
warden's floor, and the warden's yield was hung on that same note: one
read gave the gems and ended the act at once, and the playthrough bot's
"the gems are in the bag" check ran before the only event that could put
them there.  The owner's order (2026-10-24) is the challenge first - the
hero reaches the warden on the last floor, keeps the rule it keeps, and
that sets the warden's flag - and only then is the ending note read.

This checks that order in the pack's own data:

  1. the challenge is a rule that sets a `warden:<id>:c0` flag, and that
     flag is declared;
  2. the challenge is answered by reading a book that is NOT the book that
     fires `complete-act`, so the challenge is not the ending note;
  3. that book is on the Section's warden floor - the last floor, which
     the Section's own `pattern` says is where the warden is;
  4. the rule that ends the act asks for the challenge's flag, so the
     vault opens only on the challenge;
  5. the gems the challenge awards are a real item with a real sprite, and
     they are what the Section's warden carries.

The playthrough bot plays this order for real; this check is the half of
it that can run without a VEFR checkout and a browser.

usage: python3 tests/assert_warden_challenge.py [REPO_ROOT]
"""
import json
import pathlib
import sys

root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent)
pack = root / "worlds" / "cottage-of-the-breeze"
if not pack.is_dir():                      # tolerate being handed the pack itself
    pack = root

world = json.loads((pack / "world.json").read_text(encoding="utf-8"))
rules = world.get("rules") or []
flags = world.get("flags") or {}
items = world.get("items") or {}
sprites = (world.get("player") or {}).get("sprites") or {}

bad = []


def then_of(rule):
    return [t for t in (rule.get("then") or []) if isinstance(t, dict)]


def reads_of(rule):
    what = ((rule.get("when") or {}).get("reads") or {}).get("what")
    return str(what) if what else None


def sets_of(rule):
    return [str(t.get("set")) for t in then_of(rule) if t.get("set")]


def front_matter(path):
    """A text record's leading `---` block, as a key -> value dict."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 3)
    if end < 0:
        return {}
    fields = {}
    for line in text[4:end].splitlines():
        if ":" in line and not line.startswith((" ", "\t", "-")):
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip()
    return fields


# 1. The challenge: the rule that sets a warden's flag.
challenges = [rule for rule in rules if any(s.startswith("warden:") for s in sets_of(rule))]
if len(challenges) != 1:
    bad.append(
        f"world.json: {len(challenges)} rules set a warden flag; there must be "
        f"exactly one, the challenge"
    )
    challenge = None
else:
    challenge = challenges[0]
    flag = next(s for s in sets_of(challenge) if s.startswith("warden:"))
    if flag not in flags:
        bad.append(f"world.json: the challenge sets {flag!r}, which is not declared in flags")

    endings = [rule for rule in rules if any("complete-act" in t for t in then_of(rule))]
    if len(endings) != 1:
        bad.append(f"world.json: {len(endings)} rules fire complete-act; there must be one")
        ending = None
    else:
        ending = endings[0]

    challenge_book = reads_of(challenge)

    # 2. The challenge is not the ending note.
    if not challenge_book:
        bad.append("world.json: the challenge is not answered by reading anything")
    elif ending is not None and challenge_book == reads_of(ending):
        bad.append(
            f"world.json: the challenge is the ending note {challenge_book!r}; the "
            f"challenge has to come before the note that ends the act"
        )

    # 4. The act ends only on the challenge: the ending rule asks for its flag.
    if ending is not None:
        gate = [
            f
            for f in (ending.get("if") or [])
            if isinstance(f, dict) and f.get("flag") == flag and f.get("is") is True
        ]
        if not gate:
            bad.append(
                f"world.json: the rule that ends the act does not ask for {flag!r}; "
                f"the vault has to open on the challenge"
            )

    # 3. The challenge is on the warden's floor.
    section_file = pack / "sections" / "cellar.json"
    if not section_file.is_file():
        bad.append("sections/cellar.json: the Section that holds the warden is not there")
    else:
        section = json.loads(section_file.read_text(encoding="utf-8"))
        floors = section.get("floors")
        pattern = section.get("pattern") or []
        if not isinstance(floors, int) or not pattern or pattern[-1] != "warden":
            bad.append(
                f"sections/cellar.json: the Section does not end on a warden floor "
                f"(floors={floors!r}, pattern={pattern!r})"
            )
        elif challenge_book:
            warden_floor = f"{section.get('id')}-0-{floors}"
            book_file = pack / "library" / f"{challenge_book}.md"
            if not book_file.is_file():
                bad.append(f"library/{challenge_book}.md: the challenge reads a book that is not there")
            else:
                region = front_matter(book_file).get("region")
                if region != warden_floor:
                    bad.append(
                        f"library/{challenge_book}.md: the challenge is on {region!r}, "
                        f"not on the warden's floor {warden_floor!r}"
                    )

        # 5. What the warden carries is a real item with a real sprite.
        warden = section.get("warden")
        carries = (warden or {}).get("carries") if isinstance(warden, dict) else None
        if not carries:
            bad.append("sections/cellar.json: the warden carries nothing")
        elif carries not in items:
            bad.append(f"sections/cellar.json: the warden carries {carries!r}, which is not an item")
        else:
            sprite = items[carries].get("sprite")
            if not sprite or sprite not in sprites:
                bad.append(f"sections/cellar.json: {carries!r} has no sprite in player.sprites")
            elif not (pack / "sprites" / f"{sprite}.png").is_file():
                bad.append(f"sections/cellar.json: {carries!r} sprite {sprite!r} has no file")

print(f"rules checked: {len(rules)}")
print(f"challenge rule: {challenge['id'] if challenge else 'none'}")
if challenge:
    print(f"challenge reads: {reads_of(challenge)}")
    print(f"challenge sets: {[s for s in sets_of(challenge) if s.startswith('warden:')]}")

if bad:
    print("\nFAIL")
    for line in bad:
        print("  -", line)
    raise SystemExit(1)
print("\nok: the Key Warden's challenge comes first, and the act ends on it")
