#!/bin/bash
# codex_batch.sh: make several pictures in ONE Codex call and save them with a credits line.
#
#   codex_batch.sh OUTDIR NAME COUNT "BRIEF" [REFERENCE_IMAGE ...]
#
# Why one call: Codex bills a single image per tool call, so asking for COUNT variations in one
# request is cheaper (measured 2026-10-01: 2 images in one call used about 40% fewer tokens per
# image than 2 separate calls). Run it on the machine where `codex login status` says you are
# logged in. Output: OUTDIR/NAME_v1.png ... NAME_vN.png plus NAME_vN.credits.txt for each.
# Env: CODEX_IMAGE_DIR (default ~/.codex/generated_images), ART_TOOL (credits text).
set -euo pipefail
[ $# -ge 4 ] || { sed -n '2,12p' "$0"; exit 2; }
OUT=$1; NAME=$2; N=$3; BRIEF=$4; shift 4
GI=${CODEX_IMAGE_DIR:-$HOME/.codex/generated_images}
TOOL=${ART_TOOL:-Codex CLI built-in image generation (batched call)}
mkdir -p "$OUT"
REFS=(); for r in "$@"; do REFS+=(-i "$r"); done
before=$(find "$GI" -type f -name '*.png' 2>/dev/null | sort || true)
LOG="$OUT/${NAME}_batch.log"
timeout 900 codex exec "Use your built-in image generation tool to create exactly $N separate images in this single request (generate them together, do not stop after the first). They are $N different variations of the same brief. Brief for each image: $BRIEF Reply with only the word DONE." \
  --skip-git-repo-check -s read-only "${REFS[@]}" > "$LOG" 2>&1 < /dev/null || true  # </dev/null: otherwise codex waits on stdin ("Reading additional input from stdin") until the timeout
new=$(comm -13 <(echo "$before") <(find "$GI" -type f -name '*.png' | sort) || true)
got=$(echo "$new" | grep -c . || true)
tokens=$(grep -i 'tokens used' -A1 "$LOG" | tail -1 || true)
echo "$NAME: asked $N, got $got, tokens $tokens"
[ "$got" -eq "$N" ] || echo "WARNING: expected $N images, saved $got. Check $LOG." >&2
# The credits line names each reference from the repo root, so it stays
# readable (and distributable) off the machine that drew the picture. A
# reference that is not in the repo - a session scratch image under /tmp, say -
# is not kept, so the line says "session scratch; not retained" instead of a
# path only that machine could resolve.
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
CREDITS=""
for ref in "$@"; do
  case $ref in
    "$ROOT"/*) rel=${ref#"$ROOT"/} ;;
    /*) rel="" ;;
    *) rel=$ref ;;
  esac
  if [ -n "$rel" ] && [ -e "$ROOT/$rel" ]; then
    CREDITS="${CREDITS:+$CREDITS }$rel"
  else
    CREDITS="${CREDITS:+$CREDITS }session scratch; not retained"
  fi
done
i=1
for f in $new; do
  cp "$f" "$OUT/${NAME}_v$i.png"
  printf '%s_v%s.png · Rylee and Claude · tool: %s · references: %s · prompt: %s · %s · status: draft (not approved)\n' \
    "$NAME" "$i" "$TOOL" "${CREDITS:-none}" "$BRIEF" "$(date +%F)" > "$OUT/${NAME}_v$i.credits.txt"
  i=$((i+1))
done
