# CURRENT — Cottage of the Breeze

**Stage: playable prototype with the new look** (2026-10-02). Six rooms, seven residents, five monsters with art, six fogged cellar floors (floors 4-6 are the deeper zone, generated and plain-looking), a trader, notes and a chest, all in one offline HTML file (`DEMO.md` tells a player how to play it). The pack validates (`norns validate`, checked against VEFR `main` 947eec0). The art tools have tests (`art/tests/`).

**Engine, now in VEFR `main`:** the rules engine (eleven events: starts, enters, comes-near, opens, picks-up, defeats, buys, sells, reads, phase-changes, uses-with), `keep` items, the Why-did-that-happen and Where-next panels. See `../vefr/docs/guides/rules.md`. Cottage declares two rules so far (`the-letter-read`, `the-keeper-knows`; the letter in the chest, then the Spell Keeper).

**Not in the engine yet:** XP and levels, equipment slots (`design/equipment.md`, proposed), random floors (`design/random-floors.md`, proposed). Rylee wants classic XP and learn-by-doing both built as neutral VEFR capabilities, with Cottage using classic XP (2026-10-02).

**The one next step:** play the letter -> Keeper moment, then growth (`../vefr/design/growth.md`, PR #194, proposed). Plan: `docs/GAME-PLAN.md`; story passes: `docs/story-spine-notes.md`; decisions: `NOTES.md` (newest first).
