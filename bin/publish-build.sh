#!/usr/bin/env bash
# Weave the current pack into one offline HTML file and post it to the dev gallery.
#   usage: bin/publish-build.sh        (build is named for the checked-out HEAD's short sha)
# Needs this machine's ssh key accepted by the gallery stage host (added 2026-10-02).
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel)"
PACK="$ROOT/worlds/cottage-of-the-breeze"
SHA="$(git -C "$ROOT" rev-parse --short HEAD)"
OUT="$(mktemp -d)"
trap 'rm -rf "$OUT"' EXIT
( cd ~/code/Rylee-Bee/vefr && uv run python -c "
import sys; from pathlib import Path; from vefr import cli
Path(sys.argv[2], 'index.html').write_text(cli.weave_html(Path(sys.argv[1])))" "$PACK" "$OUT" )
GALLERY_BY=claude ~/.agents/bin/gallery build cottage-of-the-breeze "$OUT" --sha "$SHA"
