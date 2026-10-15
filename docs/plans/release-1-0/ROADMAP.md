# Cottage of the Breeze 1.0: finish-line roadmap

**Proposed for owner review:** 2026-10-14  
**Owner decisions:** [Cottage #168](https://github.com/rylee-bee-labs/cottage-of-the-breeze/issues/168)  
**VEFR engine dependency:** [VEFR #489](https://github.com/rylee-bee-labs/vefr/issues/489)  
**Planning rule:** This is a delivery plan, not a declaration that features are built or that draft story/art is approved. The [canonical story](../../story/STORY.md) remains authoritative. This roadmap does not change story canon, assets, gameplay code or the current shipped beta.

## The promise to the player

A complete browser-first, four-Section (36-floor) turn-based story dungeon crawler with a real ending, heavily procedural floors, classless character progression, meaningful enchanted loot and spells, an evolving home and town, and approachable tactical encounters. Exploration remains curious, playful and low-bandwidth. Aim for **25+ hours of enjoyable story/exploration content**, including optional discovery and replay, **without padding or mandatory grinding**. Duration is a *target*, not a measured claim.

### Locked 1.0 gameplay boundaries

- **Persistent adventurer:** earned equipment, spells, levels, discoveries, story choices and town improvements stay. Death returns the player to town; dropped resources are recoverable. Death must not delete progression.
- **Temporary chaos:** an expedition may grant Wind blessings and temporary floor rules; these **move on** when that expedition ends, not when a save is made. Item ownership persists even if its temporary modifiers change.
- **Tactical, not frantic:** active turn-based movement/attacks/spells and passive gear reactions; readable, bounded combination chains; lucky overpowered builds are allowed.
- **Procedural, not arbitrary:** varied layouts, monsters, loot and secrets with guaranteed traversable story anchors and repeatable seed tests.
- **Winds, not a new genre:** Breeze, Gust, Gale, Squall and Tempest are distinct generator patterns; a rare whimsical Zephyr can visit. Pick an *unlocked dominant Wind* before a descent; a *passing Wind* can briefly change a floor. Winds are **not** plain difficulty tiers. Unlock timing can be chosen as a narrow implementation decision without adding another interview round.
- **One main story:** optional discoveries and kindness can change NPC dialogue, town and ending details; no branching-campaign rewrite.
- **Device target:** works on desktop and mobile browsers using keyboard, mouse and touch. Installable web app support is best effort unless effortless within existing architecture.

## Baseline: what is actually known

- The repository's current orientation file, [.project/CURRENT.md](../../../.project/CURRENT.md), calls it **Section 1 beta**. This is a useful intermediate gate, **not the newly agreed 1.0 ship scope**. Updating that router to a later milestone requires verified evidence, not wishful status changes.
- Four nine-floor Section definitions exist: Cellar, Rootworks, Siltworks, Emberhall. Existence is not evidence that all four narrative arcs, item/build depth or the full playthrough work.
- On 2026-10-13 the documented bot reported **40/40 checks on desktop and phone viewports** for Section 1. [Playthrough documentation](../../../tests/playthrough/README.md) explains that the standard full traversal removes monsters and then tests a fight separately; the **--monsters** option is required to establish real combat-filled travel.
- Full human Section 1 playthrough and a physical-device mobile pass are still open: [#161](https://github.com/rylee-bee-labs/cottage-of-the-breeze/issues/161), [#157](https://github.com/rylee-bee-labs/cottage-of-the-breeze/issues/157).
- Existing release blockers and owner choices include [#159](https://github.com/rylee-bee-labs/cottage-of-the-breeze/issues/159) (story draft/approval), [#162](https://github.com/rylee-bee-labs/cottage-of-the-breeze/issues/162) (art/status/provenance), [#165](https://github.com/rylee-bee-labs/cottage-of-the-breeze/issues/165) (phone note overlay), [#166](https://github.com/rylee-bee-labs/cottage-of-the-breeze/issues/166) (desktop ending framing) and [#158](https://github.com/rylee-bee-labs/cottage-of-the-breeze/issues/158) (touch tutorial text).
- Do not equate VEFR architecture proposals or previously merged primitives with Cottage integration. Audit actual runtime behavior before marking new work complete.

## One critical path, five quality gates

Each gate is **done only with linked code/pack change, automated evidence, and human review when indicated**. Do not open a parallel mega-backlog.

### Gate 0: Section 1 earns trust

**Cottage:** finish a full real-player run on desktop and an actual phone; address input/overlay/framing issues; run multiple fully populated --monsters descents; validate story ending, safe return home, recovery, readability and no soft locks. Triage current release/art/draft issues rather than silently promoting drafts.

**VEFR:** provide only verified player fixes needed by this gate via [player epic #452](https://github.com/rylee-bee-labs/vefr/issues/452), particularly [device QA #459](https://github.com/rylee-bee-labs/vefr/issues/459), [touch #453](https://github.com/rylee-bee-labs/vefr/issues/453), and save expectations [#456](https://github.com/rylee-bee-labs/vefr/issues/456).

**Exit proof:** a human can complete the nine-floor story Section on supported inputs, with monsters enabled, and report defects with reproducible steps. Current scripted beta evidence is retained, not overstated.

### Gate 1: Prove the RPG/build loop in one Section

**VEFR:** audit existing rarity/affix/identification/spell systems, then fill **only** the missing generic, pack-authored mechanics for meaningful item and spell effects, classless build synergy, bounded passive reactions and safe save semantics. Prefer extending existing code rather than a separate chaos engine. [VEFR Winds/effects epic #489](https://github.com/rylee-bee-labs/vefr/issues/489) owns the gap inventory.

**Cottage:** build a small, replayable item-and-spell matrix in the Cellar: more than one viable build, a useful enchanted find, at least one deliberately exciting chain reaction, and a trustworthy defeat/recovery loop. Distinguish authored expectations from observed balancing.

**Exit proof:** actual combat-driven playthroughs reveal meaningful playstyle variation, and saved/restored and repeated-seed behavior remains consistent. Rarely too-strong is acceptable; infinite loops, unexplainable effects or duplicated loot are not.

### Gate 2: Complete the four-Section adventure

**Cottage:** finish story progression and unique feel across Rootworks, Siltworks and Emberhall, with anchored story beats, distinct inhabitants/encounters and linked return paths. Wire incremental cottage/town services and NPC state changes. Build the four-Section ending without revising the approved Cellar King canon. Track approved vs draft prose and art.

**VEFR:** implement only generic gaps exposed by exercising the four Sections: stable anchors, state transitions, spells/status/combat, recoverable floor-state persistence and accessible controls. Require pack/schema validation and seeded route tests.

**Exit proof:** full 36-floor story from start to final ending is traversable across a documented sample of seeds, including populated combat and returns to town; story/character state survives saves. Human review verifies every story Section and the final ending.

### Gate 3: Add a **small** Windrose, then stop

**VEFR:** one deterministic, versioned modifier/event hook set, scoped to expedition and floor, with safe action reactions and explainable state; no runtime-generated lore or arbitrary scripts. Check current seeded rune/omen implementations before extending them.

**Cottage:** one simple distinguishable core interaction for each named Wind, one optional passing-Wind floor event path, and **a few** rare Zephyr surprises. Keep the unlock mechanism simple and tested. Ensure permanent treasure remains permanent and temporary Wind effects expire only at expedition end.

**Exit proof:** switching dominant Wind changes behavior, passing Wind modifies one floor without breaking story anchors, save/load never rerolls, and item/spell triggers are legible. A player can complete the main story without using the wildest Wind.

**Scope warning:** five names do **not** demand five systems, an enormous affix library, a calendar-driven live service or new quest arcs. Creative extras get parked, not bolted into v1.0.

### Gate 4: Release candidate and public 1.0

**Cottage:** test complete runs, encounter distribution, economy, rewards, pacing, accessibility, clear tutorial/help, real phone and desktop UI, performance and save handling; verify all release-critical text, licenses/art sources and attribution. Confirm how/where to host and distribute a tested build. Maintain the complete story as 1.0 scope.

**VEFR:** reproducible export with pinned VEFR+Cottage revisions; browser compatibility tests, import/export where required, no broken pre-existing games; use [#456](https://github.com/rylee-bee-labs/vefr/issues/456) and [#459](https://github.com/rylee-bee-labs/vefr/issues/459) rather than parallel fixes.

**Exit proof:** published build identity and provenance, tested saves and upgrades, actual mobile/desktop manual play, no release-blocking defects, owner-approved story/assets, complete ending, multi-seed test report, and honest playtime report. **25+ hours is a target to validate through observed play, not a guarantee or reason to pad.**

## Coordination / reporting discipline

- **Cottage issue #168:** immutable-enough *design intent*; change only on explicit owner decision.
- **This roadmap:** **one release critical path**, progress by gates (Not started / Active / Verified / Blocked), each with a concrete issue or PR, test report and evidence link. Do not use unsupported percent-complete estimates.
- **VEFR issue #489:** reusable engine implementation planning and acceptance, not Cottage-specific content.
- Existing GitHub issues remain the work queue. Link them to gates; do not recreate duplicates. A parked idea stays parked unless a measured release problem makes it necessary.
- **Current gate:** Gate 0; Gate 1 is the next substantive integration, contingent on code audit. Later gates are scoped plans, not claims of active implementation.
- No invented deadlines, target dates, coverage claims or sign-off. The owner chooses release when evidence meets Gate 4.

## Explicitly parked until after 1.0

- Endless/post-story dungeon mode and deep ongoing expansions, though the base story is already procedural.
- More than a few rare novelty event chains or a huge Wind effect catalog.
- Full roguelite resets, character classes, permanent permadeath, extensive crafting/farming, major branching questlines and a life-sim layer.
- Native app/storefront launch packaging, elaborate multiplayer/online seasons, server-driven daily randomization or required live services.
- More art systems, UI redesigns or engine abstractions **solely** for their own sake.

These are **not rejected ideas**, simply not allowed to delay the finished four-Section adventure.

## First execution packet

1. Preserve current beta evidence and resolve/triage [Cottage #161](https://github.com/rylee-bee-labs/cottage-of-the-breeze/issues/161), [#157](https://github.com/rylee-bee-labs/cottage-of-the-breeze/issues/157), [#165](https://github.com/rylee-bee-labs/cottage-of-the-breeze/issues/165), and [#166](https://github.com/rylee-bee-labs/cottage-of-the-breeze/issues/166) using device evidence.
2. Complete the [VEFR #489](https://github.com/rylee-bee-labs/vefr/issues/489) **code-level capability map** before adding effects or Winds; link existing PRs/ADRs and label each capability Built / Partial / Missing / Unverified.
3. Make one thin Cellar integration of mechanical loot, spells and bounded reactions; test with --monsters and save/resume.
4. Reconcile [#159](https://github.com/rylee-bee-labs/cottage-of-the-breeze/issues/159) and [#162](https://github.com/rylee-bee-labs/cottage-of-the-breeze/issues/162) before any 1.0 story/asset promotion.
5. Only then fan out the other three Sections and the minimal Winds layer.

**Success:** a complete, polished, pleasantly surprising game that invites one more descent. Not the largest roadmap we can write.
