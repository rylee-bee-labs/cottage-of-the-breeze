# CURRENT — Cottage of the Breeze

**Stage: playable prototype with the new look** (2026-10-02). Six rooms, seven residents, five monsters with art, three fogged cellar floors, a trader, notes and a chest, all in one offline HTML file (`DEMO.md` tells a player how to play it). The pack validates (`norns validate`, checked against VEFR `main` 947eec0). The art tools have tests (`art/tests/`).

**Engine, now in VEFR `main`:** the rules engine (eleven events: starts, enters, comes-near, opens, picks-up, defeats, buys, sells, reads, phase-changes, uses-with), `keep` items, the Why-did-that-happen and Where-next panels. See `../vefr/docs/guides/rules.md`. **Cottage declares no rules yet** (`world.json` has none).

**Not in the engine yet:** XP and levels, equipment slots (`design/equipment.md`, proposed), random floors (`design/random-floors.md`, proposed). Rylee wants classic XP and learn-by-doing both built as neutral VEFR capabilities, with Cottage using classic XP (2026-10-02).

**The one next step:** wire the first reactions (the letter, then the Keeper), and design growth with Rylee. Plan: `docs/GAME-PLAN.md`; story passes: `docs/story-spine-notes.md`; decisions: `NOTES.md` (newest first).
