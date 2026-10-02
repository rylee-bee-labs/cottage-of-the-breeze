# 10 · Cottage proof (Codex probes, reverified)

Codex ran the probes at VEFR `649034f` against this pack. I reran them on 2026-10-02 from a scratch worktree; evidence went to the scratchpad, never the repo, and this pack was not modified (`git status` clean).

## Commands and observed output

```
uv run --group test pytest -q experiments/language-proof/test_prototype.py
  9 passed in 0.43s

uv run --group test python experiments/language-proof/run.py \
  --pack .../cottage-of-the-breeze/worlds/cottage-of-the-breeze \
  --region floor-2 --sprite shade --rule the-keeper-knows --out <scratchpad>
  real family exact equality + current validation: PASS
  real rule exact equality + validator + engine + DOM + reload comparison: PASS
  floor repeat/dressing independence/reachability: PASS
```

## What each probe shows on this pack

- **A, families:** the three `floor-2` shades expand exactly from one family plus instances. The repeated scalars are `name, sprite, hp, atk, xp` x two extra copies = 10 occurrences removed (derived from the table in `02`). Current validation accepts the result.
- **B, rules:** `the-keeper-knows` lowers to identical rule JSON and behaves identically in the shipped engine and woven-player DOM, including `once`, ordering, state, speech and why. `the-letter-read` was **not** run: `UNVERIFIED`.
- **C, floors:** unchanged `generate_floor_v2`; separate layout and dressing seeds; stairs reachable; impossible placement and unsupported controls fail. The ending was synthetic because no authored ending room exists in this pack.

## Pre-existing finding

The WHY log survives a reload; rule flags and `once` markers do not. Reproduced in both representations, so it is engine behavior, not the experiment.

## Fit

Cottage's creature records are the one place the layer clearly shrinks the pack. Its two rules and growth table need no change. A first Cottage migration step, if authorized, is creature families only, behind byte-equality fixtures against today's contracts.
