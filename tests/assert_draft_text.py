"""Assert the pack's unapproved text is marked, and stays in the inventory.

cottage#159: `DEMO.md` told players every name and line was an unapproved
draft, while `vefr check --release` said "no drafts - every word in this pack
is approved", because nothing in the pack carried `status: draft`. Rylee's
decision (2026-10-16, cottage#159) was to mark the drafts rather than soften
`DEMO.md`, so the release check's list is the approval queue.

This is the repo-local half of that gate, in the shape of
`assert_chest_drops.py`: stdlib only, no VEFR checkout, safe to run in CI.

  1. Every book in the pack's `library/` carries `status: draft` in its front
     matter. A missing status means a new book would ship unmarked; a status
     other than `draft` means something wrote `approved`, which no agent may
     do (AGENTS.md: Rylee writes the stories).
  2. `docs/plans/release-1-0/DRAFT-TEXT.md` names every text-bearing pack
     file, and names nothing that is not there. A book, a voice, a contract or
     a Section that joins the pack without being inventoried would otherwise
     become unapproved player-facing text nobody is tracking.

The engine's own `vefr check --release` is not run here: it needs a VEFR
checkout, which a bare worker worktree does not have. This checks the same
inventory the release check reads, from this side.

usage: python3 tests/assert_draft_text.py [REPO_ROOT]
"""
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent)
pack = root / "worlds" / "cottage-of-the-breeze"
if not pack.is_dir():                      # tolerate being handed the pack itself
    pack = root
inventory = root / "docs" / "plans" / "release-1-0" / "DRAFT-TEXT.md"

bad = []


def front_matter(path):
    """A pack text record's leading `---` block, as a key -> value dict.

    Values are kept as written; a list like `at: [8, 16]` stays one string,
    which is all this check needs to read.
    """
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 3)
    if end < 0:
        return None
    fields = {}
    for line in text[4:end].splitlines():
        if ":" in line and not line.startswith((" ", "\t", "-")):
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip()
    return fields


# 1. Every book is a marked draft, and nothing else wrote a status.
books = sorted((pack / "library").glob("*.md")) if (pack / "library").is_dir() else []
marked = 0
for book in books:
    fields = front_matter(book)
    if fields is None:
        bad.append(f"{book.name}: no front matter, so it cannot carry a status")
        continue
    if "status" not in fields:
        bad.append(f"{book.name}: no 'status' in front matter (cottage#159: unapproved text is a draft)")
    elif fields["status"] != "draft":
        bad.append(f"{book.name}: status is {fields['status']!r}; only Rylee may approve text")
    else:
        marked += 1

# 2. The inventory names every text-bearing pack file, and only real ones.
pack_files = {
    pack / "world.json",
    pack / "blueprint.json",
    pack / "logbok.md",
    pack / "ledger.md",
    pack / "map.md",
    pack / "EDITS.md",
}
for pattern in ("library/*.md", "acts/*/world.json", "acts/*/*/contract.json",
                "acts/*/*/voices/*.md", "sections/*.json"):
    pack_files.update(pack.glob(pattern))

pack_files = {p for p in pack_files if p.is_file()}

if not inventory.is_file():
    bad.append(f"missing {inventory.relative_to(root)} (the cottage#159 draft-text inventory)")
    named = set()
else:
    text = inventory.read_text(encoding="utf-8")
    # Only full pack-relative paths to files in backticks are inventory
    # entries; a bare filename in prose, or a directory such as
    # `worlds/cottage-of-the-breeze/library/`, is not.
    named = {root / m for m in re.findall(r"`(worlds/cottage-of-the-breeze/[\w./-]+\.\w+)`", text)}

for path in sorted(pack_files - named):
    bad.append(f"{path.relative_to(root)}: unapproved text the inventory does not name")
for path in sorted(named - pack_files):
    bad.append(f"{inventory.relative_to(root)}: names {path.relative_to(root)}, which is not in the pack")

print(f"books marked status: draft: {marked} of {len(books)}")
print(f"pack text files inventoried: {len(named & pack_files)} of {len(pack_files)}")

if bad:
    print("\nFAIL")
    for line in bad:
        print("  -", line)
    raise SystemExit(1)
print("\nok: every book is a marked draft and the inventory names every text file in the pack")