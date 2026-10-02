#!/usr/bin/env bash
# Weave the current pack into one offline HTML file and post it to the dev gallery.
# The dev VM's ssh key is not accepted by the gallery stage host; Bazzite's is,
# so the finished file is copied to Bazzite and published from there.
#   usage: bin/publish-build.sh            (uses the checked-out HEAD's short sha)
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel)"
PACK="$ROOT/worlds/cottage-of-the-breeze"
SHA="$(git -C "$ROOT" rev-parse --short HEAD)"
OUT="$(mktemp -d)"
trap 'rm -rf "$OUT"' EXIT
( cd ~/code/Rylee-Bee/vefr && uv run python -c "
import sys; from pathlib import Path; from vefr import cli
Path(sys.argv[2], 'index.html').write_text(cli.weave_html(Path(sys.argv[1])))" "$PACK" "$OUT" )
REMOTE="\$HOME/.cache/cottage-publish/$SHA"
ssh bazzite "mkdir -p $REMOTE"
scp -q "$OUT/index.html" "bazzite:.cache/cottage-publish/$SHA/index.html"
ssh bazzite "GALLERY_BY=claude \$HOME/.agents/bin/gallery build cottage-of-the-breeze $REMOTE --sha $SHA"
