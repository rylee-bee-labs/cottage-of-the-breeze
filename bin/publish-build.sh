#!/usr/bin/env bash
# Weave the current pack into one offline HTML file and post it to the dev gallery.
#   usage: bin/publish-build.sh        (build is named for the checked-out HEAD's short sha)
# Needs this machine's ssh key accepted by the gallery stage host (added 2026-10-02).
# VEFR_DIR picks the VEFR checkout that weaves it (default ~/code/Rylee-Bee/vefr). ~/.agents/bin/publish-build
# sets it to VEFR's origin/main, so a coordinator's build is exactly what merged (Rylee, 2026-10-09).
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel)"
PACK="$ROOT/worlds/cottage-of-the-breeze"
SHA="$(git -C "$ROOT" rev-parse --short HEAD)"
VEFR="${VEFR_DIR:-$HOME/code/Rylee-Bee/vefr}"
OUT="$(mktemp -d)"
trap 'rm -rf "$OUT"' EXIT
chmod 755 "$OUT"   # mktemp makes 0700; the gallery copies the mode and nginx then cannot read it
( cd "$VEFR" && uv run python -c "
import sys; from pathlib import Path; from vefr import cli
Path(sys.argv[2], 'index.html').write_text(cli.weave_html(Path(sys.argv[1])))" "$PACK" "$OUT" )
# Reproducibility (#75): record exactly which engine and pack revisions made this file.
VEFR_SHA="$(git -C "$VEFR" rev-parse --short HEAD)"
VEFR_DIRTY="$(git -C "$VEFR" status --porcelain --untracked-files=no | wc -l)"
printf 'cottage-of-the-breeze %s\nvefr %s (uncommitted changes: %s)\n' "$SHA" "$VEFR_SHA" "$VEFR_DIRTY" > "$OUT/build-info.txt"
echo "build: cottage $SHA, vefr $VEFR_SHA"
GALLERY_BY=claude ~/.agents/bin/gallery build cottage-of-the-breeze "$OUT" --sha "$SHA"
