# Words, batch 1: the cellar's RPG core

**Status: draft, every word on this page.** Rylee's rule (2026-10-29, answer
14): "I draft, you approve batches". Claude drafted these for the Gate 1 cellar
build; Rylee keeps, edits or bins each one in one sitting. Until then they ship
only in the draft build, and `DEMO.md` already tells players every word is a
draft. Nothing here changes an existing word.

Mark each line **keep**, **edit: …** or **bin**. A bin with no replacement
removes the thing (a trait or a spell) rather than leaving a hole.

## Trait words (found on gear, read by the Spell Keeper)

A rolled piece of gear bears 0 to 3 of these, by rarity (common 0, fine 1, rare
2, heroic 2, mythic 3). Each is one plain word the bag prints after "traits:".

| Word | What it does | Where it rolls | Draft reason |
|---|---|---|---|
| keen | +1 Attack | hand | the plainest sharp word |
| sturdy | +1 Guard | body, head, feet | armour, said kindly |
| hale | +2 Health | body, head, feet | old word for healthy |
| deep | +2 Mana | head, charm | a well of it |
| lucky | +6% critical hits | hand, feet, charm | |
| warming | a kill restores 1 health | hand, charm | canon: what you carry up is heat |
| eager | the first blow on an unhurt foe is doubled | hand, charm | |
| thorned | a foe that hits you takes 1 | body, charm | cellar brambles and roots |
| reckless | +3 Attack, but each miss stings you for 1 | hand, charm | **a curse** (shows "(cursed)") |
| brittle | +2 Attack, but -2 Health | body | **a curse** (shows "(cursed)") |

## Spells (learned by level)

| Id | Name the player reads | School | Learned at | Cost | Does |
|---|---|---|---|---|---|
| ember-flick | a flick of ember | ember | level 2 | 2 mana | 3 harm to a foe within 5 tiles, past guard |
| hearth-ward | a hearth ward | hearth | level 3 | 2 mana | +2 Guard for 3 turns |
| warm-hands | warm hands | hearth | level 4 | 3 mana | heals 4 |

The two school words, **ember** and **hearth**, are drafts too: the bag prints
them beside each spell's name. Both lean on canon's heat ("What you are carrying
up is heat") and the Spell Keeper's cake.

## The fight row

| Button | Word | Note |
|---|---|---|
| attack | **Strike** | the engine's own word, now named by the pack |
| cast | **Cast** | shows only once a harmful spell is known |

## Engine sentences the player now reads

These are VEFR's own defaults (ADR 0021), not pack words. A pack may replace
any of them through `player_words`; listed so nothing is a surprise:

- "You miss {foe}." / "A clean hit! You hit {foe} for {n}."
- "{foe} misses you." / "A heavy blow! {foe} hits you for {n}."
- "You find {n} gold."
- "{item} warms you: you recover {n} health." / "{item} stings you for {n}." /
  "{item} bites back for {n}." / "{item} makes the first blow count."
- "You wake, whole again. What you carried waits where you fell."
- "What you carried waits on this floor." / "You find your satchel. Everything
  you carried is back."
- "You rest. You are whole again."
- "Not enough mana for {spell}: it needs {n} and you have {m}."

## Already approved, reused here (not part of this batch)

- The rarity words **common, fine, rare, heroic, mythic** (DESIGN.md, decided
  2026-10-08).
- Every item name, keepsake name and resident line: unchanged, word for word.
